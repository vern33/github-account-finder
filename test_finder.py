import base64
import json
import unittest

import finder


class FakeAPI:
    def __init__(self, *, marker=True, photos=True, profile=None, commit=None):
        self.marker = marker
        self.photos = photos
        self.profile = profile or {
            "name": "Nobody",
            "created_at": "2022-08-20T00:00:00Z",
        }
        self.commit = commit or {}

    def request(self, path, **_kwargs):
        if "/git/trees/" in path:
            tree = [{"type": "blob", "path": ".github/workflows/deploy.yml", "sha": "wf"}]
            if self.photos:
                tree.append({"type": "blob", "path": "images/mountain.jpg", "sha": "im"})
            return {"tree": tree, "truncated": False}
        if "/git/blobs/wf" in path:
            text = "uses: actions/deploy-pages" if self.marker else "name: test"
            return {"encoding": "base64", "content": base64.b64encode(text.encode()).decode()}
        if path.startswith("/users/"):
            return self.profile
        if "/commits?" in path:
            return ([{"commit": {"author": self.commit}, "author": None}] if self.commit else [])
        raise AssertionError(path)


def repository(owner):
    return {
        "full_name": f"{owner}/{owner}.github.io",
        "name": f"{owner}.github.io",
        "has_pages": True,
        "owner": {"login": owner, "type": "User"},
        "default_branch": "main",
        "html_url": "https://example.test",
        "created_at": "2022-08-21T00:00:00Z",
        "pushed_at": "2022-10-02T00:00:00Z",
        "homepage": None,
        "description": None,
    }


def project_repository(owner, name="blog"):
    repo = repository(owner)
    repo.update({
        "full_name": f"{owner}/{name}",
        "name": name,
    })
    return repo


class FinderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads(finder.CONFIG_PATH.read_text())

    def test_user_centric_stage_order_and_query(self):
        tasks = finder.seed_search_tasks(self.config)
        self.assertEqual(tasks[0]["stage"], "users")
        self.assertEqual(tasks[0]["term"], "liuxuan")
        self.assertEqual(tasks[1]["term"], "xuanliu")
        stages = [task["stage"] for task in tasks]
        self.assertLess(stages.index("personal"), stages.index("site"))
        self.assertEqual(tasks[-1]["stage"], "site")
        self.assertFalse({task["stage"] for task in tasks} & {"blog", "pages", "other"})
        self.assertNotIn("jesse", self.config["identity"]["name_primary"])
        self.assertNotIn("jesse", self.config["user_search_seeds"])
        self.assertNotIn("xiaxiatian", self.config["user_search_seeds"])
        self.assertIn("xiaoxiatian", self.config["user_search_seeds"])
        self.assertIn("in:login,name", finder.task_query(tasks[0]))

    def test_public_metadata_tokens_are_redacted_recursively(self):
        leaked = "ghp_" + "A" * 36
        fine_grained = "github_pat_" + "B" * 30
        value = {"bio": f"prefix {leaked} suffix", "nested": [fine_grained, 3]}
        safe = finder.redact_secrets(value)
        self.assertNotIn(leaked, json.dumps(safe))
        self.assertNotIn(fine_grained, json.dumps(safe))
        self.assertEqual(safe["bio"], "prefix [REDACTED_GITHUB_TOKEN] suffix")
        self.assertEqual(safe["nested"][1], 3)

    def test_strategy_correction_prunes_orphan_task_without_losing_progress(self):
        state = {
            "adaptive_searches": {
                "old": {
                    "stage": "users", "term": "xiaxiatian",
                    "start": "2022-06-01", "end": "2022-10-15",
                    "order": 12, "page": 1, "complete": True, "split": False,
                },
                "adaptive:users:jessie:2022-06-01:2022-10-15": {
                    "stage": "users", "term": "jessie",
                    "start": "2022-06-01", "end": "2022-10-15",
                    "order": 8, "page": 7, "complete": True, "split": False,
                },
            }
        }
        tasks = finder.initialize_adaptive_tasks(state, self.config)
        self.assertFalse(any(task["term"] == "xiaxiatian" for task in tasks.values()))
        self.assertTrue(any(task["term"] == "xiaoxiatian" for task in tasks.values()))
        kept = next(task for task in tasks.values() if task["term"] == "jessie")
        self.assertEqual(kept["page"], 7)
        self.assertTrue(kept["complete"])

    def test_user_pages_repositories_are_date_filtered_before_inspection(self):
        class RepoListAPI:
            def request(self, path, **_kwargs):
                self.path = path
                return [
                    {"name": "target", "has_pages": True, "created_at": "2022-08-20T00:00:00Z"},
                    {"name": "future", "has_pages": True, "created_at": "2026-01-01T00:00:00Z"},
                    {"name": "not-pages", "has_pages": False, "created_at": "2022-09-01T00:00:00Z"},
                ]

        api = RepoListAPI()
        repositories = finder.get_user_pages_repositories(
            api, "someone", 3, "2022-06-01", "2022-10-15"
        )
        self.assertEqual([repo["name"] for repo in repositories], ["target"])
        self.assertIn("sort=created", api.path)
        self.assertIn("direction=desc", api.path)

    def test_identity_tiers_and_number_boundaries(self):
        self.assertEqual(finder.identity_tier("liuxuan0503", [], [], self.config), 2)
        self.assertEqual(finder.identity_tier("jessie0503", [], [], self.config), 2)
        self.assertEqual(finder.identity_tier("jliu", [], [], self.config), 1)
        self.assertEqual(finder.identity_tier("someone", ["liu"], [], self.config), 1)
        numbers = set(self.config["identity"]["numbers"])
        self.assertTrue(finder.token_matches("0503", "jessie0503", numbers))
        self.assertFalse(finder.token_matches("0503", "jessie105030", numbers))

    def test_identity_and_structural_admission(self):
        strong = finder.inspect_repository(
            FakeAPI(), repository("liuxuan0503"), self.config, {}
        )
        self.assertEqual(strong["identity_tier"], 2)
        fallback = finder.inspect_repository(
            FakeAPI(), repository("randomperson"), self.config, {}
        )
        self.assertEqual(fallback["identity_tier"], 0)
        rejected = finder.inspect_repository(
            FakeAPI(marker=False), repository("randomperson"), self.config, {}
        )
        self.assertIsNone(rejected)

    def test_personal_pages_with_actions_needs_no_detected_photo(self):
        candidate = finder.inspect_repository(
            FakeAPI(marker=True, photos=False),
            repository("randomperson"),
            self.config,
            {},
        )
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate["identity_tier"], 0)
        self.assertEqual(candidate["probable_photo_count"], 0)

    def test_project_pages_with_actions_and_image_is_admitted(self):
        candidate = finder.inspect_repository(
            FakeAPI(marker=True, photos=True),
            project_repository("randomperson", "blog"),
            self.config,
            {},
        )
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate["identity_tier"], 0)
        self.assertFalse(candidate["is_personal_pages"])

    def test_commit_identity_can_admit_candidate(self):
        candidate = finder.inspect_repository(
            FakeAPI(
                marker=False,
                photos=False,
                commit={"name": "Jessie Liu", "email": "jessie@example.com"},
            ),
            repository("randomperson"),
            self.config,
            {},
        )
        self.assertEqual(candidate["identity_tier"], 1)

if __name__ == "__main__":
    unittest.main()

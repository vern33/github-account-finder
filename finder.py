#!/usr/bin/env python3
"""Find a newly-created 2023 GitHub identity and its Pages repositories.

The built-in Actions GITHUB_TOKEN is intentionally used instead of a PAT.
State and candidate reports are committed by the workflow after every run.
"""

from __future__ import annotations

import base64
import datetime as dt
import html
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
STATE_PATH = ROOT / "state.json"
CANDIDATES_PATH = ROOT / "candidates.json"
REPORT_PATH = ROOT / "candidates.md"
PROGRESS_PATH = ROOT / "progress.md"

IMAGE_RE = re.compile(r"\.(?:jpe?g|png|webp|heic)$", re.I)
REAL_PHOTO_RE = re.compile(
    r"(?:^|/)(?:img|images?|photos?|album|gallery|uploads?|assets|static|public|"
    r"source/_posts|content/posts?|posts?)/",
    re.I,
)
NON_PHOTO_RE = re.compile(
    r"(?:favicon|logo|icon|screenshot|screen[-_ ]?shot|banner|avatar|diagram|"
    r"chart|graph|sprite|texture|node_modules|vendor|assets?/icons?)",
    re.I,
)
POST_RE = re.compile(
    r"(?:^|/)(?:_posts|source/_posts|content/posts?|posts?|blog)/.*\.(?:md|markdown|html)$",
    re.I,
)
WORKFLOW_RE = re.compile(r"^\.github/workflows/.*\.ya?ml$", re.I)


class BudgetExhausted(RuntimeError):
    pass


class GitHub:
    def __init__(self, token: str, budget: int):
        self.token = token
        self.budget = budget
        self.used = 0
        self.search_last = 0.0
        self.core_last = 0.0

    def request(self, path: str, *, search: bool = False, accept: str | None = None):
        if self.used >= self.budget:
            raise BudgetExhausted
        if search:
            # User/repository search allows 30 requests/minute. Staying below it
            # also reduces secondary-limit risk.
            delay = 2.2 - (time.monotonic() - self.search_last)
            if delay > 0:
                time.sleep(delay)
        else:
            # Stay below the documented secondary REST point ceiling instead
            # of bursting tree/profile/commit requests back-to-back.
            delay = 0.1 - (time.monotonic() - self.core_last)
            if delay > 0:
                time.sleep(delay)
        url = path if path.startswith("https://") else f"https://api.github.com{path}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {self.token}")
        req.add_header("Accept", accept or "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "vern33-github-account-finder")
        for attempt in range(4):
            try:
                self.used += 1
                with urllib.request.urlopen(req, timeout=30) as response:
                    if search:
                        self.search_last = time.monotonic()
                    else:
                        self.core_last = time.monotonic()
                    return json.load(response)
            except urllib.error.HTTPError as exc:
                if exc.code in (403, 429):
                    reset = exc.headers.get("x-ratelimit-reset")
                    remaining = exc.headers.get("x-ratelimit-remaining")
                    if remaining == "0":
                        raise BudgetExhausted(f"rate limit reset={reset}") from exc
                    wait = int(exc.headers.get("retry-after", "60"))
                    time.sleep(min(wait, 120))
                    continue
                if exc.code in (404, 409, 422):
                    return None
                if exc.code in (500, 502, 503, 504):
                    if attempt == 3:
                        raise
                    time.sleep(2**attempt)
                    continue
                raise
            except (urllib.error.URLError, TimeoutError, http.client.RemoteDisconnected):
                if attempt == 3:
                    raise
                time.sleep(2**attempt)
        return None

    def search_repositories(self, query: str, page: int):
        params = urllib.parse.urlencode({"q": query, "per_page": 100, "page": page})
        return self.request(f"/search/repositories?{params}", search=True)

    def search_users(self, query: str, page: int):
        params = urllib.parse.urlencode({"q": query, "per_page": 100, "page": page})
        return self.request(f"/search/users?{params}", search=True)

    def reserve_from_live_limit(self, reserve: int = 30):
        limits = self.request("/rate_limit") or {}
        core = limits.get("resources", {}).get("core", {})
        remaining = int(core.get("remaining", self.budget))
        self.budget = min(self.budget, max(self.used, remaining - reserve))
        if self.budget <= self.used:
            raise BudgetExhausted(
                f"core quota low: remaining={remaining}, reset={core.get('reset')}"
            )


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def save_json(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def date_chunks(start: str, end: str):
    current = dt.date.fromisoformat(start)
    final = dt.date.fromisoformat(end)
    while current <= final:
        yield current.isoformat()
        current += dt.timedelta(days=1)


def task_key(stage: str, term: str, start: str, end: str):
    return f"adaptive:{stage}:{term or '-'}:{start}:{end}"


def seed_search_tasks(config: dict):
    start, end = config["target_created_from"], config["target_created_to"]
    tasks = []
    order = 0
    for term in config["user_search_seeds"]:
        tasks.append({"stage": "users", "term": term, "start": start, "end": end, "order": order})
        order += 1
    identity = config["identity"]
    for term in dict.fromkeys(identity["name_primary"] + identity["name_component"]):
        tasks.append({"stage": "identity", "term": term, "start": start, "end": end, "order": order})
        order += 1
    tasks.append({"stage": "personal", "term": "", "start": start, "end": end, "order": order})
    order += 1
    for term in config.get("site_name_seeds", []):
        tasks.append({"stage": "site", "term": term, "start": start, "end": end, "order": order})
        order += 1
    return tasks


def initialize_adaptive_tasks(state: dict, config: dict):
    tasks = state.setdefault("adaptive_searches", {})
    for seed in seed_search_tasks(config):
        key = task_key(seed["stage"], seed["term"], seed["start"], seed["end"])
        tasks.setdefault(key, {**seed, "page": 1, "complete": False, "split": False})
    # Strategy upgrades may reorder existing persisted tasks. Refresh order
    # from the current seed plan without clearing any cursor or completion data.
    current_orders = {
        (seed["stage"], seed["term"]): seed["order"]
        for seed in seed_search_tasks(config)
    }
    # Remove obsolete seed groups without disturbing cursors for active groups.
    # This lets spelling/strategy corrections preserve useful progress while
    # preventing completed or pending orphan tasks from consuming more budget.
    for key, task in list(tasks.items()):
        if (task["stage"], task["term"]) not in current_orders:
            del tasks[key]
    for task in tasks.values():
        task["order"] = current_orders.get(
            (task["stage"], task["term"]), task.get("order", 9999)
        )
    return tasks


def task_query(task: dict):
    created = f"created:{task['start']}..{task['end']}"
    if task["stage"] == "users":
        return f"{task['term']} in:login,name {created} type:user"
    if task["stage"] == "personal":
        return f"github.io in:name {created}"
    return f"{task['term']} in:name {created}"


def split_task(tasks: dict, key: str, task: dict):
    start = dt.date.fromisoformat(task["start"])
    end = dt.date.fromisoformat(task["end"])
    if start >= end:
        return False
    midpoint = start + (end - start) // 2
    ranges = [(start, midpoint), (midpoint + dt.timedelta(days=1), end)]
    for child_start, child_end in ranges:
        child = {
            "stage": task["stage"],
            "term": task["term"],
            "start": child_start.isoformat(),
            "end": child_end.isoformat(),
            "order": task["order"],
            "page": 1,
            "complete": False,
            "split": False,
        }
        child_key = task_key(child["stage"], child["term"], child["start"], child["end"])
        tasks.setdefault(child_key, child)
    task["complete"] = True
    task["split"] = True
    task["total_count"] = task.get("total_count", 0)
    return True


def pending_tasks(tasks: dict):
    return sorted(
        ((key, task) for key, task in tasks.items() if not task.get("complete")),
        key=lambda item: (item[1]["order"], item[1]["start"], item[1]["end"]),
    )


def enforce_query_result_limits(tasks: dict, config: dict):
    limits = config.get("query_result_limits", {})
    groups = {}
    for task in tasks.values():
        if task.get("split"):
            continue
        groups.setdefault((task["stage"], task["term"]), []).append(task)
    for (stage, _term), group in groups.items():
        limit = int(limits.get(stage, 0))
        completed_results = sum(
            int(task.get("total_count", 0)) for task in group if task.get("complete")
        )
        if limit and completed_results >= limit:
            for task in group:
                if not task.get("complete"):
                    task["complete"] = True
                    task["capped"] = True
                    task["stop_reason"] = (
                        f"query group reached {completed_results:,} results "
                        f"(limit {limit:,})"
                    )


def token_matches(token: str, source: str, numbers: set[str]):
    token = token.lower()
    source = source.lower()
    if token in numbers:
        return bool(re.search(rf"(?<![0-9]){re.escape(token)}(?![0-9])", source))
    return token in source


def matching_tokens(source: str, terms: list[str], numbers: set[str]):
    return sorted({term for term in terms if token_matches(term, source, numbers)})


def identity_terms(config: dict):
    identity = config["identity"]
    return list(dict.fromkeys(
        identity["name_primary"] + identity["name_component"] + identity["numbers"]
    ))


def identity_evidence(owner: str, profile: dict, config: dict):
    terms = identity_terms(config)
    numbers = set(config["identity"]["numbers"])
    login_hits = matching_tokens(owner, terms, numbers)
    profile_source = " ".join(
        str(profile.get(field) or "")
        for field in ("name", "bio")
    ).lower()
    return login_hits, matching_tokens(profile_source, terms, numbers)


def commit_identity_evidence(commit_author: dict, config: dict):
    terms = identity_terms(config)
    numbers = set(config["identity"]["numbers"])
    login = str(commit_author.get("login") or "").lower()
    metadata = " ".join(
        str(commit_author.get(field) or "")
        for field in ("name", "email")
    ).lower()
    return sorted(set(
        matching_tokens(login, terms, numbers)
        + matching_tokens(metadata, terms, numbers)
    ))


def identity_tier(login: str, profile_hits: list[str], commit_hits: list[str], config: dict):
    identity = config["identity"]
    numbers = set(identity["numbers"])
    login_hits = matching_tokens(login, identity_terms(config), numbers)
    combined_words = {"jessieliu", "liujessie", "liuxuan", "xuanliu"}
    if combined_words.intersection(login_hits):
        return 2
    families = set()
    lowered = login.lower()
    if "jess" in lowered or "jessie" in lowered:
        families.add("jess")
    if "liu" in lowered or "jliu" in lowered:
        families.add("liu")
    if "xuan" in lowered:
        families.add("xuan")
    number_hit = any(token_matches(term, lowered, numbers) for term in numbers)
    if len(families) >= 2 or (families and number_hit):
        return 2
    return 1 if login_hits or profile_hits or commit_hits else 0


def nickname_hits(login: str, profile: dict, config: dict):
    source = " ".join((login, str(profile.get("name") or ""), str(profile.get("bio") or ""))).lower()
    return sorted({term for term in config["identity"]["nickname_low"] if term in source})


def calculate_score(item: dict, config: dict):
    score = 0
    identity = config["identity"]
    login_hits = set(item.get("identity_hits", []))
    if item.get("identity_tier") == 2:
        score += 10
    else:
        if login_hits.intersection(identity["name_primary"]):
            score += 6
        elif login_hits.intersection(identity["name_component"]):
            score += 3
        number_hits = login_hits.intersection(identity["numbers"])
        if number_hits:
            score += 5 if number_hits.intersection({"110503", "20110503"}) else 3
    if item.get("profile_identity_hits"):
        score += 3
    if item.get("commit_identity_hits"):
        score += 2
    if item.get("nickname_hits"):
        score += 2
    if item.get("workflow_markers"):
        score += 3
    if item.get("is_personal_pages"):
        score += 3
    if item.get("account_created_in_window"):
        score += 3
    repo_created = (item.get("created_at") or "")[:10]
    if "2023-07-01" <= repo_created <= "2023-09-30":
        score += 2
    photos = item.get("probable_photo_count", 0)
    if photos >= 1:
        score += 2
    if photos >= 3:
        score += 2
    if item.get("dormant"):
        score += 2
    if item.get("post_count_sampled", 0):
        score += 1
    if item.get("content_only_hits"):
        score += 2
    return score


def normalize_candidate_scores(candidates: list[dict], config: dict):
    for item in candidates:
        repo_name = item.get("repository", "").split("/", 1)[-1]
        direct_hits, profile_hits = identity_evidence(item.get("owner", ""), item.get("owner_profile", {}), config)
        item["identity_hits"] = direct_hits
        item["profile_identity_hits"] = profile_hits
        item["commit_identity_hits"] = commit_identity_evidence(item.get("commit_author", {}), config)
        item["identity_tier"] = identity_tier(item.get("owner", ""), profile_hits, item["commit_identity_hits"], config)
        item["is_personal_pages"] = repo_name.lower() == (
            f"{item.get('owner', '').lower()}.github.io"
        )
        item["score"] = calculate_score(item, config)


def decode_blob(api: GitHub, full_name: str, sha: str) -> str:
    data = api.request(f"/repos/{full_name}/git/blobs/{sha}")
    if not data or data.get("encoding") != "base64":
        return ""
    try:
        return base64.b64decode(data["content"]).decode("utf-8", "replace")
    except (ValueError, KeyError):
        return ""


def get_owner_profile(api: GitHub, login: str, profile_cache: dict):
    key = login.lower()
    if key not in profile_cache:
        data = api.request(f"/users/{urllib.parse.quote(login, safe='')}") or {}
        profile_cache[key] = {
            field: data.get(field)
            for field in (
                "name", "bio", "blog", "email", "location", "twitter_username",
                "created_at",
            )
            if data.get(field) not in (None, "")
        }
    return profile_cache[key]


def get_commit_author(api: GitHub, full_name: str):
    params = urllib.parse.urlencode({"per_page": 1})
    commits = api.request(f"/repos/{full_name}/commits?{params}") or []
    if not commits:
        return {}
    commit = commits[0]
    author = commit.get("commit", {}).get("author", {}) or {}
    github_author = commit.get("author") or {}
    return {
        key: value
        for key, value in {
            "name": author.get("name"),
            "email": author.get("email"),
            "login": github_author.get("login"),
        }.items()
        if value not in (None, "")
    }


def get_user_pages_repositories(
    api: GitHub,
    login: str,
    max_pages: int,
    created_from: str,
    created_to: str,
):
    repositories = []
    for page in range(1, max_pages + 1):
        params = urllib.parse.urlencode(
            {
                "per_page": 100,
                "page": page,
                "type": "owner",
                "sort": "created",
                "direction": "desc",
            }
        )
        items = api.request(
            f"/users/{urllib.parse.quote(login, safe='')}/repos?{params}"
        ) or []
        for repo in items:
            if not repo.get("has_pages"):
                continue
            created = (repo.get("created_at") or "")[:10]
            if created_from <= created <= created_to:
                repositories.append(repo)
        if len(items) < 100:
            break
    return repositories


def inspect_repository(api: GitHub, repo: dict, config: dict, profile_cache: dict):
    full_name = repo["full_name"]
    pushed = repo.get("pushed_at") or ""
    if not repo.get("has_pages"):
        return None
    if repo.get("owner", {}).get("type") != "User":
        return None
    owner = repo.get("owner", {}).get("login", "")
    is_personal_pages = repo["name"].lower() == f"{owner.lower()}.github.io"
    branch = repo.get("default_branch") or "main"
    tree_data = api.request(f"/repos/{full_name}/git/trees/{urllib.parse.quote(branch, safe='')}?recursive=1")
    if not tree_data:
        return None
    tree_truncated = bool(tree_data.get("truncated"))
    tree = [item for item in tree_data.get("tree", []) if item.get("type") == "blob"]
    workflow_files = [item for item in tree if WORKFLOW_RE.search(item["path"])]
    post_files = [item for item in tree if POST_RE.search(item["path"])][:12]
    image_paths = [item["path"] for item in tree if IMAGE_RE.search(item["path"])]
    probable_photos = [
        path for path in image_paths
        if REAL_PHOTO_RE.search(path) and not NON_PHOTO_RE.search(path)
    ]

    markers = []
    for item in workflow_files[:2]:
        workflow_text = decode_blob(api, full_name, item["sha"])
        markers = [
            marker
            for marker in config["workflow_markers"]
            if marker.lower() in workflow_text.lower()
        ]
        if markers:
            break
    profile = get_owner_profile(api, owner, profile_cache)
    identity_hits, profile_identity_hits = identity_evidence(owner, profile, config)
    commit_author = get_commit_author(api, full_name)
    commit_identity_hits = commit_identity_evidence(commit_author, config)
    tier = identity_tier(owner, profile_identity_hits, commit_identity_hits, config)
    nick_hits = nickname_hits(owner, profile, config)
    account_created = (profile.get("created_at") or "")[:10]
    account_created_in_window = (
        config["account_created_from"] <= account_created <= config["account_created_to"]
    )
    repo_created = (repo.get("created_at") or "")[:10]
    pushed_date = pushed[:10]
    dormant = repo_created.startswith("2023-") and bool(pushed_date) and pushed_date <= "2023-12-31"
    path_source = "\n".join(item["path"] for item in tree).lower()
    content_only_hits = sorted({
        term for term in config["identity"]["content_only"]
        if term.lower() in path_source
    })
    markers_present = bool(markers)
    has_blog_signal = (
        is_personal_pages
        or len(image_paths) >= 1
        or bool(post_files)
        or bool(content_only_hits)
    )
    fingerprint = account_created_in_window and markers_present and has_blog_signal
    if tier < 1 and not fingerprint:
        return None

    candidate = {
        "owner": owner,
        "repository": full_name,
        "url": repo["html_url"],
        "pages_url": repo.get("homepage") or (
            f"https://{repo['owner']['login']}.github.io/"
            if repo["name"].lower() == f"{repo['owner']['login'].lower()}.github.io"
            else f"https://{repo['owner']['login']}.github.io/{repo['name']}/"
        ),
        "created_at": repo.get("created_at"),
        "pushed_at": pushed,
        "workflow_markers": markers,
        "identity_hits": identity_hits,
        "profile_identity_hits": profile_identity_hits,
        "commit_identity_hits": commit_identity_hits,
        "commit_author": commit_author,
        "owner_profile": profile,
        "identity_tier": tier,
        "nickname_hits": nick_hits,
        "content_only_hits": content_only_hits,
        "account_created_in_window": account_created_in_window,
        "dormant": dormant,
        "is_personal_pages": is_personal_pages,
        "tree_truncated": tree_truncated,
        "image_count": len(image_paths),
        "probable_photo_count": len(probable_photos),
        "sample_photos": probable_photos[:20],
        "post_count_sampled": len(post_files),
        "sample_posts": [item["path"] for item in post_files[:12]],
        "description": repo.get("description"),
        "first_seen_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    candidate["score"] = calculate_score(candidate, config)
    if candidate["score"] < config["minimum_candidate_score"]:
        return None
    return candidate


def render_report(candidates: list[dict], state: dict):
    lines = [
        "# Candidate accounts",
        "",
        "Generated incrementally by GitHub Actions. Behavior score is the primary ranking key.",
        "",
        f"Last run: `{state['stats'].get('last_run_utc')}`  ",
        f"Repositories inspected: `{state['stats'].get('repositories_inspected', 0)}`  ",
        f"Candidates: `{len(candidates)}`",
        "",
    ]
    if not candidates:
        lines.append("No candidates have been recorded yet.")
    for item in sorted(candidates, key=candidate_sort_key):
        identity_summary = ", ".join(
            sorted(
                set(
                    item["identity_hits"]
                    + item.get("profile_identity_hits", [])
                    + item.get("commit_identity_hits", [])
                )
            )
        ) or "none"
        summary = (
            f'<summary><strong>Tier {item.get("identity_tier", 0)} · {item["score"]} points — '
            f'<a href="{html.escape(item["url"], quote=True)}">'
            f'{html.escape(item["repository"])}</a></strong> · '
            f'probable photos {item["probable_photo_count"]} · '
            f'identity {html.escape(identity_summary)}</summary>'
        )
        lines += [
            "<details>",
            summary,
            "",
            f"- Owner: [{item['owner']}](https://github.com/{item['owner']})",
            f"- Live site: {item.get('pages_url') or 'none'}",
            f"- Identity tier: **{item.get('identity_tier', 0)}**",
            f"- Created / pushed: `{item['created_at']}` / `{item['pushed_at']}`",
            f"- Account created: `{item.get('owner_profile', {}).get('created_at') or 'unknown'}` · in window `{item.get('account_created_in_window', False)}`",
            f"- Dormant signal: `{item.get('dormant', False)}`",
            f"- Pages workflow: `{', '.join(item['workflow_markers'])}`",
            f"- Identity hits: `{', '.join(item['identity_hits']) or 'none'}`",
            f"- Profile identity hits: `{', '.join(item.get('profile_identity_hits', [])) or 'none'}`",
            f"- Profile name: `{item.get('owner_profile', {}).get('name') or 'none'}`",
            f"- Commit identity hits: `{', '.join(item.get('commit_identity_hits', [])) or 'none'}`",
            f"- Latest commit author: `{item.get('commit_author', {}).get('name') or 'none'}` / `{item.get('commit_author', {}).get('email') or 'none'}`",
            f"- Nickname hits: `{', '.join(item.get('nickname_hits', [])) or 'none'}`",
            f"- Content/path hints: `{', '.join(item.get('content_only_hits', [])) or 'none'}`",
            f"- Images / probable photos: `{item['image_count']}` / `{item['probable_photo_count']}`",
            f"- Tree truncated: `{item.get('tree_truncated', False)}`",
            "",
        ]
        for label, paths in (("Sample posts", item["sample_posts"]), ("Sample photos", item["sample_photos"])):
            lines += [f"<details><summary>{label} ({len(paths)})</summary>", ""]
            if paths:
                lines.extend(f"- `{path}`" for path in paths)
            else:
                lines.append("None.")
            lines += ["", "</details>", ""]
        lines += ["</details>", ""]
    REPORT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def candidate_sort_key(item: dict):
    return (
        -int(item.get("score", 0)),
        -int(item.get("identity_tier", 0)),
        -int(bool(item.get("dormant"))),
        item["repository"].lower(),
    )


def render_progress(tasks: dict, state: dict, candidates: list[dict]):
    leaf_tasks = [task for task in tasks.values() if not task.get("split")]
    completed = sum(bool(task.get("complete")) for task in leaf_tasks)
    pending = pending_tasks(tasks)
    active = (
        f"{pending[0][1]['stage']}:{pending[0][1]['term'] or 'username.github.io'} "
        f"{pending[0][1]['start']}..{pending[0][1]['end']}, page {pending[0][1].get('page', 1)}"
        if pending else "complete"
    )
    repositories = sorted(
        set(state.get("processed_repositories", []))
        | set(state.get("processed_repositories_v2", []))
    )
    owners = {name.split("/", 1)[0].lower() for name in repositories if "/" in name}
    # Adaptive ranges are implementation details: splitting one dense range into
    # two used to increase the denominator and made progress appear to move
    # backwards. Report fixed seed/date coverage instead. Each seed contributes
    # one unit per day in the configured window, regardless of how often GitHub's
    # 1,000-result ceiling forces that window to be subdivided.
    configured_seeds = {
        (task["stage"], task["term"], task["start"], task["end"])
        for task in seed_search_tasks(load_json(CONFIG_PATH, {}))
    }

    def coverage_for(stage=None):
        relevant_seeds = [seed for seed in configured_seeds if stage is None or seed[0] == stage]
        total_days = sum(
            (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days + 1
            for _seed_stage, _term, start, end in relevant_seeds
        )
        covered = set()
        seed_terms = {(seed_stage, term) for seed_stage, term, _start, _end in relevant_seeds}
        for task in leaf_tasks:
            identity = (task["stage"], task["term"])
            if identity not in seed_terms or not task.get("complete"):
                continue
            for day in date_chunks(task["start"], task["end"]):
                covered.add((task["stage"], task["term"], day))
        return len(covered), total_days

    covered_days, total_days = coverage_for()
    percent = (covered_days / total_days * 100) if total_days else 100.0
    stats = state.get("stats", {})
    stage_specs = [
        ("users: login/profile name + account created date", "users"),
        ("identity: repository names", "identity"),
        ("personal: strict username.github.io fallback", "personal"),
        ("site: project-page blog names", "site"),
    ]
    stage_rows = []
    for label, stage in stage_specs:
        done, total = coverage_for(stage)
        stage_percent = (done / total * 100) if total else 100.0
        stage_rows.append(f"| {label} | {done:,} / {total:,} seed-days | {stage_percent:.1f}% |")
    capped = sum(bool(task.get("capped")) for task in leaf_tasks)
    lines = [
        "# Search progress",
        "",
        f"- Fixed search coverage: **{covered_days:,} / {total_days:,} seed-days ({percent:.1f}%)**",
        f"- Adaptive range diagnostics: **{completed:,} / {len(leaf_tasks):,} leaf ranges complete**",
        f"- Current cursor: `{active}`",
        f"- Repository results seen: **{stats.get('repositories_seen', 0):,}**",
        f"- User search results seen: **{stats.get('users_seen', 0):,}**",
        f"- Pages repositories found through users: **{stats.get('user_pages_repositories_seen', 0):,}**",
        f"- Identity users fully checked: **{len(state.get('processed_identity_users', [])):,}**",
        f"- Unique repositories investigated: **{len(repositories):,}**",
        f"- Unique account owners investigated: **{len(owners):,}**",
        f"- Candidates recorded: **{len(candidates):,}**",
        f"- Ranges stopped by result caps: **{capped:,}**",
        f"- Workflow runs: **{stats.get('runs', 0):,}**",
        f"- Last run (UTC): `{stats.get('last_run_utc')}`",
        f"- Last API requests used: **{stats.get('last_api_requests', 0):,}**",
        f"- Last stop reason: `{stats.get('last_error') or 'none'}`",
        "",
        "## Progress by stage",
        "",
        "| Stage | Completed | Progress |",
        "|---|---:|---:|",
        *stage_rows,
        "",
        "The main percentage uses a fixed denominator: one unit per seed per day in the configured",
        "account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than",
        "1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.",
        "Already investigated repositories are never inspected again.",
    ]
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("GH_TOKEN is required")
    config = load_json(CONFIG_PATH, {})
    state = load_json(STATE_PATH, {})
    candidates = load_json(CANDIDATES_PATH, [])
    normalize_candidate_scores(candidates, config)
    api = GitHub(token, int(os.environ.get("MAX_API_REQUESTS", "950")))
    tasks = initialize_adaptive_tasks(state, config)
    enforce_query_result_limits(tasks, config)
    # Version the inspection set when hard filters change. Keep the legacy set
    # for audit/progress, but allow high-value searches to re-evaluate repos
    # that an older strategy may have incorrectly rejected.
    processed = set(state.get("processed_repositories_v2", []))
    processed_identity_users = set(state.get("processed_identity_users", []))
    profile_cache = state.setdefault("owner_profiles", {})
    for login, profile in list(profile_cache.items()):
        profile_cache[login] = {
            field: value
            for field, value in profile.items()
            if value not in (None, "")
        }
    by_repo = {item["repository"].lower(): item for item in candidates}
    state.setdefault("searches", {})  # Retain legacy daily cursors as history.
    stats = state.setdefault("stats", {})
    stats["runs"] = stats.get("runs", 0) + 1
    stats["last_run_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    stats["last_error"] = None

    try:
        api.reserve_from_live_limit()
        while pending_tasks(tasks):
            key, cursor = pending_tasks(tasks)[0]
            while not cursor["complete"]:
                if cursor["stage"] == "users":
                    result = api.search_users(task_query(cursor), cursor["page"])
                else:
                    result = api.search_repositories(task_query(cursor), cursor["page"])
                if not result:
                    cursor["complete"] = True
                    break
                cursor["total_count"] = int(result.get("total_count", 0))
                if cursor["page"] == 1 and cursor["total_count"] > 1000:
                    if split_task(tasks, key, cursor):
                        enforce_query_result_limits(tasks, config)
                        break
                items = result.get("items", [])
                if cursor["stage"] == "users":
                    stats["users_seen"] = stats.get("users_seen", 0) + len(items)
                else:
                    stats["repositories_seen"] = stats.get("repositories_seen", 0) + len(items)
                for item in items:
                    if cursor["stage"] == "users":
                        login = item.get("login", "")
                        if not login or login.lower() in processed_identity_users:
                            continue
                        repositories_to_check = get_user_pages_repositories(
                            api,
                            login,
                            int(config.get("user_repo_pages", 2)),
                            config["target_created_from"],
                            config["target_created_to"],
                        )
                        stats["user_pages_repositories_seen"] = (
                            stats.get("user_pages_repositories_seen", 0)
                            + len(repositories_to_check)
                        )
                    else:
                        repositories_to_check = [item]
                    for repo in repositories_to_check:
                        if cursor["stage"] == "personal" and repo["name"].lower() != (
                            f"{repo['owner']['login'].lower()}.github.io"
                        ):
                            continue
                        full_name = repo["full_name"].lower()
                        if full_name in processed:
                            continue
                        candidate = inspect_repository(api, repo, config, profile_cache)
                        processed.add(full_name)
                        stats["repositories_inspected"] = stats.get("repositories_inspected", 0) + 1
                        if candidate:
                            by_repo[full_name] = candidate
                    if cursor["stage"] == "users":
                        processed_identity_users.add(login.lower())
                if len(items) < 100 or cursor["page"] >= 10:
                    cursor["complete"] = True
                else:
                    cursor["page"] += 1
                enforce_query_result_limits(tasks, config)
    except BudgetExhausted as exc:
        stats["last_error"] = str(exc) or "request budget exhausted"
    except Exception as exc:  # Preserve progress and make the failure visible.
        stats["last_error"] = f"{type(exc).__name__}: {exc}"
    finally:
        stats["last_api_requests"] = api.used
        stats["last_api_budget"] = api.budget
        state["processed_repositories_v2"] = sorted(processed)
        state["processed_identity_users"] = sorted(processed_identity_users)
        save_json(STATE_PATH, state)
        candidate_list = list(by_repo.values())
        save_json(CANDIDATES_PATH, candidate_list)
        render_report(candidate_list, state)
        render_progress(tasks, state, candidate_list)
        print(f"API requests: {api.used}/{api.budget}")
        print(f"Processed repositories: {len(processed)}")
        print(f"Candidates: {len(by_repo)}")


if __name__ == "__main__":
    main()

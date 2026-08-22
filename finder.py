#!/usr/bin/env python3
"""Incrementally find photo-oriented GitHub Pages repositories from 2023.

The built-in Actions GITHUB_TOKEN is intentionally used instead of a PAT.
State and candidate reports are committed by the workflow after every run.
"""

from __future__ import annotations

import base64
import datetime as dt
import html
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
REAL_PHOTO_RE = re.compile(r"(?:^|/)(?:img|images?|photos?|album|gallery|uploads?)/", re.I)
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

    def request(self, path: str, *, search: bool = False, accept: str | None = None):
        if self.used >= self.budget:
            raise BudgetExhausted
        if search:
            # User/repository search allows 30 requests/minute. Staying below it
            # also reduces secondary-limit risk.
            delay = 2.2 - (time.monotonic() - self.search_last)
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
                raise
            except (urllib.error.URLError, TimeoutError):
                if attempt == 3:
                    raise
                time.sleep(2**attempt)
        return None

    def search_repositories(self, query: str, page: int):
        params = urllib.parse.urlencode({"q": query, "per_page": 100, "page": page})
        return self.request(f"/search/repositories?{params}", search=True)

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
    for term in config["priority_name_terms"]:
        tasks.append({"stage": term, "term": term, "start": start, "end": end, "order": order})
        order += 1
    tasks.append({"stage": "personal", "term": "", "start": start, "end": end, "order": order})
    order += 1
    for term in config["site_name_terms"]:
        tasks.append({"stage": "other", "term": term, "start": start, "end": end, "order": order})
        order += 1
    for term in config["identity_terms"]:
        tasks.append({"stage": "identity", "term": term, "start": start, "end": end, "order": order})
        order += 1
    return tasks


def initialize_adaptive_tasks(state: dict, config: dict):
    tasks = state.setdefault("adaptive_searches", {})
    for seed in seed_search_tasks(config):
        key = task_key(seed["stage"], seed["term"], seed["start"], seed["end"])
        tasks.setdefault(key, {**seed, "page": 1, "complete": False, "split": False})
    return tasks


def task_query(task: dict):
    created = f"created:{task['start']}..{task['end']}"
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


def priority_name_evidence(repo_name: str, terms: list[str]):
    name = repo_name.lower()
    hits = [term.lower() for term in terms if term.lower() in name]
    if any(name == term for term in hits):
        return 8, hits
    if any(name.startswith(term) or name.endswith(term) for term in hits):
        return 6, hits
    if hits:
        return 4, hits
    return 0, []


def decode_blob(api: GitHub, full_name: str, sha: str) -> str:
    data = api.request(f"/repos/{full_name}/git/blobs/{sha}")
    if not data or data.get("encoding") != "base64":
        return ""
    try:
        return base64.b64decode(data["content"]).decode("utf-8", "replace")
    except (ValueError, KeyError):
        return ""


def inspect_repository(api: GitHub, repo: dict, config: dict):
    full_name = repo["full_name"]
    pushed = repo.get("pushed_at") or ""
    if not repo.get("has_pages"):
        return None
    branch = repo.get("default_branch") or "main"
    tree_data = api.request(f"/repos/{full_name}/git/trees/{urllib.parse.quote(branch, safe='')}?recursive=1")
    if not tree_data or tree_data.get("truncated"):
        return None
    tree = [item for item in tree_data.get("tree", []) if item.get("type") == "blob"]
    workflow_files = [item for item in tree if WORKFLOW_RE.search(item["path"])]
    post_files = [item for item in tree if POST_RE.search(item["path"])][:12]
    image_paths = [item["path"] for item in tree if IMAGE_RE.search(item["path"])]
    probable_photos = [
        path for path in image_paths
        if REAL_PHOTO_RE.search(path) and not NON_PHOTO_RE.search(path)
    ]

    workflow_texts = [decode_blob(api, full_name, item["sha"]) for item in workflow_files[:8]]
    workflow_text = "\n".join(workflow_texts)
    markers = [marker for marker in config["workflow_markers"] if marker.lower() in workflow_text.lower()]
    if not markers:
        return None

    post_texts = [decode_blob(api, full_name, item["sha"])[:100_000] for item in post_files]
    searchable = "\n".join(post_texts)
    identity_haystack = " ".join(
        [repo.get("owner", {}).get("login", ""), repo.get("name", ""), repo.get("description") or "", searchable]
    ).lower()
    identity_hits = sorted({term for term in config["identity_terms"] if term in identity_haystack})
    priority_name_bonus, priority_name_hits = priority_name_evidence(
        repo["name"], config["priority_name_terms"]
    )
    # The forgotten account is personal. Organization documentation sites
    # dominate Pages results and produce overwhelming false positives.
    if repo.get("owner", {}).get("type") != "User":
        return None
    if not (identity_hits or post_files or len(probable_photos) >= config["minimum_photo_count"]):
        return None

    score = 5  # Verified Pages workflow.
    if repo["name"].lower() == f"{repo['owner']['login'].lower()}.github.io":
        score += 5
    created = repo.get("created_at", "")[:10]
    if config["target_created_from"] <= created <= config["target_created_to"]:
        score += 4
    if len(probable_photos) >= config["minimum_photo_count"]:
        score += 5
    elif image_paths:
        score += 1
    if post_files:
        score += 2
    score += min(5, len(identity_hits) * 3)
    score += priority_name_bonus

    if score < config["minimum_candidate_score"]:
        return None
    return {
        "score": score,
        "owner": repo["owner"]["login"],
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
        "priority_name_hits": priority_name_hits,
        "priority_name_bonus": priority_name_bonus,
        "image_count": len(image_paths),
        "probable_photo_count": len(probable_photos),
        "sample_photos": probable_photos[:20],
        "post_count_sampled": len(post_files),
        "sample_posts": [item["path"] for item in post_files[:12]],
        "description": repo.get("description"),
        "first_seen_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def render_report(candidates: list[dict], state: dict):
    lines = [
        "# Candidate accounts",
        "",
        "Generated incrementally by GitHub Actions. Higher scores should be reviewed first.",
        "",
        f"Last run: `{state['stats'].get('last_run_utc')}`  ",
        f"Repositories inspected: `{state['stats'].get('repositories_inspected', 0)}`  ",
        f"Candidates: `{len(candidates)}`",
        "",
    ]
    if not candidates:
        lines.append("No candidates have been recorded yet.")
    for item in sorted(candidates, key=lambda x: (-x["score"], x["repository"].lower())):
        identity_summary = ", ".join(item["identity_hits"]) or "none"
        summary = (
            f'<summary><strong>{item["score"]} points — '
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
            f"- Created / pushed: `{item['created_at']}` / `{item['pushed_at']}`",
            f"- Pages workflow: `{', '.join(item['workflow_markers'])}`",
            f"- Identity hits: `{', '.join(item['identity_hits']) or 'none'}`",
            f"- Priority-name hits / bonus: `{', '.join(item.get('priority_name_hits', [])) or 'none'}` / `+{item.get('priority_name_bonus', 0)}`",
            f"- Images / probable photos: `{item['image_count']}` / `{item['probable_photo_count']}`",
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


def render_progress(tasks: dict, state: dict, candidates: list[dict]):
    leaf_tasks = [task for task in tasks.values() if not task.get("split")]
    completed = sum(bool(task.get("complete")) for task in leaf_tasks)
    pending = pending_tasks(tasks)
    active = (
        f"{pending[0][1]['stage']}:{pending[0][1]['term'] or 'username.github.io'} "
        f"{pending[0][1]['start']}..{pending[0][1]['end']}, page {pending[0][1].get('page', 1)}"
        if pending else "complete"
    )
    repositories = state.get("processed_repositories", [])
    owners = {name.split("/", 1)[0].lower() for name in repositories if "/" in name}
    percent = (completed / len(leaf_tasks) * 100) if leaf_tasks else 100.0
    stats = state.get("stats", {})
    priority_terms = load_json(CONFIG_PATH, {}).get("priority_name_terms", [])
    stage_specs = [(term, term) for term in priority_terms] + [
        ("username.github.io", "personal"),
        ("other site names", "other"),
        ("identity fragments", "identity"),
    ]
    stage_rows = []
    for label, stage in stage_specs:
        stage_tasks = [task for task in leaf_tasks if task["stage"] == stage]
        done = sum(bool(task.get("complete")) for task in stage_tasks)
        stage_percent = (done / len(stage_tasks) * 100) if stage_tasks else 100.0
        stage_rows.append(f"| {label} | {done:,} / {len(stage_tasks):,} | {stage_percent:.1f}% |")
    lines = [
        "# Search progress",
        "",
        f"- Adaptive search ranges: **{completed:,} / {len(leaf_tasks):,} ({percent:.1f}%)**",
        f"- Current cursor: `{active}`",
        f"- Repository results seen: **{stats.get('repositories_seen', 0):,}**",
        f"- Unique repositories investigated: **{len(repositories):,}**",
        f"- Unique account owners investigated: **{len(owners):,}**",
        f"- Candidates recorded: **{len(candidates):,}**",
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
        "Each stage starts as one three-month query. A range is split only when GitHub",
        "reports more than 1,000 results, so the denominator may grow while a dense",
        "range is being subdivided. Already investigated repositories are never",
        "inspected again.",
    ]
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("GH_TOKEN is required")
    config = load_json(CONFIG_PATH, {})
    state = load_json(STATE_PATH, {})
    candidates = load_json(CANDIDATES_PATH, [])
    # Remove scores produced by the retired memory-based content keywords so
    # old and new candidates remain comparable without rerunning searches.
    for item in candidates:
        old_hits = item.pop("content_hits", [])
        item["score"] = max(0, item.get("score", 0) - min(4, len(old_hits) * 2))
        if "priority_name_bonus" not in item:
            repo_name = item.get("repository", "/").split("/", 1)[-1]
            bonus, hits = priority_name_evidence(repo_name, config["priority_name_terms"])
            item["priority_name_bonus"] = bonus
            item["priority_name_hits"] = hits
            item["score"] = item.get("score", 0) + bonus
    api = GitHub(token, int(os.environ.get("MAX_API_REQUESTS", "950")))
    tasks = initialize_adaptive_tasks(state, config)
    processed = set(state.get("processed_repositories", []))
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
                result = api.search_repositories(task_query(cursor), cursor["page"])
                if not result:
                    cursor["complete"] = True
                    break
                cursor["total_count"] = int(result.get("total_count", 0))
                if cursor["page"] == 1 and cursor["total_count"] > 1000:
                    if split_task(tasks, key, cursor):
                        break
                items = result.get("items", [])
                stats["repositories_seen"] = stats.get("repositories_seen", 0) + len(items)
                for repo in items:
                    if cursor["stage"] == "personal" and repo["name"].lower() != (
                        f"{repo['owner']['login'].lower()}.github.io"
                    ):
                        continue
                    full_name = repo["full_name"].lower()
                    if full_name in processed:
                        continue
                    candidate = inspect_repository(api, repo, config)
                    processed.add(full_name)
                    stats["repositories_inspected"] = stats.get("repositories_inspected", 0) + 1
                    if candidate:
                        by_repo[full_name] = candidate
                if len(items) < 100 or cursor["page"] >= 10:
                    cursor["complete"] = True
                else:
                    cursor["page"] += 1
    except BudgetExhausted as exc:
        stats["last_error"] = str(exc) or "request budget exhausted"
    except Exception as exc:  # Preserve progress and make the failure visible.
        stats["last_error"] = f"{type(exc).__name__}: {exc}"
    finally:
        stats["last_api_requests"] = api.used
        stats["last_api_budget"] = api.budget
        state["processed_repositories"] = sorted(processed)
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

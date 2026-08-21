#!/usr/bin/env python3
"""Incrementally find photo-oriented GitHub Pages repositories from 2023.

The built-in Actions GITHUB_TOKEN is intentionally used instead of a PAT.
State and candidate reports are committed by the workflow after every run.
"""

from __future__ import annotations

import base64
import datetime as dt
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


def build_search_plan(config: dict):
    start, end = config["target_created_from"], config["target_created_to"]
    plan = []
    # Daily partitioning avoids GitHub's 1,000-result search ceiling.
    for day in date_chunks(start, end):
        plan.append((f"personal:{day}", f"github.io in:name created:{day}"))
    for term in config["site_name_terms"]:
        for day in date_chunks(start, end):
            plan.append((f"named:{term}:{day}", f"{term} in:name created:{day}"))
    for term in config["identity_terms"]:
        for day in date_chunks(start, end):
            plan.append((f"identity:{term}:{day}", f"{term} in:name created:{day}"))
    return plan


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
    content_hits = sorted({term for term in config["content_terms"] if term.lower() in searchable.lower()})

    # The forgotten account is personal. Organization documentation sites
    # dominate Pages results and produce overwhelming false positives.
    if repo.get("owner", {}).get("type") != "User":
        return None
    if not (identity_hits or content_hits or post_files or len(probable_photos) >= config["minimum_photo_count"]):
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
    score += min(4, len(content_hits) * 2)

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
        "content_hits": content_hits,
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
        lines += [
            f"## {item['score']} points — [{item['repository']}]({item['url']})",
            "",
            f"- Owner: [{item['owner']}](https://github.com/{item['owner']})",
            f"- Created / pushed: `{item['created_at']}` / `{item['pushed_at']}`",
            f"- Pages workflow: `{', '.join(item['workflow_markers'])}`",
            f"- Identity hits: `{', '.join(item['identity_hits']) or 'none'}`",
            f"- Content hits: `{', '.join(item['content_hits']) or 'none'}`",
            f"- Images / probable photos: `{item['image_count']}` / `{item['probable_photo_count']}`",
            f"- Sample posts: `{', '.join(item['sample_posts']) or 'none'}`",
            f"- Sample photos: `{', '.join(item['sample_photos']) or 'none'}`",
            "",
        ]
    REPORT_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def render_progress(plan: list[tuple[str, str]], state: dict, candidates: list[dict]):
    searches = state.get("searches", {})
    completed = sum(bool(searches.get(key, {}).get("complete")) for key, _ in plan)
    active = next(
        (
            f"{key}, page {searches.get(key, {}).get('page', 1)}"
            for key, _ in plan
            if not searches.get(key, {}).get("complete")
        ),
        "complete",
    )
    repositories = state.get("processed_repositories", [])
    owners = {name.split("/", 1)[0].lower() for name in repositories if "/" in name}
    percent = (completed / len(plan) * 100) if plan else 100.0
    stats = state.get("stats", {})
    lines = [
        "# Search progress",
        "",
        f"- Search tasks: **{completed:,} / {len(plan):,} ({percent:.1f}%)**",
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
        "The task percentage is exact for the current strategy. The account total is",
        "dynamic because different queries overlap and GitHub does not expose a global",
        "deduplicated total in advance.",
    ]
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("GH_TOKEN is required")
    config = load_json(CONFIG_PATH, {})
    state = load_json(STATE_PATH, {})
    candidates = load_json(CANDIDATES_PATH, [])
    api = GitHub(token, int(os.environ.get("MAX_API_REQUESTS", "950")))
    plan = build_search_plan(config)
    processed = set(state.get("processed_repositories", []))
    by_repo = {item["repository"].lower(): item for item in candidates}
    searches = state.setdefault("searches", {})
    stats = state.setdefault("stats", {})
    stats["runs"] = stats.get("runs", 0) + 1
    stats["last_run_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    stats["last_error"] = None

    try:
        api.reserve_from_live_limit()
        for key, query in plan:
            cursor = searches.setdefault(key, {"page": 1, "complete": False})
            if cursor["complete"]:
                continue
            while not cursor["complete"]:
                result = api.search_repositories(query, cursor["page"])
                if not result:
                    cursor["complete"] = True
                    break
                items = result.get("items", [])
                stats["repositories_seen"] = stats.get("repositories_seen", 0) + len(items)
                for repo in items:
                    if key.startswith("personal:") and repo["name"].lower() != (
                        f"{repo['owner']['login'].lower()}.github.io"
                    ):
                        continue
                    full_name = repo["full_name"].lower()
                    if full_name in processed:
                        continue
                    processed.add(full_name)
                    stats["repositories_inspected"] = stats.get("repositories_inspected", 0) + 1
                    candidate = inspect_repository(api, repo, config)
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
        render_progress(plan, state, candidate_list)
        print(f"API requests: {api.used}/{api.budget}")
        print(f"Processed repositories: {len(processed)}")
        print(f"Candidates: {len(by_repo)}")


if __name__ == "__main__":
    main()

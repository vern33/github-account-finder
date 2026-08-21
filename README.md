# GitHub Account Finder

This repository incrementally searches for the forgotten GitHub Pages account described in this project. The search runs entirely in GitHub Actions with the repository-scoped `GITHUB_TOKEN`; it does not use a personal access token or the local machine's GitHub API quota.

## Search strategy

The workflow prioritizes repositories that:

1. were created from August through October 2023;
2. have GitHub Pages enabled, regardless of later activity;
3. use a recognizable GitHub Pages deployment workflow;
4. contain blog posts and multiple likely photographs;
5. contain identity fragments such as `jess`, `jessie`, `jesse`, `liu`, `xuan`, or `lx` in repository content or ownership metadata.

Location text (including 河南), language, article count, and activity after 2023 are **not** hard filters.

The first pass searches personal repositories named `owner.github.io`. Later passes search photo/blog/site-like repository names and identity fragments. Searches are split by day to avoid GitHub's 1,000-result search ceiling.

## Outputs

- [`candidates.md`](candidates.md): human-readable candidates, highest score first.
- [`candidates.json`](candidates.json): structured candidate evidence.
- [`state.json`](state.json): durable pagination and deduplication state.

The scheduled workflow commits changes to these files after each run. It runs hourly and can also be started manually from the Actions tab.

## Security and rate limits

The workflow uses only `${{ github.token }}`. Do not add a personal token unless there is a specific reason to share the personal account's API quota. Each run has an explicit core-request budget and throttles search requests to reduce secondary-rate-limit failures.

## Manual run

Open **Actions → Search forgotten GitHub Pages account → Run workflow**. The optional request budget defaults to 750, below the normal 1,000 requests/hour limit for an Actions `GITHUB_TOKEN`.

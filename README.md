# GitHub Account Finder

This repository incrementally searches for the forgotten GitHub Pages account described in this project. The search runs entirely in GitHub Actions with the repository-scoped `GITHUB_TOKEN`; it does not use a personal access token or the local machine's GitHub API quota.

## Search strategy

The workflow prioritizes repositories that:

1. were created from August through October 2023;
2. have GitHub Pages enabled, regardless of later activity;
3. may use a recognizable GitHub Pages deployment workflow as supporting evidence;
4. contain blog posts and multiple likely photographs;
5. contain identity fragments such as `jess`, `jessie`, `jesse`, `liu`, `xuan`, or `lx` in account, repository, profile, or commit-author metadata.

Search stages run in this order: strict `username.github.io`, user logins containing identity fragments, repository name `pages`, repository name `blog`, other site-like names, then repository-name identity fragments. `blog` and `pages` affect score only; they are never required. An exact name earns 8 points, a prefix or suffix earns 6, and any other name occurrence earns 4. Each query starts with the full three-month range and is recursively split only when GitHub reports more than 1,000 results; the old fixed set of 1,748 daily queries is no longer used.

Broad query groups have result caps so a generic word cannot consume the entire search budget. Identity fragments score only when present in the account login, repository name, or public owner profile fields; occurrences inside article text do not count.

GitHub Pages deployment workflows are supporting evidence, not a hard requirement. Repositories with truncated recursive trees are evaluated using the partial tree instead of being discarded. Photo paths include Hexo/Hugo/Jekyll conventions such as `source/_posts`, `content/posts`, `static`, `public`, and `assets`. Public owner profile fields are cached compactly and checked for identity fragments. Candidate-like repositories also inspect the latest commit author's name, email, and linked GitHub login.

Every strict `owner.github.io` repository passes structural admission so its commit author can be evaluated even when no conventional post or photo paths are recognized. The final score threshold still rejects personal Pages repositories without enough date or identity evidence.

The legacy processed-repository set is retained for audit, while the corrected inspection policy writes to a versioned v2 set. This lets high-value personal/user searches re-evaluate repositories that the former workflow/truncation hard filters may have rejected, without losing old progress.

Location, language, remembered wording, article count, and activity after 2023 are **not** filters. No travel or place words are used for scoring because the remembered text is uncertain.
Organization-owned Pages sites are excluded because the missing account was a personal account. During the personal-site phase, a repository must be named exactly `owner.github.io`; this avoids spending API requests on unrelated repositories whose names merely contain `github.io`.

The first pass searches personal repositories named `owner.github.io`. Identity-user results then inspect up to 200 public repositories per user and retain every repository with Pages enabled, including project Pages. Later passes search photo/blog/site-like repository names and identity fragments. Date ranges are split adaptively only when needed to avoid GitHub's 1,000-result search ceiling.

## Outputs

- [`candidates.md`](candidates.md): human-readable candidates, highest score first.
- [`candidates.json`](candidates.json): structured candidate evidence.
- [`state.json`](state.json): durable pagination and deduplication state.
- [`progress.md`](progress.md): completed search tasks, investigated accounts, API usage, and the current cursor.

The scheduled workflow commits changes to these files after each run. It runs hourly and can also be started manually from the Actions tab.

## Security and rate limits

The workflow uses only `${{ github.token }}`. Do not add a personal token unless there is a specific reason to share the personal account's API quota. Each run has an explicit core-request budget and throttles both search and ordinary REST requests to reduce secondary-rate-limit failures.

## Manual run

Open **Actions → Search forgotten GitHub Pages account → Run workflow**. The optional request budget defaults to 950. Every scheduled run reads the live API quota first and reserves 30 core requests instead of blindly assuming that the full hourly quota is available.

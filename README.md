# GitHub Account Finder

This private repository incrementally searches for a forgotten personal GitHub
account. The workflow is user-centric: it first finds accounts created during
the target window whose login or public name resembles the remembered identity,
then inspects those users' GitHub Pages repositories.

## Target identity

- Account created between 2023-06-01 and 2023-10-15.
- Likely names include Jessie Liu and Liu Xuan, with components `jess`, `liu`,
  `xuan`, or `jliu`.
- Possible birthday suffixes are `0503`, `110503`, and `20110503`.
- Low-confidence nicknames are retained only as supporting evidence.
- Travel and mountain words are content hints, never identity evidence or hard
  filters.

## Search strategy

Stages run in this order:

1. **Users:** search every configured identity/name/number seed with GitHub's
   `in:login,name`, `created:2023-06-01..2023-10-15`, and `type:user`
   qualifiers. For each result, inspect up to 300 public repositories and keep
   every Pages repository created inside the target 2023 window. Later Pages
   repositories are discarded before tree, commit, profile, or workflow reads.
2. **Identity repository names:** search Pages candidates through repository
   names containing the primary and component name tokens.
3. **Strict personal Pages fallback:** search `github.io in:name` last and only
   admit an identity-free `owner.github.io` repository when the owner account
   was created in the target window, a recognized Actions deployment marker is
   present, and at least one probable photo exists.

The former `blog`, `pages`, and other generic site-name stages have been
removed. They produced broad repository matches but weak identity evidence.

Dense search ranges are split adaptively to stay below GitHub's 1,000-result
search ceiling. Result caps, core/search throttling, retries, request-budget
guards, incremental state, and repository/user de-duplication remain enabled.

## Candidate admission and ranking

A repository is recorded only when it has identity tier 1 or 2, or passes the
strict personal-Pages fallback above. It must also meet the configured minimum
score.

- **Tier 2:** the login contains a combined identity such as `jessieliu`,
  `liujessie`, `liuxuan`, or `xuanliu`; two distinct name families; or a
  name family plus a boundary-safe birthday token.
- **Tier 1:** the login, profile name/bio, or latest commit author contains one
  primary, component, or birthday token.
- **Tier 0:** no identity token; possible only through the strict structural
  fallback.

Reports sort by `(identity tier descending, score descending, dormant signal
descending)`. Thus all identity-bearing candidates appear before structural
fallbacks. Number matching uses digit boundaries so `0503` does not match a
longer unrelated number.

## Outputs

- [`candidates.md`](candidates.md): collapsible human-readable candidates.
- [`candidates.json`](candidates.json): structured evidence.
- [`state.json`](state.json): durable cursors and de-duplication state.
- [`progress.md`](progress.md): overall and per-stage progress.

The scheduled workflow runs hourly and commits changed outputs. Search API calls
use the read-only `SEARCH_PAT` Actions secret when configured and otherwise fall
back to the repository-scoped `${{ github.token }}`. Checkout and result pushes
continue to use `github.token`; the PAT is exposed only to the Python search step.

## Manual run

Open **Actions → Search forgotten GitHub Pages account → Run workflow**. The
optional request budget defaults to 950. Normal operation relies on the hourly
schedule; strategy changes should not manually dispatch a search unless that is
explicitly requested.

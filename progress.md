# Search progress

- Fixed search coverage: **4,359 / 4,384 seed-days (99.4%)**
- Adaptive range diagnostics: **178 / 180 leaf ranges complete**
- Current cursor: `site:travel 2022-09-21..2022-09-28, page 9`
- Repository results seen: **105,897**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **88,557**
- Unique account owners investigated: **79,359**
- Candidates recorded: **1,254**
- Ranges stopped by result caps: **10**
- Workflow runs: **26**
- Last run (UTC): `2026-08-28T14:11:06.025879+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 1,208 / 1,233 seed-days | 98.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

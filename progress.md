# Search progress

- Fixed search coverage: **3,699 / 4,384 seed-days (84.4%)**
- Adaptive range diagnostics: **127 / 133 leaf ranges complete**
- Current cursor: `site:photos 2022-06-01..2022-08-08, page 1`
- Repository results seen: **68,706**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **55,100**
- Unique account owners investigated: **49,822**
- Candidates recorded: **1,230**
- Ranges stopped by result caps: **10**
- Workflow runs: **21**
- Last run (UTC): `2026-08-26T23:35:39.645532+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 548 / 1,233 seed-days | 44.4% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

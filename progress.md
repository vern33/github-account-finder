# Search progress

- Fixed search coverage: **1,285 / 4,384 seed-days (29.3%)**
- Adaptive range diagnostics: **13 / 37 leaf ranges complete**
- Current cursor: `users:liu 2024-07-23..2024-08-08, page 7`
- Repository results seen: **0**
- User search results seen: **4,195**
- Pages repositories found through users: **141**
- Identity users fully checked: **4,049**
- Unique repositories investigated: **141**
- Unique account owners investigated: **95**
- Candidates recorded: **132**
- Ranges stopped by result caps: **0**
- Workflow runs: **1**
- Last run (UTC): `2026-08-29T14:40:16.825192+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,285 / 1,781 seed-days | 72.2% |
| identity: repository names | 0 / 1,233 seed-days | 0.0% |
| personal: strict username.github.io fallback | 0 / 137 seed-days | 0.0% |
| site: project-page blog names | 0 / 1,233 seed-days | 0.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

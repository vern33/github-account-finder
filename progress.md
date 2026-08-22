# Search progress

- Adaptive search ranges: **3 / 25 (12.0%)**
- Current cursor: `users:jesse 2023-06-01..2023-08-08, page 2`
- Repository results seen: **0**
- User search results seen: **711**
- Pages repositories found through users: **134**
- Identity users fully checked: **614**
- Unique repositories investigated: **134**
- Unique account owners investigated: **54**
- Candidates recorded: **133**
- Ranges stopped by result caps: **0**
- Workflow runs: **1**
- Last run (UTC): `2026-08-22T11:36:24.810795+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 3 / 14 | 21.4% |
| identity: repository names | 0 / 10 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

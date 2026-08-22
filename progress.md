# Search progress

- Adaptive search ranges: **7 / 29 (24.1%)**
- Current cursor: `users:liu 2023-06-01..2023-06-09, page 5`
- Repository results seen: **0**
- User search results seen: **2,696**
- Pages repositories found through users: **812**
- Identity users fully checked: **2,268**
- Unique repositories investigated: **618**
- Unique account owners investigated: **174**
- Candidates recorded: **615**
- Ranges stopped by result caps: **0**
- Workflow runs: **4**
- Last run (UTC): `2026-08-22T14:39:58.527514+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 7 / 18 | 38.9% |
| identity: repository names | 0 / 10 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

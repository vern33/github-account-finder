# Search progress

- Adaptive search ranges: **45 / 52 (86.5%)**
- Current cursor: `personal:username.github.io 2023-06-03..2023-06-03, page 8`
- Repository results seen: **7,317**
- User search results seen: **12,545**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,709**
- Unique repositories investigated: **6,335**
- Unique account owners investigated: **4,955**
- Candidates recorded: **1,140**
- Ranges stopped by result caps: **2**
- Workflow runs: **6**
- Last run (UTC): `2026-08-23T04:53:07.959941+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 2 / 9 | 22.2% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

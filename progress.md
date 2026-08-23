# Search progress

- Adaptive search ranges: **47 / 53 (88.7%)**
- Current cursor: `personal:username.github.io 2023-06-05..2023-06-05, page 10`
- Repository results seen: **9,617**
- User search results seen: **12,545**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,709**
- Unique repositories investigated: **7,608**
- Unique account owners investigated: **6,227**
- Candidates recorded: **1,150**
- Ranges stopped by result caps: **2**
- Workflow runs: **7**
- Last run (UTC): `2026-08-23T05:46:45.246610+00:00`
- Last API requests used: **3,538**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 4 / 10 | 40.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

# Search progress

- Adaptive search ranges: **71 / 76 (93.4%)**
- Current cursor: `personal:username.github.io 2023-06-29..2023-06-29, page 4`
- Repository results seen: **33,917**
- User search results seen: **12,546**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,710**
- Unique repositories investigated: **21,315**
- Unique account owners investigated: **19,931**
- Candidates recorded: **1,263**
- Ranges stopped by result caps: **2**
- Workflow runs: **16**
- Last run (UTC): `2026-08-23T14:41:56.179947+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 28 / 33 | 84.8% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

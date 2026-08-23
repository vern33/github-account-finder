# Search progress

- Adaptive search ranges: **60 / 64 (93.8%)**
- Current cursor: `personal:username.github.io 2023-06-18..2023-06-18, page 10`
- Repository results seen: **23,117**
- User search results seen: **12,546**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,710**
- Unique repositories investigated: **15,194**
- Unique account owners investigated: **13,811**
- Candidates recorded: **1,207**
- Ranges stopped by result caps: **2**
- Workflow runs: **12**
- Last run (UTC): `2026-08-23T10:42:39.543511+00:00`
- Last API requests used: **4,413**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 17 / 21 | 81.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

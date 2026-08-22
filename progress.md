# Search progress

- Adaptive search ranges: **9 / 29 (31.0%)**
- Current cursor: `users:liu 2023-07-06..2023-07-14, page 3`
- Repository results seen: **0**
- User search results seen: **3,054**
- Pages repositories found through users: **399**
- Identity users fully checked: **2,738**
- Unique repositories investigated: **387**
- Unique account owners investigated: **177**
- Candidates recorded: **379**
- Ranges stopped by result caps: **0**
- Workflow runs: **4**
- Last run (UTC): `2026-08-22T18:49:57.380667+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 9 / 19 | 47.4% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

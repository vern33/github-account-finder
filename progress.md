# Search progress

- Adaptive search ranges: **16 / 32 (50.0%)**
- Current cursor: `users:xuan 2023-08-09..2023-10-15, page 1`
- Repository results seen: **0**
- User search results seen: **6,075**
- Pages repositories found through users: **872**
- Identity users fully checked: **5,301**
- Unique repositories investigated: **830**
- Unique account owners investigated: **379**
- Candidates recorded: **785**
- Ranges stopped by result caps: **2**
- Workflow runs: **8**
- Last run (UTC): `2026-08-22T22:39:40.626465+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 16 / 22 | 72.7% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

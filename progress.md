# Search progress

- Adaptive search ranges: **15 / 32 (46.9%)**
- Current cursor: `users:xuan 2023-06-01..2023-08-08, page 1`
- Repository results seen: **0**
- User search results seen: **5,276**
- Pages repositories found through users: **762**
- Identity users fully checked: **4,648**
- Unique repositories investigated: **721**
- Unique account owners investigated: **323**
- Candidates recorded: **698**
- Ranges stopped by result caps: **2**
- Workflow runs: **7**
- Last run (UTC): `2026-08-22T21:37:10.376699+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 15 / 22 | 68.2% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

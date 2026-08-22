# Search progress

- Adaptive search ranges: **12 / 31 (38.7%)**
- Current cursor: `users:liu 2023-08-09..2023-08-25, page 1`
- Repository results seen: **0**
- User search results seen: **4,678**
- Pages repositories found through users: **616**
- Identity users fully checked: **4,090**
- Unique repositories investigated: **577**
- Unique account owners investigated: **256**
- Candidates recorded: **564**
- Ranges stopped by result caps: **0**
- Workflow runs: **6**
- Last run (UTC): `2026-08-22T20:41:31.771141+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 12 / 21 | 57.1% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

# Search progress

- Adaptive search ranges: **11 / 29 (37.9%)**
- Current cursor: `users:liu 2023-07-23..2023-08-08, page 1`
- Repository results seen: **0**
- User search results seen: **3,880**
- Pages repositories found through users: **496**
- Identity users fully checked: **3,420**
- Unique repositories investigated: **483**
- Unique account owners investigated: **216**
- Candidates recorded: **472**
- Ranges stopped by result caps: **0**
- Workflow runs: **5**
- Last run (UTC): `2026-08-22T19:36:51.962761+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 11 / 19 | 57.9% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

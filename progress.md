# Search progress

- Adaptive search ranges: **8 / 27 (29.6%)**
- Current cursor: `users:liu 2023-06-28..2023-07-05, page 1`
- Repository results seen: **0**
- User search results seen: **2,356**
- Pages repositories found through users: **296**
- Identity users fully checked: **2,066**
- Unique repositories investigated: **287**
- Unique account owners investigated: **123**
- Candidates recorded: **282**
- Ranges stopped by result caps: **0**
- Workflow runs: **3**
- Last run (UTC): `2026-08-22T17:37:18.537042+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 8 / 17 | 47.1% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

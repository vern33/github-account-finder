# Search progress

- Adaptive search ranges: **5 / 26 (19.2%)**
- Current cursor: `users:liu 2023-06-01..2023-06-09, page 1`
- Repository results seen: **0**
- User search results seen: **704**
- Pages repositories found through users: **141**
- Identity users fully checked: **604**
- Unique repositories investigated: **138**
- Unique account owners investigated: **47**
- Candidates recorded: **136**
- Ranges stopped by result caps: **0**
- Workflow runs: **1**
- Last run (UTC): `2026-08-22T15:36:20.154810+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 5 / 16 | 31.2% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

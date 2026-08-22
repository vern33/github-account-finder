# Search progress

- Adaptive search ranges: **6 / 26 (23.1%)**
- Current cursor: `users:liu 2023-06-10..2023-06-18, page 2`
- Repository results seen: **0**
- User search results seen: **1,502**
- Pages repositories found through users: **218**
- Identity users fully checked: **1,315**
- Unique repositories investigated: **215**
- Unique account owners investigated: **90**
- Candidates recorded: **212**
- Ranges stopped by result caps: **0**
- Workflow runs: **2**
- Last run (UTC): `2026-08-22T16:42:41.469645+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 6 / 16 | 37.5% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

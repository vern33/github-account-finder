# Search progress

- Adaptive search ranges: **4 / 25 (16.0%)**
- Current cursor: `users:jesse 2023-08-09..2023-10-15, page 1`
- Repository results seen: **0**
- User search results seen: **1,356**
- Pages repositories found through users: **407**
- Identity users fully checked: **1,124**
- Unique repositories investigated: **315**
- Unique account owners investigated: **76**
- Candidates recorded: **314**
- Ranges stopped by result caps: **0**
- Workflow runs: **2**
- Last run (UTC): `2026-08-22T13:02:30.084892+00:00`
- Last API requests used: **950**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 4 / 14 | 28.6% |
| identity: repository names | 0 / 10 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

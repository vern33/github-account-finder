# Search progress

- Adaptive search ranges: **35 / 41 (85.4%)**
- Current cursor: `identity:jess 2023-06-01..2023-08-08, page 7`
- Repository results seen: **855**
- User search results seen: **12,545**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,709**
- Unique repositories investigated: **1,441**
- Unique account owners investigated: **923**
- Candidates recorded: **781**
- Ranges stopped by result caps: **2**
- Workflow runs: **4**
- Last run (UTC): `2026-08-23T03:16:31.048459+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 5 / 10 | 50.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

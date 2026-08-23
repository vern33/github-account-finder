# Search progress

- Adaptive search ranges: **58 / 63 (92.1%)**
- Current cursor: `personal:username.github.io 2023-06-16..2023-06-16, page 2`
- Repository results seen: **20,217**
- User search results seen: **12,546**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,710**
- Unique repositories investigated: **13,601**
- Unique account owners investigated: **12,219**
- Candidates recorded: **1,198**
- Ranges stopped by result caps: **2**
- Workflow runs: **11**
- Last run (UTC): `2026-08-23T09:44:38.113426+00:00`
- Last API requests used: **4,041**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 15 / 20 | 75.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

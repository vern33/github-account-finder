# Search progress

- Adaptive search ranges: **63 / 69 (91.3%)**
- Current cursor: `personal:username.github.io 2023-06-21..2023-06-21, page 7`
- Repository results seen: **25,917**
- User search results seen: **12,546**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,710**
- Unique repositories investigated: **16,791**
- Unique account owners investigated: **15,407**
- Candidates recorded: **1,221**
- Ranges stopped by result caps: **2**
- Workflow runs: **13**
- Last run (UTC): `2026-08-23T11:36:30.421838+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 20 / 26 | 76.9% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

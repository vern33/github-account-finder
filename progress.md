# Search progress

- Adaptive search ranges: **52 / 60 (86.7%)**
- Current cursor: `personal:username.github.io 2023-06-10..2023-06-10, page 9`
- Repository results seen: **14,717**
- User search results seen: **12,546**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,710**
- Unique repositories investigated: **10,493**
- Unique account owners investigated: **9,111**
- Candidates recorded: **1,173**
- Ranges stopped by result caps: **2**
- Workflow runs: **9**
- Last run (UTC): `2026-08-23T07:48:29.561773+00:00`
- Last API requests used: **3,542**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 9 / 17 | 52.9% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

# Search progress

- Adaptive search ranges: **66 / 72 (91.7%)**
- Current cursor: `personal:username.github.io 2023-06-24..2023-06-24, page 5`
- Repository results seen: **28,817**
- User search results seen: **12,546**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,710**
- Unique repositories investigated: **18,432**
- Unique account owners investigated: **17,048**
- Candidates recorded: **1,241**
- Ranges stopped by result caps: **2**
- Workflow runs: **14**
- Last run (UTC): `2026-08-23T13:03:22.587035+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 23 / 29 | 79.3% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

# Search progress

- Adaptive search ranges: **67 / 85 (78.8%)**
- Current cursor: `personal:username.github.io 2023-06-25..2023-06-25, page 3`
- Repository results seen: **29,376**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **18,859**
- Unique account owners investigated: **17,475**
- Candidates recorded: **1,333**
- Ranges stopped by result caps: **2**
- Workflow runs: **11**
- Last run (UTC): `2026-08-24T03:17:30.597256+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 24 / 29 | 82.8% |
| site: project-page blog names | 0 / 13 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

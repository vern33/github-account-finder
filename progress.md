# Search progress

- Adaptive search ranges: **23 / 37 (62.2%)**
- Current cursor: `users:jess 2023-07-06..2023-07-22, page 2`
- Repository results seen: **0**
- User search results seen: **8,668**
- Pages repositories found through users: **457**
- Identity users fully checked: **8,257**
- Unique repositories investigated: **457**
- Unique account owners investigated: **250**
- Candidates recorded: **445**
- Ranges stopped by result caps: **2**
- Workflow runs: **3**
- Last run (UTC): `2026-08-23T02:00:32.805088+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 23 / 27 | 85.2% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

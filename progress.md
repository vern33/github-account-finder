# Search progress

- Adaptive search ranges: **23 / 50 (46.0%)**
- Current cursor: `users:jess 2023-07-06..2023-07-22, page 2`
- Repository results seen: **0**
- User search results seen: **8,924**
- Pages repositories found through users: **458**
- Identity users fully checked: **8,505**
- Unique repositories investigated: **458**
- Unique account owners investigated: **251**
- Candidates recorded: **448**
- Ranges stopped by result caps: **2**
- Workflow runs: **3**
- Last run (UTC): `2026-08-23T17:35:58.959633+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 23 / 27 | 85.2% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |
| site: project-page blog names | 0 / 13 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

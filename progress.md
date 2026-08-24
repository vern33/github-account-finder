# Search progress

- Adaptive search ranges: **119 / 131 (90.8%)**
- Current cursor: `site:hugo 2023-09-12..2023-09-28, page 3`
- Repository results seen: **58,670**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **45,780**
- Unique account owners investigated: **41,566**
- Candidates recorded: **1,405**
- Ranges stopped by result caps: **13**
- Workflow runs: **15**
- Last run (UTC): `2026-08-24T09:05:46.712803+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 33 / 33 | 100.0% |
| site: project-page blog names | 43 / 55 | 78.2% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

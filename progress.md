# Search progress

- Adaptive search ranges: **154 / 162 (95.1%)**
- Current cursor: `site:gallery 2023-08-26..2023-09-03, page 1`
- Repository results seen: **82,665**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **66,248**
- Unique account owners investigated: **59,395**
- Candidates recorded: **1,435**
- Ranges stopped by result caps: **13**
- Workflow runs: **18**
- Last run (UTC): `2026-08-24T11:45:17.975225+00:00`
- Last API requests used: **3,622**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 33 / 33 | 100.0% |
| site: project-page blog names | 78 / 86 | 90.7% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

# Search progress

- Adaptive search ranges: **145 / 154 (94.2%)**
- Current cursor: `site:gallery 2023-06-10..2023-06-18, page 1`
- Repository results seen: **77,068**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **61,461**
- Unique account owners investigated: **55,287**
- Candidates recorded: **1,430**
- Ranges stopped by result caps: **13**
- Workflow runs: **17**
- Last run (UTC): `2026-08-24T10:54:43.239546+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 33 / 33 | 100.0% |
| site: project-page blog names | 69 / 78 | 88.5% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

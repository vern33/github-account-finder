# Search progress

- Adaptive search ranges: **93 / 112 (83.0%)**
- Current cursor: `site:blog 2023-06-20..2023-06-20, page 5`
- Repository results seen: **45,763**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **32,978**
- Unique account owners investigated: **30,493**
- Candidates recorded: **1,388**
- Ranges stopped by result caps: **6**
- Workflow runs: **14**
- Last run (UTC): `2026-08-24T07:30:03.470128+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 33 / 33 | 100.0% |
| site: project-page blog names | 17 / 36 | 47.2% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

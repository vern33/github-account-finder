# Search progress

- Adaptive search ranges: **133 / 142 (93.7%)**
- Current cursor: `site:photo 2023-08-01..2023-08-08, page 6`
- Repository results seen: **68,151**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **54,060**
- Unique account owners investigated: **48,809**
- Candidates recorded: **1,425**
- Ranges stopped by result caps: **13**
- Workflow runs: **16**
- Last run (UTC): `2026-08-24T10:05:26.195328+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 33 / 33 | 100.0% |
| site: project-page blog names | 57 / 66 | 86.4% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

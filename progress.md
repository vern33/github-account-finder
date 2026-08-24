# Search progress

- Adaptive search ranges: **164 / 173 (94.8%)**
- Current cursor: `site:travel 2023-06-19..2023-06-23, page 6`
- Repository results seen: **90,003**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **72,984**
- Unique account owners investigated: **65,239**
- Candidates recorded: **1,443**
- Ranges stopped by result caps: **13**
- Workflow runs: **19**
- Last run (UTC): `2026-08-24T12:20:42.618832+00:00`
- Last API requests used: **4,289**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 33 / 33 | 100.0% |
| site: project-page blog names | 88 / 97 | 90.7% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

# Search progress

- Adaptive search ranges: **15 / 43 (34.9%)**
- Current cursor: `users:liu 2023-07-23..2023-08-08, page 9`
- Repository results seen: **0**
- User search results seen: **4,813**
- Pages repositories found through users: **174**
- Identity users fully checked: **4,639**
- Unique repositories investigated: **174**
- Unique account owners investigated: **102**
- Candidates recorded: **172**
- Ranges stopped by result caps: **0**
- Workflow runs: **2**
- Last run (UTC): `2026-08-23T16:44:22.590530+00:00`
- Last API requests used: **569**
- Last stop reason: `rate limit reset=1787505052`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 15 / 20 | 75.0% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |
| site: project-page blog names | 0 / 13 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

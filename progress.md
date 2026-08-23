# Search progress

- Adaptive search ranges: **76 / 76 (100.0%)**
- Current cursor: `complete`
- Repository results seen: **34,617**
- User search results seen: **12,546**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,710**
- Unique repositories investigated: **21,691**
- Unique account owners investigated: **20,307**
- Candidates recorded: **1,265**
- Ranges stopped by result caps: **6**
- Workflow runs: **17**
- Last run (UTC): `2026-08-23T15:38:19.847700+00:00`
- Last API requests used: **1,050**
- Last stop reason: `none`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 33 / 33 | 100.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

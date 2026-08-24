# Search progress

- Adaptive search ranges: **71 / 89 (79.8%)**
- Current cursor: `personal:username.github.io 2023-06-29..2023-06-29, page 8`
- Repository results seen: **34,076**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **21,519**
- Unique account owners investigated: **20,135**
- Candidates recorded: **1,370**
- Ranges stopped by result caps: **2**
- Workflow runs: **13**
- Last run (UTC): `2026-08-24T05:54:34.423944+00:00`
- Last API requests used: **602**
- Last stop reason: `rate limit reset=1787551384`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 28 / 33 | 84.8% |
| site: project-page blog names | 0 / 13 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

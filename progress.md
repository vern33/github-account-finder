# Search progress

- Adaptive search ranges: **40 / 57 (70.2%)**
- Current cursor: `identity:liu 2023-09-12..2023-10-15, page 3`
- Repository results seen: **3,635**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **4,003**
- Unique account owners investigated: **2,912**
- Candidates recorded: **1,072**
- Ranges stopped by result caps: **2**
- Workflow runs: **5**
- Last run (UTC): `2026-08-23T19:36:55.108927+00:00`
- Last API requests used: **596**
- Last stop reason: `rate limit reset=1787514579`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 10 / 13 | 76.9% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |
| site: project-page blog names | 0 / 13 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

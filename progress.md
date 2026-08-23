# Search progress

- Adaptive search ranges: **40 / 44 (90.9%)**
- Current cursor: `identity:liu 2023-09-12..2023-10-15, page 4`
- Repository results seen: **3,676**
- User search results seen: **12,545**
- Pages repositories found through users: **712**
- Identity users fully checked: **11,709**
- Unique repositories investigated: **4,012**
- Unique account owners investigated: **2,919**
- Candidates recorded: **1,061**
- Ranges stopped by result caps: **2**
- Workflow runs: **5**
- Last run (UTC): `2026-08-23T04:05:13.546702+00:00`
- Last API requests used: **1,176**
- Last stop reason: `rate limit reset=1787458591`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 10 / 13 | 76.9% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

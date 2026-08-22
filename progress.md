# Search progress

- Adaptive search ranges: **16 / 32 (50.0%)**
- Current cursor: `users:liu 2023-08-09..2023-08-25, page 1`
- Repository results seen: **0**
- User search results seen: **4,730**
- Pages repositories found through users: **175**
- Identity users fully checked: **4,528**
- Unique repositories investigated: **175**
- Unique account owners investigated: **103**
- Candidates recorded: **172**
- Ranges stopped by result caps: **0**
- Workflow runs: **2**
- Last run (UTC): `2026-08-22T23:36:24.045942+00:00`
- Last API requests used: **563**
- Last stop reason: `rate limit reset=1787442024`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 16 / 22 | 72.7% |
| identity: repository names | 0 / 9 | 0.0% |
| personal: strict username.github.io fallback | 0 / 1 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

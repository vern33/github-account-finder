# Search progress

- Adaptive search ranges: **54 / 73 (74.0%)**
- Current cursor: `personal:username.github.io 2023-06-12..2023-06-12, page 9`
- Repository results seen: **16,676**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **11,746**
- Unique account owners investigated: **10,364**
- Candidates recorded: **1,238**
- Ranges stopped by result caps: **2**
- Workflow runs: **8**
- Last run (UTC): `2026-08-23T22:39:31.599472+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 30 / 30 | 100.0% |
| identity: repository names | 13 / 13 | 100.0% |
| personal: strict username.github.io fallback | 11 / 17 | 64.7% |
| site: project-page blog names | 0 / 13 | 0.0% |

Each seed starts with the configured account-creation window. A range is split only when GitHub
reports more than 1,000 results, so the denominator may grow while a dense
range is being subdivided. Already investigated repositories are never
inspected again.

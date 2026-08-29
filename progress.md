# Search progress

- Fixed search coverage: **1,627 / 4,384 seed-days (37.1%)**
- Adaptive range diagnostics: **27 / 48 leaf ranges complete**
- Current cursor: `users:jess 2024-09-29..2024-10-15, page 7`
- Repository results seen: **0**
- User search results seen: **12,542**
- Pages repositories found through users: **630**
- Identity users fully checked: **11,658**
- Unique repositories investigated: **630**
- Unique account owners investigated: **385**
- Candidates recorded: **599**
- Ranges stopped by result caps: **2**
- Workflow runs: **3**
- Last run (UTC): `2026-08-29T21:46:10.317360+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,627 / 1,781 seed-days | 91.4% |
| identity: repository names | 0 / 1,233 seed-days | 0.0% |
| personal: strict username.github.io fallback | 0 / 137 seed-days | 0.0% |
| site: project-page blog names | 0 / 1,233 seed-days | 0.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

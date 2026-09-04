# Search progress

- Fixed search coverage: **4,384 / 4,384 seed-days (100.0%)**
- Adaptive range diagnostics: **188 / 188 leaf ranges complete**
- Current cursor: `complete`
- Repository results seen: **109,503**
- User search results seen: **12,621**
- Pages repositories found through users: **630**
- Identity users fully checked: **11,724**
- Unique repositories investigated: **92,170**
- Unique account owners investigated: **81,496**
- Candidates recorded: **1,493**
- Ranges stopped by result caps: **12**
- Workflow runs: **32**
- Last run (UTC): `2026-09-04T05:56:44.355908+00:00`
- Last API requests used: **1**
- Last stop reason: `none`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 1,233 / 1,233 seed-days | 100.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

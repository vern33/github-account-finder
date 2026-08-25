# Search progress

- Fixed search coverage: **2,466 / 4,384 seed-days (56.2%)**
- Adaptive range diagnostics: **33 / 48 leaf ranges complete**
- Current cursor: `identity:jess 2022-06-01..2022-08-08, page 5`
- Repository results seen: **665**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **1,229**
- Unique account owners investigated: **818**
- Candidates recorded: **702**
- Ranges stopped by result caps: **2**
- Workflow runs: **4**
- Last run (UTC): `2026-08-25T15:07:07.997559+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 685 / 1,233 seed-days | 55.6% |
| personal: strict username.github.io fallback | 0 / 137 seed-days | 0.0% |
| site: project-page blog names | 0 / 1,233 seed-days | 0.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

# Search progress

- Fixed search coverage: **4,316 / 4,384 seed-days (98.4%)**
- Adaptive range diagnostics: **176 / 181 leaf ranges complete**
- Current cursor: `site:travel 2023-08-09..2023-08-13, page 5`
- Repository results seen: **98,503**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **81,304**
- Unique account owners investigated: **72,542**
- Candidates recorded: **1,451**
- Ranges stopped by result caps: **13**
- Workflow runs: **20**
- Last run (UTC): `2026-08-24T13:01:33.850927+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 1,165 / 1,233 seed-days | 94.5% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

# Search progress

- Fixed search coverage: **3,155 / 4,384 seed-days (72.0%)**
- Adaptive range diagnostics: **80 / 94 leaf ranges complete**
- Current cursor: `site:blog 2024-06-05..2024-06-05, page 2`
- Repository results seen: **38,289**
- User search results seen: **12,621**
- Pages repositories found through users: **630**
- Identity users fully checked: **11,724**
- Unique repositories investigated: **25,538**
- Unique account owners investigated: **23,984**
- Candidates recorded: **1,403**
- Ranges stopped by result caps: **6**
- Workflow runs: **15**
- Last run (UTC): `2026-09-01T10:11:41.553876+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 4 / 1,233 seed-days | 0.3% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

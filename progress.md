# Search progress

- Fixed search coverage: **3,425 / 4,384 seed-days (78.1%)**
- Adaptive range diagnostics: **112 / 121 leaf ranges complete**
- Current cursor: `site:hugo 2024-06-01..2024-07-05, page 5`
- Repository results seen: **57,795**
- User search results seen: **12,621**
- Pages repositories found through users: **630**
- Identity users fully checked: **11,724**
- Unique repositories investigated: **44,723**
- Unique account owners investigated: **40,555**
- Candidates recorded: **1,420**
- Ranges stopped by result caps: **9**
- Workflow runs: **17**
- Last run (UTC): `2026-09-01T18:34:42.396117+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 274 / 1,233 seed-days | 22.2% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

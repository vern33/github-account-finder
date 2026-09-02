# Search progress

- Fixed search coverage: **3,965 / 4,384 seed-days (90.4%)**
- Adaptive range diagnostics: **136 / 140 leaf ranges complete**
- Current cursor: `site:photo 2024-10-08..2024-10-15, page 3`
- Repository results seen: **75,404**
- User search results seen: **12,621**
- Pages repositories found through users: **630**
- Identity users fully checked: **11,724**
- Unique repositories investigated: **60,123**
- Unique account owners investigated: **53,817**
- Candidates recorded: **1,466**
- Ranges stopped by result caps: **9**
- Workflow runs: **19**
- Last run (UTC): `2026-09-02T00:17:25.154430+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 814 / 1,233 seed-days | 66.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

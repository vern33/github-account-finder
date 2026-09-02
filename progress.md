# Search progress

- Fixed search coverage: **4,179 / 4,384 seed-days (95.3%)**
- Adaptive range diagnostics: **147 / 152 leaf ranges complete**
- Current cursor: `site:gallery 2024-08-09..2024-08-17, page 2`
- Repository results seen: **83,195**
- User search results seen: **12,621**
- Pages repositories found through users: **630**
- Identity users fully checked: **11,724**
- Unique repositories investigated: **66,884**
- Unique account owners investigated: **59,755**
- Candidates recorded: **1,470**
- Ranges stopped by result caps: **9**
- Workflow runs: **20**
- Last run (UTC): `2026-09-02T05:52:05.665372+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 1,028 / 1,233 seed-days | 83.4% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

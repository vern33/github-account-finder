# Search progress

- Fixed search coverage: **4,333 / 4,384 seed-days (98.8%)**
- Adaptive range diagnostics: **179 / 184 leaf ranges complete**
- Current cursor: `site:travel 2024-08-26..2024-08-28, page 3`
- Repository results seen: **105,629**
- User search results seen: **12,621**
- Pages repositories found through users: **630**
- Identity users fully checked: **11,724**
- Unique repositories investigated: **88,312**
- Unique account owners investigated: **78,208**
- Candidates recorded: **1,491**
- Ranges stopped by result caps: **9**
- Workflow runs: **23**
- Last run (UTC): `2026-09-02T19:49:02.506013+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 1,182 / 1,233 seed-days | 95.9% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

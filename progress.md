# Search progress

- Fixed search coverage: **3,164 / 4,384 seed-days (72.2%)**
- Adaptive range diagnostics: **89 / 102 leaf ranges complete**
- Current cursor: `site:blog 2022-06-14..2022-06-14, page 1`
- Repository results seen: **46,976**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **33,742**
- Unique account owners investigated: **31,605**
- Candidates recorded: **1,211**
- Ranges stopped by result caps: **5**
- Workflow runs: **19**
- Last run (UTC): `2026-08-26T17:33:16.174355+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 13 / 1,233 seed-days | 1.1% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

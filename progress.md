# Search progress

- Fixed search coverage: **4,128 / 4,384 seed-days (94.2%)**
- Adaptive range diagnostics: **148 / 152 leaf ranges complete**
- Current cursor: `site:gallery 2022-06-19..2022-07-05, page 8`
- Repository results seen: **85,719**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **69,582**
- Unique account owners investigated: **62,730**
- Candidates recorded: **1,240**
- Ranges stopped by result caps: **10**
- Workflow runs: **23**
- Last run (UTC): `2026-08-27T15:48:50.000865+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 977 / 1,233 seed-days | 79.2% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

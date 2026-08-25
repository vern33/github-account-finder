# Search progress

- Fixed search coverage: **3,029 / 4,384 seed-days (69.1%)**
- Adaptive range diagnostics: **56 / 70 leaf ranges complete**
- Current cursor: `personal:username.github.io 2022-06-16..2022-06-16, page 8`
- Repository results seen: **21,595**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **15,712**
- Unique account owners investigated: **14,158**
- Candidates recorded: **1,117**
- Ranges stopped by result caps: **2**
- Workflow runs: **11**
- Last run (UTC): `2026-08-25T21:45:05.657684+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 15 / 137 seed-days | 10.9% |
| site: project-page blog names | 0 / 1,233 seed-days | 0.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

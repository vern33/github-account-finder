# Search progress

- Fixed search coverage: **1,525 / 4,384 seed-days (34.8%)**
- Adaptive range diagnostics: **20 / 43 leaf ranges complete**
- Current cursor: `users:jess 2022-06-19..2022-07-05, page 4`
- Repository results seen: **0**
- User search results seen: **8,112**
- Pages repositories found through users: **461**
- Identity users fully checked: **7,721**
- Unique repositories investigated: **460**
- Unique account owners investigated: **228**
- Candidates recorded: **430**
- Ranges stopped by result caps: **2**
- Workflow runs: **3**
- Last run (UTC): `2026-08-25T14:06:09.908018+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,525 / 1,781 seed-days | 85.6% |
| identity: repository names | 0 / 1,233 seed-days | 0.0% |
| personal: strict username.github.io fallback | 0 / 137 seed-days | 0.0% |
| site: project-page blog names | 0 / 1,233 seed-days | 0.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

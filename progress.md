# Search progress

- Fixed search coverage: **3,026 / 4,384 seed-days (69.0%)**
- Adaptive range diagnostics: **54 / 69 leaf ranges complete**
- Current cursor: `personal:username.github.io 2024-06-13..2024-06-13, page 3`
- Repository results seen: **17,394**
- User search results seen: **12,621**
- Pages repositories found through users: **630**
- Identity users fully checked: **11,724**
- Unique repositories investigated: **12,234**
- Unique account owners investigated: **10,829**
- Candidates recorded: **1,161**
- Ranges stopped by result caps: **2**
- Workflow runs: **8**
- Last run (UTC): `2026-08-30T21:09:42.332778+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 12 / 137 seed-days | 8.8% |
| site: project-page blog names | 0 / 1,233 seed-days | 0.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

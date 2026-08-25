# Search progress

- Fixed search coverage: **3,020 / 4,384 seed-days (68.9%)**
- Adaptive range diagnostics: **47 / 62 leaf ranges complete**
- Current cursor: `personal:username.github.io 2022-06-07..2022-06-07, page 1`
- Repository results seen: **11,495**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **9,420**
- Unique account owners investigated: **7,867**
- Candidates recorded: **1,082**
- Ranges stopped by result caps: **2**
- Workflow runs: **7**
- Last run (UTC): `2026-08-25T17:46:31.668791+00:00`
- Last API requests used: **4,196**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 6 / 137 seed-days | 4.4% |
| site: project-page blog names | 0 / 1,233 seed-days | 0.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

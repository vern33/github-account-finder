# Search progress

- Fixed search coverage: **3,015 / 4,384 seed-days (68.8%)**
- Adaptive range diagnostics: **42 / 59 leaf ranges complete**
- Current cursor: `personal:username.github.io 2022-06-02..2022-06-02, page 7`
- Repository results seen: **6,895**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **6,534**
- Unique account owners investigated: **4,984**
- Candidates recorded: **1,065**
- Ranges stopped by result caps: **2**
- Workflow runs: **5**
- Last run (UTC): `2026-08-25T16:01:47.246075+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 1 / 137 seed-days | 0.7% |
| site: project-page blog names | 0 / 1,233 seed-days | 0.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

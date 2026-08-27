# Search progress

- Fixed search coverage: **3,914 / 4,384 seed-days (89.3%)**
- Adaptive range diagnostics: **138 / 144 leaf ranges complete**
- Current cursor: `site:photo 2022-08-18..2022-08-25, page 3`
- Repository results seen: **77,412**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **62,654**
- Unique account owners investigated: **56,616**
- Candidates recorded: **1,234**
- Ranges stopped by result caps: **10**
- Workflow runs: **22**
- Last run (UTC): `2026-08-27T09:51:56.676679+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 763 / 1,233 seed-days | 61.9% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

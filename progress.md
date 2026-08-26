# Search progress

- Fixed search coverage: **3,187 / 4,384 seed-days (72.7%)**
- Adaptive range diagnostics: **107 / 122 leaf ranges complete**
- Current cursor: `site:blog 2022-07-07..2022-07-07, page 4`
- Repository results seen: **59,216**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **45,830**
- Unique account owners investigated: **42,171**
- Candidates recorded: **1,219**
- Ranges stopped by result caps: **5**
- Workflow runs: **20**
- Last run (UTC): `2026-08-26T19:19:47.469652+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 36 / 1,233 seed-days | 2.9% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

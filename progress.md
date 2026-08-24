# Search progress

- Fixed search coverage: **4,372 / 4,384 seed-days (99.7%)**
- Adaptive range diagnostics: **189 / 191 leaf ranges complete**
- Current cursor: `site:travel 2023-10-04..2023-10-07, page 5`
- Repository results seen: **107,173**
- User search results seen: **12,803**
- Pages repositories found through users: **713**
- Identity users fully checked: **11,967**
- Unique repositories investigated: **89,886**
- Unique account owners investigated: **79,960**
- Candidates recorded: **1,462**
- Ranges stopped by result caps: **13**
- Workflow runs: **21**
- Last run (UTC): `2026-08-24T14:03:05.758421+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 1,221 / 1,233 seed-days | 99.0% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

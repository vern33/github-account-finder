# Search progress

- Fixed search coverage: **4,256 / 4,384 seed-days (97.1%)**
- Adaptive range diagnostics: **159 / 164 leaf ranges complete**
- Current cursor: `site:travel 2022-06-10..2022-06-14, page 4`
- Repository results seen: **93,014**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **75,897**
- Unique account owners investigated: **68,278**
- Candidates recorded: **1,246**
- Ranges stopped by result caps: **10**
- Workflow runs: **24**
- Last run (UTC): `2026-08-27T20:32:09.270203+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 1,105 / 1,233 seed-days | 89.6% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

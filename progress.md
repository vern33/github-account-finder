# Search progress

- Fixed search coverage: **4,308 / 4,384 seed-days (98.3%)**
- Adaptive range diagnostics: **169 / 171 leaf ranges complete**
- Current cursor: `site:travel 2022-08-01..2022-08-08, page 4`
- Repository results seen: **99,393**
- User search results seen: **12,137**
- Pages repositories found through users: **704**
- Identity users fully checked: **11,343**
- Unique repositories investigated: **82,155**
- Unique account owners investigated: **73,749**
- Candidates recorded: **1,249**
- Ranges stopped by result caps: **10**
- Workflow runs: **25**
- Last run (UTC): `2026-08-28T05:25:35.019625+00:00`
- Last API requests used: **4,500**
- Last stop reason: `request budget exhausted`

## Progress by stage

| Stage | Completed | Progress |
|---|---:|---:|
| users: login/profile name + account created date | 1,781 / 1,781 seed-days | 100.0% |
| identity: repository names | 1,233 / 1,233 seed-days | 100.0% |
| personal: strict username.github.io fallback | 137 / 137 seed-days | 100.0% |
| site: project-page blog names | 1,157 / 1,233 seed-days | 93.8% |

The main percentage uses a fixed denominator: one unit per seed per day in the configured
account-creation window. Adaptive leaf ranges may still increase when GitHub reports more than
1,000 results, but that diagnostic count no longer changes or reduces the displayed coverage.
Already investigated repositories are never inspected again.

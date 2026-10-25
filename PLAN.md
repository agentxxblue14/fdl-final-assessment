# FDL Development Plan, Timeline and Cost Estimate

Prepared by Judah Rivera for the Lead Developer final assessment, 26 October 2026.
Based on: FDL Technical Master Sheet, Candidate Edition (extract of Master Feature Specification v6, 23 October 2026).

All hours, dates and cost totals below come from one script, [`plan/estimate_model.py`](plan/estimate_model.py). Change an assumption there (start date, weekly capacity, who does what, contingency) and rerun it to see how the calendar moves. Milestone dates are the Friday of the week the work finishes.

## The short answer

| Question | Answer |
|---|---|
| 1. Total development hours | **About 6,800 hours realistic** (range 3,850 to 9,300), covering every feature in the Master Sheet, including native apps and AI features. Realistic split: Lead about 2,900 h, Technical Assistant about 3,300 h, mobile contractor about 630 h. |
| 2. Total timeline | **About 102 weeks, roughly 23 months, realistic** (range 52 to 158 weeks, about 12 to 36 months) with a Lead Developer, one Technical Assistant and a mobile contractor for the native apps. |
| 3. Phase plan | 9 phases, 25 workstreams, 5 milestones. See "Phase-by-phase plan". |
| 4. First customer-ready version | **Internal pilot for the owner's own company: about week 25 (30 April 2027).** Version 1 that outside companies can sign up for and pay: **about week 53 (12 November 2027).** |
| 5. Entire platform complete | **About week 102 (20 October 2028) realistic.** 5 November 2027 at best, 16 November 2029 if the conservative case happens. |
| 6. Lead vs Technical Assistant | Lead owns architecture, security, money logic, integrations, every code review and every release. TA builds screens and forms from written tickets, writes tests and does QA. See "Who does what". |
| 7. AI tools | Claude Code and Replit Agent for building, ChatGPT for requirements (as the Master Sheet already uses it), a separate AI review pass on every change. Quality comes from tests, CI and human review, not from trusting AI output. |
| 8. Monthly technical costs | **About $260 to $650 a month while building**, about $350 to $1,400 a month once live with first customers, then usage-based items (AI document processing, SMS, maps) that grow with customers. One-time and outside-people costs (mobile contractor, adviser, designer, security test, legal): **about $16,000 to $77,000** over the project. Lead and TA salaries not included. |
| 9. Extra people | Mobile app contractor (Phase 8), accounting/IFTA adviser, external security test before outside customers, part-time UX designer, legal/privacy review. A second developer later if the timeline must be shorter. |
| 10. Main risks | Third-party API access (load boards, ELD, factoring), the unknown state of the existing Replit project, scope size for a two-person team, AI document accuracy against the 95% automation goal, accounting and compliance correctness. |

Dates assume work starts **Monday 9 November 2026**. Every date moves with the real start date.

## How I estimated

1. I read the whole Master Sheet and split it into 25 workstreams. Every bullet in the sheet maps to one of them.
2. For each workstream I gave a low, likely and high number of hours. These are feature hours: building it plus the tests for that feature.
3. For each workstream I set how much needs the Lead (architecture, security, money rules, integration design) and how much the TA can do from written tickets (screens, forms, imports, test suites, vendor sandbox work). The split is balanced on purpose so the Lead is not the bottleneck.
4. On top of feature hours: 8% for QA, regression testing, releases and documentation (TA), and 7% for leadership: writing tickets, reviewing the TA's work, reports and demos (Lead).
5. Capacity: Lead 40 h and TA 40 h paid a week. I plan on **32 productive hours each** (realistic), because of holidays, sick days, production support and meetings. The TA is planned at **24 hours** during Phases 0 to 2 while learning the codebase.
6. Lead work can only be done by the Lead. TA tickets can be picked up by either person. So a phase ends when the Lead's own work is done, or when the pair's combined hours run out, whichever is later.
7. Native apps are built by a mobile contractor in parallel with Phases 5 to 7. The Lead spends about 15% of the contractor's hours reviewing that work.
8. The hours already assume AI-assisted coding. In the first-round assessment, a **prototype** of sign-in, roles and company separation with 75 tests took about a day with AI tools. The production version (workstream 2, 240 likely hours) is much more: password reset, MFA, six roles plus teams, migrations, three environments, owner review rounds, and hardening every other module will rely on. I did not apply any AI speed-up to discovery, integrations with outside companies, owner decisions, review, app store release or accounting validation.

### Three scenarios

| Scenario | Hours used | Productive hours a week | Contingency | Assumptions |
|---|---|---|---|---|
| Optimistic | low column | Lead 35, TA 35 (30 while ramping) | none | The existing Replit project is reusable for about a third of the UI. Owner decisions come back within 2 working days. Load-board, ELD and factoring partners approve API access on the first request. No major rework after the accounting adviser's review. |
| Realistic | likely column | Lead 32, TA 32 (24 while ramping) | 15% | The existing project is mostly a reference: screens are reused, the backend is rebuilt where discovery shows it is not safe. Some vendor approvals take 2 to 6 weeks, worked around by building other features meanwhile. One round of rework after accounting review and after pilot feedback. |
| Conservative | high column | Lead 28, TA 28 (20 while ramping) | none (the high column is already pessimistic; adding contingency on top would count the same risk twice) | The existing project cannot be kept. A provider refuses API access or changes pricing, so an alternative must be built. The 95% automation target needs extra rounds of document-model tuning. The TA ramps up slowly. Scope grows during the build. |

| Scenario | Lead hours | TA hours | Contractor hours | Total |
|---|---|---|---|---|
| Optimistic | 1,646 | 1,856 | 350 | **3,852** |
| Realistic | 2,903 | 3,288 | 632 | **6,824** |
| Conservative | 3,942 | 4,477 | 850 | **9,269** |

### Hours by workstream

| # | Workstream | Low | Likely | High | Lead share |
|---|---|---|---|---|---|
| 1 | Discovery and baseline | 60 | 80 | 120 | 70% |
| 2 | Platform foundations | 160 | 240 | 360 | 60% |
| 3 | Dispatch and loads | 160 | 240 | 360 | 45% |
| 4 | Drivers, fleet, brokers and customers | 90 | 140 | 220 | 25% |
| 5 | Documents and proof of delivery | 70 | 110 | 170 | 55% |
| 6 | Driver mobile web | 90 | 140 | 210 | 25% |
| 7 | Notifications | 50 | 80 | 130 | 25% |
| 8 | Accounting portal core | 280 | 420 | 640 | 55% |
| 9 | Load cost and profitability (Master Sheet section A) | 130 | 190 | 290 | 65% |
| 10 | Reports and analytics | 80 | 120 | 190 | 35% |
| 11 | Company onboarding and platform admin | 80 | 120 | 190 | 55% |
| 12 | Public website, signup and billing | 120 | 180 | 280 | 25% |
| 13 | Customer shipment portal | 60 | 90 | 140 | 35% |
| 14 | Security, backups and reliability | 110 | 160 | 240 | 60% |
| 15 | GPS tracking, maps and arrival estimates | 160 | 250 | 400 | 50% |
| 16 | Fleet maintenance, DOT inspections and DVIR | 150 | 230 | 350 | 35% |
| 17 | Driver performance scorecard | 50 | 80 | 130 | 55% |
| 18 | Automated back office | 320 | 500 | 800 | 50% |
| 19 | Factoring integrations and settlements | 80 | 140 | 240 | 45% |
| 20 | Accounting exports, IFTA and bookkeeping support | 170 | 270 | 420 | 45% |
| 21 | Load-board access and AI load outreach | 200 | 320 | 520 | 50% |
| 22 | Broker intelligence and rating | 70 | 110 | 170 | 35% |
| 23 | Roadside repair and service intelligence | 70 | 110 | 180 | 25% |
| 24 | Unified communications and AI analysis | 190 | 290 | 460 | 40% |
| 25 | Native iOS and Android apps | 350 | 550 | 850 | contractor |
| | **Team feature hours (1 to 24)** | **3,000** | **4,610** | **7,210** | |
| | QA, release, docs (+8%, TA) | 240 | 369 | 577 | |
| | Leadership and reporting (+7%, Lead) | 210 | 323 | 505 | |
| | Lead review of contractor (+15% of 25) | 52 | 82 | 128 | |
| | Contractor (25) | 350 | 550 | 850 | |
| | **Total before contingency** | **3,852** | **5,934** | **9,269** | |
| | **Total used** | **3,852** | **6,824** (+15%) | **9,269** | |

What each workstream includes, its dependencies, staff and milestone are in the full template table further down ("Estimate deliverable template").

## Timeline

### Milestones

| Milestone | What the owner gets | Optimistic | Realistic | Conservative |
|---|---|---|---|---|
| **M1 Internal pilot** | Dispatch, loads, drivers, fleet, customers, documents and POD, driver phone screens, in-app alerts. First on fictional data, then on the owner's own company after his approval. | week 13, 5 Feb 2027 | **week 25, 30 Apr 2027** | week 39, 6 Aug 2027 |
| **M2 Customer-ready version 1** | M1 plus accounting portal, load profitability calculator, reports, company onboarding, public website with signup and billing, GA4 and UTM tracking, customer tracking portal, backups and an external security test. Outside companies can sign up and pay. | week 28, 21 May 2027 | **week 53, 12 Nov 2027** | week 80, 19 May 2028 |
| **M3 Tracking and fleet compliance** | GPS tracking and maps, maintenance, DOT inspections, DVIR, driver scorecard. | week 34, 2 Jul 2027 | **week 65, 4 Feb 2028** | week 99, 29 Sep 2028 |
| **M4 Automated back office** | Rate-confirmation intake, document reading, invoicing and factoring packages, exception queue, accounting exports, IFTA support. | week 43, 3 Sep 2027 | **week 84, 16 Jun 2028** | week 130, 4 May 2029 |
| **M5 Full platform** | Load-board access with AI outreach, broker and repair intelligence, unified communications and AI analysis, native iOS and Android apps. | week 52, 5 Nov 2027 | **week 102, 20 Oct 2028** | week 158, 16 Nov 2029 |

If the owner wants M5 sooner, the most effective lever is a second full-stack developer from M2 (28 productive hours a week, 4 weeks at half speed to ramp up, mostly on Lead-type work). On the realistic case that brings M5 forward by about **13 weeks**, from 20 October 2028 to about 21 July 2028. Adding people before the foundations are stable would slow things down, not speed them up.

### Phase-by-phase plan

| Phase | Workstreams | Lead / TA hours (realistic) | Weeks | Ends (realistic) | Deliverables and exit check |
|---|---|---|---|---|---|
| **0 Discovery** | 1 | 71 / 35 | 2.2 | week 3, 27 Nov 2026 | Owner-controlled access confirmed. Baseline commit and backup of the existing Replit project. Inventory of every screen, route, table, API and cost, each classed as working, partial, UI-only, broken or not built, shown live. Written gap analysis and a refreshed estimate. **Exit: owner approves the gap analysis and the build-vs-reuse decision.** |
| **1 Foundations** | 2 | 185 / 132 | 5.8 | week 8, 1 Jan 2027 | Sign-in, roles, company separation enforced by the server and by database rules, audit log, separate dev/test/prod, CI, fictional data for two companies. **Exit: automated test proves a user from Company A cannot read, change, search, export or download anything from Company B.** |
| **2 Dispatch core** | 3 to 7 | 354 / 585 | 16.8 | week 25, 30 Apr 2027 | Loads end to end, drivers, fleet, customers, documents and POD, driver phone screens, in-app and email alerts. **Exit: M1 pilot, owner and one dispatcher run a week of fictional loads.** |
| **3 Money** | 8 to 10 | 515 / 451 | 16.1 | week 41, 20 Aug 2027 | Invoices, payments, settlements, expenses, fuel, the load profitability calculator wired into the load screen, reports with written metric definitions. **Exit: accounting adviser signs off the rules; estimate vs actual works on fictional loads.** |
| **4 Customer-ready release** | 11 to 14 | 319 / 409 | 11.4 | week 53, 12 Nov 2027 | Company onboarding, Super Admin, public site, signup and billing, GA4, UTM attribution, SEO, customer tracking portal, daily immutable backups, restore drill, external security test. **Exit: M2, first outside company onboarded.** |
| **5 Tracking and fleet compliance** | 15 to 17 | 364 / 409 | 12.1 | week 65, 4 Feb 2028 | Phone GPS and one ELD integration, map, arrival estimates, geofence alerts, maintenance, DOT inspection reading, DVIR, scorecard. **Exit: M3.** |
| **6 Automated back office** | 18 to 20 | 605 / 631 | 19.3 | week 84, 16 Jun 2028 | Rate confirmations to loads, document reading and matching, invoice and factoring packages, exception queue, per-customer cost telemetry, QuickBooks/Xero export, IFTA records. **Exit: M4, measured straight-through rate reported on real volume.** |
| **7 AI and intelligence** | 21 to 24 | 492 / 638 | 17.6 | week 102, 20 Oct 2028 | Authorized load-board access, AI outreach and negotiation with human approval, broker intelligence, roadside repair intelligence, phone and text provider, communication history, shift handoffs, AI communication analyst. **Exit: M5 with the apps.** |
| **8 Native apps (parallel)** | 25 | contractor 632 | about 23 weeks at 28 h | inside Phases 5 to 7 | React Native apps for iOS and Android, driver features first, offline queue, push notifications, store release. |

Phases 0, 1 and 3 are limited by the Lead's own work (security and money rules); the others by the pair's combined hours. Lead and TA hours include the 15% contingency.

Critical path: Discovery, then Foundations, then Loads, then Accounting, then the customer-ready release. Everything after M2 depends on outside parties (ELD, load boards, factoring, phone provider, app stores), so discovery for those starts early, during Phase 3, while the team builds features that do not need them.

## What exists today, and what still needs checking

| Item | Status | What I would do |
|---|---|---|
| Existing Replit project "FAMILY DISPATCH" (Stage 1 demo, sample data) | **Not verified.** I have not seen its code. The Master Sheet says not to assume any screen is backed by a database or production-ready. | Phase 0 inventory, live demo of each feature, written classification. No rebuild without a written reason and owner approval. |
| My first-round assessment prototype (github.com/agentxxblue14/family-dispatch-assessment) | A prototype, not a product. It proves the company-separation design (a filter in the code plus rules inside the database, each tested with the other switched off). | Reuse the design and the tests as a reference for Phase 1, not as a codebase to ship. |
| Load profitability formulas | Fixed and tested in this assessment (`profitability.py`, 29 tests). | Port the same rules into the shared calculation service in Phase 3, with the same tests. |
| Third-party APIs (ELD, load boards, factoring, phone/text, QuickBooks/Xero, maps) | **Need discovery.** Access, pricing and terms unknown. | Discovery is estimated inside each workstream. No integration is attempted without approved credentials. |

## Who does what: Lead Developer and Technical Assistant

| Area | Lead Developer | Technical Assistant |
|---|---|---|
| Architecture, data model, tenancy contract | Owns and documents | Follows; raises questions |
| Security, permissions, tenant isolation, audit log | Builds and reviews | Writes extra permission tests from a checklist |
| Money logic (accounting, profitability, IFTA) | Builds; validates with the accounting adviser | Builds the screens around it |
| Screens, forms, lists, filters | Reviews | Builds from written tickets with acceptance criteria |
| Integrations with outside providers | Discovery, design, build | Vendor research, sandbox setup, test data |
| Tests | Sets the test plan; writes the hard ones | Writes most feature tests; runs QA passes before demos |
| Code review | Reviews every TA change before merge | Reads the Lead's changes to learn the codebase |
| Releases to production | Prepares; releases after owner approval | No production access |
| Documentation | Architecture, runbooks | Setup guide, feature notes, screenshots |
| Owner reporting | Writes weekly report, runs demos | Supplies the done list and QA notes |

The TA gets work as small tickets (half a day to two days), each with: what to build, acceptance criteria, which tests must pass, and which files they may touch. Work is never "build the accounting module".

## AI tools and how quality is kept

| Tool | Used for |
|---|---|
| Claude Code | Main coding agent working in the GitHub repo: features, tests, refactors, migrations, all through pull requests. |
| Replit Agent | Scoped tasks inside the Replit workspace, as the Master Sheet's working model describes. Its output goes through the same review as anyone else's. |
| ChatGPT | The owner's requirements assistant (per Master Sheet B1): keeping the master spec current, drafting tickets and test checklists. |
| A second AI session for review | A fresh session that did not write the change reviews it for bugs and security before the human review. |
| GitHub security tools | Dependabot and code scanning for vulnerable packages and common security mistakes. |

Rules that keep quality up:

1. **Tests first for money and permissions.** Formulas and access rules get tests before the screens are built, like the 24 extra tests in this assessment.
2. **CI must be green** before anything merges: tests, lint, type checks, the tenant-isolation suite.
3. **A human reads every change.** Passing a build is not proof of correctness or security (Master Sheet B1 says the same).
4. **AI never sees real data or secrets.** Fictional data in development; secrets only in the hosting secret store.
5. **Every pull request says what AI wrote** and how it was checked.

## Preventing unauthorized changes to production

1. The owner owns the GitHub organization, the Replit workspace, the domain, the production database and every paid account. Developers use named accounts with two-factor sign-in; no shared passwords or codes.
2. The main branch is protected: no direct pushes, every change by pull request, at least one approving review, CI must pass.
3. Separate development, test and production environments, each with its own database and secrets. Production runs as a separate deployment in the owner's account where only the owner and the Lead can deploy or read production secrets. The TA works in the development workspace only.
4. Production releases go out only from a tagged release, by the Lead, after the owner approves the release notes. Paid integrations, domain changes and real-data migrations need the owner's written yes.
5. Database changes go through reviewed migration files with a backup taken first and a written rollback.
6. Daily backups with a monthly restore test, plus the audit log, so any change can be traced and reversed.

## Bugs, missed deadlines and disagreements

**Bugs.** Every bug gets a severity:

| Severity | Example | Response |
|---|---|---|
| Critical | Data from one company visible to another, production down, wrong money totals | Stop other work, fix or roll back the same day, tell the owner within the hour, write a short incident note |
| High | A main workflow broken for some users | Fix within 2 working days |
| Normal / Low | Workarounds exist, cosmetic issues | Scheduled into the next weekly plan |

Every fixed bug gets a test so it cannot come back.

Outside working hours, uptime and error alerts go to the Lead's phone, and a one-page rollback runbook lets the Lead (or the owner, if needed) put back the last good release in minutes. Working hours overlap US Eastern business hours by agreement.

**Missed deadlines.** I tell the owner as soon as a date is at risk, not on the day it is missed, with options: cut scope, move the date, or add help. Estimates are re-checked at every milestone against actual hours.

**Technical disagreements.** Inside the team: a short written note with the options, costs and risks, a quick prototype or test if it is cheap to try, then the Lead decides and records why. Business, scope and spending decisions go to the owner with a recommendation.

## Progress reports to the owner

- **Weekly written report (Friday):** done this week, planned next week, blocked or waiting on the owner, risks, hours by workstream against the estimate, spend against budget, links to try new features.
- **Live demo every two weeks** on fictional data, of working features only.
- **Milestone review** at each phase end: what is complete, partial or simulated, test results, updated estimate.
- Feature lists always separate "working", "partly working" and "sample data only", as the Master Sheet requires.

## Estimated monthly technical costs

Approximate public list prices as I know them in October 2026. Every line needs a current price check before purchase. Lead and TA salaries are not included; outside people are in the one-time table.

### While building (Phases 0 to 3)

| Item | Per month |
|---|---|
| Replit plan for 2 developers in the owner's workspace | $50 to $80 |
| Replit development and test deployments, database usage | $10 to $50 |
| GitHub (Free or Team); paid code scanning for private repos is optional | $0 to $70 |
| AI coding tools for 2 developers at heavy daily use (Claude Code, Replit Agent usage) | $200 to $400 |
| Error monitoring and uptime checks | $0 to $30 |
| Transactional email | $0 to $20 |
| Domain and DNS | about $2 |
| **Total while building** | **about $260 to $650** |

### Live with first customers (from M1 and M2), added to the above

| Item | Per month |
|---|---|
| Production hosting (always-on or autoscale) | $20 to $150 |
| Managed Postgres with point-in-time recovery | $25 to $100 |
| Off-site immutable backups | $5 to $30 |
| Document and photo storage | $5 to $50, grows with photos |
| Email at volume | $15 to $50 |
| SMS (US business texting registration plus per-message fees), after the provider choice | $20 to $100 |
| Maps and geocoding | $0 to $200, usage-based |
| Logs and monitoring | $0 to $60 |
| Card payments for subscriptions | about 2.9% + $0.30 per charge (standard US card pricing), not a fixed cost |
| **Added when live** | **about $90 to $740**, so **about $350 to $1,400 in total** |

### Full platform (usage-based, grows with customers)

| Item | Estimate |
|---|---|
| AI document reading for the back office | about $0.01 to $0.10 per document, tracked per customer as the Master Sheet requires |
| AI for negotiation drafts and communication analysis | $50 to $500 a month at early volume |
| Business phone and texting (provider not chosen yet) | about $15 to $35 per user a month |
| ELD and telematics APIs | **Unknown until discovery.** Often tied to the carrier's own ELD subscription or a partner program. |
| Load-board API access | **Unknown until discovery.** Usually a commercial agreement with the load board. |
| Factoring integrations | **Unknown until discovery**, per factoring company |
| QuickBooks Online / Xero API | Free to start; check the current partner program limits before launch |
| App stores | Apple Developer $99 a year, Google Play $25 once; push notifications $0 to $100 a month |

### One-time and outside-people costs

| Item | Hours and rate | Estimate |
|---|---|---|
| Mobile contractor for native apps (Phase 8) | 350 to 850 h at $25 to $60 an hour (550 h likely) | $8,750 to $51,000 |
| Accounting and IFTA adviser review | 20 to 40 h at $75 to $150 an hour | $1,500 to $6,000 |
| Part-time UX designer for the design system and driver screens | 40 to 80 h at $25 to $60 an hour | $1,000 to $4,800 |
| External penetration test before outside customers (Phase 4) | fixed quote | $3,000 to $10,000 |
| Legal and privacy review (location consent, SMS consent, terms, AI commitments) | fixed quote | $1,500 to $5,000 |
| **Total** | | **about $15,750 to $76,800** |

Hourly rates are typical ranges for offshore and US freelance specialists and need real quotes.

## Additional staffing and outside expertise

| Who | When | Why |
|---|---|---|
| Mobile developer (React Native), contractor | Phase 8, alongside Phases 5 to 7 | Native apps, background location, offline queue and store releases are a specialist skill. |
| Accounting and IFTA adviser | Phase 3, Phase 6 | The Master Sheet requires a qualified professional to validate accounting, tax and IFTA rules. I have an accountancy degree and can design the ledger rules and write the tests, but a US trucking tax professional must sign off on IFTA and payroll treatment. |
| External security tester | Before M2 | Independent check of tenant isolation and access before outside companies trust the platform with their data. |
| Part-time UX designer | Phases 1 and 2 | Driver screens used in the field and a design system the TA can build from consistently. |
| Legal and privacy adviser | Before tracking, SMS and AI negotiation go live | Driver location consent, SMS consent rules, terms of service, limits on what AI may commit to. |
| Second full-stack developer (optional) | From M2 | Brings M5 forward by about 13 weeks on the realistic case. |
| Part-time QA tester (optional) | Around M2 and M4 releases | Extra manual testing on real devices before big releases. |

## Main technical challenges, risks and dependencies

| Risk or dependency | Impact | How I would handle it |
|---|---|---|
| Unknown state of the existing Replit project | Could add weeks if its backend is not safe to build on | Phase 0 inventory before any estimate is final; rebuild only with a written reason and owner approval |
| Third-party API access (load boards, ELD, factoring, phone/text) | Integrations cannot start without approval; pricing may change | Start discovery in Phase 3; build features that do not need them in the meantime; keep each integration behind one adapter so a provider can be swapped |
| Scope size for a two-person team | Timeline grows if new features are added mid-phase | Each phase has a fixed scope; new ideas go to a backlog the owner prioritizes at milestone reviews |
| Company data isolation | One leak breaks customer trust and may have legal consequences | Separation enforced in the code and in the database, a dedicated test suite on every change, external test before M2 |
| AI document accuracy vs the 95% straight-through goal | Too many exceptions make the back office expensive to run | Measure the straight-through and human-intervention rates from day one; route low-confidence cases to the exception queue; set the price only after measuring real cost |
| Accounting and compliance correctness | Wrong totals or IFTA numbers have real financial cost | Decimal money math, tests for every rule, adviser sign-off, no "guaranteed compliance" claims |
| Replit hosting limits | Background jobs, scaling and long-running AI work may outgrow one Replit deployment | Keep the code portable (standard Postgres, containers); decide on hosting at the Phase 4 review |
| Driver location privacy, SMS consent rules | Fines or app store rejection | Consent screens, tracking only during defined working periods, retention limits, legal review |
| Key-person risk on a small team | Knowledge sits with two people | Owner owns all accounts; documented setup, runbooks and decisions; the TA is cross-trained through reviews |
| Time zones | The owner and US customers are on Eastern time | Agreed overlap hours for meetings and production support; written handoffs |

## Questions for the owner before the estimate is final

1. **Sections 3 (User Roles and Permissions) and C (Acceptance Criteria for the New Feature) have headings but no content** in the candidate edition. Could I see them? They affect workstreams 2 and 9.
2. The Master Sheet says the Full Dispatch fee is 10% **of linehaul revenue only**. The calculator in this assessment applies `dispatch_pct` to total revenue. If loads carry fuel surcharge or accessorial charges, the two give different fees. Which base should the product calculator use?
3. Who will use the platform first: only Family Auto Transportation for a while, or outside carriers early? This decides whether M1 or M2 matters more.
4. Which ELD or GPS providers do your trucks and likely customers use today?
5. Do you already have a load-board subscription (for example DAT or Truckstop), and which factoring companies do you or your customers work with?
6. Which accounting software should exports go to: QuickBooks Online, Xero or another?
7. Is the existing Replit project, its repository and database in an account you own?
8. Is there a target date or budget limit that should shape the phase order?

## Estimate deliverable template

As requested in the Master Sheet: workstream, features included, hours (low / likely / high), dependencies, staff, milestone.

| # | Workstream | Features included | Hours (low / likely / high) | Dependencies | Staff | Milestone |
|---|---|---|---|---|---|---|
| 1 | Discovery and baseline | Access and ownership check, baseline commit and backup of the existing Replit, inventory of screens, routes, schema, auth, APIs and costs, each feature classed working / partial / UI-only / broken / not built, gap analysis, refreshed estimate | 60 / 80 / 120 | Owner grants named access | Lead, TA assists inventory | Phase 0 exit |
| 2 | Platform foundations | Auth and password reset, MFA for owner/admin, roles (Super Admin, owner, dispatcher, driver, helper, read-only), teams/pods, tenant isolation in API and database, audit log, dev/test/prod separation, CI, synthetic two-company data, backup baseline | 160 / 240 / 360 | 1 | Lead builds security core, TA builds screens and tests | M1 |
| 3 | Dispatch and loads | Load create/edit/search/filter, auto-haul vehicle details, multi-stop, assignment with conflict warnings, configurable lifecycle, status history, internal vs shared notes, exception and dispute history | 160 / 240 / 360 | 2 | Lead + TA | M1 |
| 4 | Drivers, fleet, brokers and customers | Driver profiles with restricted personal data, onboarding/offboarding, trucks/trailers/equipment, broker/customer/shipper records, duplicate prevention, private commercial terms | 90 / 140 / 220 | 2 | TA leads, Lead reviews | M1 |
| 5 | Documents and POD | Upload validation, storage outside the web root, tenant and role checks on every download, versioning, retention rules | 70 / 110 / 170 | 2, 3 | Lead | M1 |
| 6 | Driver mobile web | Assigned loads, status updates, photos, signatures, BOL/POD upload, delay and issue reports, common phone sizes | 90 / 140 / 210 | 3, 5 | TA builds, Lead reviews | M1 |
| 7 | Notifications | In-app alerts, email, overdue and expiry alerts; SMS after the provider decision | 50 / 80 / 130 | 3 | TA | M1 |
| 8 | Accounting portal core | Revenue by load, invoices and receivables, partial payments and allocation, settlements, expenses and payables, receipt capture, manual fuel entry, void/correction, financial permissions | 280 / 420 / 640 | 3, 4, 5 | Lead (logic), TA (screens), adviser review | M2 |
| 9 | Load cost and profitability | Expense categories, company and truck cost profiles, cost per mile with loaded/deadhead miles, estimator in the load screen, target rate, estimate snapshots, estimate vs actual | 130 / 190 / 290 | 8 | Lead | M2 |
| 10 | Reports and analytics | Operational and financial dashboards, metric definitions, filters, CSV/PDF export with tenant and role checks | 80 / 120 / 190 | 8, 9 | TA builds, Lead defines metrics | M2 |
| 11 | Company onboarding and platform admin | Onboarding with approval, Super Admin console, support-access policy and audit, deactivation, data export and offboarding, labelled demo mode | 80 / 120 / 190 | 2 | Lead | M2 |
| 12 | Public website, signup and billing | Marketing site, lead funnel, signup, subscription billing, support link, GA4 conversion events, UTM attribution, technical SEO, consent | 120 / 180 / 280 | 11 | TA builds, Lead reviews tracking and privacy | M2 |
| 13 | Customer shipment portal | Sign-in or expiring links, own shipments only, approved documents only, revocable, non-guessable IDs | 60 / 90 / 140 | 3, 5 | TA builds, Lead reviews security | M2 |
| 14 | Security, backups and reliability | Daily immutable snapshots, retention, restore drill, monitoring, security tests across modules, external pen test, disaster recovery runbook | 110 / 160 / 240 | 2 to 13 | Lead + external tester | M2 |
| 15 | GPS tracking, maps and arrival estimates | Phone GPS vs ELD discovery, consent, one ELD integration, staleness, map, labelled estimates, geofence and late alerts, retention | 160 / 250 / 400 | 6; provider API approval | Lead (integration), TA (map UI) | M3 |
| 16 | Fleet maintenance, DOT inspections and DVIR | Maintenance schedules and reminders, DOT report upload with AI extraction and review, out-of-service alerts, corrective actions, DVIR in FDL plus ELD import | 150 / 230 / 350 | 4, 5, 15 | TA builds, Lead owns extraction and rules | M3 |
| 17 | Driver performance scorecard | Explainable score from objective records, careful cause attribution, adjustable weights, owner keeps personnel decisions | 50 / 80 / 130 | 16 | Lead | M3 |
| 18 | Automated back office | Rate-confirmation intake, document classification, BOL/POD extraction and matching, invoice and factoring packages, exception queue, per-customer telemetry, straight-through and intervention rates | 320 / 500 / 800 | 5, 8, 14 | Lead (pipeline), TA (exception queue) | M4 |
| 19 | Factoring integrations and settlements | Authorized factoring APIs where offered, otherwise prepared packages, owner-controlled payments and settlements | 80 / 140 / 240 | 18; factoring partner access | Lead | M4 |
| 20 | Accounting exports, IFTA and bookkeeping | QuickBooks Online / Xero export or sync, IFTA mileage and fuel by jurisdiction, payroll and bookkeeping data, fuel-card import | 170 / 270 / 420 | 8, 15; adviser review | Lead + adviser | M4 |
| 21 | Load-board access and AI outreach | Authorized load-board API only, owner rules, AI-drafted outreach and negotiation, human approval before commitments, logging, escalation | 200 / 320 / 520 | 9, 22; load-board agreement | Lead | M5 |
| 22 | Broker intelligence and rating | Internal broker history, explainable score and categories, incidents and disputes, shown before booking, no cross-carrier disclosure | 70 / 110 / 170 | 3, 8 | TA builds, Lead owns rules | M5 |
| 23 | Roadside repair and service intelligence | Breakdown report, nearby repair search, owner authorization, repair docs into maintenance and expenses, provider history, no paid ranking | 70 / 110 / 180 | 6, 16; places API | TA builds, Lead reviews | M5 |
| 24 | Unified communications and AI analysis | Provider comparison and selection, calling and texting with SMS registration, call/text history per load and customer, transcripts, shift handoffs, AI communication analyst | 190 / 290 / 460 | 3, 4; provider selection | Lead | M5 |
| 25 | Native iOS and Android apps | React Native, driver features first then parity target, offline queue, push, background location rules, store release | 350 / 550 / 850 | 6, 15 | Mobile contractor, Lead reviews | M5 |

**Testing, hardening, rollout, documentation and contingency:** each workstream's hours include its own tests. On top: 8% for regression testing, releases and documentation, 7% for leadership and reporting, and a 15% contingency in the realistic case.

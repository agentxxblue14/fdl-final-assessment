"""FDL estimate model. Every hour total, week count, date and cost total in PLAN.md comes from here.

Run:  python plan/estimate_model.py          (prints the tables used in PLAN.md)
Change an assumption below and rerun to see how the calendar moves.
"""

import datetime as dt
import math

START = dt.date(2026, 11, 9)  # assumed first Monday of work; every date shifts with the real start

# id, phase, workstream, features included, low, likely, high, depends on, staff
WORKSTREAMS = [
    (1, 0, "Discovery and baseline",
     "Access and ownership check, baseline commit and backup of the existing FAMILY DISPATCH Replit, inventory of screens, routes, schema, auth, APIs, costs; each feature classed working / partial / UI-only / broken / not built; written gap analysis against the full Master Sheet; refreshed estimate",
     60, 80, 120, "Owner grants named access", "Lead (TA assists inventory)"),
    (2, 1, "Platform foundations",
     "Auth and password reset, MFA for owner/admin, roles (Super Admin, owner, dispatcher, driver, helper, read-only), teams/pods, tenant isolation in the API and the database (Row Level Security), audit log, dev/test/prod separation, CI, synthetic two-company test data, backup baseline",
     160, 240, 360, "1", "Lead builds security core, TA builds screens and tests"),
    (3, 2, "Dispatch and loads",
     "Load create/edit/search/filter, auto-haul vehicle details, multi-stop, assignment with conflict warnings, configurable lifecycle (New to Completed, Cancelled, On Hold), status history with user and time, internal vs driver/customer notes, exception and dispute history",
     160, 240, 360, "2", "Lead + TA"),
    (4, 2, "Drivers, fleet, brokers and customers",
     "Driver profiles with restricted personal data, onboarding/offboarding, trucks/trailers/equipment, broker/customer/shipper records, duplicate prevention, private commercial terms",
     90, 140, 220, "2", "TA leads, Lead reviews"),
    (5, 2, "Documents and proof of delivery",
     "Upload validation (type, size, signature), storage outside the web root, tenant and role checks on every download, versioning instead of overwrite, retention rules",
     70, 110, 170, "2, 3", "Lead"),
    (6, 2, "Driver mobile web",
     "Phone-first driver screens: assigned loads, status updates, photos, signatures, BOL/POD upload, delay and issue reports; works on common iPhone and Android sizes",
     90, 140, 210, "3, 5", "TA builds, Lead reviews"),
    (7, 2, "Notifications",
     "In-app alerts for assignments, status changes, delays, documents; email; configurable overdue and expiry alerts. SMS waits for the provider decision (WS 24)",
     50, 80, 130, "3", "TA"),
    (8, 3, "Accounting portal core",
     "Revenue by load, invoices and receivables, partial payments and allocation, settlements, expenses and payables, receipt capture, manual fuel entry, void/correction workflow, financial permissions",
     280, 420, 640, "3, 4, 5", "Lead (accounting logic), TA (screens)"),
    (9, 3, "Load cost and profitability (Master Sheet section A)",
     "Expense categories, company and truck cost profiles, cost per mile with loaded/deadhead miles, estimator inside the load screen, target rate, saved estimate snapshots, estimate vs actual variance",
     130, 190, 290, "8", "Lead"),
    (10, 3, "Reports and analytics",
     "Operational and financial dashboards, a written definition for every metric, filters, CSV/PDF export with tenant and role checks",
     80, 120, 190, "8, 9", "TA builds, Lead defines metrics"),
    (11, 4, "Company onboarding and platform admin",
     "Self-serve and approved company onboarding, Super Admin console, support-access policy with audit trail, deactivation, data export and offboarding, labelled demo mode",
     80, 120, 190, "2", "Lead"),
    (12, 4, "Public website, signup and billing",
     "Marketing site, contact/lead funnel, signup, subscription billing, support desk link, GA4 with conversion events, UTM attribution stored with the lead, technical SEO (sitemap, meta, schema), consent handling",
     120, 180, 280, "11", "TA builds, Lead reviews tracking and privacy"),
    (13, 4, "Customer shipment portal",
     "Customer sign-in or expiring tracking links, only their own shipments, approved documents only, revocable access, non-guessable IDs",
     60, 90, 140, "3, 5", "TA builds, Lead reviews security"),
    (14, 4, "Security, backups and reliability",
     "Daily immutable company snapshots, retention, restore drill, monitoring and alerting, security tests across every module, external penetration test support, disaster recovery runbook",
     110, 160, 240, "2 to 13", "Lead"),
    (15, 5, "GPS tracking, maps and arrival estimates",
     "Discovery of phone GPS vs ELD/telematics providers, phone location with driver consent, one ELD integration, last-known location with staleness, map, estimates labelled as estimates, geofence and late alerts, location retention",
     160, 250, 400, "6; provider API approval", "Lead (integration), TA (map UI)"),
    (16, 5, "Fleet maintenance, DOT inspections and DVIR",
     "Maintenance schedules by date/mileage, reminders, receipts; DOT report upload with AI extraction and review queue; out-of-service alerts; corrective actions; pre/post-trip DVIR in FDL plus ELD DVIR import where available",
     150, 230, 350, "4, 5, 15", "TA builds, Lead owns extraction and rules"),
    (17, 5, "Driver performance scorecard",
     "Explainable score from objective records, cause attribution only when evidence supports it, adjustable weights, owner keeps all personnel decisions",
     50, 80, 130, "16", "Lead"),
    (18, 6, "Automated back office",
     "Rate-confirmation ingestion to load records, document classification, BOL/POD extraction and matching, invoice and factoring package generation, exception queue for VAs, per-customer cost and usage telemetry, straight-through and human-intervention rates",
     320, 500, 800, "5, 8, 14", "Lead (pipeline), TA (exception queue UI)"),
    (19, 6, "Factoring integrations and settlements",
     "Package submission where a factoring company offers an authorized API, otherwise a prepared package; owner-controlled payments and settlements. Per-provider discovery",
     80, 140, 240, "18; factoring partner access", "Lead"),
    (20, 6, "Accounting exports, IFTA and bookkeeping support",
     "QuickBooks Online / Xero export or sync, IFTA mileage and fuel records by jurisdiction, payroll and bookkeeping support data, fuel-card import",
     170, 270, 420, "8, 15; accounting adviser review", "Lead + accounting adviser"),
    (21, 7, "Load-board access and AI load outreach",
     "Authorized load-board API access only, owner-defined rules, AI drafts outreach and negotiation, human approval before any commitment, full logging, exception escalation",
     200, 320, 520, "9, 22; load-board API agreement", "Lead"),
    (22, 7, "Broker intelligence and rating",
     "Internal broker history from FDL-managed loads, explainable score (Preferred / Good / Caution / High Risk), incidents and disputes, shown before booking, no cross-carrier disclosure",
     70, 110, 170, "3, 8", "TA builds, Lead owns rules"),
    (23, 7, "Roadside repair and service intelligence",
     "Driver breakdown report, nearby repair search, owner authorization, repair docs into maintenance and expenses, internal provider history, no paid ranking",
     70, 110, 180, "6, 16; places/maps API", "TA builds, Lead reviews"),
    (24, 7, "Unified communications and AI analysis",
     "Provider comparison and selection (not yet chosen), calling and texting with SMS compliance registration, call/text logging per load and customer, transcripts, shift handoff summaries, AI communication analyst reports for human review",
     190, 290, 460, "3, 4; provider selection", "Lead"),
    (25, 8, "Native iOS and Android apps",
     "Shared React Native codebase, driver features first then web parity target, offline queue for poor signal, push notifications, background location rules, App Store and Google Play release",
     350, 550, 850, "6, 15", "Mobile contractor, Lead reviews"),
]

PHASES = {
    0: "Phase 0: Discovery",
    1: "Phase 1: Foundations",
    2: "Phase 2: Dispatch core",
    3: "Phase 3: Money",
    4: "Phase 4: Customer-ready release",
    5: "Phase 5: Tracking and fleet compliance",
    6: "Phase 6: Automated back office",
    7: "Phase 7: AI and intelligence",
}
NATIVE_APPS = 25  # built by a mobile contractor in parallel with phases 5 to 7

# Share of each workstream's feature hours done by the Lead; the TA does the rest.
# Balanced on purpose so the Lead (the scarcer person) is not the bottleneck: the Lead keeps
# architecture, security, money rules and integration design; the TA builds screens, forms,
# imports, test suites and vendor sandbox work from written tickets.
LEAD_SHARE = {1: .70, 2: .60, 3: .45, 4: .25, 5: .55, 6: .25, 7: .25, 8: .55, 9: .65, 10: .35,
              11: .55, 12: .25, 13: .35, 14: .60, 15: .50, 16: .35, 17: .55, 18: .50, 19: .45,
              20: .45, 21: .50, 22: .35, 23: .25, 24: .40}

# Cross-cutting work on top of feature hours (feature hours already include that feature's tests).
QA_RELEASE_DOCS = 0.08    # regression suite, releases, docs, environments: TA
LEADERSHIP = 0.07         # tickets, reviewing TA work, owner reports, demos, planning: Lead
CONTRACTOR_REVIEW = 0.15  # share of contractor hours the Lead spends reviewing the native apps

# Productive hours a week on planned work, out of 40 paid hours each (holidays, sick days,
# production support and meetings take the rest). The TA is slower while learning the codebase.
SCENARIOS = {
    # The high column is already the pessimistic estimate, so it gets no extra contingency;
    # stacking both would count the same risk twice.
    "Optimistic":   dict(col=4, contingency=0.00, lead=35, ta=35, ta_ramp=30, contractor=30),
    "Realistic":    dict(col=5, contingency=0.15, lead=32, ta=32, ta_ramp=24, contractor=28),
    "Conservative": dict(col=6, contingency=0.00, lead=28, ta=28, ta_ramp=20, contractor=24),
}
RAMP_PHASES = (0, 1, 2)  # phases where the TA works at ta_ramp instead of ta

MILESTONES = [  # milestone, phase it closes
    ("M1 Internal pilot: dispatch, drivers, documents, driver phone screens", 2),
    ("M2 Customer-ready version 1 (outside companies can sign up and pay)", 4),
    ("M3 Tracking and fleet compliance live", 5),
    ("M4 Automated back office live", 6),
    ("M5 Full platform including AI features and native apps", 7),
]

# Optional: a second full-stack developer from M2. Productive 28 h a week after a 4-week
# ramp at half speed; works mostly on Lead-type work.
SECOND_DEV = dict(weekly=28, ramp_weeks=4, lead_type_share=0.7)


def ws(i):
    return next(w for w in WORKSTREAMS if w[0] == i)


def phase_hours(phase, s):
    """Lead and TA hours for one phase, contingency included."""
    lead = ta = 0.0
    for w in WORKSTREAMS:
        if w[1] != phase or w[0] == NATIVE_APPS:
            continue
        h = w[s["col"]]
        lead += h * LEAD_SHARE[w[0]] + h * LEADERSHIP
        ta += h * (1 - LEAD_SHARE[w[0]]) + h * QA_RELEASE_DOCS
    if phase in (5, 6, 7):  # Lead reviews the contractor's app work, spread over phases 5 to 7
        lead += ws(NATIVE_APPS)[s["col"]] * CONTRACTOR_REVIEW / 3
    k = 1 + s["contingency"]
    return lead * k, ta * k


def schedule(s, second_dev=False):
    """Phases run in order; a phase ends when all of its Lead and TA work is done."""
    rows, end = [], 0.0
    for p in PHASES:
        lead, ta = phase_hours(p, s)
        ta_cap = s["ta_ramp"] if p in RAMP_PHASES else s["ta"]
        lead_cap = s["lead"]
        if second_dev and p >= 5:
            lead_cap += SECOND_DEV["weekly"] * SECOND_DEV["lead_type_share"]
            ta_cap += SECOND_DEV["weekly"] * (1 - SECOND_DEV["lead_type_share"])
        # Lead-share work needs the Lead; TA tickets can be picked up by either person,
        # so a phase is limited either by the Lead's own work or by the pair's total capacity.
        lead_bound = lead / lead_cap
        pair_bound = (lead + ta) / (lead_cap + ta_cap)
        weeks = max(lead_bound, pair_bound)
        if second_dev and p == 5:
            weeks += SECOND_DEV["ramp_weeks"] / 2  # half speed while ramping
        end += weeks
        rows.append(dict(phase=p, lead=lead, ta=ta, weeks=weeks, end=end,
                         limit="Lead" if lead_bound >= pair_bound else "Both"))
    contractor = ws(NATIVE_APPS)[s["col"]] * (1 + s["contingency"])
    return rows, contractor


def friday_of_week(n):
    return START + dt.timedelta(weeks=math.ceil(n) - 1, days=4)


def fmt_date(d):
    return d.strftime("%d %b %Y").lstrip("0")


# Monthly technical costs (USD, approximate public list prices, verify before purchase).
COSTS_BUILD = [
    ("Replit plan for 2 developers in the owner's workspace", 50, 80),
    ("Replit development and test deployments, database usage", 10, 50),
    ("GitHub (Free or Team); paid code scanning for private repos is optional", 0, 70),
    ("AI coding tools for 2 developers at heavy daily use", 200, 400),
    ("Error monitoring and uptime checks", 0, 30),
    ("Transactional email", 0, 20),
    ("Domain and DNS", 2, 2),
]
COSTS_LIVE = [
    ("Production hosting (always-on or autoscale)", 20, 150),
    ("Managed Postgres with point-in-time recovery", 25, 100),
    ("Off-site immutable backups", 5, 30),
    ("Document and photo storage", 5, 50),
    ("Email at volume", 15, 50),
    ("SMS (US business texting registration plus per-message fees)", 20, 100),
    ("Maps and geocoding", 0, 200),
    ("Logs and monitoring", 0, 60),
]
# One-time and people costs outside the Lead and TA salaries:
# (item, low hours or dollars, high, hourly rate low, hourly rate high)
ONE_TIME = [
    ("Mobile contractor for native apps", None, None, 25, 60),  # hours come from workstream 25
    ("Accounting and IFTA adviser", 20, 40, 75, 150),
    ("Part-time UX designer", 40, 80, 25, 60),
    ("External penetration test", 3000, 10000, None, None),
    ("Legal and privacy review", 1500, 5000, None, None),
]


def cost_tables():
    b = (sum(c[1] for c in COSTS_BUILD), sum(c[2] for c in COSTS_BUILD))
    live = (sum(c[1] for c in COSTS_LIVE), sum(c[2] for c in COSTS_LIVE))
    rows = []
    for name, lo, hi, rlo, rhi in ONE_TIME:
        if name.startswith("Mobile"):
            lo, hi = ws(NATIVE_APPS)[4], ws(NATIVE_APPS)[6]
        if rlo is None:
            rows.append((name, f"${lo:,} to ${hi:,}", lo, hi))
        else:
            rows.append((name, f"{lo:,} to {hi:,} h at ${rlo} to ${rhi}/h = ${lo*rlo:,} to ${hi*rhi:,}",
                         lo * rlo, hi * rhi))
    return b, live, rows


def report():
    print("## Hours by workstream (feature hours)")
    print("| # | Workstream | Low | Likely | High | Lead share |")
    print("|---|---|---|---|---|---|")
    for w in WORKSTREAMS:
        share = "contractor" if w[0] == NATIVE_APPS else f"{LEAD_SHARE[w[0]]:.0%}"
        print(f"| {w[0]} | {w[2]} | {w[4]:,} | {w[5]:,} | {w[6]:,} | {share} |")
    team = [sum(w[c] for w in WORKSTREAMS if w[0] != NATIVE_APPS) for c in (4, 5, 6)]
    app = [ws(NATIVE_APPS)[c] for c in (4, 5, 6)]
    print(f"| | Team feature hours (1 to 24) | {team[0]:,} | {team[1]:,} | {team[2]:,} | |")
    print(f"| | QA, release, docs +{QA_RELEASE_DOCS:.0%} | " + " | ".join(f"{t*QA_RELEASE_DOCS:,.0f}" for t in team) + " | |")
    print(f"| | Leadership and reporting +{LEADERSHIP:.0%} | " + " | ".join(f"{t*LEADERSHIP:,.0f}" for t in team) + " | |")
    print(f"| | Lead review of contractor +{CONTRACTOR_REVIEW:.0%} of 25 | " + " | ".join(f"{a*CONTRACTOR_REVIEW:,.0f}" for a in app) + " | |")
    print()

    print("## Scenarios")
    print("| Scenario | Lead hours | TA hours | Contractor hours | Total hours | M1 | M2 | M3 | M4 | M5 |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for name, s in SCENARIOS.items():
        rows, contractor = schedule(s)
        lead = sum(r["lead"] for r in rows)
        ta = sum(r["ta"] for r in rows)
        ms = []
        for label, ph in MILESTONES:
            e = next(r["end"] for r in rows if r["phase"] == ph)
            ms.append(f"wk {math.ceil(e)}, {fmt_date(friday_of_week(e))} ({e/4.345:.1f} mo)")
        print(f"| {name} | {lead:,.0f} | {ta:,.0f} | {contractor:,.0f} | {lead+ta+contractor:,.0f} | " + " | ".join(ms) + " |")
    print()

    s = SCENARIOS["Realistic"]
    rows, contractor = schedule(s)
    print(f"## Phase calendar, realistic (Lead {s['lead']} h/wk, TA {s['ta_ramp']} h/wk in phases 0 to 2 then {s['ta']})")
    print("| Phase | Lead hours | TA hours | Weeks | Ends | Limited by |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {PHASES[r['phase']]} | {r['lead']:,.0f} | {r['ta']:,.0f} | {r['weeks']:.1f} | "
              f"wk {math.ceil(r['end'])}, {fmt_date(friday_of_week(r['end']))} | {r['limit']} |")
    print(f"| Phase 8: Native apps (contractor) | review in 5 to 7 | | {contractor / s['contractor']:.1f} at {s['contractor']} h/wk | inside phases 5 to 7 | |")
    print()
    rows2, _ = schedule(s, second_dev=True)
    print(f"Second developer from M2 (realistic): M5 moves from week {math.ceil(rows[-1]['end'])} "
          f"({fmt_date(friday_of_week(rows[-1]['end']))}) to week {math.ceil(rows2[-1]['end'])} "
          f"({fmt_date(friday_of_week(rows2[-1]['end']))}), {rows[-1]['end'] - rows2[-1]['end']:.0f} weeks sooner.")
    print()

    b, live, one = cost_tables()
    print(f"Monthly while building: ${b[0]:,} to ${b[1]:,}")
    print(f"Added when live: ${live[0]:,} to ${live[1]:,}; total live: ${b[0]+live[0]:,} to ${b[1]+live[1]:,}")
    print("One-time and people costs outside Lead and TA salaries:")
    for name, text, lo, hi in one:
        print(f"  {name}: {text}")
    print(f"  Total: ${sum(r[2] for r in one):,} to ${sum(r[3] for r in one):,}")


if __name__ == "__main__":
    report()

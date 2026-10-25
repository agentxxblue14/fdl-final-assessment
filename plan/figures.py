"""Drawings for PLAN.md and SUBMISSION.md, written to docs/*.svg.

Every number in a drawing comes from estimate_model.py or from profitability.py, so the
pictures cannot drift from the tables. Run: python plan/figures.py
"""
import datetime as dt
import math
import pathlib
import sys
from html import escape

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import estimate_model as m  # noqa: E402
from profitability import calculate_load  # noqa: E402

INK, MUTED, LINE = "#17232f", "#5d6a77", "#d8dee6"
SKY, ROAD, LANE = "#e3eff8", "#3b444e", "#f4c430"
SIGN, BLUE, AMBER = "#1d6b48", "#2a6f9e", "#e39b2d"
RED, GREEN, PAPER = "#c4473a", "#2f8a57", "#ffffff"
HEAD = "Bahnschrift, 'DIN Alternate', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
BODY = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"


# ---------------------------------------------------------------- numbers from the model

def scenario_summary():
    out = {}
    for name, s in m.SCENARIOS.items():
        rows, contractor = m.schedule(s)
        ms = []
        for _, ph in m.MILESTONES:
            e = next(r["end"] for r in rows if r["phase"] == ph)
            ms.append((math.ceil(e), m.friday_of_week(e)))
        lead, ta = sum(r["lead"] for r in rows), sum(r["ta"] for r in rows)
        out[name] = dict(rows=rows, milestones=ms, lead=lead, ta=ta, contractor=contractor,
                         total=lead + ta + contractor)
    return out


SC = scenario_summary()
REAL = SC["Realistic"]
BUILD, LIVE_ADD, ONE_TIME = m.cost_tables()
LIVE = (BUILD[0] + LIVE_ADD[0], BUILD[1] + LIVE_ADD[1])
ONE = (sum(r[2] for r in ONE_TIME), sum(r[3] for r in ONE_TIME))
README_LOAD = (2000, 500, 4, 10, 400, 50, 10, 100, 20)
FIXED = calculate_load(*README_LOAD)
# Output of the original code (commit af3c023) for the same load, see evidence/tests-before.txt.
ORIGINAL = dict(fuel_cost=20000, dispatch_fee=20000, total_cost=40550, profit=-38550,
                margin_pct=-95.07, break_even_rate=20550, suggested_rate=25687.5)


def n(x):
    return f"{x:,.0f}"


def about(lo, hi):
    """Cost range as the plan states it: low end to the nearest $10, high end to the nearest $50."""
    return f"${n(round(lo, -1))} to ${n(round(hi / 50) * 50)}"


def d(day):
    return day.strftime("%d %b %Y").lstrip("0")


def money(x):
    s = f"{abs(x):,.2f}".removesuffix(".00")
    return ("-$" if x < 0 else "$") + s


# ---------------------------------------------------------------- svg helpers

def svg(w, h, title, body, bg=True):
    back = f'<rect width="{w}" height="{h}" rx="14" fill="{PAPER}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>{back}{body}</svg>')


def text(x, y, s, size=13, fill=INK, weight=400, anchor="start", font=BODY, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(str(s))}</text>')


def g(body, x=0, y=0, s=1):
    return f'<g transform="translate({x} {y}) scale({s})">{body}</g>'


def car(x, y, s=1, color="#d9534f"):
    """Small car, side view, wheels resting on y."""
    b = (f'<rect x="0" y="-13" width="40" height="8" rx="3" fill="{color}"/>'
         f'<path d="M8 -13 L13.5 -19.5 L27 -19.5 L32.5 -13 Z" fill="{color}"/>'
         '<path d="M14.5 -18.5 L19.5 -18.5 L19.5 -13.8 L11 -13.8 Z M21 -18.5 L26.3 -18.5 L30.2 -13.8 L21 -13.8 Z" fill="#dbeefa"/>'
         '<circle cx="9.5" cy="-4.5" r="4.3" fill="#1f252b"/><circle cx="9.5" cy="-4.5" r="1.7" fill="#b9c2ca"/>'
         '<circle cx="30.5" cy="-4.5" r="4.3" fill="#1f252b"/><circle cx="30.5" cy="-4.5" r="1.7" fill="#b9c2ca"/>')
    return g(b, x, y, s)


def wheel(cx, cy, r=9):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#1f252b"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .42:.1f}" fill="#b9c2ca"/>')


def truck(x, y, s=1, cab=BLUE):
    """Car-hauler truck facing right, wheels resting on y. About 232 wide and 60 tall at s=1."""
    frame = "#5b6570"
    b = [f'<rect x="0" y="-55" width="162" height="4" rx="1" fill="{frame}"/>',
         f'<rect x="0" y="-24" width="162" height="5" rx="1" fill="{frame}"/>']
    for ux in (4, 56, 108, 158):
        b.append(f'<rect x="{ux}" y="-55" width="3" height="34" fill="{frame}"/>')
    for cx, col in ((10, "#d9534f"), (60, "#f2f4f6"), (110, AMBER)):
        b.append(car(cx, -55, 1.05, col))
    for cx, col in ((10, "#7aa7c7"), (60, "#4d5a66")):
        b.append(car(cx, -24, 1.05, col))
    b.append(f'<rect x="96" y="-19" width="136" height="6" fill="#2d343b"/>')
    b.append(f'<path d="M162 -55 L174 -55 L174 -40 L162 -40 Z" fill="{frame}"/>')
    b.append(f'<rect x="168" y="-50" width="44" height="37" rx="5" fill="{cab}"/>')
    b.append(f'<rect x="200" y="-33" width="30" height="20" rx="4" fill="{cab}"/>')
    b.append('<path d="M175 -45 L198 -45 L206 -32 L175 -32 Z" fill="#cfe4f2"/>')
    b.append('<rect x="226" y="-17" width="8" height="5" rx="1" fill="#9aa3ab"/>')
    b.append('<circle cx="227" cy="-27" r="2.6" fill="#ffd76a"/>')
    b.append('<rect x="172" y="-62" width="4" height="13" rx="1" fill="#9aa3ab"/>')
    b.append(wheel(120, -9) + wheel(142, -9) + wheel(182, -9) + wheel(214, -9))
    return g("".join(b), x, y, s)


def signpost(x, ground, title, sub, w=96, color=SIGN, post=58):
    top = ground - post - 44
    return (f'<rect x="{x - 2}" y="{ground - post - 2}" width="4" height="{post + 2}" fill="#8a939c"/>'
            f'<rect x="{x - w / 2}" y="{top}" width="{w}" height="44" rx="6" fill="{color}"/>'
            f'<rect x="{x - w / 2 + 3}" y="{top + 3}" width="{w - 6}" height="38" rx="4" fill="none" stroke="#fff" stroke-width="1.3"/>'
            + text(x, top + 19, title, 13.5, "#fff", 700, "middle", HEAD)
            + text(x, top + 34, sub, 11, "#fff", 400, "middle", HEAD))


def flag(x, ground, h=46):
    sq = "".join(f'<rect x="{x + 2 + c * 7}" y="{ground - h + r * 7}" width="7" height="7" fill="{INK if (r + c) % 2 == 0 else "#fff"}"/>'
                 for r in range(3) for c in range(4))
    return (f'<rect x="{x - 1}" y="{ground - h}" width="3" height="{h}" fill="{INK}"/>{sq}'
            f'<rect x="{x + 2}" y="{ground - h}" width="28" height="21" fill="none" stroke="{INK}" stroke-width="1"/>')


SKIN = ("#e9b98f", "#c98e64", "#a8724b", "#f1c9a5")


def person(x, y, shirt, skin=SKIN[0], s=1, hair="#2b2320"):
    b = (f'<rect x="-12" y="-16" width="10" height="16" rx="3" fill="#2f3a45"/>'
         f'<rect x="2" y="-16" width="10" height="16" rx="3" fill="#2f3a45"/>'
         f'<path d="M-17 -16 L-17 -44 Q-17 -52 -9 -52 L9 -52 Q17 -52 17 -44 L17 -16 Z" fill="{shirt}"/>'
         f'<rect x="-4" y="-57" width="8" height="7" fill="{skin}"/>'
         f'<circle cx="0" cy="-66" r="11" fill="{skin}"/>'
         f'<path d="M-11 -67 Q-11 -79 0 -79 Q11 -79 11 -67 Q6 -73 -2 -72 Q-8 -71 -11 -67 Z" fill="{hair}"/>')
    return g(b, x, y, s)


def laptop(x, y, s=1):
    b = ('<path d="M-16 0 L-12 -20 L12 -20 L16 0 Z" fill="#cfd6dd"/>'
         '<path d="M-10 -18 L10 -18 L13 -3 L-13 -3 Z" fill="#7aa7c7"/>'
         '<rect x="-20" y="0" width="40" height="3" rx="1.5" fill="#9aa3ab"/>')
    return g(b, x, y, s)


def icon(name, cx, cy, r=17, color=INK):
    """Line icons on a white disc."""
    st = f'fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
    k = r / 17
    p = {
        "shield": f'<path d="M0 -10 L8 -7 L8 0 Q8 7 0 11 Q-8 7 -8 0 L-8 -7 Z" {st}/><path d="M-3.5 0 L-1 3 L4 -3" {st}/>',
        "coins": f'<ellipse cx="0" cy="-6" rx="8" ry="3" {st}/><path d="M-8 -6 V6 Q0 10 8 6 V-6 M-8 0 Q0 4 8 0" {st}/>',
        "plug": f'<path d="M-4 -11 V-5 M4 -11 V-5 M-7 -5 H7 V0 Q7 6 0 6 Q-7 6 -7 0 Z M0 6 V11" {st}/>',
        "magnifier": f'<circle cx="-2" cy="-2" r="6.5" {st}/><path d="M3 3 L9 9" {st}/>',
        "screen": f'<rect x="-10" y="-8" width="20" height="13" rx="1.5" {st}/><path d="M-4 10 H4 M0 5 V10" {st}/>',
        "checklist": f'<path d="M-9 -7 L-7 -5 L-4 -9 M-9 1 L-7 3 L-4 -1 M-9 9 L-7 11 L-4 7 M0 -7 H9 M0 1 H9 M0 9 H9" {st}/>',
        "ticket": f'<path d="M-10 -6 H10 V-2 Q7 0 10 2 V6 H-10 V2 Q-7 0 -10 -2 Z M-3 -6 V6" {st}/>',
        "phone": f'<rect x="-6" y="-11" width="12" height="22" rx="2.5" {st}/><path d="M-2 7 H2" {st}/>',
        "key": f'<circle cx="-5" cy="0" r="5" {st}/><path d="M0 0 H10 M6 0 V4 M9 0 V3" {st}/>',
        "check": f'<path d="M-8 0 L-2 6 L9 -7" {st}/>',
        "flag": f'<path d="M-6 11 V-10 M-6 -9 H8 L4 -4 L8 1 H-6" {st}/>',
        "lock": f'<rect x="-8" y="-2" width="16" height="12" rx="2" {st}/><path d="M-5 -2 V-6 Q-5 -11 0 -11 Q5 -11 5 -6 V-2" {st}/>',
        "question": f'<path d="M-5 -5 Q-5 -11 0 -11 Q6 -11 6 -5 Q6 -1 1 1 Q0 2 0 4" {st}/><circle cx="0" cy="9" r="1.2" fill="{color}"/>',
        "boxes": f'<rect x="-10" y="0" width="9" height="9" {st}/><rect x="1" y="0" width="9" height="9" {st}/><rect x="-4.5" y="-10" width="9" height="9" {st}/>',
        "doc": f'<path d="M-7 -11 H3 L8 -6 V11 H-7 Z M3 -11 V-6 H8" {st}/><path d="M-3 7 L4 -1" {st}/><circle cx="-2.5" cy="-0.5" r="1.4" {st}/><circle cx="3.5" cy="6" r="1.4" {st}/>',
        "pr": f'<circle cx="-5" cy="-8" r="2.6" {st}/><circle cx="-5" cy="8" r="2.6" {st}/><circle cx="6" cy="8" r="2.6" {st}/><path d="M-5 -5.4 V5.4 M6 5.4 V-2 Q6 -6 2 -6 H-1" {st}/>',
    }[name]
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
            f'<g transform="translate({cx} {cy}) scale({k:.2f})">{p}</g>')


def road(x1, x2, y, h=34, lane=True):
    b = (f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="{h}" fill="{ROAD}"/>'
         f'<rect x="{x1}" y="{y + 2}" width="{x2 - x1}" height="1.5" fill="#e9edf1"/>'
         f'<rect x="{x1}" y="{y + h - 3.5}" width="{x2 - x1}" height="1.5" fill="#e9edf1"/>')
    if lane:
        b += f'<line x1="{x1}" y1="{y + h / 2}" x2="{x2}" y2="{y + h / 2}" stroke="{LANE}" stroke-width="2.5" stroke-dasharray="16 11"/>'
    return b


def coin_stack(x, base, coins, faded=0, w=46):
    out = []
    for i in range(coins + faded):
        y = base - i * 6
        fill, edge = ("#f0c24b", "#c99a26") if i < coins else ("#fbeec6", "#ead9a1")
        out.append(f'<rect x="{x - w / 2}" y="{y - 6}" width="{w}" height="6" rx="3" fill="{edge}"/>'
                   f'<ellipse cx="{x}" cy="{y - 6}" rx="{w / 2}" ry="3.2" fill="{fill}"/>')
    return "".join(out)


# ---------------------------------------------------------------- figures

def fig_glance():
    W, H = 1000, 330
    b = []
    # Panel 1: hours, three people in front of bars sized by their hours
    b.append(text(30, 40, "Hours to build everything", 15, MUTED, 600, font=HEAD))
    b.append(text(30, 78, f"{n(REAL['total'])} h", 34, INK, 700, font=HEAD))
    b.append(text(30, 100, f"realistic, range {n(SC['Optimistic']['total'])} to {n(SC['Conservative']['total'])}", 12.5, MUTED))
    people = (("Lead", REAL["lead"], BLUE, SKIN[1]), ("TA", REAL["ta"], GREEN, SKIN[0]),
              ("Mobile contractor", REAL["contractor"], AMBER, SKIN[2]))
    base = 262
    for i, (who, hrs, col, skin) in enumerate(people):
        cx = 72 + i * 100
        bh = 74 * hrs / REAL["ta"]
        b.append(f'<rect x="{cx - 34}" y="{base - bh:.0f}" width="68" height="{bh:.0f}" rx="5" fill="{col}"/>')
        b.append(person(cx, base - bh, col, skin, .78))
        b.append(text(cx, base + 20, who.replace("Mobile contractor", "Contractor"), 12.5, INK, 600, "middle"))
        b.append(text(cx, base + 37, f"{n(hrs)} h", 13, INK, 700, "middle", HEAD))
    b.append(f'<line x1="338" y1="30" x2="338" y2="305" stroke="{LINE}" stroke-width="1.5"/>')

    # Panel 2: tear-off calendars for the three dates the owner cares about
    b.append(text(368, 40, "When the owner can use it", 15, MUTED, 600, font=HEAD))
    cal = (("Internal pilot", REAL["milestones"][0][1]), ("Version 1 for", REAL["milestones"][1][1]),
           ("Full platform", REAL["milestones"][4][1]))
    sub = ("own company", "outside companies", "apps and AI")
    for i, ((label, day), s2) in enumerate(zip(cal, sub)):
        x = 378 + i * 100
        b.append(f'<rect x="{x}" y="80" width="80" height="96" rx="7" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>')
        b.append(f'<path d="M{x} 107 V87 Q{x} 80 {x + 7} 80 H{x + 73} Q{x + 80} 80 {x + 80} 87 V107 Z" fill="{RED if i == 2 else BLUE}"/>')
        for rx in (x + 20, x + 60):
            b.append(f'<rect x="{rx - 3}" y="72" width="6" height="16" rx="3" fill="#8a939c"/>')
        b.append(text(x + 40, 100, day.strftime("%b %Y"), 13, "#fff", 700, "middle", HEAD))
        b.append(text(x + 40, 152, day.day, 38, INK, 700, "middle", HEAD))
        b.append(text(x + 40, 168, day.strftime("%A"), 10.5, MUTED, 400, "middle"))
        b.append(text(x + 40, 200, label, 12.5, INK, 600, "middle"))
        b.append(text(x + 40, 216, s2, 12.5, INK, 600, "middle"))
    b.append(text(368, 258, f"Start assumed Monday {d(m.START)}.", 12.5, MUTED))
    b.append(text(368, 276, f"Best case full platform {d(SC['Optimistic']['milestones'][4][1])},", 12.5, MUTED))
    b.append(text(368, 294, f"conservative {d(SC['Conservative']['milestones'][4][1])}.", 12.5, MUTED))
    b.append(f'<line x1="688" y1="30" x2="688" y2="305" stroke="{LINE}" stroke-width="1.5"/>')

    # Panel 3: coin stacks, one coin = $100 a month; pale coins show the top of the range
    b.append(text(718, 40, "Monthly technical costs", 15, MUTED, 600, font=HEAD))
    coin = 100
    for i, (label, (lo, hi)) in enumerate((("While building", BUILD), ("Once live", LIVE))):
        cx = 765 + i * 115
        solid = round(lo / coin)
        b.append(coin_stack(cx, 262, solid, max(round(hi / coin) - solid, 0)))
        b.append(text(cx, 284, label, 12.5, INK, 600, "middle"))
        b.append(text(cx, 301, about(lo, hi), 12.5, INK, 700, "middle", HEAD))
    b.append(text(718, 70, "1 coin = $100 a month, pale coins = top of range", 11.5, MUTED))
    b.append(text(718, 88, "Salaries not included", 11.5, MUTED))
    return svg(W, H, "At a glance: hours, dates and monthly costs", "".join(b))


def fig_roadmap():
    W, H = 1000, 350
    rows, ms = REAL["rows"], REAL["milestones"]
    last = rows[-1]["end"]
    x0, x1 = 120, 930
    X = lambda wk: x0 + (x1 - x0) * wk / last  # noqa: E731
    b = [f'<rect x="0" y="0" width="{W}" height="200" rx="14" fill="{SKY}"/>',
         f'<rect x="0" y="186" width="{W}" height="14" fill="{SKY}"/>',
         '<path d="M0 190 Q120 150 260 176 T560 168 T860 160 T1000 172 V200 H0 Z" fill="#cfe3d4"/>',
         '<circle cx="940" cy="52" r="24" fill="#fde7b0"/>']
    b.append(road(0, W, 196, 40))
    b.append(truck(6, 228, .43))
    b.append(text(x0, 260, f"Start {d(m.START)}", 12, INK, 600, "middle", HEAD))
    names = ["Discovery", "Foundations", "Dispatch core", "Money", "Release", "Tracking, fleet",
             "Back office", "AI and intelligence"]
    shades = ["#9ab8cf", "#7ea4c2", BLUE, "#2f8a57", "#226b45", AMBER, "#c9822a", RED]
    start = 0
    for r, nm, col in zip(rows, names, shades):
        a, z = X(start), X(r["end"])
        b.append(f'<rect x="{a:.1f}" y="272" width="{z - a - 2:.1f}" height="26" rx="4" fill="{col}"/>')
        label = f"{r['phase']}  {nm}" if z - a > 7.2 * len(nm) + 24 else str(r["phase"])
        b.append(text((a + z) / 2, 289.5, label, 12, "#fff", 700, "middle", HEAD))
        start = r["end"]
    b.append(text(x0, 316, "Phase 0 Discovery, phase 1 Foundations", 11.5, MUTED))
    a, z = X(rows[4]["end"]), X(last)
    b.append(f'<rect x="{a:.1f}" y="304" width="{z - a - 2:.1f}" height="18" rx="4" fill="none" stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="5 3"/>')
    b.append(text((a + z) / 2, 317, "8  Native apps, mobile contractor, in parallel", 11.5, INK, 600, "middle", HEAD))
    short = ["Pilot", "Version 1", "Tracking", "Back office", "Full platform"]
    for i, ((wk, day), lab) in enumerate(zip(ms, short)):
        x = X(wk)
        if i == 4:
            b.append(flag(x + 4, 196, 52))
            x -= 40
        b.append(signpost(x, 196, f"M{i + 1} {lab}", d(day), 116 if i == 4 else 96, post=50 + (i % 2) * 34))
    b.append(text(24, 32, "Realistic road to the full platform", 17, INK, 700, font=HEAD))
    b.append(text(24, 52, f"{n(REAL['total'])} hours, Lead and Technical Assistant at 32 productive hours a week each", 12.5, MUTED))
    return svg(W, H, "Realistic roadmap with phases and milestones", "".join(b))


def fig_scenarios():
    W, H = 1000, 300
    end = max(v["milestones"][4][0] for v in SC.values())
    x0, x1 = 190, 950
    X = lambda wk: x0 + (x1 - x0) * wk / end  # noqa: E731
    b = [text(24, 32, "Three possible roads", 17, INK, 700, font=HEAD),
         text(24, 52, "Milestones M1 to M5 on each scenario, same start date", 12.5, MUTED)]
    for yr in range(2027, 2031):
        wk = (dt.date(yr, 1, 1) - m.START).days / 7
        if wk > end:
            break
        if wk < 12:
            continue
        x = X(wk)
        b.append(f'<line x1="{x:.1f}" y1="72" x2="{x:.1f}" y2="262" stroke="{LINE}" stroke-width="1.2" stroke-dasharray="3 4"/>')
        b.append(text(x, 280, f"1 Jan {yr}", 11.5, MUTED, 400, "middle", HEAD))
    b.append(text(x0, 280, d(m.START), 11.5, MUTED, 400, "middle", HEAD))
    for i, (name, v) in enumerate(SC.items()):
        y = 86 + i * 60
        b.append(text(24, y + 14, name, 15, INK, 700, font=HEAD))
        b.append(text(24, y + 32, f"{n(v['total'])} hours", 12.5, MUTED))
        last_x = X(v["milestones"][4][0])
        b.append(road(x0, last_x, y, 30, lane=False))
        b.append(f'<line x1="{x0}" y1="{y + 15}" x2="{last_x}" y2="{y + 15}" stroke="{LANE}" stroke-width="2" stroke-dasharray="10 8"/>')
        for k, (wk, day) in enumerate(v["milestones"]):
            x = X(wk)
            b.append(f'<rect x="{x - 13}" y="{y + 3}" width="26" height="24" rx="5" fill="{SIGN}" stroke="#fff" stroke-width="1.5"/>')
            b.append(text(x, y + 20, f"M{k + 1}", 11.5, "#fff", 700, "middle", HEAD))
        b.append(flag(last_x + 18, y + 30, 32))
        b.append(text(last_x + 52, y + 20, d(v["milestones"][4][1]), 12.5, INK, 700, font=HEAD))
    return svg(W, H, "Optimistic, realistic and conservative timelines", "".join(b))


def fig_team():
    W, H = 1000, 330
    crew = [
        ("Owner", "owns every account", "#6b5b95", SKIN[3], "clipboard",
         [("key", "All|accounts"), ("check", "Approves|releases"), ("flag", "Sets|priorities")]),
        ("Lead Developer", "the hard and risky parts", BLUE, SKIN[1], "laptop",
         [("shield", "Security"), ("coins", "Money|rules"), ("plug", "Outside|systems"), ("magnifier", "Reviews|all code")]),
        ("Technical Assistant", "builds from small tickets", GREEN, SKIN[0], "laptop",
         [("screen", "Screens|and forms"), ("checklist", "Tests|and QA"), ("ticket", "Small|tickets")]),
        ("Mobile contractor", "native apps, phases 5 to 7", AMBER, SKIN[2], "phone",
         [("phone", "iOS and|Android"), ("magnifier", "Lead|reviews")]),
    ]
    b = []
    for i, (who, line, col, skin, prop, badges) in enumerate(crew):
        cx = 125 + i * 250
        b.append(f'<ellipse cx="{cx}" cy="168" rx="70" ry="10" fill="{SKY}"/>')
        b.append(person(cx, 166, col, skin, 1.45))
        if prop == "laptop":
            b.append(f'<rect x="{cx - 50}" y="140" width="100" height="10" rx="3" fill="#b08a62"/>')
            b.append(f'<rect x="{cx - 44}" y="150" width="6" height="18" fill="#8d6d4c"/><rect x="{cx + 38}" y="150" width="6" height="18" fill="#8d6d4c"/>')
            b.append(laptop(cx, 140, 1.1))
        elif prop == "phone":
            b.append(f'<rect x="{cx + 14}" y="88" width="15" height="26" rx="3" fill="{INK}"/><rect x="{cx + 16}" y="91" width="11" height="18" rx="1" fill="#7aa7c7"/>')
        else:
            b.append(f'<rect x="{cx + 10}" y="92" width="24" height="31" rx="2" fill="#b08a62"/><rect x="{cx + 13}" y="97" width="18" height="23" fill="#fff"/>'
                     f'<path d="M{cx + 16} 103 H{cx + 28} M{cx + 16} 108 H{cx + 28} M{cx + 16} 113 H{cx + 24}" stroke="{MUTED}" stroke-width="1.4"/>')
        b.append(text(cx, 200, who, 15, INK, 700, "middle", HEAD))
        b.append(text(cx, 218, line, 12, MUTED, 400, "middle"))
        k = len(badges)
        for j, (ic, cap) in enumerate(badges):
            bx = cx + (j - (k - 1) / 2) * 60
            b.append(icon(ic, bx, 256, 17, col))
            for li, part in enumerate(cap.split("|")):
                b.append(text(bx, 290 + li * 14, part, 11, INK, 400, "middle"))
        if i < 3:
            b.append(f'<line x1="{cx + 125}" y1="40" x2="{cx + 125}" y2="310" stroke="{LINE}" stroke-width="1.2"/>')
    return svg(W, H, "Who does what: owner, Lead, Technical Assistant and mobile contractor", "".join(b))


def gate(x, ground, label_y, label1, label2, ic, color):
    """A toll-style barrier with its arm raised."""
    b = (f'<rect x="{x - 9}" y="{ground - 40}" width="18" height="40" rx="3" fill="{INK}"/>'
         f'<circle cx="{x}" cy="{ground - 34}" r="3" fill="{LANE}"/>'
         f'<g class="gate-arm" data-x="{x}" data-y="{ground - 34}" transform="rotate(-62 {x} {ground - 34})">'
         + "".join(f'<rect x="{x + 6 + k * 14}" y="{ground - 38}" width="14" height="8" fill="{RED if k % 2 == 0 else "#fff"}" stroke="{RED}" stroke-width=".8"/>' for k in range(6))
         + '</g>' + icon(ic, x - 38, ground - 22, 18, color)
         + text(x, label_y, label1, 12.5, INK, 700, "middle", HEAD)
         + text(x, label_y + 16, label2, 11.5, MUTED, 400, "middle"))
    return b


def fig_gates():
    W, H = 1000, 292
    ground = 206
    b = [text(24, 32, "Every change passes four gates before it reaches production", 17, INK, 700, font=HEAD),
         road(0, W, ground - 34, 34)]
    b.append(f'<g class="gate-truck">{truck(8, ground - 8, .38)}</g>')
    stops = [(250, "Pull request", "no direct pushes", "pr", BLUE),
             (420, "Tests pass", "CI must be green", "check", GREEN),
             (590, "Lead review", "a human reads it", "magnifier", BLUE),
             (760, "Owner says yes", "approves release notes", "key", "#6b5b95")]
    for x, l1, l2, ic, col in stops:
        b.append(gate(x, ground - 34, ground + 26, l1, l2, ic, col))
    b.append(text(105, ground + 26, "TA's dev workspace", 12.5, INK, 700, "middle", HEAD))
    b.append(text(105, ground + 42, "no production access", 11.5, MUTED, 400, "middle"))
    vx = 905
    b.append(f'<rect x="{vx - 50}" y="{ground - 120}" width="100" height="86" rx="6" fill="#56636f"/>'
             f'<path d="M{vx - 58} {ground - 120} L{vx} {ground - 146} L{vx + 58} {ground - 120} Z" fill="{INK}"/>'
             f'<circle cx="{vx}" cy="{ground - 80}" r="26" fill="#7d8a96" stroke="#c7ced5" stroke-width="3"/>')
    b.append(icon("lock", vx, ground - 80, 15, INK))
    b.append(text(vx, ground + 26, "Production", 12.5, INK, 700, "middle", HEAD))
    b.append(text(vx, ground + 42, "only the Lead deploys", 11.5, MUTED, 400, "middle"))
    b.append(text(24, 280, "Backups are taken before every database change, and the audit log shows who changed what.", 12, MUTED))
    return svg(W, H, "Release gates: pull request, tests, Lead review, owner approval, then production", "".join(b))


def fig_severity():
    W, H = 780, 200
    b = [f'<rect x="40" y="22" width="74" height="160" rx="16" fill="{INK}"/>',
         f'<rect x="70" y="182" width="14" height="14" fill="{INK}"/>']
    rows = [(RED, "Critical", "one company sees another's data, production down, wrong money totals",
             "fix or roll back the same day, owner told within the hour"),
            (AMBER, "High", "a main workflow is broken for some users", "fixed within 2 working days"),
            (GREEN, "Normal or low", "a workaround exists, or it is cosmetic", "planned into next week's work")]
    for i, (col, name, ex, resp) in enumerate(rows):
        cy = 52 + i * 50
        b.append(f'<circle cx="77" cy="{cy}" r="19" fill="{col}"/><circle cx="71" cy="{cy - 6}" r="5" fill="#fff" opacity=".35"/>')
        b.append(f'<line x1="104" y1="{cy}" x2="150" y2="{cy}" stroke="{LINE}" stroke-width="1.5"/>')
        b.append(text(160, cy - 4, name, 15, INK, 700, font=HEAD))
        b.append(text(300, cy - 4, resp, 13, INK, 600))
        b.append(text(300, cy + 13, f"Example: {ex}", 12, MUTED))
    return svg(W, H, "Bug severity levels and response times", "".join(b))


def fig_costs():
    W, H = 1000, 300
    b = [text(24, 32, "What the technology costs", 17, INK, 700, font=HEAD),
         text(24, 52, "One coin = $50 a month. Pale coins show the top of each range. Salaries not included.", 12.5, MUTED)]
    coin = 50
    for i, (label, (lo, hi), sub) in enumerate((("While building", BUILD, "phases 0 to 3"),
                                                ("Live with first customers", LIVE, "from the pilot on"))):
        cx = 150 + i * 270
        solid = round(lo / coin)
        b.append(f'<ellipse cx="{cx}" cy="250" rx="62" ry="8" fill="{SKY}"/>')
        b.append(coin_stack(cx - 20, 248, solid, max(round(hi / coin) - solid, 0)))
        b.append(text(cx + 70, 160, about(lo, hi), 19, INK, 700, font=HEAD))
        b.append(text(cx + 70, 180, "a month", 12.5, MUTED))
        b.append(text(cx, 276, label, 13, INK, 700, "middle", HEAD))
        b.append(text(cx, 292, sub, 11.5, MUTED, 400, "middle"))
    bx = 800
    b.append(f'<path d="M{bx - 52} 246 Q{bx - 66} 170 {bx - 22} 140 L{bx - 34} 118 Q{bx} 106 {bx + 34} 118 L{bx + 22} 140 Q{bx + 66} 170 {bx + 52} 246 Z" fill="#c9a26a"/>'
             f'<path d="M{bx - 26} 136 Q{bx} 146 {bx + 26} 136" stroke="#8d6d4c" stroke-width="4" fill="none"/>')
    b.append(text(bx, 210, "$", 44, "#fff", 700, "middle", HEAD))
    b.append(f'<ellipse cx="{bx}" cy="250" rx="62" ry="8" fill="{SKY}" opacity=".9"/>')
    b.append(text(bx, 276, "One-time and outside people", 13, INK, 700, "middle", HEAD))
    b.append(text(bx, 292, f"${n(ONE[0])} to ${n(ONE[1])} over the project", 11.5, MUTED, 400, "middle"))
    b.append(text(bx - 100, 90, "Mobile contractor, adviser, designer,", 11.5, MUTED))
    b.append(text(bx - 100, 105, "security test, legal review", 11.5, MUTED))
    return svg(W, H, "Monthly and one-time technical costs", "".join(b))


def fig_risks():
    W, H = 1000, 210
    risks = [("plug", "Outside API access", "load boards, ELD, factoring"),
             ("question", "Existing Replit project", "not seen yet, checked in phase 0"),
             ("boxes", "Big scope", "for a two-person team"),
             ("lock", "Company data isolation", "one leak breaks trust"),
             ("doc", "AI document accuracy", "against the 95% goal")]
    b = []
    for i, (ic, t1, t2) in enumerate(risks):
        cx = 100 + i * 200
        b.append(f'<g class="risk-sign" style="transform-origin:{cx}px 144px">')
        b.append(f'<rect x="{cx - 2}" y="104" width="4" height="40" fill="#8a939c"/>')
        b.append(f'<rect x="{cx - 40}" y="32" width="80" height="80" rx="9" fill="{LANE}" stroke="{INK}" stroke-width="2.5" transform="rotate(45 {cx} 72)"/>')
        b.append(f'<rect x="{cx - 34}" y="38" width="68" height="68" rx="6" fill="none" stroke="{INK}" stroke-width="1.2" transform="rotate(45 {cx} 72)"/>')
        b.append(icon(ic, cx, 72, 21, INK).replace('fill="#fff" stroke="#d8dee6"', f'fill="{LANE}" stroke="{LANE}"') + '</g>')
        b.append(text(cx, 168, t1, 13.5, INK, 700, "middle", HEAD))
        b.append(text(cx, 186, t2, 11.5, MUTED, 400, "middle"))
    return svg(W, H, "The five main risks", "".join(b))


def receipt(x, y, title, values, good):
    w, h = 290, 330
    zig = "".join(f" L{x + w - k * 14.5 - 7.25:.2f} {y + h + 8} L{x + w - (k + 1) * 14.5:.2f} {y + h}" for k in range(20))
    b = [f'<path d="M{x} {y} H{x + w} V{y + h}{zig} Z" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>',
         text(x + w / 2, y + 34, title, 17, INK, 700, "middle", HEAD),
         text(x + w / 2, y + 54, "README example load", 11.5, MUTED, 400, "middle"),
         f'<line x1="{x + 16}" y1="{y + 68}" x2="{x + w - 16}" y2="{y + 68}" stroke="{LINE}" stroke-dasharray="4 3"/>']
    labels = [("Fuel cost", "fuel_cost"), ("Dispatch fee", "dispatch_fee"), ("Total cost", "total_cost"),
              ("Profit", "profit"), ("Margin", "margin_pct"), ("Break-even rate", "break_even_rate"),
              ("Suggested rate", "suggested_rate")]
    for i, (lab, key) in enumerate(labels):
        yy = y + 98 + i * 33
        v = values[key]
        shown = f"{v:,.2f}%".replace(".00%", "%") if key == "margin_pct" else money(v)
        b.append(text(x + 40, yy, lab, 13.5, INK))
        b.append(text(x + w - 18, yy, shown, 14, GREEN if good else RED, 700, "end", HEAD))
        mark = (f'<path d="M{x + 18} {yy - 5} L{x + 23} {yy} L{x + 31} {yy - 10}" stroke="{GREEN}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
                if good else
                f'<path d="M{x + 19} {yy - 11} L{x + 29} {yy - 1} M{x + 29} {yy - 11} L{x + 19} {yy - 1}" stroke="{RED}" stroke-width="2.6" stroke-linecap="round"/>')
        b.append(mark)
    return "".join(b)


def fig_bugs():
    W, H = 1000, 420
    b = [receipt(30, 40, "Original code", ORIGINAL, False), receipt(680, 40, "Fixed code", FIXED, True)]
    cx = 500
    # wrench
    b.append(f'<g transform="rotate(-35 {cx} 120)">'
             f'<rect x="{cx - 9}" y="92" width="18" height="96" rx="9" fill="#8a96a3"/>'
             f'<path d="M{cx - 26} 62 A30 30 0 1 0 {cx + 26} 62 L{cx + 13} 62 L{cx + 13} 80 L{cx - 13} 80 L{cx - 13} 62 Z" fill="#8a96a3"/></g>')
    b.append(text(cx, 222, "6 bugs fixed", 24, INK, 700, "middle", HEAD))
    b.append(text(cx, 244, "fuel, dispatch fee, margin, break-even,", 12, MUTED, 400, "middle"))
    b.append(text(cx, 260, "suggested rate, input checks", 12, MUTED, 400, "middle"))
    for i, (lab, ok, total, col) in enumerate((("Tests passing before", 1, 5, RED), ("Tests passing after", 32, 32, GREEN))):
        y = 300 + i * 52
        b.append(text(cx - 140, y, lab, 12.5, INK, 600))
        b.append(text(cx + 140, y, f"{ok} of {total}", 13, col, 700, "end", HEAD))
        b.append(f'<rect x="{cx - 140}" y="{y + 8}" width="280" height="14" rx="7" fill="{SKY}"/>')
        b.append(f'<rect x="{cx - 140}" y="{y + 8}" width="{280 * ok / total:.0f}" height="14" rx="7" fill="{col}"/>')
    b.append(f'<path d="M340 150 H392 M380 140 L392 150 L380 160 M608 150 H660 M648 140 L660 150 L648 160" stroke="{LINE}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    return svg(W, H, "Before and after the fix, on the README example load", "".join(b))


FIGURES = {
    "glance": fig_glance, "roadmap": fig_roadmap, "scenarios": fig_scenarios, "team": fig_team,
    "gates": fig_gates, "severity": fig_severity, "costs": fig_costs, "risks": fig_risks, "bugs": fig_bugs,
}


def cover_scene():
    """Full-page cover drawing for the PDF (1056 x 816, Letter landscape at 96 dpi)."""
    W, H = 1056, 816
    ms = REAL["milestones"]
    b = ['<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe4f3"/>'
         '<stop offset="1" stop-color="#f4f9fd"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
         '<circle cx="900" cy="140" r="58" fill="#fde7b0"/>']
    for k, (x, w, h) in enumerate(((640, 34, 120), (680, 26, 170), (712, 40, 140), (758, 22, 200), (786, 36, 110),
                                    (828, 30, 150), (864, 44, 95), (914, 26, 135), (946, 38, 180), (990, 30, 120))):
        b.append(f'<rect x="{x}" y="{560 - h}" width="{w}" height="{h}" fill="#b4c7d6"/>')
        for wy in range(560 - h + 12, 548, 18):
            b.append(f'<rect x="{x + 6}" y="{wy}" width="{w - 12}" height="5" fill="#cddbe6"/>')
    b.append('<path d="M0 600 Q180 520 380 566 T760 548 T1056 556 V640 H0 Z" fill="#cfe3d4"/>')
    b.append('<path d="M0 628 Q260 580 520 612 T1056 600 V640 H0 Z" fill="#b6d5bf"/>')
    b.append(road(0, W, 636, 86))
    b.append(f'<rect x="0" y="722" width="{W}" height="{H - 722}" fill="#9fc9a8"/>')
    b.append(truck(70, 700, 1.15))
    x0, x1 = 400, 990
    last = ms[4][0]
    labels = ["Pilot", "Version 1", "Tracking", "Back office", "Full platform"]
    for i, ((wk, day), lab) in enumerate(zip(ms, labels)):
        x = x0 + (x1 - x0) * (wk - ms[0][0]) / (last - ms[0][0])
        if i == 4:
            b.append(flag(x + 2, 636, 64))
            x -= 36
        b.append(signpost(x, 636, f"M{i + 1} {lab}", d(day), 116 if i == 4 else 96, post=52 + (i % 2) * 40))
    return svg(W, H, "A car-hauler truck on the road past five milestone signs", "".join(b), bg=False)


def main():
    out = HERE.parent / "docs"
    out.mkdir(exist_ok=True)
    for name, fn in FIGURES.items():
        (out / f"{name}.svg").write_text(fn(), encoding="utf8")
    print("wrote", ", ".join(f"docs/{k}.svg" for k in FIGURES))


if __name__ == "__main__":
    main()

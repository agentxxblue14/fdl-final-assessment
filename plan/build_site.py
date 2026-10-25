"""Build index.html, the interactive version of the submission.

All numbers come from estimate_model.py and profitability.py, and the drawings from figures.py,
so the page cannot drift from PLAN.md. Run: python plan/build_site.py
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import estimate_model as m  # noqa: E402
import figures as f  # noqa: E402

PHASE_NAMES = {p: name.split(": ", 1)[1] for p, name in m.PHASES.items()}
MILESTONE_OF_PHASE = {0: 1, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 5}
MILESTONE_NAMES = ["Internal pilot", "Customer-ready version 1", "Tracking and fleet compliance",
                   "Automated back office", "Full platform"]
NOTES = {
    "Optimistic": "Low hours, 35 productive hours a week, fast owner decisions and vendor approvals.",
    "Realistic": "Likely hours plus 15% contingency, 32 productive hours a week, some vendor delays.",
    "Conservative": "High hours, 28 productive hours a week, a provider refuses access, scope grows.",
}


def data():
    scenarios = {}
    for name, v in f.SC.items():
        start, phases = 0.0, []
        for r in v["rows"]:
            phases.append(dict(phase=r["phase"], name=PHASE_NAMES[r["phase"]], start=round(start, 2),
                               end=round(r["end"], 2), lead=round(r["lead"]), ta=round(r["ta"])))
            start = r["end"]
        scenarios[name] = dict(
            phases=phases, total=round(v["total"]), lead=round(v["lead"]), ta=round(v["ta"]),
            contractor=round(v["contractor"]), note=NOTES[name],
            apps=dict(start=phases[5]["start"], end=phases[7]["end"]),
            milestones=[dict(week=wk, date=f.d(day)) for wk, day in v["milestones"]])
    workstreams = [dict(id=w[0], phase=w[1], name=w[2], low=w[4], likely=w[5], high=w[6],
                        lead=None if w[0] == m.NATIVE_APPS else m.LEAD_SHARE[w[0]],
                        staff=w[8], milestone=MILESTONE_OF_PHASE[w[1]]) for w in m.WORKSTREAMS]
    one_time = [dict(name=r[0], low=r[2], high=r[3]) for r in f.ONE_TIME]
    return dict(
        start=f.d(m.START), scenarios=scenarios, workstreams=workstreams, milestoneNames=MILESTONE_NAMES,
        costs=dict(build=[dict(name=c[0], low=c[1], high=c[2]) for c in m.COSTS_BUILD],
                   live=[dict(name=c[0], low=c[1], high=c[2]) for c in m.COSTS_LIVE],
                   buildTotal=f.about(*f.BUILD), liveTotal=f.about(*f.LIVE),
                   oneTime=one_time, oneTimeTotal=f"${f.n(f.ONE[0])} to ${f.n(f.ONE[1])}"),
        bugs=dict(original=f.ORIGINAL, fixed=f.FIXED),
    )


def main():
    page = (HERE / "site_template.html").read_text(encoding="utf8")
    real = f.REAL
    cover_ms = "".join(
        f'<g class="hero-sign" data-x="{300 + i * 195}">{f.signpost(300 + i * 195, 150, "M%d %s" % (i + 1, lab), f.d(day), 112 if i == 4 else 100, post=48 + (i % 2) * 22)}</g>'
        for i, ((wk, day), lab) in enumerate(zip(real["milestones"], ["Pilot", "Version 1", "Tracking", "Back office", "Full platform"])))
    parts = {
        "/*DATA*/": json.dumps(data(), separators=(",", ":")),
        "<!--HERO_SIGNS-->": cover_ms,
        "<!--HERO_TRUCK-->": f.truck(0, 196, .9),
        "<!--HERO_FLAG-->": f.flag(1150, 150, 52),
        "<!--TEAM-->": f.fig_team(),
        "<!--GATES-->": f.fig_gates(),
        "<!--RISKS-->": f.fig_risks(),
        "<!--SEVERITY-->": f.fig_severity(),
    }
    for key, value in parts.items():
        assert page.count(key) == 1, key
        page = page.replace(key, value)
    for ch in ("–", "—"):
        assert ch not in page, "dash in page text"
    out = HERE.parent / "index.html"
    out.write_text(page, encoding="utf8")
    print(out, f"{out.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

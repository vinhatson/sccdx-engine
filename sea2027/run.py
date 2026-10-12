# -*- coding: utf-8 -*-
"""
sea2027.run - the 2027 qualitative reading for the eleven ASEAN states
=======================================================================
    python sea2027/run.py            # Vietnamese report, the default
    python sea2027/run.py --lang en
    python sea2027/run.py --json out.json

WHAT "2027" MEANS HERE
----------------------
Run date is 2026-10-09. The engine integrates forward from the measured
present, so the 2027 reading is the state at t = 1.23 years - end of calendar
2027 - taken from `horizon_verdict` on a run with horizon_years = 1.23. A
second pass at 15 years is kept alongside it, not as a longer forecast but
because the gate ORDER and the loop set are the things the engine is actually
good for, and both are invisible inside fifteen months.

Three sensitivity passes run on top:
  1. OAT +/-20% on the threshold parameters, per sccd Part IV eq (SA), against
     the qualitative verdict rather than against a number
  2. Monte-Carlo measurement bands on the ten sub-components
  3. two named counterfactuals on the two most arguable ANALYST inputs in
     sea2027/judgment.py - Singapore's state_type and Vietnam's a4

Nothing below is a probability, a date or an actionable level. See README
section 10, and read `calibration` in the JSON before quoting anything.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for p in (ROOT, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

from sccdx.engine2 import diagnose2, _oat_targets
from sccdx.events import EventInput
from sccdx.world import diagnose_world, PolityInput
from sccdx import i18n, i18n_render, narrative
# i18n_ui mirrors its table into i18n.T at import time, and the
# narrative layer looks up res.* / w.* / th.* through T. serve.py gets
# that import for free; a standalone script has to ask for it, or
# narrate() raises on the first missing template under strict mode.
import sccdx.i18n_ui  # noqa: F401  (registers 199 more templates)

import mapping as M
from judgment import JUDGMENT

N_OAT = len(_oat_targets())
RUN_DATE = "2026-10-09"
BASE_YEAR = 2026
H_2027 = 1.23          # 2026-10-09 -> 2027-12-31
H_LONG = 15.0
MC_DRAWS = 400

# ---------------------------------------------------------------------------
# THE 2027 STRESS BRANCH
#
# README section 7 is blunt about the discipline here: an event is a level
# shift for something that has NOT happened yet, or has happened but is not
# yet in the numbers entered - it is not for re-describing the baseline. Set
# s3 low because a scandal is already in the polling AND switch on
# corruption_scandal, and you have charged the same scandal twice; the engine
# cannot detect it.
#
# So every event below is strictly PROSPECTIVE as of 2026-10-09, and the
# conditions already in the baseline are deliberately NOT re-entered:
#   - no mass_protest for Indonesia or the Philippines; the 2025-26 waves are
#     already inside `unrest` and inside protest/c2
#   - no civil_conflict for Myanmar; conflict=0.95 already says no actor holds
#     a monopoly
#   - no haven_flight_surge anywhere; a4 is a 2026 measured/argued level
#   - no corruption_scandal for the Philippines or Thailand; both are priced
#     into s3 through `unrest`
#
# tariff_war is applied region-wide because it is one shock with one source,
# which is precisely the configuration Sync_Risk is supposed to detect.
STRESS = {
 "ID": [("tariff_war", 0.50), ("sovereign_debt_stress", 0.50),
        ("currency_crisis", 0.40)],
 "SG": [("tariff_war", 0.60), ("whitecollar_displacement", 0.60),
        ("agency_crisis_visible", 0.40)],
 "TH": [("tariff_war", 0.55), ("constitutional_crisis", 0.50),
        ("pension_reform_failure", 0.40)],
 "VN": [("tariff_war", 0.70), ("whitecollar_displacement", 0.40),
        ("inflation_surge", 0.40)],
 "PH": [("tariff_war", 0.40), ("constitutional_crisis", 0.45),
        ("whitecollar_displacement", 0.50)],
 "MY": [("tariff_war", 0.55), ("polarising_election", 0.60)],
 "MM": [("relief_system_failure", 0.60), ("currency_crisy_placeholder", 0.0)],
 "KH": [("tariff_war", 0.60), ("interstate_war_onset", 0.45)],
 "LA": [("sovereign_debt_stress", 0.50), ("inflation_surge", 0.50)],
 "BN": [("energy_shock", 0.60)],
 "TL": [("relief_system_failure", 0.40), ("youth_unemployment_surge", 0.50)],
}
STRESS["MM"] = [("relief_system_failure", 0.60), ("currency_crisis", 0.60)]

STRESS_WHY = {
 "ID": "a breach of the 3% deficit cap crystallising the Moody's negative "
       "outlook, plus rupiah pressure. Neither is in the baseline; the "
       "protests already are.",
 "SG": "the displacement OUTCOME of an adoption rate already measured at "
       "64.3%. a1 is what people use; whitecollar_displacement is what it "
       "does to them, and that has not happened yet.",
 "TH": "the Article 151 motion resolving against the government, plus the "
       "pension commitment failing rather than being reformed. pension=0.70 "
       "is the size of the commitment, not its failure.",
 "VN": "the highest tariff exposure in the set (trade at 190% of GDP), plus "
       "the IMF's own inflation path (3.3% in 2025 to 4.9% in 2026 and 4.6% "
       "in 2027) and white-collar displacement on a1=0.279.",
 "PH": "the impeachment verdict and its aftermath, plus BPO displacement on "
       "the region's highest white-collar exposure.",
 "MY": "GE16, due by February 2028 and possibly early. The state-level "
       "losses are baseline; the national election is not.",
 "MM": "relief-system failure and a further currency break. The war itself "
       "is baseline - adding civil_conflict would charge the coup twice.",
 "KH": "border re-escalation as an ONSET rather than as standing pressure. "
       "Note the catalogue has interstate_war_onset RAISING s2 and s3 - the "
       "rally effect sccd Part V documents for 1941-45 - so this event is "
       "not uniformly adverse, and that is the engine's reading, not mine.",
 "LA": "a default or restructuring event on liabilities the IMF already "
       "calls unsustainable, plus inflation back through 10%.",
 "BN": "an oil-price downside on a single-commodity revenue base with 2025 "
       "growth already at 0.7%.",
 "TL": "Petroleum Fund drawdown outrunning the ESI, plus the youth cohort "
       "arriving with NEET already at 29.1%.",
}

# Per-component measurement SD in normalised units, for the Monte-Carlo pass.
# Two things set each number: the proxy QUALITY sccd Part III assigns the
# component, and how much of THIS dataset's value for it is ANALYST rather
# than measured. The second consideration dominates. A component the paper
# rates High quality but which I built on an argued coefficient does not
# deserve a High-quality band.
#
#   s3  0.13  Part III's own highest-risk proxy, and BLOCKED: P.4 L_vol has no
#             cross-national source and P.6 L_comply has no panel. On top of
#             that the `unrest` drawdown is an argued number.
#   c5  0.13  fully ANALYST for all eleven - no audience-overlap series, no
#             comparable legislative-polarisation scale for ASEAN
#   s2  0.10  UCDP is token-gated, so the conflict arm is ANALYST
#   c1  0.10  Gini standing in for a top-1% wealth share, PAF argued
#   s4  0.07  Med-High, but the implemented/enacted ratio is CODING-only
#   c2  0.07  Med-High; the coordination-effectiveness arm is ANALYST
#   c4  0.07  High on the capital arm (Chinn-Ito), argued on labour and IP
#   s5  0.07  Medium; fiscal-component-only fallback, no T_horizon term
#   s1  0.06  High, but the mandatory-spending split is not in any feed
#   c3  0.05  the best-sourced of the ten here: RSF 2026 + V-Dem + WDI
SIGMA = {"s1": 0.06, "s2": 0.10, "s3": 0.13, "s4": 0.07, "s5": 0.07,
         "c1": 0.10, "c2": 0.07, "c3": 0.05, "c4": 0.07, "c5": 0.13}


# ---------------------------------------------------------------------------
def run_all(mc_draws: int = MC_DRAWS):
    pols, provs = M.build_all()

    short, long = {}, {}
    for p in pols:
        kw = dict(demo=p.demo, disp=p.disp, state_type=p.state_type,
                  revenue_polarisation=p.revenue_polarisation,
                  security_pressure=p.security_pressure,
                  base_revenue_demand=p.base_revenue_demand)
        short[p.code] = diagnose2(p.name, BASE_YEAR, p.sub,
                                  horizon_years=H_2027, mc_draws=mc_draws, sigma=SIGMA,
                                  with_trajectory=True, with_sensitivity=True,
                                  **kw)
        long[p.code] = diagnose2(p.name, BASE_YEAR, p.sub,
                                 horizon_years=H_LONG,
                                 with_trajectory=True, with_sensitivity=False,
                                 **kw)

    world_2027 = diagnose_world(pols, BASE_YEAR, horizon_years=H_2027)
    world_long = diagnose_world(pols, BASE_YEAR, horizon_years=H_LONG)

    # --- counterfactual 1: Singapore read as a liberal democracy -----------
    sg_alt_pol, _ = M.build("SG", state_type_override="liberal_democracy")
    sg_alt = diagnose2(sg_alt_pol.name, BASE_YEAR, sg_alt_pol.sub,
                       demo=sg_alt_pol.demo, disp=sg_alt_pol.disp,
                       state_type="liberal_democracy",
                       revenue_polarisation=sg_alt_pol.revenue_polarisation,
                       security_pressure=sg_alt_pol.security_pressure,
                       base_revenue_demand=sg_alt_pol.base_revenue_demand,
                       horizon_years=H_2027, with_sensitivity=False)

    # --- counterfactual 2: Vietnam's a4 read off volume, not premium -------
    vn_alt_pol, _ = M.build("VN", haven_override=0.40)
    vn_alt = diagnose2(vn_alt_pol.name, BASE_YEAR, vn_alt_pol.sub,
                       demo=vn_alt_pol.demo, disp=vn_alt_pol.disp,
                       state_type=vn_alt_pol.state_type,
                       revenue_polarisation=vn_alt_pol.revenue_polarisation,
                       security_pressure=vn_alt_pol.security_pressure,
                       base_revenue_demand=vn_alt_pol.base_revenue_demand,
                       horizon_years=H_2027, with_sensitivity=False)

    # --- the 2027 stress branch -------------------------------------------
    stress, stress_pols = {}, []
    for p in pols:
        ev = [EventInput(id=i, intensity=x) for i, x in STRESS.get(p.code, [])]
        stress[p.code] = diagnose2(
            p.name, BASE_YEAR, p.sub, demo=p.demo, disp=p.disp,
            state_type=p.state_type,
            revenue_polarisation=p.revenue_polarisation,
            security_pressure=p.security_pressure,
            base_revenue_demand=p.base_revenue_demand,
            events=ev, horizon_years=H_2027, with_sensitivity=False)
        q = PolityInput(**{k: v for k, v in vars(p).items() if k != "events"})
        q.events = ev
        stress_pols.append(q)
    world_stress = diagnose_world(stress_pols, BASE_YEAR,
                                  horizon_years=H_2027)

    return dict(polities=pols, provenance=provs, short=short, long=long,
                world_2027=world_2027, world_long=world_long,
                sg_alt=sg_alt, vn_alt=vn_alt,
                stress=stress, world_stress=world_stress)


# ---------------------------------------------------------------------------
def _v(d, lang):
    return i18n_render.localize_diagnosis(d.as_dict(traj_stride=1), lang)


def report(res, lang="vi") -> str:
    lang = i18n.norm_lang(lang)
    L = []
    w = L.append
    w("=" * 78)
    w(f"SCCD-X v2.00  -  11 ASEAN polities  -  run {RUN_DATE}  -  lang={lang}")
    w("=" * 78)

    pols = {p.code: p for p in res["polities"]}
    order = sorted(pols, key=lambda c: -pols[c].weight)

    # ---- 1. the input table ----------------------------------------------
    w("")
    w("--- 1. EFFECTIVE INPUTS (post boundary compression, pre forcing) ----")
    keys = ["s1", "s2", "s3", "s4", "s5", "c1", "c2", "c3", "c4", "c5"]
    w("code " + "".join(k.rjust(7) for k in keys) + "    wt  state_type")
    for c in order:
        p = pols[c]; d = p.sub.as_dict()
        w(c.ljust(5) + "".join(f"{d[k]:.3f}".rjust(7) for k in keys)
          + f"  {p.weight:5.3f}  {p.state_type}")
    w("")
    w("code " + "".join(k.rjust(7) for k in ["d1", "d2", "d3", "d4", "d5"])
      + "  |" + "".join(k.rjust(7) for k in ["a1", "a2", "a3", "a4", "a5", "a6"]))
    for c in order:
        p = pols[c]; d = p.demo.as_dict(); a = p.disp.as_dict()
        w(c.ljust(5)
          + "".join(f"{d[k]:.3f}".rjust(7) for k in ["d1", "d2", "d3", "d4", "d5"])
          + "  |"
          + "".join(f"{a[k]:.3f}".rjust(7) for k in ["a1", "a2", "a3", "a4", "a5", "a6"]))

    aud = M.audit(res["provenance"])
    w("")
    w(f"provenance over {aud['n_fields']} derived fields: " +
      ", ".join(f"{k}={v}" for k, v in sorted(aud["counts"].items())))

    # ---- 2. the 2027 verdict ---------------------------------------------
    w("")
    w("--- 2. THE 2027 VERDICT  (state at t=1.23y, from horizon_verdict) ---")
    for c in order:
        d = res["short"][c]
        loc = _v(d, lang)
        now, fut = loc["verdict"], loc.get("horizon_verdict") or loc["verdict"]
        tr = d.trajectory
        w("")
        w(f"[{c}] {pols[c].name}   ({pols[c].state_type})")
        w(f"   2026 : {now['regime_text']} / {now['coherence_tier_text']} ; "
          f"{now['adjustment_mode_text']} ; Psi={d.capacity.psi:.3f} "
          f"th25={d.capacity.theta25:.3f} Dn={d.capacity.delta_norm:+.3f}")
        w(f"   2027 : {fut['regime_text']} / {fut['coherence_tier_text']} ; "
          f"{fut['adjustment_mode_text']} ; Psi={tr.psi[-1]:.3f} "
          f"th25={tr.theta25[-1]:.3f} Dn={tr.delta_norm[-1]:+.3f}")
        w(f"   gate : {loc['verdict']['gate_text']}")
        w(f"   loops: {'+'.join(d.verdict.active_loops) or 'none'}   "
          f"CAI core={d.verdict.cai_core:.3f} ext={d.verdict.cai_ext:.3f}   "
          f"R_B={d.verdict.R_B}   decoupled={d.verdict.decoupling_active}")
        dd = d.bifurcation.get("d_delta_dt")
        w(f"   dDn/dt={(tr.delta_norm[-1]-tr.delta_norm[0])/H_2027:+.4f}/yr  "
          f"measured dD/dt={dd:+.4f}" if dd is not None else "")
        if d.uncertainty:
            u = d.uncertainty
            w(f"   MC   : Dn median={u.median_delta_norm:+.3f} "
              f"ci80=[{u.ci80[0]:+.3f},{u.ci80[1]:+.3f}] "
              f"Psi median={u.median_psi:.3f}")
            top = sorted(u.regime_distribution.items(), key=lambda kv: -kv[1])[:3]
            w("          regime mix: " +
              ", ".join(f"{i18n.regime(k, lang)} {v:.0%}" for k, v in top))
        flips = [f for f in d.fragility if f.flips_low or f.flips_high]
        if flips:
            w(f"   OAT  : {len(flips)} of {N_OAT} parameters flip the verdict "
              f"at +/-20% -> " + ", ".join(f.parameter for f in flips[:6]))
            for f in flips[:3]:
                for ch in f.changed[:2]:
                    w(f"          {f.parameter} {ch['side']}: "
                      f"{ch['field']} {ch['from']} -> {ch['to']}")
        else:
            w(f"   OAT  : none of {N_OAT} parameters flips the verdict "
              f"at +/-20%")

    # ---- 3. gate order over fifteen years --------------------------------
    w("")
    w("--- 3. GATE ORDER AND LOOP SET OVER 15 YEARS ------------------------")
    w("code  2041 band / tier                 gate            loops")
    for c in order:
        d = res["long"][c]
        loc = _v(d, lang)
        hv = loc.get("horizon_verdict") or loc["verdict"]
        w(f"{c.ljust(5)} {(hv['regime_text'] + ' / ' + hv['coherence_tier_text'])[:32].ljust(33)}"
          f"{loc['verdict']['gate_code'].ljust(16)}"
          f"{'+'.join(d.verdict.active_loops) or 'none'}")
    w("")
    for c in order:
        d = res["long"][c]
        projs = d.forcing.as_dict().get("gates", []) or []
        if not projs:
            continue
        rows = [p for p in projs if p.get("years_to_gate") is not None]
        if not rows:
            continue
        rows.sort(key=lambda r: r["years_to_gate"])
        w(f"{c}: " + ", ".join(
            f"{r['component']}->{r['threshold']:.2f} in {r['years_to_gate']:.1f}y"
            for r in rows[:4]))

    # ---- 4. the system ---------------------------------------------------
    w("")
    w("--- 4. THE SYSTEM THEY FORM ----------------------------------------")
    w("")
    w("Psi_G is a SNAPSHOT aggregate over the eleven current capacity "
      "vectors, not")
    w("a trajectory, so the 2027 and 2041 passes return the same number by "
      "construction;")
    w("the horizon only moves each polity's own path. One row is printed, "
      "plus the")
    w("stress branch, which does move it because events shift the levels "
      "Psi_G reads.")
    for tag, wd in (("baseline", res["world_2027"]),
                    ("stress  ", res["world_stress"])):
        lw = i18n_render.localize_world(wd.as_dict(), lang)
        w("")
        w(f"[{tag}] Psi_G={wd.psi_G:.4f} (crit {wd.psi_G_crit:.3f})  "
          f"Sync_Risk={wd.sync_risk:.3f} "
          f"(prior {wd.sync_risk_prior:.3f} + haven {wd.sync_risk_haven:.3f})")
        w(f"      CAI_weighted={wd.cai_weighted:.3f}  "
          f"adjustment divergence={wd.adjustment_divergence:.3f}  "
          f"AI divergence={wd.ai_divergence:.3f}  "
          f"haven pressure={wd.haven_pressure:.3f}")
        w(f"      hegemon={wd.hegemon}  challenger={wd.challenger}  "
          f"R_B,G={wd.global_bifurcation.get('R_B_G')}")
        for k, v in sorted(wd.adjustment_split.items()):
            if v:
                w(f"      {k}: {' '.join(v)}")
        if lw.get("verdict"):
            w(f"      verdict: {lw['verdict']}")
        if lw.get("warnings"):
            for x in lw["warnings"][:6]:
                w(f"      ! {x}")
        tg = wd.talent_gradient[:5]
        if tg:
            w("      talent gradient: " + ", ".join(
                f"{r['origin']}->{r['destination']} {r['pressure']:.4f}"
                for r in tg))
        else:
            w("      talent gradient: empty - no origin/destination pair "
              "clears d5>0.45 AND d4>0.45 anywhere in the region")

    # ---- 5. counterfactuals ----------------------------------------------
    w("")
    w("--- 5. THE TWO MOST ARGUABLE ANALYST INPUTS -------------------------")
    base_sg = res["short"]["SG"]; alt_sg = res["sg_alt"]
    w("")
    w("SG state_type: developmental_autocracy (used) vs liberal_democracy")
    for tag, d in (("used", base_sg), ("alt ", alt_sg)):
        hv = d.horizon_verdict or d.verdict
        w(f"   {tag}: 2027 {i18n.regime(hv.regime, lang)} / "
          f"{i18n.tier(hv.coherence_tier, lang)} ; "
          f"Psi={d.trajectory.psi[-1]:.3f} Dn={d.trajectory.delta_norm[-1]:+.3f} "
          f"R_B={hv.R_B} loops={'+'.join(d.verdict.active_loops) or 'none'}")
    base_vn = res["short"]["VN"]; alt_vn = res["vn_alt"]
    w("")
    w("VN a4 haven: 0.70 from the premium (used) vs 0.40 from the volume")
    for tag, d in (("used", base_vn), ("alt ", alt_vn)):
        hv = d.horizon_verdict or d.verdict
        w(f"   {tag}: 2027 {i18n.regime(hv.regime, lang)} / "
          f"{i18n.tier(hv.coherence_tier, lang)} ; "
          f"Psi={d.trajectory.psi[-1]:.3f} Dn={d.trajectory.delta_norm[-1]:+.3f} "
          f"R_B={hv.R_B} loops={'+'.join(d.verdict.active_loops) or 'none'}")

    # ---- 6. the stress branch -------------------------------------------
    w("")
    w("--- 6. THE 2027 STRESS BRANCH (prospective events only) -------------")
    w("Baseline -> stress, both read at t=1.23y. Events are level shifts for")
    w("things that have NOT happened; see STRESS in this file for what was")
    w("deliberately left out of each row to avoid charging it twice.")
    for c in order:
        b, st = res["short"][c], res["stress"][c]
        bh = b.horizon_verdict or b.verdict
        sh = st.horizon_verdict or st.verdict
        shifted = (bh.regime != sh.regime
                   or bh.coherence_tier != sh.coherence_tier
                   or bh.adjustment_mode != sh.adjustment_mode
                   or bh.R_B != sh.R_B
                   or b.verdict.active_loops != st.verdict.active_loops)
        w("")
        w(f"[{c}] " + ("VERDICT MOVES" if shifted else "verdict holds")
          + "   events: "
          + ", ".join(f"{i}@{x:.2f}" for i, x in STRESS.get(c, [])))
        w(f"   base  : {i18n.regime(bh.regime, lang)} / "
          f"{i18n.tier(bh.coherence_tier, lang)} / "
          f"{i18n.mode(bh.adjustment_mode, lang)} ; "
          f"Psi={b.trajectory.psi[-1]:.3f} Dn={b.trajectory.delta_norm[-1]:+.3f} "
          f"th25={b.trajectory.theta25[-1]:.3f} R_B={bh.R_B} "
          f"loops={'+'.join(b.verdict.active_loops) or 'none'}")
        w(f"   stress: {i18n.regime(sh.regime, lang)} / "
          f"{i18n.tier(sh.coherence_tier, lang)} / "
          f"{i18n.mode(sh.adjustment_mode, lang)} ; "
          f"Psi={st.trajectory.psi[-1]:.3f} Dn={st.trajectory.delta_norm[-1]:+.3f} "
          f"th25={st.trajectory.theta25[-1]:.3f} R_B={sh.R_B} "
          f"loops={'+'.join(st.verdict.active_loops) or 'none'}")
        w(f"   why   : {STRESS_WHY.get(c, '')}")
        if st.events:
            for a in st.events.as_dict().get("audit", []):
                ap = a.get("applied", {})
                w(f"   shift  {a['id']}@{a['intensity']:.2f}: " + " ".join(
                    f"{k}{v:+.3f}" for k, v in ap.items()))
            cl_ = st.events.as_dict().get("clamped") or []
            if cl_:
                w(f"   clamped at the [0,1] boundary: {cl_}")

    # ---- 7. narratives ---------------------------------------------------
    w("")
    w("--- 7. NARRATIVE PER POLITY ----------------------------------------")
    for c in order:
        w("")
        w(f"### {c} {pols[c].name}")
        # serve.py's comment at line 167 is the rule: localise FIRST, then
        # narrate - narrate() reads the rendered dict, so handing it a raw
        # payload prints None for every band, tier, mode and loop name.
        w(narrative.narrate(
            i18n_render.localize_diagnosis(
                res["short"][c].as_dict(traj_stride=6), lang), lang=lang))
    w("")
    w("### WORLD")
    w(narrative.narrate_world(
        i18n_render.localize_world(res["world_2027"].as_dict(), lang),
        lang=lang))

    # ---- 7. calibration --------------------------------------------------
    w("")
    w("--- 8. CALIBRATION ---------------------------------------------------")
    w(json.dumps(res["short"]["VN"].calibration, indent=1, ensure_ascii=False))
    return "\n".join(L)


def dump(res, path, lang="vi"):
    pols = {p.code: p for p in res["polities"]}
    out = {
        "run_date": RUN_DATE, "base_year": BASE_YEAR,
        "horizon_2027_years": H_2027, "horizon_long_years": H_LONG,
        "lang": lang,
        "inputs": {c: {"name": p.name, "state_type": p.state_type,
                       "weight": p.weight,
                       "sub": p.sub.as_dict(), "demo": p.demo.as_dict(),
                       "disp": p.disp.as_dict(),
                       "revenue_polarisation": p.revenue_polarisation,
                       "security_pressure": p.security_pressure,
                       "base_revenue_demand": p.base_revenue_demand,
                       "ret": p.ret, "opportunity": p.opportunity,
                       "capital_controls": p.capital_controls,
                       "skilled_supply": p.skilled_supply}
                   for c, p in pols.items()},
        "provenance": {c: {k: {"tag": t, "terms": x}
                           for k, (t, x) in pr.items()}
                       for c, pr in res["provenance"].items()},
        "judgment": {c: {k: v for k, v in j.items()}
                     for c, j in JUDGMENT.items()},
        "audit": M.audit(res["provenance"]),
        "diagnosis_2027": {c: i18n_render.localize_diagnosis(
            d.as_dict(traj_stride=6), lang) for c, d in res["short"].items()},
        "diagnosis_15y": {c: i18n_render.localize_diagnosis(
            d.as_dict(traj_stride=12), lang) for c, d in res["long"].items()},
        "world_2027": i18n_render.localize_world(
            res["world_2027"].as_dict(), lang),
        "world_15y": i18n_render.localize_world(
            res["world_long"].as_dict(), lang),
        "stress_2027": {c: i18n_render.localize_diagnosis(
            d.as_dict(traj_stride=12), lang) for c, d in res["stress"].items()},
        "world_stress_2027": i18n_render.localize_world(
            res["world_stress"].as_dict(), lang),
        "stress_design": {"events": STRESS, "rationale": STRESS_WHY},
        "sigma": SIGMA,
        "counterfactuals": {
            "SG_liberal_democracy": i18n_render.localize_diagnosis(
                res["sg_alt"].as_dict(traj_stride=12), lang),
            "VN_haven_from_volume": i18n_render.localize_diagnosis(
                res["vn_alt"].as_dict(traj_stride=12), lang),
        },
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    return path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="vi")
    ap.add_argument("--json", default="")
    ap.add_argument("--mc", type=int, default=MC_DRAWS)
    a = ap.parse_args()
    res = run_all(mc_draws=a.mc)
    txt = report(res, a.lang)
    sys.stdout.reconfigure(encoding="utf-8")
    print(txt)
    if a.json:
        print("\nJSON ->", dump(res, a.json, a.lang), file=sys.stderr)

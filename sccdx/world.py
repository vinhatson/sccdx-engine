# -*- coding: utf-8 -*-
"""
SCCD-X — World Layer
=====================
Runs diagnose2 across a set of polities, assembles them into sccd's network
layer (Part IV 4-6), and adds the two global aggregates the new papers imply.

WHAT THE NEW BLOCKS ADD AT THE WORLD LEVEL
------------------------------------------
1. SYNC_RISK GETS AN ENDOGENOUS DRIVER. sccd's Psi_G is a weighted coherence
   aggregate discounted by Sync_Risk, and Sync_Risk in v1.00 is a bare
   historical prior - the four numbers 0.12 / 0.24 / 0.41 / 0.58 for 1980 /
   1995 / 2010 / 2024, with no generating mechanism. Displacement supplies
   one: haven flight is simultaneous across systemically weighted states
   because its cause is a shared psychological shift rather than any
   country's local conditions. The paper's own breadth-of-demand argument is
   the support - demand "across all investor types". So the engine computes
   Sync_Risk as the historical prior PLUS a haven term, and reports both
   parts separately so the prior is never silently overwritten.

2. ADJUSTMENT DIVERGENCE IS THE MIGRATION GRADIENT. Degrow's two channels
   coexist on one planet: polities in voluntary mode have inverting pyramids
   and need workers, polities in violent-exposed mode have surplus youth with
   no stake. The DISPERSION of d3 across the world is therefore not a
   statistical curiosity, it is the pressure differential driving sccd's
   existing F^talent channel. A world where every polity shares the same d3
   has no such gradient regardless of how high the pressure is.

HONESTY NOTE
------------
sccd flags Psi_G as UNCALIBRATED in v1.00 because the paper specifies its
properties but not its closed form. Everything added here is ANALYST on top
of that. The world verdict is a structural reading - which faults are loaded,
and whether they are loaded together - and explicitly not a forecast of any
event or date. sccd Part IV 6.3's own words for R_B,G: it "identifies a
structural condition (overloaded-fault analogy), NOT a prediction of a
specific event or timeline".
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from sccd import network as net1
from sccd import spec as s1spec
from sccd.aggregate import SubComponents
from . import spec2
from .engine2 import Diagnosis2, diagnose2
from .events import EventInput
from .forcing import DemoBlock, DispBlock


@dataclass
class PolityInput:
    """One polity's full input bundle."""
    code: str
    name: str
    sub: SubComponents
    demo: DemoBlock
    disp: DispBlock
    state_type: str = "liberal_democracy"
    weight: float = 1.0              # systemic weight for Psi_G
    revenue_polarisation: float = 0.0
    security_pressure: float = 0.0
    base_revenue_demand: float = 0.0
    g_shock: float = 0.0
    events: List[EventInput] = field(default_factory=list)
    # network-channel inputs (sccd Part IV N.3-N.6)
    ret: float = 0.0                 # risk-adjusted return
    opportunity: float = 0.0
    capital_controls: float = 0.0
    skilled_supply: float = 0.0
    provenance: str = "ANALYST prior"
    confidence: str = "low"


@dataclass
class WorldDiagnosis:
    year: int
    polities: Dict[str, dict]            # code -> Diagnosis2.as_dict()
    psi_G: float
    psi_G_crit: float
    sync_risk: float
    sync_risk_prior: float
    sync_risk_haven: float
    cai_weighted: float
    thucydides: dict
    global_bifurcation: dict
    adjustment_divergence: float
    adjustment_split: Dict[str, List[str]]
    ai_divergence: float
    haven_pressure: float
    talent_gradient: List[dict]
    flow_matrix: List[List[float]]
    flow_codes: List[str]
    hegemon: Optional[str]
    challenger: Optional[str]
    verdict_parts: List[tuple] = field(default_factory=list)
    warning_codes: List[tuple] = field(default_factory=list)

    def as_dict(self) -> dict:
        d = asdict(self)
        d["verdict_parts"] = [list(x) for x in self.verdict_parts]
        d["warning_codes"] = [list(x) for x in self.warning_codes]
        return d


def _weighted_dispersion(vals: Sequence[float], w: Sequence[float]) -> float:
    """Weighted standard deviation, normalised to [0,1] by its maximum.

    A two-point distribution at 0 and 1 with equal weight has sd 0.5, which
    is the maximum possible for values confined to [0,1]. Dividing by 0.5
    makes the output a readable 0-to-1 dispersion score.
    """
    a = np.asarray(vals, dtype=float)
    ww = np.asarray(w, dtype=float)
    if a.size < 2 or ww.sum() <= 0:
        return 0.0
    ww = ww / ww.sum()
    mu = float((ww * a).sum())
    var = float((ww * (a - mu) ** 2).sum())
    return min(1.0, float(np.sqrt(var)) / 0.5)


def diagnose_world(polities: List[PolityInput], year: int,
                   params: Optional[dict] = None,
                   horizon_years: float = 15.0,
                   sync_risk_prior: Optional[float] = None,
                   router_mode: str = "conserve",
                   with_trajectory: bool = True,
                   with_sensitivity: bool = False,
                   mc_draws: Optional[int] = None,
                   sigma: Optional[Dict[str, float]] = None) -> WorldDiagnosis:
    """Run every polity, then the network and global layers.

    with_sensitivity defaults to False here: the OAT pass re-evaluates the
    whole pipeline ~90 times per polity, which is fine for one country and
    wasteful for ten. Turn it on per polity via diagnose2 when you need it.
    """
    params = dict(params or {})
    if not polities:
        raise ValueError("diagnose_world needs at least one polity")

    diags: Dict[str, Diagnosis2] = {}
    for pi in polities:
        diags[pi.code] = diagnose2(
            pi.name, year, pi.sub, demo=pi.demo, disp=pi.disp,
            state_type=pi.state_type,
            revenue_polarisation=pi.revenue_polarisation,
            security_pressure=pi.security_pressure,
            base_revenue_demand=pi.base_revenue_demand,
            g_shock=pi.g_shock, params=params, events=pi.events or None,
            horizon_years=horizon_years, router_mode=router_mode,
            with_trajectory=with_trajectory,
            with_sensitivity=with_sensitivity,
            sigma=sigma, mc_draws=mc_draws)

    codes = [p.code for p in polities]
    by_code = {p.code: p for p in polities}
    w = np.array([p.weight for p in polities], dtype=float)

    # ---- build sccd network nodes on the EFFECTIVE components -------------
    nodes: List[net1.Node] = []
    for p in polities:
        D = diags[p.code]
        eff = D.forcing.effective
        nodes.append(net1.Node(
            code=p.code, delta_norm=D.capacity.delta_norm, psi=D.capacity.psi,
            cai=D.loops.cai_core,          # core, not ext: keeps Psi_G
                                           # comparable to sccd's own CAI_G_crit
            c1=eff.c1, c4=eff.c4, s1=eff.s1, s4=eff.s4, c3=eff.c3,
            weight=p.weight, opportunity=p.opportunity, ret=p.ret,
            capital_controls=p.capital_controls,
            skilled_supply=p.skilled_supply))

    F = net1.flow_matrix(nodes, net1.network_params())

    # ---- Sync_Risk: historical prior + endogenous haven term --------------
    prior = (sync_risk_prior if sync_risk_prior is not None
             else net1.SYNC_RISK_HISTORY[max(net1.SYNC_RISK_HISTORY)])
    a4 = np.array([by_code[c].disp.a4 for c in codes], dtype=float)
    ww = w / w.sum()
    haven_pressure = float((ww * a4).sum())
    gain = params.get("haven_sync_gain", spec2.WORLD2["haven_sync_gain"].value)
    sync_haven = gain * haven_pressure
    sync_risk = float(min(0.95, prior + sync_haven))

    psi_G = net1.global_coherence(nodes, sync_risk)

    # ---- Thucydides between the two highest-capacity polities ------------
    # Rank by SYSTEMIC WEIGHT first, Delta_norm only as a tie-break. Ranking
    # by Delta_norm alone picks whichever polity happens to post the widest
    # capacity differential, which can be a small state - the engine was
    # pairing China against Japan rather than against the United States. sccd
    # Part IV's hegemonic-transition question is about systemic position.
    order = sorted(codes,
                   key=lambda c: (by_code[c].weight,
                                  diags[c].capacity.delta_norm),
                   reverse=True)
    heg = order[0] if order else None
    chal = order[1] if len(order) > 1 else None
    if heg and chal:
        dh = diags[heg].capacity.delta_norm
        dc = diags[chal].capacity.delta_norm
        # Convergence speed, from each side's own measured dDelta/dt. v1.00
        # required this as a caller argument; the trajectories supply it.
        gh = diags[heg].bifurcation.get("d_delta_dt", 0.0) or 0.0
        gc = diags[chal].bifurcation.get("d_delta_dt", 0.0) or 0.0
        d_gap = gh - gc
        tt = net1.thucydides(dh, dc, d_gap, sustained_years=10.0, p=params)
        tt["hegemon"] = heg
        tt["challenger"] = chal
        tt["d_gap_dt_source_key"] = "tt.gap_source"
    else:
        tt = {"T_trap": 0, "note_key": "tt.needs_two"}

    rbg = net1.global_bifurcation_risk(psi_G, tt.get("T_trap", 0), nodes,
                                       p=params)
    rbg["interpretation_key"] = "rbg.interp"
    rbg.pop("interpretation", None)

    # ---- the two new global aggregates -----------------------------------
    d3 = [by_code[c].demo.d3 for c in codes]
    a1 = [by_code[c].disp.a1 for c in codes]
    adj_div = _weighted_dispersion(d3, w)
    ai_div = _weighted_dispersion(a1, w)

    split: Dict[str, List[str]] = {"VOLUNTARY": [], "VIOLENT_EXPOSED": [],
                                   "MIXED": [], "SLACK": []}
    for c in codes:
        split[diags[c].verdict.adjustment_mode].append(c)

    # Talent gradient: for each ordered pair, the d3 differential that
    # sccd's F^talent channel responds to.
    tg_gain = params.get("divergence_talent_gain",
                         spec2.WORLD2["divergence_talent_gain"].value)
    grad: List[dict] = []
    for a in codes:
        for b in codes:
            if a == b:
                continue
            push = by_code[a].demo.d5          # surplus youth at origin
            pull = by_code[b].demo.d4          # inversion at destination
            if push > 0.45 and pull > 0.45:
                grad.append(dict(origin=a, destination=b,
                                 push_d5=round(push, 3),
                                 pull_d4=round(pull, 3),
                                 pressure=round(tg_gain * push * pull, 4)))
    grad.sort(key=lambda g: -g["pressure"])

    # ---- world verdict, as (key, params) descriptors ---------------------
    crit = params.get("psi_G_crit", s1spec.NETWORK["psi_G_crit"].value)
    cai_crit = params.get("CAI_G_crit", s1spec.NETWORK["CAI_G_crit"].value)
    vparts: List[tuple] = [
        ("wv.psiG", {"psi": f"{psi_G:.3f}", "crit": f"{crit:.2f}",
                     "cmp": "w.below" if psi_G < crit else "w.above"}),
        ("wv.sync", {"sync": f"{sync_risk:.3f}", "prior": f"{prior:.2f}",
                     "haven": f"{sync_haven:.3f}"}),
        ("wv.cai", {"cai": f"{rbg['CAI_weighted']:.2f}",
                    "crit": f"{cai_crit:.2f}"}),
    ]
    if tt.get("T_trap"):
        vparts.append(("wv.trap", {"h": heg, "c": chal}))
    vparts.append(("wv.rbg", {"v": rbg["R_B_G"]}))
    if adj_div > 0.35:
        vparts.append(("wv.divergence",
                       {"d": f"{adj_div:.2f}",
                        "nv": len(split["VOLUNTARY"]),
                        "nx": len(split["VIOLENT_EXPOSED"])}))

    warn: List[tuple] = [("warn.psiG_uncal", {}), ("warn.rbg_structural", {})]
    if len(polities) < 3:
        warn.append(("warn.few_polities", {"n": len(polities)}))
    if sync_risk >= 0.95:
        warn.append(("warn.sync_capped", {}))
    low_conf = [p.code for p in polities if p.confidence == "low"]
    if low_conf:
        warn.append(("warn.low_confidence", {"codes": ", ".join(low_conf)}))

    return WorldDiagnosis(
        year=year,
        polities={c: diags[c].as_dict() for c in codes},
        psi_G=psi_G, psi_G_crit=crit,
        sync_risk=sync_risk, sync_risk_prior=prior,
        sync_risk_haven=sync_haven,
        cai_weighted=rbg["CAI_weighted"],
        thucydides=tt, global_bifurcation=rbg,
        adjustment_divergence=adj_div, adjustment_split=split,
        ai_divergence=ai_div, haven_pressure=haven_pressure,
        talent_gradient=grad[:12],
        flow_matrix=[[round(float(v), 6) for v in row] for row in F],
        flow_codes=codes, hegemon=heg, challenger=chal,
        verdict_parts=vparts, warning_codes=warn)

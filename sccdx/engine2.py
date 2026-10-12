# -*- coding: utf-8 -*-
"""
SCCD-X — Orchestrator v2.00
============================
Single entry point: diagnose2() -> Diagnosis2

Pipeline:

  events -> forcing -> aggregate -> classify -> loops -> dynamics
         -> bifurcation -> sensitivity -> report
  (events) (D + A)    (sccd II)   (band +   (L1-L8)  (10-state)  (eq 23)  (eq SA)
                                   tier +
                                   mode)

TWO THINGS THIS DOES THAT v1.00 COULD NOT
-----------------------------------------
1. dDelta/dt IS COMPUTED, NOT ASKED FOR. sccd's bifurcation test (eq 23)
   needs three conditions, one of which is momentum: dDelta/dt < -delta_c.
   v1.00's `diagnose` takes that as a caller-supplied argument, so the
   analyst has to already know the answer to the most forward-looking part of
   the question. With S1/S2/S4/S5 promoted to states, the trajectory supplies
   it directly. Passing d_delta_dt explicitly still overrides.

2. THE SENSITIVITY PROTOCOL ACTUALLY RUNS ON THE VERDICT. sccd Part IV eq
   (SA) mandates OAT +/-20% on threshold parameters. The engine runs it
   against the QUALITATIVE VERDICT - regime band, coherence tier, loop set,
   R_B - and reports which parameters flip it. This is not decoration. The
   worked US case shows the whole theta25 collapse resting on one ANALYST
   coefficient (compress_s5); a reader who cannot see that is being misled,
   and `fragility` is where it shows up.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple

import numpy as np

from sccd import spec as s1spec
from sccd import loops as l1
from sccd.aggregate import SubComponents, Capacity, compute, classify_regime
from sccd.normalize import propagate, UncertainDelta
from . import spec2
from .forcing import (DemoBlock, DispBlock, Forcing, apply_forcing,
                      coherence_tier)
from .loops2 import LoopDiagnosis2, diagnose_loops2
from .dynamics2 import Context2, Trajectory2, simulate2
from .events import EventInput, apply_events, EventApplication


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------
@dataclass
class Verdict:
    """The qualitative triple plus the risk flags. This is the answer."""
    regime: str                 # sccd Part II Table 2 band (enum name)
    stability: str              # enum name
    coherence_tier: str         # new second axis (enum name)
    adjustment_mode: str        # new third axis (enum name)
    gate_code: str              # language-free gate verdict
    gate_years: Optional[float]
    R_B: int
    cai_core: float
    cai_ext: float
    active_loops: List[str]
    decoupling_active: bool
    headline_parts: List[tuple]   # [(i18n key, params), ...]

    def signature(self) -> tuple:
        """The tuple the sensitivity pass checks for flips."""
        return (self.regime, self.coherence_tier, self.adjustment_mode,
                self.R_B, tuple(self.active_loops))

    def as_dict(self) -> dict:
        d = asdict(self)
        d["headline_parts"] = [list(x) for x in self.headline_parts]
        return d


@dataclass
class Fragility:
    """One OAT perturbation result."""
    parameter: str
    status: str
    baseline: float
    low: float
    high: float
    flips_low: bool
    flips_high: bool
    changed: List[dict]        # [{field, from, to, side}] - enum names only

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Diagnosis2:
    country: str
    year: int
    state_type: str
    verdict: Verdict
    capacity: Capacity              # on effective components
    capacity_base: Capacity         # before forcing, for comparison
    forcing: Forcing
    loops: LoopDiagnosis2
    bifurcation: dict
    attractor: dict
    trajectory: Optional[Trajectory2]
    horizon_verdict: Optional[Verdict]
    uncertainty: Optional[UncertainDelta]
    fragility: List[Fragility]
    events: Optional[EventApplication]
    calibration: dict
    warning_codes: List[tuple] = field(default_factory=list)

    def as_dict(self, traj_stride: int = 6) -> dict:
        return {
            "country": self.country, "year": self.year,
            "state_type": self.state_type,
            "verdict": self.verdict.as_dict(),
            "capacity": self.capacity.as_dict(),
            "capacity_base": self.capacity_base.as_dict(),
            "forcing": self.forcing.as_dict(),
            "loops": self.loops.as_dict(),
            "bifurcation": self.bifurcation,
            "attractor": self.attractor,
            "trajectory": (self.trajectory.as_dict(stride=traj_stride)
                           if self.trajectory else None),
            "horizon_verdict": (self.horizon_verdict.as_dict()
                                if self.horizon_verdict else None),
            "uncertainty": (asdict(self.uncertainty) if self.uncertainty
                            else None),
            "fragility": [f.as_dict() for f in self.fragility],
            "events": self.events.as_dict() if self.events else None,
            "calibration": self.calibration,
            "warning_codes": [list(c) for c in self.warning_codes],
        }


# ---------------------------------------------------------------------------
# Verdict assembly
# ---------------------------------------------------------------------------
def _build_verdict(cap: Capacity, F: Forcing, L: LoopDiagnosis2,
                   rb: dict) -> Verdict:
    tier, _ = coherence_tier(cap.psi)
    mode = F.demo.adjustment_mode

    # The headline is assembled as (key, params) descriptors, not as a
    # sentence. The localiser turns it into one in whichever language was
    # asked for; the engine itself never commits to a language.
    parts: List[tuple] = [("hl.band_tier",
                           {"regime": f"regime.{cap.regime}",
                            "tier": f"tier.{tier}"})]
    if mode != "SLACK":
        parts.append(("hl.mode", {"mode": f"mode.{mode}"}))
    if F.gate_code not in ("OPEN", "OPEN_NEAREST"):
        # Nested-with-params form: the gate template needs its year count.
        parts.append(("hl.gate",
                      {"gate": {"__key": f"tg.{F.gate_code}",
                                "y": f"{(F.gate_years or 0):.0f}"}}))
    if L.active:
        parts.append(("hl.loops", {"loops": "+".join(L.active)}))
    if rb["R_B"] == 1:
        parts.append(("hl.rb", {}))
    if F.disp.decoupling_active:
        parts.append(("hl.decoupled", {}))

    return Verdict(
        regime=cap.regime, stability=cap.stability, coherence_tier=tier,
        adjustment_mode=mode, gate_code=F.gate_code,
        gate_years=F.gate_years, R_B=rb["R_B"],
        cai_core=L.cai_core, cai_ext=L.cai_ext,
        active_loops=list(L.active),
        decoupling_active=F.disp.decoupling_active, headline_parts=parts)


# ---------------------------------------------------------------------------
# Core evaluation, factored out so the sensitivity pass can re-run it cheaply
# ---------------------------------------------------------------------------
def _evaluate(sub: SubComponents, dm: DemoBlock, ap: DispBlock,
              state_type: str, params: dict,
              revenue_polarisation: float, security_pressure: float,
              base_revenue_demand: float, router_mode: str,
              haven_single_channel: bool,
              d_delta_dt: Optional[float],
              g_shock: float,
              horizon: float,
              with_trajectory: bool) -> Tuple[Verdict, dict, Forcing,
                                              LoopDiagnosis2, Capacity,
                                              Optional[Trajectory2], dict]:
    F = apply_forcing(sub, dm, ap, p=params, router_mode=router_mode,
                      haven_single_channel=haven_single_channel,
                      security_pressure=security_pressure,
                      base_revenue_demand=base_revenue_demand)
    cap = compute(F.effective, state_type=state_type, params=params)
    L = diagnose_loops2(F, dm, ap, revenue_polarisation=revenue_polarisation,
                        p=params)

    traj: Optional[Trajectory2] = None
    ddt = d_delta_dt
    if with_trajectory or ddt is None:
        ctx = Context2(c2=F.effective.c2, c3=F.effective.c3,
                       c4=F.effective.c4, dm=dm, ap=ap,
                       revenue_polarisation=revenue_polarisation,
                       security_pressure=security_pressure,
                       base_revenue_demand=base_revenue_demand,
                       router_mode=router_mode,
                       haven_single_channel=haven_single_channel)
        traj = simulate2(F.effective, ctx, years=horizon, params=params,
                         state_type=state_type, g_multiplier=F.g_multiplier)
        if ddt is None:
            # Momentum for sccd eq (23), measured over the first three years
            # of the trajectory rather than demanded from the caller. Three
            # years because eq (23)'s delta_c is specified per year and a
            # one-step slope would just read integrator noise.
            w = traj.t <= traj.t[0] + 3.0
            if w.sum() >= 2:
                ddt = float((traj.delta_norm[w][-1] - traj.delta_norm[w][0])
                            / (traj.t[w][-1] - traj.t[w][0]))
            else:
                ddt = 0.0

    rb = l1.bifurcation_risk(cap.delta_norm, ddt, cap.psi, p=params)
    rb["d_delta_dt"] = ddt
    rb["d_delta_dt_source_key"] = ("ddt.caller" if d_delta_dt is not None
                                   else "ddt.measured")
    att = l1.attractor(F.effective, g_shock, p=params)
    verdict = _build_verdict(cap, F, L, rb)
    return verdict, rb, F, L, cap, traj, att


# ---------------------------------------------------------------------------
# Sensitivity - sccd Part IV eq (SA), OAT +/-20%
# ---------------------------------------------------------------------------
# Which parameters to perturb. The protocol says "threshold parameters"; the
# engine reads that as every parameter the verdict can plausibly hinge on,
# which means all of Block D and Block A (since all of them are ANALYST) plus
# the sccd FREE parameters that enter the C denominator and the loop tests.
_OAT_SCCD_FREE = ("phi", "psi", "alpha_exit", "epsilon",
                  "L3_c5_thresh", "L3_revpol_thresh",
                  "L4_c4_thresh", "L4_c1_thresh")


def _oat_targets() -> List[Tuple[str, float, str]]:
    out: List[Tuple[str, float, str]] = []
    for name, P in spec2.DEMO.items():
        out.append((name, P.value, P.status))
    for name, P in spec2.DISP.items():
        out.append((name, P.value, P.status))
    for name in _OAT_SCCD_FREE:
        for grp in (s1spec.FRAGMENTATION, s1spec.THETA, s1spec.LOOPS):
            if name in grp:
                out.append((name, grp[name].value, grp[name].status))
                break
    return out


def _sensitivity(baseline: Verdict, run, variation: float) -> List[Fragility]:
    """Perturb each target +/-variation and record verdict flips."""
    base_sig = baseline.signature()
    fields = ("regime", "coherence_tier", "adjustment_mode", "R_B",
              "active_loops")
    out: List[Fragility] = []

    for name, val, status in _oat_targets():
        lo, hi = val * (1.0 - variation), val * (1.0 + variation)
        changed: List[str] = []
        flips = {}
        for tag, v in (("low", lo), ("high", hi)):
            try:
                vd = run({name: v})
            except Exception:
                flips[tag] = False
                continue
            flips[tag] = vd.signature() != base_sig
            if flips[tag]:
                for f in fields:
                    if getattr(vd, f) != getattr(baseline, f):
                        changed.append({"field": f,
                                        "from": getattr(baseline, f),
                                        "to": getattr(vd, f),
                                        "side": tag})
        if flips.get("low") or flips.get("high"):
            out.append(Fragility(parameter=name, status=status, baseline=val,
                                 low=lo, high=hi,
                                 flips_low=bool(flips.get("low")),
                                 flips_high=bool(flips.get("high")),
                                 changed=changed))
    return out


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def diagnose2(country: str, year: int, sub: SubComponents,
              demo: Optional[DemoBlock] = None,
              disp: Optional[DispBlock] = None,
              state_type: str = "liberal_democracy",
              revenue_polarisation: float = 0.0,
              security_pressure: float = 0.0,
              base_revenue_demand: float = 0.0,
              d_delta_dt: Optional[float] = None,
              g_shock: float = 0.0,
              params: Optional[dict] = None,
              sigma: Optional[Dict[str, float]] = None,
              mc_draws: Optional[int] = None,
              events: Optional[List[EventInput]] = None,
              horizon_years: float = 15.0,
              router_mode: str = "conserve",
              haven_single_channel: bool = False,
              with_trajectory: bool = True,
              with_sensitivity: bool = True) -> Diagnosis2:
    """Full single-polity diagnosis.

    `events` are applied to the sub-components and the two blocks BEFORE
    anything else, so the whole pipeline downstream sees the post-event state.
    """
    dm = demo or DemoBlock()
    ap = disp or DispBlock()
    params = dict(params or {})

    # ---- events first -----------------------------------------------------
    ev: Optional[EventApplication] = None
    if events:
        ev = apply_events(sub, dm, ap, events)
        sub, dm, ap = ev.sub, ev.demo, ev.disp
        revenue_polarisation = min(1.0, revenue_polarisation
                                   + ev.extra.get("revenue_polarisation", 0.0))
        security_pressure = min(1.0, security_pressure
                                + ev.extra.get("security_pressure", 0.0))
        base_revenue_demand += ev.extra.get("base_revenue_demand", 0.0)
        g_shock += ev.extra.get("g_shock", 0.0)

    common = dict(state_type=state_type,
                  revenue_polarisation=revenue_polarisation,
                  security_pressure=security_pressure,
                  base_revenue_demand=base_revenue_demand,
                  router_mode=router_mode,
                  haven_single_channel=haven_single_channel,
                  d_delta_dt=d_delta_dt, g_shock=g_shock,
                  horizon=horizon_years)

    verdict, rb, F, L, cap, traj, att = _evaluate(
        sub, dm, ap, params=params, with_trajectory=with_trajectory, **common)
    cap_base = compute(sub, state_type=state_type, params=params)

    # ---- verdict at the horizon ------------------------------------------
    hv: Optional[Verdict] = None
    if traj is not None:
        i = -1
        end = SubComponents(
            s1=float(traj.s1[i]), s2=float(traj.s2[i]), s3=float(traj.s3[i]),
            s4=float(traj.s4[i]), s5=float(traj.s5[i]), c1=float(traj.c1[i]),
            c2=F.effective.c2, c3=F.effective.c3, c4=F.effective.c4,
            c5=float(traj.c5[i]))
        dm_end = DemoBlock(d1=dm.d1, d2=dm.d2, d3=dm.d3,
                           d4=float(traj.d4[i]), d5=dm.d5)
        # Re-run the classification on the horizon state. Note this reuses the
        # same Block A inputs - see the Context2 constancy caveat.
        hv, _, _, _, _, _, _ = _evaluate(
            end, dm_end, ap, params=params, with_trajectory=False,
            **{**common, "d_delta_dt": 0.0})

    # ---- Monte Carlo on measurement error --------------------------------
    unc: Optional[UncertainDelta] = None
    if sigma:
        unc = propagate(F.effective, sigma, state_type=state_type,
                        params=params, draws=mc_draws)

    # ---- OAT sensitivity on the verdict ----------------------------------
    frag: List[Fragility] = []
    if with_sensitivity:
        var = s1spec.SENSITIVITY["oat_variation"].value   # 0.20, PAPER
        def run(override: dict) -> Verdict:
            pp = dict(params); pp.update(override)
            v, *_ = _evaluate(sub, dm, ap, params=pp,
                              with_trajectory=False,
                              **{**common, "d_delta_dt": rb["d_delta_dt"]})
            return v
        frag = _sensitivity(verdict, run, var)

    # ---- warnings, as codes ---------------------------------------------
    warn: List[tuple] = list(F.note_codes) + list(L.overlap_codes)
    warn.append(("warn.calib_tags", {}))
    if frag:
        names = ", ".join(f.parameter for f in frag[:6])
        warn.append(("warn.oat_flips",
                     {"n": len(frag), "names": names,
                      "more": " ..." if len(frag) > 6 else ""}))
    else:
        warn.append(("warn.oat_none", {}))
    if sub.s3 < 0.45:
        warn.append(("warn.s3_low", {}))
    if cap.psi > 0.40 and cap.delta_norm < -0.08:
        warn.append(("warn.psi_high_delta_crisis", {}))
    if ev is not None:
        warn.extend(ev.note_codes)

    calib = {
        "spec_version": s1spec.SPEC_VERSION,
        "spec2_version": spec2.SPEC2_VERSION,
        "audit": spec2.combined_audit(),
        "open_problems_v2": spec2.OPEN_PROBLEMS_V2,
        "known_inconsistencies_v1": s1spec.KNOWN_INCONSISTENCIES,
        "patch_defaults": {"sccd_patch": True, "c1_dynamic": True,
                           "rationale_key": "patch.rationale"},
        "epistemic_limit_key": "epistemic.limit",
    }

    return Diagnosis2(
        country=country, year=year, state_type=state_type,
        verdict=verdict, capacity=cap, capacity_base=cap_base,
        forcing=F, loops=L, bifurcation=rb, attractor=att,
        trajectory=traj, horizon_verdict=hv, uncertainty=unc,
        fragility=frag, events=ev, calibration=calib, warning_codes=warn)

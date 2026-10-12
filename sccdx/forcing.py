# -*- coding: utf-8 -*-
"""
SCCD-X — Forcing Layer
=======================
Converts the Block D (demographic) and Block A (displacement/AI) inputs into:

  1. LEVEL SHIFTS on C1, C2, C4   - channels sccd's proxies structurally miss
  2. DRIFT RATES on S1..S5 and C5 - including values for sccd's exogenous
                                    S3_natural and C5_structural, which
                                    v1.00 left blank
  3. TIME-TO-GATE projections      - linear extrapolation of those drifts
                                     against sccd's PAPER thresholds
  4. DIAGNOSTIC FLAGS              - the structural readings that only exist
                                     because these two blocks were added

See spec2's LEVEL vs DRIFT section for why the split is not arbitrary: giving
an S component a level shift double counts whatever its annual-flow proxy
already embeds. That bug is easy to write and hard to see, so the rule is
enforced here structurally - demo_forcing and disp_forcing return `levels`
and `drifts` as separate dicts, and apply_forcing refuses a level on an
S component.

This is the only module where the new papers touch the old engine. Everything
downstream is sccd v1.00 arithmetic operating on what comes out of here.
Keeping the seam this narrow is deliberate: any v2 result can be reproduced
by running v1.00 on the effective components this module prints.

SIGN CONVENTIONS
----------------
Drifts are per-year rates, positive = the variable rises.
Levels are shifts in normalised [0,1] units.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple

from sccd import spec as s1spec
from sccd.aggregate import SubComponents, legitimacy_multiplier
from . import spec2


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else (hi if x > hi else x)


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
@dataclass
class DemoBlock:
    """Block D inputs, each normalised to [0,1]. See spec2.DEMO_COMPONENTS."""
    d1: float = 0.50   # carrying-capacity load
    d2: float = 0.50   # expectation trap
    d3: float = 0.50   # adjustment autonomy  (THE ROUTER)
    d4: float = 0.40   # dependency inversion
    d5: float = 0.35   # surplus youth cohort

    def validate(self) -> None:
        for k, v in asdict(self).items():
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"DemoBlock.{k}={v} outside [0,1]")

    def as_dict(self) -> Dict[str, float]:
        return asdict(self)


@dataclass
class DispBlock:
    """Block A inputs, each normalised to [0,1]. See spec2.DISP_COMPONENTS."""
    a1: float = 0.50   # AI penetration
    a2: float = 0.40   # self-efficacy erosion   (Tier 1)
    a3: float = 0.35   # agency erosion          (Tier 2)
    a4: float = 0.40   # haven reallocation
    a5: float = 0.20   # counter-tech mobilisation
    a6: float = 0.40   # AI productivity windfall
    physical_share: Optional[float] = None   # physical vs paper split of a4
    luxury_contraction: float = 0.0          # observed luxury demand contraction

    def validate(self) -> None:
        d = asdict(self)
        d.pop("physical_share")
        for k, v in d.items():
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"DispBlock.{k}={v} outside [0,1]")
        if self.physical_share is not None and not (0.0 <= self.physical_share <= 1.0):
            raise ValueError("DispBlock.physical_share outside [0,1]")

    def as_dict(self) -> Dict[str, float]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------
@dataclass
class DemoForcing:
    load_effective: float
    pressure_total: float
    pressure_violent: float
    pressure_voluntary: float
    router_mode: str
    adjustment_mode: str
    drifts: Dict[str, float] = field(default_factory=dict)
    levels: Dict[str, float] = field(default_factory=dict)
    note_codes: List[tuple] = field(default_factory=list)

    def as_dict(self) -> dict:
        d = asdict(self)
        d["note_codes"] = [list(c) for c in self.note_codes]
        return d


@dataclass
class DispForcing:
    anxiety: float
    g_multiplier: float
    tau_demanded: float
    tau_feasible: float
    extraction_squeeze: float
    physical_share: float
    decoupling_active: bool
    decoupling_index: float
    drifts: Dict[str, float] = field(default_factory=dict)
    levels: Dict[str, float] = field(default_factory=dict)
    note_codes: List[tuple] = field(default_factory=list)

    def as_dict(self) -> dict:
        d = asdict(self)
        d["note_codes"] = [list(c) for c in self.note_codes]
        return d


@dataclass
class GateProjection:
    """Linear extrapolation of one component's drift against a threshold."""
    component: str
    level: float
    drift: float
    threshold: float
    threshold_status: str      # PAPER / FREE / ANALYST
    margin: float
    years_to_gate: Optional[float]
    crossed: bool
    meaning_key: str          # i18n key; prose is added by the localiser

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Forcing:
    base: SubComponents
    effective: SubComponents          # base + LEVEL shifts only
    demo: DemoForcing
    disp: DispForcing
    drifts: Dict[str, float]
    levels: Dict[str, float]
    s3_natural: float                 # -> sccd.dynamics.Context.s3_natural
    c5_structural: float              # -> sccd.dynamics.Context.c5_structural
    d4_drift: float
    g_multiplier: float
    gates: List[GateProjection]
    gate_code: str                 # S5_GATE_NEAR, OPEN, ... (language-free)
    gate_years: Optional[float]    # years to the nearest gate, if approaching
    clamped: List[str]
    note_codes: List[tuple] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "base": self.base.as_dict(),
            "effective": self.effective.as_dict(),
            "demo": self.demo.as_dict(),
            "disp": self.disp.as_dict(),
            "drifts": self.drifts,
            "levels": self.levels,
            "s3_natural": self.s3_natural,
            "c5_structural": self.c5_structural,
            "d4_drift": self.d4_drift,
            "g_multiplier": self.g_multiplier,
            "gates": [g.as_dict() for g in self.gates],
            "gate_code": self.gate_code,
            "gate_years": self.gate_years,
            "clamped": self.clamped,
            "note_codes": [list(c) for c in self.note_codes],
        }


# ===========================================================================
#  BLOCK D
# ===========================================================================
def demo_forcing(dm: DemoBlock, sc: SubComponents,
                 p: Optional[dict] = None,
                 router_mode: str = "conserve") -> DemoForcing:
    """The demographic pressure router.

    STEP 1 - effective load. Degrow's argument is that the modern binding
    constraint is not food but the cost of household formation, and that this
    constraint only EXISTS in a high-expectation society. So the expectation
    trap enters multiplied by adjustment autonomy, which is the engine's proxy
    for 'modern high-expectation environment'. The sum is normalised by its
    own maximum weight so that load stays a genuine [0,1] quantity instead of
    saturating at the ceiling for every rich country:

        L_eff = (d1 + kappa_exp * d2 * d3) / (1 + kappa_exp)

    STEP 2 - the router. Total pressure is split by the availability of
    voluntary instruments:

        violent_share = (1 - d3)^route_sharpness
        P_violent     = P * violent_share
        P_voluntary   = P * (1 - violent_share)

    router_mode='conserve' (default) keeps P fixed and only redirects it,
    which is the strict reading of 'different manifestations of the same
    fundamental law'. router_mode='discount' additionally shrinks P itself,
    on the argument that prevention is cheaper than clearance. The paper does
    not settle this (spec2 OP2-1), so it is a dial, not a hidden assumption.

    STEP 3 - the two channels discharge into DIFFERENT sccd variables, and
    that asymmetry is the whole point.
        violent   -> C5 up, S2 down, S4 down, S3 down
        voluntary -> d4 up, then S5 down, S1 down, S3 down
    All of these are DRIFTS. Block D produces no level shifts at all: every
    variable it touches is on the S side or is C5, and sccd measures all of
    them as annual flows that already embed today's demography.
    """
    p = p or {}
    g = lambda k: p.get(k, spec2.DEMO[k].value)
    dm.validate()

    kappa = g("kappa_exp")
    sharp = g("route_sharpness")

    load = _clamp((dm.d1 + kappa * dm.d2 * dm.d3) / (1.0 + kappa))
    P = load
    codes: List[tuple] = []
    if router_mode == "discount":
        P = load * (1.0 - 0.30 * dm.d3)
        codes.append(("note.router_discount", {}))
    elif router_mode != "conserve":
        raise ValueError("router_mode must be 'conserve' or 'discount'")

    violent_share = (1.0 - dm.d3) ** sharp
    P_v = P * violent_share
    P_q = P * (1.0 - violent_share)

    drifts = {
        # violent channel - the ancient path
        "c5": g("nu_youth_frag") * P_v * dm.d5,
        "s2": -g("erode_s2") * P_v * dm.d5,
        "s4": -g("erode_s4_corrupt") * P_v,
        # voluntary channel - the modern path
        "d4": g("iota_inversion") * P_q,
        "s5": -g("compress_s5") * dm.d4,
        "s1": -g("compress_s1") * dm.d4,
        # S3 is drained by BOTH channels, through different mechanisms:
        #   violent   = relief failure, the broken mandate of heaven
        #   voluntary = the expectation trap, a legitimacy drain that needs
        #               no economic downturn at all
        "s3": (-g("sigma_relief") * P_v * (1.0 - dm.d3)
               - g("sigma_expect") * dm.d2 * dm.d3),
    }

    # --- adjustment mode overlay ---
    d3_t, d5_t = g("d3_voluntary_thresh"), g("d5_violent_thresh")
    if P < 0.25:
        mode = "SLACK"
    elif dm.d3 >= d3_t and dm.d5 < d5_t:
        mode = "VOLUNTARY"
    elif dm.d3 < d3_t and dm.d5 >= d5_t:
        mode = "VIOLENT_EXPOSED"
    else:
        mode = "MIXED"

    return DemoForcing(
        load_effective=load, pressure_total=P,
        pressure_violent=P_v, pressure_voluntary=P_q,
        router_mode=router_mode, adjustment_mode=mode,
        drifts=drifts, levels={}, note_codes=codes,
    )


# ===========================================================================
#  BLOCK A
# ===========================================================================
def disp_forcing(ap: DispBlock, sc: SubComponents,
                 p: Optional[dict] = None,
                 d4: float = 0.0,
                 security_pressure: float = 0.0,
                 base_revenue_demand: float = 0.0,
                 haven_single_channel: bool = False) -> DispForcing:
    """The displacement forcing block.

    THE TWO RESULTS THAT MATTER, both absent from sccd v1.00:

    (1) G/S3 DECOUPLING. g_multiplier > 1 while the S3 drift is negative.
        Every other windfall in the source paper raised legitimacy alongside
        output - Part V's 1941-45 build-up is the type case. This one does
        not, because what it erodes is authorship. The engine flags the
        condition explicitly rather than letting it hide inside a trajectory.

    (2) EXTRACTION SQUEEZE. tau_feasible reuses sccd's own re-extraction rate
        from Part II eq (17) - tau_max * S1 * (1 - C4) * lam/lam_max -
        evaluated on the EFFECTIVE C4 after haven flight. tau_demanded is
        what the fiscal programme needs: baseline, plus pension pre-commitment
        (Block D's d4), plus security. The gap is the quantity Degrow
        describes as milking an emaciated cow, and it drives loop L6.

    Level shifts here are confined to C1, C2 and C4 - the three components
    whose sccd proxies structurally omit these channels.
    """
    p = p or {}
    g = lambda k: p.get(k, spec2.DISP[k].value)
    ap.validate()

    phys = (ap.physical_share if ap.physical_share is not None
            else g("physical_share_default"))

    # --- two-tier anxiety architecture (DISPL 4.4.4) ---
    anxiety = _clamp(g("tier_w1") * ap.a2 + g("tier_w2") * ap.a3
                     + g("tier_w_cross") * ap.a2 * ap.a3)

    # --- LEVEL shifts: the three sccd blind spots ---
    levels = {
        # Chinn-Ito + OECD DIOC measure exit by JURISDICTION and contain no
        # term for exit by ASSET FORM. Gold in a domestic vault is invisible
        # to every proxy sccd Part III lists for C4.
        "c4": g("zeta_haven_c4") * ap.a4,
        # V-Dem associational density lags a counter-technological revival.
        "c2": g("zeta_ctr_c2") * ap.a5,
        # WID wealth shares lag the UHNW/aspirational divergence the paper
        # documents in its own segment data.
        "c1": g("zeta_uhnw_c1") * anxiety * (1.0 - ap.a5),
    }

    # --- DRIFTS ---
    drifts = {
        "s3": -g("sigma_agency") * ap.a3 * ap.a1,
        "c5": (g("nu_narrative") * ap.a3 * ap.a1
               - g("nu_counter") * ap.a5 * sc.c2),
        "s1": -g("zeta_lux_s1") * ap.luxury_contraction,
    }
    codes: List[tuple] = []
    if haven_single_channel:
        codes.append(("note.haven_single", {}))
    else:
        drifts["s1"] -= g("zeta_base_s1") * ap.a4 * phys

    g_mult = 1.0 + g("g_ai") * ap.a6

    # --- (2) the extraction squeeze ---
    c4_eff = _clamp(sc.c4 + levels["c4"])
    lam = legitimacy_multiplier(sc.s3,
                                lambda_min=p.get("lambda_min"),
                                lambda_max=p.get("lambda_max"),
                                k=p.get("k"), s3_mid=p.get("s3_mid"))
    lam_max = p.get("lambda_max", s1spec.LAMBDA["lambda_max"].value)
    tau_max = p.get("tau_max", s1spec.DYNAMICS["tau_max"].value)

    tau_feasible = tau_max * sc.s1 * (1.0 - c4_eff) * (lam / lam_max)
    tau_demanded = (base_revenue_demand
                    + 0.5 * tau_max * d4
                    + 0.3 * tau_max * security_pressure)
    squeeze = tau_demanded - tau_feasible

    # --- (1) decoupling flag ---
    # Require a material magnitude on BOTH legs. Without a floor the flag
    # fires on any trace windfall paired with any trace drift, which makes it
    # true almost everywhere and therefore says nothing.
    decoup = (g_mult - 1.0) >= 0.05 and drifts["s3"] <= -0.005
    decoup_idx = max(g_mult - 1.0, 0.0) * abs(min(drifts["s3"], 0.0)) * 100.0
    if decoup:
        codes.append(("note.decoupling",
                      {"g": f"{g_mult:.3f}", "drift": f"{drifts['s3']:+.4f}"}))

    return DispForcing(
        anxiety=anxiety, g_multiplier=g_mult,
        tau_demanded=tau_demanded, tau_feasible=tau_feasible,
        extraction_squeeze=squeeze, physical_share=phys,
        decoupling_active=decoup, decoupling_index=decoup_idx,
        drifts=drifts, levels=levels, note_codes=codes,
    )


# ===========================================================================
#  GATE PROJECTIONS - the Wheel of Fate written in sccd's own thresholds
# ===========================================================================
#   voluntary/aging path  -> closes the S5 gate (crit 0.15, PAPER)
#   violent/youth path    -> closes the S2 gate (crit 0.25, PAPER)
# Both send theta25 -> 0, which sends Psi = lam*theta25*(1-C5) -> 0 and so
# trips R_B's third condition. Same terminus, two doors.
_GATES = [
    ("s5", "s5_crit", "PAPER", "gate.s5"),
    ("s2", "s2_crit", "PAPER", "gate.s2"),
]


def gate_projections(
        sc_eff: SubComponents, drifts: Dict[str, float],
        p: Optional[dict] = None
) -> Tuple[List[GateProjection], str, Optional[float]]:
    """Linear time-to-threshold for each gated component, plus a verdict.

    Linear extrapolation is the right tool here and not a shortcut: the drifts
    this module produces are themselves constants over the projection, so a
    higher-order method would add precision the inputs do not have. What the
    number is for is ordering - which gate closes first, and roughly how far
    away it is. Treat 'years' as a magnitude, not a date.
    """
    p = p or {}
    out: List[GateProjection] = []

    for comp, crit_key, status, meaning_key in _GATES:
        thr = p.get(crit_key, s1spec.THETA[crit_key].value)
        lvl = getattr(sc_eff, comp)
        dr = drifts.get(comp, 0.0)
        margin = lvl - thr
        crossed = margin <= 0.0
        yrs: Optional[float] = None
        if crossed:
            yrs = 0.0
        elif dr < -1e-9:
            yrs = margin / (-dr)
        out.append(GateProjection(
            component=comp, level=lvl, drift=dr, threshold=thr,
            threshold_status=status, margin=margin,
            years_to_gate=yrs, crossed=crossed,
            meaning_key=meaning_key))

    # S3 against sccd's L2 explosive threshold (PAPER, 0.30)
    s3_thr = p.get("L2_s3_thresh", s1spec.LOOPS["L2_s3_thresh"].value)
    s3_dr = drifts.get("s3", 0.0)
    s3_margin = sc_eff.s3 - s3_thr
    s3_yrs = 0.0 if s3_margin <= 0 else (
        s3_margin / (-s3_dr) if s3_dr < -1e-9 else None)
    out.append(GateProjection(
        component="s3", level=sc_eff.s3, drift=s3_dr, threshold=s3_thr,
        threshold_status="PAPER", margin=s3_margin, years_to_gate=s3_yrs,
        crossed=s3_margin <= 0, meaning_key="gate.s3"))

    # C5 rises, so its gate is an upper bound. sccd's L3 threshold is FREE.
    c5_thr = p.get("L3_c5_thresh", s1spec.LOOPS["L3_c5_thresh"].value)
    c5_dr = drifts.get("c5", 0.0)
    c5_margin = c5_thr - sc_eff.c5
    c5_yrs = 0.0 if c5_margin <= 0 else (
        c5_margin / c5_dr if c5_dr > 1e-9 else None)
    out.append(GateProjection(
        component="c5", level=sc_eff.c5, drift=c5_dr, threshold=c5_thr,
        threshold_status="FREE", margin=c5_margin, years_to_gate=c5_yrs,
        crossed=c5_margin <= 0, meaning_key="gate.c5"))

    # verdict — a language-free CODE plus the years, so the caller can
    # render it in any language and validate2 can assert on it directly.
    closed = [g for g in out if g.crossed and g.component in ("s5", "s2")]
    years: Optional[float] = None
    if len(closed) == 2:
        code = "BOTH_GATES_CLOSED"
    elif closed:
        code = ("S5_GATE_CLOSED" if closed[0].component == "s5"
                else "S2_GATE_CLOSED")
        years = 0.0
    else:
        pend = [g for g in out if g.component in ("s5", "s2")
                and g.years_to_gate is not None]
        if pend:
            soonest = min(pend, key=lambda g: g.years_to_gate)
            years = soonest.years_to_gate
            tag = soonest.component.upper()
            # Tiered, not binary. A single "closing within the horizon" test
            # fires for every aging polity at once and so distinguishes
            # nothing; NEAR is what belongs in a headline.
            if years <= 5.0:
                code = f"{tag}_GATE_NEAR"
            elif years <= 15.0:
                code = f"{tag}_GATE_CLOSING"
            else:
                code = "OPEN_NEAREST"
        else:
            code = "OPEN"
    return out, code, years


# ===========================================================================
#  COMBINE
# ===========================================================================
def apply_forcing(sc: SubComponents,
                  dm: Optional[DemoBlock] = None,
                  ap: Optional[DispBlock] = None,
                  p: Optional[dict] = None,
                  router_mode: str = "conserve",
                  haven_single_channel: bool = False,
                  security_pressure: float = 0.0,
                  base_revenue_demand: float = 0.0) -> Forcing:
    """Run both blocks, fold their LEVEL shifts into effective sub-components,
    and keep their DRIFTS separate for the dynamics layer and the gate
    projections.

    `.effective` is a plain sccd.SubComponents - from that point on the engine
    is v1.00 arithmetic. `.clamped` names any component that hit the [0,1]
    boundary, because a clamped component means the forcing layer wanted to
    push past what the normalisation scale can represent, and the resulting
    level is a boundary artefact rather than a measurement.
    """
    dm = dm or DemoBlock()
    ap = ap or DispBlock()

    D = demo_forcing(dm, sc, p=p, router_mode=router_mode)
    A = disp_forcing(ap, sc, p=p, d4=dm.d4,
                     security_pressure=security_pressure,
                     base_revenue_demand=base_revenue_demand,
                     haven_single_channel=haven_single_channel)

    levels: Dict[str, float] = {}
    for src in (D.levels, A.levels):
        for k, v in src.items():
            if k not in spec2.LEVEL_TARGETS:
                raise AssertionError(
                    f"forcing block returned a LEVEL shift on {k!r}, but only "
                    f"{spec2.LEVEL_TARGETS} may take level shifts. An S-side "
                    f"level shift double counts what the annual-flow proxy "
                    f"already embeds - see spec2 LEVEL vs DRIFT.")
            levels[k] = levels.get(k, 0.0) + v

    drifts: Dict[str, float] = {}
    for src in (D.drifts, A.drifts):
        for k, v in src.items():
            drifts[k] = drifts.get(k, 0.0) + v

    raw = sc.as_dict()
    clamped: List[str] = []
    out: Dict[str, float] = {}
    for k, v in raw.items():
        nv = v + levels.get(k, 0.0)
        if nv < 0.0 or nv > 1.0:
            clamped.append(k)
        out[k] = _clamp(nv)
    eff = SubComponents(**out)

    gates, gate_code, gate_years = gate_projections(eff, drifts, p=p)

    codes: List[tuple] = list(D.note_codes) + list(A.note_codes)
    if gate_code not in ("OPEN", "OPEN_NEAREST"):
        codes.append(("theta25.gate_note", {}))
    if clamped:
        codes.append(("note.clamped", {"names": ", ".join(clamped)}))

    return Forcing(
        base=sc, effective=eff, demo=D, disp=A,
        drifts=drifts, levels=levels,
        s3_natural=drifts.get("s3", 0.0),
        c5_structural=drifts.get("c5", 0.0),
        d4_drift=drifts.get("d4", 0.0),
        g_multiplier=A.g_multiplier,
        gates=gates, gate_code=gate_code, gate_years=gate_years,
        clamped=clamped, note_codes=codes,
    )


# ---------------------------------------------------------------------------
# Coherence tier - the second regime axis
# ---------------------------------------------------------------------------
def coherence_tier(psi: float) -> Tuple[str, str]:
    """Classify Psi against sccd's PAPER Psi_crit plus one ANALYST inner cut."""
    for name, lo, hi in spec2.COHERENCE_TIERS:
        if lo < psi <= hi:
            return name, spec2.COHERENCE_TIER_SRC
    return "Incoherent", spec2.COHERENCE_TIER_SRC

"""
SCCD Engine — Feedback Loop Diagnostics (Part IV §2, eq. CAI)
==============================================================
Loops L1-L4 with their activation thresholds, cross-coupling map, and the
Compound Acceleration Index.

This is the analogue of the Lục Hào "Cục" layer: a set of named configurations
that, once triggered, override the baseline reading.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

from . import spec
from .aggregate import SubComponents, legitimacy_multiplier


LOOP_NAMES = {
    "L1": "Regulatory Capture Accelerator",
    "L2": "Legitimacy Death Spiral",
    "L3": "Polarisation Trap",
    "L4": "Exit-Fragmentation Coupling",
}

# Part IV §2.4 "Loop Cross-Coupling Structure"
CROSS_COUPLING: Dict[str, List[str]] = {
    "L1": ["L3", "L4"],   # raises C₁ → funds polarising media; raises exit incentive
    "L2": ["L1", "L3"],   # lowers S₃ → weaker effective Ŝ₂; institutional failure raises C₅
    "L3": ["L2", "L4"],   # raises C₅ → incoherent policy lowers S₃; elites exit
    "L4": ["L2", "L3"],   # raises C₅, lowers S₁ → coercion up; further fragmentation
}


@dataclass
class LoopState:
    loop: str
    name: str
    active: bool
    margin: float          # how far past threshold (>0 = active), normalised units
    detail: str
    uncalibrated: bool     # True if activation test relies on a FREE parameter

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class LoopDiagnosis:
    loops: Dict[str, LoopState]
    cai: float
    cai_band: str
    cai_horizon: str
    active_count: int
    uncalibrated_loops: List[str]
    synchronised: List[str]   # active loops that also feed another active loop

    def as_dict(self) -> dict:
        return {"loops": {k: v.as_dict() for k, v in self.loops.items()},
                "cai": self.cai, "cai_band": self.cai_band,
                "cai_horizon": self.cai_horizon,
                "active_count": self.active_count,
                "uncalibrated_loops": self.uncalibrated_loops,
                "synchronised": self.synchronised}


# ---------------------------------------------------------------------------
# L1 — Regulatory Capture Accelerator  (Part IV §2.1)
#   "crossed when C₁ exceeds ~0.70 of historical max AND Ŝ₂ falls below ~0.60"
# ---------------------------------------------------------------------------
def test_L1(sc: SubComponents, p: Optional[dict] = None) -> LoopState:
    p = p or {}
    c1_t = p.get("L1_c1_thresh", spec.LOOPS["L1_c1_thresh"].value)
    s2_t = p.get("L1_s2_thresh", spec.LOOPS["L1_s2_thresh"].value)
    cond_c1 = sc.c1 > c1_t
    cond_s2 = sc.s2 < s2_t
    active = cond_c1 and cond_s2
    margin = min(sc.c1 - c1_t, s2_t - sc.s2)
    return LoopState(
        "L1", LOOP_NAMES["L1"], active, margin,
        f"Ĉ₁={sc.c1:.2f} vs crit {c1_t:.2f} ({'OVER' if cond_c1 else 'under'}); "
        f"Ŝ₂={sc.s2:.2f} vs crit {s2_t:.2f} ({'BELOW' if cond_s2 else 'above'})",
        uncalibrated=False,   # both thresholds are PAPER values
    )


# ---------------------------------------------------------------------------
# L2 — Legitimacy Death Spiral  (Part IV §2.2, Part V V.US)
#   explosive when S₃ < 0.30  (equivalently λ < ~0.80)
# ---------------------------------------------------------------------------
def test_L2(sc: SubComponents, p: Optional[dict] = None) -> LoopState:
    p = p or {}
    s3_t = p.get("L2_s3_thresh", spec.LOOPS["L2_s3_thresh"].value)
    lam_t = p.get("L2_lambda_thresh", spec.LOOPS["L2_lambda_thresh"].value)
    lam = legitimacy_multiplier(sc.s3,
                                lambda_min=p.get("lambda_min"),
                                lambda_max=p.get("lambda_max"),
                                k=p.get("k"), s3_mid=p.get("s3_mid"))
    cond_s3 = sc.s3 < s3_t
    cond_lam = lam < lam_t
    active = cond_s3 or cond_lam
    margin = max(s3_t - sc.s3, (lam_t - lam) / lam_t)
    status = "EXPLOSIVE" if active else ("APPROACHING" if sc.s3 < s3_t + 0.10 else "damped")
    return LoopState(
        "L2", LOOP_NAMES["L2"], active, margin,
        f"S₃={sc.s3:.2f} vs crit {s3_t:.2f}; λ={lam:.3f} vs crit {lam_t:.2f} → {status}",
        uncalibrated=False,
    )


# ---------------------------------------------------------------------------
# L3 — Polarisation Trap  (Part IV §2.3)
#   self-sustaining when ε_p·Rev_Pol + η·C₅·C₃ > natural depolarisation rate
#   NOTE: ε_p, η and the natural rate are all FREE → this test is UNCALIBRATED.
#   Fallback: level-based proxy using C₅ and Revenue_Polarisation.
# ---------------------------------------------------------------------------
def test_L3(sc: SubComponents, revenue_polarisation: float,
            p: Optional[dict] = None,
            natural_depolarisation_rate: Optional[float] = None) -> LoopState:
    p = p or {}
    eps_p = p.get("epsilon_p", spec.LOOPS["epsilon_p"].value)
    eta = p.get("eta_echo", spec.LOOPS["eta_echo"].value)
    c5_t = p.get("L3_c5_thresh", spec.LOOPS["L3_c5_thresh"].value)
    rp_t = p.get("L3_revpol_thresh", spec.LOOPS["L3_revpol_thresh"].value)

    if natural_depolarisation_rate is not None:
        drive = eps_p * revenue_polarisation + eta * sc.c5 * sc.c3
        active = drive > natural_depolarisation_rate
        margin = drive - natural_depolarisation_rate
        detail = (f"drive={drive:.4f} vs natural depol rate "
                  f"{natural_depolarisation_rate:.4f} (formal test, eq L3)")
    else:
        active = (sc.c5 > c5_t) and (revenue_polarisation > rp_t)
        margin = min(sc.c5 - c5_t, revenue_polarisation - rp_t)
        detail = (f"C₅={sc.c5:.2f} vs {c5_t:.2f}; Rev_Pol={revenue_polarisation:.2f} "
                  f"vs {rp_t:.2f} (LEVEL PROXY — formal test needs ε_p, η, natural rate)")
    return LoopState("L3", LOOP_NAMES["L3"], active, margin, detail, uncalibrated=True)


# ---------------------------------------------------------------------------
# L4 — Exit-Fragmentation Coupling  (Part IV §2.4)
#   self-reinforcing when ξ·Ĉ₄·Ĉ₁ > natural C₅ decay
#                     AND χ·Ĉ₄·Ĉ₁ > G_base / S₁
# ---------------------------------------------------------------------------
def test_L4(sc: SubComponents, p: Optional[dict] = None,
            natural_c5_decay: Optional[float] = None,
            g_base: Optional[float] = None, s1_level: Optional[float] = None) -> LoopState:
    p = p or {}
    c4_t = p.get("L4_c4_thresh", spec.LOOPS["L4_c4_thresh"].value)
    c1_t = p.get("L4_c1_thresh", spec.LOOPS["L4_c1_thresh"].value)
    xi = p.get("xi", spec.LOOPS["xi"].value)
    chi = p.get("chi", spec.LOOPS["chi"].value)

    if natural_c5_decay is not None and g_base is not None and s1_level:
        cond_a = xi * sc.c4 * sc.c1 > natural_c5_decay
        cond_b = chi * sc.c4 * sc.c1 > g_base / s1_level
        active = cond_a and cond_b
        margin = min(xi * sc.c4 * sc.c1 - natural_c5_decay,
                     chi * sc.c4 * sc.c1 - g_base / s1_level)
        detail = f"formal test (eq L4): cond_a={cond_a}, cond_b={cond_b}"
    else:
        active = (sc.c4 > c4_t) and (sc.c1 > c1_t)
        margin = min(sc.c4 - c4_t, sc.c1 - c1_t)
        detail = (f"Ĉ₄={sc.c4:.2f} vs {c4_t:.2f}; Ĉ₁={sc.c1:.2f} vs {c1_t:.2f} "
                  f"(LEVEL PROXY — formal test needs ξ, χ, natural C₅ decay, G_base)")
    return LoopState("L4", LOOP_NAMES["L4"], active, margin, detail, uncalibrated=True)


# ---------------------------------------------------------------------------
# CAI  — Part IV eq. (CAI)
# ---------------------------------------------------------------------------
def _cai_band(cai: float) -> tuple[str, str]:
    if cai <= 0.0:
        return "damped", "linear dynamics dominate"
    if cai <= 2.0:
        return "manageable", "1-2 loops active; manageable non-linear effects"
    if cai <= 3.0:
        return "compounding", "3 loops active; crisis likely within 5-10 years"
    return "imminent", "all loops active; bifurcation imminent; 1-3 year horizon"


def diagnose(sc: SubComponents,
             revenue_polarisation: float = 0.0,
             p: Optional[dict] = None,
             **formal_kwargs) -> LoopDiagnosis:
    """Run all four loop tests and compute CAI."""
    p = p or {}
    states = {
        "L1": test_L1(sc, p),
        "L2": test_L2(sc, p),
        "L3": test_L3(sc, revenue_polarisation, p,
                      natural_depolarisation_rate=formal_kwargs.get("natural_depolarisation_rate")),
        "L4": test_L4(sc, p,
                      natural_c5_decay=formal_kwargs.get("natural_c5_decay"),
                      g_base=formal_kwargs.get("g_base"),
                      s1_level=formal_kwargs.get("s1_level")),
    }

    cai = 0.0
    for key, st in states.items():
        if st.active:
            cw = p.get(f"coupling_{key}", spec.LOOP_COUPLING_WEIGHT[key].value)
            sp = p.get(f"speed_{key}", spec.LOOP_SPEED[key].value)
            cai += cw * sp

    band, horizon = _cai_band(cai)
    active = [k for k, v in states.items() if v.active]
    sync = [k for k in active if any(t in active for t in CROSS_COUPLING[k])]

    return LoopDiagnosis(
        loops=states, cai=cai, cai_band=band, cai_horizon=horizon,
        active_count=len(active),
        uncalibrated_loops=[k for k, v in states.items() if v.uncalibrated],
        synchronised=sync,
    )


# ---------------------------------------------------------------------------
# Bifurcation risk  — Part II eq. (23)
# ---------------------------------------------------------------------------
def bifurcation_risk(delta_norm: float, d_delta_dt: float, psi: float,
                     p: Optional[dict] = None) -> dict:
    """R_B = 1[Δ<Δ_crit] · 1[dΔ/dt<−δ_c] · 1[Ψ<Ψ_crit]  — all three required."""
    p = p or {}
    d_crit = p.get("delta_crit", spec.COHERENCE["delta_crit"].value)
    dc = p.get("delta_c", spec.COHERENCE["delta_c"].value)
    psi_crit = p.get("psi_crit", spec.COHERENCE["psi_crit"].value)

    c1 = delta_norm < d_crit
    c2 = d_delta_dt < -dc
    c3 = psi < psi_crit
    return {
        "R_B": int(c1 and c2 and c3),
        "cond_delta_below_crit": c1,
        "cond_momentum": c2,
        "cond_low_coherence": c3,
        "detail": (f"Δ_norm={delta_norm:+.3f} vs {d_crit:+.2f} [{c1}]; "
                   f"dΔ/dt={d_delta_dt:+.3f} vs {-dc:+.2f} [{c2}]; "
                   f"Ψ={psi:.3f} vs {psi_crit:.2f} [{c3}]"),
    }


# ---------------------------------------------------------------------------
# Post-bifurcation attractor selection  — Part II eq. (21)
# ---------------------------------------------------------------------------
def attractor(sc: SubComponents, g_shock: float, p: Optional[dict] = None) -> dict:
    """Which of A₁/A₂/A₃ the system heads toward if R_B=1."""
    p = p or {}
    c1_crit = p.get("c1_crit", spec.CAPTURE["c1_crit"].value)
    scores = {
        "A1_S_dominant_reconstitution": g_shock,
        "A2_C_dominant_capture": max(sc.c1 - c1_crit, 0.0) * (1.0 - sc.s2),
        "A3_fragmentation_collapse": sc.c5 ** 2 * (1.0 - max(sc.c1 - c1_crit, 0.0)),
    }
    winner = max(scores, key=scores.get)
    return {"scores": scores, "most_likely": winner,
             "note": "relative scores only; Part IV says attractor selection "
                     "requires the full non-linear manifold — UNCALIBRATED"}

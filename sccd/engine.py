"""
SCCD Engine — Orchestrator
===========================
Single entry point:  diagnose() -> Diagnosis

Pipeline (mirrors the Lục Hào engine's fixed stage order):

  ingest  →  normalise  →  aggregate  →  classify  →  loops  →  risk  →  report
  (Part III)  (Part III §5)  (Part II)   (Part II T2)  (Part IV §2)  (eq 23)

Every output carries a CALIBRATION TAG:
  CALIBRATED   — depends only on PAPER-specified parameters
  UNCALIBRATED — depends on at least one FREE parameter
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

from . import spec, loops as loopmod, network as netmod
from .aggregate import SubComponents, Capacity, compute
from .normalize import propagate, UncertainDelta


CALIBRATED_OUTPUTS = (
    "lambda", "theta25", "S", "delta", "delta_norm", "regime", "psi",
    "L1_active", "L2_active", "R_B",
)
UNCALIBRATED_OUTPUTS = (
    "C", "L3_active", "L4_active", "CAI", "trajectory", "psi_G",
    "T_trap", "attractor",
)


@dataclass
class Diagnosis:
    country: str
    year: int
    state_type: str
    capacity: Capacity
    loop_diagnosis: loopmod.LoopDiagnosis
    bifurcation: dict
    attractor: dict
    uncertainty: Optional[UncertainDelta]
    calibration_notes: List[str]
    inputs: Dict[str, float]

    # -- rendering ----------------------------------------------------------
    def summary(self) -> str:
        c = self.capacity
        L = self.loop_diagnosis
        lines = [
            f"SCCD DIAGNOSIS — {self.country} {self.year}   "
            f"[spec v{spec.SPEC_VERSION}, state_type={self.state_type}]",
            "=" * 78,
            f"  S  = {c.S:+.4f}    (λ={c.lam:.3f}  θ₂₅={c.theta25:.4f}  "
            f"core={c.s_core:.4f})",
            f"  C  = {c.C:+.4f}    (Π={c.pi_exit:.3f}  num={c.c_numerator:.4f}  "
            f"den={c.c_denominator:.4f})   [UNCALIBRATED: φ, ψ, α_exit]",
            f"  Δ  = {c.delta:+.4f}   Δ_norm = {c.delta_norm:+.4f}",
            f"  REGIME: {c.regime}  ({c.stability})",
            f"  Ψ  = {c.psi:.4f}   vs Ψ_crit = {spec.COHERENCE['psi_crit'].value:.2f}"
            f"  → {'ABOVE' if c.psi > spec.COHERENCE['psi_crit'].value else 'BELOW'}",
            "-" * 78,
            f"  FEEDBACK LOOPS   CAI = {L.cai:.2f} ({L.cai_band}): {L.cai_horizon}",
        ]
        for k in ("L1", "L2", "L3", "L4"):
            st = L.loops[k]
            tag = "ACTIVE  " if st.active else "damped  "
            unc = " [UNCAL]" if st.uncalibrated else ""
            lines.append(f"    {k} {tag}{st.name}{unc}")
            lines.append(f"        {st.detail}")
        if L.synchronised:
            lines.append(f"    CROSS-COUPLED & ACTIVE: {', '.join(L.synchronised)} "
                         f"→ compound acceleration operative")
        lines += [
            "-" * 78,
            f"  BIFURCATION RISK  R_B = {self.bifurcation['R_B']}",
            f"        {self.bifurcation['detail']}",
        ]
        if self.bifurcation["R_B"] == 1:
            lines.append(f"  → most likely attractor: {self.attractor['most_likely']}")
        if self.uncertainty:
            u = self.uncertainty
            lines += [
                "-" * 78,
                f"  UNCERTAINTY ({u.draws} MC draws)",
                f"    Δ_norm median {u.median_delta_norm:+.4f}  "
                f"80% CI [{u.ci80[0]:+.4f}, {u.ci80[1]:+.4f}]  "
                f"95% CI [{u.ci95[0]:+.4f}, {u.ci95[1]:+.4f}]",
                f"    regime distribution: " + ", ".join(
                    f"{k} {v:.0%}" for k, v in u.regime_distribution.items()),
            ]
        if self.calibration_notes:
            lines += ["-" * 78, "  CALIBRATION WARNINGS"]
            lines += [f"    ! {n}" for n in self.calibration_notes]
        return "\n".join(lines)


def diagnose(country: str, year: int, sub: SubComponents,
             state_type: str = "liberal_democracy",
             revenue_polarisation: float = 0.0,
             d_delta_dt: float = 0.0,
             g_shock: float = 0.0,
             params: Optional[dict] = None,
             sigma: Optional[Dict[str, float]] = None,
             mc_draws: Optional[int] = None) -> Diagnosis:
    """Run the full single-state pipeline."""
    cap = compute(sub, state_type=state_type, params=params)
    L = loopmod.diagnose(sub, revenue_polarisation=revenue_polarisation, p=params)
    rb = loopmod.bifurcation_risk(cap.delta_norm, d_delta_dt, cap.psi, p=params)
    att = loopmod.attractor(sub, g_shock, p=params)

    unc = None
    if sigma:
        unc = propagate(sub, sigma, state_type=state_type, params=params,
                        draws=mc_draws)

    notes: List[str] = []
    notes.append("C and Δ depend on φ, ψ, α_exit — all FREE in the paper. "
                 "Δ level is therefore scenario-relative, not absolute.")
    if L.uncalibrated_loops:
        notes.append(f"Loops {', '.join(L.uncalibrated_loops)} use LEVEL-PROXY "
                     f"activation tests; formal tests need ε_p, η, χ, ξ and the "
                     f"natural depolarisation/decay rates.")
    notes.append("CAI uses unit Coupling_Weight and Loop_Speed — the paper "
                 "states no values, so CAI is effectively a count of active loops.")
    if sub.s3 < 0.45:
        notes.append("S₃ is the highest-risk proxy (Part III §2.3). Widen all "
                     "λ-dependent intervals.")

    return Diagnosis(country=country, year=year, state_type=state_type,
                     capacity=cap, loop_diagnosis=L, bifurcation=rb,
                     attractor=att, uncertainty=unc, calibration_notes=notes,
                     inputs=sub.as_dict())

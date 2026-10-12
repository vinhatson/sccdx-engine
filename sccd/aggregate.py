"""
SCCD Engine — Aggregation Layer
================================
Implements Part II equations (1)-(10): the mapping from the ten normalised
sub-components (Ŝ1..Ŝ5, Ĉ1..Ĉ5) to the scalars S, C, Δ, Δ_norm, plus the
legitimacy multiplier λ and threshold factor θ₂₅.

This is the deterministic core — the analogue of the Lục Hào "trạng thái hào"
layer. Given the ten normalised inputs it is fully determined; no data access,
no I/O, no randomness.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from typing import Dict, Optional

from . import spec


# ---------------------------------------------------------------------------
# Input container
# ---------------------------------------------------------------------------
@dataclass
class SubComponents:
    """Normalised sub-components, each in [0,1] (post boundary-compression)."""
    s1: float  # Fiscal Extraction Capacity
    s2: float  # Coercive Monopoly Index
    s3: float  # Legitimacy Capital
    s4: float  # Administrative Penetration Depth
    s5: float  # Temporal Leverage
    c1: float  # Private Capital Concentration
    c2: float  # Civil Organization Density
    c3: float  # Information Autonomy
    c4: float  # Exit Option Availability
    c5: float  # Preference Fragmentation (INHIBITOR — raw, not inverted)

    def validate(self) -> None:
        for k, v in asdict(self).items():
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"{k}={v} outside [0,1]; normalise first (Part III §5.4)")

    def as_dict(self) -> Dict[str, float]:
        return asdict(self)


@dataclass
class Capacity:
    """Output of the aggregation layer."""
    S: float
    C: float
    delta: float
    delta_norm: float
    lam: float           # λ(S₃)
    theta25: float       # θ₂₅
    pi_exit: float       # Π exit adjustment
    s_core: float        # the bracket term in eq (5), pre-multiplier
    c_numerator: float
    c_denominator: float
    regime: str
    stability: str
    psi: float           # coherence index, eq (22)

    def as_dict(self) -> Dict[str, float]:
        return asdict(self)


# ---------------------------------------------------------------------------
# λ(S₃)  — Part II eq. (2)
# ---------------------------------------------------------------------------
def legitimacy_multiplier(s3: float,
                          lambda_min: Optional[float] = None,
                          lambda_max: Optional[float] = None,
                          k: Optional[float] = None,
                          s3_mid: Optional[float] = None) -> float:
    """Hill-function legitimacy multiplier.

        λ(S₃) = λ_min + (λ_max − λ_min) · S₃^k / (S₃^k + S₃_mid^k)
    """
    lmin = spec.LAMBDA["lambda_min"].value if lambda_min is None else lambda_min
    lmax = spec.LAMBDA["lambda_max"].value if lambda_max is None else lambda_max
    kk = spec.LAMBDA["k"].value if k is None else k
    mid = spec.LAMBDA["s3_mid"].value if s3_mid is None else s3_mid

    if s3 <= 0.0:
        return lmin
    num = s3 ** kk
    den = num + mid ** kk
    return lmin + (lmax - lmin) * (num / den)


# ---------------------------------------------------------------------------
# θ₂₅  — Part II eq. (4)
# ---------------------------------------------------------------------------
def _smooth_heaviside(x: float, eps: float) -> float:
    """H(x) = 1/(1+exp(−x/ε)); ε→0 gives a hard step."""
    z = x / eps
    if z > 60:      # avoid overflow
        return 1.0
    if z < -60:
        return 0.0
    return 1.0 / (1.0 + math.exp(-z))


def threshold_factor(s2: float, s5: float,
                     s2_crit: Optional[float] = None,
                     s5_crit: Optional[float] = None,
                     eps: Optional[float] = None) -> float:
    """θ₂₅ = H(Ŝ₂ − Ŝ₂,c) · H(Ŝ₅ − Ŝ₅,c)"""
    c2 = spec.THETA["s2_crit"].value if s2_crit is None else s2_crit
    c5 = spec.THETA["s5_crit"].value if s5_crit is None else s5_crit
    e = spec.THETA["epsilon"].value if eps is None else eps
    return _smooth_heaviside(s2 - c2, e) * _smooth_heaviside(s5 - c5, e)


# ---------------------------------------------------------------------------
# S aggregation  — Part II eq. (5)
# ---------------------------------------------------------------------------
def aggregate_S(sc: SubComponents,
                state_type: str = "liberal_democracy",
                params: Optional[dict] = None) -> tuple[float, float, float, float]:
    """
        S = λ(Ŝ₃) · [ w₁·Ŝ₁ + w₄·Ŝ₄ + θ₂₅ · min(Ŝ₂,Ŝ₅) · ω₂₅ ]

    Returns (S, lambda, theta25, s_core).
    """
    p = params or {}
    if state_type not in spec.STATE_TYPE_WEIGHTS:
        raise ValueError(f"unknown state_type {state_type!r}; "
                         f"choose from {list(spec.STATE_TYPE_WEIGHTS)}")
    w1, w4, om25 = spec.STATE_TYPE_WEIGHTS[state_type]

    lam = legitimacy_multiplier(
        sc.s3,
        lambda_min=p.get("lambda_min"), lambda_max=p.get("lambda_max"),
        k=p.get("k"), s3_mid=p.get("s3_mid"),
    )
    th = threshold_factor(
        sc.s2, sc.s5,
        s2_crit=p.get("s2_crit"), s5_crit=p.get("s5_crit"), eps=p.get("epsilon"),
    )
    s_core = w1 * sc.s1 + w4 * sc.s4 + th * min(sc.s2, sc.s5) * om25
    return lam * s_core, lam, th, s_core


# ---------------------------------------------------------------------------
# C aggregation  — Part II eq. (6)-(8)
# ---------------------------------------------------------------------------
def aggregate_C(sc: SubComponents,
                params: Optional[dict] = None,
                pi_scope: Optional[str] = None) -> tuple[float, float, float, float]:
    """
        C = [ Σ_{j∈1..4} v_j·Ĉ_j · Π ] / (1 + φ·C₅^ψ)
        Π = 1 − α_exit·Ĉ₄                                  (eq 7)

    pi_scope == "c1_only"   : Π multiplies only the v₁Ĉ₁ term (eq 7 wording)
    pi_scope == "whole_sum" : Π multiplies the whole numerator (eq 6 wording)

    Returns (C, pi, numerator, denominator).
    """
    p = params or {}
    scope = pi_scope or spec.PI_SCOPE

    v1 = p.get("v1", spec.C_WEIGHTS["v1"].value)
    v2 = p.get("v2", spec.C_WEIGHTS["v2"].value)
    v3 = p.get("v3", spec.C_WEIGHTS["v3"].value)
    v4 = p.get("v4", spec.C_WEIGHTS["v4"].value)
    phi = p.get("phi", spec.FRAGMENTATION["phi"].value)
    psi = p.get("psi", spec.FRAGMENTATION["psi"].value)
    a_exit = p.get("alpha_exit", spec.FRAGMENTATION["alpha_exit"].value)

    pi = 1.0 - a_exit * sc.c4

    if scope == "c1_only":
        numerator = v1 * sc.c1 * pi + v2 * sc.c2 + v3 * sc.c3 + v4 * sc.c4
    elif scope == "whole_sum":
        numerator = (v1 * sc.c1 + v2 * sc.c2 + v3 * sc.c3 + v4 * sc.c4) * pi
    else:
        raise ValueError(f"pi_scope must be 'c1_only' or 'whole_sum', got {scope!r}")

    denominator = 1.0 + phi * (sc.c5 ** psi)
    return numerator / denominator, pi, numerator, denominator


# ---------------------------------------------------------------------------
# Coherence index Ψ  — Part II eq. (22)
# ---------------------------------------------------------------------------
def coherence_index(lam: float, theta25: float, c5: float) -> float:
    """Ψ(t) = λ(S₃) · θ₂₅ · (1 − C₅),  range [0, λ_max]."""
    return lam * theta25 * (1.0 - c5)


# ---------------------------------------------------------------------------
# Regime classification  — Part II Table 2
# ---------------------------------------------------------------------------
def classify_regime(delta_norm: float) -> tuple[str, str]:
    for name, lo, hi, stab in spec.REGIME_BANDS:
        if lo < delta_norm <= hi:
            return name, stab
    if delta_norm <= spec.REGIME_BANDS[-1][1]:
        return "Crisis (below modelled range)", "Unstable (bifurcation)"
    return "Imperial (above modelled range)", "Unstable (drain)"


# ---------------------------------------------------------------------------
# Full aggregation
# ---------------------------------------------------------------------------
def compute(sc: SubComponents,
            state_type: str = "liberal_democracy",
            params: Optional[dict] = None,
            pi_scope: Optional[str] = None,
            validate: bool = True) -> Capacity:
    """Run the complete Part II aggregation chain."""
    if validate:
        sc.validate()
    p = params or {}

    S, lam, th, s_core = aggregate_S(sc, state_type=state_type, params=p)
    C, pi, c_num, c_den = aggregate_C(sc, params=p, pi_scope=pi_scope)

    delta = S - C
    lmax = p.get("lambda_max", spec.LAMBDA["lambda_max"].value)
    delta_norm = delta / lmax                      # eq (10)

    regime, stability = classify_regime(delta_norm)
    psi = coherence_index(lam, th, sc.c5)

    return Capacity(S=S, C=C, delta=delta, delta_norm=delta_norm,
                    lam=lam, theta25=th, pi_exit=pi, s_core=s_core,
                    c_numerator=c_num, c_denominator=c_den,
                    regime=regime, stability=stability, psi=psi)

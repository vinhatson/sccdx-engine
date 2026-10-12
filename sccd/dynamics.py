"""
SCCD Engine — Dynamics Layer (Part II eq. 11-18, Part IV eq. NL)
=================================================================
The four-state non-linear single-state system:

    state vector y = [S, C, S3, C5]

    dS/dt  = G − D − E − Γ − κ(1−λ/λmax)S₁ − χĈ₄Ĉ₁(S₁−S₁floor)
    dC/dt  = D + R − T − W + μΓ + ξĈ₄Ĉ₁(1−C₅)
    dS3/dt = S3_natural − ρ_b(1−λ/λmax)² − ζC₅^ψ(S₃−S₃floor)
    dC5/dt = C5_structural + ε_p C₅(1−C₅)Rev_Pol + η C₅²C₃ + ξĈ₄Ĉ₁(1−C₅)

Integrated with LSODA / Radau per Part IV §8.1 (the system is stiff).

WARNING: nearly every coefficient in this module is a FREE parameter — the
paper proposes functional forms but no estimated values. Trajectories are
STRUCTURAL SCENARIOS, not forecasts, until Stage 1-4 estimation is done.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Sequence

import numpy as np
try:
    from scipy.integrate import solve_ivp
    _SOLVER_BACKEND = "scipy"
except ImportError:                     # SCCD-X: scipy-free fallback (see sccdx/integrate.py)
    from sccdx.integrate import solve_ivp
    _SOLVER_BACKEND = "DP45-fallback"

from . import spec
from .aggregate import SubComponents, legitimacy_multiplier, threshold_factor


# ---------------------------------------------------------------------------
# Term-by-term implementations
# ---------------------------------------------------------------------------
def G(t: float, p: Dict[str, float],
      t_shock: Callable[[float], float] | None = None,
      w_shock: Callable[[float], float] | None = None) -> float:
    """Generation function, Part II eq. (12).

        G(t) = G_base·(1 + g_tech·T_shock)·(1 + g_war·W_shock)
    """
    ts = t_shock(t) if t_shock else 0.0
    ws = w_shock(t) if w_shock else 0.0
    return p["G_base"] * (1.0 + p["g_tech"] * ts) * (1.0 + p["g_war"] * ws)


def pulse(t0: float, tau: float, amplitude: float = 1.0) -> Callable[[float], float]:
    """Exponentially decaying shock pulse, Part II §5.1 ('spike then decay')."""
    def f(t: float) -> float:
        if t < t0:
            return 0.0
        return amplitude * math.exp(-(t - t0) / tau)
    return f


def D(S: float, c1: float, c2: float, p: Dict[str, float]) -> Dict[str, float]:
    """Drain function, Part II eq. (13). Returns the three channels + total."""
    d_prod = p["delta_p"] * S * max(1.0 - c1 - c2, 0.0)
    d_dist = p["delta_d"] * p["policy"] * S * (c2 ** 2)
    d_spont = p["delta_s"] * S
    return {"prod": d_prod, "dist": d_dist, "spont": d_spont,
            "total": d_prod + d_dist + d_spont}


def E(t: float, shocks: Sequence[dict] | None) -> float:
    """Exogenous shock term, Part II eq. (14).

    shocks: [{'t': year, 'e': severity, 'tau': recovery timescale}, ...]
    """
    if not shocks:
        return 0.0
    tot = 0.0
    for s in shocks:
        if t >= s["t"]:
            tot += s["e"] * math.exp(-(t - s["t"]) / s["tau"])
    return tot


def Gamma(S: float, c1: float, s2: float, p: Dict[str, float]) -> float:
    """Capture function, Part II eq. (15).

        Γ = γ₀ · max(Ĉ₁ − Ĉ₁,crit, 0)^β · (1 − Ŝ₂) · S
    """
    excess = max(c1 - p["c1_crit"], 0.0)
    if excess == 0.0:
        return 0.0
    return p["gamma0"] * (excess ** p["beta"]) * (1.0 - s2) * S


def R(c1: float, p: Dict[str, float]) -> float:
    """Civilian compound growth, Part II eq. (16) — logistic in C₁."""
    return p["r_cap"] * c1 * (1.0 - c1 / p["c1_max"])


def T(S: float, C: float, s1: float, c4: float, lam: float,
      p: Dict[str, float]) -> float:
    """State re-extraction, Part II eq. (17).

        T = τ_eff·C,   τ_eff = τ_max·Ŝ₁·(1−Ĉ₄)·λ/λ_max
    """
    tau_eff = p["tau_max"] * s1 * (1.0 - c4) * (lam / p["lambda_max"])
    return tau_eff * C


def W(C: float, c5: float, p: Dict[str, float]) -> float:
    """Civilian dissipation, Part II eq. (18):  W = ω·C₅^ψ·C."""
    return p["omega_w"] * (c5 ** p["psi"]) * C


# ---------------------------------------------------------------------------
# Default parameter bundle
# ---------------------------------------------------------------------------
def default_params(state_type: str = "liberal_democracy") -> Dict[str, float]:
    p: Dict[str, float] = {}
    for grp in (spec.LAMBDA, spec.THETA, spec.C_WEIGHTS, spec.FRAGMENTATION,
                spec.COHERENCE, spec.CAPTURE, spec.DYNAMICS, spec.LOOPS,
                spec.PATCH_V101):
        for k, v in grp.items():
            p[k] = v.value
    w1, w4, om25 = spec.STATE_TYPE_WEIGHTS[state_type]
    p.update(w1=w1, w4=w4, omega25=om25)
    return p


def free_parameters_used() -> list[str]:
    """Names of FREE parameters this module depends on."""
    out = []
    for grp in (spec.FRAGMENTATION, spec.DYNAMICS, spec.LOOPS, spec.THETA):
        for k, v in grp.items():
            if v.status == "FREE":
                out.append(k)
    return sorted(set(out))


# ---------------------------------------------------------------------------
# The RHS of the four-state system
# ---------------------------------------------------------------------------
@dataclass
class Context:
    """Sub-components held fixed (or exogenously driven) during integration.

    S₃ and C₅ become dynamical variables in the non-linear model (Part IV §3);
    the remaining six stay exogenous unless a driver is supplied.
    """
    s1: float
    s2: float
    s4: float
    s5: float
    c1: float
    c2: float
    c3: float
    c4: float
    revenue_polarisation: float = 0.0
    s3_natural: float = 0.0        # exogenous legitimacy trend
    c5_structural: float = 0.0     # exogenous fragmentation trend
    shocks: Sequence[dict] | None = None
    t_shock: Callable[[float], float] | None = None
    w_shock: Callable[[float], float] | None = None


def rhs(t: float, y: np.ndarray, ctx: Context, p: Dict[str, float],
        patch: bool = False, c1_dynamic: bool = False) -> list[float]:
    """RHS of the state system.

    c1_dynamic=False → 4 states [S, C, S₃, C₅]  (eq NL / INT §7.1 as written)
    c1_dynamic=True  → 5 states [S, C, S₃, C₅, C₁] using Part IV §2.1's own
                       dC₁/dt. This CLOSES loops L1 and L4 (spec INC-9).
    """
    if c1_dynamic:
        S, C, s3, c5, c1 = y
        c1 = min(max(c1, 0.0), 1.0)
    else:
        S, C, s3, c5 = y
        c1 = ctx.c1
    s3 = min(max(s3, 0.0), 1.0)
    c5 = min(max(c5, 0.0), 1.0)
    S = max(S, 0.0)
    C = max(C, 0.0)

    lam = legitimacy_multiplier(s3, p["lambda_min"], p["lambda_max"],
                                p["k"], p["s3_mid"])
    lam_ratio = lam / p["lambda_max"]

    g = G(t, p, ctx.t_shock, ctx.w_shock)
    d = D(S, c1, ctx.c2, p)["total"]
    e = E(t, ctx.shocks)
    gam = Gamma(S, c1, ctx.s2, p)
    r = R(c1, p)
    tt = T(S, C, ctx.s1, ctx.c4, lam, p)
    w = W(C, c5, p)

    exit_prod = ctx.c4 * c1
    tau_eff = p["tau_max"] * ctx.s1 * (1.0 - ctx.c4) * (lam / p["lambda_max"])

    # dS/dt  — Part IV eq. (NL)
    dS = (g - d - e - gam
          - p["kappa"] * (1.0 - lam_ratio) * ctx.s1
          - p["chi"] * exit_prod * max(ctx.s1 - p["s1_floor"], 0.0))

    # dC/dt
    dC = (d + r - tt - w
          + p["mu"] * gam
          + p["xi"] * exit_prod * (1.0 - c5))

    # dS₃/dt
    dS3 = (ctx.s3_natural
           - p["rho_b"] * (1.0 - lam_ratio) ** 2
           - p["zeta"] * (c5 ** p["psi"]) * max(s3 - p["s3_floor"], 0.0))

    # dC₅/dt
    dC5 = (ctx.c5_structural
           + p["epsilon_p"] * c5 * (1.0 - c5) * ctx.revenue_polarisation
           + p["eta_echo"] * (c5 ** 2) * ctx.c3
           + p["xi"] * exit_prod * (1.0 - c5))

    # ---- PATCH v1.01: terms the paper describes in prose but omits from (NL)
    if patch:
        # INC-7: natural depolarisation, counterweighted by civil organisation
        dC5 -= p["nu_depol"] * c5 * ctx.c2
        # INC-8: legitimacy recovery toward a performance-set target
        s3_target = p["s3_target_gain"] * ctx.s4
        dS3 += p["sigma_rec"] * (s3_target - s3)

    if not c1_dynamic:
        return [dS, dC, dS3, dC5]

    # ---- C₁ as a fifth state variable — Part IV §2.1, verbatim:
    #   dC₁/dt = v₁·D_drain→C₁ + r(t)·C₁(1−C₁/C₁max) − τ_eff·C₁ + μ·Γ
    dC1 = (p["v1"] * d
           + r
           - tau_eff * c1
           + p["mu"] * gam)
    return [dS, dC, dS3, dC5, dC1]


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------
@dataclass
class Trajectory:
    t: np.ndarray
    S: np.ndarray
    C: np.ndarray
    s3: np.ndarray
    c5: np.ndarray
    delta: np.ndarray
    delta_norm: np.ndarray
    psi: np.ndarray
    method: str
    success: bool
    message: str
    uncalibrated: bool = True
    free_params: tuple = ()
    c1: np.ndarray | None = None   # populated when c1_dynamic=True
    n_states: int = 4
    patched: bool = False


def simulate(sc: SubComponents, ctx: Context, years: float = 10.0,
             t0: float = 0.0, params: Optional[dict] = None,
             state_type: str = "liberal_democracy",
             method: str = "LSODA", n_out: int = 200,
             patch: Optional[bool] = None,
             c1_dynamic: bool = False) -> Trajectory:
    """Integrate the four-state non-linear system.

    Part IV §8.1 mandates adaptive stiff solvers: LSODA or Radau.

    patch=False reproduces eq (NL) verbatim — note that C₅ then rises
    monotonically and Ψ collapses on every path (spec INC-7/INC-8).
    patch=True adds the two missing restoring terms.
    """
    if patch is None:
        patch = spec.PATCH_ENABLED_BY_DEFAULT
    if method not in ("LSODA", "Radau", "BDF"):
        raise ValueError("Part IV §8.1 requires a stiff solver: LSODA, Radau or BDF")
    if _SOLVER_BACKEND != "scipy":
        # Part IV §8.1 asks for a stiff solver; without scipy we run explicit
        # DP45. Honest about it rather than silently pretending.
        method_label = f"{method} (requested) via {_SOLVER_BACKEND}"
    else:
        method_label = method

    p = default_params(state_type)
    if params:
        p.update(params)

    from .aggregate import compute
    cap0 = compute(sc, state_type=state_type, params=p)
    y0 = [cap0.S, cap0.C, sc.s3, sc.c5]
    if c1_dynamic:
        y0.append(sc.c1)

    t_eval = np.linspace(t0, t0 + years, n_out)
    sol = solve_ivp(rhs, (t0, t0 + years), y0, args=(ctx, p, patch, c1_dynamic),
                    method=method, t_eval=t_eval, rtol=1e-6, atol=1e-9)

    if c1_dynamic:
        S, C, s3, c5, c1 = sol.y
    else:
        S, C, s3, c5 = sol.y
        c1 = None
    lam = np.array([legitimacy_multiplier(v, p["lambda_min"], p["lambda_max"],
                                          p["k"], p["s3_mid"]) for v in s3])
    th = threshold_factor(ctx.s2, ctx.s5, p["s2_crit"], p["s5_crit"], p["epsilon"])
    delta = S - C
    return Trajectory(
        t=sol.t, S=S, C=C, s3=s3, c5=c5,
        delta=delta, delta_norm=delta / p["lambda_max"],
        psi=lam * th * (1.0 - c5),
        method=method_label, success=sol.success, message=sol.message,
        free_params=tuple(free_parameters_used()),
        c1=c1, n_states=5 if c1_dynamic else 4, patched=bool(patch),
    )

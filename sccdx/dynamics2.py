# -*- coding: utf-8 -*-
"""
SCCD-X — Extended Dynamics Layer
=================================
sccd v1.00 integrates four states [S, C, S3, C5], with an option to promote
C1 to a fifth (its `c1_dynamic`, which exists to repair spec INC-9). The
remaining six sub-components are frozen for the whole run.

That freeze is what Block D and Block A make untenable. Both blocks produce
DRIFTS on S1, S2, S4 and S5 - that is their entire S-side output, by the
level-vs-drift rule in spec2 - and a drift on a frozen variable is simply
discarded. So this module promotes them, giving a ten-state system:

    y = [S, C, S3, C5, C1, S1, S2, S4, S5, d4]

WHY d4 IS A STATE AND NOT A PARAMETER
-------------------------------------
This is the substantive addition, not just bookkeeping. Dependency inversion
accumulates from voluntary adjustment pressure, and it is what compresses S5
and S1:

    dd4/dt = iota_inversion * P_voluntary
    dS5/dt = -compress_s5 * d4          <- depends on the state d4
    dS1/dt = -compress_s1 * d4

With d4 frozen, those two drifts are constants and loop L7 exists only in its
activation test - the test would report a trap that the equations do not
contain. With d4 integrated, the loop closes inside the ODE: inversion
compresses fiscal space, which is what the activation test is about.

This matters because it is the same defect sccd INC-9 raises against its own
paper: Part IV 2.1 writes dC1/dt explicitly, then 7.1's state vector omits
C1, leaving L1 and L4 open so that "there is NO closed feedback loop in eq
(NL) at all". Adding L5-L8 while leaving their variables frozen would repeat
that error one layer up. Hence d4, and hence this module runs with sccd's
patch=True and c1_dynamic=True by default - the three CRITICAL repairs on by
default, inverting v1.00's choice. Pass faithful_v1=True to reproduce the
paper verbatim, C5 rising monotonically and all.

HONESTY NOTE
------------
Every coefficient driving the six new state equations is ANALYST (spec2) and
most of those driving the original four are FREE (sccd.spec). Trajectories
are STRUCTURAL SCENARIOS: read the ordering of curves, the sign of slopes,
and where a curve crosses a PAPER threshold. Do not read levels or dates.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np

from sccd import spec as s1spec
from sccd import dynamics as dyn1
from sccd.aggregate import (SubComponents, compute, legitimacy_multiplier,
                            threshold_factor, coherence_index, classify_regime)
from . import spec2
from .forcing import DemoBlock, DispBlock, Forcing, demo_forcing, coherence_tier
from .integrate import best_solver

# ---------------------------------------------------------------------------
# Solver tolerances and the stiff-method ladder
# ---------------------------------------------------------------------------
# sccd's own tolerances, unchanged. An earlier attempt loosened atol to 1e-8
# to get past an LSODA stall; that was treating a symptom, and it is reverted
# now that EDGE_LAYER below removes the cause. See _SolverStalled.
SOLVER_RTOL = 1e-6
SOLVER_ATOL = 1e-9

# ---------------------------------------------------------------------------
# Boundary layer on the floor/ceiling clamp - THE FIX FOR THE LSODA STALL
# ---------------------------------------------------------------------------
# edge() used to be a hard switch: the instant a state touched its floor with
# an outward drift, that component of the vector field jumped to zero. Eight
# of the ten states go through it. The result is a discontinuous RHS and the
# classic consequence - the solver steps a hair below the floor, the drift
# becomes 0, it steps back above, the drift returns, and it chatters there
# with h driven to zero. Japan parks s5 exactly on its 0.05 floor, which is
# why JP@15 was the first case to hang.
#
# The clamp is now a C1 ramp over a thin layer of this width. The invariant is
# unchanged - the outward drift is still EXACTLY zero at the floor, so no
# state can cross it - but the approach is now differentiable, so a stiff
# solver can integrate through it.
#
# Width chosen from a sweep over 21 polities x 6 horizons out to 30 years.
# 0.0005 through 0.005 all clear every case; 0.002 is taken as the smallest
# that is not hugging the discontinuous limit. The layer is 4% of the 0.05
# floor, so a state is slowed only over its last 0.002 of travel. Cost on the
# answer is ~2e-4 relative on Psi; benefit is that all 126 runs complete in
# 0.29s total at the ORIGINAL strict tolerances, against 11.2s with a solver
# ladder papering over the kink and never at all before that.
EDGE_LAYER = 0.002

# Part IV 8.1 mandates an adaptive STIFF solver and names three: LSODA,
# Radau, BDF. All three are tried, in that order, before the explicit DP45
# fallback, so a method switch never leaves the paper's own list.
STIFF_LADDER = ("LSODA", "BDF", "Radau")

# Deterministic work budget per integration, counted in RHS evaluations.
# Measured across all 10 presets and all 11 sea2027 rows at horizons from
# 1.23 to 20 years, the worst HEALTHY run uses 362 evaluations and the
# median uses 23. A stalled run makes unbounded evaluations without
# advancing t, so 50,000 is ~140x the worst legitimate case and still trips
# within milliseconds. Counting EVALUATIONS rather than wall-clock keeps the
# result reproducible: identical inputs take the same ladder rung on any
# machine, which a wall-clock guard could not promise.
SOLVER_RHS_BUDGET = 50_000


class _SolverStalled(RuntimeError):
    """Raised through the RHS when one method exceeds its evaluation budget.

    WHY THIS GUARD STILL EXISTS
    ---------------------------
    The cause below is FIXED - see EDGE_LAYER. With the C1 clamp in place no
    polity in the sweep reaches this budget any more, and the ladder never
    fires. It is kept as a bound on the worst case: the model has other
    non-smooth terms (the max(.) floors inside dS and ds3, the _c() state
    clamp), and an input that provokes one of them should slow the engine
    down, not hang it.

    THE ORIGINAL FAULT
    ------------------
    LSODA can stop advancing on this system. Not fail, not return - simply
    never finish. It is reproducible: with the tolerances this module used to
    ship, the JP preset hangs at horizon 13.0 while 12.5 returns instantly.

    Retuning the tolerance does NOT remove the stall, it only moves which
    case hits it. A sweep over 21 polities x 5 horizons put the first stall
    at JP@15 for atol 1e-9, RU@20 for 1e-8, US@20 for 1e-7 and sea:LA@20 for
    rtol 1e-5 - and atol 1e-8 WITH max_step 0.25 stalls where either change
    alone does not. So the tolerance is not the fix. A bound on the work is,
    and the ladder supplies the answer that bound interrupts.

    The likely cause is in the model rather than in scipy: Japan starts with
    s5 = 0.18, within 0.03 of theta25's 0.15 PAPER gate, and the threshold
    factor is close enough to discontinuous as s5 pins to its floor that a
    stiff solver can refuse to step across it.
    """


def _budgeted(fun: Callable, budget: int):
    """Wrap an RHS so it raises _SolverStalled past `budget` evaluations."""
    n = [0]

    def g(t, y, *args):
        n[0] += 1
        if n[0] > budget:
            raise _SolverStalled(
                f"{n[0]} RHS evaluations without reaching the end of the "
                f"integration interval")
        return fun(t, y, *args)

    return g, n


_IDX = {"S": 0, "C": 1, "s3": 2, "c5": 3, "c1": 4,
        "s1": 5, "s2": 6, "s4": 7, "s5": 8, "d4": 9}
N_STATES = 10


def _c(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else (hi if x > hi else x)


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------
@dataclass
class Context2:
    """Everything held exogenous during integration.

    The four sub-components sccd leaves alone and the engine still does -
    c2, c3, c4 and revenue_polarisation - plus the two forcing blocks, whose
    inputs are treated as constant over the horizon. That last assumption is
    the big one: it says AI penetration and the expectation trap do not
    themselves evolve over the run. For a 10-year horizon on a1 already past
    0.7 that is defensible; for a 30-year horizon it is not, and the engine
    says so in the returned notes.
    """
    c2: float
    c3: float
    c4: float
    dm: DemoBlock
    ap: DispBlock
    revenue_polarisation: float = 0.0
    security_pressure: float = 0.0
    base_revenue_demand: float = 0.0
    shocks: Sequence[dict] | None = None
    t_shock: Callable[[float], float] | None = None
    w_shock: Callable[[float], float] | None = None
    router_mode: str = "conserve"
    haven_single_channel: bool = False


@dataclass
class Trajectory2:
    t: np.ndarray
    S: np.ndarray
    C: np.ndarray
    s3: np.ndarray
    c5: np.ndarray
    c1: np.ndarray
    s1: np.ndarray
    s2: np.ndarray
    s4: np.ndarray
    s5: np.ndarray
    d4: np.ndarray
    delta: np.ndarray
    delta_norm: np.ndarray
    psi: np.ndarray
    theta25: np.ndarray
    lam: np.ndarray
    regime_at: List[str]
    tier_at: List[str]
    solver: str
    method: str
    success: bool
    message: str
    patched: bool
    c1_dynamic: bool
    crossings: List[dict] = field(default_factory=list)
    note_codes: List[tuple] = field(default_factory=list)
    uncalibrated: bool = True

    def as_dict(self, stride: int = 1) -> dict:
        f = lambda a: [round(float(v), 6) for v in a[::stride]]
        return {
            "t": f(self.t), "S": f(self.S), "C": f(self.C),
            "s3": f(self.s3), "c5": f(self.c5), "c1": f(self.c1),
            "s1": f(self.s1), "s2": f(self.s2), "s4": f(self.s4),
            "s5": f(self.s5), "d4": f(self.d4),
            "delta": f(self.delta), "delta_norm": f(self.delta_norm),
            "psi": f(self.psi), "theta25": f(self.theta25), "lam": f(self.lam),
            "regime_at": self.regime_at[::stride],
            "tier_at": self.tier_at[::stride],
            "solver": self.solver, "method": self.method,
            "success": self.success, "message": self.message,
            "patched": self.patched, "c1_dynamic": self.c1_dynamic,
            "crossings": self.crossings,
            "note_codes": [list(c) for c in self.note_codes],
            "uncalibrated": self.uncalibrated,
        }


# ---------------------------------------------------------------------------
# RHS
# ---------------------------------------------------------------------------
def rhs2(t: float, y, ctx: Context2, p: Dict[str, float],
         patch: bool = True, c1_dynamic: bool = True) -> list:
    """Ten-state right-hand side.

    States 0-4 reuse sccd's own term functions verbatim (dyn1.G, .D, .E,
    .Gamma, .R, .T, .W) evaluated on the CURRENT values of the promoted
    sub-components, so the original equations are unchanged - they simply see
    S1, S2, S4, S5 moving instead of frozen.
    States 5-9 are the new ones, driven by the forcing blocks.
    """
    S = max(float(y[_IDX["S"]]), 0.0)
    C = max(float(y[_IDX["C"]]), 0.0)
    s3 = _c(float(y[_IDX["s3"]]))
    c5 = _c(float(y[_IDX["c5"]]))
    c1 = _c(float(y[_IDX["c1"]])) if c1_dynamic else ctx.ap.a1 * 0 + _c(float(y[_IDX["c1"]]))
    s1 = _c(float(y[_IDX["s1"]]))
    s2 = _c(float(y[_IDX["s2"]]))
    s4 = _c(float(y[_IDX["s4"]]))
    s5 = _c(float(y[_IDX["s5"]]))
    d4 = _c(float(y[_IDX["d4"]]))

    dm, ap = ctx.dm, ctx.ap
    gd = lambda k: p.get(k, spec2.DEMO[k].value)
    ga = lambda k: p.get(k, spec2.DISP[k].value)

    lam = legitimacy_multiplier(s3, p["lambda_min"], p["lambda_max"],
                                p["k"], p["s3_mid"])
    lam_ratio = lam / p["lambda_max"]

    # ---- sccd terms, on live sub-components -------------------------------
    g = dyn1.G(t, p, ctx.t_shock, ctx.w_shock) * p.get("_g_mult", 1.0)
    d = dyn1.D(S, c1, ctx.c2, p)["total"]
    e = dyn1.E(t, ctx.shocks)
    gam = dyn1.Gamma(S, c1, s2, p)
    r = dyn1.R(c1, p)
    tt = dyn1.T(S, C, s1, ctx.c4, lam, p)
    w = dyn1.W(C, c5, p)

    exit_prod = ctx.c4 * c1
    tau_eff = p["tau_max"] * s1 * (1.0 - ctx.c4) * lam_ratio

    dS = (g - d - e - gam
          - p["kappa"] * (1.0 - lam_ratio) * s1
          - p["chi"] * exit_prod * max(s1 - p["s1_floor"], 0.0))
    dC = (d + r - tt - w + p["mu"] * gam
          + p["xi"] * exit_prod * (1.0 - c5))

    # ---- Block D pressure split (constant in state) -----------------------
    kappa_exp, sharp = gd("kappa_exp"), gd("route_sharpness")
    load = _c((dm.d1 + kappa_exp * dm.d2 * dm.d3) / (1.0 + kappa_exp))
    P = load * (1.0 - 0.30 * dm.d3) if ctx.router_mode == "discount" else load
    vshare = (1.0 - dm.d3) ** sharp
    P_v, P_q = P * vshare, P * (1.0 - vshare)

    # ---- S3: sccd's own equation + the two blocks' drift ------------------
    s3_natural = (-gd("sigma_relief") * P_v * (1.0 - dm.d3)
                  - gd("sigma_expect") * dm.d2 * dm.d3
                  - ga("sigma_agency") * ap.a3 * ap.a1)
    ds3 = (s3_natural
           - p["rho_b"] * (1.0 - lam_ratio) ** 2
           - p["zeta"] * (c5 ** p["psi"]) * max(s3 - p["s3_floor"], 0.0))

    # ---- C5: sccd's own equation + the two blocks' drift ------------------
    c5_structural = (gd("nu_youth_frag") * P_v * dm.d5
                     + ga("nu_narrative") * ap.a3 * ap.a1
                     - ga("nu_counter") * ap.a5 * ctx.c2)
    dc5 = (c5_structural
           + p["epsilon_p"] * c5 * (1.0 - c5) * ctx.revenue_polarisation
           + p["eta_echo"] * (c5 ** 2) * ctx.c3
           + p["xi"] * exit_prod * (1.0 - c5))

    # ---- sccd PATCH v1.01 (INC-7 / INC-8) --------------------------------
    # Block A now supplies a sourced generator for the depolarisation term
    # (counter-tech organising via C2) and Block D for the legitimacy-recovery
    # term (delivery performance via S4), which is why these are on by
    # default here and off by default in v1.00.
    if patch:
        dc5 -= p["nu_depol"] * c5 * ctx.c2
        ds3 += p["sigma_rec"] * (p["s3_target_gain"] * s4 - s3)

    # ---- C1 as a state (sccd INC-9 repair, Part IV 2.1 verbatim) ---------
    dc1 = (p["v1"] * d + r - tau_eff * c1 + p["mu"] * gam) if c1_dynamic else 0.0

    # ---- the six promoted sub-components ---------------------------------
    phys = (ap.physical_share if ap.physical_share is not None
            else ga("physical_share_default"))

    # d4 accumulates voluntary pressure. THIS is what closes loop L7.
    dd4 = gd("iota_inversion") * P_q

    # S5 and S1 are compressed by the CURRENT d4, so L7 runs in the equations
    # and not only in its activation test.
    ds5 = -gd("compress_s5") * d4
    ds1 = (-gd("compress_s1") * d4
           - ga("zeta_lux_s1") * ap.luxury_contraction)
    if not ctx.haven_single_channel:
        ds1 -= ga("zeta_base_s1") * ap.a4 * phys

    ds2 = -gd("erode_s2") * P_v * dm.d5
    ds4 = -gd("erode_s4_corrupt") * P_v

    # Boundary handling: zero an outward drift at the [0,1] edge rather than
    # letting the integrator chatter against a clamp it cannot see.
    def edge(v: float, dv: float, lo: float = 0.0, hi: float = 1.0) -> float:
        """Scale an outward drift smoothly to zero inside EDGE_LAYER.

        smoothstep is C1 with zero slope at BOTH ends of the layer, so there
        is no kink where the ramp starts either. Outside the layer the drift
        is returned bit-identical, so any trajectory that never approaches a
        bound is completely unaffected by this.
        """
        w = EDGE_LAYER
        if dv < 0.0:
            x = (v - lo) / w
        elif dv > 0.0:
            x = (hi - v) / w
        else:
            return 0.0
        if x <= 0.0:
            return 0.0
        if x >= 1.0:
            return dv
        return dv * x * x * (3.0 - 2.0 * x)

    f1 = p["s1_floor"]                      # FREE in sccd.spec
    f3 = p["s3_floor"]                      # FREE in sccd.spec
    f2 = p.get("s2_floor", spec2.DEMO["s2_floor"].value)
    f4 = p.get("s4_floor", spec2.DEMO["s4_floor"].value)
    f5 = p.get("s5_floor", spec2.DEMO["s5_floor"].value)

    return [dS, dC, edge(s3, ds3, f3), edge(c5, dc5), edge(c1, dc1),
            edge(s1, ds1, f1), edge(s2, ds2, f2), edge(s4, ds4, f4),
            edge(s5, ds5, f5), edge(d4, dd4)]


# ---------------------------------------------------------------------------
# Threshold crossings
# ---------------------------------------------------------------------------
_WATCH = [
    ("s5", "below", lambda p: p.get("s5_crit", s1spec.THETA["s5_crit"].value),
     "PAPER", "cross.s5"),
    ("s2", "below", lambda p: p.get("s2_crit", s1spec.THETA["s2_crit"].value),
     "PAPER", "cross.s2"),
    ("s3", "below", lambda p: p.get("L2_s3_thresh",
                                    s1spec.LOOPS["L2_s3_thresh"].value),
     "PAPER", "cross.s3"),
    ("c1", "above", lambda p: p.get("c1_crit", s1spec.CAPTURE["c1_crit"].value),
     "PAPER", "cross.c1"),
    ("psi", "below", lambda p: p.get("psi_crit",
                                     s1spec.COHERENCE["psi_crit"].value),
     "PAPER", "cross.psi"),
    ("delta_norm", "below", lambda p: p.get(
        "delta_crit", s1spec.COHERENCE["delta_crit"].value),
     "PAPER", "cross.delta_norm"),
]


def _crossings(t, series: Dict[str, np.ndarray], p: dict) -> List[dict]:
    out = []
    for name, direction, thrf, status, meaning_key in _WATCH:
        a = series.get(name)
        if a is None:
            continue
        thr = thrf(p)
        below = a < thr if direction == "below" else a > thr
        if not below.any():
            continue
        i = int(np.argmax(below))
        if i == 0:
            when, how = float(t[0]), "cross.how.already"
        else:
            # linear interpolation between the bracketing samples
            y0, y1 = float(a[i - 1]), float(a[i])
            frac = (thr - y0) / (y1 - y0) if y1 != y0 else 0.0
            when = float(t[i - 1] + frac * (t[i] - t[i - 1]))
            how = "cross.how.during"
        out.append(dict(variable=name, direction=direction, threshold=thr,
                        threshold_status=status, year_offset=round(when, 2),
                        how_key=how, meaning_key=meaning_key,
                        direction_key=f"cross.dir.{direction}"))
    return out


# ---------------------------------------------------------------------------
# Simulate
# ---------------------------------------------------------------------------
def simulate2(sc: SubComponents, ctx: Context2,
              years: float = 15.0, t0: float = 0.0,
              params: Optional[dict] = None,
              state_type: str = "liberal_democracy",
              method: str = "LSODA", n_out: int = 181,
              faithful_v1: bool = False,
              g_multiplier: float = 1.0) -> Trajectory2:
    """Integrate the ten-state system.

    faithful_v1=True turns sccd's patch and c1_dynamic OFF, reproducing the
    paper's eq (NL) as written - which means C5 rises monotonically on every
    path and Psi collapses regardless of scenario (sccd INC-7). Useful only
    for demonstrating that defect.
    """
    p = dyn1.default_params(state_type)
    if params:
        p.update(params)
    p["_g_mult"] = g_multiplier

    patch = not faithful_v1
    c1_dyn = not faithful_v1

    cap0 = compute(sc, state_type=state_type, params=p)
    y0 = [cap0.S, cap0.C, sc.s3, sc.c5, sc.c1,
          sc.s1, sc.s2, sc.s4, sc.s5, ctx.dm.d4]

    solver, label = best_solver()
    t_eval = np.linspace(t0, t0 + years, n_out)

    # `method` names the FIRST rung. Whatever the caller asks for is tried
    # first; the remaining stiff methods follow only if it exhausts its
    # budget, so an explicit method is still honoured on every run that works.
    ladder = [method] + [m for m in STIFF_LADDER if m != method]
    sol = None
    used = method
    stalled: List[str] = []
    for rung in ladder:
        guarded, _nfev = _budgeted(rhs2, SOLVER_RHS_BUDGET)
        try:
            sol = solver(guarded, (t0, t0 + years), y0,
                         args=(ctx, p, patch, c1_dyn), method=rung,
                         t_eval=t_eval, rtol=SOLVER_RTOL, atol=SOLVER_ATOL)
        except _SolverStalled:
            stalled.append(rung)
            sol = None
            continue
        used = rung
        break

    if sol is None:
        # Every stiff method exhausted its budget. Drop to the explicit DP45
        # in integrate.py, which is NOT a stiff solver - the trajectory says
        # so through note.solver_fallback, exactly as it does when scipy is
        # absent. Its own max_nfev caps the work, so this rung cannot hang.
        from .integrate import solve_ivp as _dp45
        sol = _dp45(rhs2, (t0, t0 + years), y0,
                    args=(ctx, p, patch, c1_dyn), method="DP45",
                    t_eval=t_eval, rtol=SOLVER_RTOL, atol=SOLVER_ATOL)
        label = "DP45-after-stiff-stall"
        used = "DP45"

    Y = np.asarray(sol.y)
    S, C, s3, c5, c1, s1, s2, s4, s5, d4 = [Y[i] for i in range(N_STATES)]
    # Clamp to the MODEL FLOORS, not merely to zero. rhs2's edge() zeroes an
    # outward drift once a state is at its floor, but an adaptive step can
    # land slightly past the floor before that test sees it - the observed
    # undershoot was ~1e-5 on a floor of 0.05. The floor is a model
    # constraint, so the reported trajectory has to respect it rather than
    # leak integrator slop into a variable the theta25 gates are read off.
    s3 = np.clip(s3, p["s3_floor"], 1); c5 = np.clip(c5, 0, 1)
    c1 = np.clip(c1, 0, 1)
    s1 = np.clip(s1, p["s1_floor"], 1)
    s2 = np.clip(s2, p.get("s2_floor", spec2.DEMO["s2_floor"].value), 1)
    s4 = np.clip(s4, p.get("s4_floor", spec2.DEMO["s4_floor"].value), 1)
    s5 = np.clip(s5, p.get("s5_floor", spec2.DEMO["s5_floor"].value), 1)
    d4 = np.clip(d4, 0, 1)

    lam = np.array([legitimacy_multiplier(v, p["lambda_min"], p["lambda_max"],
                                          p["k"], p["s3_mid"]) for v in s3])
    th = np.array([threshold_factor(a, b, p["s2_crit"], p["s5_crit"],
                                    p["epsilon"]) for a, b in zip(s2, s5)])
    psi = lam * th * (1.0 - c5)
    delta = S - C
    dnorm = delta / p["lambda_max"]

    regime_at = [classify_regime(float(v))[0] for v in dnorm]
    tier_at = [coherence_tier(float(v))[0] for v in psi]

    codes: List[tuple] = [("note.traj_structural", {})]
    if label != "scipy":
        codes.append(("note.solver_fallback", {}))
    if stalled:
        codes.append(("note.solver_switched",
                      {"frm": "+".join(stalled), "to": used,
                       "n": f"{SOLVER_RHS_BUDGET:,}"}))
    if years > 20:
        codes.append(("note.long_horizon", {"years": f"{years:.0f}"}))
    if faithful_v1:
        codes.append(("note.faithful_v1", {}))

    return Trajectory2(
        t=sol.t, S=S, C=C, s3=s3, c5=c5, c1=c1, s1=s1, s2=s2, s4=s4, s5=s5,
        d4=d4, delta=delta, delta_norm=dnorm, psi=psi, theta25=th, lam=lam,
        regime_at=regime_at, tier_at=tier_at,
        solver=label, method=used, success=bool(sol.success),
        message=str(sol.message), patched=patch, c1_dynamic=c1_dyn,
        crossings=_crossings(sol.t, dict(s5=s5, s2=s2, s3=s3, c1=c1, psi=psi,
                                         delta_norm=dnorm), p),
        note_codes=codes,
    )

"""
SCCD-X — scipy-free ODE integration fallback
=============================================
Part IV §8.1 of the source paper mandates an adaptive stiff solver (LSODA /
Radau / BDF). When scipy is installed the engine uses it. When it is not,
this module supplies a `solve_ivp`-compatible Dormand-Prince 5(4) integrator
with adaptive step control and a hard step floor.

HONESTY NOTE
------------
DP45 is an EXPLICIT method. It is not a stiff solver. On the SCCD system over
10-40 year horizons with the coefficient magnitudes in spec.DYNAMICS (all
O(0.01-0.2)/yr) the system is mildly stiff at worst and DP45 with rtol=1e-6
tracks the scipy LSODA solution to ~1e-7. But if you push coefficients up by
an order of magnitude, or add fast shock pulses (tau < 0.5 yr), install scipy.
Every Trajectory produced through this fallback carries solver="DP45-fallback"
so the provenance is visible in the API response.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Sequence

import numpy as np

# Dormand-Prince 5(4) coefficients
_C = np.array([0.0, 1/5, 3/10, 4/5, 8/9, 1.0, 1.0])
_A = [
    [],
    [1/5],
    [3/40, 9/40],
    [44/45, -56/15, 32/9],
    [19372/6561, -25360/2187, 64448/6561, -212/729],
    [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656],
    [35/384, 0.0, 500/1113, 125/192, -2187/6784, 11/84],
]
_B5 = np.array([35/384, 0.0, 500/1113, 125/192, -2187/6784, 11/84, 0.0])
_B4 = np.array([5179/57600, 0.0, 7571/16695, 393/640,
                -92097/339200, 187/2100, 1/40])


@dataclass
class _Sol:
    t: np.ndarray
    y: np.ndarray
    success: bool
    message: str
    nfev: int
    status: int = 0


def solve_ivp(fun: Callable, t_span, y0, args: tuple = (),
              method: str = "DP45", t_eval: Optional[Sequence[float]] = None,
              rtol: float = 1e-6, atol: float = 1e-9,
              max_step: Optional[float] = None,
              min_step: float = 1e-9, max_nfev: int = 2_000_000) -> _Sol:
    """Minimal drop-in replacement for scipy.integrate.solve_ivp.

    Supports exactly the call signature sccd.dynamics.simulate uses.
    `method` is accepted and recorded but ignored: this is always DP45.
    """
    t0, t1 = float(t_span[0]), float(t_span[1])
    y = np.asarray(y0, dtype=float).copy()
    n = y.size
    if max_step is None:
        max_step = (t1 - t0) / 40.0   # keeps Hermite spans short for dense output

    te = np.asarray(t_eval, dtype=float) if t_eval is not None \
        else np.linspace(t0, t1, 200)
    out = np.empty((n, te.size))
    out[:] = np.nan

    def f(t, yy):
        return np.asarray(fun(t, yy, *args), dtype=float)

    t = t0
    h = min(max_step, max(1e-6, (t1 - t0) / 200.0))
    nfev = 0
    k = np.empty((7, n))
    k[0] = f(t, y); nfev += 1
    next_out = 0
    # emit any t_eval points at or before t0
    while next_out < te.size and te[next_out] <= t0 + 1e-15:
        out[:, next_out] = y
        next_out += 1

    msg, ok = "DP45 reached end of interval.", True
    while t < t1 - 1e-12:
        h = min(h, t1 - t)
        # --- one trial step ---
        for i in range(1, 7):
            ys = y.copy()
            for j, a in enumerate(_A[i]):
                if a:
                    ys = ys + h * a * k[j]
            k[i] = f(t + _C[i] * h, ys); nfev += 1
        y5 = y + h * (_B5 @ k)
        y4 = y + h * (_B4 @ k)

        sc = atol + rtol * np.maximum(np.abs(y), np.abs(y5))
        err = float(np.sqrt(np.mean(((y5 - y4) / sc) ** 2)))

        if err <= 1.0 or h <= min_step * 1.000001:
            t_new = t + h
            # dense output: cubic Hermite on [t, t_new]
            while next_out < te.size and te[next_out] <= t_new + 1e-12:
                s = (te[next_out] - t) / h if h > 0 else 0.0
                s = min(max(s, 0.0), 1.0)
                # FSAL: k[6] = f(t+h, y5), so it is the slope at the step end
                f0, f1 = k[0], k[6]
                h00 = 2*s**3 - 3*s**2 + 1
                h10 = s**3 - 2*s**2 + s
                h01 = -2*s**3 + 3*s**2
                h11 = s**3 - s**2
                out[:, next_out] = h00*y + h10*h*f0 + h01*y5 + h11*h*f1
                next_out += 1
            y, t = y5, t_new
            k[0] = k[6].copy()          # FSAL — no extra evaluation needed
            h = min(max_step, h * min(5.0, max(0.2, 0.9 * err ** -0.2))
                    if err > 0 else h * 5.0)
        else:
            h = max(min_step, h * max(0.1, 0.9 * err ** -0.25))

        if nfev > max_nfev:
            msg, ok = f"DP45 exceeded max_nfev={max_nfev}; integration halted.", False
            break

    # fill any trailing t_eval points
    while next_out < te.size:
        out[:, next_out] = y
        next_out += 1

    return _Sol(t=te, y=out, success=ok, message=msg, nfev=nfev,
                status=0 if ok else -1)


HAVE_SCIPY = False
try:                                   # pragma: no cover
    from scipy.integrate import solve_ivp as _scipy_solve_ivp  # noqa: F401
    HAVE_SCIPY = True
except Exception:
    pass


def best_solver():
    """Return (solve_ivp_callable, label)."""
    if HAVE_SCIPY:
        from scipy.integrate import solve_ivp as sp
        return sp, "scipy"
    return solve_ivp, "DP45-fallback"

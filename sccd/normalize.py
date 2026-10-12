"""
SCCD Engine — Normalisation & Uncertainty Layer (Part III §5)
==============================================================
Five-step construction procedure:
  1. within-country standardisation          (eq 5.1)
  2. reliability-weighted multi-proxy merge   (eq 5.2) + Cronbach α gate
  3. missing-data imputation (Tier 1-4)       (§5.3)
  4. min-max normalisation + boundary compression (eq 5.3)
  5. Monte Carlo uncertainty propagation      (eq 5.4)

The Lục Hào engine needs none of this — a quẻ is given exactly. SCCD does,
because all ten inputs are latent. This layer is what makes the difference
between a rule engine and a measurement instrument.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import spec
from .aggregate import SubComponents, compute, Capacity


ImputeTier = int  # 0 = observed, 1..4 per Part III §5.3


# ---------------------------------------------------------------------------
# Step 1 — within-country standardisation (eq 5.1)
# ---------------------------------------------------------------------------
def standardise(series: Sequence[float]) -> np.ndarray:
    """z = (x − μ_country) / σ_country, over the full available series."""
    a = np.asarray(series, dtype=float)
    mu = np.nanmean(a)
    sd = np.nanstd(a)
    if sd == 0 or not np.isfinite(sd):
        return np.zeros_like(a)
    return (a - mu) / sd


# ---------------------------------------------------------------------------
# Step 2 — reliability-weighted merge (eq 5.2) + Cronbach α gate (§5.2)
# ---------------------------------------------------------------------------
def cronbach_alpha(items: np.ndarray) -> float:
    """items: (n_obs, k_proxies). Returns Cronbach's α."""
    items = np.asarray(items, dtype=float)
    items = items[~np.isnan(items).any(axis=1)]
    k = items.shape[1]
    if k < 2 or items.shape[0] < 3:
        return float("nan")
    item_var = items.var(axis=0, ddof=1).sum()
    total_var = items.sum(axis=1).var(ddof=1)
    if total_var == 0:
        return float("nan")
    return (k / (k - 1.0)) * (1.0 - item_var / total_var)


def reliability_weight(measurement_variance: float, coverage_score: float) -> float:
    """r_k = (1 / σ²_measurement,k) × Coverage_Score_k   (eq 5.2)"""
    if measurement_variance <= 0:
        raise ValueError("measurement_variance must be > 0")
    return (1.0 / measurement_variance) * coverage_score


def merge_proxies(z_by_proxy: Dict[str, np.ndarray],
                  weights: Dict[str, float],
                  enforce_alpha: bool = True) -> Tuple[np.ndarray, dict]:
    """Reliability-weighted composite with the Cronbach gate.

    If α < 0.65 the gate FAILS and the function falls back to the single
    highest-weight proxy, per Part III §5.2, and reports it.
    """
    names = list(z_by_proxy)
    mat = np.column_stack([z_by_proxy[n] for n in names])
    alpha = cronbach_alpha(mat) if len(names) > 1 else float("nan")
    a_min = spec.MEASUREMENT["cronbach_min"].value

    gate_failed = enforce_alpha and len(names) > 1 and np.isfinite(alpha) and alpha < a_min
    if gate_failed:
        best = max(names, key=lambda n: weights.get(n, 0.0))
        return z_by_proxy[best], {
            "alpha": alpha, "alpha_gate": "FAILED",
            "action": f"single-proxy fallback to {best}; widen CI",
            "proxies_used": [best],
        }

    w = np.array([weights.get(n, 1.0) for n in names], dtype=float)
    comp = (mat * w).sum(axis=1) / w.sum()
    return comp, {"alpha": alpha,
                  "alpha_gate": "PASSED" if len(names) > 1 else "N/A (single proxy)",
                  "action": "reliability-weighted merge",
                  "proxies_used": names}


# ---------------------------------------------------------------------------
# Step 3 — imputation (§5.3)
# ---------------------------------------------------------------------------
def impute(series: Sequence[float],
           volatile: bool = False) -> Tuple[np.ndarray, List[ImputeTier]]:
    """Tier-1 linear interpolation for gaps <= 3 years; longer gaps stay NaN
    and are flagged Tier 4 (Tier 2/3 require external proxies/covariates that
    this function does not have).

    volatile=True (S₁, C₁) disables Tier 1 per §5.3.
    """
    a = np.asarray(series, dtype=float).copy()
    tiers: List[ImputeTier] = [0 if np.isfinite(v) else 4 for v in a]
    if volatile:
        return a, tiers

    max_gap = int(spec.MEASUREMENT["interp_max_gap"].value)
    idx = np.arange(len(a))
    good = np.isfinite(a)
    if good.sum() < 2:
        return a, tiers

    # find NaN runs bounded by observed values
    i = 0
    while i < len(a):
        if np.isfinite(a[i]):
            i += 1
            continue
        j = i
        while j < len(a) and not np.isfinite(a[j]):
            j += 1
        run = j - i
        if i > 0 and j < len(a) and run <= max_gap:
            a[i:j] = np.interp(idx[i:j], [i - 1, j], [a[i - 1], a[j]])
            for t in range(i, j):
                tiers[t] = 1
        i = j
    return a, tiers


def imputation_quality(tiers: Sequence[ImputeTier]) -> dict:
    t = np.asarray(tiers)
    share_34 = float(np.mean((t == 3) | (t == 4))) if len(t) else 0.0
    limit = spec.MEASUREMENT["tier34_max_share"].value
    return {"tier34_share": share_34, "limit": limit,
            "verdict": "PRELIMINARY ONLY" if share_34 > limit else "acceptable"}


# ---------------------------------------------------------------------------
# Step 4 — min-max + boundary compression (eq 5.3)
# ---------------------------------------------------------------------------
def minmax(series: Sequence[float],
           x_min: Optional[float] = None,
           x_max: Optional[float] = None,
           rolling_window: Optional[int] = None) -> np.ndarray:
    """Within-country min-max to [0,1] (Part II eq 1).

    rolling_window: if set, X_max is a trailing-window max (Part II §1,
    'rolling thirty-year window maximum' when the polity may be at an
    all-time high).
    """
    a = np.asarray(series, dtype=float)
    if rolling_window:
        out = np.empty_like(a)
        for i in range(len(a)):
            lo = max(0, i - rolling_window + 1)
            win = a[lo:i + 1]
            wmin = np.nanmin(win) if x_min is None else x_min
            wmax = np.nanmax(win) if x_max is None else x_max
            out[i] = 0.0 if wmax == wmin else (a[i] - wmin) / (wmax - wmin)
        return out
    lo = np.nanmin(a) if x_min is None else x_min
    hi = np.nanmax(a) if x_max is None else x_max
    if hi == lo:
        return np.zeros_like(a)
    return (a - lo) / (hi - lo)


def compress(x: np.ndarray | float) -> np.ndarray | float:
    """X̂_compressed = 0.02 + 0.96·X̂_raw   (eq 5.3) — keeps Hill/θ well-posed."""
    lo = spec.MEASUREMENT["boundary_lo"].value
    span = spec.MEASUREMENT["boundary_span"].value
    return lo + span * np.asarray(x) if isinstance(x, (list, np.ndarray)) else lo + span * x


# ---------------------------------------------------------------------------
# Step 5 — Monte Carlo uncertainty propagation (eq 5.4)
# ---------------------------------------------------------------------------
@dataclass
class UncertainDelta:
    median_delta_norm: float
    ci80: Tuple[float, float]
    ci95: Tuple[float, float]
    regime_distribution: Dict[str, float]
    draws: int
    median_psi: float
    psi_ci80: Tuple[float, float]
    width80: float
    expected_width_note: str


def propagate(point: SubComponents,
              sigma: Dict[str, float],
              state_type: str = "liberal_democracy",
              params: Optional[dict] = None,
              draws: Optional[int] = None,
              seed: int = 0) -> UncertainDelta:
    """Monte Carlo propagation of proxy measurement error to Δ and Ψ.

    sigma: per-sub-component measurement SD in normalised units
           (e.g. {'s3': 0.08, 'c5': 0.05, ...}).
    """
    M = int(draws or spec.MEASUREMENT["mc_draws"].value)
    rng = np.random.default_rng(seed)
    keys = list(point.as_dict())

    deltas = np.empty(M)
    psis = np.empty(M)
    regimes: Dict[str, int] = {}

    for m in range(M):
        d = {}
        for k in keys:
            v = getattr(point, k) + rng.normal(0.0, sigma.get(k, 0.0))
            d[k] = float(min(max(v, 0.0), 1.0))
        cap: Capacity = compute(SubComponents(**d), state_type=state_type,
                                params=params, validate=False)
        deltas[m] = cap.delta_norm
        psis[m] = cap.psi
        regimes[cap.regime] = regimes.get(cap.regime, 0) + 1

    q = lambda a, p: float(np.percentile(a, p))
    ci80 = (q(deltas, 10), q(deltas, 90))
    return UncertainDelta(
        median_delta_norm=float(np.median(deltas)),
        ci80=ci80, ci95=(q(deltas, 2.5), q(deltas, 97.5)),
        regime_distribution={k: v / M for k, v in
                             sorted(regimes.items(), key=lambda kv: -kv[1])},
        draws=M,
        median_psi=float(np.median(psis)),
        psi_ci80=(q(psis, 10), q(psis, 90)),
        width80=ci80[1] - ci80[0],
        expected_width_note="Part III §5.5 expects 80% CI half-width of "
                            "±0.08–0.12 Δ units for OECD post-1970, "
                            "±0.15–0.25 for lower-quality data.",
    )

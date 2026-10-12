"""
SCCD Engine — Network Layer (Part IV §4-6)
===========================================
Multi-state extension: flow matrix F decomposed into four channels, network
equilibrium check, hegemon's balance condition, Thucydides Trap activation,
Global Coherence Index Ψ_G and global bifurcation risk R_B,G.

This is the layer that makes the engine useful for GOVERNMENT-level questions
that are inherently relational (hegemonic transition, capital flight,
alliance burden) rather than single-state diagnostics.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

import numpy as np

from . import spec


# ---------------------------------------------------------------------------
# Node description
# ---------------------------------------------------------------------------
@dataclass
class Node:
    code: str                  # "US", "CN", ...
    delta_norm: float
    psi: float
    cai: float
    c1: float
    c4: float
    s1: float
    s4: float
    c3: float
    weight: float = 1.0        # systemic weight w_i for Ψ_G and CAI_weighted
    opportunity: float = 0.0   # for talent channel
    ret: float = 0.0           # risk-adjusted return, for capital channel
    capital_controls: float = 0.0
    skilled_supply: float = 0.0


# ---------------------------------------------------------------------------
# Flow channels  — Part IV eq. (N.3)-(N.6)
# ---------------------------------------------------------------------------
def f_capital(i: Node, j: Node, p: Dict[str, float]) -> float:
    """F^capital = τ_cap·Ĉ₁,i·Ĉ₄,i·max(Return_j − Return_i,0)·(1 − controls_j)"""
    return (p["tau_cap"] * i.c1 * i.c4 * max(j.ret - i.ret, 0.0)
            * (1.0 - j.capital_controls))


def f_talent(i: Node, j: Node, p: Dict[str, float],
             language_transferability: float = 1.0) -> float:
    """F^talent = σ_lab·Skilled_Supply_i·max(Opp_j − Opp_i,0)·Lang_ij"""
    return (p["sigma_lab"] * i.skilled_supply
            * max(j.opportunity - i.opportunity, 0.0) * language_transferability)


def f_military(security_provision: float, strategic_value: float,
               tribute_rate: float = 0.0, c_j: float = 0.0,
               military_dominance: float = 0.0,
               subtype: str = "A") -> float:
    """F^military, Part IV eq (N.5).

    Type A — patron-client (hegemon PROVIDES security): outflow from i.
    Type B — extraction (imperial power EXTRACTS): inflow to i.
    """
    if subtype == "A":
        return security_provision * strategic_value
    if subtype == "B":
        return -tribute_rate * c_j * military_dominance
    raise ValueError("subtype must be 'A' or 'B'")


def f_information(i: Node, j: Node, p: Dict[str, float],
                  language_reach: float = 1.0, ideology_gap: float = 0.0,
                  platform_penetration: float = 1.0) -> float:
    """F^information = ι·C₃,i·Lang_ij·Ideology_Gap_ij·Platform_ij"""
    return p["iota"] * i.c3 * language_reach * ideology_gap * platform_penetration


def flow_matrix(nodes: Sequence[Node], p: Dict[str, float],
                military: Optional[Dict[tuple, float]] = None,
                lang: Optional[Dict[tuple, float]] = None,
                ideology: Optional[Dict[tuple, float]] = None) -> np.ndarray:
    """Assemble F_ij = F^cap + F^tal + F^mil + F^info, with F_ii = 0 (eq N.1-N.2)."""
    n = len(nodes)
    F = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            i, j = nodes[a], nodes[b]
            key = (i.code, j.code)
            lg = (lang or {}).get(key, 1.0)
            ig = (ideology or {}).get(key, 0.0)
            F[a, b] = (f_capital(i, j, p)
                       + f_talent(i, j, p, lg)
                       + (military or {}).get(key, 0.0)
                       + f_information(i, j, p, lg, ig))
    return F


def absorption(F: np.ndarray, nodes: Sequence[Node],
               eta_from_s4: bool = True) -> np.ndarray:
    """η_ji absorption efficiency (Part IV §4.1, note 3): increasing in Ŝ₄,j.

    Returns the η matrix applied to inflows.
    """
    n = len(nodes)
    H = np.ones((n, n))
    if eta_from_s4:
        for b in range(n):
            H[:, b] = nodes[b].s4     # simple linear form; paper leaves form open
    return H


# ---------------------------------------------------------------------------
# Hegemon's balance  — Part IV eq. (N.7)
# ---------------------------------------------------------------------------
def hegemon_balance(provision_cost: float, capital_inflow_premium: float,
                    delta_G_security: float, seigniorage: float) -> dict:
    """Viable iff (a)+(b)+(c) > Σ F^{mil,A}."""
    returns = capital_inflow_premium + delta_G_security + seigniorage
    return {"provision_cost": provision_cost, "returns": returns,
            "margin": returns - provision_cost,
            "viable": returns > provision_cost}


# ---------------------------------------------------------------------------
# Thucydides Trap  — Part IV eq. (TT.1)
# ---------------------------------------------------------------------------
def thucydides(delta_h: float, delta_c: float, d_gap_dt: float,
               sustained_years: float, p: Optional[dict] = None) -> dict:
    """T_trap = 1[δ_hc<δ_crit] · 1[dδ_hc/dt<−ε_speed] · 1[t_sustained>T_min]"""
    p = p or {}
    d_crit = p.get("delta_crit_tt", spec.NETWORK["delta_crit_tt"].value)
    eps = p.get("eps_speed", spec.NETWORK["eps_speed"].value)
    tmin = p.get("T_min", spec.NETWORK["T_min"].value)

    gap = delta_h - delta_c
    c1 = gap < d_crit
    c2 = d_gap_dt < -eps
    c3 = sustained_years > tmin
    return {"hegemonic_gap": gap, "T_trap": int(c1 and c2 and c3),
            "cond_gap_below_crit": c1, "cond_converging": c2,
            "cond_sustained": c3,
            "uncalibrated": True,
            "note": "ε_speed and T_min are FREE parameters (no values in paper); "
                    "δ_crit=0.25 is PAPER-calibrated from historical cases."}


# ---------------------------------------------------------------------------
# Global Coherence Index  — Part IV §6
# ---------------------------------------------------------------------------
def global_coherence(nodes: Sequence[Node], sync_risk: float) -> float:
    """Weighted global coherence, discounted by synchronisation risk.

    Part IV §6.1 specifies Ψ_G as a weighted aggregation of individual Ψ_i in
    which a systemically important state's low Ψ strongly depresses Ψ_G, and
    in which Sync_Risk further reduces it. The paper does not give the closed
    form, so the engine uses a weighted geometric mean × (1 − Sync_Risk),
    which satisfies both stated properties. FLAGGED UNCALIBRATED.
    """
    w = np.array([n.weight for n in nodes], dtype=float)
    psi = np.array([max(n.psi, 1e-9) for n in nodes], dtype=float)
    w = w / w.sum()
    geo = float(np.exp((w * np.log(psi)).sum()))
    return geo * (1.0 - sync_risk)


def global_bifurcation_risk(psi_G: float, t_trap: int,
                            nodes: Sequence[Node],
                            p: Optional[dict] = None) -> dict:
    """R_B,G = 1[Ψ_G<Ψ_G,crit] · 1[T_trap=1] · 1[CAI_weighted>CAI_G,crit]"""
    p = p or {}
    psi_crit = p.get("psi_G_crit", spec.NETWORK["psi_G_crit"].value)
    cai_crit = p.get("CAI_G_crit", spec.NETWORK["CAI_G_crit"].value)

    w = np.array([n.weight for n in nodes], dtype=float)
    w = w / w.sum()
    cai_w = float((w * np.array([n.cai for n in nodes])).sum())

    c1 = psi_G < psi_crit
    c2 = t_trap == 1
    c3 = cai_w > cai_crit
    return {"R_B_G": int(c1 and c2 and c3), "psi_G": psi_G,
            "CAI_weighted": cai_w,
            "cond_low_global_coherence": c1, "cond_trap": c2,
            "cond_compound_acceleration": c3,
            "interpretation": "R_B,G=1 identifies a structural condition "
                              "(overloaded-fault analogy), NOT a prediction of "
                              "a specific event or timeline (Part IV §6.3)."}


# Part IV eq. (G.2) — stated Sync_Risk trajectory, usable as a prior
SYNC_RISK_HISTORY = {1980: 0.12, 1995: 0.24, 2010: 0.41, 2024: 0.58}


def sync_risk_from_psi(psi_series_by_country: Dict[str, Sequence[float]],
                       window: int = 10) -> float:
    """Part IV note 5: average pairwise correlation of annual Ψ changes across
    states, on a rolling window."""
    codes = list(psi_series_by_country)
    if len(codes) < 2:
        return float("nan")
    diffs = {c: np.diff(np.asarray(psi_series_by_country[c], dtype=float))[-window:]
             for c in codes}
    cors = []
    for a in range(len(codes)):
        for b in range(a + 1, len(codes)):
            x, y = diffs[codes[a]], diffs[codes[b]]
            n = min(len(x), len(y))
            if n < 3:
                continue
            c = np.corrcoef(x[-n:], y[-n:])[0, 1]
            if np.isfinite(c):
                cors.append(c)
    return float(np.mean(cors)) if cors else float("nan")


def network_params() -> Dict[str, float]:
    return {k: v.value for k, v in spec.NETWORK.items()}

"""
SCCD Engine — Rule Specification  v1.00
========================================
Mirrors the versioned-rule-spec pattern of the Lục Hào engine: every constant
carries (a) its source equation in the paper, and (b) a STATUS flag.

STATUS flags
------------
PAPER   : numeric value stated explicitly in the paper → engine constant
DERIVED : computed from other PAPER values
FREE    : NO numeric value in the paper → must be estimated from data.
          Defaults here are placeholders only. Any output that depends on a
          FREE parameter is tagged UNCALIBRATED by the engine.

Source: Vi Nhat Son, "Sovereign-Civilian Capacity Dynamics", Parts I-V.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, Literal, Tuple

SPEC_VERSION = "1.00"

Status = Literal["PAPER", "DERIVED", "FREE"]


@dataclass(frozen=True)
class P:
    """A single parameter: value + provenance."""
    value: float
    status: Status
    eq: str
    note: str = ""

    def __float__(self) -> float:
        return float(self.value)


# ---------------------------------------------------------------------------
# 1. LEGITIMACY MULTIPLIER  λ(S₃)   — Part II eq. (2)-(3)
# ---------------------------------------------------------------------------
LAMBDA = {
    "lambda_min": P(0.30, "PAPER", "II.eq3", "floor: delegitimised state still 30% effective"),
    "lambda_max": P(2.50, "PAPER", "II.eq3", "ceiling: max legitimacy ~triples raw capacity"),
    "k":          P(2.50, "PAPER", "II.eq3", "Hill cooperativity; raise for polarised societies"),
    "s3_mid":     P(0.50, "PAPER", "II.eq3", "half-saturation point"),
}

# ---------------------------------------------------------------------------
# 2. THRESHOLD FUNCTION  θ₂₅  — Part II eq. (4), §2.2
# ---------------------------------------------------------------------------
THETA = {
    "s2_crit":  P(0.25, "PAPER", "II.§2.2", "non-state armed capacity ~1/4 of state"),
    "s5_crit":  P(0.15, "PAPER", "II.§2.2", "uncommitted revenue horizon < ~3 years"),
    "epsilon":  P(0.05, "FREE",  "II.eq4",  "smooth-Heaviside width; paper gives no value"),
}

# ---------------------------------------------------------------------------
# 3. S AGGREGATION WEIGHTS  — Part II eq. (5), Table 1
#    Constraint: w1 + w4 + omega25 = 1
# ---------------------------------------------------------------------------
STATE_TYPE_WEIGHTS: Dict[str, Tuple[float, float, float]] = {
    # state_type            : (w1 fiscal, w4 admin, omega25 threshold)
    "liberal_democracy":      (0.40, 0.35, 0.25),
    "developmental_autocracy": (0.35, 0.45, 0.20),
    "extractive_patrimonial": (0.50, 0.20, 0.30),
    "failed_state":           (0.60, 0.25, 0.15),
}
STATE_TYPE_WEIGHTS_STATUS: Status = "PAPER"  # Part II Table 1

# NOTE (engine-detected inconsistency #1):
# failed_state weights sum to 1.00 (0.60+0.25+0.15) OK;
# all four rows sum to 1.00. Constraint satisfied.

# ---------------------------------------------------------------------------
# 4. C AGGREGATION  — Part II eq. (6)-(8)
# ---------------------------------------------------------------------------
C_WEIGHTS = {
    "v1": P(0.35, "PAPER", "II.eq8", "private capital — highest weight"),
    "v2": P(0.25, "PAPER", "II.eq8", "civil organisation"),
    "v3": P(0.20, "PAPER", "II.eq8", "information autonomy"),
    "v4": P(0.20, "PAPER", "II.eq8", "exit availability"),
}
FRAGMENTATION = {
    "phi":       P(1.00, "FREE", "II.eq6", "fragmentation sensitivity — NO value in paper"),
    "psi":       P(1.50, "FREE", "II.eq6", "fragmentation exponent, ψ>=1 — NO value in paper"),
    "alpha_exit": P(0.50, "FREE", "II.eq7", "exit neutralisation fraction — NO value in paper"),
}

# Engine-detected inconsistency #2:
#   eq (6) writes Π(Ĉ1,Ĉ4,t) multiplying the ENTIRE Σ_j v_j Ĉ_j
#   eq (7) states "effective C₁ contribution = v₁·Ĉ₁·Π"  (Π applies to C₁ only)
# These are not equivalent. Engine implements eq (7) by default.
PI_SCOPE: Literal["c1_only", "whole_sum"] = "c1_only"

# ---------------------------------------------------------------------------
# 5. REGIME CLASSIFICATION  — Part II Table 2 (Δ_norm thresholds)
# ---------------------------------------------------------------------------
REGIME_BANDS = [
    # (name, lower_exclusive, upper_inclusive, stability)
    ("Imperial",    0.60,  1.00, "Unstable (drain)"),
    ("Hegemonic",   0.30,  0.60, "Metastable"),
    ("Negotiated",  0.08,  0.30, "Conditionally stable"),
    ("Equilibrium", -0.08, 0.08, "Stable or Gridlock"),
    ("Crisis",      -0.40, -0.08, "Unstable (bifurcation)"),
]
REGIME_BANDS_STATUS: Status = "PAPER"

# Engine-detected inconsistency #3:
#   Part I Table 1 gives Imperial (0.6,1.0] on a Δ scale normalised to (-1,1).
#   Part II Table 2 gives Imperial > 0.60 on Δ_norm = Δ/λ_max ∈ (-0.40,1.00).
#   The band EDGES coincide but the two stated ranges differ at the bottom
#   (-1.0 vs -0.40). Engine uses Part II (Δ_norm), which is dimensionally
#   consistent with eq (10).

# ---------------------------------------------------------------------------
# 6. COHERENCE & BIFURCATION  — Part II eq. (22)-(23)
# ---------------------------------------------------------------------------
COHERENCE = {
    "psi_crit":   P(0.40, "PAPER", "II.eq23", "coherence below which transition likely"),
    "delta_crit": P(-0.08, "PAPER", "II.eq23", "Crisis regime entry"),
    "delta_c":    P(0.05, "PAPER", "II.eq23", "min |dΔ/dt| per year for momentum condition"),
    "psi_min":    P(0.40, "DERIVED", "II.eq24", "taken = psi_crit; paper says 'Ψ_min' w/o value"),
}

# ---------------------------------------------------------------------------
# 7. CAPTURE FUNCTION Γ  — Part II eq. (15), Part IV App. A
# ---------------------------------------------------------------------------
CAPTURE = {
    "c1_crit": P(0.70, "PAPER", "II.§5.4", "capture threshold (0.70 of historical max)"),
    "beta":    P(2.00, "PAPER", "IV.AppA", "superlinearity exponent, baseline"),
    "gamma0":  P(0.30, "PAPER", "IV.AppA", "capture rate coefficient, baseline"),
    "mu":      P(0.50, "PAPER", "IV.AppA", "fraction of captured S landing in C₁"),
}

# ---------------------------------------------------------------------------
# 8. DRAIN / GENERATION / EXTRACTION  — Part II eq. (12)-(18)
#    Almost entirely FREE. This is the main calibration gap.
# ---------------------------------------------------------------------------
DYNAMICS = {
    # Drain D  (eq 13)
    "delta_p": P(0.030, "FREE", "II.eq13", "productive drain coefficient"),
    "delta_d": P(0.020, "FREE", "II.eq13", "distributional drain coefficient"),
    "delta_s": P(0.010, "FREE", "II.eq13", "spontaneous drain coefficient (>0 always)"),
    "policy":  P(1.000, "FREE", "II.eq13", "Policy(t) redistribution-vs-investment tilt"),
    # Generation G  (eq 12)
    "G_base":  P(0.015, "FREE", "II.eq12", "baseline surplus generation rate"),
    "g_tech":  P(1.000, "FREE", "II.eq12", "tech windfall scaling"),
    "g_war":   P(1.000, "FREE", "II.eq12", "war dividend scaling"),
    "tau_T":   P(10.0,  "FREE", "II.eq12", "tech shock decay time constant (yr)"),
    "tau_W":   P(8.0,   "FREE", "II.eq12", "war shock decay time constant (yr)"),
    # Civilian compound growth R  (eq 16)
    "r_cap":   P(0.040, "FREE", "II.eq16", "return on private capital"),
    "c1_max":  P(1.000, "FREE", "II.eq16", "carrying capacity of domestic private capital"),
    # Re-extraction T  (eq 17)
    "tau_max": P(0.200, "FREE", "II.eq17", "max effective extraction rate"),
    # Dissipation W  (eq 18)
    "omega_w": P(0.050, "FREE", "II.eq18", "civilian dissipation coefficient"),
    # Floors
    "s1_floor": P(0.05, "FREE", "IV.NL", "S₁ floor"),
    "s3_floor": P(0.05, "FREE", "IV.NL", "S₃ floor"),
}

# ---------------------------------------------------------------------------
# 9. FEEDBACK LOOPS L1-L4  — Part IV §2
# ---------------------------------------------------------------------------
LOOPS = {
    # L1 activation (Part IV §2.1): Ĉ₁>0.70 AND Ŝ₂<0.60
    "L1_c1_thresh": P(0.70, "PAPER", "IV.§2.1", ""),
    "L1_s2_thresh": P(0.60, "PAPER", "IV.§2.1", "state coercive capacity below which capture bites"),
    # L2 (Part IV §2.2): S₃<0.30 → λ≈0.50 explosive; also λ_crit≈0.80 (Part V)
    "L2_s3_thresh":     P(0.30, "PAPER", "IV.§2.2", ""),
    "L2_lambda_thresh": P(0.80, "PAPER", "V.V-US",  "critical λ for explosive L2"),
    "kappa":   P(0.05, "FREE", "IV.L2", "enforcement-cost drain coefficient"),
    "rho_b":   P(0.02, "FREE", "IV.L2", "coercion-backlash coefficient"),
    # L3 (Part IV §2.3)
    "epsilon_p": P(0.03, "FREE", "IV.L3", "political-entrepreneurship polarisation rate"),
    "eta_echo":  P(0.02, "FREE", "IV.L3", "echo-chamber amplification"),
    "zeta":      P(0.02, "FREE", "IV.L3", "policy-incoherence S₃ erosion"),
    "L3_c5_thresh":      P(0.50, "FREE", "IV.§2.3", "no explicit numeric threshold given"),
    "L3_revpol_thresh":  P(0.50, "FREE", "IV.§2.3", "no explicit numeric threshold given"),
    # L4 (Part IV §2.4)
    "chi": P(0.02, "FREE", "IV.L4", "exit-driven fiscal compression"),
    "xi":  P(0.02, "FREE", "IV.L4", "exit-driven C₅ increase"),
    "L4_c4_thresh": P(0.70, "FREE", "IV.§2.4", "inferred; paper states 'high C₄' qualitatively"),
    "L4_c1_thresh": P(0.70, "FREE", "IV.§2.4", "inferred from C₁,crit"),
}

# CAI bands — Part IV eq. (CAI)
CAI_BANDS = {
    "damped_max":   P(0.0, "PAPER", "IV.CAI", "CAI=0: linear dynamics"),
    "manageable":   P(2.0, "PAPER", "IV.CAI", "CAI in (0,2): 1-2 loops active"),
    "crisis_5_10y": P(3.0, "PAPER", "IV.CAI", "CAI in (2,3): crisis likely 5-10y"),
    # CAI > 3 : bifurcation imminent, 1-3y horizon
}
# Coupling_Weight_l and Loop_Speed_l in eq (CAI) have NO stated values.
LOOP_COUPLING_WEIGHT = {"L1": P(1.0, "FREE", "IV.CAI", ""),
                        "L2": P(1.0, "FREE", "IV.CAI", ""),
                        "L3": P(1.0, "FREE", "IV.CAI", ""),
                        "L4": P(1.0, "FREE", "IV.CAI", "")}
LOOP_SPEED = {"L1": P(1.0, "FREE", "IV.CAI", ""),
              "L2": P(1.0, "FREE", "IV.CAI", ""),
              "L3": P(1.0, "FREE", "IV.CAI", ""),
              "L4": P(1.0, "FREE", "IV.CAI", "")}

# ---------------------------------------------------------------------------
# 10. NETWORK  — Part IV §4-6
# ---------------------------------------------------------------------------
NETWORK = {
    "tau_cap":  P(0.05, "FREE", "IV.N3", "capital flow sensitivity"),
    "sigma_lab": P(0.03, "FREE", "IV.N4", "talent flow sensitivity"),
    "iota":     P(0.05, "FREE", "IV.N6", "information flow coefficient"),
    "delta_crit_tt": P(0.25, "PAPER", "IV.TT1", "hegemonic gap below which provision ROI<0"),
    "eps_speed": P(0.01, "FREE", "IV.TT1", "min convergence speed"),
    "T_min":     P(5.0,  "FREE", "IV.TT1", "min sustained convergence period (yr)"),
    "psi_G_crit": P(0.40, "PAPER", "IV.G3", "global coherence critical"),
    "CAI_G_crit": P(1.50, "PAPER", "IV.G3", "calibrated from interwar 1929-39"),
}

# ---------------------------------------------------------------------------
# 11. MEASUREMENT / NORMALISATION  — Part III §5
# ---------------------------------------------------------------------------
MEASUREMENT = {
    "boundary_lo":   P(0.02, "PAPER", "III.eq5.3", "compression: 0.02 + 0.96x"),
    "boundary_span": P(0.96, "PAPER", "III.eq5.3", ""),
    "cronbach_min":  P(0.65, "PAPER", "III.§5.2", "reject composite below this"),
    "mc_draws":      P(1000, "PAPER", "III.eq5.4", "Monte Carlo draws"),
    "interp_max_gap": P(3,   "PAPER", "III.§5.3", "Tier-1 linear interpolation max gap (yr)"),
    "rolling_max_window": P(30, "PAPER", "II.§1", "rolling window for X_max when at all-time high"),
    "tier34_max_share": P(0.30, "PAPER", "III.§5.3", ">30% imputed → preliminary only"),
}

# ---------------------------------------------------------------------------
# Sensitivity protocol — Part IV eq. (SA)
# ---------------------------------------------------------------------------
SENSITIVITY = {
    "oat_variation": P(0.20, "PAPER", "IV.SA", "±20% one-at-a-time on threshold params"),
    "lhs_draws":     P(10000, "PAPER", "IV.SA", "Latin Hypercube minimum draws"),
}

# ---------------------------------------------------------------------------
# ENGINE PATCH v1.01 — closes INC-7 and INC-8.
# These terms are NOT in the paper. They are the minimal additions that make
# the ODE system capable of representing the dynamics the paper itself
# describes in prose (depolarisation, legitimacy reconstitution).
# Enable with simulate(..., patch=True). Keep OFF to reproduce the paper
# exactly; keep ON for any usable trajectory.
# ---------------------------------------------------------------------------
PATCH_V101 = {
    "nu_depol":  P(0.030, "FREE", "PATCH/IV.§2.3",
                   "natural depolarisation: −ν·C₅·C₂ in dC₅/dt. Part IV §2.3 "
                   "names C₂ as the counterweight to L3 but omits the term."),
    "sigma_rec": P(0.040, "FREE", "PATCH/IV.§2.2",
                   "legitimacy recovery: +σ·(S₃_target − S₃) in dS₃/dt, driven "
                   "by demonstrated implementation (S₄). Part IV §2.2 names a "
                   "'natural legitimacy recovery rate' but omits the term."),
    "s3_target_gain": P(1.000, "FREE", "PATCH",
                        "maps S₄ performance to the S₃ attractor: "
                        "S₃_target = s3_target_gain · Ŝ₄"),
}
PATCH_ENABLED_BY_DEFAULT = False


# ---------------------------------------------------------------------------
# Audit helper
# ---------------------------------------------------------------------------
_ALL_GROUPS = {
    "lambda": LAMBDA, "theta": THETA, "c_weights": C_WEIGHTS,
    "fragmentation": FRAGMENTATION, "coherence": COHERENCE,
    "capture": CAPTURE, "dynamics": DYNAMICS, "loops": LOOPS,
    "cai_bands": CAI_BANDS, "loop_coupling": LOOP_COUPLING_WEIGHT,
    "loop_speed": LOOP_SPEED, "network": NETWORK,
    "measurement": MEASUREMENT, "sensitivity": SENSITIVITY,
    "patch_v101": PATCH_V101,
}


def audit() -> dict:
    """Count PAPER vs FREE parameters. Returns a report dict."""
    rows = []
    for group, d in _ALL_GROUPS.items():
        for name, p in d.items():
            # qualify names that repeat across groups (e.g. L1..L4 appear in
            # both loop_coupling and loop_speed)
            qual = name if group not in ("loop_coupling", "loop_speed") \
                else f"{group.split('_')[1]}_{name}"
            rows.append({"group": group, "name": qual, "status": p.status,
                         "eq": p.eq, "value": p.value, "note": p.note})
    counts: Dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return {"rows": rows, "counts": counts, "total": len(rows),
            "spec_version": SPEC_VERSION}


KNOWN_INCONSISTENCIES = [
    dict(id="INC-1", severity="low", where="Part II Table 1",
         issue="State-type weight rows all sum to 1.00 — constraint satisfied. No action."),
    dict(id="INC-2", severity="HIGH", where="Part II eq (6) vs eq (7)",
         issue="eq(6) applies the exit-adjustment Π to the entire Σ v_j Ĉ_j; "
               "eq(7) applies it to v₁·Ĉ₁ only. Not equivalent. "
               "Engine default = eq(7) (c1_only); switch via spec.PI_SCOPE."),
    dict(id="INC-3", severity="medium", where="Part I Table 1 vs Part II Table 2",
         issue="Part I states Δ normalised to (-1,1); Part II derives Δ_norm ∈ (-0.40,1.00). "
               "Band edges agree; lower bound does not. Engine uses Part II."),
    dict(id="INC-4", severity="medium", where="Part II §2.1 vs eq (3)",
         issue="Paper states λ(0.20)≈0.55 and λ(0.38)≈0.93, but eq(2) with the eq(3) "
               "parameters yields 0.502 and 1.037. λ(0.50)=1.40 matches exactly. "
               "Either the quoted examples use different k/mid, or they are approximations."),
    dict(id="INC-5", severity="HIGH", where="Part III §3.5 vs Part IV §2.3",
         issue="US C₅ in 2024 given as 0.72 (Part III, MFS) and 0.74 (Part IV §2.3 and "
               "Part V V.US). Small but the engine must pick one; defaults to 0.74 (Part V)."),
    dict(id="INC-6", severity="medium", where="Part III §3.5 vs Part IV §2.3",
         issue="US C₅ 1980 baseline given as 0.35 (Part III) and 0.28 (Part IV §2.3)."),
    dict(id="INC-7", severity="CRITICAL", where="Part IV eq (NL), dC₅/dt",
         issue="dC₅/dt = C₅_structural + ε_p·C₅(1−C₅)·Rev_Pol + η·C₅²·C₃ "
               "+ ξ·Ĉ₄Ĉ₁(1−C₅). ALL THREE endogenous terms are POSITIVE and "
               "there is no depolarisation term, even though §2.3 defines the "
               "L3 activation test against a 'Natural_Depolarisation_Rate'. "
               "As written, C₅ is monotonically increasing toward 1 for every "
               "trajectory, hence Ψ = λ·θ₂₅·(1−C₅) → 0 regardless of scenario. "
               "FIX: add −ν·C₅ (or −ν·C₅·C₂, since Part IV §2.3 names C₂ as "
               "'the primary counterweight to L3') to dC₅/dt."),
    dict(id="INC-8", severity="CRITICAL", where="Part IV eq (NL), dS₃/dt",
         issue="dS₃/dt = S₃_natural − ρ_b(1−λ/λmax)² − ζC₅^ψ(S₃−S₃floor). Both "
               "endogenous terms are NEGATIVE. With S₃_natural exogenous, S₃ "
               "can only decay, so the model cannot generate the legitimacy "
               "RECONSTITUTION that Part V §2.3 documents for 1980-86 "
               "(λ 1.2 → 1.7) or the 1941-45 build-up. Part IV §2.2 names a "
               "'natural legitimacy recovery' rate but it never enters the ODE. "
               "FIX: add a recovery term, e.g. +σ·(S₃_target(performance) − S₃), "
               "driven by S₄ implementation success."),
    dict(id="INC-9", severity="CRITICAL", where="Part IV §2.1 vs §7.1 state vector",
         issue="§2.1 writes the C₁ equation explicitly — 'dC₁/dt = v₁·D_drain→C₁ "
               "+ r(t)C₁(1−C₁/C₁max) − τ_eff·C₁ + μ·Γ' — but §7.1 (INT) lists "
               "the state variables as [S_i, C_i, S₃,i, C₅,i]: C₁ is OMITTED and "
               "treated as exogenous. Consequence: with C₁ exogenous, neither "
               "dS₃/dt nor dC₅/dt depends on S or C, so [S₃,C₅] is an AUTONOMOUS "
               "subsystem driving [S,C] one-way. There is NO closed feedback loop "
               "in eq (NL) at all — L1 and L4 are open, and the cross-coupling "
               "table of §2.4 is not implemented by the equations as written. "
               "Diagnostic: every scenario gives identical C₅(t) and Ψ(t). "
               "FIX: promote C₁ to a fifth state variable using §2.1's own "
               "equation. Engine: simulate(..., c1_dynamic=True)."),
]

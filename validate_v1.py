#!/usr/bin/env python3
"""
SCCD Engine — Validation against the paper's OWN stated numbers.

This is the "rà mâu thuẫn" pass: before trusting the engine, check that the
engine reproduces every number the paper asserts. Where it does not, the
discrepancy is reported with the arithmetic, so the rule can be fixed.
"""
from __future__ import annotations

import math
import sys

# --- UTF-8 console (a default Windows cp1252 console would otherwise abort on
#     the first Vietnamese or Greek character this script prints) ---
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):      # non-TTY or already wrapped
        pass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np

from sccd import spec, proxies
from sccd.aggregate import (SubComponents, compute, legitimacy_multiplier,
                            threshold_factor, coherence_index)
from sccd.engine import diagnose

OK, FAIL, WARN = "  PASS", "  FAIL", "  WARN"
results = []


def check(label, got, want, tol, note=""):
    ok = abs(got - want) <= tol
    results.append(ok)
    tag = OK if ok else FAIL
    print(f"{tag}  {label:<52} got {got:+.4f}  paper {want:+.4f}  "
          f"(tol ±{tol:g}){'  ' + note if note else ''}")
    return ok


print("=" * 88)
print("SCCD ENGINE VALIDATION   spec v%s" % spec.SPEC_VERSION)
print("=" * 88)

# ---------------------------------------------------------------------------
print("\n[1] LEGITIMACY MULTIPLIER λ(S₃) — Part II eq (2) with eq (3) parameters")
print("    λ = 0.30 + 2.20 · S₃^2.5 / (S₃^2.5 + 0.50^2.5)")
print("-" * 88)
check("λ(0.50) — paper §2.1 'achieves λ ≈ 1.40'", legitimacy_multiplier(0.50), 1.40, 0.005)
check("λ(0.20) — paper §2.1 'achieves λ ≈ 0.55'", legitimacy_multiplier(0.20), 0.55, 0.02)
check("λ(0.38) — paper Part V V.US 'λ ≈ 0.93'", legitimacy_multiplier(0.38), 0.93, 0.02)
check("λ(0.4317) — paper Part V 'λ ≈ 1.2 (1980)'", legitimacy_multiplier(0.4317), 1.20, 0.02)
check("λ(0.625)  — paper Part V 'λ ≈ 1.7 (1986)'", legitimacy_multiplier(0.625), 1.70, 0.02)

lam_ceiling = legitimacy_multiplier(1.0)
print(f"\n    λ CEILING TEST: S₃ = 1.0 (theoretical maximum) → λ = {lam_ceiling:.4f}")
print(f"    λ_max declared in eq (3) = {spec.LAMBDA['lambda_max'].value:.2f} "
      f"(an ASYMPTOTE, unreachable)")
print(f"    Paper asserts λ ≈ 2.3 for the US in 1945/1965 (Part V §2.1, §2.2).")
if 2.3 > lam_ceiling:
    print(f"{FAIL}  λ ≈ 2.3 is UNREACHABLE: max attainable λ = {lam_ceiling:.4f} at S₃ = 1.0")
    print(f"        → the Hill form caps λ at λ_min + (λ_max−λ_min)·1/(1+0.5^2.5)")
    print(f"        → = 0.30 + 2.20 × 0.8498 = {lam_ceiling:.4f}")
    print(f"        → FIX: either S₃,mid < 0.30, or k > 6, or λ_max ≈ 2.65+, "
          f"or restate the 1945 figure as ~2.17")
    results.append(False)

# ---------------------------------------------------------------------------
print("\n[2] COHERENCE INDEX Ψ — Part II eq (22):  Ψ = λ(S₃) · θ₂₅ · (1 − C₅)")
print("    Paper's own US-2024 inputs: S₃ = 0.38, C₅ = 0.74  (Part V V.US)")
print("-" * 88)
s3_us, c5_us = 0.38, 0.74
lam_us = legitimacy_multiplier(s3_us)
# US S₂ and S₅ are comfortably above their critical values → θ₂₅ ≈ 1
th_us = threshold_factor(0.90, 0.35)
psi_engine = coherence_index(lam_us, th_us, c5_us)
print(f"    λ(0.38)   = {lam_us:.4f}")
print(f"    θ₂₅       = {th_us:.6f}   (S₂=0.90 vs crit 0.25; S₅=0.35 vs crit 0.15)")
print(f"    (1 − C₅)  = {1 - c5_us:.4f}")
check("Ψ(US 2024) — paper Part V V.US 'Ψ ≈ 0.43'", psi_engine, 0.43, 0.03)

# Also with the paper's own quoted λ
psi_with_quoted_lam = 0.93 * th_us * (1 - c5_us)
print(f"\n    Using the paper's OWN quoted λ = 0.93 instead: Ψ = {psi_with_quoted_lam:.4f}")
print(f"    Still ≠ 0.43. The identity Ψ = λ·θ₂₅·(1−C₅) with θ₂₅ ≤ 1 and C₅ = 0.74")
print(f"    bounds Ψ ≤ λ × 0.26 = {0.93 * 0.26:.4f}. 0.43 is OUTSIDE this bound.")

# Back-solve what S₃ would be required
need_lam = 0.43 / (th_us * (1 - c5_us))
print(f"\n    BACK-SOLVE: to get Ψ = 0.43 at C₅ = 0.74 you need λ = {need_lam:.4f}")
if need_lam < lam_ceiling:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if legitimacy_multiplier(mid) < need_lam:
            lo = mid
        else:
            hi = mid
    print(f"                → which requires S₃ = {hi:.4f}, not the stated 0.38")
else:
    print(f"                → UNREACHABLE at any S₃ (ceiling {lam_ceiling:.4f})")

# Alternatively, back-solve C₅ holding S₃ = 0.38
need_1mc5 = 0.43 / (lam_us * th_us)
print(f"    BACK-SOLVE: to get Ψ = 0.43 at S₃ = 0.38 you need (1−C₅) = {need_1mc5:.4f}")
print(f"                → C₅ = {1 - need_1mc5:.4f}, not the stated 0.74")

print(f"\n    CONSEQUENCE — this is not cosmetic. Ψ_crit = 0.40 (eq 23).")
print(f"      Paper's Ψ = 0.43  → 'marginally ABOVE critical' → R_B = 0 → no bifurcation flag")
print(f"      Engine's Ψ = {psi_engine:.3f} → BELOW critical → R_B = 1 if dΔ/dt < −0.05")
print(f"      The headline structural verdict FLIPS on this single arithmetic point.")

# ---------------------------------------------------------------------------
print("\n[3] LOOP ACTIVATION — Part IV §2, Part V (V.US) for the US in 2024")
print("-" * 88)
us24 = SubComponents(
    s1=0.30,   # NDRR compressed: mandatory+debt service >70% of revenue (Part I §3.2)
    s2=0.90,   # advanced democracy: TCAI near 1 by default (Part III §2.2)
    s3=0.38,   # PAPER (Part V V.US)
    s4=0.50,   # high technical capacity, low implementation fidelity (Part I §3.2)
    s5=0.35,   # debt accumulation + T_horizon ≈ 4-6 yr (Part III §2.5)
    c1=0.82,   # PAPER
    c2=0.40,   # PAPER (Part IV §2.3: 'US C₂ from 0.68 in 1965 to 0.40 in 2024')
    c3=0.90,   # 'near theoretical maximum' (Part III §3.3)
    c4=0.86,   # PAPER
    c5=0.74,   # PAPER
)
d = diagnose("United States", 2024, us24,
             state_type="liberal_democracy",
             revenue_polarisation=0.78,   # PAPER (Part V V.US)
             d_delta_dt=-0.006,           # Δ fell ~0.74 over 84 yr ⇒ mean ≈ −0.009/yr
             g_shock=0.0,
             sigma={"s1": .06, "s2": .05, "s3": .10, "s4": .07, "s5": .07,
                    "c1": .05, "c2": .08, "c3": .04, "c4": .06, "c5": .06},
             mc_draws=2000)
print(d.summary())

print("\n    Paper's claimed values vs engine, same inputs:")
check("    L1 active (Ĉ₁=0.82 > 0.70)", float(d.loop_diagnosis.loops["L1"].active), 1.0, 0.5,
      "paper: ACTIVE above threshold")
check("    CAI", d.loop_diagnosis.cai, 2.1, 0.6, "paper: CAI ≈ 2.1")
check("    Δ_norm", d.capacity.delta_norm, -0.02, 0.10, "paper: Δ ≈ −0.02")

print(f"\n    NOTE on L1: the paper's own §2.1 threshold is 'Ĉ₁ > 0.70 AND Ŝ₂ < 0.60'.")
print(f"    US Ŝ₂ ≈ 0.90 (advanced democracy, TCAI → 1), so the CONJUNCTION FAILS")
print(f"    even though Ĉ₁ = 0.82 clears its threshold. Part V nonetheless calls L1")
print(f"    'ACTIVE above threshold' using the Ĉ₁ condition alone.")
print(f"    → INCONSISTENCY: Part IV §2.1 (joint condition) vs Part V V.US (C₁ only).")
print(f"    → Engine implements the joint condition (Part IV, the formal statement).")

# ---------------------------------------------------------------------------
print("\n[4] US 1945 IMPERIAL APEX — Part V §2.1 asserts Δ ≈ 0.72")
print("-" * 88)
us45 = SubComponents(
    s1=0.95, s2=0.98, s3=0.95, s4=0.90, s5=0.95,
    c1=0.25,   # Depression destroyed private capital (Part V §2.1)
    c2=0.35,   # New Deal partially subordinated civil orgs
    c3=0.30,   # three-network era, state-adjacent info environment
    c4=0.10,   # Bretton Woods capital controls; minimal exit
    c5=0.10,   # 'near historical minimum due to wartime unity'
)
cap45 = compute(us45)
print(f"    S = {cap45.S:.4f}   C = {cap45.C:.4f}   Δ = {cap45.delta:+.4f}   "
      f"Δ_norm = {cap45.delta_norm:+.4f}")
print(f"    λ = {cap45.lam:.4f}  (paper asserts λ ≈ 2.3; ceiling is {lam_ceiling:.3f})")
print(f"    regime = {cap45.regime}")
check("    Δ_norm(US 1945) — paper 'Δ ≈ 0.72'", cap45.delta_norm, 0.72, 0.08)

# ---------------------------------------------------------------------------
print("\n[5] PARAMETER SPECIFICATION AUDIT")
print("-" * 88)
a = spec.audit()
tot = a["total"]
for st in ("PAPER", "DERIVED", "FREE"):
    n = a["counts"].get(st, 0)
    print(f"    {st:<8} {n:>3} / {tot}   ({n/tot:5.1%})")
print()
free = [r for r in a["rows"] if r["status"] == "FREE"]
print(f"    The {len(free)} FREE parameters (no numeric value anywhere in Parts I-V):")
for r in free:
    print(f"      · {r['name']:<22} {r['eq']:<12} {r['note'][:48]}")

# ---------------------------------------------------------------------------
print("\n[6] WHICH OUTPUTS ARE CALIBRATED?")
print("-" * 88)
print("    CALIBRATED (PAPER params only) — usable as-is:")
print("      λ(S₃), θ₂₅, S, regime bands, Ψ, L1/L2 activation, R_B, Γ, Ĉ₁,crit")
print("    UNCALIBRATED (depends on ≥1 FREE param) — scenario-relative only:")
print("      C (needs φ, ψ, α_exit)  →  therefore Δ and Δ_norm too")
print("      L3/L4 activation (needs ε_p, η, χ, ξ, natural rates)")
print("      CAI (needs Coupling_Weight, Loop_Speed)")
print("      every ODE trajectory (needs δ_p, δ_d, δ_s, G_base, r, τ_max, ω, κ, ρ_b, ζ)")
print("      Ψ_G, T_trap timing, attractor selection")

# ---------------------------------------------------------------------------
print("\n[7] API READINESS OF THE TEN-COMPONENT INPUT VECTOR")
print("-" * 88)
r = proxies.api_readiness()
print(f"    {r['automatable_primary']} of {r['total']} primary proxies are fetchable "
      f"without manual work.")
print(f"    AUTO:    {', '.join(r['automatable_keys'])}")
print(f"    BLOCKED: {', '.join(r['blocked_keys'])}\n")
for row in r["rows"]:
    mark = "AUTO" if row["primary_automatable"] else "BLOCKED"
    print(f"    [{mark:>7}] {row['component']:<42} quality={row['quality']}")
    for b in row["blockers"]:
        print(f"              ✗ HARD BLOCKER: {b[:92]}")
    for dg in row["degraded"]:
        print(f"              ~ degraded without: {dg[:92]}")

blocked = set(r["blocked_keys"])
hinges = {"s3", "c5"}
print(f"\n    STRUCTURAL OBSERVATION:")
print(f"    The model's two NON-LINEAR HINGES are S₃ (the λ multiplier, which")
print(f"    scales everything) and C₅ (the fragmentation denominator).")
if hinges & blocked:
    print(f"    Both of those are in the BLOCKED set: {sorted(hinges & blocked)}.")
    print(f"    → The parts of the ten-vector that are easy to automate are the")
    print(f"      LINEAR, additive ones (S₁, S₅, C₁, C₄). The parts that drive the")
    print(f"      non-linearity — and therefore the regime calls — are the ones")
    print(f"      with no machine-readable source. This is the single biggest")
    print(f"      practical obstacle to an API-fed SCCD engine.")

print("\n" + "=" * 88)
print(f"RESULT: {sum(results)} passed / {len(results)} checks")
print("=" * 88)
print("\nKNOWN INCONSISTENCIES REGISTERED IN spec.py:")
for inc in spec.KNOWN_INCONSISTENCIES:
    print(f"  [{inc['severity']:>6}] {inc['id']} {inc['where']}")
    print(f"           {inc['issue']}")

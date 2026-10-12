"""
SCCD Engine
===========
A modular forecasting/diagnostic engine built from Vi Nhat Son,
"Sovereign-Civilian Capacity Dynamics" (Parts I-V).

Layer map
---------
  spec       rule/parameter specification, versioned (v1.00)
  proxies    Part III — the API seam: 10 latent components → data sources
  normalize  Part III §5 — standardise, merge, impute, compress, Monte Carlo
  aggregate  Part II eq. 1-10 — the deterministic core (S, C, Δ, λ, θ₂₅, Ψ)
  loops      Part IV §2 — L1-L4 activation, cross-coupling, CAI
  dynamics   Part II eq. 11-18 + Part IV eq. NL — four-state stiff ODE
  network    Part IV §4-6 — flow matrix, hegemon balance, Thucydides, Ψ_G
  engine     orchestrator + report
"""
from .spec import SPEC_VERSION, audit, KNOWN_INCONSISTENCIES
from .aggregate import (SubComponents, Capacity, compute,
                        legitimacy_multiplier, threshold_factor,
                        coherence_index, classify_regime)
from .engine import diagnose, Diagnosis
from . import spec, proxies, normalize, aggregate, loops, dynamics, network, engine

__version__ = SPEC_VERSION

__all__ = [
    "SPEC_VERSION", "__version__", "audit", "KNOWN_INCONSISTENCIES",
    "SubComponents", "Capacity", "compute", "legitimacy_multiplier",
    "threshold_factor", "coherence_index", "classify_regime",
    "diagnose", "Diagnosis",
    "spec", "proxies", "normalize", "aggregate", "loops", "dynamics",
    "network", "engine",
]

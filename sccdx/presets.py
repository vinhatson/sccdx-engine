# -*- coding: utf-8 -*-
"""
SCCD-X — Baseline Presets, 2026
================================
Starting values so the API and the form are usable immediately.

READ THIS BEFORE USING ANY NUMBER BELOW
---------------------------------------
With ONE exception these are ANALYST PRIORS. They are not measurements, they
were not produced by running sccd's Part III proxy pipeline, and they have no
confidence interval. They exist so the form opens with something plausible in
every box rather than 0.5 everywhere.

The exception is the United States, where the source papers state values
directly and the engine uses them:
    S3 = 0.38    sccd Part V, V-US
    C5 = 0.74    sccd Part IV 2.3 and Part V (Part III 3.5 says 0.72 - sccd
                 spec INC-5 flags the discrepancy; 0.74 is taken, per spec)
    C1 = 0.82    sccd Part IV 2.1
    S2 ~ 0.90    sccd Part IV 2.1, from the L1 condition discussion
Those four carry tag PAPER. Everything else on the US row, and every value on
every other row, is tagged ANALYST.

To replace a row with measured values, run sccd.proxies / sccd.normalize over
the data sources listed in sccd.proxies and feed the result in through the API
instead. Note sccd's own api_readiness(): 7 of 10 components are machine-
retrievable, and the three that are NOT - S3 legitimacy, S4 administrative
penetration, C5 fragmentation - are precisely the ones that drive lambda, S
and the C denominator. The blocked components are the decisive ones. That is
not an accident of this preset file; it is the structural data problem sccd
Part III 5 documents.

The Block D and Block A values are weaker still: no proxy pipeline exists for
them at all, in either new paper. They are reasoned guesses from public
knowledge of each polity's demography and AI adoption as of early 2026.
"""
from __future__ import annotations

from typing import Dict, List

from sccd.aggregate import SubComponents
from .forcing import DemoBlock, DispBlock
from .world import PolityInput


def _p(code, name, state_type, weight, sub, demo, disp, *,
       revenue_polarisation=0.0, security_pressure=0.0,
       base_revenue_demand=0.0, ret=0.0, opportunity=0.0,
       capital_controls=0.0, skilled_supply=0.0,
       provenance="ANALYST prior", confidence="low", rationale="") -> dict:
    return dict(code=code, name=name, state_type=state_type, weight=weight,
                sub=sub, demo=demo, disp=disp,
                revenue_polarisation=revenue_polarisation,
                security_pressure=security_pressure,
                base_revenue_demand=base_revenue_demand,
                ret=ret, opportunity=opportunity,
                capital_controls=capital_controls,
                skilled_supply=skilled_supply,
                provenance=provenance, confidence=confidence,
                rationale=rationale)


# ---------------------------------------------------------------------------
# sub:  s1 fiscal, s2 coercive monopoly, s3 legitimacy, s4 admin depth,
#       s5 temporal leverage, c1 capital concentration, c2 civil org,
#       c3 info autonomy, c4 exit options, c5 fragmentation (INHIBITOR)
# demo: d1 load, d2 expectation trap, d3 adjustment autonomy (ROUTER),
#       d4 dependency inversion, d5 surplus youth
# disp: a1 AI penetration, a2 self-efficacy erosion, a3 agency erosion,
#       a4 haven reallocation, a5 counter-tech, a6 AI windfall
# ---------------------------------------------------------------------------
PRESETS_2026: List[dict] = [

    _p("US", "United States", "liberal_democracy", 1.00,
       SubComponents(s1=0.55, s2=0.90, s3=0.38, s4=0.62, s5=0.30,
                     c1=0.82, c2=0.55, c3=0.60, c4=0.72, c5=0.74),
       DemoBlock(d1=0.62, d2=0.78, d3=0.82, d4=0.58, d5=0.22),
       DispBlock(a1=0.80, a2=0.62, a3=0.58, a4=0.62, a5=0.22, a6=0.68,
                 luxury_contraction=0.55),
       revenue_polarisation=0.62, security_pressure=0.45,
       base_revenue_demand=0.085, ret=0.055, opportunity=0.80,
       skilled_supply=0.70,
       provenance="MIXED: s3/c5/c1/s2 are PAPER (sccd Part IV-V); all else "
                  "ANALYST",
       confidence="medium",
       rationale="The only row with any paper-stated values. Note sccd's own "
                 "validation finds Psi(US 2024) = 0.265 against the paper's "
                 "stated 0.43 - with theta25 <= 1 and C5 = 0.74 the identity "
                 "Psi = lambda*theta25*(1-C5) caps Psi at 0.24 using the "
                 "paper's own lambda = 0.93, so 0.43 is outside its own "
                 "bound. The engine reports the computed value and the "
                 "conclusion inverts: R_B can arm where the paper says it "
                 "cannot."),

    _p("CN", "China", "developmental_autocracy", 0.95,
       SubComponents(s1=0.60, s2=0.88, s3=0.55, s4=0.82, s5=0.38,
                     c1=0.68, c2=0.22, c3=0.20, c4=0.28, c5=0.42),
       DemoBlock(d1=0.72, d2=0.80, d3=0.76, d4=0.56, d5=0.34),
       DispBlock(a1=0.70, a2=0.52, a3=0.44, a4=0.58, a5=0.12, a6=0.62,
                 luxury_contraction=0.70),
       revenue_polarisation=0.25, security_pressure=0.50,
       base_revenue_demand=0.080, ret=0.045, opportunity=0.55,
       skilled_supply=0.60, capital_controls=0.70,
       rationale="High s4 and s2, low c2/c3/c4 by construction of the state "
                 "type. d4 set near the US despite a far younger recent past "
                 "because the inversion is arriving faster. luxury "
                 "contraction set highest of any row: the Displacement paper "
                 "locates the sharpest attrition and the 'luxury shame' "
                 "phenomenon here specifically."),

    _p("EU", "European Union (bloc)", "liberal_democracy", 0.85,
       SubComponents(s1=0.58, s2=0.72, s3=0.50, s4=0.70, s5=0.32,
                     c1=0.66, c2=0.68, c3=0.72, c4=0.70, c5=0.58),
       DemoBlock(d1=0.60, d2=0.74, d3=0.86, d4=0.68, d5=0.26),
       DispBlock(a1=0.62, a2=0.50, a3=0.46, a4=0.52, a5=0.34, a6=0.46,
                 luxury_contraction=0.48),
       revenue_polarisation=0.45, security_pressure=0.55,
       base_revenue_demand=0.090, ret=0.035, opportunity=0.62,
       skilled_supply=0.62,
       rationale="Treated as one polity, which is a real distortion: the "
                 "bloc has no single s2 or s3 and its c5 is partly "
                 "between-member rather than within-member. Split it into "
                 "member states if the question is about internal "
                 "fragmentation. Highest a5 of the large polities - the "
                 "counter-tech counterweight is strongest here."),

    _p("JP", "Japan", "liberal_democracy", 0.45,
       SubComponents(s1=0.48, s2=0.78, s3=0.58, s4=0.80, s5=0.18,
                     c1=0.58, c2=0.52, c3=0.62, c4=0.55, c5=0.38),
       DemoBlock(d1=0.58, d2=0.72, d3=0.90, d4=0.88, d5=0.14),
       DispBlock(a1=0.60, a2=0.46, a3=0.40, a4=0.50, a5=0.30, a6=0.52,
                 luxury_contraction=0.40),
       revenue_polarisation=0.22, security_pressure=0.45,
       base_revenue_demand=0.095, ret=0.030, opportunity=0.55,
       skilled_supply=0.50,
       rationale="The purest test of Degrow's voluntary terminus: d4 = 0.88 "
                 "and s5 = 0.18, already within 0.03 of theta25's PAPER gate "
                 "at 0.15. If the S5 mechanism in Block D is right at all, it "
                 "should show here first and most clearly. Note the "
                 "counterpoint the engine must not hide: Japan has sat near "
                 "this gate for two decades without the collapse the gate is "
                 "supposed to mark, which is evidence against compress_s5 "
                 "being as large as spec2 sets it."),

    _p("KR", "South Korea", "liberal_democracy", 0.30,
       SubComponents(s1=0.56, s2=0.76, s3=0.44, s4=0.76, s5=0.30,
                     c1=0.76, c2=0.50, c3=0.64, c4=0.58, c5=0.66),
       DemoBlock(d1=0.66, d2=0.92, d3=0.92, d4=0.62, d5=0.20),
       DispBlock(a1=0.76, a2=0.60, a3=0.52, a4=0.54, a5=0.18, a6=0.64,
                 luxury_contraction=0.52),
       revenue_polarisation=0.58, security_pressure=0.60,
       base_revenue_demand=0.075, ret=0.045, opportunity=0.60,
       skilled_supply=0.58,
       rationale="d2 = 0.92, the highest expectation trap in the set - "
                 "housing, private education and the hours culture together. "
                 "Degrow names Seoul explicitly as its modern case. Highest "
                 "d3 alongside JP, so loop L7 should be armed."),

    _p("IN", "India", "developmental_autocracy", 0.60,
       SubComponents(s1=0.34, s2=0.70, s3=0.56, s4=0.48, s5=0.34,
                     c1=0.70, c2=0.48, c3=0.44, c4=0.40, c5=0.70),
       DemoBlock(d1=0.78, d2=0.62, d3=0.52, d4=0.20, d5=0.62),
       DispBlock(a1=0.48, a2=0.40, a3=0.30, a4=0.56, a5=0.10, a6=0.44,
                 luxury_contraction=0.20),
       revenue_polarisation=0.50, security_pressure=0.50,
       base_revenue_demand=0.055, ret=0.060, opportunity=0.38,
       skilled_supply=0.68, capital_controls=0.45,
       rationale="d3 = 0.52 sits right at the router's midpoint, so pressure "
                 "splits roughly evenly down both of Degrow's channels - the "
                 "only row in the set that does. a4 is high for its income "
                 "level because household gold holding is structural here "
                 "rather than a 2023-26 reallocation, which is a genuine "
                 "measurement problem for Block A: the variable is meant to "
                 "capture a SHIFT, not a stock."),

    _p("RU", "Russia", "extractive_patrimonial", 0.40,
       SubComponents(s1=0.46, s2=0.84, s3=0.48, s4=0.56, s5=0.26,
                     c1=0.84, c2=0.18, c3=0.18, c4=0.22, c5=0.46),
       DemoBlock(d1=0.64, d2=0.66, d3=0.72, d4=0.62, d5=0.30),
       DispBlock(a1=0.44, a2=0.36, a3=0.30, a4=0.68, a5=0.08, a6=0.32,
                 luxury_contraction=0.60),
       revenue_polarisation=0.30, security_pressure=0.85,
       base_revenue_demand=0.105, ret=0.040, opportunity=0.30,
       skilled_supply=0.42, capital_controls=0.80,
       rationale="c1 = 0.84 with s2 = 0.84: capture is extreme but the "
                 "coercive monopoly is intact, so sccd's L1 does NOT arm - "
                 "its condition is Ĉ1 > 0.70 AND Ŝ2 < 0.60, both required. "
                 "Highest a4 in the set and highest capital controls, which "
                 "is exactly the OP2-4 configuration: jurisdiction exit shut, "
                 "asset-form exit wide open."),

    _p("BR", "Brazil", "liberal_democracy", 0.30,
       SubComponents(s1=0.42, s2=0.52, s3=0.46, s4=0.52, s5=0.28,
                     c1=0.74, c2=0.54, c3=0.58, c4=0.48, c5=0.72),
       DemoBlock(d1=0.68, d2=0.64, d3=0.68, d4=0.34, d5=0.52),
       DispBlock(a1=0.46, a2=0.38, a3=0.32, a4=0.46, a5=0.12, a6=0.36,
                 luxury_contraction=0.30),
       revenue_polarisation=0.62, security_pressure=0.55,
       base_revenue_demand=0.070, ret=0.065, opportunity=0.35,
       skilled_supply=0.40,
       rationale="s2 = 0.52, below sccd's L1 threshold of 0.60, with c1 = "
                 "0.74 above C1,crit = 0.70. Both PAPER conditions met, so "
                 "L1 arms here and not in Russia. c5 = 0.72 near the US "
                 "level. The MIXED adjustment mode row."),

    _p("GB", "United Kingdom", "liberal_democracy", 0.28,
       SubComponents(s1=0.50, s2=0.74, s3=0.44, s4=0.64, s5=0.22,
                     c1=0.78, c2=0.58, c3=0.68, c4=0.76, c5=0.64),
       DemoBlock(d1=0.64, d2=0.82, d3=0.84, d4=0.64, d5=0.24),
       DispBlock(a1=0.72, a2=0.56, a3=0.52, a4=0.56, a5=0.26, a6=0.56,
                 luxury_contraction=0.50),
       revenue_polarisation=0.52, security_pressure=0.45,
       base_revenue_demand=0.092, ret=0.040, opportunity=0.58,
       skilled_supply=0.60,
       rationale="Highest c4 in the set - an open capital account and an "
                 "English-language emigration option - combined with s5 = "
                 "0.22. That pairing is the sharpest L6 configuration: "
                 "revenue demand high, legible base mobile."),

    _p("NG", "Nigeria", "failed_state", 0.18,
       SubComponents(s1=0.22, s2=0.42, s3=0.34, s4=0.28, s5=0.24,
                     c1=0.62, c2=0.42, c3=0.46, c4=0.34, c5=0.70),
       DemoBlock(d1=0.84, d2=0.52, d3=0.24, d4=0.10, d5=0.86),
       DispBlock(a1=0.20, a2=0.16, a3=0.14, a4=0.38, a5=0.04, a6=0.14,
                 luxury_contraction=0.10),
       revenue_polarisation=0.48, security_pressure=0.78,
       base_revenue_demand=0.045, ret=0.070, opportunity=0.18,
       skilled_supply=0.30,
       rationale="The row that makes the engine honest. d5 = 0.86 with d3 = "
                 "0.24 is Degrow's ancient channel, undiluted, and loop L8 "
                 "exists for exactly this case. Without it the instrument "
                 "would read the whole young half of the world as 'quiet' "
                 "simply because L5-L7 are all rich-aging-society loops. "
                 "s2 = 0.42 is already within 0.17 of theta25's 0.25 PAPER "
                 "gate, by the violent door rather than the fiscal one."),
]

BY_CODE: Dict[str, dict] = {p["code"]: p for p in PRESETS_2026}


def preset_polities(codes: List[str] | None = None) -> List[PolityInput]:
    """Build PolityInput objects from the presets."""
    want = codes or list(BY_CODE)
    out: List[PolityInput] = []
    for c in want:
        if c not in BY_CODE:
            raise ValueError(f"unknown preset code {c!r}; "
                             f"have {sorted(BY_CODE)}")
        d = dict(BY_CODE[c])
        d.pop("rationale", None)
        out.append(PolityInput(**d))
    return out


def preset_json() -> dict:
    """Serialisable form for the API and the web form."""
    return {
        "year": 2026,
        "polities": [
            {"code": p["code"], "name": p["name"],
             "state_type": p["state_type"], "weight": p["weight"],
             "sub": p["sub"].as_dict(), "demo": p["demo"].as_dict(),
             "disp": p["disp"].as_dict(),
             "revenue_polarisation": p["revenue_polarisation"],
             "security_pressure": p["security_pressure"],
             "base_revenue_demand": p["base_revenue_demand"],
             "ret": p["ret"], "opportunity": p["opportunity"],
             "capital_controls": p["capital_controls"],
             "skilled_supply": p["skilled_supply"],
             "provenance": p["provenance"], "confidence": p["confidence"],
             "rationale": p.get("rationale", "")}
            for p in PRESETS_2026],
        "disclaimer": (
            "ANALYST PRIORS, not measurements. Only four values in the whole "
            "file are paper-stated: US s3=0.38, c5=0.74, c1=0.82, s2~0.90. "
            "Nothing here was produced by running sccd's Part III proxy "
            "pipeline, and no value has a confidence interval. Replace rows "
            "with measured inputs before quoting any result."),
    }

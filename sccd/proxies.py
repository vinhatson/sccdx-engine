"""
SCCD Engine — Proxy / Data-Ingestion Layer (Part III)
======================================================
This is THE API SEAM. Each of the ten latent sub-components maps to a primary
proxy formula plus secondary proxies, and each proxy maps to one or more named
data sources with an explicit ACCESS MODE.

ACCESS modes
------------
API        : live programmatic endpoint, no key or free key
API_KEY    : live endpoint, registration required
BULK       : bulk file download (CSV/XLSX/Stata), machine-readable, no API
BULK_REG   : bulk download behind registration
MANUAL     : published only as PDF/report → requires human or LLM extraction
COMMERCIAL : paid licence required
CODING     : no dataset exists; requires original manual coding by the analyst

The engine refuses to emit a calibrated Δ for any country-year where a
sub-component's proxies are all MANUAL/CODING/missing — it emits the value
flagged instead. This is the discipline that keeps the output honest.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Literal, Optional

Access = Literal["API", "API_KEY", "BULK", "BULK_REG", "MANUAL", "COMMERCIAL", "CODING"]
Quality = Literal["High", "Med-High", "Medium", "Low-Medium", "Low"]


@dataclass
class Source:
    name: str
    access: Access
    endpoint: str = ""
    coverage: str = ""
    note: str = ""
    verify: bool = True    # endpoint should be re-checked before production use
    required: bool = True  # False = the proxy can be built without it
                           # (degraded quality, per an explicit paper fallback
                           #  or an available substitute source)
    substitute: str = ""   # what stands in when a required source is missing


@dataclass
class Proxy:
    code: str                  # e.g. "P.1"
    name: str                  # e.g. "Net Discretionary Revenue Ratio"
    abbr: str                  # e.g. "NDRR"
    formula: str
    sources: List[Source]
    role: Literal["primary", "secondary"] = "primary"
    reliability: float = 1.0   # r_k in Part III eq (5.2); relative weight


@dataclass
class Component:
    key: str                   # s1..s5, c1..c5
    label: str
    construct: str
    quality: Quality
    proxies: List[Proxy]
    inhibitor: bool = False    # True only for C₅
    warning: str = ""

    def access_profile(self) -> Dict[str, int]:
        prof: Dict[str, int] = {}
        for px in self.proxies:
            for s in px.sources:
                prof[s.access] = prof.get(s.access, 0) + 1
        return prof

    MACHINE = ("API", "API_KEY", "BULK", "BULK_REG")

    def automatable(self) -> bool:
        """True iff every REQUIRED source of every primary proxy is
        machine-accessible. A required MANUAL/CODING/COMMERCIAL source blocks
        the component — that is the honest test, because the proxy formula
        cannot be evaluated without its inputs."""
        prim = [p for p in self.proxies if p.role == "primary"]
        if not prim:
            return False
        for p in prim:
            for s in p.sources:
                if s.required and s.access not in Component.MACHINE:
                    return False
        return True

    def degraded(self) -> List[str]:
        """Sources marked optional — automatable only at reduced quality."""
        return [f"{s.name} ({s.access})" + (f" → {s.substitute}" if s.substitute else "")
                for p in self.proxies if p.role == "primary"
                for s in p.sources
                if not s.required and s.access not in Component.MACHINE]

    def blockers(self) -> List[str]:
        return [f"{s.name} ({s.access}): {s.note or 'no machine source'}"
                for p in self.proxies if p.role == "primary"
                for s in p.sources
                if s.required and s.access not in Component.MACHINE]


# ===========================================================================
# S COMPONENTS  — Part III §2
# ===========================================================================
S1 = Component(
    key="s1", label="S₁ — Fiscal Extraction Capacity", quality="High",
    construct="Ability to convert economic activity into deployable finance "
              "in excess of mandatory commitments.",
    proxies=[
        Proxy("P.1", "Net Discretionary Revenue Ratio", "NDRR",
              "(Total_Revenue − Mandatory_Spending − Debt_Service) / GDP",
              [Source("IMF Fiscal Monitor / IMF Data", "API",
                      "https://www.imf.org/external/datamapper/api/v1/",
                      "189 countries, 1990–present",
                      "Mandatory-vs-discretionary split is NOT in the feed — "
                      "requires manual classification per Part III §2.1"),
               Source("OECD Revenue Statistics", "API",
                      "OECD SDMX-JSON / stats API", "38 OECD members, 1965–",
                      "advanced economies only", required=False,
                      substitute="IMF Fiscal Monitor covers non-OECD")],
              reliability=0.65),
        Proxy("P.1b", "Tax effort gap", "TEG",
              "(actual tax/GDP − IMF estimated tax capacity) / capacity",
              [Source("IMF tax capacity estimates", "MANUAL", "",
                      "", "published in staff papers, not a dataset")],
              role="secondary", reliability=0.20),
        Proxy("P.1c", "Bond market confidence spread", "BMCS",
              "inverted, normalised 10y sovereign spread over risk-free",
              [Source("BIS / national treasuries / FRED", "API",
                      "https://api.stlouisfed.org/fred/ (key)", "varies")],
              role="secondary", reliability=0.15),
    ],
)

S2 = Component(
    key="s2", label="S₂ — Coercive Monopoly Index", quality="Medium",
    construct="Asymmetry between state coercive capacity and the maximum "
              "capacity of any non-state armed actor.",
    proxies=[
        Proxy("P.2", "Territorial Control Asymmetry Index", "TCAI",
              "1 − Max_NonState_Armed_Capacity / State_Military_Capacity",
              [Source("UCDP Conflict Database", "API",
                      "https://ucdpapi.pcr.uu.se/api/", "all states, 1946–",
                      "under-reports low-level non-state violence"),
               Source("SIPRI Military Expenditure", "BULK",
                      "SIPRI milex database (XLSX)", "170+ countries, 1949–",
                      "expenditure ≠ effectiveness; no non-state benchmark"),
               Source("Fragile States Index (security sub-score)", "BULK",
                      "Fund for Peace FSI data", "178 countries, 2006–",
                      "composite partly circular with the construct"),
               Source("World Bank WGI Rule of Law", "API",
                      "https://api.worldbank.org/v2/", "215 countries, 1996–")],
              reliability=0.60),
        Proxy("P.2b", "Private military contractor share", "PMCS",
              "PMC spending / total defence budget",
              [Source("national budget documents", "CODING")],
              role="secondary", reliability=0.20),
        Proxy("P.2c", "Organised crime territorial penetration", "OCTP",
              "Global Organised Crime Index territorial control sub-score",
              [Source("Global Organized Crime Index", "BULK",
                      "ocindex.net data download", "193 countries, 2021–")],
              role="secondary", reliability=0.20),
    ],
)

S3 = Component(
    key="s3", label="S₃ — Legitimacy Capital", quality="Medium",
    construct="Degree to which state directives receive voluntary compliance; "
              "enters the model as the Hill multiplier λ.",
    warning="HIGHEST-RISK PROXY IN THE FRAMEWORK (Part III §2.3 Measurement "
            "Warning). All proxies measure downstream consequences of "
            "legitimacy, not legitimacy. Single-proxy implementations are "
            "strongly discouraged. Widen CIs on anything λ-dependent.",
    proxies=[
        Proxy("P.3", "Four-Pillar Legitimacy Index", "4PLI",
              "¼·(L_vol + L_bond + L_comply + L_elite)",
              # The four pillars are the inputs; the binding ones are listed
              # here because 4PLI cannot be evaluated without them.
              [Source("BIS debt securities (L_bond)", "API",
                      "https://stats.bis.org/api/", "reporting countries"),
               Source("World Bank migration (L_elite)", "API",
                      "https://api.worldbank.org/v2/"),
               Source("military enlistment bonus / conscription evasion (L_vol)",
                      "CODING", "", "",
                      "Part III P.4: bonus-to-GDP-per-capita. Published for the "
                      "US only; most states publish neither bonuses nor "
                      "conscription-evasion rates. NO substitute dataset."),
               Source("tax gap estimates (L_comply)", "MANUAL", "", "",
                      "IRS/HMRC publish as periodic PDF reports; IMF TADAT is "
                      "per-country, not a panel. No cross-national series.",
                      required=False,
                      substitute="WVS tax-morale item (BULK_REG, irregular waves)")],
              reliability=0.60),
        Proxy("P.4", "Voluntary Compliance Pillar", "L_vol",
              "1 − Military_Enlistment_Bonus_USD / GDP_per_capita",
              [Source("national defence recruitment data", "CODING", "",
                      "", "US: DoD; most countries: not published"),
               Source("WVS / Edelman / Gallup institutional trust", "BULK_REG",
                      "worldvaluessurvey.org (reg.)", "irregular waves",
                      "Edelman is MANUAL (PDF); Gallup World Poll is COMMERCIAL")],
              role="secondary", reliability=0.25),
        Proxy("P.5", "Bond Market Trust Pillar", "L_bond",
              "Domestic_Holdings_GovBonds / Total_Gov_Debt_Outstanding",
              [Source("BIS debt securities statistics", "API",
                      "https://stats.bis.org/api/", "reporting countries"),
               Source("national treasury holder data", "BULK")],
              role="secondary", reliability=0.25),
        Proxy("P.6", "Tax Compliance Pillar", "L_comply",
              "1 − Tax_Gap / Potential_Revenue",
              [Source("IRS Tax Gap (US)", "MANUAL", "", "periodic", "PDF reports"),
               Source("HMRC Tax Gap (UK)", "BULK"),
               Source("IMF TADAT assessments", "MANUAL", "",
                      "", "country reports; not a panel")],
              role="secondary", reliability=0.20),
        Proxy("P.7", "Elite Alignment Pillar", "L_elite",
              "1 − Elite_Emigration_Rate × Capital_Flight_Index",
              [Source("OECD DIOC", "BULK", "", "OECD destinations"),
               Source("World Bank migration data", "API",
                      "https://api.worldbank.org/v2/"),
               Source("Global Financial Integrity", "MANUAL", "", "", "reports"),
               Source("BIS banking statistics (residual method)", "API",
                      "https://stats.bis.org/api/")],
              role="secondary", reliability=0.20),
    ],
)

S4 = Component(
    key="s4", label="S₄ — Administrative Penetration Depth", quality="Med-High",
    construct="Ability to translate political intention into implemented "
              "outcomes — effective implementation, not technical capability.",
    proxies=[
        Proxy("P.8", "Policy Implementation Fidelity Index", "PIFI",
              "WGI_GovtEffectiveness × (Implemented_Policies / Enacted_Policies)",
              [Source("World Bank WGI Government Effectiveness", "API",
                      "https://api.worldbank.org/v2/", "215 countries, 1996–",
                      "conflates capacity with orientation"),
               Source("policy implementation ratio", "CODING", "",
                      "", "Part III §2.4: 'requires manual coding for historical "
                          "cases'. THIS IS THE BINDING CONSTRAINT ON S₄.")],
              reliability=0.60),
        Proxy("P.8b", "Bureaucratic quality score", "ICRG-BQ",
              "ICRG political risk bureaucratic quality sub-component",
              [Source("PRS Group ICRG", "COMMERCIAL", "", "140 countries, 1984–")],
              role="secondary", reliability=0.20),
        Proxy("P.8c", "Public service delivery outcomes", "PSDO",
              "actual / income-expected delivery on core services",
              [Source("World Bank WDI", "API", "https://api.worldbank.org/v2/")],
              role="secondary", reliability=0.20),
    ],
)

S5 = Component(
    key="s5", label="S₅ — Temporal Leverage", quality="Medium",
    construct="Ability to make credible long-horizon commitments and draw on "
              "future resources.",
    proxies=[
        Proxy("P.9", "Fiscal Temporal Capacity Index", "FTCI",
              "1 − Net_Debt / (Uncommitted_Revenue × T_horizon)",
              [Source("IMF Fiscal Monitor / WEO", "API",
                      "https://www.imf.org/external/datamapper/api/v1/"),
               Source("senior civil service tenure records (T_horizon)", "CODING", "",
                      "", "Part III §2.5: 'not systematically available "
                          "cross-nationally'", required=False,
                      substitute="fiscal component only (NetDebt/Uncommitted_Rev) — "
                                 "the paper's own explicit fallback, lower quality")],
              reliability=0.60),
        Proxy("P.9b", "Long-term bond issuance share", "LTBIS",
              "share of sovereign debt with maturity > 10y",
              [Source("BIS debt securities", "API", "https://stats.bis.org/api/")],
              role="secondary", reliability=0.25),
        Proxy("P.9c", "Infrastructure investment horizon", "IIH",
              "budget-weighted mean design life of state projects",
              [Source("national infrastructure plans", "CODING")],
              role="secondary", reliability=0.15),
    ],
)

# ===========================================================================
# C COMPONENTS  — Part III §3
# ===========================================================================
C1 = Component(
    key="c1", label="C₁ — Private Capital Concentration", quality="High",
    construct="Politically activated private capital, not mere inequality.",
    warning="Wealth-share component is High quality; political-activation "
            "factor is Low-Medium and available only for advanced democracies.",
    proxies=[
        Proxy("P.10", "Politically Active Capital Index", "PACI",
              "(Top1%_WealthShare / GDP) × Political_Activation_Factor,  PAF ∈ [0.3,1.0]",
              [Source("WID.world (Piketty et al.)", "BULK",
                      "wid.world bulk download / R+Stata packages",
                      "70+ countries, 1900–", "coverage thins pre-1960 non-West"),
               Source("OpenSecrets (US lobbying)", "API_KEY",
                      "https://www.opensecrets.org/api/", "US only",
                      required=False, substitute="PAF floor of 0.3 where no "
                                                 "lobbying register exists"),
               Source("EU Transparency Register", "API",
                      "ec.europa.eu transparency register", "EU",
                      required=False),
               Source("revolving-door rates", "CODING", "", "",
                      "systematic only for US/UK/EU", required=False,
                      substitute="PAF from lobbying+campaign finance only "
                                 "(2 of 3 terms), quality drops to Low")],
              reliability=0.70),
    ],
)

C2 = Component(
    key="c2", label="C₂ — Civil Organization Density", quality="Med-High",
    construct="Density AND collective-action effectiveness of non-state "
              "organisation — not organisational count.",
    proxies=[
        Proxy("P.11", "Effective Civil Society Index", "ECSI",
              "V-Dem_CSO_Participation × (1 − Repression_Index) × Coordination_Effectiveness",
              [Source("V-Dem Project", "BULK",
                      "v-dem.net dataset / vdemdata R package",
                      "202 countries, 1789–",
                      "ordinal codings need IRT scaling for cardinal use"),
               Source("GDELT protest database", "API",
                      "https://api.gdeltproject.org/api/v2/doc/doc "
                      "(also BigQuery gdelt-bq)", "post-1979",
                      "Coordination_Effectiveness = successful/initiated "
                      "collective actions — requires an event-classification "
                      "pipeline on top of raw GDELT")],
              reliability=0.65),
    ],
)

C3 = Component(
    key="c3", label="C₃ — Information Autonomy", quality="High",
    construct="Civilian ability to produce, distribute and act on information "
              "independently of the state.",
    proxies=[
        Proxy("P.12", "Information Autonomy Score", "IAS",
              "(1 − State_Media_Share) × Press_Freedom_Score × (1 − Internet_Censorship_Index)",
              [Source("RSF Press Freedom Index", "BULK",
                      "rsf.org/en/index data", "180 countries, 2002–"),
               Source("Freedom House (Freedom on the Net / Media)", "BULK",
                      "freedomhouse.org data downloads"),
               Source("OONI", "API", "https://api.ooni.io/", "global, 2012–"),
               Source("V-Dem media indicators", "BULK",
                      "v-dem.net (government media censorship, media bias, "
                      "print/broadcast censorship)", "202 countries, 1789–",
                      "stands in for State_Media_Share"),
               Source("Reuters Institute Digital News Report", "MANUAL", "", "",
                      "PDF; state media share needs extraction", required=False,
                      substitute="V-Dem media indicators (listed above)")],
              reliability=0.70),
    ],
)

C4 = Component(
    key="c4", label="C₄ — Exit Option Availability", quality="High",
    construct="Ability of mobile capital, skilled labour and IP to leave the "
              "jurisdiction. Highly asymmetric across asset classes.",
    proxies=[
        Proxy("P.13", "Jurisdictional Exit Capability Index", "JECI",
              "0.50·Ĉ₄,capital + 0.30·Ĉ₄,labour + 0.20·Ĉ₄,IP",
              [Source("Chinn-Ito Index (KAOPEN)", "BULK",
                      "web.pdx.edu/~ito/Chinn-Ito_website.htm",
                      "182 countries, 1970–", "static file, annual update"),
               Source("OECD DIOC (skilled emigration)", "BULK"),
               Source("visa-free access scores", "BULK", "",
                      "", "e.g. Henley/IATA-derived datasets"),
               Source("WIPO IP statistics", "API",
                      "WIPO IP Statistics Data Center", "",
                      "IP jurisdiction-shopping index requires construction; "
                      "Part III rates this component Low quality, post-2000 only",
                      required=False,
                      substitute="drop the w_ip term and renormalise "
                                 "w_cap/w_lab to 0.625/0.375")],
              reliability=0.70),
    ],
)

C5 = Component(
    key="c5", label="C₅ — Preference Fragmentation Index", quality="Med-High",
    inhibitor=True,
    construct="Degree of fragmentation in preferences, information "
              "environments and political identities. INHIBITOR — enters the "
              "C aggregation as a denominator.",
    proxies=[
        Proxy("P.14", "Multidimensional Fragmentation Score", "MFS",
              "⅓·(P_legislative + P_media + P_social)",
              [Source("DW-NOMINATE / Voteview (US)", "API",
                      "https://voteview.com/api/ (also CSV downloads)",
                      "US Congress 1789–", "US-specific"),
               Source("CHES (Chapel Hill Expert Survey)", "BULK",
                      "chesdata.eu", "EU parties, 1999–"),
               Source("ParlGov", "BULK", "parlgov.org", "37 democracies"),
               Source("World Values Survey (social trust)", "BULK_REG",
                      "worldvaluessurvey.org", "irregular waves"),
               Source("Eurobarometer / Afrobarometer", "BULK_REG"),
               Source("Reuters Institute / Comscore (audience overlap)",
                      "MANUAL", "", "",
                      "P_media: audience-overlap Gini is NOT systematically "
                      "cross-national. Binding constraint on C₅ outside the US/EU.")],
              reliability=0.65),
    ],
)

REGISTRY: Dict[str, Component] = {
    c.key: c for c in (S1, S2, S3, S4, S5, C1, C2, C3, C4, C5)
}


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------
def api_readiness() -> dict:
    """How much of the ten-component vector can be fetched automatically."""
    rows = []
    for key, comp in REGISTRY.items():
        rows.append({
            "key": key,
            "component": comp.label,
            "quality": comp.quality,
            "primary_automatable": comp.automatable(),
            "n_sources": sum(comp.access_profile().values()),
            "access_profile": comp.access_profile(),
            "blockers": comp.blockers(),
            "degraded": comp.degraded(),
            "warning": comp.warning,
        })
    auto = [r for r in rows if r["primary_automatable"]]
    return {"rows": rows,
            "automatable_primary": len(auto),
            "automatable_keys": [r["key"] for r in auto],
            "blocked_keys": [r["key"] for r in rows if not r["primary_automatable"]],
            "degraded_keys": [r["key"] for r in rows if r["degraded"]],
            "total": len(rows)}


def all_sources() -> List[dict]:
    seen = {}
    for comp in REGISTRY.values():
        for px in comp.proxies:
            for s in px.sources:
                if s.name not in seen:
                    seen[s.name] = {"name": s.name, "access": s.access,
                                    "endpoint": s.endpoint, "used_by": []}
                seen[s.name]["used_by"].append(comp.key)
    return sorted(seen.values(), key=lambda r: (r["access"], r["name"]))

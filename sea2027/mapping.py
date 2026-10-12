# -*- coding: utf-8 -*-
"""
sea2027.mapping - measured panel -> SCCD-X v2.00 inputs
========================================================
Every formula below is written out so a reader can disagree with a weight
rather than with a black box. Each returns (value, tag, terms) where `terms`
lists what went in, so audit() can print the whole derivation.

Tags
  MEASURED  every term came from a dated observation in raw_2026.RAW
  MIXED     a measured composite shifted or gated by a JUDGMENT term
  ANALYST   no usable series exists; the number is argued in judgment.py

Band edges in nz(x, lo, hi) are the plausible CROSS-NATIONAL range of each
series, not the observed range of these eleven. Using the local range would
pin the regional extremes at 0 and 1 by construction and make the region look
more differentiated than it is.

The LEVEL vs DRIFT rule of spec2 applies downstream, not here: this module
produces LEVELS for all ten sccd components and all eleven block inputs, and
sccdx.forcing decides which of them may take a level shift and which may only
take a drift.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from sccd.aggregate import SubComponents
from sccd.normalize import compress
from sccdx.forcing import DemoBlock, DispBlock
from sccdx.world import PolityInput

from raw_2026 import RAW
from judgment import JUDGMENT

CODES = ["BN", "KH", "ID", "LA", "MY", "MM", "PH", "SG", "TH", "TL", "VN"]
NAMES = {"BN": "Brunei Darussalam", "KH": "Cambodia", "ID": "Indonesia",
         "LA": "Lao PDR", "MY": "Malaysia", "MM": "Myanmar",
         "PH": "Philippines", "SG": "Singapore", "TH": "Thailand",
         "TL": "Timor-Leste", "VN": "Viet Nam"}


def nz(x, lo, hi) -> float:
    v = (float(x) - lo) / (hi - lo)
    return 0.0 if v < 0.0 else (1.0 if v > 1.0 else v)


def cl(x) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else float(x))


# ---------------------------------------------------------------------------
# FILL - measured series missing for a given polity. (value, reason)
# ---------------------------------------------------------------------------
FILL: Dict[str, Dict[str, Tuple[float, str]]] = {
 "BN": {
  "gg_rev": (26.0, "no IMF WEO revenue row; oil-and-gas receipts have run "
                   "~25-30% of GDP through the 2020s"),
  "gg_exp": (28.0, "chronic post-2015 deficits on a ~26% revenue base"),
  "gini": (33.0, "no published Gini; rentier distribution with universal "
                 "subsidies, assumed mid-range"),
  "contra_mod": (60.0, "no DHS/MICS series"),
  "socprot_cov": (90.0, "universal state provision, no income tax"),
  "vdem_civsoc": (0.10, "absent from V-Dem: absolute monarchy under a state "
                        "of emergency continuous since 1962, no elected "
                        "legislature, no legal parties"),
  "vdem_freeexpr": (0.12, "absent from V-Dem; sedition and SPA restrictions"),
  "vdem_freeassoc": (0.10, "absent from V-Dem"),
  "vdem_corrupt": (0.30, "absent from V-Dem; WGI control of corruption at "
                         "the 68th percentile is strong for the income class"),
  "vdem_rol": (0.65, "absent from V-Dem; WGI rule of law 70th percentile"),
  "kaopen": (0.85, "absent from Chinn-Ito; currency board with the SGD under "
                   "the 1967 Interchangeability Agreement, no material "
                   "capital restrictions"),
  "rd_gdp": (0.28, "no series"),
  "slums": (21.6, "WDI 2022 observation is present; kept for symmetry"),
 },
 "SG": {
  "gg_rev": (19.0, "no IMF WEO row; MOF operating revenue ~17-18% of GDP "
                   "plus the NIRC contribution"),
  "gg_exp": (19.5, "balanced-budget rule across an electoral term"),
  "gini": (37.0, "SingStat household-income Gini before transfers; not in WDI"),
  "contra_mod": (72.0, "no recent WDI observation"),
  "socprot_cov": (95.0, "CPF is near-universal for residents"),
 },
 "LA": {
  "gg_rev": (15.5, "no IMF WEO row; the post-2023 VAT and excise reform "
                   "lifted revenue off its 2021 trough"),
  "gg_exp": (16.0, "the 2026 Article IV holds the primary balance positive by "
                   "compressing spending, not by raising revenue"),
 },
 "TL": {
  "gg_rev": (21.6, "WDI tax_gdp 2022. The Petroleum Fund transfer, not "
                   "domestic tax, funds ~80% of the budget, so this both "
                   "overstates extraction CAPACITY and understates current "
                   "resources - both errors are live"),
  "gg_exp": (60.0, "expenditure runs far above domestic revenue, financed by "
                   "Fund withdrawals above the ESI"),
  "kaopen": (0.42, "no Chinn-Ito observation; fully dollarised with no "
                   "exchange restrictions but a very thin financial sector"),
  "pension_cov": (3.0, "no series; veterans' and old-age transfers are near "
                       "universal but are not a contributory pension"),
 },
 "MM": {
  "gg_rev": (15.6, "IMF WEO 2024. The 2019 WDI tax figure of 6.0% is the "
                   "last pre-coup observation and is not usable"),
  "gg_exp": (20.67, "IMF WEO 2024"),
 },
 "ID": {"gg_rev": (14.55, "IMF WEO 2024"),
        "gg_exp": (16.84, "IMF WEO 2024")},
 "VN": {"gg_rev": (17.58, "IMF WEO 2024"),
        "gg_exp": (19.12, "IMF WEO 2024")},
 "KH": {"gg_rev": (14.58, "IMF WEO 2024"),
        "gg_exp": (17.26, "IMF WEO 2024"),
        "gini": (30.5, "no WDI observation in the 2012-2026 window; the last "
                       "CSES-based estimates sit around 30, which is almost "
                       "certainly a floor - consumption Ginis understate "
                       "concentration badly where the top of the "
                       "distribution is informal")},
 "MY": {"gg_rev": (19.91, "IMF WEO 2024"),
        "gg_exp": (23.86, "IMF WEO 2024")},
 "PH": {"gg_rev": (21.16, "IMF WEO 2024"),
        "gg_exp": (24.94, "IMF WEO 2024")},
 "TH": {"gg_rev": (21.42, "IMF WEO 2024"),
        "gg_exp": (22.71, "IMF WEO 2024")},
}


def g(c: str, key: str, default=None):
    r = RAW[c].get(key)
    if r is not None:
        return r[1]
    f = FILL.get(c, {}).get(key)
    if f is not None:
        return f[0]
    if default is not None:
        return default
    raise KeyError(f"{c}.{key}: no observation and no FILL entry")


def imf(c: str, key: str, default=None):
    v = RAW[c].get(key)
    if v is None:
        if default is None:
            raise KeyError(f"{c}.{key}")
        return default
    return v


def is_measured(c: str, key: str) -> bool:
    return RAW[c].get(key) is not None


def _tag(c: str, keys: List[str], analyst: bool = False) -> str:
    if analyst:
        return "ANALYST"
    if all(is_measured(c, k) for k in keys):
        return "MEASURED"
    return "MIXED"


# ===========================================================================
# S COMPONENTS
# ===========================================================================
def s1_fiscal(c):
    """S1 Fiscal Extraction Capacity - sccd P.1 NDRR analogue.

    NDRR wants (revenue - mandatory - debt service)/GDP. The mandatory split
    is not in any feed for these eleven, so the construct is approximated as
    a revenue level discounted by the debt stock and gated by regulatory
    quality (the state's ability to actually collect what it levies).
    """
    rev = g(c, "gg_rev")
    debt = imf(c, "gg_debt_2026")
    rq = g(c, "wgi_rq")
    terms = {"gg_rev": rev, "gg_debt_2026": debt, "wgi_rq": rq}
    v = (0.50 * nz(rev, 10, 30)
         + 0.25 * (1 - nz(debt, 20, 110))
         + 0.25 * nz(rq, 20, 95))
    return cl(v), _tag(c, ["wgi_rq"]) if is_measured(c, "gg_rev") else "MIXED", terms


def s2_coercive(c):
    """S2 Coercive Monopoly - sccd P.2 TCAI. The conflict term is ANALYST
    because UCDP is now behind an access token, so every row is MIXED."""
    j = JUDGMENT[c]
    pv, rl = g(c, "wgi_pv"), g(c, "wgi_rl")
    terms = {"wgi_pv": pv, "wgi_rl": rl, "conflict(ANALYST)": j["conflict"]}
    v = (0.45 * nz(pv, 10, 95)
         + 0.25 * nz(rl, 20, 90)
         + 0.30 * (1 - j["conflict"]))
    return cl(v), "MIXED", terms


def s3_legitimacy(c):
    """S3 Legitimacy Capital - sccd's HIGHEST-RISK proxy, and BLOCKED: P.4
    L_vol has no cross-national source at all and P.6 L_comply has no panel.
    What is used instead is a four-term stand-in - delivery, integrity, order,
    and the inverse of household exit - minus an ANALYST drawdown for
    legitimacy events later than the 2025 vintage of WGI and V-Dem.

    Every value this function returns is MIXED at best. sccd Part III's own
    measurement warning applies in full: widen the interval on anything
    lambda-dependent."""
    j = JUDGMENT[c]
    ge, pv = g(c, "wgi_ge"), g(c, "wgi_pv")
    corrupt = g(c, "vdem_corrupt")
    terms = {"wgi_ge": ge, "vdem_corrupt": corrupt, "wgi_pv": pv,
             "haven(ANALYST)": j["haven"], "unrest(ANALYST)": j["unrest"]}
    base = (0.30 * nz(ge, 15, 95)
            + 0.30 * (1 - corrupt)
            + 0.20 * nz(pv, 10, 95)
            + 0.20 * (1 - j["haven"]))
    # The drawdown is PROPORTIONAL, not subtractive. An absolute subtraction
    # is not scale-consistent: the composite is low across the whole region
    # because V-Dem's political-corruption index is high for most of it, so a
    # flat -0.30 drove the Philippines to within 0.04 of Myanmar, which is not
    # a reading anyone would defend. Multiplying says what is meant - this
    # share of the polity's legitimacy capital has been drawn down by events
    # later than the measurement vintage - and cannot reach zero.
    v = base * (1.0 - j["unrest"])
    terms["base_before_drawdown"] = round(base, 4)
    return cl(v), "MIXED", terms


def s4_admin(c):
    """S4 Administrative Penetration - sccd P.8 PIFI. The implemented/enacted
    policy ratio is CODING-only, so WGI government effectiveness carries the
    construct, with three delivery outcomes behind it."""
    ge = g(c, "wgi_ge")
    elec, sp, sl = g(c, "elec"), g(c, "socprot_cov"), g(c, "slums")
    terms = {"wgi_ge": ge, "elec": elec, "socprot_cov": sp, "slums": sl}
    v = (0.50 * nz(ge, 15, 95)
         + 0.20 * nz(elec, 78, 100)
         + 0.15 * nz(sp, 2, 95)
         + 0.15 * (1 - nz(sl, 0, 60)))
    return cl(v), _tag(c, ["wgi_ge", "elec", "socprot_cov", "slums"]), terms


def s5_temporal(c):
    """S5 Temporal Leverage - sccd P.9 FTCI, fiscal-component-only fallback
    (the paper's own explicit degraded form; the T_horizon term needs senior
    civil-service tenure records, which exist for nobody here).

    Note the LEVEL vs DRIFT trap documented in spec2: a measured S5 already
    nets out existing pre-commitment. The `pension` judgment term is NOT
    subtracted here - it feeds Block D's d4, which supplies a DRIFT. Charging
    it in both places would double count."""
    debt = imf(c, "gg_debt_2026")
    bal = imf(c, "gg_bal_2026")
    dep = g(c, "dep_old")
    infl = imf(c, "pcpipch_2026")
    terms = {"gg_debt_2026": debt, "gg_bal_2026": bal, "dep_old": dep,
             "pcpipch_2026": infl}
    v = (0.45 * (1 - nz(debt, 20, 110))
         + 0.25 * nz(bal, -6, 3)
         + 0.20 * (1 - nz(dep, 7, 25))
         + 0.10 * (1 - nz(infl, 0, 20)))
    return cl(v), "MEASURED", terms


# ===========================================================================
# C COMPONENTS
# ===========================================================================
def c1_capital(c):
    """C1 Private Capital Concentration - sccd P.10 PACI. WID top-1% wealth
    share is not available for nine of the eleven, so the Gini stands in for
    the wealth term (a known downward bias: income inequality understates
    wealth concentration), and the political-activation factor is the
    `crony` judgment plus V-Dem's political-corruption index."""
    j = JUDGMENT[c]
    gini, corrupt = g(c, "gini"), g(c, "vdem_corrupt")
    terms = {"gini": gini, "crony(ANALYST)": j["crony"],
             "vdem_corrupt": corrupt}
    v = 0.35 * nz(gini, 28, 45) + 0.40 * j["crony"] + 0.25 * corrupt
    return cl(v), "MIXED", terms


def c2_civil(c):
    """C2 Civil Organization Density - sccd P.11 ECSI. V-Dem supplies the
    participation and association terms; the coordination-effectiveness term
    needs an event-classification pipeline over GDELT, so it is ANALYST."""
    j = JUDGMENT[c]
    cs, fa = g(c, "vdem_civsoc"), g(c, "vdem_freeassoc")
    terms = {"vdem_civsoc": cs, "vdem_freeassoc": fa,
             "protest(ANALYST)": j["protest"]}
    v = 0.55 * cs + 0.30 * fa + 0.15 * j["protest"]
    return cl(v), "MIXED", terms


def c3_info(c):
    """C3 Information Autonomy - sccd P.12 IAS. RSF 2026 rank carries press
    freedom, V-Dem freedom of expression carries censorship, and internet
    penetration carries distribution reach."""
    rank = g(c, "rsf_rank")
    fe, net = g(c, "vdem_freeexpr"), g(c, "internet")
    rsf = 1 - (rank - 1) / 179.0
    terms = {"rsf_rank_2026": rank, "rsf_norm": round(rsf, 3),
             "vdem_freeexpr": fe, "internet": net}
    v = 0.40 * rsf + 0.40 * fe + 0.20 * nz(net, 30, 100)
    return cl(v), _tag(c, ["rsf_rank", "vdem_freeexpr", "internet"]), terms


def c4_exit(c):
    """C4 Exit Option Availability - sccd P.13 JECI, at the paper's own
    weights 0.50 capital / 0.30 labour / 0.20 IP. Chinn-Ito 2023 supplies the
    capital arm directly; the labour and IP arms are ANALYST.

    This is JURISDICTION exit only. Asset-form exit is Block A's a4 and
    reaches the engine as a level shift on C4 inside sccdx.forcing - which is
    exactly the channel sccd cannot see and must not be added here."""
    j = JUDGMENT[c]
    ka = g(c, "kaopen")
    terms = {"kaopen_2023": ka, "labour_exit(ANALYST)": j["labour_exit"],
             "ip_exit(ANALYST)": j["ip_exit"]}
    v = 0.50 * ka + 0.30 * j["labour_exit"] + 0.20 * j["ip_exit"]
    return cl(v), "MIXED", terms


def c5_frag(c):
    """C5 Preference Fragmentation (INHIBITOR) - sccd P.14 MFS.

    FULLY ANALYST for all eleven, and the reader should treat it that way.
    P_media wants an audience-overlap Gini, which is not systematically
    cross-national; P_legislative wants DW-NOMINATE-equivalent scaling, which
    exists for the US Congress and some European parliaments and for no ASEAN
    legislature; P_social wants WVS waves that most of these eleven have never
    been in. The three arms are argued in judgment.py."""
    j = JUDGMENT[c]
    terms = {"polar(ANALYST)": j["polar"],
             "party_frag(ANALYST)": j["party_frag"],
             "social_frag(ANALYST)": j["social_frag"]}
    v = (j["polar"] + j["party_frag"] + j["social_frag"]) / 3.0
    return cl(v), "ANALYST", terms


# ===========================================================================
# BLOCK D
# ===========================================================================
def d1_load(c):
    """Carrying-capacity load. DEGROW's modern form of the construct is the
    ability to supply stable-income jobs, affordable housing, education,
    healthcare and a sustainable environment - so NEET, vulnerable
    employment, youth dependency and the income level itself."""
    neet, vul = g(c, "neet"), g(c, "vuln_emp")
    dy, ppp = g(c, "dep_young"), g(c, "gdp_pc_ppp")
    terms = {"neet": neet, "vuln_emp": vul, "dep_young": dy,
             "gdp_pc_ppp": ppp}
    v = (0.28 * nz(neet, 5, 30)
         + 0.24 * nz(vul, 4, 80)
         + 0.18 * nz(dy, 15, 55)
         + 0.30 * (1 - nz(ppp, 4000, 100000)))
    return cl(v), "MEASURED", terms


def d2_expectation(c):
    """Expectation trap. The paper's substitute for Malthusian scarcity:
    cost of household formation against income. Numbeo's price-to-income
    ratio is the closest available series and it is measured for six of the
    eleven; the fertility collapse is treated as the revealed outcome of the
    trap rather than as a separate cause."""
    tfr, pti = g(c, "tfr"), g(c, "pti")
    urb, ter = g(c, "urban"), g(c, "tert_enrol")
    terms = {"tfr": tfr, "pti_2026": pti, "urban": urb, "tert_enrol": ter}
    v = (0.35 * (1 - nz(tfr, 0.9, 2.8))
         + 0.35 * nz(pti, 8, 38)
         + 0.15 * nz(urb, 25, 100)
         + 0.15 * nz(ter, 14, 100))
    return cl(v), _tag(c, ["tfr", "pti", "urban", "tert_enrol"]), terms


def d3_autonomy(c):
    """THE ROUTER. Availability AND use of voluntary adjustment instruments:
    contraception, financial planning, information, and welfare substitution
    for old-age support - which is the term that, in the paper's words,
    severed the intergenerational survival link.

    This single number decides whether a polity's adjustment pressure
    discharges through the voluntary door (d4 -> S5 compression) or the
    violent one (surplus youth -> S2 erosion). It is the highest-leverage
    input in Block D and the most weakly sourced: four of the eleven have no
    contraceptive-prevalence observation after 2021."""
    cm, sp = g(c, "contra_mod"), g(c, "socprot_cov")
    ppp, ter = g(c, "gdp_pc_ppp"), g(c, "tert_enrol")
    terms = {"contra_mod": cm, "socprot_cov": sp, "gdp_pc_ppp": ppp,
             "tert_enrol": ter}
    v = (0.30 * nz(cm, 20, 75)
         + 0.25 * nz(sp, 2, 95)
         + 0.25 * nz(ppp, 4000, 100000)
         + 0.20 * nz(ter, 14, 100))
    return cl(v), _tag(c, ["contra_mod", "socprot_cov", "gdp_pc_ppp",
                           "tert_enrol"]), terms


def d4_inversion(c):
    j = JUDGMENT[c]
    dep, p65 = g(c, "dep_old"), g(c, "pop65")
    terms = {"dep_old": dep, "pop65": p65, "pension(ANALYST)": j["pension"]}
    v = 0.50 * nz(dep, 6, 40) + 0.25 * nz(p65, 4, 22) + 0.25 * j["pension"]
    return cl(v), "MIXED", terms


def d5_youth(c):
    """Surplus youth cohort - the paper's reserve army of chaos. Headline
    youth unemployment is useless across this region (Cambodia reads 0.7%
    while 52% of its workforce is in vulnerable employment), so NEET and
    vulnerable employment carry the construct and adolescent fertility
    stands in for early, unsupported household formation."""
    neet, dy = g(c, "neet"), g(c, "dep_young")
    vul, af = g(c, "vuln_emp"), g(c, "adol_fert")
    terms = {"neet": neet, "dep_young": dy, "vuln_emp": vul,
             "adol_fert": af}
    v = (0.35 * nz(neet, 5, 32)
         + 0.30 * nz(dy, 15, 55)
         + 0.20 * nz(vul, 4, 80)
         + 0.15 * nz(af, 2, 82))
    return cl(v), "MEASURED", terms


# ===========================================================================
# BLOCK A
# ===========================================================================
def a_block(c, haven_override=None):
    """Block A. a1 is the only measured input - Microsoft's Q2 2026
    generative-AI diffusion rate, printed for SG, VN, PH and ID and ANALYST
    for the other seven. a2 and a3 are built off a1 by white-collar exposure,
    which is the paper's own mechanism: the tiers are driven by confronting a
    system that outperforms you at your own work, so the same adoption rate
    means different things in Singapore and in Laos."""
    j = JUDGMENT[c]
    a1 = g(c, "ai_diffusion")
    a2 = cl(a1 * (0.55 + 0.95 * j["whitecollar"]))
    a3 = cl(0.80 * a2 + 0.20 * a1)
    a4 = j["haven"] if haven_override is None else haven_override
    mb = g(c, "mobile_broad")
    a6 = cl(0.60 * a1 + 0.40 * nz(mb, 0, 28))
    terms = {"a1_ai_diffusion": a1, "whitecollar(ANALYST)": j["whitecollar"],
             "a2_derived": round(a2, 3), "a3_derived": round(a3, 3),
             "a4_haven(ANALYST)": a4, "mobile_broad": mb,
             "a6_derived": round(a6, 3)}
    blk = DispBlock(a1=a1, a2=a2, a3=a3, a4=cl(a4), a5=j["counter"], a6=a6,
                    physical_share=j["phys_share"],
                    luxury_contraction=j["lux"])
    return blk, terms


# ===========================================================================
# NETWORK CHANNELS
# ===========================================================================
def channels(c):
    j = JUDGMENT[c]
    gini = g(c, "gini")
    mil = g(c, "mil_gdp")
    grow = imf(c, "ngdp_rpch_2026")
    fdi = g(c, "fdi_gdp", 0.5)
    ppp = g(c, "gdp_pc_ppp")
    ter, net = g(c, "tert_enrol"), g(c, "internet")
    rd = g(c, "rd_gdp", 0.1)
    out = dict(
        revenue_polarisation=cl(0.50 * nz(gini, 28, 45) + 0.50 * j["polar"]),
        security_pressure=cl(0.45 * nz(mil, 0.2, 7.0)
                             + 0.55 * j["ext_threat"]),
        base_revenue_demand=round(g(c, "gg_exp") / 100.0, 4),
        ret=cl(0.60 * nz(grow, -2, 8) + 0.40 * nz(fdi, 0, 12)),
        opportunity=cl(nz(ppp, 3000, 170000)),
        capital_controls=cl(1.0 - g(c, "kaopen")),
        skilled_supply=cl(0.50 * nz(ter, 14, 100)
                          + 0.30 * nz(net, 30, 100)
                          + 0.20 * nz(rd, 0, 2.5)),
    )
    return out


def systemic_weight(c) -> float:
    """Relative systemic weight for Psi_G, indexed to Indonesia = 1.00 on
    nominal GDP. sccd gives no rule for this; GDP share is the obvious
    reading of 'systemically weighted' and it is stated rather than hidden."""
    return round(g(c, "gdp_usd") / RAW["ID"]["gdp_usd"][1], 4)


# ===========================================================================
# ASSEMBLY
# ===========================================================================
def build(c, haven_override=None, state_type_override=None):
    s1, t_s1, x_s1 = s1_fiscal(c)
    s2, t_s2, x_s2 = s2_coercive(c)
    s3, t_s3, x_s3 = s3_legitimacy(c)
    s4, t_s4, x_s4 = s4_admin(c)
    s5, t_s5, x_s5 = s5_temporal(c)
    c1, t_c1, x_c1 = c1_capital(c)
    c2, t_c2, x_c2 = c2_civil(c)
    c3, t_c3, x_c3 = c3_info(c)
    c4, t_c4, x_c4 = c4_exit(c)
    c5, t_c5, x_c5 = c5_frag(c)
    d1, t_d1, x_d1 = d1_load(c)
    d2, t_d2, x_d2 = d2_expectation(c)
    d3, t_d3, x_d3 = d3_autonomy(c)
    d4, t_d4, x_d4 = d4_inversion(c)
    d5, t_d5, x_d5 = d5_youth(c)
    disp, x_a = a_block(c, haven_override=haven_override)

    # Part III eq (5.3) boundary compression, X_hat = 0.02 + 0.96*X_raw,
    # applied to all ten sccd components. This is a PAPER step, not a
    # cosmetic one: it keeps the Hill multiplier and theta25 well posed, and
    # it is what stops Myanmar's s3 and Singapore's s4 from sitting exactly
    # on 0 and 1 where the band edges clip them. Block D and Block A inputs
    # are NOT compressed - spec2 defines them on the closed interval and
    # sccdx.forcing clamps them itself.
    sub = SubComponents(**{k: float(compress(v)) for k, v in dict(
        s1=s1, s2=s2, s3=s3, s4=s4, s5=s5,
        c1=c1, c2=c2, c3=c3, c4=c4, c5=c5).items()})
    demo = DemoBlock(d1=d1, d2=d2, d3=d3, d4=d4, d5=d5)
    sub.validate(); demo.validate(); disp.validate()

    ch = channels(c)
    pol = PolityInput(
        code=c, name=NAMES[c], sub=sub, demo=demo, disp=disp,
        state_type=state_type_override or JUDGMENT[c]["state_type"],
        weight=systemic_weight(c),
        provenance="sea2027: WDI/WGI 2025 + IMF WEO Oct-2026 + V-Dem 2025 + "
                   "Chinn-Ito 2023 + RSF 2026, composited per "
                   "sea2027/mapping.py; C5 and parts of S2/S3/C1/C2/C4 "
                   "ANALYST per sea2027/judgment.py",
        confidence="low",
        **ch)

    prov = {
        "s1": (t_s1, x_s1), "s2": (t_s2, x_s2), "s3": (t_s3, x_s3),
        "s4": (t_s4, x_s4), "s5": (t_s5, x_s5), "c1": (t_c1, x_c1),
        "c2": (t_c2, x_c2), "c3": (t_c3, x_c3), "c4": (t_c4, x_c4),
        "c5": (t_c5, x_c5), "d1": (t_d1, x_d1), "d2": (t_d2, x_d2),
        "d3": (t_d3, x_d3), "d4": (t_d4, x_d4), "d5": (t_d5, x_d5),
        "A":  ("MIXED", x_a),
    }
    return pol, prov


def build_all(haven_override: Dict[str, float] | None = None):
    pols, provs = [], {}
    for c in CODES:
        ho = (haven_override or {}).get(c)
        p, pr = build(c, haven_override=ho)
        pols.append(p); provs[c] = pr
    return pols, provs


def audit(provs) -> dict:
    counts = {"MEASURED": 0, "MIXED": 0, "ANALYST": 0}
    per = {}
    for c, pr in provs.items():
        row = {}
        for k, (tag, _) in pr.items():
            counts[tag] = counts.get(tag, 0) + 1
            row[k] = tag
        per[c] = row
    return {"counts": counts, "per_polity": per,
            "n_fields": sum(counts.values())}

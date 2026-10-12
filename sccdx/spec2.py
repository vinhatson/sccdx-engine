# -*- coding: utf-8 -*-
"""
SCCD-X Engine — Rule Specification v2.00
=========================================
Extends sccd.spec (v1.00, Vi Nhat Son "Sovereign-Civilian Capacity Dynamics"
Parts I-V) with two new forcing blocks derived from two further papers by the
same author:

  BLOCK D — "The Wheel of Fate: From Ancient 'Prosperity Trap' to the Modern
             Fertility Crisis"                                  [tag: DEGROW]
  BLOCK A — "The Displacement Hypothesis", 2nd ed., Feb 2026     [tag: DISPL]

WHY THESE TWO PAPERS PLUG IN HERE, STRUCTURALLY
-----------------------------------------------
sccd v1.00 leaves two terms of its own ODE system purely exogenous:

    dS3/dt = **S3_natural**    - rho_b(1-lam/lam_max)^2 - zeta*C5^psi*(S3-S3_floor)
    dC5/dt = **C5_structural** + eps_p*C5(1-C5)*RevPol + eta*C5^2*C3 + xi*C4*C1*(1-C5)

Those two starred terms are the engine's largest hole: they set the drift of
the two variables that control the whole non-linear core (S3 drives lambda,
which multiplies everything; C5 is the C denominator and the (1-C5) factor in
Psi), and v1.00 has nothing to say about either. The Wheel of Fate supplies a
mechanism for S3_natural and C5_structural on a demographic timescale; the
Displacement Hypothesis supplies one on an AI-adoption timescale. That is the
join. Everything else in this module follows from it.

PROVENANCE STATUS - read this before trusting any number
--------------------------------------------------------
SCCD      : inherited from sccd.spec v1.00 (itself 36 PAPER / 46 FREE)
DEGROW    : the SIGN and DIRECTION of the coupling is argued in Degrow.pdf
DISPL     : the SIGN and DIRECTION is argued in The Displacement Hypothesis
DISPL_NUM : an actual NUMBER stated in The Displacement Hypothesis
ANALYST   : magnitude chosen by the engine author. NO SOURCE. Placeholder.

The two new papers are a qualitative essay and a qualitative working paper.
Between them they contain ZERO coefficients usable as an ODE rate. Therefore
every coupling MAGNITUDE in Block D and Block A is ANALYST. What IS sourced
is the causal structure: which latent variable pushes which, and with what
sign. The engine is consequently an ORDINAL instrument in these blocks - it
ranks scenarios and locates threshold crossings; it does not produce
trustworthy absolute levels. This is the same epistemic standing Part V 1 of
the source paper claims for itself ("The validation standard is
qualitative-structural"), so nothing is lost by saying so plainly.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal

SPEC2_VERSION = "2.00"
BUILT_ON = "sccd.spec 1.00"

Status2 = Literal["SCCD", "DEGROW", "DISPL", "DISPL_NUM", "ANALYST", "DERIVED2"]

# ===========================================================================
#  LEVEL vs DRIFT - the rule that prevents double counting
# ===========================================================================
# A new forcing block may touch an sccd component in one of two ways: shift
# its LEVEL, or set its DRIFT (per-year rate). Choosing wrongly double counts,
# and the trap is easy to fall into. Worked example: sccd Part III defines
# S5 Temporal Leverage as the UNCOMMITTED revenue horizon. Pension liabilities
# are revenue pre-commitment, so a measured S5 ALREADY has them netted out.
# Subtracting a further compress_s5 * d4 from the level therefore charges the
# same pensions twice. What Block D legitimately knows that the measurement
# does not is how fast pre-commitment is still GROWING as the cohort ages -
# a rate, not a level.
#
# The rule the engine follows:
#
#   S-side components (S1..S5) take DRIFTS ONLY.
#     sccd's S proxies are annual flow measures - net discretionary revenue
#     ratio, UCDP/SIPRI-based coercive monopoly, WGI administrative reach.
#     Each already embeds present conditions, including whatever the new
#     blocks describe. Only the forward rate of change is new information.
#
#   C-side components (C1, C2, C4) take LEVEL SHIFTS.
#     sccd's C proxies are institutional stock measures that STRUCTURALLY
#     omit the new channels. Chinn-Ito plus OECD DIOC measure exit by
#     jurisdiction and contain no term whatever for exit by asset form;
#     V-Dem associational density lags a counter-technological revival by
#     years; WID wealth shares lag the UHNW/aspirational divergence. These
#     are blind spots, not double counts, so a level shift is the correct
#     correction.
#
#   C5 takes a DRIFT, because it is the variable sccd itself integrates
#     (dC5/dt in eq NL), and C5_structural is precisely the slot being filled.
#
# Consequence for reading the parameter table below: every coefficient whose
# target is an S component or C5 is a PER-YEAR RATE. Every coefficient whose
# target is C1, C2 or C4 is a DIMENSIONLESS LEVEL SHIFT. The `note` field on
# each says which.
LEVEL_TARGETS = ("c1", "c2", "c4")
DRIFT_TARGETS = ("s1", "s2", "s3", "s4", "s5", "c5", "d4")



@dataclass(frozen=True)
class P2:
    """A parameter: value + provenance + the sentence it came from."""
    value: float
    status: Status2
    src: str           # paper section / page
    note: str = ""

    def __float__(self) -> float:
        return float(self.value)


# ===========================================================================
#  BLOCK D - DEMOGRAPHIC PRESSURE ROUTER   [Degrow.pdf]
# ===========================================================================
# The paper's central claim, in its own words: the ancient demographic
# explosion-then-collapse and the modern fertility freeze are "different
# manifestations of the same fundamental law - the law of inevitable
# adjustment between humans and the resource/social limits within which they
# exist". Its stage model is
#     Prosperity (Pax) -> Population Boom -> Resource & Institutional Overload
#     -> Adjustment through Chaos and Death
# and its modern counterpart replaces the last arrow with voluntary fertility
# refusal: "cutting the spiral at its first stage (boom)".
#
# ENGINE READING. That is not one more pressure on the state. It is a ROUTER.
# A quantity of adjustment pressure is generated by load; what the paper
# actually varies is WHICH CHANNEL carries it. So Block D computes a scalar
# pressure and then splits it, and the split variable is the availability of
# voluntary adjustment tools ("contraception, financial planning, and
# risk-management thinking"). This is the whole formalisation.
# ---------------------------------------------------------------------------

DEMO_COMPONENTS = {
    "d1": ("Carrying-Capacity Load",
           "Population + expectation load relative to the system's ability to "
           "supply an acceptable standard of living. Ancient: arable land, "
           "irrigation, static yields. Modern, per the paper: 'the ability to "
           "provide stable-income jobs, affordable housing, quality education "
           "and healthcare services, and a sustainable ecological environment'."),
    "d2": ("Expectation Trap",
           "Cost of household formation relative to income - housing/income "
           "ratio, education and childcare cost, plus expectation inflation. "
           "The paper's substitute for Malthusian food scarcity: 'too much "
           "pressure for perfection, too many fixed costs'. Explicitly "
           "analogised to ancient landlessness: both are 'a denial of the "
           "opportunity to establish a stable family foundation'."),
    "d3": ("Adjustment Autonomy",
           "Availability AND use of voluntary adjustment instruments: "
           "contraception, financial planning, information, individual "
           "autonomy, and welfare substitution for old-age support (which "
           "'severed the intergenerational survival link'). 0 = ancient "
           "(no tools, pressure must discharge violently). 1 = modern OECD. "
           "THIS IS THE ROUTER VARIABLE."),
    "d4": ("Dependency Inversion",
           "Old-age dependency ratio plus the share of revenue pre-committed "
           "to PAYG pensions and health. The paper: 'When the pyramid "
           "inverts, this model collapses.'"),
    "d5": ("Surplus Youth Cohort",
           "Young cohort without assets, land, employment or prospects - the "
           "paper's 'reserve army of chaos', 'impoverished, uneducated youths "
           "with no assets and no future... the biofuel for revolution and "
           "civil war'."),
}

DEMO = {
    # --- pressure construction ---
    "kappa_exp": P2(0.60, "ANALYST", "DEGROW Legacy of the Modern Golden Age",
                    "weight of the expectation trap inside effective load. "
                    "The paper asserts d2 REPLACES classical scarcity in rich "
                    "societies but gives no exchange rate."),
    # --- router ---
    "route_sharpness": P2(1.00, "ANALYST", "DEGROW Revolutionary Difference",
                          "exponent on d3 in the split. 1.0 = linear split. "
                          ">1 means violent discharge persists until tools are "
                          "nearly universal. The paper implies a sharp "
                          "transition ('revolution in survival thinking') but "
                          "quantifies nothing."),
    # --- VIOLENT CHANNEL: ancient path, discharges through C5 and S2 ---
    "nu_youth_frag": P2(0.040, "ANALYST", "DEGROW Stage 2",
                        "surplus youth -> C5_structural. Sign from 'deep "
                        "polarization among the populace'."),
    "sigma_relief": P2(0.030, "ANALYST", "DEGROW Stage 2.1",
                       "relief-system failure -> S3 drift. Sign from 'the "
                       "breaking of the most sacred social contract... The "
                       "people's trust in the dynasty's mandate of heaven "
                       "completely shattered.'"),
    "erode_s2": P2(0.035, "ANALYST", "DEGROW Stage 2.2",
                   "the reserve army degrades the state's COERCIVE MONOPOLY "
                   "(not its coercive volume): 'gathered into gangs, lived "
                   "outside the law, ready to become mercenaries, bandits'. "
                   "Hits S2-hat, which gates theta25 at S2,crit=0.25 (PAPER)."),
    "erode_s4_corrupt": P2(0.022, "ANALYST", "DEGROW Stage 2.3",
                           "administrative penetration decays under strain: "
                           "'corruption transformed from individual behavior "
                           "into the default operating mechanism', central "
                           "authority in 'information blindness'."),
    # --- VOLUNTARY CHANNEL: modern path, discharges through S5 and S1 ---
    "iota_inversion": P2(0.018, "ANALYST", "DEGROW Refusing to Breed",
                         "voluntary pressure accumulates into dependency "
                         "inversion. This is the price the paper names: "
                         "'They accept facing a new demographic challenge "
                         "(aging) as the price to pay to avoid an old "
                         "demographic disaster.'"),
    "compress_s5": P2(0.018, "ANALYST", "DEGROW Invert the Welfare Pyramid",
                      "dependency inversion compresses TEMPORAL LEVERAGE "
                      "S5-hat. S5 is defined in sccd Part III as the "
                      "uncommitted revenue horizon; pensions are precisely "
                      "revenue pre-commitment. REVISED DOWN from an initial "
                      "0.045 against a direct counter-example: Japan has sat "
                      "within ~0.03 of theta25's 0.15 gate for two decades "
                      "without the discontinuity the gate is supposed to "
                      "mark. At 0.045 the gate closed inside 15 years for "
                      "every aging polity in the preset set, which makes the "
                      "diagnostic unfalsifiable rather than informative. "
                      "0.018 keeps the mechanism and restores discrimination. "
                      "The constant-drain form still assumes NO policy "
                      "response - no retirement-age move, no benefit "
                      "reindexation - so it remains an upper bound on the "
                      "compression rate."),
    "compress_s1": P2(0.022, "ANALYST", "DEGROW Invert the Welfare Pyramid",
                      "shrinking contributor base vs fixed obligations erodes "
                      "net discretionary revenue S1-hat."),
    "sigma_expect": P2(0.014, "ANALYST", "DEGROW Expectation Trap",
                       "the expectation trap as a pure LEGITIMACY drain, "
                       "independent of output. This is the mechanism that "
                       "lets S3 fall while GDP rises - the modern equivalent "
                       "of ancient land hunger. Conventional macro models "
                       "have no slot for it."),
    # --- thresholds for the Block-D regime overlay ---
    "d5_violent_thresh": P2(0.55, "ANALYST", "DEGROW Stage 3",
                            "surplus-youth level above which the violent "
                            "channel is the operative one."),
    "d3_voluntary_thresh": P2(0.60, "ANALYST", "DEGROW Modern Era",
                              "adjustment-autonomy level above which the "
                              "polity is in voluntary mode."),
    "d4_inversion_thresh": P2(0.55, "ANALYST", "DEGROW Invert the Pyramid", ""),
    "d2_trap_thresh": P2(0.60, "ANALYST", "DEGROW Expectation Trap", ""),
    # --- floors. sccd.spec.DYNAMICS defines s1_floor and s3_floor (both FREE,
    # both 0.05) but gives none for S2, S4 or S5, because v1.00 never
    # integrates those three. Block D does, so they need floors or the drain
    # runs them to exactly zero - which would claim a state with literally no
    # discretionary revenue and literally no coercive monopoly. Same value and
    # same idiom as the two sccd already has.
    "s2_floor": P2(0.05, "ANALYST", "by analogy with sccd IV.NL s1_floor",
                   "level shift: hard floor on the integrated S2"),
    "s4_floor": P2(0.05, "ANALYST", "by analogy with sccd IV.NL s1_floor",
                   "level shift: hard floor on the integrated S4"),
    "s5_floor": P2(0.05, "ANALYST", "by analogy with sccd IV.NL s1_floor",
                   "level shift: hard floor on the integrated S5. NOTE this "
                   "floor sits BELOW theta25's S5,crit=0.15 PAPER gate, so "
                   "the gate still closes - the floor only stops the drain "
                   "from reaching an absurd zero."),
}

# Historical anchors the paper DOES state numerically. Not parameters - they
# are the only quantitative content in Degrow.pdf, kept for back-testing.
DEGROW_HISTORICAL_ANCHORS = [
    dict(case="Roman Empire peak", metric="population", value="60-70 million",
         stage="Stage 1 peak"),
    dict(case="Qing Kangxi to Qianlong", metric="population",
         value="~150M -> >300M", stage="Stage 1 boom"),
    dict(case="Ming collapse 1600-1644", metric="population",
         value="150-200M -> 100-120M", stage="Stage 3 adjustment",
         note="paper states 'at least one-third, possibly up to 40%' loss"),
    dict(case="generic Stage-3 adjustment", metric="population loss",
         value="30% to 60%", stage="Stage 3",
         note="the only range the paper gives for the adjustment magnitude"),
    dict(case="Ming tenancy burden", metric="land rent share of output",
         value="60-70%", stage="Stage 2"),
]


# ===========================================================================
#  BLOCK A - DISPLACEMENT / AI FORCING   [The Displacement Hypothesis v2]
# ===========================================================================
# The paper's three mechanisms: compensatory substitution (AI replaces the
# psychological function of conspicuous consumption), self-efficacy erosion
# (Tier 1, "can I still earn a living?"), and agency collapse (Tier 2,
# "am I still me?"). Its observable consequence is a capital reallocation
# "away from identity-signaling goods (luxury) and toward stability-preserving
# assets (gold, silver)".
#
# ENGINE READING. Two of its claims matter to a sovereign-capacity model and
# the paper itself does not draw either out, because it is written as a
# markets paper:
#
#   (1) THE G/S3 DECOUPLING. Everywhere in sccd v1.00 a generation windfall
#       and legitimacy move TOGETHER - Part V's 1941-45 build-up is the type
#       case, war dividend raising both. AI is the first windfall in the
#       model's history that raises G while LOWERING S3, because the thing it
#       erodes is agency, and agency is what consent is made of. The engine
#       must therefore break an implicit co-movement that v1.00 never had to
#       state. Diagnostic consequence: a polity can post rising S and rising
#       Delta_norm while Psi collapses - high capacity, no coherence to aim
#       it. v1.00's five Delta bands cannot express that, which is why this
#       module adds a coherence overlay.
#
#   (2) HAVEN FLIGHT IS EXIT IN THE C4 SENSE - but of a kind sccd Part III
#       does not measure. C4 is built from capital-account openness
#       (Chinn-Ito) and emigration options: exit by JURISDICTION. Gold in a
#       domestic vault is exit by ASSET FORM - the holder does not leave, the
#       wealth simply stops being legible, and therefore stops being taxable,
#       inflatable or repressible. sccd's own re-extraction term already has
#       the right shape for this: tau_eff = tau_max*S1*(1-C4)*lam/lam_max.
#       Push C4 up and T falls. The paper's third prediction - "physical gold
#       will increasingly command a premium over paper gold" - is precisely
#       the statement that the flight is into the NON-LEGIBLE form
#       specifically.
#
# AND THIS IS WHERE THE TWO PAPERS MEET. Both independently arrive at the same
# failure mode: a state raising extraction on a shrinking legible base.
#   Degrow Stage 2.1: "the crudest solution was to increase tax rates based on
#     that antiquated data, a socially suicidal act. It was like continuing to
#     milk a cow that was already emaciated to the bone."
#   Displacement 5-8: the base relocates into tangible, non-legible metal.
# Same spiral, six centuries apart, reached from demography and from
# psychology. The engine makes it loop L6.
# ---------------------------------------------------------------------------

DISP_COMPONENTS = {
    "a1": ("AI Penetration",
           "Share of daily cognitive and decision tasks mediated by AI. The "
           "paper's adoption variable: 'mass adoption at a pace exceeding any "
           "prior consumer technology'."),
    "a2": ("Self-Efficacy Erosion (Tier 1)",
           "Bandura-sense efficacy loss from confronting systems that "
           "outperform the user. 'Can I still earn a living?' Drives "
           "defensive financial behaviour."),
    "a3": ("Agency Erosion (Tier 2)",
           "Existential loss of authorship: the Puppet Effect, blurring of "
           "self and algorithm, dissolution of narrative identity. 'Am I "
           "still me?' The paper's deepest layer, and the one that reaches "
           "sovereign legitimacy."),
    "a4": ("Haven Reallocation",
           "Share of discretionary capital moved into tangible, "
           "algorithm-independent, state-illegible stores of value - "
           "physical gold and silver above all. 'Gold... becomes a symbol of "
           "resistance - a tangible anchor for the self.'"),
    "a5": ("Counter-Tech Mobilisation",
           "The predicted New Luddism: 'conscious technology withdrawal... "
           "resurgence of artisanal and handcraft economies... "
           "community-building centered on physical co-presence'. Note it is "
           "an ORGANISING force, so in sccd terms it RAISES C2-hat."),
    "a6": ("AI Productivity Windfall",
           "The output-side term. Enters sccd's G(t) through the same slot as "
           "T_shock in Part II eq (12)."),
}

DISP = {
    # --- Tier architecture (4.4.4) ---
    "tier_w1": P2(0.35, "ANALYST", "DISPL 4.4.4", "weight on Tier-1 (a2)"),
    "tier_w2": P2(0.45, "ANALYST", "DISPL 4.4.4", "weight on Tier-2 (a3)"),
    "tier_w_cross": P2(0.20, "ANALYST", "DISPL 4.4.4",
                       "the mutual-reinforcement term a2*a3. The paper is "
                       "explicit that this interaction exists: 'economic "
                       "helplessness deepens the existential crisis... and "
                       "existential crisis intensifies economic paralysis. "
                       "The compound effect...'. Magnitude unsourced."),
    # --- (1) the decoupling: agency erosion -> S3 ---
    "sigma_agency": P2(0.030, "ANALYST", "DISPL 4.4.3, 8.6",
                       "agency erosion -> S3 drift, scaled by penetration. "
                       "Sign from the paper's identity-crisis and "
                       "meaninglessness mechanisms plus its own policy "
                       "section: the affected population 'retain their jobs "
                       "but lose their sense of agency, competence, and "
                       "self-authored identity'. Consent of the governed is "
                       "made of exactly that."),
    "g_ai": P2(0.400, "ANALYST", "DISPL 1",
               "windfall multiplier into G(t). Enters as g_tech*T_shock does "
               "in sccd Part II eq (12)."),
    # --- (2) haven flight: the legibility channel ---
    "zeta_haven_c4": P2(0.260, "ANALYST", "DISPL 5.2-5.4",
                        "haven reallocation -> EFFECTIVE C4-hat. Asset-form "
                        "exit added to sccd's jurisdiction-form exit."),
    "zeta_base_s1": P2(0.030, "ANALYST", "DISPL 5.4.2, prediction 3",
                       "the non-legible share of haven wealth leaves the "
                       "extractable base. Multiplied by physical_share, "
                       "because paper gold stays legible and taxable - that "
                       "distinction IS the paper's third prediction."),
    "zeta_lux_s1": P2(0.012, "ANALYST", "DISPL 2.3, 6.2",
                      "consumption-tax base erosion from the aspirational "
                      "segment's exit. The paper's own figure: aspirational "
                      "buyers were 60-70% of the luxury customer base and "
                      "the attrition was 'overwhelmingly concentrated' there."),
    # --- fragmentation and its counterweight ---
    "nu_narrative": P2(0.028, "ANALYST", "DISPL 4.4.2",
                       "narrative-identity dissolution -> C5_structural. "
                       "'The individual's life story becomes less a "
                       "self-authored novel...' plus the fear of assimilation "
                       "into 'AI-optimized, AI-influenced sameness'."),
    "nu_counter": P2(0.030, "ANALYST", "DISPL 8.5",
                     "counter-tech community organising DEPOLARISES, via "
                     "C2-hat. NOTE: this is the first SOURCED generator for "
                     "the term sccd INC-7 says is missing from dC5/dt. "
                     "v1.00's patch added -nu*C5*C2 on the grounds that Part "
                     "IV 2.3 names C2 as the counterweight but omits the "
                     "term; Block A now supplies a mechanism that actually "
                     "produces it."),
    "zeta_ctr_c2": P2(0.170, "ANALYST", "DISPL 8.5",
                      "counter-tech mobilisation -> C2-hat civil-organisation "
                      "density. 'They will attract mainstream participation "
                      "from precisely the demographic most exposed to agency "
                      "erosion: educated, digitally fluent professionals.'"),
    # --- capital concentration: the UHNW asymmetry ---
    "zeta_uhnw_c1": P2(0.130, "ANALYST", "DISPL 2.4, 6.2",
                       "erosion is class-asymmetric, so it CONCENTRATES "
                       "C1-hat. The paper: UHNW 'whose identity and agency "
                       "are secured by capital rather than cognitive labor' "
                       "hold position while the aspirational tier is "
                       "stripped. C1 then feeds sccd loop L1 at its PAPER "
                       "threshold C1,crit = 0.70."),
    # --- thresholds for Block-A overlays and loops ---
    "a1_mass_thresh": P2(0.60, "ANALYST", "DISPL 6.1", "mass-adoption level"),
    "a3_crisis_thresh": P2(0.55, "ANALYST", "DISPL 4.4.3", ""),
    "a4_flight_thresh": P2(0.55, "ANALYST", "DISPL 5.3", ""),
    "squeeze_thresh": P2(0.10, "ANALYST", "DEGROW 2.1 x DISPL 5.4",
                         "extraction squeeze (demanded minus feasible rate) "
                         "above which loop L6 is self-reinforcing."),
    "physical_share_default": P2(0.45, "ANALYST", "DISPL 6.4, prediction 3",
                                 "default physical (vs paper/ETF) share of "
                                 "haven allocation when the caller gives none. "
                                 "Paper's data point: bar and coin demand "
                                 "exceeded 1,200 tonnes annually alongside "
                                 "record ETF inflows."),
}

# Numbers actually printed in The Displacement Hypothesis. Used by the
# back-test harness, never as coefficients.
DISPL_STATED_NUMBERS = [
    dict(k="luxury consumers lost 2022-2025", v="50-60 million", src="Abstract, 1"),
    dict(k="aspirational share of luxury base pre-2023", v="60-70%", src="2.3"),
    dict(k="gold late-2023", v="~$2,000/oz", src="1"),
    dict(k="gold Jan-2026", v=">$5,500/oz", src="1, Table 1"),
    dict(k="gold 2025 move", v="+66% to ~$4,325/oz", src="Table 1"),
    dict(k="silver 2025", v="~+150%", src="6.5"),
    dict(k="platinum 2025", v="~+110%", src="6.5"),
    dict(k="central bank gold buying", v="60+ tonnes/month", src="6.4"),
    dict(k="bar and coin demand", v=">1,200 tonnes/yr", src="6.4"),
    dict(k="aspirational buyer income band", v="$80k-$150k household", src="5.1"),
    dict(k="aspirational luxury spend", v="$3,000-$8,000/yr", src="5.1"),
    dict(k="AI subscription cost", v="~$20/month", src="3.3, 5.1"),
]


# ===========================================================================
#  NEW FEEDBACK LOOPS L5-L8
# ===========================================================================
LOOP2_NAMES = {
    "L5": "Agency-Legitimacy Spiral",
    "L6": "Legibility-Extraction Spiral",
    "L7": "Demographic Inversion Trap",
    "L8": "Youth-Surplus Discharge",
}

LOOP2_DESCRIPTIONS = {
    "L5": "a3 agency erosion drains S3 -> lambda falls -> delivery capacity "
          "falls -> policy fails visibly -> meaning and authorship erode "
          "further. Source: DISPL 4.4 for the drain; the return leg is sccd's "
          "own lambda-multiplier structure. Couples into L2 and L3.",
    "L6": "Extraction demanded exceeds extraction feasible -> the state leans "
          "harder on the legible base -> more wealth relocates into "
          "non-legible form (a4) -> the legible base shrinks further. "
          "Source: DEGROW Stage 2.1 (the emaciated cow) x DISPL 5.4 (the "
          "flight into physical metal). This loop is the point where the two "
          "new papers are the same paper. Couples into L1 and L4.",
    "L7": "Dependency inversion crowds fiscal space -> support for household "
          "formation is what gets cut -> the expectation trap tightens -> "
          "fertility falls further -> inversion deepens. Source: DEGROW "
          "Invert the Welfare Pyramid + Expectation Trap, closed into a loop "
          "(the paper describes both arms but never joins them). Couples into "
          "L2 and L6.",
    "L8": "Surplus youth with no stake x weak coercive monopoly x no "
          "voluntary adjustment tools -> the ancient discharge path: "
          "fragmentation and unrest rise, S2-hat falls below its theta25 "
          "gate. Source: DEGROW Stages 2-3. This is the loop that lets the "
          "engine read the young half of the world at all; L5-L7 are "
          "rich-aging-society loops. Couples into L2 and L3.",
}

# Cross-coupling, extending sccd.loops.CROSS_COUPLING (which covers L1-L4).
CROSS_COUPLING2: Dict[str, List[str]] = {
    "L1": ["L3", "L4", "L6"],
    "L2": ["L1", "L3", "L5"],
    "L3": ["L2", "L4", "L5"],
    "L4": ["L2", "L3", "L6"],
    "L5": ["L2", "L3"],
    "L6": ["L1", "L4", "L7"],
    "L7": ["L2", "L6"],
    "L8": ["L2", "L3"],
}

LOOP2_COUPLING_WEIGHT = {k: P2(1.0, "ANALYST", "sccd IV.CAI by analogy",
                               "sccd gives no Coupling_Weight values for "
                               "L1-L4 either; unit weights keep CAI a count "
                               "of active loops, which is at least honest.")
                         for k in ("L5", "L6", "L7", "L8")}
LOOP2_SPEED = {k: P2(1.0, "ANALYST", "sccd IV.CAI by analogy", "")
               for k in ("L5", "L6", "L7", "L8")}

# CAI banding.
#   CAI_core  = L1-L4 only, scored and banded EXACTLY as sccd Part IV eq (CAI)
#               specifies. Comparable to anything v1.00 produced.
#   CAI_ext   = L1-L8. The paper's bands were set against four loops, so they
#               are rescaled by 4/8. Flagged UNCALIBRATED-EXT and reported
#               alongside, never instead of, CAI_core.
CAI_EXT_SCALE = P2(0.50, "DERIVED2", "4 paper loops / 8 engine loops",
                   "rescales sccd's CAI bands to the extended loop set")


# ===========================================================================
#  REGIME OVERLAYS
# ===========================================================================
# sccd Part II Table 2 classifies on Delta_norm alone - five bands. Block A
# makes that insufficient: the whole point of the G/S3 decoupling is that
# Delta and Psi can now move in OPPOSITE directions, and a single Delta band
# cannot say so. The engine therefore reports a triple.

COHERENCE_TIERS = [
    # (name, lower_exclusive, upper_inclusive)
    ("Coherent",   0.40, 99.0),   # at or above sccd's PAPER Psi_crit = 0.40
    ("Strained",   0.25, 0.40),
    ("Incoherent", -1.0, 0.25),
]
COHERENCE_TIER_SRC = ("Psi_crit = 0.40 is a PAPER value (sccd II.eq23). The "
                      "0.25 inner cut is ANALYST - it splits 'below "
                      "threshold' from 'far below threshold'.")

ADJUSTMENT_MODES = {
    "VOLUNTARY": "d3 high, d5 low - pressure discharges through fertility "
                 "refusal and then dependency inversion. Degrow's modern "
                 "path. Terminal gate: S5-hat falling through theta25's 0.15 "
                 "floor.",
    "VIOLENT_EXPOSED": "d3 low, d5 high - no voluntary instruments and a "
                       "large cohort with no stake. Degrow's ancient path. "
                       "Terminal gate: S2-hat falling through theta25's 0.25 "
                       "floor.",
    "MIXED": "both channels carrying pressure, or neither dominant.",
    "SLACK": "load low enough that no adjustment is being demanded.",
}

# The unified result worth stating, and the reason both blocks live in one
# module: BOTH of Degrow's paths terminate in the collapse of the SAME sccd
# object - the threshold factor theta25 - through two different gates. The
# aging path closes the S5 gate (revenue pre-committed, no temporal leverage).
# The youth path closes the S2 gate (coercive monopoly lost). theta25 -> 0
# sends S -> lambda*(w1*S1 + w4*S4) with the entire threshold term gone, and
# simultaneously sends Psi = lambda*theta25*(1-C5) -> 0, so R_B's coherence
# condition trips too. The Wheel of Fate, written in sccd's own variables, is
# a statement about theta25.
THETA25_GATE_NOTE = (
    "Degrow's two adjustment channels terminate in the same object - theta25 "
    "- through different gates: voluntary/aging closes S5 (crit 0.15, PAPER), "
    "violent/youth closes S2 (crit 0.25, PAPER). Both drive Psi -> 0 via "
    "Psi = lambda*theta25*(1-C5), tripping R_B's third condition."
)


# ===========================================================================
#  WORLD / NETWORK EXTENSIONS
# ===========================================================================
WORLD2 = {
    "haven_sync_gain": P2(0.350, "ANALYST", "DISPL 6.4-6.5",
                          "simultaneous haven flight across systemically "
                          "weighted states is itself a synchronisation "
                          "channel, so it raises Sync_Risk in sccd's Psi_G. "
                          "sccd's own Sync_Risk was a bare historical prior "
                          "(0.12/0.24/0.41/0.58 for 1980/95/2010/2024); this "
                          "gives it one endogenous driver. The paper's "
                          "breadth-of-demand argument is the support: demand "
                          "'across all investor types... consistent with a "
                          "pervasive psychological shift'."),
    "divergence_talent_gain": P2(0.280, "ANALYST", "DEGROW x sccd IV.N4",
                                 "dispersion of d3 across the world IS the "
                                 "migration pressure gradient: one half of "
                                 "the world in voluntary mode needs workers, "
                                 "the other half has surplus youth. Feeds "
                                 "sccd's existing F^talent channel."),
    "ai_divergence_gain": P2(0.220, "ANALYST", "DISPL 8.1-8.2",
                             "dispersion of a1 widens capacity gaps, which is "
                             "an input to the Thucydides convergence test."),
}


# ===========================================================================
#  AUDIT + OPEN PROBLEMS
# ===========================================================================
_GROUPS2 = {"demo": DEMO, "disp": DISP, "world2": WORLD2,
            "loop2_coupling": LOOP2_COUPLING_WEIGHT, "loop2_speed": LOOP2_SPEED,
            "cai_ext": {"CAI_EXT_SCALE": CAI_EXT_SCALE}}


def audit2() -> dict:
    """Provenance census for the v2 layer. Mirrors sccd.spec.audit()."""
    rows, counts = [], {}
    for g, d in _GROUPS2.items():
        for name, p in d.items():
            qual = name if g not in ("loop2_coupling", "loop2_speed") \
                else f"{g.split('_')[1]}_{name}"
            rows.append(dict(group=g, name=qual, status=p.status,
                             src=p.src, value=p.value, note=p.note))
            counts[p.status] = counts.get(p.status, 0) + 1
    return dict(rows=rows, counts=counts, total=len(rows),
                spec2_version=SPEC2_VERSION, built_on=BUILT_ON)


def combined_audit() -> dict:
    """v1 + v2 provenance in one view - the number to quote when asked how
    calibrated this engine is."""
    from sccd import spec as s1
    a1, a2 = s1.audit(), audit2()
    return {
        "v1": {"total": a1["total"], "counts": a1["counts"],
               "spec_version": a1["spec_version"]},
        "v2": {"total": a2["total"], "counts": a2["counts"],
               "spec2_version": a2["spec2_version"]},
        "headline": (
            f"{a1['counts'].get('PAPER', 0)} of {a1['total']} v1 parameters "
            f"carry a value from the source paper; {a1['counts'].get('FREE', 0)} "
            f"do not. ALL {a2['total']} v2 parameters are ANALYST or DERIVED2 - "
            f"the two new papers are qualitative and state no coefficients. "
            f"Read every v2-dependent output as ORDINAL: a ranking and a "
            f"threshold-crossing map, not a level."
        ),
    }


OPEN_PROBLEMS_V2 = [
    dict(id="OP2-1", severity="HIGH", where="Block D router",
         issue="The split P_violent/P_voluntary = (1-d3)/d3 is the engine's "
               "reading of Degrow, not Degrow's own statement. The paper "
               "argues the two channels are 'different manifestations of the "
               "same fundamental law' and that modern tools let people 'cut "
               "the spiral at its first stage', which is what a router means. "
               "But the paper never says total pressure is CONSERVED across "
               "the split. If voluntary adjustment is cheaper in total "
               "pressure terms - plausible, since it prevents rather than "
               "clears overload - then d3 should reduce P_demo itself and not "
               "merely redirect it. The engine exposes this as `router_mode` "
               "('conserve' | 'discount') so the assumption is a dial rather "
               "than a hidden choice. Default: conserve."),
    dict(id="OP2-2", severity="HIGH", where="Block A, sigma_agency",
         issue="The agency->legitimacy link is the load-bearing claim of the "
               "whole v2 layer and it is the least evidenced. Displacement "
               "documents agency erosion and documents capital reallocation; "
               "it does NOT document a fall in regime legitimacy, and offers "
               "no survey series on consent. The engine asserts the link on "
               "the ground that consent of the governed is constituted by "
               "exactly the self-authorship the paper says is dissolving. "
               "That is an argument, not a measurement. If it is wrong, L5 "
               "is spurious and S3 drift in rich democracies is overstated."),
    dict(id="OP2-3", severity="medium", where="Block A, a4 double-counting",
         issue="Haven flight hits S1 twice: directly through zeta_base_s1, "
               "and indirectly because the raised C4 cuts tau_eff through "
               "sccd's own (1-C4) factor. These are genuinely different "
               "channels (base size vs extraction rate) but the engine cannot "
               "prove they do not overlap. Set `haven_single_channel=True` to "
               "disable the direct term and route everything through C4."),
    dict(id="OP2-4", severity="medium", where="Block A vs sccd C4 measurement",
         issue="Effective C4 now mixes two things sccd Part III measured as "
               "one: jurisdiction exit (Chinn-Ito, OECD DIOC) and asset-form "
               "exit (haven share). They have different reversal dynamics - "
               "capital controls can close jurisdiction exit in a weekend; "
               "metal in a domestic vault is not recalled by decree. Treating "
               "them as one scalar understates how hard asset-form exit is to "
               "reverse."),
    dict(id="OP2-5", severity="medium", where="Blocks D and A overlap",
         issue="d2 (expectation trap) and a2 (self-efficacy erosion) are "
               "measured separately but both depress household formation and "
               "both drain S3. In a 2026 OECD panel they would be strongly "
               "collinear. The engine does not de-collinearise them, so a "
               "caller who sets both high is double-counting one pressure. "
               "Cronbach gating (sccd.normalize) would catch it given series; "
               "with hand-entered point values nothing does."),
    dict(id="OP2-6", severity="low", where="L8 vs sccd L2",
         issue="L8's activation overlaps sccd's L2 (legitimacy death spiral) "
               "whenever surplus youth has already driven S3 below 0.30. CAI "
               "then counts two loops where arguably one mechanism is "
               "running. The cross-coupling map marks the pair, and the "
               "engine reports `cai_overlap_warning`, but the count is not "
               "corrected."),
    dict(id="OP2-7", severity="low", where="inherited",
         issue="Everything in sccd.spec.KNOWN_INCONSISTENCIES still applies. "
               "INC-7/8/9 are CRITICAL and the v2 engine therefore runs with "
               "sccd's patch=True and c1_dynamic=True by DEFAULT, inverting "
               "v1.00's default. Rationale: Block A supplies a sourced "
               "mechanism for the depolarisation term INC-7 says is missing "
               "(counter-tech organising through C2), and Block D supplies "
               "one for the legitimacy-recovery term INC-8 says is missing "
               "(delivery performance through S4). Set `faithful_v1=True` to "
               "reproduce the paper verbatim instead."),
]

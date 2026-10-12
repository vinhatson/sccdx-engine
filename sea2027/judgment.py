# -*- coding: utf-8 -*-
"""
sea2027.judgment - the ANALYST overlay
=======================================
One block per polity. Every field here is a number the analyst is asserting,
with the reason it is asserted. Nothing in this file is a measurement.

  conflict   : max non-state armed capacity / state capacity, as an erosion of
               the coercive MONOPOLY (sccd P.2 TCAI; UCDP is now token-gated)
  crony      : political activation factor on concentrated capital (sccd P.10
               PACI, PAF in [0.3,1.0]; no lobbying register exists in any of
               the eleven, so PAF cannot be measured)
  unrest     : live legitimacy drawdown not yet inside WGI 2025 or V-Dem 2025
  polar,
  party_frag,
  social_frag: the three arms of C5. ALL ANALYST for ALL eleven - there is no
               cross-national audience-overlap series and no comparable
               legislative-polarisation score for ASEAN parliaments, which is
               Part III's own stated binding constraint on C5 outside US/EU
  protest    : collective-action EFFECTIVENESS, third term of P.11 ECSI
  labour_exit,
  ip_exit    : the two non-capital arms of P.13 JECI
  whitecollar: share of employment in cognitive/clerical work exposed to
               generative AI; drives Block A's a2 and a3 off measured a1
  haven      : Block A a4
  phys_share : physical vs paper split of haven demand
  counter    : Block A a5 counter-tech mobilisation
  lux        : observed luxury-demand contraction
  pension    : share of revenue pre-committed to PAYG pensions and health
  ext_threat : external / border security pressure
"""
from __future__ import annotations

from typing import Dict

JUDGMENT: Dict[str, dict] = {

 "BN": dict(
   state_type="extractive_patrimonial",
   conflict=0.00, crony=0.70, unrest=0.00,
   polar=0.10, party_frag=0.02, social_frag=0.20,
   protest=0.04, labour_exit=0.60, ip_exit=0.18,
   whitecollar=0.45, haven=0.25, phys_share=0.85, counter=0.04, lux=0.10,
   pension=0.55, ext_threat=0.12,
   why="A hydrocarbon rentier monarchy with the region's lowest political "
       "temperature and its most exposed single-commodity revenue base. "
       "crony is high not through lobbying but through fusion: royal "
       "household, sovereign fund and state are not separable, which is the "
       "PACI construct at its purest. polar and party_frag are near zero "
       "because there is no legislature to fragment. The live risk is s1 and "
       "s5, not s2 or c5 - 2025 growth of 0.7% on a maturing field base, and "
       "the first sustained oil undershoot converts straight into an L6 "
       "squeeze with no tax instrument to fall back on."),

 "KH": dict(
   state_type="extractive_patrimonial",
   conflict=0.22, crony=0.90, unrest=0.05,
   polar=0.25, party_frag=0.08, social_frag=0.30,
   protest=0.12, labour_exit=0.52, ip_exit=0.14,
   whitecollar=0.18, haven=0.42, phys_share=0.88, counter=0.03, lux=0.08,
   pension=0.15, ext_threat=0.58,
   why="crony 0.90, the highest in the set: the oknha system ties licence to "
       "patronage directly and V-Dem's political-corruption index of 0.904 is "
       "the second worst of the eleven. conflict is non-zero for a reason a "
       "state-based conflict series would miss - the scam compounds are armed "
       "and, on the Prime Minister's own February 2026 account, destroying "
       "the legal economy; that is a rival to the coercive monopoly inside "
       "Cambodian territory. ext_threat 0.58 is the Thai border: two rounds "
       "of fighting in 2025, a 27 December ceasefire that Stratfor rated "
       "still holding but non-normalising in August 2026, and Thai forces on "
       "ground Phnom Penh calls occupied. haven 0.42 in a dollarised economy "
       "where gold is the household savings instrument of record."),

 "ID": dict(
   state_type="liberal_democracy",
   conflict=0.14, crony=0.80, unrest=0.26,
   polar=0.52, party_frag=0.45, social_frag=0.60,
   protest=0.85, labour_exit=0.45, ip_exit=0.30,
   whitecollar=0.38, haven=0.66, phys_share=0.88, counter=0.08, lux=0.18,
   pension=0.40, ext_threat=0.20,
   why="unrest 0.26 is the largest penalty applied to any s3 here and it is "
       "the most consequential single ANALYST number in the file. V-Dem's "
       "2025 liberal-democracy score of 0.296 is already a decade low, and "
       "the 2025-26 protest wave - cost of living, layoffs, legislators' "
       "allowances, police violence, then the free-meals poisonings and the "
       "June 2026 fuel-price round - sits ON TOP of that reading rather than "
       "inside it. protest 0.85 because those mobilisations repeatedly forced "
       "policy reversals, and coordination EFFECTIVENESS is what P.11 asks "
       "for. haven 0.66 is the firmest Block A number in the set: 38.1t of "
       "bar and coin in H1 2026, more than Thailand and Vietnam combined, "
       "+40% y/y, with the WGC's own attribution being currency weakness and "
       "concerns about the domestic outlook. polar sits below what party_frag "
       "would imply because Prabowo holds an oversized coalition - the split "
       "is street-against-elite, not legislative."),

 "LA": dict(
   state_type="developmental_autocracy",
   conflict=0.05, crony=0.75, unrest=0.10,
   polar=0.14, party_frag=0.04, social_frag=0.35,
   protest=0.07, labour_exit=0.46, ip_exit=0.12,
   whitecollar=0.14, haven=0.58, phys_share=0.90, counter=0.03, lux=0.05,
   pension=0.15, ext_threat=0.10,
   why="The clearest L6 case in the region on measured numbers alone. The "
       "IMF's February 2026 Article IV calls public debt unsustainable and "
       "the country in external and overall debt distress even as the ratio "
       "falls; inflation returned to about 10% by April 2026; and the US "
       "State Department's 2026 statement holds that IMF figures undercount "
       "the liabilities to China. Social protection covers 2.2% of the "
       "population. haven 0.58 because two episodes of 20-30% inflation "
       "inside four years teach a household what the kip is worth. unrest "
       "0.10 rather than zero: there is no protest channel, so the legitimacy "
       "drawdown surfaces as exit and informality instead."),

 "MY": dict(
   state_type="liberal_democracy",
   conflict=0.05, crony=0.75, unrest=0.14,
   polar=0.70, party_frag=0.72, social_frag=0.75,
   protest=0.50, labour_exit=0.60, ip_exit=0.50,
   whitecollar=0.55, haven=0.44, phys_share=0.70, counter=0.08, lux=0.20,
   pension=0.45, ext_threat=0.20,
   why="social_frag 0.75 is the highest non-Myanmar value and it is "
       "structural rather than episodic - the cleavage is communal and "
       "constitutionally entrenched, not a swing of opinion. party_frag 0.72 "
       "on a grand coalition that has now lost Sabah, Johor and Negeri "
       "Sembilan at state level while holding the federal centre, with GE16 "
       "due by February 2028 and Anwar publicly weighing an early call. "
       "unrest 0.14 for the subsidy-rationalisation cost-of-living channel "
       "plus the collapse of the Zahid prosecution, which is the exact "
       "mechanism sccd's L_comply pillar is about. pension only 0.45 because "
       "the EPF is funded rather than PAYG - Malaysia's ageing bill lands on "
       "households, not on the budget."),

 "MM": dict(
   state_type="failed_state",
   conflict=0.95, crony=0.85, unrest=0.15,
   polar=0.85, party_frag=0.80, social_frag=0.85,
   protest=0.55, labour_exit=0.58, ip_exit=0.10,
   whitecollar=0.12, haven=0.78, phys_share=0.92, counter=0.03, lux=0.04,
   pension=0.20, ext_threat=0.95,
   why="conflict 0.95 is not a claim about who is winning; it is the "
       "statement that no actor holds a monopoly. BTI 2026 puts junta "
       "authority as contested in over two thirds of the territory with more "
       "than half of 330 townships in active conflict; stable Tatmadaw "
       "control was put at 72-220 of 330 townships as of December 2025; the "
       "Arakan Army holds most of Rakhine; three regional commands have "
       "fallen. The December 2025 phased election changed the legal claim, "
       "not the control map. unrest is only 0.15, and deliberately so: "
       "WGI 2025 and V-Dem 2025 already price the collapse in full - "
       "government effectiveness at the 19th percentile, "
       "liberal-democracy 0.015, the lowest of the eleven - so a larger "
       "drawdown would charge the coup twice. haven "
       "0.78 at phys_share 0.92: 22% inflation in 2025 and a kyat no one "
       "holds voluntarily. This row exists to test whether loop L8 fires "
       "where it should."),

 "PH": dict(
   state_type="liberal_democracy",
   conflict=0.30, crony=0.85, unrest=0.30,
   polar=0.78, party_frag=0.70, social_frag=0.58,
   protest=0.85, labour_exit=0.85, ip_exit=0.35,
   whitecollar=0.72, haven=0.38, phys_share=0.85, counter=0.07, lux=0.12,
   pension=0.45, ext_threat=0.45,
   why="The one polity where three channels load at once. Legitimacy: the "
       "flood-control scandal, with the Department of Finance costing the "
       "loss at up to PHP 118.5bn over 2023-25, a 600,000-strong Iglesia ni "
       "Cristo rally in November 2025, 37 criminal complaints filed and - as "
       "of February 2026 - no sitting legislator detained, plus an allegation "
       "that PHP 25bn reached the President himself. The gap between outrage "
       "and consequence is what unrest 0.30 encodes. Fragmentation: the "
       "Marcos-Duterte rupture is now institutional, with the "
       "Vice-President's second impeachment trial running since 6 July 2026 "
       "and the Senate court having altered its own conviction threshold in "
       "September. Block A: whitecollar 0.72 is the highest in the set - BPO "
       "is precisely the task class generative AI substitutes for - against a "
       "measured a1 of 0.207, already third highest here. labour_exit 0.85 on "
       "remittances at 8.5% of GDP: the exit option is institutionalised, "
       "which also caps how much further C4 can rise."),

 "SG": dict(
   state_type="developmental_autocracy",
   conflict=0.00, crony=0.60, unrest=0.04,
   polar=0.35, party_frag=0.25, social_frag=0.40,
   protest=0.20, labour_exit=0.90, ip_exit=0.90,
   whitecollar=0.80, haven=0.40, phys_share=0.60, counter=0.14, lux=0.28,
   pension=0.45, ext_threat=0.25,
   why="state_type is the contestable choice in this file. Singapore is "
       "electoral and its 2025 mandate was renewed competitively, but sccd's "
       "state_type sets only three weights - w1 fiscal, w4 admin, omega25 - "
       "and on those three the developmental-autocracy profile "
       "(0.35/0.45/0.20) fits the WGI 2025 vector (government effectiveness "
       "95th percentile, voice and accountability 55th) far better than the "
       "liberal-democracy row does. run.py re-runs this polity as a "
       "liberal_democracy so the reader can see what the choice costs. a1 of "
       "0.643 is the second-highest generative-AI diffusion rate on earth "
       "after the UAE, which makes this the one polity in the region where "
       "Block A's decoupling condition can be tested on measured adoption "
       "rather than inferred. phys_share 0.60, the lowest here: Singapore's "
       "haven demand runs through vaults and funds that stay legible, so the "
       "L6 legibility channel is weak even where the reallocation is real."),

 "TH": dict(
   state_type="liberal_democracy",
   conflict=0.25, crony=0.85, unrest=0.18,
   polar=0.80, party_frag=0.75, social_frag=0.55,
   protest=0.65, labour_exit=0.35, ip_exit=0.40,
   whitecollar=0.42, haven=0.56, phys_share=0.85, counter=0.10, lux=0.35,
   pension=0.70, ext_threat=0.45,
   why="The region's demographic outlier and therefore its Block D test "
       "case: old-age dependency 23.0 and TFR 1.2 at $26,250 PPP per head - "
       "Japan's age structure on a quarter of Japan's income. pension 0.70, "
       "the highest here, because the commitment is already legislated "
       "(universal health coverage plus the old-age allowance) while formal "
       "pension coverage is 4.5%, so the burden falls on general revenue. "
       "Against that, the IMF's own October 2026 vintage has debt rising "
       "64.7 to 67.8% of GDP by 2027 on growth of 1.5% in 2026 and 2.1% in "
       "2027, the weakest pair in the region. polar 0.80: the 8 February "
       "2026 election gave Bhumjaithai 192 of 500 and left the "
       "royalist-reformist cleavage intact, and by 8 October 2026 the "
       "People's Party was collecting signatures for an Article 151 motion "
       "naming twelve ministers including the Prime Minister over the "
       "Senate-selection scandal. ext_threat 0.45 for the Cambodian border."),

 "TL": dict(
   state_type="liberal_democracy",
   conflict=0.08, crony=0.50, unrest=0.08,
   polar=0.45, party_frag=0.55, social_frag=0.35,
   protest=0.50, labour_exit=0.35, ip_exit=0.10,
   whitecollar=0.12, haven=0.20, phys_share=0.85, counter=0.03, lux=0.03,
   pension=0.45, ext_threat=0.10,
   why="The freest polity in the set on every civic measure - RSF 30th of "
       "180, ahead of every other ASEAN member and most of Europe; V-Dem "
       "liberal-democracy 0.549, nearly double Indonesia's - and the poorest "
       "by a wide margin at $4,810 PPP per head, with NEET at 29.1% and youth "
       "dependency 53.7, the highest in the region. That pairing is why the "
       "row matters: high c2 and c3 with low s1 and high d5. The binding fact "
       "is that the Petroleum Fund, not tax, pays for the state, so s1 and s5 "
       "are about the Fund's drawdown path and almost nothing else. ASEAN "
       "accession on 26 October 2025 raises opportunity and labour_exit over "
       "the next decade but changes no 2027 input. crony 0.50, the lowest "
       "here, because there is not yet enough private capital to "
       "concentrate."),

 "VN": dict(
   state_type="developmental_autocracy",
   conflict=0.02, crony=0.60, unrest=0.10,
   polar=0.18, party_frag=0.05, social_frag=0.30,
   protest=0.15, labour_exit=0.45, ip_exit=0.35,
   whitecollar=0.45, haven=0.70, phys_share=0.90, counter=0.05, lux=0.22,
   pension=0.60, ext_threat=0.35,
   why="haven 0.70 is set ABOVE Thailand's even though Vietnamese "
       "bar-and-coin volume fell 24% y/y in Q1 2026 and 31% in Q2, and the "
       "reason is the Displacement paper's own third prediction. The WGC "
       "attributes the fall to domestic supply constraint with local premiums "
       "at eye-watering levels - demand revealed through price because it "
       "cannot clear through volume. Reading the volume alone inverts the "
       "signal. This is an interpretive call and it is the most arguable "
       "number in the file; run.py reports what a volume-based 0.40 does "
       "instead. Elsewhere the picture is of consolidation: the 14th Congress "
       "closed on 23 January 2026 with To Lam re-elected 180/180 to a "
       "19-member Politburo weighted towards security and the judiciary, and "
       "a 10%-a-year growth target for 2026-30 against 8.0% actual in 2025. "
       "c5 stays very low; base_revenue_demand stays high. pension 0.60 on "
       "old-age dependency of 14.0 with 12.7% pension coverage - the "
       "inversion arrives before the institution does."),
}

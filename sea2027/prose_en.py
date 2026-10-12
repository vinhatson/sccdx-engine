# -*- coding: utf-8 -*-
"""
sea2027.prose_en - the English prose reading, one entry per polity
===================================================================
This is INTERPRETATION, and it is mine, not the engine's. The engine emits a
band, a tier, a mode, a loop set and a gate order; it does not emit an
argument about what any of that means. Everything here is an argument built
on those outputs plus the measured panel in raw_2026.py, and a reader who
accepts the numbers may still reject the reading.

Where a sentence rests on an ANALYST input rather than a measurement, it says
so. The `fragile` section of every entry names what would have to be wrong.

Companion file: prose_vi.py, the same reading in Vietnamese. The two are
written, not translated through each other - but they make the same claims,
and if they ever diverge in substance that is a bug in this file or that one.
"""
from __future__ import annotations

PROSE = {

# ===========================================================================
"TH": dict(
 title="Japan's age structure on a quarter of Japan's income",
 lede=[
  "Thailand carries three live loops into 2027 and is the only polity in the "
  "region where two of them are cross-coupled. The engine still reads it "
  "Negotiated / Strained at the end of 2027 — the band does not move inside "
  "the window — but it is the most fragile row in the set by a clear margin, "
  "and the one where a single ordinary political event flips the reading.",
 ],
 body=[
  "The demographic fact is the one to start from, because everything else "
  "bends around it. Old-age dependency is 23.0 and the fertility rate is 1.2, "
  "at $26,250 PPP per head. That is Japan's age structure on roughly a "
  "quarter of Japan's income, and it is arriving while the state's formal "
  "pension coverage is 4.5%. The commitment is already legislated — universal "
  "health coverage plus the old-age allowance — so the burden lands on "
  "general revenue rather than on a funded scheme. Against that, the IMF's "
  "October 2026 vintage has public debt rising from 64.7% to 67.8% of GDP by "
  "2027 on growth of 1.5% in 2026 and 2.1% in 2027: the weakest growth pair "
  "in Southeast Asia, at exactly the moment the demographic bill starts "
  "arriving.",

  "That configuration is what arms L7, the Demographic Inversion Trap, and "
  "L7 is running alongside L6, the Legibility–Extraction Spiral. The engine "
  "flags the pair as cross-coupled, which is its way of saying the two are "
  "not merely both present but feeding each other. The mechanism is "
  "unglamorous and old: the state needs more revenue because the dependency "
  "ratio is inverting, so it leans harder on the base it can see, and the "
  "base it can see responds by becoming less visible. Thailand's extraction "
  "squeeze is +0.284 against a 0.10 threshold — demanded 0.305 against "
  "feasible 0.020 — and its haven reallocation sits at 0.56, just over the "
  "0.55 trigger, with 20.9 tonnes of bar and coin bought in the first half "
  "of 2026 and the strongest first quarter since 2019.",

  "The third loop, L3, is the Polarisation Trap, and it is where the "
  "political year enters. Ĉ₅ has already crossed its 0.50 threshold at 0.69. "
  "The February 2026 election gave Bhumjaithai 192 of 500 seats and returned "
  "Anutin, but it did not resolve the royalist–reformist cleavage; by October "
  "2026 the People's Party was collecting signatures for an Article 151 "
  "motion naming twelve ministers including the Prime Minister over the "
  "Senate-selection scandal. The Cambodian border adds a second axis: a "
  "December 2025 ceasefire that has held through landmine incidents and "
  "forward deployments without normalising.",

  "The gate order is the part worth carrying away. Ĉ₅ is already past. Ŝ₃ "
  "reaches its 0.30 PAPER floor in about ten years and Ŝ₅ reaches 0.15 in "
  "about twenty-seven. Ŝ₂ is two centuries away. So Thailand's terminus is "
  "the voluntary door — the aging, fiscal one — not the violent one, which "
  "is what the VOLUNTARY adjustment mode means here. At fifteen years the "
  "engine reads Equilibrium / Incoherent: not collapse, but a state that has "
  "stopped being able to act coherently on anything.",
 ],
 stress="The stress branch is where Thailand separates from the rest. Add a "
        "constitutional crisis at 0.50 — the Article 151 motion resolving "
        "against the government — plus pension-reform failure at 0.40 and the "
        "region-wide tariff shock, and the verdict moves: Negotiated / "
        "Strained becomes Equilibrium / Incoherent, Ψ falls 0.320 to 0.157, "
        "and L2, the Legitimacy Death Spiral, arms on top of the three loops "
        "already running. Four simultaneous loops is the worst configuration "
        "anywhere in the region, baseline or stressed. Note what these events "
        "are: not a coup, not a war, not a financial crisis. A no-confidence "
        "motion succeeding and a pension reform failing are ordinary politics.",
 fragile="Five of the 42 OAT parameters flip Thailand's qualitative verdict "
         "at ±20% — the most fragile row in the set. Three of them "
         "(d3_voluntary_thresh, d4_inversion_thresh, d2_trap_thresh) switch "
         "L7 off, which means the Demographic Inversion Trap, the loop this "
         "whole reading is built around, rests on ANALYST coefficients that a "
         "20% nudge dislodges. Treat L7 here as a hypothesis the measured "
         "demography makes plausible, not as a finding.",
 watch=[
  "Whether the Article 151 motion is filed, and whether it carries. The "
  "stress branch is conditioned on it resolving against the government.",
  "Any move on the old-age allowance or on retirement age. The engine's d₄ "
  "drift assumes NO policy response; a real reform would falsify the "
  "steepest part of the S₅ path.",
  "Thai bar-and-coin demand through 2027. Above the 2026 run-rate keeps a₄ "
  "over the 0.55 trigger and L6 armed; a sharp fall switches L6 off.",
  "Whether 2027 growth lands near the IMF's 2.1%. Materially below it pulls "
  "the debt path above 67.8% and tightens the squeeze directly.",
  "The Cambodian border. Not for the fighting itself but for what the "
  "engine says a genuine onset would do — see the Cambodia reading.",
 ],
 limits="Thailand's reading leans harder on ANALYST inputs than any other. "
        "The pension commitment term (0.70), the three C₅ arms and the haven "
        "level are all argued, not measured, and five parameters flip the "
        "verdict under the mandated ±20% perturbation. The direction is "
        "well-supported by the measured demography and fiscal path; the "
        "specific loop set is not.",
),

# ===========================================================================
"PH": dict(
 title="The only tier change inside the window",
 lede=[
  "The Philippines is the one polity in the eleven whose verdict moves inside "
  "2027 on the baseline, with no stress events added. It enters the window "
  "Equilibrium / Strained and leaves it Equilibrium / Incoherent, with the "
  "crossing at roughly t = 0.25 — early 2027. It is also the only row where "
  "three of sccd's four ORIGINAL loops are running at once.",
 ],
 body=[
  "CAI_core is 3.0 here, the highest in the region. That number matters more "
  "than the extended CAI because L1–L4 are the loops the source paper "
  "specifies and calibrates; the four new ones are all ANALYST. So when the "
  "Philippines posts three of the original four, the engine is making a claim "
  "inside its best-supported machinery rather than in the layer this project "
  "added.",

  "L1, the Regulatory Capture Accelerator, arms because both of its PAPER "
  "conditions are met simultaneously: Ĉ₁ is 0.77, above the 0.70 capture "
  "threshold, while Ŝ₂ is 0.54, below the 0.60 floor. Russia in the stock "
  "preset set has more extreme capture and L1 does not arm, because its "
  "coercive monopoly is intact. The Philippine combination — concentrated, "
  "politically activated capital alongside a state that does not fully "
  "monopolise force — is the specific pairing the loop was written for.",

  "L2, the Legitimacy Death Spiral, is the one that moves inside the window. "
  "Ŝ₃ crosses its 0.30 PAPER floor at t = 0.33, and the coherence tier breaks "
  "to Incoherent slightly before that. The measured and researched basis is "
  "the flood-control scandal: the Department of Finance costing the loss at "
  "up to PHP 118.5bn over 2023–25, a 600,000-strong rally in November 2025, "
  "37 criminal complaints filed, and — as of February 2026 — not one sitting "
  "legislator detained. The gap between the scale of the outrage and the "
  "absence of consequence is the mechanism. Legitimacy capital is spent by "
  "demonstrating that the rules do not bind the people who write them.",

  "L3 is fed by the Marcos–Duterte rupture, which is now institutional rather "
  "than factional: the Vice-President's second impeachment trial has run "
  "since 6 July 2026, the Senate court altered its own conviction threshold "
  "in September, and a verdict was reported as possible by mid-December. "
  "Ĉ₅ has already crossed 0.50.",

  "Underneath the politics sits the Block A exposure, which is the highest in "
  "the region: white-collar exposure of 0.72 against a measured generative-AI "
  "diffusion rate of 0.207, third-highest here. The BPO sector is precisely "
  "the class of cognitive work the Displacement Hypothesis describes being "
  "substituted. Against that, labour exit is 0.85 with remittances at 8.5% of "
  "GDP — the exit option is institutionalised, which both relieves pressure "
  "and caps how much further Ĉ₄ can rise.",
 ],
 stress="Adding the impeachment aftermath and BPO displacement roughly halves "
        "Ψ, 0.234 to 0.115, without changing the verdict — because the "
        "verdict is already Incoherent. That is the signature of a polity "
        "with no headroom: the stress does not move the label, it just "
        "deepens the hole. At fifteen years the engine reads Crisis / "
        "Incoherent.",
 fragile="Only two parameters flip the verdict at ±20%, so the reading is "
         "comparatively robust by OAT. But the s₃ level itself carries an "
         "ANALYST drawdown of 0.30 for the scandal, and s₃ is sccd's own "
         "highest-risk proxy and is BLOCKED — no cross-national source exists "
         "for two of its four pillars. The tier change at t = 0.25 is a "
         "direct consequence of where that drawdown put the starting level.",
 watch=[
  "The impeachment verdict and what follows it. A conviction and an acquittal "
  "push Ĉ₅ in the same direction; what differs is whether Ŝ₃ recovers at all.",
  "Whether any sitting legislator is actually detained. On the engine's "
  "logic this is the single most legitimacy-restorative event available.",
  "BPO headcount. A measured contraction would convert the Block A exposure "
  "from a projection into an observation.",
  "Remittance flows. They are holding the floor under household income; a "
  "fall would load d₁ and d₅ at once.",
 ],
 limits="Everything above is ordinal. The engine does not say the Philippines "
        "will have a crisis in 2027; it says the tier breaks inside the "
        "window on current drifts, that three PAPER-specified loops are "
        "running, and that the nearest gate is already at zero years.",
),

# ===========================================================================
"ID": dict(
 title="The regional hegemon, reading Strained",
 lede=[
  "Indonesia carries the largest systemic weight in the eleven and the engine "
  "names it the regional hegemon. It also reads Equilibrium / Strained with "
  "two gates already crossed, and its Δ_norm crosses into negative territory "
  "inside 2027 — one of only two polities where that happens. The "
  "Monte-Carlo pass puts 10% of the probability mass in the Crisis band, the "
  "highest crisis share in the region.",
 ],
 body=[
  "Two PAPER thresholds are already behind Indonesia rather than ahead of it. "
  "Ŝ₃ is below its 0.30 floor and Ĉ₅ is above its 0.50 fragmentation "
  "threshold. Neither is a forecast; both are the starting state. What the "
  "engine then adds is that the remaining gates are far away — Ŝ₂ at 68 years "
  "and Ŝ₅ at 127 — so Indonesia is not approaching a terminus. It is already "
  "inside the band the thresholds were drawn to mark, and sitting there.",

  "L2 and L6 are the active pair. The legitimacy side is the better "
  "evidenced: V-Dem's 2025 liberal-democracy score of 0.296 is a decade low, "
  "and the 2025–26 protest wave sits on top of that reading rather than "
  "inside it — cost of living, mass layoffs, legislators' allowances, police "
  "violence, then the free-meals poisonings and the June 2026 fuel-price "
  "round. The engine encodes that as a 26% proportional drawdown on "
  "legitimacy capital, the largest applied to any polity here, and that one "
  "ANALYST number is the most consequential judgement in the whole input file.",

  "The L6 side is the firmest Block A evidence in the region, and it is "
  "measured rather than argued. Indonesian households bought 38.1 tonnes of "
  "gold bars and coins in the first half of 2026 — more than Thailand and "
  "Vietnam combined — up roughly 40% year on year, while jewellery demand "
  "fell 10%. The World Gold Council's own attribution is currency weakness "
  "and concerns about the domestic outlook. That is not ornament buying; it "
  "is balance-sheet behaviour, and it is exactly the asset-form exit sccd's "
  "jurisdiction-based Ĉ₄ cannot see.",

  "The fiscal frame tightens both. The 2026 budget runs a deficit near the "
  "3%-of-GDP statutory cap with the free-meals programme roughly doubling to "
  "around $20.7bn while transfers to regional governments were cut; Moody's "
  "moved the outlook to negative; the finance minister was replaced. A state "
  "raising demands on a base that is simultaneously reallocating into "
  "non-legible form is the L6 configuration in its plainest statement.",

  "Note what Indonesia is NOT. Protest capacity is coded at 0.85, the "
  "joint-highest in the region, because those mobilisations repeatedly forced "
  "policy reversals — that is coordination effectiveness, which is what "
  "sccd's Ĉ₂ actually asks for. A high Ĉ₂ is civilian capacity, not state "
  "weakness, and it is the main reason the 2027 band holds where the "
  "Philippines' breaks.",
 ],
 stress="The deficit cap breaking and rupiah pressure take Ψ from 0.355 to "
        "0.336 without moving the verdict. Indonesia has more headroom in "
        "2027 than its 15-year path suggests. At fifteen years the engine "
        "reads Crisis / Incoherent.",
 fragile="Three parameters flip the verdict at ±20%, and one of them "
         "(a4_flight_thresh) switches L6 off entirely at +20%. More "
         "importantly, the 0.26 unrest drawdown is an argued number with no "
         "measurement behind it: it is the analyst's claim that the protest "
         "wave is not yet priced into the 2025 V-Dem and WGI vintages. If "
         "that is wrong, Indonesia's Ŝ₃ is too low and the whole Strained "
         "reading softens.",
 watch=[
  "Whether the 3% deficit cap holds through the 2027 budget cycle.",
  "Indonesian bar-and-coin demand. A second year near 2026's run-rate turns "
  "a₄ from a one-year reallocation into a trend, which is a different claim.",
  "Whether the free-meals programme's scale survives contact with revenue.",
  "Protest frequency AND whether protests still force reversals. The second "
  "is what Ĉ₂ measures; the first alone is not.",
 ],
 limits="Indonesia is the hegemon by GDP weight, and the engine's choice of "
        "hegemon is mechanical — systemic weight, not performance. Nothing in "
        "the Ψ_G calculation should be read as a judgement that Indonesia "
        "leads the region in any other sense.",
),

# ===========================================================================
"SG": dict(
 title="The only polity where the decoupling is measurable",
 lede=[
  "Singapore reads Hegemonic / Coherent in 2027 with a single loop running, "
  "and is the only one of the eleven where the Displacement Hypothesis's "
  "central claim can be tested against a measured adoption rate rather than "
  "inferred. Its decoupling index is 0.485; the next-highest in the region "
  "is 0.046.",
 ],
 body=[
  "Microsoft's Q2 2026 diffusion figure puts 64.3% of Singaporean working-age "
  "adults using a generative-AI product — second in the world behind the UAE. "
  "That single measured number is what makes this row unusual. Everywhere "
  "else in the region Block A's a₁ is either a smaller printed figure or an "
  "analyst estimate scaled off internet penetration; here the adoption is "
  "high enough, and well enough measured, that the mechanism has something to "
  "bite on.",

  "The mechanism is L5, the Agency–Legitimacy Spiral, and it is the one loop "
  "the engine's own documentation flags as its weakest link. The chain runs: "
  "high penetration times high white-collar exposure produces agency erosion, "
  "and agency erosion drains legitimacy, because consent of the governed is "
  "made of the self-authorship the paper says is dissolving. The project's "
  "open problem OP2-2 states plainly that this link is argued, not measured — "
  "the source paper documents agency erosion and documents capital "
  "reallocation, and documents no fall in regime legitimacy anywhere. "
  "Singapore is where that argument is most exposed, because here the "
  "antecedent is real and measured. If L5 is spurious, this is where the "
  "absence should show.",

  "What `decoupling_active` means in practice is that Δ_norm and Ψ can move "
  "in opposite directions — the engine's output convention breaks, and it "
  "says so rather than hiding it. Singapore's windfall term is the largest in "
  "the region (a₆ = 0.78) and raises G, while the agency term pushes S₃ down. "
  "A v1.00 reading, which has only the five Δ bands, would report this as "
  "untroubled growth.",

  "The gate order is distinctive too. For every other polity in the region "
  "the nearest gate is Ŝ₃ or something already crossed. For Singapore it is "
  "Ĉ₅ at about thirteen years, with Ŝ₃ at twenty-one and Ŝ₅ at thirty-two. "
  "Ŝ₂ is effectively never — the projection returns tens of thousands of "
  "years, which is the engine's way of saying the drift is numerically zero. "
  "So the thing that closes first here is fragmentation, not fiscal capacity "
  "and not coercive monopoly.",

  "One choice in the input file deserves flagging, because it is the most "
  "contestable in the whole set: Singapore is read as a developmental "
  "autocracy rather than a liberal democracy. The justification is narrow — "
  "state_type only sets three weights, and on those three the WGI 2025 vector "
  "(government effectiveness 95th percentile, voice and accountability 55th) "
  "fits that row better. The counterfactual was run: band, tier, loop set and "
  "R_B all hold, and Δ_norm moves from +0.371 to +0.329. The choice costs "
  "almost nothing, which is the honest reason to stop arguing about it.",
 ],
 stress="White-collar displacement at 0.60 and a visible agency crisis at "
        "0.40, on top of the tariff shock, take Ψ from 1.269 to 1.077 — a 15% "
        "fall with no change of band. Singapore absorbs more stress without "
        "moving than anything else in the region except Brunei. At fifteen "
        "years it steps down one band to Negotiated / Coherent.",
 fragile="Two parameters flip the verdict, one of which (a1_mass_thresh) "
         "switches L5 off entirely at +20%. So even here, with the "
         "best-measured adoption rate in the region, whether the loop appears "
         "at all turns on an ANALYST threshold.",
 watch=[
  "Whether the diffusion rate keeps climbing or plateaus. The L5 trigger is "
  "a threshold on a₁, not on its rate of change.",
  "Any measurable movement in institutional-trust or consent indicators. "
  "This is the observation OP2-2 says does not yet exist anywhere.",
  "Whether the AI windfall shows up in general revenue or stays with capital. "
  "The engine routes a₆ into G; where it lands determines whether it offsets "
  "the legitimacy drain or widens it.",
 ],
 limits="L5 is the single least evidenced construct in the v2 layer and it is "
        "the only loop running here. A Singapore reading that drops L5 has no "
        "loops at all and nothing to say beyond 'Hegemonic / Coherent'.",
),

# ===========================================================================
"VN": dict(
 title="One loop, and it hangs on one judgement",
 lede=[
  "Viet Nam reads Negotiated / Coherent through 2027 with Ψ above 1.0, the "
  "third-highest in the region, and it is among the least fragile rows in the "
  "set by OAT: just one parameter of 42 flips its verdict. It is also the row "
  "where a single interpretive choice I made decides whether it shows any "
  "loop at all.",
 ],
 body=[
  "Start with what is solid. Ĉ₅ is 0.19, the second-lowest in the region, and "
  "that matters more than it looks because C₅ is both the denominator of the "
  "C aggregate and the (1−C₅) factor in Ψ. Low fragmentation is why Ψ holds "
  "above 1.0 while Thailand, with comparable raw capacity, sits at 0.32. The "
  "14th Party Congress closed on 23 January 2026 with To Lam re-elected "
  "180/180 to a 19-member Politburo weighted towards security and the "
  "judiciary, and a target of 10% average annual growth for 2026–30 against "
  "8.0% actual in 2025. Whatever else that is, it is not fragmentation.",

  "The nearest gate is Ŝ₃ at about eighteen years — comfortable by regional "
  "standards, where Laos faces six and Cambodia eight. Ŝ₅ is eighty-nine "
  "years away and Ĉ₅ sixty-six. At fifteen years the engine still reads "
  "Equilibrium / Coherent, which alongside Brunei, Singapore and Malaysia is "
  "one of only four Coherent readings left in the region at that horizon.",

  "Now the contestable part. The one active loop is L6, the "
  "Legibility–Extraction Spiral, and it arms only because I set haven "
  "reallocation at 0.70 — above the 0.55 trigger. The measured Vietnamese "
  "figure points the other way: bar-and-coin volume fell 24% year on year in "
  "Q1 2026 and 31% in Q2. I set a₄ high anyway, because the World Gold "
  "Council attributes that fall to domestic supply constraint with local "
  "premiums at what it calls eye-watering levels. That is demand revealed "
  "through price because it cannot clear through volume, and the physical-"
  "over-paper premium is the Displacement Hypothesis's own third prediction. "
  "Reading the volume alone inverts the signal.",

  "I think that reading is right, and I also think it is the most arguable "
  "number in the file, so the counterfactual is run and reported: at a₄ = "
  "0.40, taken from volume, L6 switches off and Viet Nam has no active loop "
  "whatsoever. Ψ barely moves (1.009 against 1.010) and the band and tier are "
  "identical. So the disagreement is not about Viet Nam's condition in 2027 "
  "— it is about whether a mechanism is quietly running underneath it.",

  "The structural tension the engine does surface is between the growth "
  "target and the demography. Old-age dependency is already 14.0 with pension "
  "coverage at 12.7%: the inversion is arriving before the institution that "
  "is supposed to absorb it. Vulnerable employment is 51.4%. A 10%-a-year "
  "target on that base is a commitment to outrun a dependency curve, and the "
  "engine's d₄ drift assumes no policy response.",
 ],
 stress="Viet Nam has the highest tariff exposure in the set — trade at 190% "
        "of GDP — so the region-wide shock is applied at 0.70 here against "
        "0.40–0.60 elsewhere. With white-collar displacement and the IMF's own "
        "inflation path (3.3% in 2025 to 4.9% in 2026 and 4.6% in 2027), Ψ "
        "falls from 1.009 to 0.811 and the verdict holds. That is a 20% fall "
        "absorbed without a band change.",
 fragile="One parameter flips the verdict: d3_voluntary_thresh, which moves "
         "the adjustment mode. By OAT this is among the most robust rows in "
         "the region, behind only Brunei, Malaysia and Timor-Leste, which "
         "flip on none. The real fragility is not in the parameters but in "
         "the a₄ "
         "input, and that is a reading of evidence rather than a coefficient, "
         "so the sensitivity protocol cannot see it at all.",
 watch=[
  "The Vietnamese domestic gold premium, not the volume. On the argument "
  "above, the premium is the signal and the volume is the supply constraint.",
  "Whether the 10% growth target is restated, softened, or quietly dropped at "
  "the mid-term review.",
  "Pension coverage. It is 12.7% against old-age dependency of 14.0; the gap "
  "is what d₄ is measuring.",
  "Tariff outcomes specifically, given 190%-of-GDP trade exposure.",
 ],
 limits="A Coherent reading is not a benign one. It says the system is "
        "internally consistent enough to act, not that what it does will "
        "work. The engine has nothing to say about whether a 10% growth "
        "target is achievable.",
),

# ===========================================================================
"MY": dict(
 title="Fragmentation without a spiral",
 lede=[
  "Malaysia reads Negotiated / Coherent through 2027 with one loop running, "
  "and it is one of only three polities in the region — with Brunei and "
  "Timor-Leste — where no "
  "parameter at all flips the qualitative verdict under the mandated ±20% "
  "perturbation. It is the most stable reading in the set that is not simply "
  "a rentier.",
 ],
 body=[
  "The single active loop is L3, the Polarisation Trap, and Ĉ₅ at 0.71 has "
  "already crossed the 0.50 threshold. What is interesting is what has NOT "
  "armed alongside it. Malaysia's fragmentation is high and structural — "
  "social fragmentation is coded 0.75, the highest outside Myanmar, because "
  "the cleavage is communal and constitutionally entrenched rather than a "
  "swing of opinion — and yet the legitimacy and extraction loops stay off.",

  "The reason is administrative depth and fiscal room. Ŝ₄ is 0.81, the "
  "second-highest in the region after Singapore, on WGI government "
  "effectiveness at the 72nd percentile with near-universal social-protection "
  "coverage. Ŝ₃ at 0.58 is the third-highest here. A polity can be deeply "
  "divided and still deliver, and the engine distinguishes the two in a way "
  "a single polarisation index would not.",

  "The political year supports the reading without changing it. Anwar's grand "
  "coalition has now lost Sabah, Johor and Negeri Sembilan at state level "
  "while holding the federal centre; GE16 is due by February 2028 and an "
  "early call has been publicly weighed. The subsidy-rationalisation "
  "programme is doing exactly what the engine's L_comply pillar is about — "
  "trading present legitimacy for fiscal consolidation — and the termination "
  "of the case against the Deputy Prime Minister feeds the same channel. "
  "Those give the 0.14 unrest drawdown, modest against Indonesia's 0.26 and "
  "the Philippines' 0.30.",

  "One quiet structural point: pension commitment is coded at only 0.45, well "
  "below Thailand's 0.70, because the EPF is funded rather than pay-as-you-go. "
  "Malaysia's ageing bill lands on households, not on the budget. That is why "
  "Malaysia and Thailand, at broadly similar points on the demographic curve, "
  "produce completely different loop sets: Thailand runs L7 and Malaysia does "
  "not.",
 ],
 stress="GE16 as a polarising election at 0.60, plus the tariff shock, is "
        "enough to move the tier: Coherent becomes Strained and Ψ falls from "
        "0.451 to 0.284. That is one of only three tier moves in the "
        "stress branch. The loop set does not change — L3 was already the "
        "active mechanism and the election simply feeds it.",
 fragile="No parameter flips the verdict at ±20%, which is as robust as the "
         "OAT protocol gets. The caveat is upstream: Malaysia's Ĉ₅ is built "
         "from three ANALYST arms like everyone else's, and a fully ANALYST "
         "component that happens to be insensitive to parameter perturbation "
         "is still not a measurement.",
 watch=[
  "Whether GE16 is called early. The stress branch treats it as the single "
  "decisive 2027 event for Malaysia.",
  "Further state-level losses. Three in a row is the trend the party_frag "
  "coding rests on.",
  "Subsidy rationalisation and cost-of-living pressure, which is the live "
  "legitimacy channel rather than the ethnic one.",
  "EPF adequacy debates — the point at which a funded scheme starts "
  "generating budget claims is the point d₄ would have to be re-coded.",
 ],
 limits="Malaysia is the row where the engine's distinction between "
        "fragmentation and incoherence does most work. The reading says "
        "divided-but-functional, which is a real category and not a soft "
        "version of crisis.",
),

# ===========================================================================
"MM": dict(
 title="The gate is shut; the question is what follows",
 lede=[
  "Myanmar is the only polity in the eleven with a θ₂₅ gate already CLOSED. "
  "Ŝ₂ is below its 0.25 PAPER threshold, so θ₂₅ has collapsed to 0.127 and Ψ "
  "with it, to 0.008 — two orders of magnitude below anything else in the "
  "region. The Monte-Carlo pass returns Equilibrium 100%, which is not "
  "stability. There is nothing left to vary.",
 ],
 body=[
  "The gate that closed is the violent one, not the fiscal one. Degrow's two "
  "channels terminate in the same object — θ₂₅ — through different doors: the "
  "voluntary, aging door closes Ŝ₅, and the violent, youth door closes Ŝ₂. "
  "Thailand is walking toward the first. Myanmar has already gone through the "
  "second. Ŝ₅ remains 106 years away and is irrelevant.",

  "The input that drives this is a conflict coding of 0.95, and it is worth "
  "being precise about what that asserts. It is not a claim about who is "
  "winning. It is the statement that no actor holds a monopoly. BTI 2026 puts "
  "junta authority as contested in over two-thirds of the territory with more "
  "than half of 330 townships in active conflict; stable Tatmadaw control was "
  "put at between 72 and 220 of those townships as of December 2025; the "
  "Arakan Army holds most of Rakhine; three regional commands have fallen. "
  "The December 2025 phased election changed the legal claim to authority, "
  "not the control map.",

  "Administrative penetration is 0.089 and legitimacy 0.139 — both effectively "
  "at the model floor after boundary compression. Three loops run (L2, L3, "
  "L6) but the loop set is almost beside the point: with θ₂₅ at 0.127, Ψ "
  "cannot recover through any of the channels the loops operate on.",

  "One negative result deserves stating, because the row was built to test "
  "it. **L8, the Youth-Surplus Discharge, does NOT fire.** L8 exists so the "
  "instrument can read young societies at all, and Myanmar is the obvious "
  "candidate. But d₅ computes to 0.495, below the activation threshold, "
  "because Myanmar's measured youth indicators — NEET at 15.0%, youth "
  "dependency 35.2 — are middling by regional standards; Laos and Timor-Leste "
  "both score far higher. The engine is saying that Myanmar's catastrophe is "
  "not demographic. It is a coercive-monopoly failure that happens to be "
  "occurring in a young country, and the youth-surplus mechanism is not what "
  "is driving it. Whether that is a correct reading or an artifact of the d₅ "
  "threshold is a live question, and `d5_violent_thresh` is one of the two "
  "parameters that flips this verdict.",
 ],
 stress="Relief-system failure and a further currency break — 22% inflation "
        "in 2025 is the baseline — move Ψ from 0.008 to 0.007. The stress "
        "branch is almost meaningless here, and deliberately so: civil "
        "conflict was NOT added as an event, because conflict at 0.95 already "
        "says what there is to say, and adding it would charge the coup twice.",
 fragile="Two parameters flip the verdict, and one of them is the d₅ "
         "threshold that decides the L8 question above. The deeper limitation "
         "is data: Myanmar's fiscal series is the weakest in the set — the "
         "last usable tax-to-GDP observation is 2019, pre-coup — so every "
         "fiscal reading here inherits a seven-year-old baseline.",
 watch=[
  "Township control counts, not territorial percentages. Ŝ₂ is about monopoly "
  "and the township series is the closest observable.",
  "Whether the post-election administration extends actual service delivery "
  "anywhere. Ŝ₄ at 0.089 is the floor, and it is the variable with room to "
  "move first.",
  "Kyat and inflation. 22% in 2025 with a₄ at 0.78 is the extraction base "
  "disappearing in real time.",
  "Whether youth mobilisation becomes a driver in its own right — the L8 "
  "question the engine currently answers 'no' to.",
 ],
 limits="An Equilibrium band here is a mathematical artifact of Δ_norm being "
        "small because BOTH S and C have collapsed, not a statement that "
        "anything is balanced. Read the tier and θ₂₅, not the band.",
),

# ===========================================================================
"KH": dict(
 title="No loop running, and the shortest fuse but one",
 lede=[
  "Cambodia reads Equilibrium / Coherent through 2027 with no active loop at "
  "all — and yet its Ŝ₃ gate is eight years out, the second-shortest in the "
  "region, and the fifteen-year reading is Crisis / Incoherent. It is the "
  "largest gap in the set between how settled a polity looks now and where "
  "its drifts point.",
 ],
 body=[
  "The absence of loops is genuine, not an oversight. L1 does not arm because "
  "the coercive monopoly is intact; L3 does not arm because fragmentation is "
  "0.22, among the lowest here — the opposition was dismantled, so there is "
  "little left to fragment; L6 does not arm because haven reallocation at "
  "0.42 sits below the 0.55 trigger despite an extraction squeeze of +0.202. "
  "A polity can be in poor structural condition and still show no running "
  "feedback, and Cambodia is the clearest example in the region.",

  "What the engine does register is capital concentration. Ĉ₁ is 0.63 with a "
  "crony coding of 0.90, the highest in the set, and V-Dem's political-"
  "corruption index at 0.904 is the second worst of the eleven. The oknha "
  "system ties licence to patronage directly. Chinn-Ito puts capital-account "
  "openness at 1.00 — fully open de jure, so capital controls are zero — in a "
  "dollarised economy. Concentrated capital with an unobstructed exit is a "
  "configuration the engine watches, and it is why L4's capital threshold is "
  "one of the two parameters that flips this verdict.",

  "The conflict coding of 0.22 is non-zero for a reason a state-based "
  "conflict series would miss. The scam compounds are armed, extraterritorial "
  "and — on the Prime Minister's own February 2026 account — destroying the "
  "legal economy; a US Institute of Peace estimate put the revenue at over "
  "$12.5bn a year, which he disputed. A seven-month campaign reported 5,106 "
  "arrests and 4,534 deportations. Whatever the true figure, an armed "
  "parallel economy operating inside the territory is a rival to the coercive "
  "monopoly, and that is what Ŝ₂ measures.",

  "External pressure is coded at 0.58, the second-highest here after Myanmar, "
  "and it is the Thai border: two rounds of fighting in 2025, a 27 December "
  "ceasefire that Stratfor rated as holding but not normalising in August "
  "2026, and Thai forces on ground Phnom Penh calls occupied.",
 ],
 stress="Cambodia produces the one genuinely counter-intuitive result in the "
        "whole run: under the stress branch Ψ RISES, from 0.749 to 0.842. The "
        "cause is the event catalogue's coding of interstate_war_onset, which "
        "raises Ŝ₂ and Ŝ₃ — the rally effect sccd Part V documents for "
        "1941–45. A border escalation, on the engine's own logic, "
        "consolidates a patrimonial state in the short run. That is the "
        "engine's reading and not mine, and it is exactly the kind of result "
        "worth leaving visible rather than smoothing away.",
 fragile="Two parameters flip the verdict. The input weakness is sharper than "
         "the parameter weakness here: Cambodia has no WDI Gini observation "
         "in the 2012–2026 window, so the capital-concentration term uses an "
         "argued 30.5 that is almost certainly a floor — consumption Ginis "
         "badly understate concentration where the top of the distribution is "
         "informal.",
 watch=[
  "The Ŝ₃ path. Eight years to the 0.30 floor is the second-shortest fuse in "
  "the region and nothing in the 2027 reading reflects it yet.",
  "Scam-economy enforcement, and specifically whether it reaches the "
  "patronage layer or stays at the arrest-and-deport level.",
  "Border normalisation versus the current frozen state. The engine says "
  "escalation helps in the short run; it says nothing kind about the medium.",
  "Any sign of capital leaving. Openness is 1.00 and concentration is high; "
  "there is no friction in the way.",
 ],
 limits="Coherent here means the state can act consistently, which in a "
        "patrimonial system includes acting consistently in its own "
        "interest. The tier is not a performance rating.",
),

# ===========================================================================
"LA": dict(
 title="Six years to the legitimacy floor",
 lede=[
  "Laos has the shortest fuse in the region: Ŝ₃ reaches its 0.30 PAPER floor "
  "in about six years on current drifts. It reads Equilibrium / Coherent "
  "through 2027 with one loop running, and VIOLENT-ADJUSTMENT EXPOSED as its "
  "mode — one of only two polities in that category. At fifteen years the "
  "reading is Crisis / Incoherent.",
 ],
 body=[
  "This is the clearest L6 case in the region on measured numbers alone, with "
  "the least interpretive work required. The IMF's February 2026 Article IV "
  "calls public debt unsustainable and the country in external and overall "
  "debt distress — even though the debt-to-GDP ratio is falling, from 80.6% "
  "in 2025 to a projected 68.6% by 2027. Inflation returned to around 10% by "
  "April 2026 after two episodes above 20% inside four years. The US State "
  "Department's 2026 investment statement holds that IMF figures undercount "
  "the liabilities to China.",

  "Against that, social protection covers 2.2% of the population and pension "
  "coverage 2.2%. There is essentially no buffer between a household and a "
  "price shock. That combination — a state under extraction pressure and "
  "households with no institutional protection — is why haven reallocation is "
  "coded at 0.58, above the L6 trigger. Two episodes of 20–30% inflation "
  "inside four years teach a household what the kip is worth, and the "
  "response is to hold something else.",

  "The adjustment mode is the other thing to notice. Laos routes its "
  "adjustment pressure down the violent channel because d₃, adjustment "
  "autonomy, is 0.19 — the second-lowest in the region. That variable is the "
  "router: it measures the availability and use of voluntary instruments, "
  "contraception and financial planning and welfare substitution for old-age "
  "support. Where those are absent, Degrow's model says pressure discharges "
  "the ancient way. Laos's d₁ carrying-capacity load is 0.84 and d₅ surplus "
  "youth 0.80, both among the highest here.",

  "The unrest drawdown is set at 0.10 rather than zero, and the reasoning is "
  "worth stating because it is not obvious: there is no protest channel in "
  "Laos, so the legitimacy drawdown does not surface as visible unrest. It "
  "surfaces as exit and informality instead. Vulnerable employment is 76.4%, "
  "the highest in the region by a wide margin.",
 ],
 stress="A debt event on liabilities the IMF already calls unsustainable, "
        "plus inflation back through 10%, takes Ψ from 0.721 to 0.608 without "
        "moving the verdict. Laos has more short-run absorption than its "
        "fundamentals suggest, largely because fragmentation is very low "
        "(Ĉ₅ = 0.19) and Ψ carries a (1−C₅) factor.",
 fragile="One parameter flips the verdict: a4_flight_thresh, which switches "
         "L6 off. So the single mechanism the engine identifies for Laos "
         "rests on one ANALYST threshold. The measured fiscal distress is "
         "not in question; whether it expresses itself as the legibility "
         "spiral specifically is.",
 watch=[
  "Inflation. It is both the extraction squeeze and the haven driver, and it "
  "is the most frequently published number Laos produces.",
  "Any restructuring of the China-held debt, and whether the terms become "
  "public. The State Department's claim that the obligations are undercounted "
  "is the largest unknown in this row.",
  "Social-protection coverage off a 2.2% base. Movement here would be the "
  "single most load-bearing change available to the Lao state.",
  "Labour outflow to Thailand. The engine's talent gradient scores LA→TH as "
  "the strongest pair in the region.",
 ],
 limits="A Coherent tier in 2027 alongside a six-year Ŝ₃ gate is not a "
        "contradiction — it is the engine distinguishing present consistency "
        "from the direction of travel. Reading only the 2027 band would miss "
        "the entire Laos story.",
),

# ===========================================================================
"TL": dict(
 title="The freest and the poorest, in the same row",
 lede=[
  "Timor-Leste reads Negotiated / Coherent through 2027 with no active loop, "
  "and no parameter flips its verdict at ±20%. It also carries the highest "
  "carrying-capacity load in the region (d₁ = 0.91), the second-highest "
  "surplus-youth score (d₅ = 0.79), and the largest extraction squeeze of all "
  "eleven (+0.580). Those sit together, and the pairing is the point.",
 ],
 body=[
  "On every civic measure Timor-Leste leads the region outright. RSF ranks it "
  "30th of 180 in 2026 — ahead of every other ASEAN member and most of Europe "
  "— and V-Dem's liberal-democracy score of 0.549 is nearly double "
  "Indonesia's. Civil organisation reads 0.73 and information autonomy 0.68, "
  "both the highest here. It joined ASEAN as the eleventh member on 26 "
  "October 2025.",

  "It is also the poorest by a wide margin at $4,810 PPP per head, with NEET "
  "at 29.1% and youth dependency at 53.7 — the highest in the region. That "
  "combination, high Ĉ₂ and Ĉ₃ with low Ŝ₁ and high d₅, is not a contradiction "
  "in the model. It is a specific and recognisable configuration: a state "
  "with genuine civilian capacity and very little fiscal capacity, carrying a "
  "young population it cannot yet employ.",

  "The binding fact is that the Petroleum Fund, not tax, pays for the state. "
  "Expenditure runs near 60% of GDP against domestic revenue of about 22%, "
  "financed by Fund withdrawals above the Estimated Sustainable Income. That "
  "is what produces the largest extraction squeeze in the set: demanded 0.628 "
  "against feasible 0.048. And yet L6 does not arm, because the second "
  "condition is not met — haven reallocation is 0.20, the lowest of the "
  "eleven. The squeeze is real and the legibility response is absent.",

  "That non-firing is the most instructive single result in the Timor-Leste "
  "row, and it cuts both ways. Read generously, it says the Lao-style "
  "household flight into non-legible stores of value has not started here. "
  "Read sceptically, it says a₄ = 0.20 is an analyst estimate for a country "
  "with no WGC coverage at all, and the engine is reporting the absence of a "
  "number as the absence of a phenomenon.",

  "The adjustment mode is VIOLENT-ADJUSTMENT EXPOSED, as in Laos, and for the "
  "same structural reason: d₃ is 0.15, the lowest in the region, so pressure "
  "routes down the ancient channel. Modern contraceptive prevalence is 24.1%, "
  "against 70.7% in Thailand.",
 ],
 stress="Petroleum Fund drawdown outrunning the ESI, plus a youth-employment "
        "shock on a 29.1% NEET base, takes Ψ from 0.826 to 0.621 — a 25% "
        "fall, the fourth-largest proportional hit in the region after "
        "Thailand, the Philippines and Malaysia — without moving the "
        "verdict. At fifteen years the "
        "reading is Equilibrium / Incoherent.",
 fragile="No parameter flips the verdict at ±20%, but that robustness is "
         "misleading here because the input quality is the weakest in the "
         "set. Timor-Leste has no Chinn-Ito observation, no WGC gold data, no "
         "contraceptive series after 2016, and its Ŝ₁ is built on a 2022 "
         "tax-to-GDP figure that both overstates extraction CAPACITY and "
         "understates current resources, because the Fund transfer is not tax.",
 watch=[
  "The Petroleum Fund withdrawal rate against the ESI. This is the whole of "
  "Ŝ₁ and Ŝ₅ for this polity and almost nothing else.",
  "Whether any domestic non-oil revenue base develops. ASEAN accession is the "
  "obvious vehicle and the clock on it is long.",
  "Youth employment against a 29.1% NEET base, which is what d₅ is reading.",
  "Any sign of household reallocation into gold or foreign currency. a₄ = "
  "0.20 is an estimate, and L6 switching on would change this row completely.",
 ],
 limits="The smallest systemic weight in the set (0.0013) means Timor-Leste "
        "contributes almost nothing to Ψ_G. That is a statement about GDP "
        "share and nothing else; the per-polity reading stands on its own.",
),

# ===========================================================================
"BN": dict(
 title="Slack, and one commodity away from not being",
 lede=[
  "Brunei posts the highest Ψ in the region at 1.65, reads Hegemonic / "
  "Coherent with no active loop, and has a nearest gate 126 years out. Its "
  "adjustment mode is SLACK — the only polity in the eleven in that category, "
  "meaning the engine finds no adjustment pressure requiring discharge at "
  "all. It is also the row where one event changes the mode.",
 ],
 body=[
  "The numbers are what a hydrocarbon rentier monarchy produces. Fiscal "
  "extraction reads 0.81 and coercive monopoly 0.90, both the highest or "
  "near-highest here, on WGI political stability at the 92nd percentile. "
  "Fragmentation is 0.12, the lowest of the eleven — there is no legislature "
  "to fragment, no legal parties, and a state of emergency continuous since "
  "1962. Legitimacy reads 0.75, second only to Singapore.",

  "Capital concentration is coded at 0.46 with a crony factor of 0.70, and "
  "the justification is different from everywhere else in the set. It is not "
  "lobbying — there is no register and no mechanism — it is fusion. The royal "
  "household, the sovereign fund and the state are not separable entities, "
  "which is the politically-activated-capital construct in its purest form. "
  "The engine's proxy was designed for lobbying registers and does not fit; "
  "the number is argued.",

  "Where the exposure sits is Ŝ₁ and Ŝ₅, and the engine shows it without "
  "firing a loop. The extraction squeeze is +0.285 — demanded 0.322 against "
  "feasible 0.037 — which is in the same range as Thailand's and the "
  "Philippines'. L6 does not arm only because haven reallocation is 0.25, "
  "well below the trigger. So the fiscal pressure is present and the "
  "legibility response is not: a rentier state does not need to chase a "
  "disappearing tax base, because it was never taxing one.",

  "The vulnerability is single-commodity and it is visible in the growth "
  "figure, not in any structural term. 2025 GDP growth was 0.7% — the lowest "
  "in the region by a wide margin, in a year when Viet Nam posted 8.0% and "
  "Timor-Leste 7.0% — on a maturing field base. Brunei's problem is not "
  "polarisation, legitimacy or coercive capacity. It is that one price "
  "determines the whole revenue side, and the engine's structural vocabulary "
  "has no term for that.",
 ],
 stress="An energy-price shock at 0.60 moves the adjustment mode from SLACK "
        "to VOLUNTARY — the only mode change anywhere in the stress branch. Ψ "
        "barely moves (1.651 to 1.613) and the band and tier hold. That is "
        "the engine saying something quite precise: an oil undershoot does "
        "not threaten Brunei's structure, it ends the condition of having no "
        "adjustment pressure at all. For a state that has never had to run an "
        "adjustment, that transition is the thing to watch, not the Ψ level.",
 fragile="No parameter flips the verdict, as with Malaysia and Timor-Leste. "
         "The real "
         "weakness is input coverage: Brunei is absent from V-Dem entirely "
         "and from Chinn-Ito, so six of its fields — five V-Dem components "
         "plus capital-account openness — are analyst substitutes with "
         "reasons attached rather than observations. No other polity in the "
         "set has that many.",
 watch=[
  "Hydrocarbon output and price. On this reading they are effectively the "
  "entire Brunei state-capacity variable.",
  "Whether any non-hydrocarbon revenue instrument appears. Brunei has no "
  "income tax; creating one would be the single largest structural change "
  "available and would show up immediately in Ŝ₁.",
  "Sovereign fund drawdown, which is the Ŝ₅ story and is not published in a "
  "form the engine can read.",
  "Whether the SLACK-to-VOLUNTARY transition in the stress branch shows up "
  "in reality — that is a falsifiable prediction, unusually for this engine.",
 ],
 limits="Hegemonic / Coherent with Ψ at 1.65 is the strongest reading in the "
        "region, and it should be read as a statement about structural "
        "consistency, not resilience. The engine has no commodity-price term, "
        "which for this polity is the principal omission.",
),
}

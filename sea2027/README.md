# sea2027 — the eleven ASEAN states through SCCD-X v2.00

Data retrieved and run **2026-10-09**.

```bash
python sea2027/run.py                                 # Vietnamese
python sea2027/run.py --lang en --json out.json       # English + full dump
python sea2027/gen_raw.py                             # re-fetch raw_2026.py
python sea2027/make_pdf.py                            # 22 technical PDFs
python sea2027/make_prose_pdf.py                      # 22 prose PDFs
```

## Files

```
raw_2026.py   the measured panel, AUTO-GENERATED — do not hand-edit
gen_raw.py    the fetcher that writes it
judgment.py   the ANALYST overlay: one block per polity, every number argued
mapping.py    measured panel -> the ten sccd components + Blocks D and A
run.py        the run: 2027 verdict, 15-year gate order, world layer,
              stress branch, two counterfactuals
out_{vi,en}.txt      the rendered reports
sea2027_{vi,en}.json the full payload incl. provenance per derived field
make_pdf.py   22 technical PDFs, 11 vi + 11 en, into pdf/
pdf/          SCCDX-2027-<CODE>-{vi,en}.pdf, 5-6 pages each
prose_en.py   the prose reading, English - INTERPRETATION, not engine output
prose_vi.py   the same reading in Vietnamese, written rather than translated
make_prose_pdf.py  22 prose PDFs into pdf_prose/
pdf_prose/    SCCDX-2027-PROSE-<CODE>-{vi,en}.pdf, 2 pages each
```

## Two sets of PDFs, and the difference matters

`pdf/` is the **instrument's output**: tables, per-component provenance tags,
the OAT rows, gate projections, the trajectory. Sans-serif at a 170mm measure,
because it is a reference document.

`pdf_prose/` is the **argument about what that output means**. Serif at a
115mm measure with a thin strip of figures at the top so every claim can be
checked against the run that produced it. ~20,000 words across the 22.

The split is deliberate and it is the same discipline the engine keeps
internally: the engine emits codes and never a sentence, and prose lives in
one place where it can be audited. `prose_en.py` and `prose_vi.py` are
INTERPRETATION and say so on every document — a reader who accepts every
number in `pdf/` may still reject every reading in `pdf_prose/`.

The two language sets are written, not translated through each other, but
they make the same claims. If they ever diverge in substance that is a bug in
one file or the other.

## Fonts, for the PDFs

The engine emits Unicode subscripts everywhere and the Vietnamese side needs
the full Latin Extended Additional block. Two families on this machine cover
both: **DejaVu Sans** (ships with matplotlib, free licence) for body text and
**Consolas** for the tables. `DejaVuSansMono` is NOT used — it is missing 44
Vietnamese precomposed characters, every one of them a circumflex-plus-tone,
and would have dropped them silently. A reportlab built-in such as Helvetica
or Courier has neither the subscripts nor the diacritics and renders solid
boxes.

## Fixed at source: the LSODA stall was `edge()`, not the tolerance

Installing scipy — which the parent README tells you to do, because Part IV
§8.1 mandates an adaptive **stiff** solver — used to make `validate2.py` hang:
`diagnose_world(preset_polities(), 2026, horizon_years=15)` reached the JP row
and never returned.

### The first diagnosis was wrong

The initial guess was that θ₂₅'s threshold factor is near-discontinuous at the
gate. It is not: `threshold_factor` is already a product of two logistic
sigmoids with `epsilon = 0.05`, so it is C∞ and spread over a 0.2-wide band.

The real cause is `edge()` in `rhs2`, the floor/ceiling clamp that eight of
the ten states pass through:

```python
if v <= lo and dv < 0.0: return 0.0     # hard switch in the vector field
```

That is a genuine discontinuity. When a state touches its floor with an
outward drift the derivative jumps to zero; the solver steps a hair below,
the drift becomes 0, it steps back above, the drift returns, and it chatters
with the step size driven to zero. Japan parks `s5` exactly on its 0.05
floor, which is why `JP@15` was the first case to hang.

### Evidence that it is `edge()` and not the tolerance

Tuning tolerances never removed the stall, it only moved which case hit it —
a sweep over 21 polities × 5 horizons:

| setting | first case that stalls |
|---|---|
| rtol 1e-6, atol 1e-9 (as shipped) | `preset:JP@15` |
| rtol 1e-6, atol 1e-8 | `preset:RU@20` |
| rtol 1e-6, atol 1e-7 | `preset:US@20` |
| rtol 1e-7, atol 1e-8 | `preset:JP@15` |
| rtol 1e-6, atol 1e-9, max_step 0.25 | `preset:US@20` |
| rtol 1e-5, atol 1e-8 | `sea:LA@20` |

atol 1e-8 alone clears JP and max_step 0.25 alone clears JP, but the two
**together** stall on it. Knife-edge, so no constant is safe.

Making `edge()` C¹ clears **every** previously stalling case at the original
strict tolerances, with LSODA alone and no fallback ladder — at widths from
0.0005 to 0.005 alike. That is the control experiment.

### The change

`EDGE_LAYER = 0.002` in `sccdx/dynamics2.py`. The clamp is now a smoothstep
ramp over that layer:

- The invariant is unchanged: the outward drift is still **exactly** zero at
  the floor, so no state can cross it. Verified over all 126 runs.
- Outside the layer the drift is returned **bit-identical**, so a trajectory
  that never approaches a bound is completely unaffected.
- smoothstep has zero slope at both ends, so there is no kink where the ramp
  begins either.

Width chosen from the sweep: 0.0005–0.005 all work, 0.002 is the smallest
that is not hugging the discontinuous limit. The layer is 4% of the 0.05
floor, so a state is slowed only over its last 0.002 of travel.

`SOLVER_ATOL` is back to sccd's own **1e-9** — loosening it was treating a
symptom. The `STIFF_LADDER` / `SOLVER_RHS_BUDGET` guard is kept, but it now
never fires; it stays as a bound on the worst case, because the model has
other non-smooth terms (`max(.)` inside `dS` and `ds3`, the `_c()` state
clamp) that a future input could provoke.

### Result

| | before | ladder only | `EDGE_LAYER` |
|---|---|---|---|
| 126 runs (21 polities × 6 horizons, to 30 yr) | **hangs** | 11.20 s | **0.26 s** |
| worst single run | ∞ | 3.21 s | 0.008 s |
| method switches away from LSODA | — | 6 | **0** |
| tolerances | atol 1e-9 | atol 1e-8 | atol 1e-9 (original) |

- `validate2.py`: **PASS 119 / FAIL 0 / KNOWN-DEFECT 4**, matching the
  pre-scipy baseline, now with the mandated stiff solver. Full output in
  `validate2_result.txt`.
- The hard `edge()` was also costing ~40× in solver work on cases that did
  converge.
- All sea2027 outputs regenerated: **zero change, to machine precision**
  (largest |ΔΨ| = 0.00e+00). None of the eleven comes within 0.002 of a
  floor inside either window, so the layer is never entered.

`sccdx/dynamics2.py.bak` and `sccdx/i18n.py.bak` hold the pre-fix files.


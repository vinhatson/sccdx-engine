# SCCD-X Engine — Full Guide

Everything you need to run the engine, read what it says, and know what not to
claim from it. If you want the short version, the [README](../README.md) is the
short version.

**Contents**

1. [Install](#1-install)
2. [Your first run](#2-your-first-run)
3. [The ten components](#3-the-ten-components)
4. [The two new blocks](#4-the-two-new-blocks)
5. [Reading the output](#5-reading-the-output)
6. [The eight loops](#6-the-eight-loops)
7. [The HTTP API](#7-the-http-api)
8. [Using it from Python](#8-using-it-from-python)
9. [The ASEAN 2027 run](#9-the-asean-2027-run)
10. [Validation, and what the numbers mean](#10-validation-and-what-the-numbers-mean)
11. [What you may and may not claim](#11-what-you-may-and-may-not-claim)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Install

Python 3.9 or newer.

```bash
git clone https://github.com/<your-username>/sccdx-engine.git
cd sccdx-engine
pip install numpy
```

`numpy` is the only hard requirement. Two optional installs:

```bash
pip install scipy              # the stiff solver the paper actually mandates
pip install fastapi uvicorn    # only if you want api_fastapi.py instead of serve.py
```

Install `scipy` if you can. See [§12](#12-troubleshooting) for why it matters
and when it stops being optional.

### Windows note

Nothing special is needed. The entry points set their own stdout to UTF-8, so a
default `cmd.exe` or PowerShell console renders the Vietnamese and the Greek
letters correctly rather than aborting on them.

---

## 2. Your first run

```bash
python serve.py
```

Open <http://127.0.0.1:8777>. You get a single page with three tabs and a
`VI` / `EN` pair in the corner.

| tab | what it shows |
|---|---|
| **one** | one polity: inputs on the left, the diagnosis on the right |
| **world** | the polities together, weighted — the world layer |
| **audit** | every parameter, its value, and where that value came from |

Start by picking a preset from the dropdown. Ten are built in: `US`, `CN`, `EU`,
`JP`, `KR`, `IN`, `RU`, `BR`, `GB`, `NG`.

**Press the `EN` / `VI` toggle and watch the whole page change.** It is not a
translation layer in the browser — the switch re-runs the diagnosis server-side
and every string arrives from the API. The numbers are asserted identical across
the two languages; only the words differ.

Then open the **audit** tab. This is the tab that matters most, and it is the
one most people skip. It tells you which of the numbers driving your result came
from a paper and which came from an analyst's judgment. Read §11 before you
quote anything.

---

## 3. The ten components

A polity is ten capacity components, each on [0, 1]. Five sovereign (`S`), five
civilian (`C`).

| key | name | data status |
|---|---|---|
| `s1` | Fiscal Extraction Capacity | PAPER proxy |
| `s2` | Coercive Monopoly Index | PAPER proxy |
| `s3` | **Legitimacy Capital** | **BLOCKED** |
| `s4` | **Administrative Penetration Depth** | **BLOCKED** |
| `s5` | Temporal Leverage | PAPER proxy |
| `c1` | Private Capital Concentration | PAPER proxy |
| `c2` | Civil Organisation Density | PAPER proxy |
| `c3` | Information Autonomy | PAPER proxy |
| `c4` | Exit Option Availability | PAPER proxy |
| `c5` | **Preference Fragmentation** | **BLOCKED** |

**`BLOCKED` means the source paper defines no usable proxy for that component.**
There is no measurement pipeline for `s3`, `s4` or `c5` — you supply them, and
whatever you supply is a judgment.

This is not a minor gap. `s3` drives λ, the legitimacy multiplier, and λ
multiplies *all* of S. `c5` is the denominator of C *and* the `(1−c5)` factor in
Ψ. The three blocked components are disproportionately the ones the whole
non-linear core turns on.

### State type

Four types, and the choice re-weights the aggregation:

| type | w1 | w4 | ω25 |
|---|---|---|---|
| `liberal_democracy` | 0.40 | 0.35 | 0.25 |
| `developmental_autocracy` | 0.35 | 0.45 | 0.20 |
| `extractive_patrimonial` | 0.50 | 0.20 | 0.30 |
| `failed_state` | 0.60 | 0.25 | 0.15 |

The type is an input, not an output. The engine does not infer it, and changing
it changes results — so state it when you report anything.

---

## 4. The two new blocks

This is what v2.00 adds. `sccd` v1.00 left two terms of its own ODE system
exogenous:

```
dS₃/dt = **S₃_natural**    − ρ_b(1−λ/λmax)² − ζ·C₅^ψ·(S₃−S₃floor)
dC₅/dt = **C₅_structural** + ε_p·C₅(1−C₅)·RevPol + η·C₅²·C₃ + ξ·Ĉ₄Ĉ₁(1−C₅)
```

v2 supplies both starred terms from two further papers, on two different
timescales.

### Block D — demographic (`DEGROW`)

From *The Wheel of Fate*. Five inputs:

| key | name |
|---|---|
| `d1` | Carrying-Capacity Load |
| `d2` | Expectation Trap |
| `d3` | **Adjustment Autonomy** |
| `d4` | Dependency Inversion |
| `d5` | Surplus Youth Cohort |

Block D is a **router**, not another pressure. Load generates a quantity of
adjustment pressure; what the paper varies is *which channel carries it*. The
split variable is `d3`, the availability of voluntary instruments —
contraception, financial planning, risk-management thinking:

```
violent_share = (1 − d3)^route_sharpness
```

High `d3` routes pressure through voluntary adjustment. Low `d3` routes the same
pressure through the violent channel. Both of the paper's claimed phenomena —
the ancient explosion-then-collapse and the modern fertility freeze — terminate
in the same object, θ₂₅, which is what makes the claim checkable rather than
merely suggestive.

There is a choice the source paper does not settle, so the engine exposes it as
an option rather than deciding for you:

```
router_mode = "conserve"   # default: redirect the pressure
router_mode = "discount"   # also shrink it
```

*The Wheel of Fate* does not say which is right. This is logged as open problem
`OP2-1`. If your conclusion flips between the two modes, your conclusion is
about the open problem, not about the polity.

### Block A — AI adoption (`DISPL`)

From *The Displacement Hypothesis*, 2nd ed. Six inputs:

| key | name |
|---|---|
| `a1` | AI Penetration |
| `a2` | Self-Efficacy Erosion (Tier 1) |
| `a3` | Agency Erosion (Tier 2) |
| `a4` | Haven Reallocation |
| `a5` | Counter-Tech Mobilisation |
| `a6` | AI Productivity Windfall |

Note the two tiers are separate: `a2` is erosion of the *belief* that effort
works, `a3` is erosion of the *capacity* to act. The paper distinguishes them
and so does the engine.

---

## 5. Reading the output

`POST /api/v2/diagnose` returns these top-level fields:

```
country  year  state_type  verdict  capacity  capacity_base  forcing
loops  bifurcation  attractor  trajectory  horizon_verdict
uncertainty  fragility
```

### The regime bands

The headline number lands in one of five bands:

| band | range | stability |
|---|---|---|
| Imperial | 0.60 … 1.00 | Unstable (drain) |
| Hegemonic | 0.30 … 0.60 | Metastable |
| Negotiated | 0.08 … 0.30 | Conditionally stable |
| Equilibrium | −0.08 … 0.08 | Stable **or** Gridlock |
| Crisis | −0.40 … −0.08 | Unstable (bifurcation) |

Two things worth noticing. **Imperial is unstable**, not strong — it is a drain
state. And **Equilibrium is ambiguous between stable and gridlock**: the band
alone does not separate a working settlement from a frozen one, so read the
loops.

### Adjustment modes

```
VOLUNTARY   VIOLENT_EXPOSED   MIXED   SLACK
```

This is Block D's routing verdict — the channel the adjustment pressure is
taking, not how much of it there is.

### Provenance tags

Every derived field carries a tag. You will see:

- `PAPER` — the value is stated in a source paper
- `PAPER proxy` — the paper defines a measurement proxy for it
- `BLOCKED` — the paper defines no usable proxy
- `ANALYST` — someone's judgment, with a stated rationale
- `DERIVED` / `DERIVED2` — computed from other values

**Read the tags.** A result built on `ANALYST` inputs is an argument; a result
built on `PAPER` inputs is a reading of the paper. The engine never hides which
you are looking at.

### The engine emits codes, never sentences

This is a deliberate discipline, and it is worth understanding because it
explains the whole architecture. The engine returns *codes*; prose lives in one
place (`sccdx/i18n*.py`, and `sea2027/prose_*.py` for the ASEAN run) where it
can be audited against the run that produced it.

That is why `web/index.html` contains zero Vietnamese characters, and why there
is a test that fails if it ever does.

---

## 6. The eight loops

Eight named feedback loops. The first six are v1; `L7` and `L8` come from
Block D.

| loop | name |
|---|---|
| `L1` | Regulatory Capture Accelerator |
| `L2` | Legitimacy Death Spiral |
| `L3` | Polarisation Trap |
| `L4` | Exit-Fragmentation Coupling |
| `L5` | Agency-Legitimacy Spiral |
| `L6` | Legibility-Extraction Spiral |
| `L7` | Demographic Inversion Trap |
| `L8` | Youth-Surplus Discharge |

Each reports whether it is active and why. A loop activating is usually more
informative than the headline number moving, because the loop tells you *which
mechanism* is doing the work.

Be aware of a structural caveat here — see `INC-9` in §10. As the v1 equations
are written, `C₁` is exogenous, which means `L1` and `L4` are **open**, not
closed. The engine reproduces this faithfully instead of silently fixing it. If
you want the closed version, pass `c1_dynamic=True`.

---

## 7. The HTTP API

`serve.py` needs only `numpy`. It serves the page and the API on port 8777.

### Reference endpoints (GET)

Every one takes `?lang=vi|en`.

```bash
curl http://127.0.0.1:8777/api/v2/health
curl "http://127.0.0.1:8777/api/v2/schema?lang=en"      # inputs, bands, loops, options
curl "http://127.0.0.1:8777/api/v2/presets?lang=en"     # the ten built-in polities
curl "http://127.0.0.1:8777/api/v2/events?lang=en"      # the 50 events
curl "http://127.0.0.1:8777/api/v2/audit?lang=en"       # every parameter + provenance
```

`health` tells you which solver is live:

```json
{"ok": true, "engine": "SCCD-X", "langs": ["vi", "en"],
 "sccd_spec": "1.00", "sccdx_spec": "2.00",
 "ode_backend": "scipy", "python": "3.12.10", ...}
```

### Diagnosis endpoints (POST)

```bash
curl -X POST http://127.0.0.1:8777/api/v2/diagnose \
     -H "Content-Type: application/json" \
     -d '{"lang":"en"}'

curl -X POST http://127.0.0.1:8777/api/v2/world \
     -H "Content-Type: application/json" \
     -d '{"lang":"en"}'
```

Send the component values in the body to diagnose your own polity rather than a
preset. Use `/api/v2/schema` to see every accepted key, its range and its
default.

### The FastAPI alternative

```bash
pip install fastapi uvicorn
python api_fastapi.py
```

Same engine, OpenAPI docs, ASGI app. Use it if you are mounting this inside
something else. `serve.py` is the primary server and has no such dependency.

---

## 8. Using it from Python

The web layer is a thin shell over importable packages.

```python
from sccd.dynamics import simulate
from sccd.spec import KNOWN_INCONSISTENCIES

# the v1 inconsistencies, machine-readable
for inc in KNOWN_INCONSISTENCIES:
    print(inc)
```

`simulate` takes the sub-components, a context, and these arguments:

```python
simulate(sc, ctx,
         years=10.0,
         t0=0.0,
         params=None,
         state_type="liberal_democracy",
         method="LSODA",        # falls back if scipy is absent
         n_out=200,
         patch=None,
         c1_dynamic=False)      # True promotes C1 to a 5th state variable
```

`c1_dynamic` is the switch that closes the feedback loop `INC-9` describes:

- `c1_dynamic=False` → 4 states `[S, C, S₃, C₅]`, eq (NL) / INT §7.1 **as
  written**
- `c1_dynamic=True` → 5 states `[S, C, S₃, C₅, C₁]`, using Part IV §2.1's own
  equation

The default is `False` because that is what the paper's §7.1 says. The honest
version of the model is arguably `True`. Both are available; the default is
fidelity, not correctness.

For v2, see `sccdx.dynamics2.simulate2` and `sccdx.integrate.best_solver`.

---

## 9. The ASEAN 2027 run

A complete worked application: all eleven ASEAN polities, data retrieved
2026-10-09.

```bash
python sea2027/run.py                                 # Vietnamese
python sea2027/run.py --lang en                       # English
python sea2027/run.py --lang en --json out.json       # + full dump
python sea2027/run.py --mc 2000                       # more Monte Carlo draws

python sea2027/make_pdf.py                            # 22 technical PDFs
python sea2027/make_prose_pdf.py                      # 22 prose PDFs
```

The run produces: the 2027 verdict, a 15-year gate order, the world layer, a
stress branch, and two counterfactuals.

### The files

```
raw_2026.py   the measured panel — AUTO-GENERATED, do not hand-edit
gen_raw.py    the fetcher that writes it (needs the raw source files)
judgment.py   the ANALYST overlay: one block per polity, every number argued
mapping.py    measured panel -> the ten components + Blocks D and A
run.py        the run itself
out_{vi,en}.txt       the rendered reports
sea2027_{vi,en}.json  the full payload, incl. provenance per derived field
prose_{en,vi}.py      the prose reading — INTERPRETATION, not engine output
```

Note `gen_raw.py` needs raw source files (`wb.json`, `wgi.json`, `imf.json`,
`libdem.csv`, …) that are **not** in the repository. `raw_2026.py` is the
committed output of a run that had them. You do not need to re-fetch to use the
engine.

### Two sets of PDFs

44 PDFs ship pre-built, in two sets, and the difference is the point:

- `pdf/` — the **instrument's output**. Tables, per-component provenance tags,
  OAT rows, gate projections, trajectory. Sans-serif at a 170mm measure, because
  it is a reference document. 5–6 pages each.
- `pdf_prose/` — the **argument about what that output means**. Serif at 115mm
  with a thin strip of figures at the top so every claim can be checked against
  the run behind it. 2 pages each, ~20,000 words across the 22.

`prose_en.py` and `prose_vi.py` are **INTERPRETATION** and say so on every
document. The Vietnamese prose is written, not translated.

### `judgment.py`

Read this file before trusting any ASEAN number. It is an explicit analyst
overlay: one block per polity, every value argued in place. It is a judgment and
it is labelled as one. Disagree with it in an issue rather than treating it as
measurement.

---

## 10. Validation, and what the numbers mean

```bash
python validate2.py       # the main suite
python validate_v1.py     # the v1 inconsistency report
```

The correct result for `validate2.py` is:

```
PASS 119   FAIL 0   KNOWN-DEFECT 4
```

**`KNOWN-DEFECT 4` is not four failures.** Those four lines record that the
engine faithfully reproduces a defect that `sccd.spec.KNOWN_INCONSISTENCIES`
already documents. If that count changes, something changed in the engine's
fidelity to the paper — in either direction, it wants investigating.

### What the 119 checks cover

Numerics, loop activation, gate ordering, bifurcation detection — and a block
of language-parity checks that are stricter than most bilingual projects
bother with:

- all 406 templates have both a Vietnamese and an English side
- all 160 UI strings have both sides
- a missing i18n key **raises** rather than silently rendering English
- all 50 events have a Vietnamese note; every event has a label in both
- all 10 presets have a Vietnamese rationale
- all 7 v2 open problems and all 9 v1 inconsistencies are translated
- all 46 v2 parameter notes are translated
- `web/index.html` holds **zero** Vietnamese characters
- the page exposes two separate language tabs, fetches with a `lang` parameter,
  and **re-runs the diagnosis** on a language switch
- the trajectory, the numeric results and the fragility verdict are identical
  across languages

`validate_lang.py` holds these checks but is **a module, not an entry point**.
Running it directly prints nothing and exits 0 — that is not a bug.
`validate2.py` calls it.

### The v1 inconsistencies

`validate_v1.py` prints the source model's own problems rather than patching
them. Three are `CRITICAL`:

- **INC-7** — `dC₅/dt`: all three endogenous terms are positive and there is no
  depolarisation term, even though §2.3 defines the L3 activation test against a
  'Natural_Depolarisation_Rate'. As written, C₅ increases monotonically toward 1
  on **every** trajectory, hence Ψ = λ·θ₂₅·(1−C₅) → 0 regardless of scenario.
  *Proposed fix: add* `−ν·C₅` *or* `−ν·C₅·C₂`.
- **INC-8** — `dS₃/dt`: both endogenous terms are negative, so with `S₃_natural`
  exogenous, S₃ can only decay. The model cannot generate the legitimacy
  reconstitution Part V documents for 1980–86 (λ 1.2 → 1.7) or the 1941–45
  build-up, even though §2.2 names a 'natural legitimacy recovery' rate that
  never enters the ODE.
- **INC-9** — §2.1 writes `dC₁/dt` explicitly, but §7.1 omits `C₁` from the
  state vector. With `C₁` exogenous, neither `dS₃/dt` nor `dC₅/dt` depends on S
  or C, so `[S₃,C₅]` is an **autonomous subsystem** driving `[S,C]` one-way.
  There is no closed feedback loop in eq (NL) at all. The diagnostic is that
  every scenario gives identical `C₅(t)` and `Ψ(t)`.

That last one is the big one, and it is why `c1_dynamic=True` exists.

---

## 11. What you may and may not claim

The engine states its own epistemic status at the end of every validation run:

```
36 of 83 v1 parameters carry a value from the source paper; 46 do not.
ALL 46 v2 parameters are ANALYST or DERIVED2 — the two new papers are
qualitative and state no coefficients. Read every v2-dependent output as
ORDINAL: a ranking and a threshold-crossing map, not a level.
```

So, concretely.

**You may:**
- compare two polities and report which ranks higher on a given measure
- report that a threshold is crossed, or the order in which gates fall
- report which loops activate, and which mechanism carries a result
- report that a conclusion is or is not robust to `router_mode`
- quote any `PAPER` value, with its citation

**You may not:**
- quote a v2-derived number as a level, magnitude or probability
- report a date as a forecast
- treat the ten built-in presets as measurements — the payload's own disclaimer
  says only four values in the whole file are paper-stated (US `s3`=0.38,
  `c5`=0.74, `c1`=0.82, `s2`≈0.90), nothing was produced by running the Part III
  proxy pipeline, and no value carries a confidence interval
- treat `sea2027/judgment.py` as measurement
- ignore the state type when reporting — it re-weights the aggregation

If a conclusion survives both `router_mode` settings, both `c1_dynamic`
settings, and a sweep of the `BLOCKED` components, then you have something
structural. That is the standard this engine is built to support, and it is
worth more than a number with false precision.

---

## 12. Troubleshooting

**`ModuleNotFoundError: No module named 'numpy'`**
`pip install numpy`.

**`"ode_backend": "dp45"` in `/api/v2/health`**
`scipy` is not installed. The engine fell back to the explicit DP45 in
`sccdx/integrate.py` and reported it in `trajectory.solver` and the returned
notes — it did not hide it.

DP45 is **not** a stiff solver. Part IV §8.1 mandates an adaptive stiff solver
and names LSODA, Radau and BDF. DP45 tracks this system to about 1e-6 at the
coefficient magnitudes in `spec`/`spec2`, which is fine for exploration. Install
`scipy` before you raise any rate by an order of magnitude or add sub-year shock
pulses — past that point the fallback is no longer adequate:

```bash
pip install scipy
```

**`python validate_lang.py` prints nothing**
Correct behaviour. It is a module, not an entry point. Run `validate2.py`.

**`python sea2027/gen_raw.py` fails on a missing file**
Expected. It needs raw source files that are not in the repository.
`raw_2026.py` is already the committed output.

**Port 8777 in use**
Edit the port in `serve.py`, or stop whatever holds it.

**The page shows English after I pressed `VI`**
That should be impossible — a missing i18n key raises rather than falling back.
If you see it, that is a real bug: please open an issue with the exact input.

**Unicode errors in the console**
Should not happen; the entry points set their own stdout to UTF-8. If you hit
one, report the OS, terminal and Python version — and as a workaround set
`PYTHONIOENCODING=utf-8`.

---

## See also

- [README.md](../README.md) — the short version
- [README.vi.md](../README.vi.md) — bản tiếng Việt
- [GUIDE.vi.md](GUIDE.vi.md) — this guide in Vietnamese
- [engine-notes-en.md](engine-notes-en.md) — the four structural results, in depth
- [../sea2027/README.md](../sea2027/README.md) — the ASEAN run, file by file

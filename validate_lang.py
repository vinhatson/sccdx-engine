# -*- coding: utf-8 -*-
"""
SCCD-X — Validation: language separation
=========================================
Section E of the suite, split into its own file because it is the only part
that needs the Unicode class tables.

The requirement under test is strict: pressing VI gives a page with no
English in it, pressing EN gives a page with no Vietnamese. These checks are
mechanical rather than impressionistic - they walk the WHOLE payload and look
for characters and marker phrases belonging to the other language, rather than
spot-checking a few headings.

The marker phrases are drawn from ENGINE output - loop details, gate
meanings, calibration warnings - not from the page chrome, because the chrome
was never the part that leaked. Before the i18n refactor the page was
Vietnamese in its headings and English in every string the engine produced,
and a test that only looked at headings would have passed.
"""
from __future__ import annotations

import os
import re
from typing import Any, List, Tuple

import serve as SRV
from sccd import spec as s1spec
from sccdx import spec2
from sccdx import i18n as I18N
from sccdx.events import CATALOGUE, catalogue as _event_catalogue
from sccdx.i18n_long import (EVENT_NOTES, INCONSISTENCIES, OPEN_PROBLEMS,
                             PARAM_NOTES, PRESET_RATIONALE)
from sccdx.i18n_render import localize_events
from sccdx.i18n_ui import UI as UI_TABLE
from sccdx.presets import BY_CODE as PRESET_CODES

VIET_CHARS = re.compile(
    "[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ"
    "ùúủũụưừứửữựỳýỷỹỵđĐ]", re.I)

# Phrases that only an English rendering would contain.
EN_MARKERS = [
    "threshold gate", "gate closes", "adjustment mode", "loops active",
    "legitimacy death spiral", "voluntary/aging", "violent/youth",
    "CALIBRATION TAGS", "Trajectory is a STRUCTURAL", "parameter(s) flip",
    "uncommitted revenue", "squeeze=", "vs crit", "physical share",
    "crossed during run", "measured over first", "is not installed",
    "the engine cannot", "Do not switch on", "ADDED ON TOP",
    "Every effect magnitude", "not measurements", "the whole page",
]

# Identifiers that are the SAME in both languages by design - see the
# CONVENTIONS block in spec2.py. Status tags, variable names and paper
# references must read identically so a reader comparing two runs can line
# them up.
SHARED_IDENTIFIERS = [
    "PAPER", "FREE", "ANALYST", "DERIVED2", "DERIVED", "BLOCKED",
    "UNCALIBRATED-EXT", "UNCALIBRATED", "CALIBRATED",
    "sccd", "SCCD", "Degrow", "DEGROW", "DISPL", "Displacement",
    "Wheel of Fate", "spec2", "spec", "OP2-", "INC-", "Part ", "eq ",
    "Table", "api_readiness", "router_mode", "haven_single_channel",
    "faithful_v1", "c1_dynamic", "patch", "Chinn-Ito", "V-Dem", "WID",
    "OECD", "UCDP", "SIPRI", "WGI", "DIOC", "GDELT", "IMF", "Cronbach",
    "Monte Carlo", "LSODA", "Radau", "BDF", "DP45", "scipy", "numpy",
    "Malthus", "Luddism", "Seoul", "Ming", "Qing", "Kangxi", "Qianlong",
    "Pax Romana", "Thucydides", "Sync_Risk", "CAI", "T_trap", "R_B",
    "theta25", "Psi", "Delta", "lambda", "tau_", "nu_", "sigma_", "zeta_",
    "compress_s5", "Bandura", "ETF", "PAYG", "GDP", "AI", "UHNW",
]

# Keys whose values are identifiers or codes, not prose. These are meant to
# be identical across languages, so finding "below" in them is not a leak.
CODE_KEYS = {
    "regime", "stability", "coherence_tier", "adjustment_mode", "gate_code",
    "name_key", "detail_key", "source_key", "meaning_key", "how_key",
    "direction_key", "interpretation_key", "epistemic_limit_key",
    "rationale_key", "d_delta_dt_source_key", "d_gap_dt_source_key",
    "note_key", "cai_core_band_key", "cai_core_horizon_key",
    "cai_ext_band_key", "cai_ext_horizon_key",
    "status", "threshold_status", "id", "code", "group", "loop",
    "parameter", "name", "src", "variable", "direction", "how", "method",
    "solver", "lang", "state_type", "provenance", "most_likely", "message",
    "confidence", "router_mode", "field", "from", "to", "side",
    # reference rows that quote the papers verbatim in English on purpose
    "label_en", "note", "issue", "where", "rationale", "case", "metric",
    "value", "stage", "k", "v", "expected_width_note",
}


# A language picker labels each language in its OWN name - "Tiếng Việt" stays
# Vietnamese on the English page, the same way a variable name stays put.
# Translating an autonym would make the picker harder to use for exactly the
# reader who needs it.
AUTONYM_PATHS = (".ui.lang.vi", ".ui.lang.en")


def walk_strings(o: Any, path: str = "", out: List[Tuple[str, str]] = None):
    if out is None:
        out = []
    if isinstance(o, str):
        if len(o) > 3 and path not in AUTONYM_PATHS:
            out.append((path, o))
    elif isinstance(o, dict):
        for k, v in o.items():
            if k.endswith("_key") or k in CODE_KEYS:
                continue
            walk_strings(v, f"{path}.{k}", out)
    elif isinstance(o, (list, tuple)):
        for i, v in enumerate(o):
            walk_strings(v, f"{path}[{i}]", out)
    return out


def _strip_shared(txt: str) -> str:
    for a in SHARED_IDENTIFIERS:
        txt = txt.replace(a, " ")
    return txt


def run(chk, section) -> None:
    section("E. LANGUAGE SEPARATION — VI all Vietnamese, EN all English")

    body = {"preset": "US", "year": 2026, "horizon_years": 15,
            "with_sensitivity": True,
            "events": [{"id": "haven_flight_surge", "intensity": 0.8},
                       {"id": "housing_affordability_crisis",
                        "intensity": 0.9}]}
    P = {}
    for lg in ("vi", "en"):
        b = dict(body); b["lang"] = lg
        P[lg] = SRV._do_diagnose(b)
        P[lg + "_world"] = SRV._do_world({"year": 2026, "lang": lg,
                                          "codes": ["US", "JP", "NG"]})
        P[lg + "_schema"] = SRV._schema(lg)
        P[lg + "_audit"] = SRV._audit(lg)
        P[lg + "_events"] = localize_events(_event_catalogue(), lg)
        P[lg + "_presets"] = SRV.preset_json()

    # --- EN payloads: zero Vietnamese characters anywhere ---
    for tag in ("en", "en_world", "en_schema", "en_audit", "en_events"):
        hits = [(p, s[:70]) for p, s in walk_strings(P[tag])
                if VIET_CHARS.search(s)]
        chk(f"EN payload {tag!r}: zero Vietnamese characters",
            not hits, got=hits[:3])

    # --- VI payloads: zero English marker phrases ---
    for tag in ("vi", "vi_world", "vi_schema", "vi_audit", "vi_events"):
        hits = []
        for pth, s in walk_strings(P[tag]):
            clean = _strip_shared(s)
            for m in EN_MARKERS:
                if m.lower() in clean.lower():
                    hits.append((pth, m, s[:55]))
                    break
        chk(f"VI payload {tag!r}: zero English marker phrases",
            not hits, got=hits[:3])

    # --- one narrative per response, in the asked-for language ---
    for lg in ("vi", "en"):
        d = P[lg]
        chk(f"{lg}: ONE narrative in the response, not a bilingual pair",
            "narrative" in d and "narrative_en" not in d,
            got=sorted(k for k in d if "narrative" in k))
        chk(f"{lg}: the response states which language it is",
            d.get("lang") == lg, got=d.get("lang"))
    chk("VI and EN narratives differ (no silent fallback to one language)",
        P["vi"]["narrative"] != P["en"]["narrative"])
    chk("the VI narrative is actually Vietnamese",
        bool(VIET_CHARS.search(P["vi"]["narrative"])))
    chk("the EN narrative has no Vietnamese in it",
        not VIET_CHARS.search(P["en"]["narrative"]))

    # --- switching language changes PROSE ONLY ---
    vv, ve = P["vi"]["verdict"], P["en"]["verdict"]
    chk("language changes prose only: every enum code and number is "
        "identical across VI and EN",
        (vv["regime"], vv["coherence_tier"], vv["adjustment_mode"],
         vv["gate_code"], vv["R_B"], vv["cai_core"], vv["cai_ext"],
         vv["active_loops"]) ==
        (ve["regime"], ve["coherence_tier"], ve["adjustment_mode"],
         ve["gate_code"], ve["R_B"], ve["cai_core"], ve["cai_ext"],
         ve["active_loops"]))
    chk("the RENDERED headlines do differ", vv["headline"] != ve["headline"])
    # Compare the NUMERIC fields only. The localiser adds regime_text and
    # stability_text to capacity, and those differ by design - comparing the
    # whole dict would assert that localisation did nothing.
    numeric = ("S", "C", "delta", "delta_norm", "lam", "theta25", "psi",
               "pi_exit", "s_core", "c_numerator", "c_denominator")
    chk("numeric results are identical across languages",
        all(P["vi"]["capacity"][k] == P["en"]["capacity"][k]
            for k in numeric),
        got={k: (P["vi"]["capacity"][k], P["en"]["capacity"][k])
             for k in numeric if P["vi"]["capacity"][k]
             != P["en"]["capacity"][k]})
    chk("the trajectory is identical across languages",
        P["vi"]["trajectory"]["psi"] == P["en"]["trajectory"]["psi"])
    chk("the fragility verdict is identical across languages",
        [f["parameter"] for f in P["vi"]["fragility"]]
        == [f["parameter"] for f in P["en"]["fragility"]])

    # --- translation tables complete ---
    miss_vi = [k for k, r in I18N.T.items() if not r.get("vi")]
    miss_en = [k for k, r in I18N.T.items() if not r.get("en")]
    chk(f"all {len(I18N.T)} templates have a Vietnamese side",
        not miss_vi, got=miss_vi[:5])
    chk(f"all {len(I18N.T)} templates have an English side",
        not miss_en, got=miss_en[:5])
    ui_bad = [k for k, v in UI_TABLE.items()
              if not v.get("vi") or not v.get("en")]
    chk(f"all {len(UI_TABLE)} UI strings have both sides",
        not ui_bad, got=ui_bad[:5])

    # strict mode must fail loud rather than fall back to English
    try:
        I18N.t("definitely.not.a.real.key", "vi")
        chk("a missing i18n key RAISES rather than silently rendering "
            "English", False, got="it returned a value")
    except KeyError:
        chk("a missing i18n key RAISES rather than silently rendering "
            "English", True)

    # --- reference content translated on both sides ---
    ev_miss = [e.id for e in CATALOGUE if e.id not in EVENT_NOTES]
    chk(f"all {len(CATALOGUE)} events have a Vietnamese note entry",
        not ev_miss, got=ev_miss[:5])
    lbl_miss = [e.id for e in CATALOGUE if not e.label_vi or not e.label_en]
    chk("every event has a label in both languages",
        not lbl_miss, got=lbl_miss[:5])
    pr_miss = [c for c in PRESET_CODES if c not in PRESET_RATIONALE]
    chk(f"all {len(PRESET_CODES)} presets have a Vietnamese rationale",
        not pr_miss, got=pr_miss)
    op_miss = [o["id"] for o in spec2.OPEN_PROBLEMS_V2
               if o["id"] not in OPEN_PROBLEMS]
    chk("all 7 v2 open problems are translated", not op_miss, got=op_miss)
    inc_miss = [o["id"] for o in s1spec.KNOWN_INCONSISTENCIES
                if o["id"] not in INCONSISTENCIES]
    chk("all 9 sccd inconsistencies are translated",
        not inc_miss, got=inc_miss)
    pnames = {r["name"] for r in spec2.audit2()["rows"]}
    pn_miss = sorted(pnames - set(PARAM_NOTES))
    chk(f"all {len(pnames)} v2 parameter notes are translated",
        not pn_miss, got=pn_miss[:6])

    # --- the page holds no prose of its own ---
    html = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "web", "index.html"), encoding="utf-8").read()
    found = VIET_CHARS.findall(html)
    chk("web/index.html holds ZERO Vietnamese characters - the page is a "
        "renderer and every string arrives from the API",
        not found, got=found[:6])
    chk("web/index.html exposes two separate language tabs",
        'id="L-vi"' in html and 'id="L-en"' in html)
    chk("the page fetches its reference payloads WITH a lang parameter",
        "lang=" in html and "loadRefs" in html)
    chk("the page re-runs the diagnosis on a language switch rather than "
        "translating client-side",
        "await runOne()" in html and "await loadRefs()" in html)

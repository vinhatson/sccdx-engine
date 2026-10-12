# -*- coding: utf-8 -*-
"""
SCCD-X — Localisation: the renderers
=====================================
Walks an engine payload and turns every code into prose in one language.

This is the ONLY place that produces a human-readable sentence. The engine
emits `(key, params)` descriptors and enum names; these functions resolve
them. One consequence worth stating: a key the engine emits but this module
cannot find raises under strict mode rather than falling back to English, so
a missing Vietnamese string is a loud failure during development instead of a
quiet language leak in production.

Nested keys. A headline descriptor looks like
    ("hl.band_tier", {"regime": "regime.Crisis", "tier": "tier.Incoherent"})
with i18n keys sitting INSIDE the parameters. `_res` resolves those before
formatting, which is what stops a Vietnamese sentence from containing an
English band name.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import i18n as I
from .i18n import T, norm_lang, t, tparts
from .i18n import regime, stability, tier, mode, severity


# ---------------------------------------------------------------------------
# World verdict templates (registered here so they sit beside the renderer
# that consumes them)
# ---------------------------------------------------------------------------
I._add("wv.psiG", "Ψ_G = {psi} so với ngưỡng {crit} ({cmp} ngưỡng)",
       "Psi_G = {psi} vs crit {crit} ({cmp} threshold)")
I._add("wv.sync",
       "Sync_Risk = {sync} (tiên nghiệm {prior} + thành phần trú ẩn {haven})",
       "Sync_Risk = {sync} (prior {prior} + haven term {haven})")
I._add("wv.cai", "CAI_weighted = {cai} so với ngưỡng {crit}",
       "CAI_weighted = {cai} vs crit {crit}")
I._add("wv.trap", "Bẫy Thucydides T_trap=1 ({h} đối {c})",
       "Thucydides T_trap=1 ({h} vs {c})")
I._add("wv.rbg", "R_B,G = {v}", "R_B,G = {v}")
I._add("wv.divergence",
       "phân tán điều chỉnh {d} ({nv} tự nguyện so với {nx} phơi nhiễm bạo "
       "lực)",
       "adjustment divergence {d} ({nv} voluntary vs {nx} violent-exposed)")


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------
# Resolution lives in i18n.py so the narrative layer, the web payload and
# the world layer all go through exactly one implementation.
_res = I.resolve
_render = I.render


def _codes(codes, lang) -> List[str]:
    out = []
    for c in codes or []:
        if isinstance(c, (list, tuple)) and len(c) >= 1:
            out.append(_render(c[0], c[1] if len(c) > 1 else {}, lang))
    return out


def gate_text(code: str, years: Optional[float], lang: str) -> str:
    """Render a gate verdict code into prose."""
    if code in ("S5_GATE_NEAR", "S2_GATE_NEAR", "S5_GATE_CLOSING",
                "S2_GATE_CLOSING", "OPEN_NEAREST"):
        return t(f"tg.{code}", lang, y=f"{(years or 0):.0f}")
    return t(f"tg.{code}", lang, strict=False)


_FRAG_FIELD = {
    "regime": ("băng Δ", "Delta band"),
    "coherence_tier": ("tầng mạch lạc", "coherence tier"),
    "adjustment_mode": ("chế độ điều chỉnh", "adjustment mode"),
    "R_B": ("R_B", "R_B"),
    "active_loops": ("vòng đang chạy", "active loops"),
}


def _fragility_line(ch: dict, lang: str) -> str:
    f = ch.get("field", "")
    nm = _FRAG_FIELD.get(f, (f, f))[0 if lang == "vi" else 1]
    side = "−20%" if ch.get("side") == "low" else "+20%"

    def val(x):
        if isinstance(x, list):
            return "+".join(str(i) for i in x) or "—"
        if f == "regime":
            return regime(str(x), lang)
        if f == "coherence_tier":
            return tier(str(x), lang)
        if f == "adjustment_mode":
            return mode(str(x), lang)
        return str(x)

    return f"{nm}: {val(ch.get('from'))} → {val(ch.get('to'))} [{side}]"


_ATTRACTOR = {"A1_S_dominant_reconstitution": "att.A1",
              "A2_C_dominant_capture": "att.A2",
              "A3_fragmentation_collapse": "att.A3"}


# ---------------------------------------------------------------------------
# Diagnosis
# ---------------------------------------------------------------------------
def localize_diagnosis(d: dict, lang: str) -> dict:
    """Render every code in a Diagnosis2 payload. Mutates and returns d."""
    lang = norm_lang(lang)

    def fill_verdict(vd: dict) -> dict:
        if not vd:
            return vd
        vd["regime_text"] = regime(vd.get("regime", ""), lang)
        vd["stability_text"] = stability(vd.get("stability", ""), lang)
        vd["coherence_tier_text"] = tier(vd.get("coherence_tier", ""), lang)
        vd["adjustment_mode_text"] = mode(vd.get("adjustment_mode", ""), lang)
        vd["adjustment_mode_desc"] = t(
            f"mode.{vd.get('adjustment_mode', 'SLACK')}.desc", lang,
            strict=False)
        vd["gate_text"] = gate_text(vd.get("gate_code", "OPEN"),
                                    vd.get("gate_years"), lang)
        vd["headline"] = tparts(vd.get("headline_parts"), lang)
        return vd

    fill_verdict(d.get("verdict") or {})
    fill_verdict(d.get("horizon_verdict") or {})

    for key in ("capacity", "capacity_base"):
        c = d.get(key)
        if c:
            c["regime_text"] = regime(c.get("regime", ""), lang)
            c["stability_text"] = stability(c.get("stability", ""), lang)

    F = d.get("forcing") or {}
    for g in F.get("gates", []):
        g["meaning"] = t(g.get("meaning_key", ""), lang, strict=False)
    F["gate_text"] = gate_text(F.get("gate_code", "OPEN"),
                               F.get("gate_years"), lang)
    F["notes"] = _codes(F.get("note_codes"), lang)
    for blk in ("demo", "disp"):
        b = F.get(blk) or {}
        b["notes"] = _codes(b.get("note_codes"), lang)
    dm = F.get("demo") or {}
    if "router_mode" in dm:
        dm["router_mode_text"] = t(f"router.{dm['router_mode']}", lang,
                                   strict=False)
        dm["adjustment_mode_text"] = mode(dm.get("adjustment_mode", ""), lang)

    L = d.get("loops") or {}
    for k, st in (L.get("loops") or {}).items():
        st["name"] = t(st.get("name_key", ""), lang, strict=False)
        st["detail"] = _render(st.get("detail_key", ""),
                               st.get("detail_args"), lang)
        st["source"] = t(st.get("source_key", ""), lang, strict=False)
        st["description"] = t(f"loop.{k}.desc", lang, strict=False)
    L["cai_core_band"] = t(L.get("cai_core_band_key", ""), lang, strict=False)
    L["cai_core_horizon"] = t(L.get("cai_core_horizon_key", ""), lang,
                              strict=False)
    L["cai_ext_band"] = t(L.get("cai_ext_band_key", ""), lang, strict=False)
    L["cai_ext_horizon"] = (t(L.get("cai_ext_horizon_key", ""), lang,
                              strict=False) + t("cai.ext_suffix", lang))
    L["overlap_warnings"] = _codes(L.get("overlap_codes"), lang)

    rb = d.get("bifurcation") or {}
    if "d_delta_dt_source_key" in rb:
        rb["d_delta_dt_source"] = t(rb["d_delta_dt_source_key"], lang,
                                    strict=False)

    at = d.get("attractor") or {}
    if "most_likely" in at:
        at["most_likely_text"] = t(
            _ATTRACTOR.get(at["most_likely"], "att.note"), lang, strict=False)
        at["note"] = t("att.note", lang)

    T2 = d.get("trajectory")
    if T2:
        T2["notes"] = _codes(T2.get("note_codes"), lang)
        for c in T2.get("crossings", []):
            c["meaning"] = t(c.get("meaning_key", ""), lang, strict=False)
            c["direction_text"] = t(c.get("direction_key", ""), lang,
                                    strict=False)
            c["how"] = t(c.get("how_key", ""), lang, strict=False)
        T2["regime_at_text"] = [regime(r, lang)
                                for r in T2.get("regime_at", [])]
        T2["tier_at_text"] = [tier(x, lang) for x in T2.get("tier_at", [])]

    for f in d.get("fragility", []):
        f["changed_text"] = [_fragility_line(ch, lang)
                             for ch in f.get("changed", [])]

    ev = d.get("events")
    if ev:
        ev["notes"] = _codes(ev.get("note_codes"), lang)
        for a in ev.get("audit", []):
            # Resolve the label, then DROP both source fields. Leaving them
            # in meant an EN response still shipped the Vietnamese label -
            # a real leak, caught by validate_lang's character sweep.
            a["label"] = a.get("label_vi" if lang == "vi" else "label_en", "")
            a.pop("label_vi", None)
            a.pop("label_en", None)

    d["warnings"] = _codes(d.get("warning_codes"), lang)

    cal = d.get("calibration") or {}
    if "epistemic_limit_key" in cal:
        cal["epistemic_limit"] = t(cal["epistemic_limit_key"], lang)
    pd_ = cal.get("patch_defaults") or {}
    if "rationale_key" in pd_:
        pd_["rationale"] = t(pd_["rationale_key"], lang)
    if "audit" in cal:
        cal["audit"] = localize_audit_headline(cal["audit"], lang)
    cal["open_problems_v2"] = localize_open_problems(
        cal.get("open_problems_v2", []), lang)
    cal["known_inconsistencies_v1"] = localize_inconsistencies(
        cal.get("known_inconsistencies_v1", []), lang)
    d["lang"] = lang
    return d


# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------
def localize_world(w: dict, lang: str) -> dict:
    lang = norm_lang(lang)
    w["verdict"] = tparts(w.get("verdict_parts"), lang)
    w["warnings"] = _codes(w.get("warning_codes"), lang)

    tt = w.get("thucydides") or {}
    for src, dst in (("d_gap_dt_source_key", "d_gap_dt_source"),
                     ("note_key", "note")):
        if src in tt:
            tt[dst] = t(tt[src], lang, strict=False)

    rbg = w.get("global_bifurcation") or {}
    if "interpretation_key" in rbg:
        rbg["interpretation"] = t(rbg["interpretation_key"], lang)

    w["adjustment_split_text"] = {
        mode(k, lang): v
        for k, v in (w.get("adjustment_split") or {}).items()}

    for _code, pol in (w.get("polities") or {}).items():
        localize_diagnosis(pol, lang)
    w["lang"] = lang
    return w


# ---------------------------------------------------------------------------
# Reference tables
# ---------------------------------------------------------------------------
def localize_audit_headline(a: dict, lang: str) -> dict:
    v1, v2 = a.get("v1", {}), a.get("v2", {})
    c1 = v1.get("counts", {})
    a = dict(a)
    a["headline"] = t("audit.headline", lang,
                      paper=c1.get("PAPER", 0), total=v1.get("total", 0),
                      free=c1.get("FREE", 0), v2=v2.get("total", 0))
    return a


def localize_open_problems(rows: List[dict], lang: str) -> List[dict]:
    from .i18n_long import OPEN_PROBLEMS
    out = []
    for r in rows:
        r = dict(r)
        tr = OPEN_PROBLEMS.get(r.get("id", ""))
        if lang == "vi" and tr:
            r["issue"] = tr["vi"]
            r["where"] = tr.get("where_vi", r.get("where", ""))
        r["severity_text"] = severity(r.get("severity", ""), lang)
        out.append(r)
    return out


def localize_inconsistencies(rows: List[dict], lang: str) -> List[dict]:
    from .i18n_long import INCONSISTENCIES
    out = []
    for r in rows:
        r = dict(r)
        tr = INCONSISTENCIES.get(r.get("id", ""))
        if lang == "vi" and tr:
            r["issue"] = tr["vi"]
            r["where"] = tr.get("where_vi", r.get("where", ""))
        r["severity_text"] = severity(r.get("severity", ""), lang)
        out.append(r)
    return out


def localize_param_rows(rows: List[dict], lang: str) -> List[dict]:
    from .i18n_long import PARAM_NOTES
    out = []
    for r in rows:
        r = dict(r)
        if lang == "vi":
            vi = PARAM_NOTES.get(r.get("name", ""))
            if vi is not None:
                r["note"] = vi
        out.append(r)
    return out


def localize_events(cat: dict, lang: str) -> dict:
    from .i18n_long import EVENT_NOTES
    lang = norm_lang(lang)
    cat = dict(cat)
    cat["groups"] = {
        k: {"label": v["label_vi" if lang == "vi" else "label_en"]}
        for k, v in (cat.get("groups") or {}).items()}
    evs = []
    for e in cat.get("events", []):
        e = dict(e)
        e["label"] = e.get("label_vi" if lang == "vi" else "label_en", "")
        e["note"] = (EVENT_NOTES.get(e.get("id", ""), "") if lang == "vi"
                     else e.get("note", ""))
        for k in ("label_vi", "label_en", "note_vi"):
            e.pop(k, None)
        evs.append(e)
    cat["events"] = evs
    cat["provenance"] = t(cat.pop("provenance_key", "events.provenance"), lang)
    cat["usage"] = t(cat.pop("usage_key", "events.usage"), lang)
    cat["lang"] = lang
    return cat


def localize_presets(pre: dict, lang: str) -> dict:
    from .i18n_long import PRESET_RATIONALE
    lang = norm_lang(lang)
    pre = dict(pre)
    rows = []
    for p in pre.get("polities", []):
        p = dict(p)
        if lang == "vi":
            p["rationale"] = PRESET_RATIONALE.get(p.get("code", ""),
                                                  p.get("rationale", ""))
            pv = p.get("provenance", "")
            key = ("prov.mixed_us" if pv.startswith("MIXED")
                   else ("prov.caller" if "caller" in pv else "prov.analyst"))
            p["provenance"] = t(key, lang)
        p["confidence_text"] = t(f"conf.{p.get('confidence', 'unknown')}",
                                 lang, strict=False)
        rows.append(p)
    pre["polities"] = rows
    pre["disclaimer"] = t("presets.disclaimer", lang)
    pre["lang"] = lang
    return pre

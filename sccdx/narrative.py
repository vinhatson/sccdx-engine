# -*- coding: utf-8 -*-
"""
SCCD-X — Qualitative Narrative Layer
=====================================
Turns a localised Diagnosis2 / WorldDiagnosis payload into prose.

It consumes the ALREADY-LOCALISED dict, so it contains no translation table
of its own and cannot disagree with the rest of the page. The earlier version
carried two parallel inline branches - one Vietnamese, one English - and they
drifted: the English branch gained a caveat the Vietnamese one did not. One
table, one renderer, no drift.

WHAT THIS LAYER IS ALLOWED TO SAY
---------------------------------
Only what the calibration supports, which sccd Part V 1 fixes as
"qualitative-structural". It may state the regime band, coherence tier and
adjustment mode; which loops are armed and cross-coupled; which PAPER
threshold is nearest and in which direction; the ORDER in which gates close
and a magnitude for how far off; how scenarios RANK; and what would have to
be true for the reading to be wrong.

It may NOT state a probability, a date, a Delta level as though measured, or
"this will happen". Those are not available from 36 PAPER, 46 FREE and 46
ANALYST parameters.
"""
from __future__ import annotations

from typing import Any, Dict, List

from .i18n import t, norm_lang
from . import i18n as I

# --- section labels, registered here beside the renderer that uses them ---
I._add("nar.title", "ĐỌC ĐỊNH TÍNH — {country} {year}",
       "QUALITATIVE READING - {country} {year}")
I._add("nar.spec", "[spec v{v1} / v{v2}, loại nhà nước: {st}]",
       "[spec v{v1} / v{v2}, state type: {st}]")
I._add("nar.s1", "BỘ BA CẤU TRÚC", "THE STRUCTURAL TRIPLE")
I._add("nar.s1.band", "Băng Δ", "Delta band")
I._add("nar.s1.tier", "Tầng mạch lạc", "Coherence tier")
I._add("nar.s1.mode", "Chế độ điều chỉnh", "Adjustment mode")
I._add("nar.s2", "TÁCH RỜI G/S₃ ĐANG HOẠT ĐỘNG — vì sao cần ba trục",
       "G/S3 DECOUPLING ACTIVE - why three axes are needed")
I._add("nar.s3", "CỔNG θ₂₅ — Wheel of Fate viết bằng biến của sccd",
       "THE theta25 GATES - the Wheel of Fate in sccd's own variables")
I._add("nar.s3.verdict", "Phán quyết", "Verdict")
I._add("nar.s4", "VÒNG PHẢN HỒI", "FEEDBACK LOOPS")
I._add("nar.s4.sync",
       "GHÉP CHÉO & ĐANG CHẠY: {loops} → gia tốc hợp thành đang vận hành",
       "CROSS-COUPLED & ACTIVE: {loops} -> compound acceleration operative")
I._add("nar.s5", "RỦI RO PHÂN NHÁNH  R_B = {rb}  (sccd eq 23 — cần CẢ BA "
                 "điều kiện)",
       "BIFURCATION RISK  R_B = {rb}  (sccd eq 23 - ALL THREE conditions "
       "required)")
I._add("nar.s5.attractor", "attractor gần nhất", "nearest attractor")
I._add("nar.s6", "QUỸ ĐẠO ĐẾN MỐC +{y} NĂM (KỊCH BẢN CẤU TRÚC, không phải "
                 "dự báo)",
       "TRAJECTORY TO +{y} YEARS (STRUCTURAL SCENARIO, not a forecast)")
I._add("nar.s6.now", "Hiện tại", "Now")
I._add("nar.s6.horizon", "Tại mốc", "At horizon")
I._add("nar.s6.shift",
       "→ Băng và/hoặc tầng mạch lạc CHUYỂN trong kỳ. Đọc đây là thứ tự và "
       "chiều, không phải thời điểm.",
       "-> The band and/or coherence tier SHIFTS within the horizon. Read "
       "this as ordering and direction, not as timing.")
I._add("nar.s7", "ĐIỀU GÌ KHIẾN CÁCH ĐỌC NÀY SAI",
       "WHAT WOULD MAKE THIS READING WRONG")
I._add("nar.limit", "GIỚI HẠN NHẬN THỨC", "EPISTEMIC LIMIT")
I._add("nar.active", "ĐANG CHẠY", "ACTIVE  ")
I._add("nar.damped", "tắt      ", "damped  ")
I._add("nar.yr", "năm", "yr")
I._add("nar.crossed", "đã vượt", "crossed")
I._add("nar.no_approach", "không tiến tới", "not approaching")
I._add("nar.cross_at", "vượt {var} {dir} {thr} [{st}] tại t≈{t}: {meaning}",
       "{var} crosses {dir} {thr} [{st}] at t~{t}: {meaning}")

# world
I._add("nar.w.title", "ĐỌC ĐỊNH TÍNH THẾ GIỚI — {year}",
       "QUALITATIVE WORLD READING - {year}")
I._add("nar.w.s1", "MẠCH LẠC TOÀN CỤC", "GLOBAL COHERENCE")
I._add("nar.w.sync_note",
       "Sync_Risk trong sccd v1.00 chỉ là bốn số lịch sử trần trụi "
       "(0.12/0.24/0.41/0.58 cho 1980/95/2010/2024) không có cơ chế sinh. "
       "Displacement cấp một cơ chế: dòng vốn trú ẩn đồng pha xuyên quốc gia "
       "vì nguyên nhân là một dịch chuyển tâm lý dùng chung, không phải điều "
       "kiện nội địa của nước nào. Engine tách riêng hai phần để tiên nghiệm "
       "không bị ghi đè âm thầm.",
       "Sync_Risk in sccd v1.00 is four bare historical numbers "
       "(0.12/0.24/0.41/0.58 for 1980/95/2010/2024) with no generating "
       "mechanism. Displacement supplies one: haven flight is simultaneous "
       "across states because its cause is a shared psychological shift "
       "rather than any country's local conditions. The engine reports the "
       "two parts separately so the prior is never silently overwritten.")
I._add("nar.w.s2", "THẾ GIỚI HAI KÊNH  [Wheel of Fate ở quy mô hệ thống]",
       "THE TWO-CHANNEL WORLD  [Wheel of Fate at system scale]")
I._add("nar.w.s3", "CHUYỂN DỊCH BÁ QUYỀN", "HEGEMONIC TRANSITION")
I._add("nar.w.s4", "ĐIỀU KIỆN PHÂN NHÁNH TOÀN CỤC",
       "GLOBAL BIFURCATION CONDITION")
I._add("nar.w.s5", "BẢNG THEO CHỦ THỂ", "PER-POLITY TABLE")
I._add("nar.w.warn", "CẢNH BÁO HIỆU CHUẨN", "CALIBRATION WARNINGS")
I._add("nar.w.pair", "Cặp: {h} ({hr}) đối {c}",
       "Pair: {h} ({hr}) vs {c}")
I._add("nar.w.gradients", "Chênh lệch tài năng mạnh nhất (đẩy d₅ × hút d₄):",
       "Strongest talent gradients (push d5 x pull d4):")
I._add("nar.w.caveat", "LƯU Ý", "CAVEAT")


def _n(v: Any, d: int = 4, sign: bool = False) -> str:
    """Format a number. sign=True always shows + or -, which is what a
    signed quantity like Delta_norm or a drift rate needs."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return "—"
    return f"{f:+.{d}f}" if sign else f"{f:.{d}f}"


# ===========================================================================
#  SINGLE POLITY
# ===========================================================================
def narrate(d: dict, lang: str = "vi") -> str:
    """Render a LOCALISED diagnosis dict (see i18n_render.localize_diagnosis)."""
    lang = norm_lang(lang)
    V = d.get("verdict", {})
    cap = d.get("capacity", {})
    F = d.get("forcing", {})
    L = d.get("loops", {})
    cal = d.get("calibration", {})
    out: List[str] = []
    n = 0

    out.append(t("nar.title", lang, country=d.get("country", ""),
                 year=d.get("year", "")) + "   "
               + t("nar.spec", lang, v1=cal.get("spec_version", ""),
                   v2=cal.get("spec2_version", ""),
                   st=d.get("state_type", "")))
    out.append("=" * 74)

    # ---- 1. the triple ----
    n += 1
    out.append(f"{n}. {t('nar.s1', lang)}")
    out.append(f"   {t('nar.s1.band', lang)}: {V.get('regime_text')} "
               f"({V.get('stability_text')})")
    out.append(f"      Δ_norm = {_n(cap.get('delta_norm'), sign=True)}   "
               f"S = {_n(cap.get('S'))}   C = {_n(cap.get('C'))}")
    psi = cap.get("psi", 0.0)
    out.append(f"   {t('nar.s1.tier', lang)}: {V.get('coherence_tier_text')}")
    out.append(f"      Ψ = {_n(psi)}  {t('res.vs', lang)} "
               f"Ψ_crit = 0.40 [PAPER]  → "
               f"{t('w.below', lang) if psi < 0.40 else t('w.above', lang)}")
    out.append(f"   {t('nar.s1.mode', lang)}: {V.get('adjustment_mode_text')}")
    out.append(f"      {V.get('adjustment_mode_desc', '')}")
    out.append("")

    # ---- 2. decoupling ----
    if V.get("decoupling_active"):
        n += 1
        out.append(f"{n}. {t('nar.s2', lang)}")
        for note in F.get("disp", {}).get("notes", []):
            out.append(f"   {note}")
        out.append("")

    # ---- 3. gates ----
    n += 1
    out.append(f"{n}. {t('nar.s3', lang)}")
    out.append(f"   {t('nar.s3.verdict', lang)}: {V.get('gate_text')}")
    for g in F.get("gates", []):
        dr = g.get("drift", 0.0)
        arrow = "↓" if dr < 0 else ("↑" if dr > 0 else "·")
        if g.get("crossed"):
            when = t("nar.crossed", lang)
        elif g.get("years_to_gate") is not None:
            when = f"~{g['years_to_gate']:.0f} {t('nar.yr', lang)}"
        else:
            when = t("nar.no_approach", lang)
        out.append(f"     {g['component'].upper():3s} = {g['level']:.3f} "
                   f"{arrow} {dr:+.4f}/{t('nar.yr', lang)}  → "
                   f"{g['threshold']:.2f} [{g['threshold_status']}] : {when}")
    out.append(f"   {t('theta25.gate_note', lang)}")
    out.append("")

    # ---- 4. loops ----
    n += 1
    out.append(f"{n}. {t('nar.s4', lang)}")
    out.append(f"   {t('res.cai_core', lang)} = {L.get('cai_core', 0):.1f} "
               f"({L.get('cai_core_band')}): {L.get('cai_core_horizon')}")
    out.append(f"   {t('res.cai_ext', lang)} = {L.get('cai_ext', 0):.1f} "
               f"({L.get('cai_ext_band')})")
    for k in sorted(L.get("loops", {})):
        st = L["loops"][k]
        tag = t("nar.active", lang) if st["active"] else t("nar.damped", lang)
        out.append(f"     {k} {tag} {st.get('name')}")
        if st["active"]:
            out.append(f"          {st.get('detail')}")
    if L.get("synchronised"):
        out.append("   " + t("nar.s4.sync", lang,
                             loops=", ".join(L["synchronised"])))
    if L.get("loops", {}).get("L6", {}).get("active"):
        out.append("")
        out.append(f"   [L6] {t('res.l6_note', lang)}")
    out.append("")

    # ---- 5. bifurcation ----
    n += 1
    rb = d.get("bifurcation", {})
    out.append(f"{n}. " + t("nar.s5", lang, rb=rb.get("R_B", 0)))
    out.append(f"   {t('res.cond_delta', lang)}: "
               f"{rb.get('cond_delta_below_crit')}")
    out.append(f"   {t('res.cond_momentum', lang)}: {rb.get('cond_momentum')}"
               f"   (dΔ/dt = {_n(rb.get('d_delta_dt'), sign=True)}, "
               f"{rb.get('d_delta_dt_source', '')})")
    out.append(f"   {t('res.cond_coherence', lang)}: "
               f"{rb.get('cond_low_coherence')}")
    if rb.get("R_B") == 1:
        at = d.get("attractor", {})
        out.append(f"   → {t('nar.s5.attractor', lang)}: "
                   f"{at.get('most_likely_text', at.get('most_likely', ''))}")
    out.append("")

    # ---- 6. trajectory ----
    T2 = d.get("trajectory")
    H = d.get("horizon_verdict")
    if T2 and H:
        n += 1
        yrs = T2["t"][-1] if T2.get("t") else 0
        out.append(f"{n}. " + t("nar.s6", lang, y=f"{yrs:.0f}"))
        out.append(f"   {t('nar.s6.now', lang)}      : "
                   f"{V.get('regime_text')} / {V.get('coherence_tier_text')}")
        out.append(f"   {t('nar.s6.horizon', lang)}   : "
                   f"{H.get('regime_text')} / {H.get('coherence_tier_text')}")
        if (H.get("regime"), H.get("coherence_tier")) != \
           (V.get("regime"), V.get("coherence_tier")):
            out.append(f"   {t('nar.s6.shift', lang)}")
        for c in T2.get("crossings", []):
            out.append("     " + t("nar.cross_at", lang,
                                   var=c["variable"],
                                   dir=c.get("direction_text", ""),
                                   thr=f"{c['threshold']:.2f}",
                                   st=c["threshold_status"],
                                   t=f"{c['year_offset']:.1f}",
                                   meaning=c.get("meaning", "")))
        out.append("")

    # ---- 7. fragility ----
    n += 1
    out.append(f"{n}. {t('nar.s7', lang)}")
    frag = d.get("fragility", [])
    if frag:
        out.append("   " + t("res.frag_some", lang, n=len(frag)))
        for f in frag[:6]:
            out.append(f"     {f['parameter']} [{f['status']}] = "
                       f"{f['baseline']:.4f}")
            for line in f.get("changed_text", [])[:2]:
                out.append(f"        {line}")
    else:
        out.append("   " + t("res.frag_none", lang))
    out.append("")

    # ---- limit ----
    out.append(t("nar.limit", lang))
    audit = cal.get("audit", {})
    if audit.get("headline"):
        out.append(f"   {audit['headline']}")
    if cal.get("epistemic_limit"):
        out.append(f"   {cal['epistemic_limit']}")
    return "\n".join(out)


# ===========================================================================
#  WORLD
# ===========================================================================
def narrate_world(w: dict, lang: str = "vi") -> str:
    """Render a LOCALISED world dict (see i18n_render.localize_world)."""
    lang = norm_lang(lang)
    out: List[str] = []
    out.append(t("nar.w.title", lang, year=w.get("year", "")))
    out.append("=" * 74)
    out.append("")

    # 1. global coherence
    below = w.get("psi_G", 0) < w.get("psi_G_crit", 0.4)
    out.append(f"1. {t('nar.w.s1', lang)}")
    out.append(f"   Ψ_G = {_n(w.get('psi_G'))}  {t('res.vs', lang)} "
               f"Ψ_G,crit = {w.get('psi_G_crit', 0):.2f} [PAPER] → "
               f"{t('w.below', lang) if below else t('w.above', lang)}")
    out.append(f"   Sync_Risk = {_n(w.get('sync_risk'), 3)}  = "
               f"{t('w.prior', lang)} {w.get('sync_risk_prior', 0):.2f} + "
               f"{t('w.haven_term', lang)} "
               f"{_n(w.get('sync_risk_haven'), 3)}")
    out.append(f"   {t('nar.w.sync_note', lang)}")
    out.append(f"   CAI_weighted = {w.get('cai_weighted', 0):.2f}  "
               f"{t('res.vs', lang)} 1.50 [PAPER, 1929-39]")
    out.append("")

    # 2. two-channel world
    out.append(f"2. {t('nar.w.s2', lang)}")
    for label, codes in (w.get("adjustment_split_text") or {}).items():
        if codes:
            out.append(f"   {label} ({len(codes)}): {', '.join(codes)}")
    out.append(f"   {t('w.divergence', lang)} = "
               f"{_n(w.get('adjustment_divergence'), 3)}")
    out.append(f"   {t('w.divergence_help', lang)}")
    if w.get("talent_gradient"):
        out.append(f"   {t('nar.w.gradients', lang)}")
        for g in w["talent_gradient"][:5]:
            out.append(f"     {g['origin']} → {g['destination']}   "
                       f"d₅={g['push_d5']:.2f} × d₄={g['pull_d4']:.2f} "
                       f"= {g['pressure']:.4f}")
    out.append("")

    # 3. hegemonic transition
    tt = w.get("thucydides", {})
    out.append(f"3. {t('nar.w.s3', lang)}")
    if tt.get("hegemon"):
        out.append("   " + t("nar.w.pair", lang, h=tt["hegemon"],
                             hr=t("w.hegemon", lang), c=tt["challenger"]))
        out.append(f"   δ_hc = {_n(tt.get('hegemonic_gap'), sign=True)}  "
                   f"{t('res.vs', lang)} 0.25 [PAPER]")
        out.append(f"   T_trap = {tt.get('T_trap', 0)}   "
                   f"({t('w.cond_gap', lang)}: "
                   f"{tt.get('cond_gap_below_crit')}; "
                   f"{t('w.cond_converge', lang)}: "
                   f"{tt.get('cond_converging')}; "
                   f"{t('w.cond_sustained', lang)}: "
                   f"{tt.get('cond_sustained')})")
        out.append(f"   {t('nar.w.caveat', lang)}: "
                   f"{tt.get('d_gap_dt_source', '')}")
    else:
        out.append(f"   {tt.get('note', '')}")
    out.append("")

    # 4. global bifurcation
    rbg = w.get("global_bifurcation", {})
    out.append(f"4. {t('nar.w.s4', lang)}  R_B,G = {rbg.get('R_B_G', 0)}")
    out.append(f"   {t('w.cond_low_psiG', lang)}: "
               f"{rbg.get('cond_low_global_coherence')}")
    out.append(f"   {t('w.cond_trap', lang)}: {rbg.get('cond_trap')}")
    out.append(f"   {t('w.cond_compound', lang)}: "
               f"{rbg.get('cond_compound_acceleration')}")
    out.append(f"   {rbg.get('interpretation', '')}")
    out.append("")

    # 5. per polity
    out.append(f"5. {t('nar.w.s5', lang)}")
    hdr = (f"   {t('th.code', lang):<5} "
           f"{t('nar.s1.band', lang) + ' / ' + t('nar.s1.tier', lang):<30} "
           f"{t('nar.s1.mode', lang):<28} "
           f"{t('th.loops_active', lang):<14} {'Ψ':>6}")
    out.append(hdr)
    out.append("   " + "-" * (len(hdr) - 3))
    for code, p in (w.get("polities") or {}).items():
        v = p.get("verdict", {})
        loops = "+".join(x[1:] for x in v.get("active_loops", [])) or "—"
        bt = f"{v.get('regime_text')} / {v.get('coherence_tier_text')}"
        out.append(f"   {code:<5} {bt:<30} "
                   f"{v.get('adjustment_mode_text', ''):<28} "
                   f"{loops:<14} {p.get('capacity', {}).get('psi', 0):>6.3f}")
    out.append("")

    out.append(t("nar.w.warn", lang))
    for wa in w.get("warnings", []):
        out.append(f"   ! {wa}")
    return "\n".join(out)

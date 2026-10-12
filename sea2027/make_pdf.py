# -*- coding: utf-8 -*-
"""
sea2027.make_pdf - one PDF per polity per language, 22 in all
==============================================================
    python sea2027/make_pdf.py

Reads sea2027_vi.json and sea2027_en.json - which already carry every engine
string rendered into their own language - and writes

    sea2027/pdf/SCCDX-2027-<CODE>-vi.pdf
    sea2027/pdf/SCCDX-2027-<CODE>-en.pdf

FONTS
-----
The engine emits Unicode subscripts everywhere (S3-sub, theta-25-sub, Psi,
lambda) and the Vietnamese side needs the full Latin Extended Additional
block. Only two font families on this machine cover BOTH:

    body  DejaVu Sans   (ships with matplotlib; free licence)
    mono  Consolas      (Windows)

DejaVuSansMono is missing 44 Vietnamese precomposed characters - every one
with a circumflex-plus-tone, so Ê-acute, Ô-hook, U-horn-grave and friends -
and would silently drop them. It is therefore NOT used. reportlab subsets on
embed, so only the glyphs actually printed go into the file.

Do not substitute a reportlab built-in (Helvetica, Courier): those have
neither the subscripts nor the diacritics and render solid boxes.
"""
from __future__ import annotations

import json
import os
import sys
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether,
                                PageBreak, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
OUT = os.path.join(HERE, "pdf")

CODES = ["ID", "SG", "TH", "VN", "PH", "MY", "MM", "KH", "LA", "BN", "TL"]

# imported after sys.path is set above: the engine's own regime table,
# so the Monte-Carlo band names read in the report's language rather
# than as raw enum values.
from sccdx.i18n import regime as regime_label  # noqa: E402
import sccdx.i18n_ui  # noqa: F401,E402  (mirrors 199 templates into T)

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
def _mpl_font_dir() -> str:
    import matplotlib
    return os.path.join(os.path.dirname(matplotlib.__file__),
                        "mpl-data", "fonts", "ttf")


def register_fonts() -> None:
    d = _mpl_font_dir()
    win = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    pairs = [
        ("Body", os.path.join(d, "DejaVuSans.ttf")),
        ("Body-Bold", os.path.join(d, "DejaVuSans-Bold.ttf")),
        ("Body-It", os.path.join(d, "DejaVuSans-Oblique.ttf")),
        ("Mono", os.path.join(win, "consola.ttf")),
        ("Mono-Bold", os.path.join(win, "consolab.ttf")),
    ]
    for name, path in pairs:
        if not os.path.exists(path):
            raise SystemExit(f"font missing: {path}")
        pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold",
                                  italic="Body-It", boldItalic="Body-Bold")
    pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="Mono-Bold",
                                  italic="Mono", boldItalic="Mono-Bold")


# ---------------------------------------------------------------------------
# Palette and styles
# ---------------------------------------------------------------------------
INK = colors.HexColor("#1b1b1d")
MUTED = colors.HexColor("#6c6a66")
FAINT = colors.HexColor("#97948e")
RULE = colors.HexColor("#d9d5cd")
PANEL = colors.HexColor("#f4f2ed")
ACCENT = colors.HexColor("#243b53")
OK = colors.HexColor("#2c6442")
WARN = colors.HexColor("#8a6417")
BAD = colors.HexColor("#9b2a26")

TIER_COLOR = {"Coherent": OK, "Strained": WARN, "Incoherent": BAD}

S = {}


def build_styles() -> None:
    def st(name, **kw):
        S[name] = ParagraphStyle(name, **kw)

    st("title", fontName="Body-Bold", fontSize=19, leading=23, textColor=INK,
       spaceAfter=1)
    st("subtitle", fontName="Body", fontSize=10, leading=14, textColor=MUTED)
    st("kicker", fontName="Mono-Bold", fontSize=8, leading=11, textColor=ACCENT)
    st("h1", fontName="Body-Bold", fontSize=12, leading=15, textColor=ACCENT,
       spaceBefore=12, spaceAfter=5)
    st("h2", fontName="Body-Bold", fontSize=9.6, leading=13, textColor=INK,
       spaceBefore=7, spaceAfter=3)
    st("body", fontName="Body", fontSize=8.9, leading=12.6, textColor=INK,
       alignment=TA_LEFT, spaceAfter=4)
    st("note", fontName="Body", fontSize=8.1, leading=11.4, textColor=MUTED,
       spaceAfter=3)
    st("tiny", fontName="Body", fontSize=7.2, leading=10, textColor=FAINT,
       spaceAfter=2)
    st("mono", fontName="Mono", fontSize=8.1, leading=11.2, textColor=INK)
    st("cell", fontName="Body", fontSize=7.9, leading=10.6, textColor=INK)
    st("cellm", fontName="Mono", fontSize=7.9, leading=10.6, textColor=INK)
    st("cellh", fontName="Body-Bold", fontSize=7.6, leading=10.2,
       textColor=MUTED)
    st("verdict", fontName="Body-Bold", fontSize=13.5, leading=17,
       textColor=INK, spaceAfter=2)
    st("quote", fontName="Body", fontSize=8.6, leading=12.4, textColor=INK,
       leftIndent=8, spaceAfter=4)


# ---------------------------------------------------------------------------
# Bilingual chrome. Every engine string arrives already rendered; only the
# section furniture is translated here.
# ---------------------------------------------------------------------------
L = {
 "vi": {
  "doc": "ĐỌC ĐỊNH TÍNH SCCD-X v2.00",
  "sub": "Chạy {d} · neo {y} · chân trời 2027 = {h} năm · solver {s}",
  "verdict_now": "Phán quyết {y}",
  "verdict_2027": "Phán quyết 2027",
  "s1": "1. Bộ ba cấu trúc, {y} so với 2027",
  "s2": "2. Đầu vào và xuất xứ từng thành phần",
  "s3": "3. Phần phán đoán của nhà phân tích",
  "s4": "4. Các cổng θ₂₅",
  "s5": "5. Tám vòng phản hồi",
  "s6": "6. Rủi ro phân nhánh R_B và attractor",
  "s7": "7. Dải đo Monte-Carlo",
  "s8": "8. Độ giòn OAT ±20%",
  "s9": "9. Nhánh stress 2027",
  "s10": "10. Quỹ đạo tới hết 2027",
  "s11": "11. Pass 15 năm: thứ tự cổng đóng",
  "s12": "12. Giới hạn nhận thức",
  "band": "Băng Δ", "tier": "Tầng mạch lạc", "mode": "Chế độ điều chỉnh",
  "gate": "Cổng", "loops": "Vòng đang chạy", "none": "không có",
  "state_type": "Loại nhà nước", "weight": "Trọng số hệ thống",
  "comp": "Thành phần", "val": "Giá trị", "tag": "Xuất xứ",
  "terms": "Các số đã vào công thức",
  "measure": "Đại lượng", "level": "Mức", "drift": "Trôi/năm",
  "thresh": "Ngưỡng", "years": "Số năm", "status": "Trạng thái",
  "crossed": "ĐÃ VƯỢT", "open": "còn mở",
  "loop": "Vòng", "on": "ĐANG CHẠY", "off": "tắt",
  "detail": "Chi tiết", "cond": "Điều kiện",
  "param": "Tham số", "base": "Gốc", "flip": "Đảo khi",
  "lowside": "giảm 20%", "highside": "tăng 20%", "bothside": "cả hai phía",
  "changed": "Thay đổi gì",
  "event": "Sự kiện", "intensity": "Cường độ", "shifts": "Dịch chuyển",
  "baseline": "Baseline", "stress": "Stress",
  "holds": "phán quyết giữ nguyên", "moves": "PHÁN QUYẾT DỊCH CHUYỂN",
  "why_stress": "Vì sao những sự kiện này, và vì sao không phải sự kiện khác",
  "t": "t (năm)", "mix": "Phân bố băng chế độ",
  "med": "Trung vị", "ci80": "Khoảng 80%", "ci95": "Khoảng 95%",
  "prov_note": "MEASURED = mọi số hạng đến từ một quan sát có ngày. "
               "MIXED = hợp số đã đo nhưng bị chặn hoặc dịch bởi một số "
               "hạng do nhà phân tích đặt. ANALYST = không có series nào "
               "dùng được cho chủ thể này.",
  "judg_note": "Đây là văn bản lập luận đi kèm các con số ANALYST của hàng "
               "này, trích nguyên từ sea2027/judgment.py. Nó không phải số "
               "đo, và nó là chỗ nên phản đối trước tiên.",
  "footer": "SCCD-X v2.00 · {code} · {lang} · trang {p}",
  "nodata": "không có",
  "oat_none": "Không tham số nào trong {n} tham số làm đảo phán quyết ở ±20%.",
  "oat_some": "{k} trong {n} tham số làm đảo phán quyết định tính ở ±20%, "
              "mức nhiễu sccd eq (SA) bắt buộc.",
  "sigma_note": "Độ lệch chuẩn đo lường dùng cho pass này (đơn vị đã chuẩn "
                "hóa): {s}. Hai con số lớn nhất là s3 và c5 — s3 là proxy "
                "rủi ro cao nhất của chính sccd và thuộc diện BLOCKED, c5 "
                "thì ANALYST toàn bộ ở cả 11 chủ thể.",
 },
 "en": {
  "doc": "SCCD-X v2.00 QUALITATIVE READING",
  "sub": "Run {d} · anchored {y} · 2027 horizon = {h} yr · solver {s}",
  "verdict_now": "{y} verdict",
  "verdict_2027": "2027 verdict",
  "s1": "1. The structural triple, {y} against 2027",
  "s2": "2. Inputs and per-component provenance",
  "s3": "3. What the analyst is asserting",
  "s4": "4. The θ₂₅ gates",
  "s5": "5. The eight feedback loops",
  "s6": "6. Bifurcation risk R_B and attractor",
  "s7": "7. Monte-Carlo measurement bands",
  "s8": "8. OAT fragility at ±20%",
  "s9": "9. The 2027 stress branch",
  "s10": "10. Trajectory to end-2027",
  "s11": "11. The 15-year pass: order the gates close in",
  "s12": "12. Epistemic limits",
  "band": "Δ band", "tier": "Coherence tier", "mode": "Adjustment mode",
  "gate": "Gate", "loops": "Active loops", "none": "none",
  "state_type": "State type", "weight": "Systemic weight",
  "comp": "Component", "val": "Value", "tag": "Provenance",
  "terms": "Terms that entered the formula",
  "measure": "Measure", "level": "Level", "drift": "Drift/yr",
  "thresh": "Threshold", "years": "Years", "status": "Status",
  "crossed": "CROSSED", "open": "open",
  "loop": "Loop", "on": "ACTIVE", "off": "off",
  "detail": "Detail", "cond": "Condition",
  "param": "Parameter", "base": "Baseline", "flip": "Flips on",
  "lowside": "−20%", "highside": "+20%", "bothside": "both sides",
  "changed": "What changed",
  "event": "Event", "intensity": "Intensity", "shifts": "Shifts applied",
  "baseline": "Baseline", "stress": "Stress",
  "holds": "verdict holds", "moves": "VERDICT MOVES",
  "why_stress": "Why these events, and why not others",
  "t": "t (yr)", "mix": "Regime-band distribution",
  "med": "Median", "ci80": "80% interval", "ci95": "95% interval",
  "prov_note": "MEASURED = every term came from a dated observation. "
               "MIXED = a measured composite gated or shifted by an argued "
               "term. ANALYST = no usable series exists for this polity.",
  "judg_note": "This is the argued text behind this row's ANALYST numbers, "
               "quoted verbatim from sea2027/judgment.py. It is not a "
               "measurement, and it is the first thing to disagree with.",
  "footer": "SCCD-X v2.00 · {code} · {lang} · page {p}",
  "nodata": "none",
  "oat_none": "None of the {n} parameters flips the verdict at ±20%.",
  "oat_some": "{k} of {n} parameters flip the qualitative verdict at ±20%, "
              "the perturbation sccd eq (SA) mandates.",
  "sigma_note": "Measurement SD used for this pass, in normalised units: "
                "{s}. The two largest are s3 and c5 — s3 is sccd's own "
                "highest-risk proxy and is BLOCKED, and c5 is fully ANALYST "
                "for all eleven polities.",
 },
}

LANGNAME = {"vi": "Tiếng Việt", "en": "English"}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def hx(c) -> str:
    """reportlab's hexval() returns 0xrrggbb; the markup wants #rrggbb."""
    return "#" + c.hexval()[2:]


def P(txt, style="body"):
    return Paragraph(txt if isinstance(txt, str) else str(txt), S[style])


def esc(x) -> str:
    return escape("" if x is None else str(x), quote=False)


def num(v, d=3, sign=False):
    if v is None:
        return "–"
    try:
        f = float(v)
    except (TypeError, ValueError):
        return esc(v)
    return f"{f:+.{d}f}" if sign else f"{f:.{d}f}"


def rule(w=None, color=RULE, thick=0.6, space=4):
    t = Table([[""]], colWidths=[w or 170 * mm], rowHeights=[0.1])
    t.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), thick, color),
                           ("TOPPADDING", (0, 0), (-1, -1), space),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), space)]))
    return t


def grid(rows, widths, header=True, align=None, pad=3.2, zebra=True):
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0,
              hAlign="LEFT")
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, RULE),
    ]
    if header:
        cmds += [("LINEBELOW", (0, 0), (-1, 0), 0.8, MUTED),
                 ("BOTTOMPADDING", (0, 0), (-1, 0), 4)]
    if zebra:
        for i in range(1 + (1 if header else 0), len(rows), 2):
            cmds.append(("BACKGROUND", (0, i), (-1, i), PANEL))
    for col, a in (align or {}).items():
        cmds.append(("ALIGN", (col, 0), (col, -1), a))
    t.setStyle(TableStyle(cmds))
    return t


def panel(flows, pad=8, bg=PANEL, line=RULE, width=170 * mm):
    t = Table([[flows]], colWidths=[width], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.6, line),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


# ---------------------------------------------------------------------------
# Page furniture
# ---------------------------------------------------------------------------
class Doc(BaseDocTemplate):
    def __init__(self, path, code, lang, name, **kw):
        # NOT self.lang / self.code: BaseDocTemplate owns `lang` (it becomes
        # the PDF /Lang entry) and resets it during build, which silently
        # replaced the value and blew up in _furniture.
        self.rpt_code, self.rpt_lang, self.rpt_name = code, lang, name
        super().__init__(path, pagesize=A4,
                         leftMargin=20 * mm, rightMargin=20 * mm,
                         topMargin=18 * mm, bottomMargin=16 * mm,
                         title=f"SCCD-X 2027 — {name} ({code}) — {lang}",
                         author="SCCD-X v2.00 / sea2027",
                         subject="Qualitative structural reading, 2027",
                         lang=("vi-VN" if lang == "vi" else "en"),
                         **kw)
        frame = Frame(self.leftMargin, self.bottomMargin,
                      self.width, self.height, id="main",
                      leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="p", frames=[frame],
                                            onPage=self._furniture)])

    def _furniture(self, canv, doc):
        canv.saveState()
        y = A4[1] - 11 * mm
        canv.setFont("Mono", 7)
        canv.setFillColor(FAINT)
        canv.drawString(20 * mm, y, f"{self.rpt_code} · {self.rpt_name}")
        canv.drawRightString(A4[0] - 20 * mm, y, "SCCD-X v2.00 · sea2027")
        canv.setStrokeColor(RULE)
        canv.setLineWidth(0.5)
        canv.line(20 * mm, y - 2.6 * mm, A4[0] - 20 * mm, y - 2.6 * mm)
        foot = L[self.rpt_lang]["footer"].format(
            code=self.rpt_code, lang=LANGNAME[self.rpt_lang], p=doc.page)
        canv.line(20 * mm, 13.5 * mm, A4[0] - 20 * mm, 13.5 * mm)
        canv.drawString(20 * mm, 10 * mm, foot)
        canv.restoreState()


# ---------------------------------------------------------------------------
# The report
# ---------------------------------------------------------------------------
W = 170 * mm


def chip(text, color):
    t = Table([[Paragraph(f'<font color="#ffffff"><b>{esc(text)}</b></font>',
                          S["cellh"])]], hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color),
                           ("LEFTPADDING", (0, 0), (-1, -1), 5),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


def section(story, key, t, **fmt):
    """A section head plus its rule, kept together so a heading never ends
    up orphaned at the foot of a page. No hard page breaks anywhere in this
    report: forcing one after every section left half-empty pages."""
    story.append(KeepTogether([P(esc(t[key].format(**fmt)), "h1"),
                               rule(W, MUTED, 0.8, 1)]))


def build(d, code, lang, path):
    t = L[lang]
    inp = d["inputs"][code]
    dg = d["diagnosis_2027"][code]
    lg = d["diagnosis_15y"][code]
    stz = d["stress_2027"][code]
    prov = d["provenance"][code]
    judg = d["judgment"][code]
    year = d["base_year"]
    cap, tr = dg["capacity"], dg["trajectory"]
    V = dg["verdict"]
    HV = dg["horizon_verdict"] or V

    story = []

    # ---- masthead --------------------------------------------------------
    story.append(P(esc(t["doc"]), "kicker"))
    story.append(P(f"{esc(inp['name'])} <font color='#97948e'>({code})"
                   f"</font>", "title"))
    story.append(P(esc(t["sub"].format(
        d=d["run_date"], y=year, h=d["horizon_2027_years"],
        s=tr.get("solver", "?"))), "subtitle"))
    story.append(Spacer(1, 7))

    # ---- verdict panel ---------------------------------------------------
    tc = TIER_COLOR.get(HV["coherence_tier"], MUTED)
    vp = [
        P(f"<font color='#6c6a66'>{esc(t['verdict_2027'])}</font>", "cellh"),
        Spacer(1, 2),
        P(f"{esc(HV['regime_text'])} &nbsp;/&nbsp; "
          f"<font color='{hx(tc)}'>"
          f"{esc(HV['coherence_tier_text'])}</font>", "verdict"),
        P(esc(HV["adjustment_mode_text"]), "h2"),
        Spacer(1, 3),
        P(f"<b>Ψ</b> {num(tr['psi'][-1])} &nbsp;·&nbsp; "
          f"<b>θ₂₅</b> {num(tr['theta25'][-1])} &nbsp;·&nbsp; "
          f"<b>Δ_norm</b> {num(tr['delta_norm'][-1], sign=True)}"
          f" &nbsp;·&nbsp; <b>R_B</b> {HV['R_B']}", "mono"),
        Spacer(1, 4),
        P(f"<b>{esc(t['gate'])}:</b> {esc(V['gate_text'])}", "note"),
        P(f"<b>{esc(t['loops'])}:</b> "
          f"{esc('+'.join(V['active_loops']) or t['none'])}"
          f" &nbsp;·&nbsp; CAI_core {num(V['cai_core'], 1)}"
          f" &nbsp;·&nbsp; CAI_ext {num(V['cai_ext'], 1)}"
          f" &nbsp;·&nbsp; {esc(t['state_type'])} {esc(inp['state_type'])}"
          f" &nbsp;·&nbsp; {esc(t['weight'])} {num(inp['weight'], 3)}",
          "note"),
    ]
    story.append(panel(vp, width=W))
    story.append(Spacer(1, 3))
    story.append(P(esc(V["headline"]), "tiny"))

    # ---- 1. the triple ---------------------------------------------------
    section(story, "s1", t, y=year)
    rows = [[P(esc(t["measure"]), "cellh"),
             P(str(year), "cellh"), P("2027", "cellh"),
             P("Δ", "cellh"), P(esc(t["comp"]), "cellh")]]
    series = [
        ("Ψ", cap["psi"], tr["psi"][-1], "λ·θ₂₅·(1−C₅)"),
        ("θ₂₅", cap["theta25"], tr["theta25"][-1], "Ŝ₂ / Ŝ₅ gate factor"),
        ("Δ_norm", cap["delta_norm"], tr["delta_norm"][-1], "(S−C)/(S+C)"),
        ("λ", cap["lam"], tr["lam"][-1], "Hill(S₃)"),
        ("S", cap["S"], tr["S"][-1], "λ-weighted state capacity"),
        ("C", cap["C"], tr["C"][-1], "civilian capacity / (1+φC₅^ψ)"),
        ("Ŝ₃", inp["sub"]["s3"], tr["s3"][-1], "legitimacy, BLOCKED proxy"),
        ("Ĉ₅", inp["sub"]["c5"], tr["c5"][-1], "fragmentation, ANALYST"),
        ("Ŝ₅", inp["sub"]["s5"], tr["s5"][-1], "temporal leverage"),
        ("Ŝ₂", inp["sub"]["s2"], tr["s2"][-1], "coercive monopoly"),
        ("d₄", inp["demo"]["d4"], tr["d4"][-1], "dependency inversion"),
    ]
    for nm, a, b, note in series:
        dv = (b - a) if (a is not None and b is not None) else None
        col = BAD if (dv is not None and dv < -0.01) else (
            OK if (dv is not None and dv > 0.01) else MUTED)
        rows.append([P(nm, "cellm"), P(num(a), "cellm"), P(num(b), "cellm"),
                     P(f"<font color='{hx(col)}'>"
                       f"{num(dv, 3, sign=True)}</font>", "cellm"),
                     P(esc(note), "cell")])
    story.append(grid(rows, [22 * mm, 22 * mm, 22 * mm, 22 * mm, 82 * mm],
                      align={1: "RIGHT", 2: "RIGHT", 3: "RIGHT"}))
    story.append(Spacer(1, 4))
    story.append(P(f"dΔ/dt = {num(dg['bifurcation']['d_delta_dt'], 4, True)}"
                   f" &nbsp;({esc(dg['bifurcation']['d_delta_dt_source'])})"
                   f" &nbsp;·&nbsp; decoupling_active = "
                   f"{V['decoupling_active']}"
                   f" &nbsp;·&nbsp; decoupling_index = "
                   f"{num(dg['forcing']['disp']['decoupling_index'])}", "mono"))
    story.append(Spacer(1, 2))
    story.append(P(esc(V["adjustment_mode_desc"]), "note"))

    # ---- 2. inputs and provenance ---------------------------------------
    section(story, "s2", t)
    story.append(P(esc(t["prov_note"]), "note"))
    story.append(Spacer(1, 3))
    tagcol = {"MEASURED": OK, "MIXED": WARN, "ANALYST": BAD}
    labels = {
        "s1": "Ŝ₁ fiscal extraction", "s2": "Ŝ₂ coercive monopoly",
        "s3": "Ŝ₃ legitimacy", "s4": "Ŝ₄ admin penetration",
        "s5": "Ŝ₅ temporal leverage", "c1": "Ĉ₁ capital concentration",
        "c2": "Ĉ₂ civil organisation", "c3": "Ĉ₃ information autonomy",
        "c4": "Ĉ₄ exit options", "c5": "Ĉ₅ fragmentation (inhibitor)",
        "d1": "d₁ carrying-capacity load", "d2": "d₂ expectation trap",
        "d3": "d₃ adjustment autonomy (ROUTER)",
        "d4": "d₄ dependency inversion", "d5": "d₅ surplus youth",
    }
    rows = [[P(esc(t["comp"]), "cellh"), P(esc(t["val"]), "cellh"),
             P(esc(t["tag"]), "cellh"), P(esc(t["terms"]), "cellh")]]
    allv = dict(inp["sub"]); allv.update(inp["demo"])
    for k, lab in labels.items():
        if k not in prov:
            continue
        tg = prov[k]["tag"]
        terms = prov[k]["terms"]
        txt = ", ".join(f"{kk}={num(vv, 3) if isinstance(vv, (int, float)) else esc(vv)}"
                        for kk, vv in terms.items())
        rows.append([P(esc(lab), "cell"), P(num(allv.get(k)), "cellm"),
                     P(f"<font color='{hx(tagcol[tg])}'><b>{tg}</b>"
                       f"</font>", "cellh"), P(esc(txt), "tiny")])
    story.append(grid(rows, [38 * mm, 15 * mm, 24 * mm, 93 * mm],
                      align={1: "RIGHT"}))

    story.append(P("Block A", "h2"))
    a = inp["disp"]
    aterms = prov.get("A", {}).get("terms", {})
    anames = {"a1": "a₁ AI penetration", "a2": "a₂ self-efficacy erosion",
              "a3": "a₃ agency erosion", "a4": "a₄ haven reallocation",
              "a5": "a₅ counter-tech mobilisation",
              "a6": "a₆ AI productivity windfall",
              "physical_share": "physical_share",
              "luxury_contraction": "luxury_contraction"}
    items = [(lab, a[k]) for k, lab in anames.items()]
    half = (len(items) + 1) // 2
    rows = [[P("a", "cellh"), P(esc(t["val"]), "cellh"),
             P("a", "cellh"), P(esc(t["val"]), "cellh")]]
    for i in range(half):
        j = i + half
        rows.append([P(esc(items[i][0]), "cell"), P(num(items[i][1]), "cellm"),
                     P(esc(items[j][0]) if j < len(items) else "", "cell"),
                     P(num(items[j][1]) if j < len(items) else "", "cellm")])
    story.append(grid(rows, [50 * mm, 18 * mm, 50 * mm, 18 * mm],
                      align={1: "RIGHT", 3: "RIGHT"}))
    story.append(Spacer(1, 3))
    story.append(P(", ".join(
        f"{kk}={num(vv,3) if isinstance(vv,(int,float)) else esc(vv)}"
        for kk, vv in aterms.items()), "tiny"))

    story.append(P("Network channels", "h2"))
    ch = [("revenue_polarisation", inp["revenue_polarisation"]),
          ("security_pressure", inp["security_pressure"]),
          ("base_revenue_demand", inp["base_revenue_demand"]),
          ("ret", inp["ret"]), ("opportunity", inp["opportunity"]),
          ("capital_controls", inp["capital_controls"]),
          ("skilled_supply", inp["skilled_supply"])]
    story.append(P(" &nbsp;·&nbsp; ".join(
        f"<b>{k}</b> {num(v)}" for k, v in ch), "mono"))
    story.append(Spacer(1, 4))
    dm = dg["forcing"]["demo"]
    dp = dg["forcing"]["disp"]
    story.append(P(
        f"<b>router</b> {esc(dm['router_mode_text'])} &nbsp;·&nbsp; "
        f"pressure total {num(dm['pressure_total'])} = voluntary "
        f"{num(dm['pressure_voluntary'])} + violent "
        f"{num(dm['pressure_violent'])} &nbsp;·&nbsp; "
        f"τ_demanded {num(dp['tau_demanded'])} vs τ_feasible "
        f"{num(dp['tau_feasible'])} → squeeze "
        f"{num(dp['extraction_squeeze'], 3, True)}", "mono"))

    # ---- 3. judgment -----------------------------------------------------
    section(story, "s3", t)
    story.append(P(esc(t["judg_note"]), "note"))
    story.append(Spacer(1, 3))
    jrows = [[P(k, "cellm"), P(num(v, 2) if isinstance(v, (int, float))
                               else esc(v), "cellm")]
             for k, v in judg.items() if k not in ("why", "state_type")]
    half = (len(jrows) + 1) // 2
    two = [[jrows[i][0], jrows[i][1],
            jrows[i + half][0] if i + half < len(jrows) else P("", "cell"),
            jrows[i + half][1] if i + half < len(jrows) else P("", "cell")]
           for i in range(half)]
    story.append(grid([[P(esc(t["param"]), "cellh"), P(esc(t["val"]), "cellh"),
                        P(esc(t["param"]), "cellh"),
                        P(esc(t["val"]), "cellh")]] + two,
                      [44 * mm, 18 * mm, 44 * mm, 18 * mm],
                      align={1: "RIGHT", 3: "RIGHT"}))
    story.append(Spacer(1, 6))
    story.append(panel([P(esc(judg.get("why", "")), "quote")], width=W,
                       bg=colors.HexColor("#fbf9f4")))

    # ---- 4. gates --------------------------------------------------------
    section(story, "s4", t)
    rows = [[P(esc(t["comp"]), "cellh"), P(esc(t["level"]), "cellh"),
             P(esc(t["drift"]), "cellh"), P(esc(t["thresh"]), "cellh"),
             P(esc(t["years"]), "cellh"), P(esc(t["status"]), "cellh")]]
    for g in sorted(dg["forcing"]["gates"],
                    key=lambda r: (not r["crossed"],
                                   r["years_to_gate"] if r["years_to_gate"]
                                   is not None else 9e9)):
        if g["crossed"]:
            yr, col, stt = t["crossed"], BAD, t["crossed"]
        elif g["years_to_gate"] is None:
            yr, col, stt = "–", MUTED, t["open"]
        else:
            yr = f"{g['years_to_gate']:.1f}"
            col = BAD if g["years_to_gate"] < 15 else (
                WARN if g["years_to_gate"] < 40 else MUTED)
            stt = t["open"]
        rows.append([P(g["component"], "cellm"), P(num(g["level"]), "cellm"),
                     P(num(g["drift"], 4, True), "cellm"),
                     P(f"{g['threshold']:.2f} [{g['threshold_status']}]",
                       "cellm"),
                     P(f"<font color='{hx(col)}'><b>{esc(yr)}</b>"
                       f"</font>", "cellm"), P(esc(stt), "cell")])
    story.append(grid(rows, [18 * mm, 20 * mm, 24 * mm, 30 * mm, 22 * mm,
                             56 * mm],
                      align={1: "RIGHT", 2: "RIGHT", 4: "RIGHT"}))
    story.append(Spacer(1, 4))
    for g in dg["forcing"]["gates"]:
        if g.get("meaning"):
            story.append(P(f"<b>{g['component']}</b> — {esc(g['meaning'])}",
                           "tiny"))

    # ---- 5. loops --------------------------------------------------------
    section(story, "s5", t)
    LP = dg["loops"]
    story.append(P(
        f"CAI_core (L1–L4) = {num(LP['cai_core'], 1)} "
        f"({esc(LP['cai_core_band'])}) &nbsp;·&nbsp; "
        f"CAI_ext (L1–L8) = {num(LP['cai_ext'], 1)} "
        f"({esc(LP['cai_ext_band'])})", "mono"))
    story.append(Spacer(1, 4))
    rows = [[P(esc(t["loop"]), "cellh"), P("", "cellh"),
             P(esc(t["detail"]), "cellh")]]
    for k in [f"L{i}" for i in range(1, 9)]:
        st_ = LP["loops"].get(k)
        if not st_:
            continue
        on = st_["active"]
        rows.append([
            P(f"<b>{k}</b> {esc(st_['name'])}", "cell"),
            P(f"<font color='{hx(BAD if on else MUTED)}'><b>"
              f"{esc(t['on'] if on else t['off'])}</b></font>", "cellh"),
            P(esc(st_.get("detail") or ""), "tiny")])
    story.append(grid(rows, [50 * mm, 18 * mm, 102 * mm]))
    for wtext in LP.get("overlap_warnings", []):
        story.append(Spacer(1, 3))
        story.append(P(esc(wtext), "note"))

    # ---- 6. bifurcation --------------------------------------------------
    section(story, "s6", t)
    B = dg["bifurcation"]
    conds = [("cond_delta_below_crit", "Δ_norm < −δ"),
             ("cond_momentum", "dΔ/dt < −δ_c"),
             ("cond_low_coherence", "Ψ < Ψ_crit = 0.40 [PAPER]")]
    rows = [[P(esc(t["cond"]), "cellh"), P("", "cellh")]]
    for key, lab in conds:
        v = B.get(key)
        rows.append([P(esc(lab), "cell"),
                     P(f"<font color='{hx(BAD if v else MUTED)}'>"
                       f"<b>{v}</b></font>", "cellm")])
    rows.append([P(f"<b>R_B</b>", "cell"), P(f"<b>{B['R_B']}</b>", "cellm")])
    story.append(grid(rows, [120 * mm, 50 * mm]))
    story.append(Spacer(1, 3))
    story.append(P(esc(B["detail"]), "mono"))
    at = dg["attractor"]
    story.append(Spacer(1, 5))
    story.append(P(f"<b>attractor</b> {esc(at.get('most_likely',''))} — "
                   f"{esc(at.get('most_likely_text',''))}", "note"))
    story.append(P(" &nbsp;·&nbsp; ".join(
        f"{k} {num(v)}" for k, v in at.get("scores", {}).items()), "tiny"))
    story.append(P(esc(at.get("note", "")), "tiny"))

    # ---- 7. Monte Carlo --------------------------------------------------
    section(story, "s7", t)
    U = dg["uncertainty"]
    if U:
        story.append(P(
            f"{esc(t['med'])} Δ_norm {num(U['median_delta_norm'],3,True)}"
            f" &nbsp;·&nbsp; {esc(t['ci80'])} "
            f"[{num(U['ci80'][0],3,True)}, {num(U['ci80'][1],3,True)}]"
            f" &nbsp;·&nbsp; {esc(t['ci95'])} "
            f"[{num(U['ci95'][0],3,True)}, {num(U['ci95'][1],3,True)}]"
            f" &nbsp;·&nbsp; {esc(t['med'])} Ψ {num(U['median_psi'])}"
            f" &nbsp;·&nbsp; draws {U['draws']}", "mono"))
        story.append(Spacer(1, 4))
        mix = sorted(U["regime_distribution"].items(), key=lambda kv: -kv[1])
        rows = [[P(esc(t["mix"]), "cellh"), P("%", "cellh")]]
        for k, v in mix:
            rows.append([P(esc(regime_label(k, lang)), "cell"),
                         P(f"{v:.1%}", "cellm")])
        story.append(grid(rows, [120 * mm, 50 * mm], align={1: "RIGHT"}))
        story.append(Spacer(1, 4))
    story.append(P(esc(t["sigma_note"]).format(
        s=", ".join(f"{k} {v}" for k, v in d["sigma"].items())), "tiny"))

    # ---- 8. OAT ----------------------------------------------------------
    section(story, "s8", t)
    fr = [f for f in dg["fragility"] if f["flips_low"] or f["flips_high"]]
    ntot = 42
    story.append(P(esc(t["oat_some"].format(k=len(fr), n=ntot)) if fr
                   else esc(t["oat_none"].format(n=ntot)), "body"))
    if fr:
        rows = [[P(esc(t["param"]), "cellh"), P(esc(t["base"]), "cellh"),
                 P(esc(t["tag"]), "cellh"), P(esc(t["flip"]), "cellh"),
                 P(esc(t["changed"]), "cellh")]]
        for f in fr:
            side = (t["bothside"] if (f["flips_low"] and f["flips_high"])
                    else (t["lowside"] if f["flips_low"] else t["highside"]))
            rows.append([P(esc(f["parameter"]), "cellm"),
                         P(num(f["baseline"], 3), "cellm"),
                         P(esc(f["status"]), "cellh"),
                         P(esc(side), "cell"),
                         P("<br/>".join(esc(x) for x in
                                        f.get("changed_text", [])), "tiny")])
        story.append(grid(rows, [36 * mm, 16 * mm, 23 * mm, 19 * mm,
                                 76 * mm], align={1: "RIGHT"}))

    # ---- 9. stress -------------------------------------------------------
    section(story, "s9", t)
    SV = stz["horizon_verdict"] or stz["verdict"]
    moved = (SV["regime"] != HV["regime"]
             or SV["coherence_tier"] != HV["coherence_tier"]
             or SV["adjustment_mode"] != HV["adjustment_mode"]
             or SV["R_B"] != HV["R_B"]
             or stz["verdict"]["active_loops"] != V["active_loops"])
    story.append(chip(t["moves"] if moved else t["holds"],
                      BAD if moved else MUTED))
    story.append(Spacer(1, 5))
    rows = [[P("", "cellh"), P(esc(t["band"]), "cellh"),
             P(esc(t["tier"]), "cellh"), P(esc(t["mode"]), "cellh"),
             P("Ψ", "cellh"), P("Δ_norm", "cellh"), P("θ₂₅", "cellh"),
             P(esc(t["loops"]), "cellh")]]
    for lab, vv, dd in ((t["baseline"], HV, dg), (t["stress"], SV, stz)):
        rows.append([P(f"<b>{esc(lab)}</b>", "cell"),
                     P(esc(vv["regime_text"]), "cell"),
                     P(esc(vv["coherence_tier_text"]), "cell"),
                     P(esc(vv["adjustment_mode_text"]), "cell"),
                     P(num(dd["trajectory"]["psi"][-1]), "cellm"),
                     P(num(dd["trajectory"]["delta_norm"][-1], 3, True),
                       "cellm"),
                     P(num(dd["trajectory"]["theta25"][-1]), "cellm"),
                     P(esc("+".join(
                         (dd is dg and V or stz["verdict"])["active_loops"])
                         or t["none"]), "cellm")])
    story.append(grid(rows, [20 * mm, 26 * mm, 20 * mm, 30 * mm, 16 * mm,
                             18 * mm, 16 * mm, 24 * mm]))
    story.append(Spacer(1, 5))
    ev = stz.get("events") or {}
    if ev.get("audit"):
        rows = [[P(esc(t["event"]), "cellh"), P(esc(t["intensity"]), "cellh"),
                 P(esc(t["shifts"]), "cellh")]]
        for a_ in ev["audit"]:
            rows.append([
                P(f"<b>{esc(a_['id'])}</b><br/>"
                  f"<font color='#6c6a66'>{esc(a_.get('label',''))}</font>",
                  "cell"),
                P(f"{a_['intensity']:.2f}", "cellm"),
                P("  ".join(f"{k}{v:+.3f}"
                            for k, v in a_.get("applied", {}).items()),
                  "cellm")])
        story.append(grid(rows, [56 * mm, 18 * mm, 96 * mm],
                          align={1: "RIGHT"}))
    story.append(Spacer(1, 5))
    story.append(P(f"<b>{esc(t['why_stress'])}</b>", "h2"))
    story.append(P(esc(d["stress_design"]["rationale"].get(code, "")), "note"))

    # ---- 10. trajectory --------------------------------------------------
    section(story, "s10", t)
    keys = [("delta_norm", "Δ_norm"), ("psi", "Ψ"), ("theta25", "θ₂₅"),
            ("lam", "λ"), ("s3", "Ŝ₃"), ("c5", "Ĉ₅"), ("s5", "Ŝ₅"),
            ("s2", "Ŝ₂"), ("c1", "Ĉ₁"), ("d4", "d₄")]
    rows = [[P(esc(t["t"]), "cellh")] + [P(lab, "cellh") for _, lab in keys]]
    n = len(tr["t"])
    idx = sorted(set(list(range(0, n, max(1, n // 12))) + [n - 1]))
    for i in idx:
        rows.append([P(f"{tr['t'][i]:.2f}", "cellm")]
                    + [P(num(tr[k][i], 3), "cellm") for k, _ in keys])
    story.append(grid(rows, [14 * mm] + [15.6 * mm] * 10, pad=2.4,
                      align={c: "RIGHT" for c in range(1, 11)}))
    # band/tier as a change log rather than a column of repeated wrapped
    # text: over 1.23 years neither usually moves, and when one does, the
    # moment it moves is the only thing worth printing.
    story.append(Spacer(1, 4))
    segs, prev = [], None
    for i in range(n):
        cur = (tr["regime_at_text"][i], tr["tier_at_text"][i])
        if cur != prev:
            segs.append((tr["t"][i], cur))
            prev = cur
    story.append(P(" &nbsp;→&nbsp; ".join(
        f"<b>t={s0:.2f}</b> {esc(a)} / {esc(b)}" for s0, (a, b) in segs),
        "note"))
    story.append(Spacer(1, 4))
    for nt in tr.get("notes", []):
        story.append(P(esc(nt), "tiny"))
    if tr.get("crossings"):
        story.append(Spacer(1, 3))
        for c_ in tr["crossings"]:
            # the key is year_offset, not t - printing t gave "@ t=-"
            story.append(P(
                f"<b>{esc(c_.get('variable', ''))}</b> "
                f"{esc(c_.get('direction_text', ''))} "
                f"{c_.get('threshold')} [{esc(c_.get('threshold_status',''))}]"
                f" @ t={num(c_.get('year_offset'), 2)} "
                f"({esc(c_.get('how', ''))}) — "
                f"{esc(c_.get('meaning', ''))}", "tiny"))

    # ---- 11. 15y ---------------------------------------------------------
    section(story, "s11", t)
    LHV = lg["horizon_verdict"] or lg["verdict"]
    story.append(P(
        f"{year + 15}: <b>{esc(LHV['regime_text'])} / "
        f"{esc(LHV['coherence_tier_text'])}</b> &nbsp;·&nbsp; "
        f"Ψ {num(lg['trajectory']['psi'][-1])} &nbsp;·&nbsp; "
        f"θ₂₅ {num(lg['trajectory']['theta25'][-1])} &nbsp;·&nbsp; "
        f"Δ_norm {num(lg['trajectory']['delta_norm'][-1], 3, True)}"
        f" &nbsp;·&nbsp; R_B {LHV['R_B']} &nbsp;·&nbsp; "
        f"{esc('+'.join(lg['verdict']['active_loops']) or t['none'])}",
        "mono"))
    story.append(Spacer(1, 4))
    gl = [g for g in lg["forcing"]["gates"]]
    gl.sort(key=lambda r: (not r["crossed"],
                           r["years_to_gate"] if r["years_to_gate"]
                           is not None else 9e9))
    story.append(P(" → ".join(
        f"{g['component']} "
        + (t["crossed"] if g["crossed"]
           else (f"{g['years_to_gate']:.0f}y" if g["years_to_gate"]
                 is not None else "–"))
        for g in gl), "mono"))

    # ---- 12. limits ------------------------------------------------------
    section(story, "s12", t)
    for wtext in dg.get("warnings", []):
        story.append(P(esc(wtext), "note"))
    cal = dg["calibration"]
    if cal.get("epistemic_limit"):
        story.append(Spacer(1, 3))
        story.append(panel([P(esc(cal["epistemic_limit"]), "quote")], width=W,
                           bg=colors.HexColor("#fbf4f2")))
    aud = d["audit"]["counts"]
    story.append(Spacer(1, 4))
    story.append(P(
        f"sea2027 provenance across 176 derived fields: "
        + ", ".join(f"{k} {v}" for k, v in sorted(aud.items()))
        + f" &nbsp;·&nbsp; spec {cal.get('spec_version','')} / "
          f"{cal.get('spec2_version','')}", "tiny"))

    Doc(path, code, lang, inp["name"]).build(story)


# ---------------------------------------------------------------------------
def main():
    register_fonts()
    build_styles()
    os.makedirs(OUT, exist_ok=True)
    made = []
    for lang in ("vi", "en"):
        with open(os.path.join(HERE, f"sea2027_{lang}.json"),
                  encoding="utf-8") as f:
            d = json.load(f)
        for code in CODES:
            path = os.path.join(OUT, f"SCCDX-2027-{code}-{lang}.pdf")
            build(d, code, lang, path)
            made.append(path)
            print(f"  {os.path.basename(path):30} "
                  f"{os.path.getsize(path)/1024:7.1f} KB")
    print(f"\n{len(made)} PDFs -> {OUT}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

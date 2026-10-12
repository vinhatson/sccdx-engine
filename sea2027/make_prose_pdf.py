# -*- coding: utf-8 -*-
"""
sea2027.make_prose_pdf - the prose reading, 22 PDFs
====================================================
    python sea2027/make_prose_pdf.py

Writes, into sea2027/pdf_prose/

    SCCDX-2027-PROSE-<CODE>-vi.pdf
    SCCDX-2027-PROSE-<CODE>-en.pdf

This is the companion to make_pdf.py and deliberately the opposite document.
make_pdf.py is the instrument's own output: tables, provenance tags, OAT
rows, the trajectory. This one is the argument about what that output means,
set as continuous prose with only a thin strip of numbers at the top so a
reader can check the claims against the run that produced them.

Typography differs on purpose. Body text is DejaVu SERIF at a 95mm measure
with generous leading, because this is written to be read end to end rather
than consulted. The technical report uses sans at 170mm because it is a
reference. Both faces cover full Vietnamese plus the Unicode subscripts the
engine emits; DejaVuSansMono does not, and is used in neither.

Prose lives in prose_en.py and prose_vi.py. Numbers come from the run JSON,
so the figure strip can never drift from the text's claims without the two
files being edited apart.
"""
from __future__ import annotations

import json
import os
import sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether,
                                PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

import prose_en
import prose_vi

OUT = os.path.join(HERE, "pdf_prose")
CODES = ["ID", "SG", "TH", "VN", "PH", "MY", "MM", "KH", "LA", "BN", "TL"]
PROSE = {"en": prose_en.PROSE, "vi": prose_vi.PROSE}

# ---------------------------------------------------------------------------
INK = colors.HexColor("#17171a")
MUTED = colors.HexColor("#67655f")
FAINT = colors.HexColor("#9b978f")
RULE = colors.HexColor("#d7d2c8")
PANEL = colors.HexColor("#f6f4ef")
ACCENT = colors.HexColor("#6b2318")
BLUE = colors.HexColor("#22394f")

MEASURE = 115 * mm        # the prose column
FULL = 160 * mm

S = {}


def register_fonts() -> None:
    import matplotlib
    d = os.path.join(os.path.dirname(matplotlib.__file__),
                     "mpl-data", "fonts", "ttf")
    win = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    for name, path in (
            ("Serif", os.path.join(d, "DejaVuSerif.ttf")),
            ("Serif-Bold", os.path.join(d, "DejaVuSerif-Bold.ttf")),
            ("Serif-It", os.path.join(d, "DejaVuSerif-Italic.ttf")),
            ("Sans", os.path.join(d, "DejaVuSans.ttf")),
            ("Sans-Bold", os.path.join(d, "DejaVuSans-Bold.ttf")),
            ("Mono", os.path.join(win, "consola.ttf")),
            ("Mono-Bold", os.path.join(win, "consolab.ttf"))):
        if not os.path.exists(path):
            raise SystemExit(f"font missing: {path}")
        pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold",
                                  italic="Serif-It", boldItalic="Serif-Bold")
    pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold",
                                  italic="Sans", boldItalic="Sans-Bold")


def build_styles() -> None:
    def st(n, **kw):
        S[n] = ParagraphStyle(n, **kw)
    st("kicker", fontName="Mono-Bold", fontSize=7.4, leading=10,
       textColor=ACCENT)
    st("country", fontName="Sans-Bold", fontSize=25, leading=29,
       textColor=INK, spaceAfter=2)
    st("title", fontName="Serif-It", fontSize=13.2, leading=18,
       textColor=MUTED, spaceAfter=3)
    st("lede", fontName="Serif", fontSize=11.4, leading=18.4, textColor=INK,
       alignment=TA_JUSTIFY, spaceAfter=7)
    st("body", fontName="Serif", fontSize=9.9, leading=16.6, textColor=INK,
       alignment=TA_JUSTIFY, spaceAfter=9)
    st("h", fontName="Sans-Bold", fontSize=10, leading=13, textColor=BLUE,
       spaceBefore=13, spaceAfter=4)
    st("note", fontName="Serif", fontSize=9.3, leading=15.4, textColor=INK,
       alignment=TA_JUSTIFY, spaceAfter=5)
    st("bullet", fontName="Serif", fontSize=9.3, leading=15, textColor=INK,
       alignment=TA_LEFT, leftIndent=11, bulletIndent=1, spaceAfter=5)
    st("fig", fontName="Mono", fontSize=7.8, leading=11.4, textColor=INK)
    st("figh", fontName="Sans-Bold", fontSize=6.5, leading=9,
       textColor=FAINT)
    st("tiny", fontName="Sans", fontSize=7, leading=10.4, textColor=FAINT,
       alignment=TA_JUSTIFY)


def P(t, s="body"):
    return Paragraph(t, S[s])


def esc(x):
    return escape("" if x is None else str(x), quote=False)


def n3(v, sign=False):
    if v is None:
        return "–"
    return f"{float(v):+.3f}" if sign else f"{float(v):.3f}"


def hrule(w=MEASURE, c=RULE, t=0.6, pad=3):
    tb = Table([[""]], colWidths=[w], rowHeights=[0.1])
    tb.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), t, c),
                            ("TOPPADDING", (0, 0), (-1, -1), pad),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]))
    return tb


def panel(flows, w=MEASURE, bg=PANEL, line=RULE, pad=9):
    tb = Table([[flows]], colWidths=[w], hAlign="LEFT")
    tb.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.5, line),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return tb


LBL = {
 "vi": dict(doc="SCCD-X v2.00 · DIỄN GIẢI VĂN XUÔI · DỰ BÁO 2027",
            run="Chạy {d} · chân trời tới hết 2027 · {s}",
            figs="Các số liệu cách đọc này dựa vào",
            stress="Nhánh stress", frag="Điều gì phải sai",
            watch="Cần theo dõi trong 2027", limits="Engine không nói gì",
            foot="SCCD-X v2.00 · {c} · diễn giải · trang {p}",
            disc="Đây là DIỄN GIẢI, không phải đầu ra của engine. Engine phát "
                 "ra băng, tầng, chế độ, bộ vòng và thứ tự cổng; nó không "
                 "phát ra lập luận về ý nghĩa của chúng. Báo cáo kỹ thuật "
                 "kèm theo (SCCDX-2027-{c}-vi.pdf) chứa các con số và nhãn "
                 "xuất xứ mà bản đọc này đứng trên.",
            band="Băng", tier="Tầng", mode="Chế độ", loops="Vòng",
            xed="đã vượt",
            gate="Cổng gần nhất", none="không có", y15="Mốc 15 năm"),
 "en": dict(doc="SCCD-X v2.00 · PROSE READING · THE 2027 FORECAST",
            run="Run {d} · horizon to end-2027 · {s}",
            figs="The figures this reading rests on",
            stress="The stress branch", frag="What would have to be wrong",
            watch="What to watch in 2027", limits="What the engine does not say",
            foot="SCCD-X v2.00 · {c} · prose · page {p}",
            disc="This is INTERPRETATION, not engine output. The engine emits "
                 "a band, a tier, a mode, a loop set and a gate order; it "
                 "does not emit an argument about what they mean. The "
                 "companion technical report (SCCDX-2027-{c}-en.pdf) carries "
                 "the numbers and provenance tags this reading stands on.",
            band="Band", tier="Tier", mode="Mode", loops="Loops",
            xed="crossed",
            gate="Nearest gate", none="none", y15="At 15 years")}

LANGNAME = {"vi": "Tiếng Việt", "en": "English"}


class Doc(BaseDocTemplate):
    def __init__(self, path, code, lang, name):
        self.rpt_code, self.rpt_lang, self.rpt_name = code, lang, name
        super().__init__(
            path, pagesize=A4,
            leftMargin=25 * mm, rightMargin=25 * mm,
            topMargin=20 * mm, bottomMargin=18 * mm,
            title=f"SCCD-X 2027 prose — {name} ({code}) — {lang}",
            author="SCCD-X v2.00 / sea2027",
            subject="Prose interpretation of the 2027 structural reading",
            lang="vi-VN" if lang == "vi" else "en")
        f = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                  id="m", leftPadding=0, rightPadding=0, topPadding=0,
                  bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="p", frames=[f],
                                            onPage=self._furn)])

    def _furn(self, c, doc):
        c.saveState()
        y = A4[1] - 12 * mm
        c.setFont("Mono", 6.8)
        c.setFillColor(FAINT)
        c.drawString(25 * mm, y, f"{self.rpt_code} · {self.rpt_name}")
        c.drawRightString(A4[0] - 25 * mm, y, "sea2027 · prose")
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.line(25 * mm, y - 2.4 * mm, A4[0] - 25 * mm, y - 2.4 * mm)
        c.line(25 * mm, 15 * mm, A4[0] - 25 * mm, 15 * mm)
        c.drawString(25 * mm, 11.4 * mm,
                     LBL[self.rpt_lang]["foot"].format(
                         c=self.rpt_code, p=doc.page))
        c.drawRightString(A4[0] - 25 * mm, 11.4 * mm,
                          LANGNAME[self.rpt_lang])
        c.restoreState()


def figure_strip(d, code, lang, L):
    """A thin band of the numbers the prose cites, so claims are checkable."""
    x = d["diagnosis_2027"][code]
    lg = d["diagnosis_15y"][code]
    v = x["horizon_verdict"] or x["verdict"]
    lv = lg["horizon_verdict"] or lg["verdict"]
    tr = x["trajectory"]
    gates = [g for g in x["forcing"]["gates"]]
    crossed = [g["component"] for g in gates if g["crossed"]]
    nxt = sorted((g for g in gates
                  if not g["crossed"] and g["years_to_gate"] is not None),
                 key=lambda g: g["years_to_gate"])
    gate_txt = (f"{nxt[0]['component']} ~{nxt[0]['years_to_gate']:.0f}y"
                if nxt else "–")
    if crossed:
        gate_txt += "  (" + "+".join(crossed) + " " + L["xed"] + ")"
    rows = [[P(L["band"], "figh"), P(L["tier"], "figh"), P(L["mode"], "figh"),
             P("Ψ 2027", "figh"), P("θ₂₅", "figh"), P("Δ_norm", "figh"),
             P("R_B", "figh")],
            [P(esc(v["regime_text"]), "fig"),
             P(esc(v["coherence_tier_text"]), "fig"),
             P(esc(v["adjustment_mode_text"]), "fig"),
             P(n3(tr["psi"][-1]), "fig"), P(n3(tr["theta25"][-1]), "fig"),
             P(n3(tr["delta_norm"][-1], True), "fig"),
             P(str(v["R_B"]), "fig")]]
    t1 = Table(rows, colWidths=[23 * mm, 15 * mm, 26 * mm, 13 * mm, 12 * mm,
                                15 * mm, 9 * mm], hAlign="LEFT")  # = 113mm
    t1.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 4)]))
    second = (f"<b>{esc(L['loops'])}</b> "
              f"{esc('+'.join(x['verdict']['active_loops']) or L['none'])}"
              f" &nbsp;·&nbsp; <b>{esc(L['gate'])}</b> {esc(gate_txt)}"
              f" &nbsp;·&nbsp; <b>{esc(L['y15'])}</b> "
              f"{esc(lv['regime_text'])} / {esc(lv['coherence_tier_text'])}")
    return panel([P(esc(L["figs"]), "figh"), Spacer(1, 3), t1,
                  P(second, "fig")], w=MEASURE)


def build(d, code, lang, path):
    L = LBL[lang]
    pr = PROSE[lang][code]
    name = d["inputs"][code]["name"]
    st = []

    st.append(P(esc(L["doc"]), "kicker"))
    st.append(P(f"{esc(name)} <font color='#9b978f' size='15'>({code})"
                f"</font>", "country"))
    st.append(P(esc(pr["title"]), "title"))
    st.append(P(esc(L["run"].format(d=d["run_date"],
                                    s=d["diagnosis_2027"][code]["trajectory"]
                                    ["method"])), "tiny"))
    st.append(Spacer(1, 8))
    st.append(figure_strip(d, code, lang, L))
    st.append(Spacer(1, 10))

    for para in pr["lede"]:
        st.append(P(esc(para), "lede"))
    st.append(hrule())
    st.append(Spacer(1, 4))
    for para in pr["body"]:
        # ** ** marks the one or two sentences per document that carry a
        # negative result; keep them bold rather than inventing a callout.
        txt = esc(para)
        while "**" in txt:
            txt = txt.replace("**", "<b>", 1).replace("**", "</b>", 1)
        st.append(P(txt, "body"))

    st.append(KeepTogether([P(esc(L["stress"]), "h"),
                            P(esc(pr["stress"]), "note")]))
    st.append(KeepTogether([P(esc(L["frag"]), "h"),
                            P(esc(pr["fragile"]), "note")]))

    watch = [P("— " + esc(w), "bullet") for w in pr["watch"]]
    st.append(KeepTogether([P(esc(L["watch"]), "h")] + watch[:2]))
    st.extend(watch[2:])

    st.append(KeepTogether([P(esc(L["limits"]), "h"),
                            P(esc(pr["limits"]), "note")]))
    st.append(Spacer(1, 10))
    st.append(panel([P(esc(L["disc"]).format(c=code), "tiny")],
                    w=MEASURE, bg=colors.HexColor("#fbf6f4")))

    Doc(path, code, lang, name).build(st)


def main():
    register_fonts()
    build_styles()
    os.makedirs(OUT, exist_ok=True)
    made = 0
    for lang in ("vi", "en"):
        with open(os.path.join(HERE, f"sea2027_{lang}.json"),
                  encoding="utf-8") as f:
            d = json.load(f)
        for code in CODES:
            p = os.path.join(OUT, f"SCCDX-2027-PROSE-{code}-{lang}.pdf")
            build(d, code, lang, p)
            made += 1
            print(f"  {os.path.basename(p):36} "
                  f"{os.path.getsize(p)/1024:7.1f} KB")
    print(f"\n{made} prose PDFs -> {OUT}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

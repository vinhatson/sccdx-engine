# -*- coding: utf-8 -*-
"""
SCCD-X — Localisation layer
============================
THE SINGLE SOURCE OF EVERY HUMAN-READABLE STRING IN THE ENGINE.

Design rule, and the reason this module exists at all: the engine emits
**codes**, never prose. `LoopState2.detail_key` is `"loop.L6.detail"` plus a
dict of numbers; `GateProjection.meaning_key` is `"gate.s5"`; a warning is
`("warn.oat_flips", {"n": 4})`. Nothing downstream of the engine contains an
English sentence, so there is no path by which a Vietnamese reading can leak
an English fragment or the reverse.

That is stricter than it needs to be for display, and deliberately so. The
earlier build localised at the view layer, and the result was a page that was
Vietnamese in its chrome and English in every string the engine produced -
loop details, gate meanings, calibration warnings, the whole audit tab. Codes
make the mixed state impossible to construct rather than merely discouraged.

It also makes the test suite language-independent: validate2 asserts on
`gate_code == "S5_GATE_NEAR"`, not on an English substring that a translation
pass could silently break.

CONVENTIONS
-----------
- `t(key, lang, **kw)` renders one template. A missing key raises in strict
  mode so a gap is a loud failure, not a silently English page.
- Templates use `{name}` formatting. Numbers are pre-formatted by the caller
  where the precision matters, because Vietnamese and English differ in
  decimal conventions and the engine should not be guessing.
- Variable NAMES (s1..s5, c1..c5, d1..d5, a1..a6, lambda, theta25, Psi,
  Delta, L1..L8, INC-7, OP2-2) are NOT translated. They are the formalism's
  identifiers and they appear identically in both papers.
- Parameter STATUS tags (PAPER, FREE, ANALYST, DERIVED, DERIVED2, BLOCKED)
  are NOT translated either. They are provenance markers with a fixed meaning
  defined in spec.py / spec2.py, and a reader comparing two runs needs them
  to read the same in both languages.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

LANGS = ("vi", "en")
DEFAULT_LANG = "vi"

# Identifiers that stay as-is in both languages (see CONVENTIONS).
UNTRANSLATED = ("PAPER", "FREE", "ANALYST", "DERIVED", "DERIVED2", "BLOCKED",
                "SCCD", "DEGROW", "DISPL", "DISPL_NUM", "UNCALIBRATED-EXT")


def norm_lang(lang: Optional[str]) -> str:
    l = (lang or DEFAULT_LANG).strip().lower()[:2]
    return l if l in LANGS else DEFAULT_LANG


# ===========================================================================
#  T — the template table
# ===========================================================================
T: Dict[str, Dict[str, str]] = {}


def _add(key: str, vi: str, en: str) -> None:
    T[key] = {"vi": vi, "en": en}


def t(key: str, lang: str = DEFAULT_LANG, strict: bool = True, **kw) -> str:
    """Render one template. Unknown key raises under strict (the default)."""
    lang = norm_lang(lang)
    row = T.get(key)
    if row is None:
        if strict:
            raise KeyError(f"i18n: no template for {key!r}")
        return key
    s = row.get(lang) or row.get("en") or key
    if kw:
        try:
            return s.format(**kw)
        except (KeyError, IndexError) as e:
            raise KeyError(f"i18n: {key!r} missing format arg: {e}") from None
    return s


def resolve(v: Any, lang: str) -> Any:
    """Resolve a template PARAMETER that is itself a localisable thing.

    Three forms are accepted, so a sentence never ends up containing an
    untranslated fragment of the other language:

      "regime.Crisis"                        a bare key, rendered as-is
      {"__key": "tg.S5_GATE_NEAR", "y": 2}   a key WITH its own parameters
      anything else                          passed straight through

    The dict form exists because some nested templates take arguments of
    their own - the gate verdict needs its year count - and a bare key
    cannot carry them.
    """
    if isinstance(v, dict) and "__key" in v:
        k = v["__key"]
        args = {kk: resolve(vv, lang) for kk, vv in v.items()
                if kk != "__key"}
        return t(k, lang, strict=False, **args)
    if isinstance(v, str) and "." in v and v in T:
        return t(v, lang)
    return v


def render(key: str, args: Optional[dict], lang: str) -> str:
    """Render one template, resolving any localisable parameters first."""
    a = {k: resolve(v, lang) for k, v in (args or {}).items()}
    return t(key, lang, **a)


def tparts(parts: List, lang: str, sep: str = "; ") -> str:
    """Render a list of (key, params) descriptors into one sentence."""
    out = []
    for p in parts or []:
        if isinstance(p, (list, tuple)) and len(p) >= 1:
            out.append(render(p[0], p[1] if len(p) > 1 else {}, lang))
        else:
            out.append(t(str(p), lang))
    return sep.join(out)


def tlist(codes: List, lang: str) -> List[str]:
    """Render a list of (key, params) descriptors into a list of strings."""
    out = []
    for c in codes or []:
        if isinstance(c, (list, tuple)) and len(c) >= 1:
            out.append(render(c[0], c[1] if len(c) > 1 else {}, lang))
        else:
            out.append(t(str(c), lang))
    return out


# ===========================================================================
#  1. ENUMS — regime bands, stability, coherence tiers, adjustment modes
# ===========================================================================
_add("regime.Imperial", "Đế quốc", "Imperial")
_add("regime.Hegemonic", "Bá quyền", "Hegemonic")
_add("regime.Negotiated", "Thương lượng", "Negotiated")
_add("regime.Equilibrium", "Cân bằng", "Equilibrium")
_add("regime.Crisis", "Khủng hoảng", "Crisis")
_add("regime.Crisis (below modelled range)",
     "Khủng hoảng (dưới khoảng mô hình hóa)", "Crisis (below modelled range)")
_add("regime.Imperial (above modelled range)",
     "Đế quốc (trên khoảng mô hình hóa)", "Imperial (above modelled range)")

_add("stab.Unstable (drain)", "Bất ổn (rò rỉ)", "Unstable (drain)")
_add("stab.Metastable", "Á bền", "Metastable")
_add("stab.Conditionally stable", "Bền có điều kiện",
     "Conditionally stable")
_add("stab.Stable or Gridlock", "Bền hoặc Tắc nghẽn", "Stable or Gridlock")
_add("stab.Unstable (bifurcation)", "Bất ổn (phân nhánh)",
     "Unstable (bifurcation)")

_add("tier.Coherent", "Mạch lạc", "Coherent")
_add("tier.Strained", "Căng", "Strained")
_add("tier.Incoherent", "Mất mạch lạc", "Incoherent")

_add("mode.VOLUNTARY", "ĐIỀU CHỈNH TỰ NGUYỆN", "VOLUNTARY ADJUSTMENT")
_add("mode.VIOLENT_EXPOSED", "PHƠI NHIỄM ĐIỀU CHỈNH BẠO LỰC",
     "VIOLENT-ADJUSTMENT EXPOSED")
_add("mode.MIXED", "HỖN HỢP", "MIXED")
_add("mode.SLACK", "CHƯA CHỊU ÁP", "SLACK")

_add("mode.VOLUNTARY.desc",
     "d₃ cao, d₅ thấp — áp lực xả qua đường từ chối sinh sản rồi đến đảo "
     "chiều phụ thuộc. Đây là đường hiện đại của Degrow. Cổng kết thúc: Ŝ₅ "
     "tụt xuống dưới sàn 0.15 của θ₂₅.",
     "d3 high, d5 low - pressure discharges through fertility refusal and "
     "then dependency inversion. Degrow's modern path. Terminal gate: S5 "
     "falling through theta25's 0.15 floor.")
_add("mode.VIOLENT_EXPOSED.desc",
     "d₃ thấp, d₅ cao — không có công cụ tự nguyện và có một lớp thanh niên "
     "lớn không phần. Đây là đường cổ đại của Degrow. Cổng kết thúc: Ŝ₂ tụt "
     "xuống dưới sàn 0.25 của θ₂₅.",
     "d3 low, d5 high - no voluntary instruments and a large cohort with no "
     "stake. Degrow's ancient path. Terminal gate: S2 falling through "
     "theta25's 0.25 floor.")
_add("mode.MIXED.desc",
     "cả hai kênh đều đang tải áp lực, hoặc không kênh nào trội.",
     "both channels carrying pressure, or neither dominant.")
_add("mode.SLACK.desc",
     "tải đủ thấp để chưa có điều chỉnh nào bị đòi.",
     "load low enough that no adjustment is being demanded.")

_add("router.conserve", "bảo toàn", "conserve")
_add("router.discount", "chiết giảm", "discount")

# ===========================================================================
#  2. COMPONENTS — label + help
# ===========================================================================
_add("comp.s1.label", "S₁ Năng lực Thu trích Tài khóa",
     "S1 Fiscal Extraction Capacity")
_add("comp.s1.help",
     "Tỷ lệ thu ngân sách còn quyền định đoạt. sccd Part III.",
     "Net discretionary revenue ratio. sccd Part III.")
_add("comp.s2.label", "S₂ Chỉ số Độc quyền Cưỡng chế",
     "S2 Coercive Monopoly Index")
_add("comp.s2.help",
     "Phần năng lực cưỡng chế có tổ chức mà nhà nước giữ. CÓ CỔNG tại 0.25 "
     "[PAPER]: dưới mức đó θ₂₅ sụp.",
     "State share of organised coercive capacity. GATED at 0.25 [PAPER]: "
     "below it theta25 collapses.")
_add("comp.s3.label", "S₃ Vốn Chính danh", "S3 Legitimacy Capital")
_add("comp.s3.help",
     "Điều khiển λ, mà λ nhân vào TOÀN BỘ S. sccd Part III §2.3 gọi đây là "
     "proxy rủi ro cao nhất, và api_readiness() đánh dấu BLOCKED — không có "
     "nguồn máy đọc được đa quốc gia.",
     "Drives lambda, which multiplies ALL of S. sccd Part III 2.3 names it "
     "the highest-risk proxy, and api_readiness() marks it BLOCKED - no "
     "multi-country machine source exists.")
_add("comp.s4.label", "S₄ Độ sâu Thâm nhập Hành chính",
     "S4 Administrative Penetration Depth")
_add("comp.s4.help",
     "Tầm với thực thi chính sách. api_readiness(): BLOCKED, phải mã hóa thủ "
     "công.",
     "Policy implementation reach. api_readiness(): BLOCKED, requires manual "
     "coding.")
_add("comp.s5.label", "S₅ Đòn bẩy Thời gian", "S5 Temporal Leverage")
_add("comp.s5.help",
     "Chân trời ngân sách CHƯA BỊ CAM KẾT — lương hưu và trả nợ ĐÃ bị trừ ra "
     "khỏi con số này. CÓ CỔNG tại 0.15 [PAPER].",
     "UNCOMMITTED revenue horizon - pensions and debt service are already "
     "netted out. GATED at 0.15 [PAPER].")
_add("comp.c1.label", "C₁ Tập trung Vốn Tư nhân",
     "C1 Private Capital Concentration")
_add("comp.c1.help",
     "Ngưỡng thâu tóm tại 0.70 [PAPER]: trên mức đó Γ bật và L1 có thể lên "
     "nòng.",
     "Capture threshold at 0.70 [PAPER]: above it Gamma turns on and L1 can "
     "arm.")
_add("comp.c2.label", "C₂ Mật độ Tổ chức Dân sự",
     "C2 Civil Organisation Density")
_add("comp.c2.help",
     "Trong dC₅/dt đã vá, đây là đối trọng GIẢM PHÂN CỰC, qua số hạng "
     "−ν·C₅·C₂.",
     "In the patched dC5/dt this is the DEPOLARISING counterweight, via "
     "-nu*C5*C2.")
_add("comp.c3.label", "C₃ Tự chủ Thông tin", "C3 Information Autonomy")
_add("comp.c3.help", "Độc lập của truyền thông và thông tin.",
     "Media and information independence.")
_add("comp.c4.label", "C₄ Khả dụng Lựa chọn Thoát",
     "C4 Exit Option Availability")
_add("comp.c4.help",
     "CHỈ gồm thoát theo quyền phán xử — độ mở tài khoản vốn và lựa chọn di "
     "cư. Không có số hạng nào cho thoát theo hình thái tài sản; đó là phần "
     "a₄ của Block A bổ vào.",
     "JURISDICTION exit only - capital-account openness and emigration. "
     "Contains no term for asset-form exit; that is what Block A's a4 adds.")
_add("comp.c5.label", "C₅ Phân mảnh Ưu tiên",
     "C5 Preference Fragmentation")
_add("comp.c5.help",
     "CHẤT ỨC CHẾ — vào làm mẫu số của C và làm hệ số (1−C₅) trong Ψ. "
     "api_readiness(): BLOCKED.",
     "INHIBITOR - enters as the C denominator and as (1-C5) in Psi. "
     "api_readiness(): BLOCKED.")

# --- Block D ---
_add("comp.d1.label", "d₁ Tải Sức chứa", "d1 Carrying-Capacity Load")
_add("comp.d1.help",
     "Tải dân số cộng kỳ vọng, so với khả năng của hệ thống cung cấp một mức "
     "sống chấp nhận được. Thời cổ: đất canh tác, thủy lợi, năng suất tĩnh. "
     "Thời nay, theo đúng lời paper: 'khả năng cung cấp việc làm thu nhập ổn "
     "định, nhà ở vừa khả năng chi trả, giáo dục và y tế chất lượng, và một "
     "môi trường sinh thái bền vững'.",
     "Population + expectation load relative to the system's ability to "
     "supply an acceptable standard of living. Ancient: arable land, "
     "irrigation, static yields. Modern, per the paper: 'the ability to "
     "provide stable-income jobs, affordable housing, quality education and "
     "healthcare services, and a sustainable ecological environment'.")
_add("comp.d2.label", "d₂ Bẫy Kỳ vọng", "d2 Expectation Trap")
_add("comp.d2.help",
     "Chi phí lập gia đình so với thu nhập — tỷ lệ giá nhà/thu nhập, chi phí "
     "giáo dục và trông trẻ, cộng lạm phát kỳ vọng. Đây là thứ paper đưa vào "
     "thay cho khan hiếm lương thực kiểu Malthus: 'quá nhiều áp lực phải "
     "hoàn hảo, quá nhiều chi phí cố định'. Paper ví thẳng với tình trạng mất "
     "đất thời cổ: cả hai đều là 'sự chối bỏ cơ hội thiết lập một nền tảng "
     "gia đình ổn định'.",
     "Cost of household formation relative to income - housing/income ratio, "
     "education and childcare cost, plus expectation inflation. The paper's "
     "substitute for Malthusian food scarcity: 'too much pressure for "
     "perfection, too many fixed costs'. Explicitly analogised to ancient "
     "landlessness: both are 'a denial of the opportunity to establish a "
     "stable family foundation'.")
_add("comp.d3.label", "d₃ Quyền tự chủ Điều chỉnh",
     "d3 Adjustment Autonomy")
_add("comp.d3.help",
     "Sự sẵn có VÀ việc thực sử dụng các công cụ điều chỉnh tự nguyện: tránh "
     "thai, hoạch định tài chính, thông tin, quyền tự chủ cá nhân, và việc "
     "phúc lợi thay thế vai trò con cái lúc tuổi già (điều đã 'cắt đứt mối "
     "liên kết sinh tồn giữa các thế hệ'). 0 = thời cổ (không công cụ, áp lực "
     "buộc phải xả bằng bạo lực). 1 = OECD hiện đại. ĐÂY LÀ BIẾN ĐỊNH TUYẾN.",
     "Availability AND use of voluntary adjustment instruments: "
     "contraception, financial planning, information, individual autonomy, "
     "and welfare substitution for old-age support (which 'severed the "
     "intergenerational survival link'). 0 = ancient (no tools, pressure must "
     "discharge violently). 1 = modern OECD. THIS IS THE ROUTER VARIABLE.")
_add("comp.d4.label", "d₄ Đảo chiều Phụ thuộc", "d4 Dependency Inversion")
_add("comp.d4.help",
     "Tỷ lệ phụ thuộc người cao tuổi, cộng phần ngân sách đã bị cam kết "
     "trước cho lương hưu và y tế theo cơ chế PAYG. Nguyên văn paper: 'Khi "
     "kim tự tháp đảo chiều, mô hình này sụp.'",
     "Old-age dependency ratio plus the share of revenue pre-committed to "
     "PAYG pensions and health. The paper: 'When the pyramid inverts, this "
     "model collapses.'")
_add("comp.d5.label", "d₅ Lớp Thanh niên Dư thừa",
     "d5 Surplus Youth Cohort")
_add("comp.d5.help",
     "Lớp trẻ không tài sản, không đất, không việc làm, không triển vọng — "
     "cái mà paper gọi là 'đạo quân dự bị của hỗn loạn', 'những thanh niên "
     "bần cùng, ít học, không tài sản và không tương lai... là nhiên liệu "
     "sinh học cho cách mạng và nội chiến'.",
     "Young cohort without assets, land, employment or prospects - the "
     "paper's 'reserve army of chaos', 'impoverished, uneducated youths with "
     "no assets and no future... the biofuel for revolution and civil war'.")

# --- Block A ---
_add("comp.a1.label", "a₁ Mức Thâm nhập AI", "a1 AI Penetration")
_add("comp.a1.help",
     "Tỷ phần công việc nhận thức và ra quyết định thường ngày có AI làm "
     "trung gian. Đây là biến phổ cập của paper: 'mức phổ cập đạt được với "
     "tốc độ vượt mọi công nghệ tiêu dùng trước đó'.",
     "Share of daily cognitive and decision tasks mediated by AI. The "
     "paper's adoption variable: 'mass adoption at a pace exceeding any prior "
     "consumer technology'.")
_add("comp.a2.label", "a₂ Xói mòn Tự-hiệu-năng (Tầng 1)",
     "a2 Self-Efficacy Erosion (Tier 1)")
_add("comp.a2.help",
     "Mất cảm giác tự-hiệu-năng theo nghĩa Bandura, do đối diện những hệ "
     "thống làm tốt hơn mình. 'Tôi còn kiếm sống được không?' Dẫn tới hành vi "
     "tài chính phòng vệ.",
     "Bandura-sense efficacy loss from confronting systems that outperform "
     "the user. 'Can I still earn a living?' Drives defensive financial "
     "behaviour.")
_add("comp.a3.label", "a₃ Xói mòn Tự chủ (Tầng 2)",
     "a3 Agency Erosion (Tier 2)")
_add("comp.a3.help",
     "Mất quyền tác giả ở tầng hiện sinh: Hiệu ứng Con rối, sự nhòe lẫn giữa "
     "bản thân và thuật toán, sự tan rã của bản sắc tự thuật. 'Tôi còn là tôi "
     "không?' Đây là tầng sâu nhất của paper, và là tầng chạm tới tính chính "
     "danh của quyền lực nhà nước.",
     "Existential loss of authorship: the Puppet Effect, blurring of self "
     "and algorithm, dissolution of narrative identity. 'Am I still me?' The "
     "paper's deepest layer, and the one that reaches sovereign legitimacy.")
_add("comp.a4.label", "a₄ Tái phân bổ vào Trú ẩn",
     "a4 Haven Reallocation")
_add("comp.a4.help",
     "Tỷ phần vốn khả dụng đã chuyển vào các kho giá trị hữu hình, độc lập "
     "thuật toán, và không khả-kiến với nhà nước — trước hết là vàng và bạc "
     "vật chất. Nguyên văn: 'Vàng... trở thành một biểu tượng của sự kháng "
     "cự — một mỏ neo hữu hình cho bản ngã.'",
     "Share of discretionary capital moved into tangible, "
     "algorithm-independent, state-illegible stores of value - physical gold "
     "and silver above all. 'Gold... becomes a symbol of resistance - a "
     "tangible anchor for the self.'")
_add("comp.a5.label", "a₅ Động viên Phản-công-nghệ",
     "a5 Counter-Tech Mobilisation")
_add("comp.a5.help",
     "Chủ nghĩa Luddite Mới mà paper dự báo: 'rút lui công nghệ một cách có "
     "ý thức... sự trỗi dậy lại của kinh tế thủ công và nghề làm tay... xây "
     "dựng cộng đồng lấy sự hiện diện thân thể làm trung tâm'. Lưu ý đây là "
     "một lực TỔ CHỨC, nên trong thuật ngữ sccd nó LÀM TĂNG Ĉ₂.",
     "The predicted New Luddism: 'conscious technology withdrawal... "
     "resurgence of artisanal and handcraft economies... community-building "
     "centered on physical co-presence'. Note it is an ORGANISING force, so "
     "in sccd terms it RAISES C2.")
_add("comp.a6.label", "a₆ Thặng dư Năng suất từ AI",
     "a6 AI Productivity Windfall")
_add("comp.a6.help",
     "Số hạng phía sản lượng. Vào G(t) qua cùng khe mà T_shock dùng trong "
     "sccd Part II eq (12).",
     "The output-side term. Enters sccd's G(t) through the same slot as "
     "T_shock in Part II eq (12).")

# --- scalars ---
_add("scal.revenue_polarisation.label", "Phân cực Nguồn thu",
     "Revenue polarisation")
_add("scal.revenue_polarisation.help",
     "Vào bài kiểm L3 của sccd và vào số hạng ε_p trong dC₅/dt.",
     "Enters sccd's L3 test and the dC5/dt eps_p term.")
_add("scal.security_pressure.label", "Áp lực An ninh",
     "Security pressure")
_add("scal.security_pressure.help",
     "Làm tăng τ_demanded, thứ điều khiển độ siết của vòng L6.",
     "Raises tau_demanded, which drives the L6 squeeze.")
_add("scal.base_revenue_demand.label", "Nhu cầu Thu nền",
     "Base revenue demand")
_add("scal.base_revenue_demand.help",
     "Yêu cầu tài khóa nền, tính theo tỷ lệ, so sánh được với τ_max=0.20. "
     "Thường rơi vào 0.04–0.11.",
     "Baseline fiscal claim as a rate, comparable to tau_max=0.20. Typical "
     "0.04-0.11.")
_add("scal.g_shock.label", "Cú sốc Sinh thặng dư", "Generation shock")
_add("scal.g_shock.help",
     "Đưa vào điểm chọn attractor A₁ của sccd.",
     "Feeds sccd's attractor-selection score for A1.")
_add("scal.luxury_contraction.label", "Co cụm Cầu Xa xỉ",
     "Luxury contraction")
_add("scal.luxury_contraction.help",
     "Block A. Mức co lại đã quan sát được của cầu hàng hóa định danh.",
     "Block A. Observed contraction in identity-goods demand.")
_add("scal.physical_share.label", "Tỷ phần Vật chất trong Trú ẩn",
     "Physical share of haven")
_add("scal.physical_share.help",
     "Block A. Tách vàng vật chất khỏi vàng giấy trong a₄. Dự đoán thứ ba "
     "của paper là tỷ phần này tăng.",
     "Block A. Physical vs paper split of a4. The paper's third prediction "
     "is that this rises.")

# ===========================================================================
#  3. LOOPS — names, detail templates, sources
# ===========================================================================
_add("loop.L1.name", "Bộ Gia tốc Thâu tóm Quy chế",
     "Regulatory Capture Accelerator")
_add("loop.L2.name", "Vòng Xoáy Mất Chính danh", "Legitimacy Death Spiral")
_add("loop.L3.name", "Bẫy Phân cực", "Polarisation Trap")
_add("loop.L4.name", "Ghép Thoát–Phân mảnh", "Exit-Fragmentation Coupling")
_add("loop.L5.name", "Vòng Xoáy Tự chủ–Chính danh",
     "Agency-Legitimacy Spiral")
_add("loop.L6.name", "Vòng Xoáy Khả-kiến–Thu-trích",
     "Legibility-Extraction Spiral")
_add("loop.L7.name", "Bẫy Đảo chiều Dân số", "Demographic Inversion Trap")
_add("loop.L8.name", "Xả áp Thanh niên Dư thừa", "Youth-Surplus Discharge")

_add("loop.src.sccd", "sccd Part IV §2", "sccd Part IV 2")
_add("loop.src.L5",
     "DISPL §4.4 (phía rút cạn) × sccd II.eq2-3 (nhánh hồi tiếp)",
     "DISPL 4.4 (drain) x sccd II.eq2-3 (return leg)")
_add("loop.src.L6",
     "DEGROW §2.1 (con bò gầy trơ xương) × DISPL §5.4 (dòng chảy vào kim "
     "loại vật chất) — chính là điểm hai bài báo trùng nhau",
     "DEGROW 2.1 (the emaciated cow) x DISPL 5.4 (flight into physical "
     "metal) - the point where the two papers coincide")
_add("loop.src.L7",
     "DEGROW §Đảo chiều Kim tự tháp Phúc lợi + §Bẫy Kỳ vọng, được engine "
     "khép lại thành một vòng",
     "DEGROW Invert the Welfare Pyramid + Expectation Trap, closed into a "
     "loop by the engine")
_add("loop.src.L8", "DEGROW Giai đoạn 2–3", "DEGROW Stages 2-3")

# detail templates — the numbers come from the engine as pre-formatted strings
_add("loop.L1.detail",
     "Ĉ₁={c1} so với ngưỡng {c1_t} ({c1_s}); Ŝ₂={s2} so với ngưỡng {s2_t} "
     "({s2_s})",
     "C1={c1} vs crit {c1_t} ({c1_s}); S2={s2} vs crit {s2_t} ({s2_s})")
_add("loop.L1.over", "VƯỢT", "OVER")
_add("loop.L1.under", "dưới", "under")
_add("loop.L1.below", "DƯỚI", "BELOW")
_add("loop.L1.above", "trên", "above")

_add("loop.L2.detail",
     "S₃={s3} so với ngưỡng {s3_t}; λ={lam} so với ngưỡng {lam_t} → {status}",
     "S3={s3} vs crit {s3_t}; lambda={lam} vs crit {lam_t} -> {status}")
_add("loop.L2.explosive", "BÙNG NỔ", "EXPLOSIVE")
_add("loop.L2.approaching", "ĐANG TIẾN TỚI", "APPROACHING")
_add("loop.L2.damped", "tắt", "damped")

_add("loop.L3.detail",
     "C₅={c5} so với {c5_t}; Phân cực nguồn thu={rp} so với {rp_t} "
     "(PROXY THEO MỨC — bài kiểm chính thức cần ε_p, η và tốc độ giảm phân "
     "cực tự nhiên)",
     "C5={c5} vs {c5_t}; Rev_Pol={rp} vs {rp_t} (LEVEL PROXY - the formal "
     "test needs eps_p, eta and the natural depolarisation rate)")
_add("loop.L4.detail",
     "Ĉ₄={c4} so với {c4_t}; Ĉ₁={c1} so với {c1_t} (PROXY THEO MỨC — bài "
     "kiểm chính thức cần ξ, χ, tốc độ phân rã C₅ tự nhiên và G_base)",
     "C4={c4} vs {c4_t}; C1={c1} vs {c1_t} (LEVEL PROXY - the formal test "
     "needs xi, chi, the natural C5 decay and G_base)")
_add("loop.L5.detail",
     "a₁={a1} so với {a1_t} [{c_pen}]; a₃={a3} so với {a3_t} [{c_ag}]; "
     "dS₃/dt={drift}/năm [{c_dr}] → λ hiện tại {lam}",
     "a1={a1} vs {a1_t} [{c_pen}]; a3={a3} vs {a3_t} [{c_ag}]; "
     "dS3/dt={drift}/yr [{c_dr}] -> lambda now {lam}")
_add("loop.L6.detail",
     "độ siết={sq} so với {sq_t} [{c_sq}] (đòi {dem} so với khả thi {feas}); "
     "a₄={a4} so với {a4_t} [{c_fl}], tỷ phần vật chất {phys}",
     "squeeze={sq} vs {sq_t} [{c_sq}] (demanded {dem} vs feasible {feas}); "
     "a4={a4} vs {a4_t} [{c_fl}], physical share {phys}")
_add("loop.L7.detail",
     "d₄={d4} so với {d4_t} [{c4}]; d₂={d2} so với {d2_t} [{c2}]; "
     "d₃={d3} so với {d3_t} [{c3}]",
     "d4={d4} vs {d4_t} [{c4}]; d2={d2} vs {d2_t} [{c2}]; d3={d3} vs "
     "{d3_t} [{c3}]")
_add("loop.L8.detail",
     "d₅={d5} so với {d5_t} [{c5}]; d₃={d3} dưới {d3_t} [{c3}]; S₂={s2} dưới "
     "{s2_t} [{cs2}]; áp lực bạo lực {pv}",
     "d5={d5} vs {d5_t} [{c5}]; d3={d3} below {d3_t} [{c3}]; S2={s2} below "
     "{s2_t} [{cs2}]; violent pressure {pv}")

# loop descriptions (long form, shown in the schema and the audit tab)
_add("loop.L5.desc",
     "a₃ xói mòn tự chủ rút cạn S₃ → λ giảm → năng lực giao hàng chính sách "
     "giảm → chính sách thất bại lộ rõ → ý nghĩa và quyền tác giả xói mòn "
     "thêm. Nguồn: DISPL §4.4 cho phía rút cạn; nhánh hồi tiếp là chính cấu "
     "trúc số nhân λ của sccd. Ghép vào L2 và L3.",
     "a3 agency erosion drains S3 -> lambda falls -> delivery capacity falls "
     "-> policy fails visibly -> meaning and authorship erode further. "
     "Source: DISPL 4.4 for the drain; the return leg is sccd's own "
     "lambda-multiplier structure. Couples into L2 and L3.")
_add("loop.L6.desc",
     "Mức thu-trích bị đòi vượt mức khả thi → nhà nước đè nặng hơn lên phần "
     "cơ sở còn khả-kiến → thêm tài sản dịch sang hình thái không khả-kiến "
     "(a₄) → phần cơ sở khả-kiến teo thêm. Nguồn: DEGROW §2.1 × DISPL §5.4. "
     "Vòng này chính là chỗ hai bài báo mới là cùng một bài. Ghép vào L1 và "
     "L4.",
     "Extraction demanded exceeds extraction feasible -> the state leans "
     "harder on the legible base -> more wealth relocates into non-legible "
     "form (a4) -> the legible base shrinks further. Source: DEGROW 2.1 x "
     "DISPL 5.4. This loop is the point where the two new papers are the "
     "same paper. Couples into L1 and L4.")
_add("loop.L7.desc",
     "Đảo chiều phụ thuộc chèn ép không gian tài khóa → thứ bị cắt chính là "
     "hỗ trợ lập gia đình → bẫy kỳ vọng siết lại → sinh suất giảm thêm → đảo "
     "chiều sâu thêm. Nguồn: DEGROW §Đảo chiều Kim tự tháp Phúc lợi + §Bẫy "
     "Kỳ vọng — paper mô tả cả hai nhánh nhưng không bao giờ nối chúng lại. "
     "Ghép vào L2 và L6.",
     "Dependency inversion crowds fiscal space -> support for household "
     "formation is what gets cut -> the expectation trap tightens -> "
     "fertility falls further -> inversion deepens. Source: DEGROW Invert "
     "the Welfare Pyramid + Expectation Trap - the paper describes both arms "
     "but never joins them. Couples into L2 and L6.")
_add("loop.L8.desc",
     "Thanh niên dư thừa không phần × độc quyền cưỡng chế yếu × không công "
     "cụ điều chỉnh tự nguyện → đường xả cổ đại: phân mảnh và bất ổn tăng, "
     "Ŝ₂ tụt xuống dưới cổng θ₂₅ của nó. Nguồn: DEGROW Giai đoạn 2–3. Đây là "
     "vòng cho phép engine đọc được nửa trẻ của thế giới; L5–L7 đều là vòng "
     "của xã hội giàu và già. Ghép vào L2 và L3.",
     "Surplus youth with no stake x weak coercive monopoly x no voluntary "
     "adjustment tools -> the ancient discharge path: fragmentation and "
     "unrest rise, S2 falls below its theta25 gate. Source: DEGROW Stages "
     "2-3. This is the loop that lets the engine read the young half of the "
     "world at all; L5-L7 are rich-aging-society loops. Couples into L2 and "
     "L3.")

# CAI bands + horizons
_add("cai.damped", "tắt", "damped")
_add("cai.manageable", "kiểm soát được", "manageable")
_add("cai.compounding", "hợp thành", "compounding")
_add("cai.imminent", "cận kề", "imminent")
_add("cai.h.damped", "động lực học tuyến tính chiếm ưu thế",
     "linear dynamics dominate")
_add("cai.h.manageable",
     "1–2 vòng đang chạy; hiệu ứng phi tuyến còn kiểm soát được",
     "1-2 loops active; manageable non-linear effects")
_add("cai.h.compounding",
     "3 vòng đang chạy; khủng hoảng có khả năng xảy ra trong 5–10 năm",
     "3 loops active; crisis likely within 5-10 years")
_add("cai.h.imminent",
     "mọi vòng đang chạy; phân nhánh cận kề; chân trời 1–3 năm",
     "all loops active; bifurcation imminent; 1-3 year horizon")
_add("cai.ext_suffix",
     " [MỞ RỘNG: biên băng đã chia lại theo tỷ lệ 4/8, UNCALIBRATED-EXT]",
     " [EXT: band edges rescaled 4/8, UNCALIBRATED-EXT]")

# ===========================================================================
#  4. GATES, CROSSINGS, TERMINAL-GATE VERDICTS
# ===========================================================================
_add("gate.s5",
     "Cổng ngưỡng θ₂₅ — chân trời ngân sách chưa bị cam kết. Điểm cuối tự "
     "nguyện/già hóa của Degrow.",
     "theta25 threshold gate - uncommitted revenue horizon. Degrow's "
     "voluntary/aging terminus.")
_add("gate.s2",
     "Cổng ngưỡng θ₂₅ — độc quyền cưỡng chế. Điểm cuối bạo lực/thanh niên "
     "của Degrow.",
     "theta25 threshold gate - coercive monopoly. Degrow's violent/youth "
     "terminus.")
_add("gate.s3",
     "Ngưỡng bùng nổ của vòng L2 trong sccd — dưới mức này vòng xoáy mất "
     "chính danh trở thành tự duy trì.",
     "sccd loop L2 explosive threshold - the legitimacy death spiral becomes "
     "self-sustaining below this.")
_add("gate.c5",
     "Ngưỡng bẫy phân cực của vòng L3 trong sccd. LƯU Ý ngưỡng này là một "
     "tham số FREE trong paper gốc — không có giá trị số nào được nêu ở bất "
     "kỳ đâu trong Parts I–V — nên thời điểm vượt nó là tùy ý theo cách mà "
     "các cổng S₂/S₅/S₃ không bị.",
     "sccd loop L3 polarisation-trap threshold. NOTE this one is a FREE "
     "parameter in the source paper - no numeric value is given anywhere in "
     "Parts I-V - so the crossing date is arbitrary in a way the S2/S5/S3 "
     "gates are not.")

_add("cross.s5",
     "cổng θ₂₅ đóng — điểm cuối tự nguyện/già hóa của Degrow",
     "theta25 gate closes - Degrow voluntary/aging terminus")
_add("cross.s2",
     "cổng θ₂₅ đóng — điểm cuối bạo lực/thanh niên của Degrow",
     "theta25 gate closes - Degrow violent/youth terminus")
_add("cross.s3",
     "vòng xoáy mất chính danh L2 của sccd trở thành bùng nổ",
     "sccd L2 legitimacy death spiral becomes explosive")
_add("cross.c1",
     "ngưỡng thâu tóm C₁,crit của sccd — Γ bật",
     "sccd capture threshold C1,crit - Gamma turns on")
_add("cross.psi",
     "Ψ_crit của sccd — điều kiện mạch lạc của R_B bật",
     "sccd Psi_crit - R_B coherence condition trips")
_add("cross.delta_norm",
     "vào băng Khủng hoảng của sccd — điều kiện mức của R_B bật",
     "sccd Crisis regime entry - R_B level condition trips")
_add("cross.dir.below", "xuống dưới", "below")
_add("cross.dir.above", "lên trên", "above")
_add("cross.how.already", "đã vượt từ t₀", "already past at t0")
_add("cross.how.during", "vượt trong kỳ chạy", "crossed during run")

_add("tg.BOTH_GATES_CLOSED", "CẢ HAI CỔNG ĐÃ ĐÓNG", "BOTH GATES CLOSED")
_add("tg.S5_GATE_CLOSED",
     "CỔNG S₅ ĐÃ ĐÓNG (điểm cuối tự nguyện/già hóa)",
     "S5 GATE CLOSED (voluntary/aging terminus)")
_add("tg.S2_GATE_CLOSED",
     "CỔNG S₂ ĐÃ ĐÓNG (điểm cuối bạo lực/thanh niên)",
     "S2 GATE CLOSED (violent/youth terminus)")
_add("tg.S5_GATE_NEAR",
     "CỔNG S₅ SẮP ĐÓNG (~{y} năm theo drift hiện tại)",
     "S5 GATE NEAR (~{y} yr at current drift)")
_add("tg.S2_GATE_NEAR",
     "CỔNG S₂ SẮP ĐÓNG (~{y} năm theo drift hiện tại)",
     "S2 GATE NEAR (~{y} yr at current drift)")
_add("tg.S5_GATE_CLOSING",
     "CỔNG S₅ ĐANG HẸP LẠI (~{y} năm theo drift hiện tại)",
     "S5 GATE CLOSING (~{y} yr at current drift)")
_add("tg.S2_GATE_CLOSING",
     "CỔNG S₂ ĐANG HẸP LẠI (~{y} năm theo drift hiện tại)",
     "S2 GATE CLOSING (~{y} yr at current drift)")
_add("tg.OPEN_NEAREST", "MỞ (cổng gần nhất ~{y} năm)",
     "OPEN (nearest gate ~{y} yr)")
_add("tg.OPEN", "MỞ", "OPEN")

_add("theta25.gate_note",
     "Hai kênh điều chỉnh của Degrow kết thúc ở CÙNG một đối tượng — θ₂₅ — "
     "qua hai cửa khác nhau: đường tự nguyện/già hóa đóng cửa S₅ (crit 0.15, "
     "PAPER), đường bạo lực/thanh niên đóng cửa S₂ (crit 0.25, PAPER). Đóng "
     "cửa nào thì Ψ = λ·θ₂₅·(1−C₅) cũng → 0, làm bật điều kiện thứ ba của "
     "R_B.",
     "Degrow's two adjustment channels terminate in the same object - "
     "theta25 - through different gates: voluntary/aging closes S5 (crit "
     "0.15, PAPER), violent/youth closes S2 (crit 0.25, PAPER). Both drive "
     "Psi -> 0 via Psi = lambda*theta25*(1-C5), tripping R_B's third "
     "condition.")

# ===========================================================================
#  5. HEADLINE PARTS
# ===========================================================================
_add("hl.band_tier", "{regime} / {tier}", "{regime} / {tier}")
_add("hl.mode", "chế độ điều chỉnh {mode}", "adjustment mode {mode}")
_add("hl.gate", "θ₂₅ {gate}", "theta25 {gate}")
_add("hl.loops", "vòng đang chạy {loops}", "loops active {loops}")
_add("hl.rb", "R_B=1 ĐIỀU KIỆN PHÂN NHÁNH ĐÃ HỘI ĐỦ",
     "R_B=1 BIFURCATION CONDITION MET")
_add("hl.decoupled", "G/S₃ đã tách rời", "G/S3 decoupled")

# ===========================================================================
#  6. FORCING / DYNAMICS NOTES
# ===========================================================================
_add("note.router_discount",
     "router_mode=discount: tổng áp lực điều chỉnh bị co lại bởi điều chỉnh "
     "tự nguyện, chứ không chỉ bị chuyển hướng (cách đọc thay thế theo "
     "spec2 OP2-1).",
     "router_mode=discount: total adjustment pressure is shrunk by voluntary "
     "adjustment, not merely redirected (spec2 OP2-1 alternative reading).")
_add("note.haven_single",
     "haven_single_channel=True: drift S₁ trực tiếp đã tắt; dòng vốn trú ẩn "
     "chỉ tác động qua C₄, nghĩa là chỉ tác động lên TỶ LỆ thu-trích "
     "(spec2 OP2-3).",
     "haven_single_channel=True: the direct S1 base drift is off; haven "
     "flight acts only through C4, i.e. only on the extraction RATE "
     "(spec2 OP2-3).")
_add("note.decoupling",
     "TÁCH RỜI G/S₃ ĐANG HOẠT ĐỘNG: năng lực sinh thặng dư đang được nâng "
     "(×{g}) trong khi tính chính danh trôi xuống ({drift}/năm). Không một cú "
     "hích nào trong sccd Parts I–V hành xử như vậy — ca 1941–45 ở Part V "
     "nâng cả hai cùng lúc. Hệ quả: Δ_norm và Ψ có thể đi NGƯỢC chiều, điều "
     "mà năm băng Δ của Part II Table 2 tự thân không diễn đạt nổi; hãy đọc "
     "tầng mạch lạc song song với băng.",
     "G/S3 DECOUPLING ACTIVE: output generation is being raised (x{g}) while "
     "legitimacy drifts down ({drift}/yr). No windfall in sccd Parts I-V "
     "behaves this way - Part V's 1941-45 case raises both together. Expect "
     "Delta_norm and Psi to move in OPPOSITE directions, which the five "
     "Delta bands of Part II Table 2 cannot express on their own; read the "
     "coherence tier alongside the band.")
_add("note.clamped",
     "BỊ CHẶN ở biên [0,1]: {names}. Lớp forcing đòi một dịch chuyển vượt quá "
     "đầu thang chuẩn hóa, nên mức bị chặn là một tạo tác của trần/sàn, "
     "không phải một phép đo. Hãy coi mọi kết quả phụ thuộc vào nó là thứ tự "
     "mà thôi.",
     "CLAMPED at the [0,1] boundary: {names}. The forcing layer asked for a "
     "shift past the end of the normalisation scale, so the clamped level is "
     "a ceiling artefact, not a measurement. Treat any result depending on it "
     "as ordinal only.")
_add("note.traj_structural",
     "Quỹ đạo là một KỊCH BẢN CẤU TRÚC. Mọi hệ số trong sáu phương trình "
     "trạng thái mới đều là ANALYST (spec2) và phần lớn hệ số trong bốn "
     "phương trình gốc là FREE (sccd.spec). Hãy đọc THỨ TỰ các đường cong, "
     "DẤU của độ dốc, và các điểm vượt ngưỡng PAPER. Không đọc mức, không "
     "đọc ngày.",
     "Trajectory is a STRUCTURAL SCENARIO. Every coefficient in the six new "
     "state equations is ANALYST (spec2) and most in the original four are "
     "FREE (sccd.spec). Read curve ORDERING, slope SIGNS, and PAPER-"
     "threshold crossings. Do not read levels or dates.")
_add("note.solver_fallback",
     "Chưa cài scipy, nên việc tích phân chạy trên bộ giải tường minh DP45 "
     "dự phòng của engine thay vì bộ giải stiff mà sccd Part IV §8.1 đòi. Độ "
     "chính xác khoảng 1e-6 trên hệ này ở thang hệ số hiện tại; hãy cài scipy "
     "trước khi nâng bất kỳ tốc độ nào lên một bậc độ lớn hoặc thêm cú sốc "
     "dạng xung dưới một năm.",
     "scipy is not installed, so integration ran on the engine's explicit "
     "DP45 fallback instead of the stiff solver sccd Part IV 8.1 asks for. "
     "Accuracy is ~1e-6 on this system at these coefficient magnitudes; "
     "install scipy before raising any rate by an order of magnitude or "
     "adding sub-year shock pulses.")
_add("note.solver_switched",
     "Bộ giải stiff đầu tiên ({frm}) đã vượt ngân sách {n} lần gọi vế phải "
     "mà chưa chạy hết khoảng tích phân, nên engine chuyển sang {to}. Cả ba "
     "phương pháp trong thang đều nằm trong danh sách sccd Part IV §8.1 yêu "
     "cầu (LSODA, Radau, BDF), nên đây là đổi phương pháp chứ không phải hạ "
     "cấp. Hiện tượng dừng này gắn với chỗ hệ số ngưỡng của θ₂₅ lật, và nới "
     "dung sai KHÔNG khử được nó — chỉ dời nó sang trường hợp khác.",
     "The first stiff method ({frm}) exceeded its budget of {n} right-hand-"
     "side evaluations without reaching the end of the integration interval, "
     "so the engine switched to {to}. All three rungs of the ladder are on "
     "the list sccd Part IV 8.1 requires (LSODA, Radau, BDF), so this is a "
     "method change and not a downgrade. The stall sits where theta25's "
     "threshold factor turns over, and loosening the tolerance does NOT "
     "remove it - it only moves which case hits it.")
_add("note.long_horizon",
     "Chân trời là {years} năm, nhưng Context2 giữ các đầu vào của Block D và "
     "Block A KHÔNG ĐỔI suốt kỳ. Mức thâm nhập AI và bẫy kỳ vọng tự thân là "
     "những thứ biến động nhanh trên khoảng đó, nên vượt quá chừng 20 năm thì "
     "đây là một bài tập tĩnh-so-sánh, không phải một phép ngoại suy.",
     "Horizon is {years} years, but Context2 holds the Block D and Block A "
     "inputs CONSTANT throughout. AI penetration and the expectation trap "
     "are themselves fast-moving over that span, so beyond roughly 20 years "
     "this is a comparative-statics exercise rather than a projection.")
_add("note.faithful_v1",
     "faithful_v1=True: patch và c1_dynamic của sccd đều TẮT. Theo spec "
     "INC-7 và INC-8, eq (NL) của paper như đã viết chỉ có số hạng dương "
     "trong dC₅/dt và chỉ có số hạng âm trong dS₃/dt, nên C₅ tăng đơn điệu "
     "về 1 và Ψ sụp trên MỌI quỹ đạo bất kể kịch bản; và theo INC-9, "
     "[S₃,C₅] là một hệ con tự trị không có vòng phản hồi khép kín nào. Chế "
     "độ này dùng để chứng minh điều đó; nó không tạo ra một quỹ đạo dùng "
     "được.",
     "faithful_v1=True: sccd's patch and c1_dynamic are OFF. Per spec INC-7 "
     "and INC-8 the paper's eq (NL) as written has only positive terms in "
     "dC5/dt and only negative terms in dS3/dt, so C5 rises monotonically to "
     "1 and Psi collapses on EVERY path regardless of scenario, and per "
     "INC-9 [S3,C5] is an autonomous subsystem with no closed feedback loop. "
     "This setting demonstrates that; it does not produce a usable "
     "trajectory.")

# ===========================================================================
#  7. WARNINGS
# ===========================================================================
_add("warn.calib_tags",
     "NHÃN HIỆU CHUẨN. CALIBRATED (chỉ dùng tham số PAPER): λ, θ₂₅, S, băng "
     "chế độ, Ψ, kích hoạt L1/L2, R_B, Γ. UNCALIBRATED (phụ thuộc ít nhất "
     "một tham số FREE/ANALYST): C và do đó cả Δ và Δ_norm; kích hoạt L3/L4; "
     "TOÀN BỘ L5–L8; CAI; mọi quỹ đạo; mọi phép chiếu cổng; việc chọn "
     "attractor.",
     "CALIBRATION TAGS. CALIBRATED (PAPER parameters only): lambda, theta25, "
     "S, the regime band, Psi, L1/L2 activation, R_B, Gamma. UNCALIBRATED "
     "(at least one FREE/ANALYST parameter): C and therefore Delta and "
     "Delta_norm; L3/L4 activation; ALL of L5-L8; CAI; every trajectory; "
     "every gate projection; the attractor choice.")
_add("warn.oat_flips",
     "{n} tham số làm ĐẢO phán quyết định tính dưới nhiễu OAT ±20% mà sccd "
     "eq (SA) bắt buộc: {names}{more}. Một phán quyết dịch chuyển khi đẩy nhẹ "
     "20% một hệ số ANALYST là một GIẢ THUYẾT, không phải một phát hiện. Hãy "
     "đọc `fragility` trước khi trích dẫn bất cứ điều gì.",
     "{n} parameter(s) flip the qualitative verdict under the +/-20% OAT "
     "perturbation sccd eq (SA) mandates: {names}{more}. A verdict that moves "
     "under a 20% nudge to an ANALYST coefficient is a hypothesis, not a "
     "finding. Read `fragility` before quoting anything.")
_add("warn.oat_none",
     "Không nhiễu OAT ±20% nào làm đảo phán quyết. Đó là độ bền trước sai số "
     "THAM SỐ mà thôi — nó không nói gì về việc cấu trúc mô hình hay mức đầu "
     "vào có đúng hay không.",
     "No OAT +/-20% perturbation flipped the verdict. That is robustness "
     "against PARAMETER error only - it says nothing about whether the model "
     "structure or the input levels are right.")
_add("warn.s3_low",
     "S₃ là proxy rủi ro cao nhất trong sccd Part III §2.3 và ở đây nó đang "
     "thấp. Mọi thứ λ chạm tới — tức toàn bộ S — thừa hưởng độ bất định đó. "
     "Hãy nới các khoảng tương ứng.",
     "S3 is the highest-risk proxy in sccd Part III 2.3 and it is low here. "
     "Everything lambda touches - which is all of S - inherits that "
     "uncertainty. Widen accordingly.")
_add("warn.psi_high_delta_crisis",
     "Ψ trên ngưỡng trong khi Δ_norm đã ở Khủng hoảng: điều kiện mạch lạc "
     "của R_B KHÔNG hội đủ, nên sccd eq (23) giữ lại cờ phân nhánh dù điều "
     "kiện mức và điều kiện động lượng có thể đã hội đủ. Đây là hành vi mà "
     "paper chủ ý, không phải lỗi.",
     "Psi above crit while Delta_norm is in Crisis: the coherence condition "
     "of R_B is NOT met, so sccd eq (23) withholds the bifurcation flag even "
     "though the level and momentum conditions may hold. This is the paper's "
     "intended behaviour, not a bug.")
_add("warn.overlap_L8_L2",
     "L8 và L2 đang chạy cùng lúc. Theo spec2 OP2-6: khi thanh niên dư thừa "
     "đã đẩy S₃ xuống dưới 0.30 thì hai bài kiểm này cùng bật trên thứ mà có "
     "thể lập luận là một cơ chế duy nhất, nên cai_ext đếm nó hai lần. Phép "
     "đếm KHÔNG được hiệu chỉnh — ở đây hãy đọc cai_ext như một chặn trên.",
     "L8 and L2 are both active. spec2 OP2-6: once surplus youth has already "
     "driven S3 below 0.30 these two tests fire on what is arguably one "
     "mechanism, so cai_ext counts it twice. The count is NOT corrected - "
     "read cai_ext as an upper bound here.")
_add("warn.overlap_L6_L4",
     "L6 và L4 đang chạy cùng lúc và cả hai đều đi qua đường thoát. L4 là "
     "thoát theo quyền phán xử (C₄ của sccd), L6 là thoát theo hình thái tài "
     "sản (tỷ phần trú ẩn). Đó thực sự là hai kênh khác nhau với động lực "
     "đảo chiều khác nhau, nhưng chúng dùng chung đại lượng C₄, nên một phần "
     "lực đẩy là chung — xem spec2 OP2-4.",
     "L6 and L4 are both active and both run through exit. L4 is "
     "jurisdiction exit (sccd C4), L6 is asset-form exit (haven share). "
     "Genuinely different channels with different reversal dynamics, but they "
     "share the C4 scalar, so some of the drive is common - see spec2 OP2-4.")

# world warnings
_add("warn.psiG_uncal",
     "Ψ_G vốn đã là UNCALIBRATED trong chính sccd v1.00 — Part IV §6.1 nêu "
     "các tính chất mà nó phải có nhưng không nêu dạng đóng, nên engine dùng "
     "một trung bình hình học có trọng số nhân với (1 − Sync_Risk), thỏa cả "
     "hai tính chất đó. Mọi thứ lớp v2 thêm lên trên đều là ANALYST.",
     "Psi_G is UNCALIBRATED in sccd v1.00 itself - Part IV 6.1 states its "
     "required properties but not its closed form, so the engine uses a "
     "weighted geometric mean times (1 - Sync_Risk), which satisfies them. "
     "Everything the v2 layer adds on top is ANALYST.")
_add("warn.rbg_structural",
     "R_B,G xác định một ĐIỀU KIỆN CẤU TRÚC — nguyên văn sccd Part IV §6.3 "
     "gọi đó là 'overloaded-fault analogy' — và KHÔNG phải một dự báo về bất "
     "kỳ sự kiện hay thời điểm nào.",
     "R_B,G identifies a STRUCTURAL CONDITION, in sccd Part IV 6.3's own "
     "words an 'overloaded-fault analogy', and is NOT a prediction of any "
     "event or date.")
_add("warn.few_polities",
     "Chỉ có {n} chủ thể được cấp. Ψ_G, Sync_Risk và các độ phân tán đều là "
     "đại lượng gộp mặt cắt ngang — chúng gần như vô nghĩa khi dưới khoảng "
     "năm chủ thể có trọng số hệ thống.",
     "Only {n} polity/polities supplied. Psi_G, Sync_Risk and the dispersion "
     "measures are all cross-sectional aggregates - they are close to "
     "meaningless below about five systemically weighted polities.")
_add("warn.sync_capped",
     "Sync_Risk đã chạm trần 0.95, nên Ψ_G đang bị điều khiển bởi cái trần "
     "đó chứ không phải bởi các đầu vào.",
     "Sync_Risk hit its 0.95 cap, so Psi_G is being driven by the cap rather "
     "than by the inputs.")
_add("warn.low_confidence",
     "Đầu vào của {codes} được đánh dấu là tiên nghiệm phân tích độ tin cậy "
     "thấp, không phải phép đo. sccd Part III §5.3 từ chối trả Δ đã hiệu "
     "chuẩn khi hơn 30% một chuỗi là số gán; giá trị điểm nhập tay còn yếu "
     "hơn số gán, vì không có chuỗi nào để kiểm định.",
     "Inputs for {codes} are flagged low-confidence analyst priors, not "
     "measurements. sccd Part III 5.3 refuses a calibrated Delta when more "
     "than 30% of a series is imputed; hand-entered point values are weaker "
     "than imputation, since there is no series to gate.")

# events
_add("warn.ev_clamped",
     "Chồng sự kiện bị chặn ở biên [0,1]: {names}. Các dịch chuyển bạn yêu "
     "cầu cộng lại đã vượt quá đầu thang chuẩn hóa, nên các mức bị chặn là "
     "tạo tác của trần. Hoặc bạn đã chồng quá nhiều sự kiện, hoặc một số "
     "trong đó đang đếm hai lần phần baseline của bạn.",
     "Event stack clamped at the [0,1] boundary: {names}. The requested "
     "shifts sum past the end of the normalisation scale, so the clamped "
     "levels are ceiling artefacts. Either you have stacked too many events "
     "or some of them are double counting your baseline.")
_add("warn.ev_unknown",
     "Đã bỏ qua các mã hoặc đích sự kiện không nhận ra: {names}",
     "Ignored unknown event ids or targets: {names}")
_add("warn.ev_deep_stack",
     "{n} sự kiện được áp đồng thời. Mọi độ lớn đều là ANALYST, nên một chồng "
     "sâu như vậy nhân các con số tự đặt lên nhau. Hãy ưu tiên vài sự kiện "
     "quyết định thay vì nhiều sự kiện nhỏ, và kiểm `fragility` trong kết "
     "quả.",
     "{n} events applied simultaneously. Every magnitude is ANALYST, so a "
     "stack this deep compounds invented numbers multiplicatively. Prefer a "
     "few decisive events over many small ones, and check `fragility` in the "
     "result.")

# ===========================================================================
#  8. MISC ENGINE PROSE
# ===========================================================================
_add("ddt.caller", "do người gọi cung cấp", "caller-supplied")
_add("ddt.measured",
     "đo trên 3 năm đầu của quỹ đạo",
     "measured over first 3 yr of trajectory")
_add("rb.detail",
     "Δ_norm={dn} so với {dcrit} [{c1}]; dΔ/dt={ddt} so với {dc} [{c2}]; "
     "Ψ={psi} so với {pcrit} [{c3}]",
     "Delta_norm={dn} vs {dcrit} [{c1}]; dDelta/dt={ddt} vs {dc} [{c2}]; "
     "Psi={psi} vs {pcrit} [{c3}]")
_add("att.A1", "A₁ tái lập, S trội", "A1 S-dominant reconstitution")
_add("att.A2", "A₂ thâu tóm, C trội", "A2 C-dominant capture")
_add("att.A3", "A₃ sụp đổ do phân mảnh", "A3 fragmentation collapse")
_add("att.note",
     "chỉ là điểm tương đối; Part IV nói việc chọn attractor cần toàn bộ đa "
     "tạp phi tuyến — UNCALIBRATED",
     "relative scores only; Part IV says attractor selection requires the "
     "full non-linear manifold - UNCALIBRATED")
_add("tt.gap_source",
     "hiệu của hai dΔ/dt đã đo; sustained_years được GIẢ ĐỊNH là 10 và KHÔNG "
     "được đo — engine chỉ có một năm đầu vào, không có chuỗi, nên điều kiện "
     "T_min của sccd không thể được kiểm định thực sự",
     "difference of the two measured dDelta/dt; sustained_years is assumed "
     "10 and NOT measured - the engine has one year of input, not a series, "
     "so sccd's T_min condition cannot be genuinely tested")
_add("tt.needs_two", "cần ít nhất hai chủ thể",
     "needs at least two polities")
_add("rbg.interp",
     "R_B,G=1 xác định một ĐIỀU KIỆN CẤU TRÚC (ví tương tự đường đứt gãy đã "
     "quá tải), KHÔNG phải một dự báo về một sự kiện hay một thời điểm cụ "
     "thể (sccd Part IV §6.3).",
     "R_B,G=1 identifies a structural condition (overloaded-fault analogy), "
     "NOT a prediction of a specific event or timeline (sccd Part IV 6.3).")
_add("epistemic.limit",
     "sccd Part V §1, nguyên văn: 'We do not, at this stage, claim "
     "predictive precision — generating quantitatively accurate forecasts "
     "from an incompletely calibrated formal model would be epistemically "
     "irresponsible. The validation standard is qualitative-structural.' Lớp "
     "v2 còn yếu hơn thế nữa, vì toàn bộ 46 tham số của nó đều là ANALYST.",
     "sccd Part V 1, verbatim: 'We do not, at this stage, claim predictive "
     "precision - generating quantitatively accurate forecasts from an "
     "incompletely calibrated formal model would be epistemically "
     "irresponsible. The validation standard is qualitative-structural.' The "
     "v2 layer is strictly weaker than that again, since all 46 of its "
     "parameters are ANALYST.")
_add("patch.rationale",
     "spec2 OP2-7: INC-7/8/9 ở mức CRITICAL, và hai block mới cấp cơ chế có "
     "nguồn cho đúng những số hạng mà INC-7 và INC-8 nói là thiếu. Truyền "
     "faithful_v1=True vào lớp dynamics để tái lập paper nguyên văn thay thế.",
     "spec2 OP2-7: INC-7/8/9 are CRITICAL, and the two new blocks supply "
     "sourced mechanisms for the terms INC-7 and INC-8 say are missing. Pass "
     "faithful_v1=True to the dynamics layer to reproduce the paper verbatim "
     "instead.")
_add("audit.headline",
     "{paper} trong {total} tham số v1 mang một giá trị được nêu trong paper "
     "gốc; {free} tham số thì không. TOÀN BỘ {v2} tham số v2 đều là ANALYST "
     "hoặc DERIVED2 — hai bài báo mới là định tính và không nêu hệ số nào. "
     "Hãy đọc mọi kết quả phụ thuộc v2 theo nghĩa THỨ TỰ: một bảng xếp hạng "
     "và một bản đồ điểm vượt ngưỡng, không phải một mức.",
     "{paper} of {total} v1 parameters carry a value from the source paper; "
     "{free} do not. ALL {v2} v2 parameters are ANALYST or DERIVED2 - the two "
     "new papers are qualitative and state no coefficients. Read every "
     "v2-dependent output as ORDINAL: a ranking and a threshold-crossing "
     "map, not a level.")
_add("level_drift.note",
     "Dịch chuyển MỨC chỉ áp cho {level} — là những thành phần mà proxy của "
     "sccd VỀ CẤU TRÚC không nhìn thấy các kênh mới. DRIFT áp cho {drift}. "
     "Cho một thành phần nhóm S một dịch chuyển mức là đếm hai lần thứ mà "
     "proxy dòng-hằng-năm của nó đã bao hàm.",
     "LEVEL shifts apply only to {level} - the components whose sccd proxies "
     "STRUCTURALLY miss the new channels. DRIFTS apply to {drift}. Giving an "
     "S-side component a level shift double counts what its annual-flow "
     "proxy already embeds.")
_add("events.provenance",
     "Mọi độ lớn hiệu ứng đều là ANALYST. Dấu và đích được lập luận từ các "
     "định nghĩa thành phần trong sccd Part III và từ hai bài báo mới; còn "
     "độ lớn là tự đặt. Hãy đổi chúng tự do — catalogue tồn tại chính là để "
     "làm việc đó.",
     "Every effect magnitude is ANALYST. Signs and targets are argued from "
     "the component definitions in sccd Part III and from the two new "
     "papers; sizes are invented. Change them freely - that is what the "
     "catalogue is for.")
_add("events.usage",
     "Một sự kiện là một DỊCH CHUYỂN MỨC CỘNG THÊM lên baseline của bạn. "
     "Đừng bật một sự kiện mà các con số baseline của bạn ĐÃ bao hàm — "
     "engine không phát hiện được việc đếm hai lần đó.",
     "An event is a LEVEL SHIFT ADDED ON TOP of your baseline components. Do "
     "not switch on an event whose effect your baseline numbers already "
     "contain - the engine cannot detect that double count.")
_add("presets.disclaimer",
     "TIÊN NGHIỆM PHÂN TÍCH, không phải phép đo. Chỉ bốn giá trị trong toàn "
     "bộ tập này là do paper nêu: Mỹ s₃=0.38, c₅=0.74, c₁=0.82, s₂≈0.90. "
     "Không có gì ở đây được tạo ra bằng cách chạy đường ống proxy Part III "
     "của sccd, và không giá trị nào có khoảng tin cậy. Hãy thay các dòng này "
     "bằng đầu vào đã đo trước khi trích dẫn bất kỳ kết quả nào.",
     "ANALYST PRIORS, not measurements. Only four values in the whole file "
     "are paper-stated: US s3=0.38, c5=0.74, c1=0.82, s2~0.90. Nothing here "
     "was produced by running sccd's Part III proxy pipeline, and no value "
     "has a confidence interval. Replace rows with measured inputs before "
     "quoting any result.")

# confidence + provenance enums
_add("conf.low", "thấp", "low")
_add("conf.medium", "trung bình", "medium")
_add("conf.unknown", "không rõ", "unknown")
_add("prov.analyst", "tiên nghiệm ANALYST", "ANALYST prior")
_add("prov.caller", "do người gọi cấp", "caller-supplied")
_add("prov.mixed_us",
     "HỖN HỢP: s₃/c₅/c₁/s₂ là PAPER (sccd Part IV–V); còn lại là ANALYST",
     "MIXED: s3/c5/c1/s2 are PAPER (sccd Part IV-V); all else ANALYST")

# severity
_add("sev.CRITICAL", "NGHIÊM TRỌNG", "CRITICAL")
_add("sev.HIGH", "CAO", "HIGH")
_add("sev.medium", "trung bình", "medium")
_add("sev.low", "thấp", "low")


# ===========================================================================
#  9. LOOKUP HELPERS used by the localisers
# ===========================================================================
def regime(name: str, lang: str) -> str:
    return t(f"regime.{name}", lang, strict=False)


def stability(name: str, lang: str) -> str:
    return t(f"stab.{name}", lang, strict=False)


def tier(name: str, lang: str) -> str:
    return t(f"tier.{name}", lang, strict=False)


def mode(name: str, lang: str) -> str:
    return t(f"mode.{name}", lang, strict=False)


def severity(name: str, lang: str) -> str:
    return t(f"sev.{name}", lang, strict=False)

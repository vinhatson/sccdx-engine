# -*- coding: utf-8 -*-
"""
SCCD-X — Event Input Layer
===========================
The catalogue of named events a caller can switch on, each with an intensity,
a weight, and a declared effect on the engine's inputs. This is the layer the
API form writes into.

WHAT AN EVENT IS, AND WHAT IT IS NOT
------------------------------------
An event is a LEVEL SHIFT the caller is ADDING ON TOP of the baseline
component estimates. It is for something that has not happened yet, or has
happened but is not yet reflected in the numbers you entered.

It is NOT for re-describing something your baseline already contains. If you
set s3 = 0.38 because polling already shows a legitimacy slump, and then also
switch on `contested_election` at full intensity, you have charged the same
slump twice. The engine cannot detect this - it has no way to know what your
0.38 was built from - so the discipline is yours. `EventApplication.audit`
prints every shift so you can at least see the total you applied.

This is the opposite situation from the forcing blocks in forcing.py, where
the level-vs-drift rule FORBIDS level shifts on S components. There the block
systematically re-derives a quantity the proxy already measures, so a level
shift is always double counting. Here the caller asserts the shift is new
information. Different claim, different treatment.

PROVENANCE
----------
Every magnitude in this catalogue is ANALYST. Neither sccd nor either new
paper tabulates event-to-component elasticities. What the catalogue is good
for is making the mapping EXPLICIT and REVIEWABLE - you can disagree with a
number and change it - rather than leaving it implicit in an analyst's head.
The sign and the target of each effect are argued from the component
definitions in sccd Part III; only the size is invented.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

from sccd.aggregate import SubComponents
from .forcing import DemoBlock, DispBlock

# Targets an event may touch.
CORE_TARGETS = ("s1", "s2", "s3", "s4", "s5", "c1", "c2", "c3", "c4", "c5")
DEMO_TARGETS = ("d1", "d2", "d3", "d4", "d5")
DISP_TARGETS = ("a1", "a2", "a3", "a4", "a5", "a6",
                "luxury_contraction", "physical_share")
EXTRA_TARGETS = ("revenue_polarisation", "security_pressure",
                 "base_revenue_demand", "g_shock")
ALL_TARGETS = CORE_TARGETS + DEMO_TARGETS + DISP_TARGETS + EXTRA_TARGETS


@dataclass(frozen=True)
class EventDef:
    id: str
    group: str
    label_en: str
    label_vi: str
    effects: Dict[str, float]      # target -> delta at intensity 1, weight 1
    default_weight: float = 1.0
    note: str = ""
    note_vi: str = ""

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class EventInput:
    """What the caller submits per event."""
    id: str
    intensity: float = 1.0         # 0..1, how severe
    weight: float = 1.0            # multiplier on the catalogue effect
    enabled: bool = True

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class EventApplication:
    sub: SubComponents
    demo: DemoBlock
    disp: DispBlock
    extra: Dict[str, float]
    audit: List[dict] = field(default_factory=list)
    clamped: List[str] = field(default_factory=list)
    unknown: List[str] = field(default_factory=list)
    note_codes: List[tuple] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"sub": self.sub.as_dict(), "demo": self.demo.as_dict(),
                "disp": self.disp.as_dict(), "extra": self.extra,
                "audit": self.audit, "clamped": self.clamped,
                "unknown": self.unknown,
                "note_codes": [list(c) for c in self.note_codes]}


def _E(**kw) -> EventDef:
    return EventDef(**kw)


# ===========================================================================
#  CATALOGUE
# ===========================================================================
CATALOGUE: List[EventDef] = [

    # ---------------- FISCAL / ECONOMIC ----------------
    _E(id="sovereign_debt_stress", group="fiscal",
       label_en="Sovereign debt stress / spread blowout",
       label_vi="Căng thẳng nợ công / spread bật mạnh",
       effects={"s1": -0.10, "s5": -0.14, "base_revenue_demand": 0.02},
       note="Hits S5 hardest: debt service is revenue pre-commitment, which "
            "is precisely what sccd's Temporal Leverage measures.",
       note_vi="Đánh mạnh nhất vào S5: trả nợ là khoản ngân sách bị cam kết "
               "trước, đúng cái mà Temporal Leverage của sccd đo."),
    _E(id="inflation_surge", group="fiscal",
       label_en="Inflation surge (sustained, >2x target)",
       label_vi="Lạm phát bùng (kéo dài, >2 lần mục tiêu)",
       effects={"s1": 0.04, "s3": -0.09, "a4": 0.12, "d2": 0.08},
       note="S1 rises short-run - inflation is a tax - while S3 falls and "
            "haven demand rises. The S1 gain is the reason inflation is "
            "chosen and the S3 loss is why it does not help for long."),
    _E(id="currency_crisis", group="fiscal",
       label_en="Currency crisis / reserve drain",
       label_vi="Khủng hoảng tỷ giá / cạn dự trữ",
       effects={"s1": -0.12, "s5": -0.12, "c4": 0.08, "a4": 0.16}),
    _E(id="energy_shock", group="fiscal",
       label_en="Energy / commodity price shock",
       label_vi="Sốc giá năng lượng / hàng hóa",
       effects={"s1": -0.07, "d1": 0.09, "s3": -0.05}),
    _E(id="tariff_war", group="fiscal",
       label_en="Tariff war / trade bloc fracture",
       label_vi="Chiến tranh thuế quan / khối thương mại rạn",
       effects={"s1": -0.05, "c4": -0.06, "c5": 0.05, "d1": 0.06},
       note="C4 FALLS: trade and capital-account closure removes exit "
            "options. One of the few events that cuts exit rather than "
            "raising it."),
    _E(id="sanctions_imposed", group="fiscal",
       label_en="Comprehensive sanctions imposed on this polity",
       label_vi="Bị áp trừng phạt toàn diện",
       effects={"s1": -0.14, "c4": -0.16, "c1": -0.08, "s3": 0.06, "a4": 0.14},
       note="S3 RISES: external pressure routinely consolidates domestic "
            "legitimacy in the short run (rally-round-the-flag). sccd has no "
            "term for this, so it enters as an event."),
    _E(id="tech_productivity_boom", group="fiscal",
       label_en="Broad productivity boom (non-AI)",
       label_vi="Bùng nổ năng suất diện rộng (không do AI)",
       effects={"s1": 0.08, "g_shock": 0.10, "d1": -0.07, "s3": 0.05}),

    # ---------------- SECURITY ----------------
    _E(id="interstate_war_onset", group="security",
       label_en="Interstate war onset (this polity a belligerent)",
       label_vi="Chiến tranh giữa các quốc gia bùng nổ (nước này tham chiến)",
       effects={"s2": 0.10, "s3": 0.12, "s5": -0.18, "s1": 0.06,
                "security_pressure": 0.35, "g_shock": 0.08},
       note="The sccd Part V 1941-45 pattern: mobilisation raises coercive "
            "capacity AND legitimacy together while consuming temporal "
            "leverage. Contrast the AI windfall, which raises output and "
            "LOWERS legitimacy - that contrast is the whole point of the "
            "decoupling flag."),
    _E(id="civil_conflict", group="security",
       label_en="Civil conflict / armed insurgency",
       label_vi="Xung đột nội bộ / nổi dậy vũ trang",
       effects={"s2": -0.22, "s3": -0.12, "s4": -0.14, "c5": 0.14,
                "security_pressure": 0.45},
       note="Drives S2 toward theta25's 0.25 PAPER gate - the violent "
            "terminus of Degrow's model."),
    _E(id="coup_or_irregular_transfer", group="security",
       label_en="Coup / irregular transfer of power",
       label_vi="Đảo chính / chuyển giao quyền lực phi chính quy",
       effects={"s3": -0.24, "s2": -0.10, "s4": -0.10, "c2": -0.10,
                "c5": 0.10}),
    _E(id="alliance_rupture", group="security",
       label_en="Alliance rupture / security guarantee withdrawn",
       label_vi="Liên minh đổ vỡ / mất bảo đảm an ninh",
       effects={"s2": -0.10, "s5": -0.10, "security_pressure": 0.30,
                "s3": -0.05}),
    _E(id="military_buildup", group="security",
       label_en="Major military build-up (peacetime)",
       label_vi="Tăng cường quân sự lớn (thời bình)",
       effects={"s2": 0.12, "s5": -0.14, "base_revenue_demand": 0.02,
                "security_pressure": 0.25}),

    # ---------------- LEGITIMACY ----------------
    _E(id="contested_election", group="legitimacy",
       label_en="Contested / disputed national election",
       label_vi="Bầu cử quốc gia bị tranh chấp",
       effects={"s3": -0.14, "c5": 0.12, "revenue_polarisation": 0.15}),
    _E(id="mass_protest", group="legitimacy",
       label_en="Sustained mass protest movement",
       label_vi="Phong trào biểu tình quy mô lớn, kéo dài",
       effects={"s3": -0.11, "c2": 0.14, "s2": -0.07, "c5": 0.06},
       note="C2 RISES - protest is civil organisation. In the patched dC5/dt "
            "that makes it a depolarising force even as it drains S3, so the "
            "net sign on fragmentation is genuinely ambiguous and depends on "
            "nu_counter vs the direct C5 term."),
    _E(id="corruption_scandal", group="legitimacy",
       label_en="Major corruption scandal at centre of power",
       label_vi="Đại án tham nhũng ở trung tâm quyền lực",
       effects={"s3": -0.12, "s4": -0.07, "c1": 0.05}),
    _E(id="constitutional_crisis", group="legitimacy",
       label_en="Constitutional / judicial-independence crisis",
       label_vi="Khủng hoảng hiến pháp / độc lập tư pháp",
       effects={"s3": -0.16, "s4": -0.09, "c5": 0.10, "c1": 0.07}),
    _E(id="succession_crisis", group="legitimacy",
       label_en="Leadership succession crisis",
       label_vi="Khủng hoảng kế vị lãnh đạo",
       effects={"s3": -0.13, "s4": -0.08, "c5": 0.08}),
    _E(id="successful_major_reform", group="legitimacy",
       label_en="Visibly successful major reform delivered",
       label_vi="Cải cách lớn được thực thi thành công rõ rệt",
       effects={"s3": 0.14, "s4": 0.12, "d2": -0.08},
       note="The positive direction matters structurally: with sccd's patch "
            "on, dS3/dt gains +sigma_rec*(s3_target_gain*S4 - S3), so a real "
            "S4 gain pulls the S3 attractor up. This is the only route the "
            "engine has to legitimacy RECONSTITUTION - the thing INC-8 says "
            "the paper's own equations cannot produce."),

    # ---------------- ADMIN ----------------
    _E(id="implementation_failure", group="admin",
       label_en="Flagship policy implementation failure",
       label_vi="Chính sách trọng điểm thất bại khi thực thi",
       effects={"s4": -0.14, "s3": -0.10}),
    _E(id="disaster_response_failure", group="admin",
       label_en="Disaster / pandemic response failure",
       label_vi="Thất bại ứng phó thảm họa / đại dịch",
       effects={"s4": -0.16, "s3": -0.14, "d1": 0.08, "c2": 0.06}),
    _E(id="state_capacity_investment", group="admin",
       label_en="Sustained state capacity investment programme",
       label_vi="Chương trình đầu tư năng lực nhà nước dài hạn",
       effects={"s4": 0.14, "s1": 0.06, "s5": -0.06}),

    # ---------------- CAPITAL ----------------
    _E(id="wealth_concentration_jump", group="capital",
       label_en="Step change in wealth / market concentration",
       label_vi="Tập trung tài sản / thị trường tăng vọt",
       effects={"c1": 0.12, "c5": 0.05, "s3": -0.06},
       note="Pushes C1 toward sccd's C1,crit = 0.70 PAPER threshold, above "
            "which the capture term Gamma turns on and loop L1 can arm."),
    _E(id="regulatory_capture_event", group="capital",
       label_en="Visible regulatory capture / revolving door scandal",
       label_vi="Thâu tóm quy chế lộ rõ / bê bối 'cửa xoay'",
       effects={"c1": 0.10, "s4": -0.08, "s3": -0.09}),
    _E(id="major_redistribution", group="capital",
       label_en="Major redistributive programme enacted",
       label_vi="Ban hành chương trình phân phối lại lớn",
       effects={"c1": -0.10, "s1": -0.06, "s3": 0.08, "d2": -0.10,
                "s5": -0.08}),

    # ---------------- CIVIL ----------------
    _E(id="civil_society_crackdown", group="civil",
       label_en="Crackdown on NGOs / associational life",
       label_vi="Trấn áp tổ chức xã hội dân sự",
       effects={"c2": -0.18, "c3": -0.10, "s2": 0.06, "c5": 0.06,
                "s3": -0.07},
       note="Note the trap this creates in the patched system: cutting C2 "
            "removes the -nu_depol*C5*C2 depolarisation term, so suppressing "
            "civil society raises long-run fragmentation. The state buys "
            "short-run S2 at the cost of permanent C5."),
    _E(id="union_or_community_resurgence", group="civil",
       label_en="Union / community organisation resurgence",
       label_vi="Nghiệp đoàn / tổ chức cộng đồng trỗi dậy",
       effects={"c2": 0.16, "c1": -0.05, "a5": 0.10}),

    # ---------------- INFORMATION ----------------
    _E(id="media_capture", group="info",
       label_en="Media capture / ownership consolidation",
       label_vi="Truyền thông bị thâu tóm / tập trung sở hữu",
       effects={"c3": -0.16, "c1": 0.07, "c5": 0.08}),
    _E(id="internet_shutdown", group="info",
       label_en="Internet shutdown / platform ban",
       label_vi="Ngắt internet / cấm nền tảng",
       effects={"c3": -0.20, "c2": -0.08, "s2": 0.05, "a1": -0.12}),
    _E(id="disinformation_surge", group="info",
       label_en="Large-scale disinformation surge",
       label_vi="Bùng nổ thông tin sai lệch quy mô lớn",
       effects={"c5": 0.13, "s3": -0.08, "c3": -0.08,
                "revenue_polarisation": 0.10}),

    # ---------------- EXIT ----------------
    _E(id="capital_controls", group="exit",
       label_en="Capital controls imposed",
       label_vi="Áp đặt kiểm soát vốn",
       effects={"c4": -0.20, "a4": 0.18, "s3": -0.07, "c1": -0.05},
       note="The sharpest demonstration of spec2 OP2-4. Controls close exit "
            "by JURISDICTION (C4 down) and in the same move push wealth into "
            "exit by ASSET FORM (a4 up), which Block A then feeds back into "
            "effective C4. Whether net exit falls at all depends on "
            "zeta_haven_c4 - and that is an ANALYST number."),
    _E(id="emigration_wave", group="exit",
       label_en="Skilled emigration wave",
       label_vi="Làn sóng di cư lao động có kỹ năng",
       effects={"c4": 0.12, "s1": -0.08, "s4": -0.07, "d5": -0.10,
                "d4": 0.07}),
    _E(id="immigration_surge", group="exit",
       label_en="Large immigration inflow",
       label_vi="Dòng nhập cư lớn",
       effects={"d4": -0.10, "d1": 0.10, "c5": 0.09, "s1": 0.05,
                "d5": 0.08},
       note="The engine's only direct link between the two halves of "
            "Degrow's world: inflow relieves the receiving polity's "
            "dependency inversion while adding load and fragmentation."),

    # ---------------- FRAGMENTATION ----------------
    _E(id="polarising_election", group="fragmentation",
       label_en="Polarising election campaign",
       label_vi="Chiến dịch tranh cử gây phân cực",
       effects={"c5": 0.12, "revenue_polarisation": 0.20, "s3": -0.05}),
    _E(id="secession_movement", group="fragmentation",
       label_en="Active secession / autonomy movement",
       label_vi="Phong trào ly khai / đòi tự trị",
       effects={"c5": 0.16, "s2": -0.12, "s4": -0.10, "s3": -0.09}),
    _E(id="ethnic_mobilisation", group="fragmentation",
       label_en="Ethnic / sectarian mobilisation",
       label_vi="Động viên sắc tộc / tôn giáo",
       effects={"c5": 0.15, "s3": -0.08, "d5": 0.07,
                "security_pressure": 0.20}),

    # ---------------- DEMOGRAPHIC  [DEGROW] ----------------
    _E(id="fertility_collapse", group="demographic",
       label_en="Fertility collapse (TFR well below replacement)",
       label_vi="Sinh suất sụp (TFR thấp xa mức thay thế)",
       effects={"d3": 0.12, "d4": 0.14, "d2": 0.08},
       note="DEGROW's modern path, as an input rather than an output. Raises "
            "the router variable d3 and the inversion d4 together."),
    _E(id="pension_reform_failure", group="demographic",
       label_en="Pension / welfare reform defeated or reversed",
       label_vi="Cải cách lương hưu / phúc lợi thất bại hoặc bị đảo",
       effects={"d4": 0.12, "s5": -0.12, "s3": -0.08,
                "base_revenue_demand": 0.015},
       note="Arms loop L7 directly: the inversion is locked in and the "
            "fiscal space to relieve the expectation trap is gone."),
    _E(id="housing_affordability_crisis", group="demographic",
       label_en="Housing affordability crisis (price/income extreme)",
       label_vi="Khủng hoảng khả năng chi trả nhà ở (giá/thu nhập cực đoan)",
       effects={"d2": 0.18, "s3": -0.08, "c1": 0.08},
       note="DEGROW's central modern mechanism. The paper's own analogy: "
            "'analogous to ancient peasants' inability to access land - both "
            "represent a denial of the opportunity to establish a stable "
            "family foundation.'"),
    _E(id="youth_unemployment_surge", group="demographic",
       label_en="Youth unemployment surge",
       label_vi="Thất nghiệp thanh niên tăng vọt",
       effects={"d5": 0.18, "d1": 0.08, "c5": 0.07, "s3": -0.07},
       note="DEGROW's 'reserve army of chaos'. Arms loop L8 where d3 is low."),
    _E(id="land_or_resource_squeeze", group="demographic",
       label_en="Land / water / food resource squeeze",
       label_vi="Siết nguồn đất / nước / lương thực",
       effects={"d1": 0.18, "s3": -0.07, "security_pressure": 0.15},
       note="The classical Malthusian constraint, still live in much of the "
            "world. DEGROW Stage 1-2."),
    _E(id="relief_system_failure", group="demographic",
       label_en="Relief / safety-net system failure in a crisis",
       label_vi="Hệ thống cứu trợ / an sinh thất bại trong khủng hoảng",
       effects={"s3": -0.18, "s4": -0.12, "d1": 0.08},
       note="DEGROW Stage 2.1 verbatim - 'the breaking of the most sacred "
            "social contract'. The largest single S3 hit in the catalogue, "
            "because the paper treats this as the moment the mandate ends."),
    _E(id="family_formation_support", group="demographic",
       label_en="Serious family-formation support package",
       label_vi="Gói hỗ trợ lập gia đình thực chất",
       effects={"d2": -0.16, "s3": 0.09, "s5": -0.08,
                "base_revenue_demand": 0.012},
       note="DEGROW's own policy prescription: 'make housing, education, and "
            "childcare genuinely affordable... The goal is to make having "
            "children a feasible and desirable choice, not an unbearable "
            "burden.' Note it COSTS S5 - relieving the trap is itself a "
            "revenue pre-commitment, which is why L7 is a trap."),

    # ---------------- DISPLACEMENT  [DISPL] ----------------
    _E(id="ai_mass_adoption", group="displacement",
       label_en="AI crosses mass-adoption threshold in daily decisions",
       label_vi="AI vượt ngưỡng phổ cập trong quyết định thường ngày",
       effects={"a1": 0.20, "a2": 0.12, "a3": 0.12, "a6": 0.14}),
    _E(id="whitecollar_displacement", group="displacement",
       label_en="White-collar / cognitive-labour displacement wave",
       label_vi="Làn sóng thay thế lao động trí thức / văn phòng",
       effects={"a2": 0.20, "a3": 0.14, "c1": 0.10, "s1": -0.08,
                "d2": 0.08, "s3": -0.07},
       note="Hits the exact cohort DISPL 8.5 names: 'the population most "
            "capable of using AI is the population most existentially "
            "threatened by it'. Note S1 falls - that cohort is the income "
            "tax base."),
    _E(id="agency_crisis_visible", group="displacement",
       label_en="Visible public agency / meaning crisis (Tier 2)",
       label_vi="Khủng hoảng ý nghĩa / tự chủ bộc lộ công khai (Tầng 2)",
       effects={"a3": 0.20, "c5": 0.08, "s3": -0.10, "a5": 0.08},
       note="DISPL 4.4.3. The engine's load-bearing and least-evidenced "
            "link - see spec2 OP2-2 before leaning on this one."),
    _E(id="haven_flight_surge", group="displacement",
       label_en="Safe-haven flight surge (gold / silver / tangibles)",
       label_vi="Bùng nổ dòng vốn trú ẩn (vàng / bạc / tài sản hữu hình)",
       effects={"a4": 0.22, "physical_share": 0.10, "c4": 0.06,
                "s1": -0.06},
       note="DISPL 5-6. The paper's documented 2023-2026 move: gold ~$2,000 "
            "to >$5,500/oz, silver ~+150%, platinum ~+110%."),
    _E(id="luxury_contraction", group="displacement",
       label_en="Luxury / identity-goods demand contraction",
       label_vi="Cầu hàng xa xỉ / hàng hiệu định danh co lại",
       effects={"luxury_contraction": 0.25, "s1": -0.05},
       note="DISPL 2.3, 6.2: 50-60 million consumers lost 2022-2025, "
            "attrition concentrated in the aspirational tier that was 60-70% "
            "of the base."),
    _E(id="counter_tech_movement", group="displacement",
       label_en="Counter-technological movement goes mainstream",
       label_vi="Phong trào phản-công-nghệ thành xu hướng chính",
       effects={"a5": 0.22, "c2": 0.12, "a1": -0.08, "a6": -0.06},
       note="DISPL 8.5 'New Luddism'. The engine's main depolarising force: "
            "it raises C2, which drives the -nu_depol*C5*C2 term that sccd "
            "INC-7 says the paper's own dC5/dt is missing."),
    _E(id="ai_windfall_captured", group="displacement",
       label_en="AI productivity windfall captured by narrow ownership",
       label_vi="Thặng dư năng suất AI bị sở hữu hẹp thâu tóm",
       effects={"a6": 0.16, "c1": 0.16, "s1": -0.06, "c5": 0.07,
                "g_shock": 0.08},
       note="The sharpest version of the decoupling: output up, capital "
            "concentration up toward C1,crit, fiscal base down. G rises while "
            "everything that makes G governable falls."),
    _E(id="digital_agency_policy", group="displacement",
       label_en="Digital-agency education / counterweight policy programme",
       label_vi="Chương trình giáo dục tự chủ số / đối trọng công cộng",
       effects={"a3": -0.14, "a2": -0.08, "c2": 0.10, "s3": 0.07,
                "base_revenue_demand": 0.008},
       note="DISPL 8.6's three prescriptions - community psychological "
            "support, digital agency education, physical and cultural "
            "counterweights - entered as one lever. The only event in the "
            "catalogue that directly reduces a3."),
]

BY_ID: Dict[str, EventDef] = {e.id: e for e in CATALOGUE}

GROUPS = {
    "fiscal": ("Fiscal / economic", "Tài khóa / kinh tế"),
    "security": ("Security / conflict", "An ninh / xung đột"),
    "legitimacy": ("Legitimacy", "Tính chính danh"),
    "admin": ("Administrative capacity", "Năng lực hành chính"),
    "capital": ("Private capital", "Vốn tư nhân"),
    "civil": ("Civil society", "Xã hội dân sự"),
    "info": ("Information", "Thông tin"),
    "exit": ("Exit options", "Lựa chọn thoát"),
    "fragmentation": ("Fragmentation", "Phân mảnh"),
    "demographic": ("Demographic [Wheel of Fate]", "Dân số [Wheel of Fate]"),
    "displacement": ("Displacement / AI [Displacement Hypothesis]",
                     "Dịch chuyển / AI [Displacement Hypothesis]"),
}


def catalogue() -> dict:
    """Machine-readable catalogue for the API and the form."""
    return {
        "groups": {k: {"label_en": v[0], "label_vi": v[1]}
                   for k, v in GROUPS.items()},
        "events": [e.as_dict() for e in CATALOGUE],
        "targets": {"core": list(CORE_TARGETS), "demo": list(DEMO_TARGETS),
                    "disp": list(DISP_TARGETS), "extra": list(EXTRA_TARGETS)},
        "provenance_key": "events.provenance",
        "usage_key": "events.usage",
    }


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else (hi if x > hi else x)


def apply_events(sub: SubComponents, demo: DemoBlock, disp: DispBlock,
                 inputs: List[EventInput]) -> EventApplication:
    """Accumulate every enabled event's weighted effect, then clamp once.

    Clamping ONCE at the end, not per event, matters: clamping per event would
    make the result depend on the order the caller happened to list them.
    """
    acc: Dict[str, float] = {}
    audit: List[dict] = []
    unknown: List[str] = []

    for ei in inputs:
        if not ei.enabled:
            continue
        d = BY_ID.get(ei.id)
        if d is None:
            unknown.append(ei.id)
            continue
        scale = float(ei.intensity) * float(ei.weight)
        applied = {}
        for tgt, mag in d.effects.items():
            if tgt not in ALL_TARGETS:
                unknown.append(f"{ei.id}:{tgt}")
                continue
            delta = mag * scale
            acc[tgt] = acc.get(tgt, 0.0) + delta
            applied[tgt] = round(delta, 5)
        audit.append(dict(id=ei.id, group=d.group, label_en=d.label_en,
                          label_vi=d.label_vi, intensity=ei.intensity,
                          weight=ei.weight, applied=applied))

    clamped: List[str] = []

    sd = sub.as_dict()
    for k in CORE_TARGETS:
        if k in acc:
            nv = sd[k] + acc[k]
            if nv < 0.0 or nv > 1.0:
                clamped.append(k)
            sd[k] = _clamp(nv)

    dd = demo.as_dict()
    for k in DEMO_TARGETS:
        if k in acc:
            nv = dd[k] + acc[k]
            if nv < 0.0 or nv > 1.0:
                clamped.append(k)
            dd[k] = _clamp(nv)

    ad = disp.as_dict()
    for k in DISP_TARGETS:
        if k not in acc:
            continue
        cur = ad.get(k)
        if k == "physical_share" and cur is None:
            from . import spec2 as _s2
            cur = _s2.DISP["physical_share_default"].value
        nv = (cur or 0.0) + acc[k]
        if nv < 0.0 or nv > 1.0:
            clamped.append(k)
        ad[k] = _clamp(nv)

    extra = {k: acc[k] for k in EXTRA_TARGETS if k in acc}

    codes: List[tuple] = []
    if clamped:
        codes.append(("warn.ev_clamped",
                      {"names": ", ".join(sorted(set(clamped)))}))
    if unknown:
        codes.append(("warn.ev_unknown",
                      {"names": ", ".join(sorted(set(unknown)))}))
    if len(audit) >= 8:
        codes.append(("warn.ev_deep_stack", {"n": len(audit)}))

    return EventApplication(
        sub=SubComponents(**sd), demo=DemoBlock(**dd), disp=DispBlock(**ad),
        extra=extra, audit=audit, clamped=sorted(set(clamped)),
        unknown=sorted(set(unknown)), note_codes=codes)

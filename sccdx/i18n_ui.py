# -*- coding: utf-8 -*-
"""
SCCD-X — Localisation: UI chrome
=================================
Every string the web form renders that is not engine output. Served to the
page through /api/v2/schema so the HTML holds no prose of its own: the page
is a renderer, and switching language re-fetches rather than patching
fragments. That is what makes the VI and EN views genuinely separate instead
of one view with some labels swapped.
"""
from __future__ import annotations

from typing import Dict

UI: Dict[str, Dict[str, str]] = {
    # --- shell ---
    "app.tagline": {
        "vi": "Engine cấu trúc định tính về chính trị thế giới · "
              "sccd v1.00 + Wheel of Fate + Displacement Hypothesis",
        "en": "Qualitative world-politics structural engine · "
              "sccd v1.00 + Wheel of Fate + Displacement Hypothesis"},
    "tab.one": {"vi": "Một chủ thể", "en": "Single polity"},
    "tab.world": {"vi": "Thế giới", "en": "World"},
    "tab.audit": {"vi": "Xuất xứ", "en": "Provenance"},
    "btn.theme": {"vi": "Chủ đề sáng/tối", "en": "Light/dark theme"},
    "lang.vi": {"vi": "Tiếng Việt", "en": "Tiếng Việt"},
    "lang.en": {"vi": "English", "en": "English"},
    "lang.switch_hint": {
        "vi": "Toàn bộ trang và toàn bộ kết quả từ engine đổi sang tiếng "
              "Việt.",
        "en": "The whole page and all engine output switch to English."},

    # --- input panel ---
    "in.title": {"vi": "Đầu vào", "en": "Inputs"},
    "in.preset": {"vi": "Mẫu dựng sẵn", "en": "Preset"},
    "in.year": {"vi": "Năm", "en": "Year"},
    "in.state_type": {"vi": "Loại nhà nước", "en": "State type"},
    "in.horizon": {"vi": "Chân trời (năm)", "en": "Horizon (yr)"},
    "in.run": {"vi": "Chạy chẩn đoán", "en": "Run diagnosis"},
    "in.running": {"vi": "Đang chạy…", "en": "Running…"},
    "in.confidence": {"vi": "độ tin cậy", "en": "confidence"},

    "comps.title": {"vi": "Thành phần & trọng số",
                    "en": "Components & weights"},
    "comps.help": {
        "vi": "Mỗi ô là một biến tiềm ẩn đã chuẩn hóa về [0,1]. Nhãn "
              "BLOCKED nghĩa là sccd.proxies.api_readiness() xác nhận không "
              "có nguồn dữ liệu máy đọc được đa quốc gia cho biến đó — bạn "
              "phải tự mã hóa.",
        "en": "Each box is a latent variable normalised to [0,1]. A BLOCKED "
              "tag means sccd.proxies.api_readiness() confirms there is no "
              "multi-country machine-readable source for it - you must code "
              "it yourself."},
    "grp.core": {"vi": "10 thành phần lõi (sccd Part II–III)",
                 "en": "10 core components (sccd Part II-III)"},
    "grp.demo": {"vi": "Block D — Dân số [Wheel of Fate]",
                 "en": "Block D - Demographic [Wheel of Fate]"},
    "grp.disp": {"vi": "Block A — Dịch chuyển/AI [Displacement Hypothesis]",
                 "en": "Block A - Displacement/AI [Displacement Hypothesis]"},
    "grp.scalars": {"vi": "Vô hướng", "en": "Scalars"},
    "grp.assumptions": {"vi": "Giả định mô hình", "en": "Model assumptions"},

    "events.title": {"vi": "Sự kiện đầu vào", "en": "Event inputs"},
    "events.help": {
        "vi": "Bật sự kiện, đặt cường độ (0–1, mức nghiêm trọng) và trọng số "
              "(hệ số nhân lên hiệu ứng trong catalogue). Sự kiện là mức "
              "CỘNG THÊM lên baseline ở trên — đừng bật một sự kiện mà các "
              "con số baseline của bạn ĐÃ bao hàm, vì engine không phát hiện "
              "được việc đếm hai lần đó.",
        "en": "Switch an event on, set its intensity (0-1, how severe) and "
              "its weight (a multiplier on the catalogue effect). An event is "
              "a level shift ADDED ON TOP of the baseline above - do not "
              "switch on an event whose effect your baseline numbers already "
              "contain, because the engine cannot detect that double count."},
    "events.intensity": {"vi": "cường độ", "en": "intensity"},
    "events.weight": {"vi": "trọng số", "en": "weight"},
    "events.applied": {"vi": "Sự kiện đã áp", "en": "Events applied"},
    "events.shift": {"vi": "Dịch chuyển thực tế", "en": "Shift actually applied"},

    # --- results: verdict ---
    "res.pick": {"vi": "Chọn mẫu dựng sẵn rồi bấm Chạy chẩn đoán.",
                 "en": "Pick a preset and press Run diagnosis."},
    "res.verdict": {"vi": "Phán quyết", "en": "Verdict"},
    "res.regime": {"vi": "Băng Δ", "en": "Delta band"},
    "res.tier": {"vi": "Tầng mạch lạc", "en": "Coherence tier"},
    "res.mode": {"vi": "Chế độ điều chỉnh", "en": "Adjustment mode"},
    "res.vs": {"vi": "so với", "en": "vs"},
    "res.regime_strip_help": {
        "vi": "sccd Part II Table 2. Ô được đánh dấu là băng hiện tại.",
        "en": "sccd Part II Table 2. The marked cell is the current band."},

    # --- results: gates ---
    "res.gates": {"vi": "Cổng ngưỡng", "en": "Threshold gates"},
    "th.variable": {"vi": "Biến", "en": "Variable"},
    "th.level": {"vi": "Mức", "en": "Level"},
    "th.drift": {"vi": "Drift /năm", "en": "Drift /yr"},
    "th.threshold": {"vi": "Ngưỡng", "en": "Threshold"},
    "th.source": {"vi": "Nguồn", "en": "Source"},
    "th.time": {"vi": "Thời gian", "en": "Time"},
    "th.meaning": {"vi": "Ý nghĩa", "en": "Meaning"},
    "val.crossed": {"vi": "đã vượt", "en": "crossed"},
    "val.no_approach": {"vi": "không tiến tới", "en": "not approaching"},
    "val.years": {"vi": "năm", "en": "yr"},
    "res.forcing_line": {
        "vi": "áp lực tổng {total} = bạo lực {violent} + tự nguyện "
              "{voluntary} · S₃_natural = {s3nat}/năm · C₅_structural = "
              "{c5str}/năm · G ×{g} · độ siết = {squeeze}",
        "en": "total pressure {total} = violent {violent} + voluntary "
              "{voluntary} · S3_natural = {s3nat}/yr · C5_structural = "
              "{c5str}/yr · G x{g} · squeeze = {squeeze}"},

    # --- results: loops ---
    "res.loops": {"vi": "Vòng phản hồi", "en": "Feedback loops"},
    "loop.active": {"vi": "ĐANG CHẠY", "en": "ACTIVE"},
    "loop.damped": {"vi": "tắt", "en": "damped"},
    "res.cai_core": {"vi": "CAI_core (L1–L4, băng theo PAPER)",
                     "en": "CAI_core (L1-L4, PAPER bands)"},
    "res.cai_ext": {"vi": "CAI_ext (L1–L8, băng chia lại 4/8)",
                    "en": "CAI_ext (L1-L8, bands rescaled 4/8)"},
    "res.synced": {
        "vi": "Ghép chéo & đang chạy: {loops} → gia tốc hợp thành đang vận "
              "hành.",
        "en": "Cross-coupled & active: {loops} -> compound acceleration "
              "operative."},
    "res.l6_note": {
        "vi": "Đây là chỗ hai bài báo mới trùng nhau. Degrow mô tả nhà nước "
              "Minh muộn tăng thuế trên sổ đất đã lạc hậu hàng thế kỷ — "
              "\"như tiếp tục vắt một con bò đã gầy trơ xương\". Displacement "
              "mô tả cơ sở thuế dịch vào kim loại vật chất mà không sổ nào "
              "thấy được. Cùng một vòng xoáy, cách nhau sáu thế kỷ, một đến "
              "từ dân số học và một từ tâm lý học. Sự bất đối xứng khiến nó "
              "khó thoát: nâng a₄ là một quyết định riêng tư làm một lần, hạ "
              "nó xuống lại đòi người giữ phải tin lại vào sổ sách.",
        "en": "This is where the two new papers coincide. Degrow describes "
              "the late-Ming state raising rates on centuries-stale land "
              "registers - \"like continuing to milk a cow that was already "
              "emaciated to the bone\". Displacement describes the base "
              "relocating into physical metal no register can see. Same "
              "spiral, six centuries apart, one reached from demography and "
              "one from psychology. The asymmetry is what makes it hard to "
              "exit: raising a4 is a private decision taken once, lowering it "
              "requires the holder to trust the register again."},

    # --- results: bifurcation ---
    "res.bifurcation": {"vi": "Rủi ro phân nhánh", "en": "Bifurcation risk"},
    "res.rb_help": {"vi": "sccd eq (23) — cần CẢ BA điều kiện",
                    "en": "sccd eq (23) - ALL THREE conditions required"},
    "res.cond_delta": {"vi": "Δ_norm dưới ngưỡng",
                       "en": "Delta_norm below crit"},
    "res.cond_momentum": {"vi": "động lượng", "en": "momentum"},
    "res.cond_coherence": {"vi": "mạch lạc thấp", "en": "low coherence"},
    "res.attractor": {"vi": "attractor gần nhất", "en": "nearest attractor"},

    # --- results: trajectory ---
    "res.traj": {"vi": "Quỹ đạo", "en": "Trajectory"},
    "res.traj_help": {
        "vi": "Mỗi panel là MỘT biến với thang riêng và ngưỡng riêng. Vạch đỏ "
              "là ngưỡng; vùng tô đỏ nhạt là phía vi phạm.",
        "en": "Each panel is ONE variable with its own scale and its own "
              "threshold. The red rule is the threshold; the pale red band is "
              "the breach side."},
    "res.at_horizon": {"vi": "Tại chân trời", "en": "At horizon"},
    "res.crossings": {"vi": "Điểm vượt ngưỡng", "en": "Threshold crossings"},
    "res.data_table": {"vi": "Bảng số", "en": "Data table"},
    "th.direction": {"vi": "Chiều", "en": "Direction"},

    # --- results: uncertainty ---
    "res.uncertainty": {"vi": "Bất định đo lường", "en": "Measurement uncertainty"},
    "res.median": {"vi": "trung vị", "en": "median"},
    "res.mc_draws": {"vi": "Số lần rút MC", "en": "MC draws"},
    "res.ci80": {"vi": "KTC 80%", "en": "80% CI"},
    "res.width80": {"vi": "độ rộng 80%", "en": "80% width"},
    "res.regime_dist": {"vi": "Phân bố băng chế độ",
                        "en": "Regime band distribution"},

    # --- results: fragility ---
    "res.fragility": {"vi": "Độ mong manh — điều gì khiến cách đọc này sai",
                      "en": "Fragility - what would make this reading wrong"},
    "res.frag_some": {
        "vi": "{n} tham số làm ĐẢO phán quyết định tính dưới nhiễu OAT ±20% "
              "mà sccd eq (SA) bắt buộc. Một phán quyết dịch chuyển khi đẩy "
              "nhẹ 20% một hệ số ANALYST là một GIẢ THUYẾT, không phải một "
              "phát hiện.",
        "en": "{n} parameter(s) FLIP the qualitative verdict under the "
              "+/-20% OAT protocol sccd eq (SA) mandates. A verdict that "
              "moves under a 20% nudge to an ANALYST coefficient is a "
              "HYPOTHESIS, not a finding."},
    "res.frag_none": {
        "vi": "Không tham số nào đảo phán quyết dưới nhiễu OAT ±20%. Đó là độ "
              "bền trước sai số THAM SỐ mà thôi — nó không nói gì về việc cấu "
              "trúc mô hình hay mức đầu vào có đúng hay không.",
        "en": "No parameter flipped the verdict under +/-20% OAT. That is "
              "robustness against PARAMETER error only - it says nothing "
              "about whether the model structure or the input levels are "
              "right."},
    "th.parameter": {"vi": "Tham số", "en": "Parameter"},
    "th.provenance": {"vi": "Xuất xứ", "en": "Provenance"},
    "th.baseline": {"vi": "Gốc", "en": "Baseline"},
    "th.changes": {"vi": "Thay đổi", "en": "Changes"},
    "val.flips": {"vi": "đảo", "en": "flips"},

    # --- results: warnings / narrative ---
    "res.warnings": {"vi": "Cảnh báo hiệu chuẩn", "en": "Calibration warnings"},
    "res.narrative": {"vi": "Diễn giải", "en": "Narrative"},
    "res.error": {"vi": "Lỗi", "en": "Error"},
    "res.error_hint": {
        "vi": "Engine đang chạy chưa? Chạy `python serve.py` rồi mở {url}",
        "en": "Is the engine running? Run `python serve.py` then open {url}"},

    # --- world tab ---
    "w.title": {"vi": "Đọc định tính thế giới", "en": "Qualitative world reading"},
    "w.help": {
        "vi": "Chọn các chủ thể để đưa vào. Ψ_G, Sync_Risk và các độ phân "
              "tán đều là đại lượng gộp mặt cắt ngang — chúng gần như vô "
              "nghĩa nếu dưới khoảng năm chủ thể có trọng số hệ thống.",
        "en": "Pick the polities to include. Psi_G, Sync_Risk and the "
              "dispersion measures are all cross-sectional aggregates - they "
              "are close to meaningless below about five systemically "
              "weighted polities."},
    "w.sync_prior": {"vi": "Sync_Risk tiên nghiệm", "en": "Sync_Risk prior"},
    "w.run": {"vi": "Chạy thế giới", "en": "Run world"},
    "w.coherence": {"vi": "Mạch lạc toàn cục", "en": "Global coherence"},
    "w.prior": {"vi": "tiên nghiệm", "en": "prior"},
    "w.haven_term": {"vi": "trú ẩn", "en": "haven"},
    "w.below": {"vi": "DƯỚI", "en": "BELOW"},
    "w.above": {"vi": "trên", "en": "above"},
    "w.structural_not_forecast": {
        "vi": "điều kiện cấu trúc, không phải dự báo",
        "en": "structural condition, not a forecast"},
    "w.two_channel": {"vi": "Thế giới hai kênh", "en": "The two-channel world"},
    "w.divergence": {"vi": "Độ phân tán điều chỉnh (độ lệch d₃ trọng số)",
                     "en": "Adjustment divergence (weighted d3 dispersion)"},
    "w.divergence_help": {
        "vi": "Độ phân tán này không phải một chỉ số phụ: nó CHÍNH LÀ chênh "
              "lệch áp lực di cư. Nước ở chế độ tự nguyện có kim tự tháp đảo "
              "và cần lao động; nước phơi nhiễm bạo lực có thanh niên dư thừa "
              "không phần. Một thế giới mà mọi nước cùng d₃ thì không có "
              "chênh lệch này, dù áp lực cao đến đâu.",
        "en": "This dispersion is not an incidental statistic: it IS the "
              "migration pressure differential. Polities in voluntary mode "
              "have inverting pyramids and need workers; violent-exposed "
              "polities have surplus youth with no stake. A world where every "
              "polity shares the same d3 has no such gradient however high "
              "the pressure."},
    "w.polities_count": {"vi": "chủ thể", "en": "polities"},
    "w.talent": {"vi": "Chênh lệch tài năng mạnh nhất (đẩy d₅ × hút d₄)",
                 "en": "Strongest talent gradients (push d5 x pull d4)"},
    "th.origin": {"vi": "Gốc", "en": "Origin"},
    "th.destination": {"vi": "Đích", "en": "Destination"},
    "th.push": {"vi": "d₅ đẩy", "en": "d5 push"},
    "th.pull": {"vi": "d₄ hút", "en": "d4 pull"},
    "th.pressure": {"vi": "Áp lực", "en": "Pressure"},
    "w.hegemony": {"vi": "Chuyển dịch bá quyền", "en": "Hegemonic transition"},
    "w.hegemon": {"vi": "bá quyền theo trọng số hệ thống",
                  "en": "hegemon by systemic weight"},
    "w.gap": {"vi": "khoảng cách δ_hc", "en": "gap delta_hc"},
    "w.cond_gap": {"vi": "khoảng cách dưới ngưỡng", "en": "gap below crit"},
    "w.cond_converge": {"vi": "đang hội tụ", "en": "converging"},
    "w.cond_sustained": {"vi": "bền (T_min)", "en": "sustained (T_min)"},
    "w.global_bif": {"vi": "Điều kiện phân nhánh toàn cục",
                     "en": "Global bifurcation condition"},
    "w.cond_low_psiG": {"vi": "mạch lạc toàn cục thấp",
                        "en": "low global coherence"},
    "w.cond_trap": {"vi": "bẫy Thucydides", "en": "Thucydides trap"},
    "w.cond_compound": {"vi": "gia tốc hợp thành", "en": "compound acceleration"},
    "w.per_polity": {"vi": "Theo chủ thể", "en": "Per polity"},
    "w.psi_by_polity": {"vi": "Ψ theo chủ thể", "en": "Psi by polity"},
    "w.psi_bar_help": {
        "vi": "Một series, sắp theo thứ tự. Vạch đỏ là Ψ_crit = {crit} "
              "[PAPER].",
        "en": "One series, ordered. The red rule is Psi_crit = {crit} "
              "[PAPER]."},
    "w.below_thresh": {"vi": "dưới ngưỡng", "en": "below threshold"},
    "th.code": {"vi": "Mã", "en": "Code"},
    "th.loops_active": {"vi": "Vòng chạy", "en": "Active loops"},
    "th.gate": {"vi": "Cổng θ₂₅", "en": "theta25 gate"},

    # --- audit tab ---
    "a.title": {"vi": "Xuất xứ tham số", "en": "Parameter provenance"},
    "a.level_drift": {"vi": "MỨC so với DRIFT", "en": "LEVEL vs DRIFT"},
    "a.open_problems": {"vi": "Vấn đề mở của lớp v2",
                        "en": "v2 layer open problems"},
    "a.inconsistencies": {"vi": "Mâu thuẫn trong chính sccd v1.00",
                          "en": "Known inconsistencies inside sccd v1.00"},
    "a.patch_note": {
        "vi": "Engine chạy mặc định với patch=True và c1_dynamic=True — tức "
              "bật cả ba bản sửa CRITICAL — vì Block A cấp cơ chế có nguồn "
              "cho số hạng mà INC-7 nói là thiếu, và Block D cấp cơ chế cho "
              "số hạng INC-8 nói là thiếu.",
        "en": "The engine runs with patch=True and c1_dynamic=True by "
              "default - all three CRITICAL repairs on - because Block A "
              "supplies a sourced mechanism for the term INC-7 says is "
              "missing, and Block D one for the term INC-8 says is missing."},
    "a.v2_params": {"vi": "Tham số lớp v2", "en": "v2 layer parameters"},
    "a.degrow_anchors": {"vi": "Mốc lịch sử Degrow nêu số",
                         "en": "Historical anchors Degrow states numerically"},
    "a.displ_numbers": {"vi": "Số liệu Displacement Hypothesis công bố",
                        "en": "Numbers printed in The Displacement Hypothesis"},
    "a.backtest_only": {
        "vi": "Dùng cho back-test, không bao giờ dùng làm hệ số.",
        "en": "For back-testing only, never used as coefficients."},
    "th.id": {"vi": "Mã", "en": "ID"},
    "th.severity": {"vi": "Mức", "en": "Severity"},
    "th.where": {"vi": "Ở đâu", "en": "Where"},
    "th.issue": {"vi": "Vấn đề", "en": "Issue"},
    "th.group": {"vi": "Nhóm", "en": "Group"},
    "th.name": {"vi": "Tên", "en": "Name"},
    "th.value": {"vi": "Giá trị", "en": "Value"},
    "th.note": {"vi": "Ghi chú", "en": "Note"},
    "th.case": {"vi": "Ca", "en": "Case"},
    "th.metric": {"vi": "Chỉ số", "en": "Metric"},
    "th.stage": {"vi": "Giai đoạn", "en": "Stage"},
    "th.section": {"vi": "Mục", "en": "Section"},
    "a.loading": {"vi": "Đang tải…", "en": "Loading…"},

    # --- trajectory panel titles ---
    "pan.psi": {"vi": "Ψ  chỉ số mạch lạc", "en": "Psi  coherence index"},
    "pan.psi.sub": {
        "vi": "Ψ = λ·θ₂₅·(1−C₅). Dưới ngưỡng → điều kiện thứ 3 của R_B bật.",
        "en": "Psi = lambda*theta25*(1-C5). Below threshold -> R_B's third "
              "condition trips."},
    "pan.delta_norm": {"vi": "Δ_norm  chênh lệch năng lực",
                       "en": "Delta_norm  capacity differential"},
    "pan.delta_norm.sub": {
        "vi": "sccd eq (10). Dưới −0.08 là vào băng Khủng hoảng.",
        "en": "sccd eq (10). Below -0.08 enters the Crisis band."},
    "pan.theta25": {"vi": "θ₂₅  hệ số ngưỡng", "en": "theta25  threshold factor"},
    "pan.theta25.sub": {
        "vi": "Cổng của Wheel of Fate. Đóng qua S₅ (già hóa) hoặc S₂ (thanh "
              "niên).",
        "en": "The Wheel of Fate's gate. Closes through S5 (aging) or S2 "
              "(youth)."},
    "pan.s3": {"vi": "S₃  vốn chính danh", "en": "S3  legitimacy capital"},
    "pan.s3.sub": {
        "vi": "Nhân vào toàn bộ S qua λ. Dưới 0.30 thì L2 thành bùng nổ.",
        "en": "Multiplies all of S through lambda. Below 0.30 L2 becomes "
              "explosive."},
    "pan.s5": {"vi": "S₅  đòn bẩy thời gian", "en": "S5  temporal leverage"},
    "pan.s5.sub": {"vi": "Điểm cuối tự nguyện/già hóa của Degrow.",
                   "en": "Degrow's voluntary/aging terminus."},
    "pan.s2": {"vi": "S₂  độc quyền cưỡng chế", "en": "S2  coercive monopoly"},
    "pan.s2.sub": {"vi": "Điểm cuối bạo lực/thanh niên của Degrow.",
                   "en": "Degrow's violent/youth terminus."},
    "pan.c5": {"vi": "C₅  phân mảnh ưu tiên",
               "en": "C5  preference fragmentation"},
    "pan.c5.sub": {
        "vi": "Mẫu số của C và hệ số (1−C₅) trong Ψ. Tăng là xấu.",
        "en": "The C denominator and the (1-C5) factor in Psi. Rising is "
              "bad."},
    "pan.c1": {"vi": "C₁  tập trung vốn", "en": "C1  capital concentration"},
    "pan.c1.sub": {
        "vi": "Trên 0.70 thì Γ bật và L1 có thể lên nòng.",
        "en": "Above 0.70 Gamma turns on and L1 can arm."},
}


def ui(lang: str) -> dict:
    """Flatten the table for one language."""
    l = "en" if (lang or "").lower().startswith("en") else "vi"
    return {k: v.get(l, v["en"]) for k, v in UI.items()}


def _register_ui_into_T() -> None:
    """Mirror every UI string into i18n.T.

    The narrative layer and the web page need the SAME strings - section
    headings, column headers, the L6 note. Keeping two tables would let them
    drift, which is the exact failure this whole refactor exists to remove.
    So UI is the authoring surface and T is the lookup surface, and this
    copies one into the other at import time.
    """
    from . import i18n as I
    for k, v in UI.items():
        if k not in I.T:
            I._add(k, v["vi"], v["en"])


_register_ui_into_T()


# ---------------------------------------------------------------------------
# Option help, registered into the main table so /api/v2/schema can serve it
# ---------------------------------------------------------------------------
def _register_option_help() -> None:
    from . import i18n as I
    I._add(
        "op.router.help",
        "Cách bộ định tuyến của Block D xử lý tổng áp lực. 'conserve' chuyển "
        "hướng nó; 'discount' còn làm nó co lại. Degrow không giải quyết điểm "
        "này — xem vấn đề mở OP2-1.",
        "How Block D's router treats total pressure. 'conserve' redirects it; "
        "'discount' also shrinks it. Degrow does not settle this - see open "
        "problem OP2-1.")
    I._add(
        "op.haven.help",
        "True sẽ dồn dòng vốn trú ẩn CHỈ qua C₄, tắt drift S₁ trực tiếp. Dùng "
        "nếu bạn cho rằng hai kênh đang đếm hai lần — vấn đề mở OP2-3.",
        "True routes haven flight ONLY through C4, disabling the direct S1 "
        "drift. Use if you think the two channels double count - open problem "
        "OP2-3.")
    I._add(
        "op.horizon.help",
        "Vượt quá khoảng 20 năm thì các đầu vào Block D và Block A bị giữ cố "
        "định trong khi lẽ ra không nên, nên nó thành bài tập tĩnh-so-sánh.",
        "Beyond about 20 years the Block D and A inputs are held constant and "
        "should not be, so it becomes comparative statics.")


_register_option_help()

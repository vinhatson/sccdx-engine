# -*- coding: utf-8 -*-
"""
SCCD-X — Localisation: the long reference texts
================================================
Split out of i18n.py purely for file size. These are the texts that appear in
the Provenance tab and in field help: the v2 open-problem register, sccd's own
nine known inconsistencies, the 46 v2 parameter notes, the 50 event notes, and
the 10 preset rationales.

The English side is the authoritative wording, because it is the wording that
sits in spec2.py / events.py / presets.py next to the code it describes. The
Vietnamese side is a translation of that, not an independent text, so the two
languages always make the same claim.

Where a passage quotes one of the source papers, the quotation is left in
English inside the Vietnamese text and marked with quotation marks. Translating
a quotation would misrepresent it - a reader checking the claim against the PDF
needs the words that are actually in the PDF.
"""
from __future__ import annotations

from typing import Dict

# ===========================================================================
#  v2 OPEN PROBLEMS  (spec2.OPEN_PROBLEMS_V2)
# ===========================================================================
OPEN_PROBLEMS: Dict[str, Dict[str, str]] = {
    "OP2-1": {
        "where_vi": "Block D, bộ định tuyến",
        "vi": "Phép chia P_violent/P_voluntary = (1−d₃)/d₃ là cách ĐỌC Degrow "
              "của engine, không phải phát biểu của chính Degrow. Paper lập "
              "luận rằng hai kênh là \"different manifestations of the same "
              "fundamental law\" và rằng công cụ hiện đại cho phép người ta "
              "\"cut the spiral at its first stage\" — đó đúng là ý nghĩa của "
              "một bộ định tuyến. Nhưng paper không bao giờ nói tổng áp lực "
              "được BẢO TOÀN qua phép chia. Nếu điều chỉnh tự nguyện rẻ hơn "
              "về tổng áp lực — điều hợp lý, vì nó phòng ngừa chứ không phải "
              "dọn dẹp quá tải — thì d₃ phải làm giảm chính P_demo chứ không "
              "chỉ chuyển hướng nó. Engine phơi điều này ra thành `router_mode` "
              "('conserve' | 'discount') để giả định là một núm điều chỉnh "
              "thay vì một chọn lựa bị che. Mặc định: conserve.",
    },
    "OP2-2": {
        "where_vi": "Block A, sigma_agency",
        "vi": "Liên kết tự-chủ → chính-danh là tuyên bố chịu lực của toàn bộ "
              "lớp v2 và đồng thời là tuyên bố ít bằng chứng nhất. "
              "Displacement có tư liệu về xói mòn tự chủ và có tư liệu về tái "
              "phân bổ vốn; nó KHÔNG có tư liệu về một sự sụt giảm tính chính "
              "danh của chế độ, và không đưa ra chuỗi khảo sát nào về sự đồng "
              "thuận. Engine khẳng định liên kết này trên cơ sở rằng sự đồng "
              "thuận của người bị trị được cấu thành bởi đúng cái quyền tự "
              "tác giả mà paper nói đang tan rã. Đó là một LẬP LUẬN, không "
              "phải một PHÉP ĐO. Nếu nó sai thì L5 là giả, và drift S₃ ở các "
              "nền dân chủ giàu bị phóng đại.",
    },
    "OP2-3": {
        "where_vi": "Block A, đếm hai lần a₄",
        "vi": "Dòng vốn trú ẩn đánh vào S₁ hai lần: trực tiếp qua "
              "zeta_base_s1, và gián tiếp vì C₄ được nâng lên sẽ cắt τ_eff "
              "thông qua chính hệ số (1−Ĉ₄) của sccd. Đây thực sự là hai kênh "
              "khác nhau (quy mô cơ sở so với tỷ lệ thu-trích) nhưng engine "
              "không thể chứng minh chúng không chồng lấn. Đặt "
              "`haven_single_channel=True` để tắt số hạng trực tiếp và dồn "
              "toàn bộ qua Ĉ₄.",
    },
    "OP2-4": {
        "where_vi": "Block A so với phép đo Ĉ₄ của sccd",
        "vi": "Ĉ₄ hiệu dụng giờ trộn hai thứ mà sccd Part III đo như một: "
              "thoát theo quyền phán xử (Chinn-Ito, OECD DIOC) và thoát theo "
              "hình thái tài sản (tỷ phần trú ẩn). Chúng có động lực đảo "
              "chiều khác nhau — kiểm soát vốn có thể đóng đường thoát theo "
              "quyền phán xử trong một cuối tuần; kim loại trong két nội địa "
              "không bị một sắc lệnh nào thu hồi. Coi chúng là một đại lượng "
              "vô hướng duy nhất là đánh giá thấp mức độ khó đảo chiều của "
              "thoát theo hình thái tài sản.",
    },
    "OP2-5": {
        "where_vi": "Chồng lấn giữa Block D và Block A",
        "vi": "d₂ (bẫy kỳ vọng) và a₂ (xói mòn tự-hiệu-năng) được đo riêng "
              "nhưng cả hai đều kéo lùi việc lập gia đình và cả hai đều rút "
              "cạn S₃. Trong một bảng dữ liệu OECD 2026 chúng sẽ cộng tuyến "
              "mạnh. Engine không khử cộng tuyến, nên một người gọi đặt cả "
              "hai đều cao là đang đếm hai lần một áp lực. Việc kiểm định "
              "Cronbach (sccd.normalize) sẽ bắt được nếu có chuỗi số liệu; "
              "với giá trị điểm nhập tay thì không gì bắt được.",
    },
    "OP2-6": {
        "where_vi": "L8 so với L2 của sccd",
        "vi": "Điều kiện kích hoạt của L8 chồng lấn với L2 của sccd (vòng xoáy "
              "mất chính danh) mỗi khi thanh niên dư thừa đã đẩy S₃ xuống "
              "dưới 0.30. CAI khi đó đếm hai vòng ở nơi mà có thể lập luận "
              "chỉ có một cơ chế đang chạy. Bản đồ ghép chéo đánh dấu cặp "
              "này, và engine báo `cai_overlap_warning`, nhưng phép đếm không "
              "được hiệu chỉnh.",
    },
    "OP2-7": {
        "where_vi": "thừa hưởng",
        "vi": "Mọi thứ trong sccd.spec.KNOWN_INCONSISTENCIES vẫn còn hiệu lực. "
              "INC-7/8/9 ở mức CRITICAL và vì vậy engine v2 chạy MẶC ĐỊNH với "
              "patch=True và c1_dynamic=True của sccd, tức đảo ngược mặc định "
              "của v1.00. Lý do: Block A cấp một cơ chế có nguồn cho số hạng "
              "giảm phân cực mà INC-7 nói là thiếu (tổ chức phản-công-nghệ "
              "thông qua Ĉ₂), và Block D cấp một cơ chế cho số hạng phục hồi "
              "chính danh mà INC-8 nói là thiếu (hiệu quả giao hàng chính "
              "sách thông qua Ŝ₄). Đặt `faithful_v1=True` để tái lập paper "
              "nguyên văn thay thế.",
    },
}

# ===========================================================================
#  sccd v1.00 KNOWN INCONSISTENCIES  (sccd.spec.KNOWN_INCONSISTENCIES)
# ===========================================================================
INCONSISTENCIES: Dict[str, Dict[str, str]] = {
    "INC-1": {
        "where_vi": "Part II Table 1",
        "vi": "Các dòng trọng số theo loại nhà nước đều cộng đúng 1.00 — ràng "
              "buộc được thỏa. Không cần hành động.",
    },
    "INC-2": {
        "where_vi": "Part II eq (6) so với eq (7)",
        "vi": "eq(6) áp phép điều chỉnh thoát Π lên toàn bộ Σ v_j·Ĉ_j; eq(7) "
              "áp nó chỉ lên v₁·Ĉ₁. Hai cách này không tương đương. Mặc định "
              "của engine là eq(7) (c1_only); đổi qua spec.PI_SCOPE.",
    },
    "INC-3": {
        "where_vi": "Part I Table 1 so với Part II Table 2",
        "vi": "Part I nói Δ được chuẩn hóa về (−1,1); Part II dẫn ra "
              "Δ_norm ∈ (−0.40, 1.00). Biên các băng khớp nhau; chặn dưới thì "
              "không. Engine dùng Part II.",
    },
    "INC-4": {
        "where_vi": "Part II §2.1 so với eq (3)",
        "vi": "Paper nói λ(0.20)≈0.55 và λ(0.38)≈0.93, nhưng eq(2) với các "
              "tham số của eq(3) cho ra 0.502 và 1.037. λ(0.50)=1.40 thì khớp "
              "chính xác. Hoặc các ví dụ được dẫn dùng k/mid khác, hoặc chúng "
              "chỉ là con số xấp xỉ.",
    },
    "INC-5": {
        "where_vi": "Part III §3.5 so với Part IV §2.3",
        "vi": "C₅ của Mỹ năm 2024 được nêu là 0.72 (Part III, MFS) và 0.74 "
              "(Part IV §2.3 và Part V V.US). Chênh lệch nhỏ nhưng engine "
              "buộc phải chọn một; mặc định lấy 0.74 (Part V).",
    },
    "INC-6": {
        "where_vi": "Part III §3.5 so với Part IV §2.3",
        "vi": "Mốc nền C₅ của Mỹ năm 1980 được nêu là 0.35 (Part III) và 0.28 "
              "(Part IV §2.3).",
    },
    "INC-7": {
        "where_vi": "Part IV eq (NL), dC₅/dt",
        "vi": "dC₅/dt = C₅_structural + ε_p·C₅(1−C₅)·Rev_Pol + η·C₅²·C₃ "
              "+ ξ·Ĉ₄Ĉ₁(1−C₅). CẢ BA số hạng nội sinh đều DƯƠNG và không có "
              "số hạng giảm phân cực nào, dù §2.3 định nghĩa bài kiểm kích "
              "hoạt L3 dựa trên một 'Natural_Depolarisation_Rate'. Như đã "
              "viết, C₅ tăng đơn điệu về 1 trên mọi quỹ đạo, do đó "
              "Ψ = λ·θ₂₅·(1−C₅) → 0 bất kể kịch bản. CÁCH SỬA: thêm −ν·C₅ "
              "(hoặc −ν·C₅·C₂, vì Part IV §2.3 gọi C₂ là 'the primary "
              "counterweight to L3') vào dC₅/dt.",
    },
    "INC-8": {
        "where_vi": "Part IV eq (NL), dS₃/dt",
        "vi": "dS₃/dt = S₃_natural − ρ_b(1−λ/λmax)² − ζ·C₅^ψ(S₃−S₃floor). Cả "
              "hai số hạng nội sinh đều ÂM. Với S₃_natural là ngoại sinh, S₃ "
              "chỉ có thể suy giảm, nên mô hình không thể sinh ra chính sự "
              "TÁI LẬP tính chính danh mà Part V §2.3 ghi nhận cho giai đoạn "
              "1980–86 (λ 1.2 → 1.7) hay cho đợt dựng lực 1941–45. Part IV "
              "§2.2 có gọi tên một tốc độ 'natural legitimacy recovery' nhưng "
              "nó không bao giờ vào hệ phương trình. CÁCH SỬA: thêm một số "
              "hạng phục hồi, ví dụ +σ·(S₃_target(performance) − S₃), được "
              "điều khiển bởi mức thành công thực thi S₄.",
    },
    "INC-9": {
        "where_vi": "Part IV §2.1 so với vector trạng thái §7.1",
        "vi": "§2.1 viết tường minh phương trình C₁ — 'dC₁/dt = v₁·D_drain→C₁ "
              "+ r(t)C₁(1−C₁/C₁max) − τ_eff·C₁ + μ·Γ' — nhưng §7.1 (INT) liệt "
              "kê các biến trạng thái là [S_i, C_i, S₃,i, C₅,i]: C₁ BỊ BỎ SÓT "
              "và bị coi là ngoại sinh. Hệ quả: với C₁ ngoại sinh, cả dS₃/dt "
              "lẫn dC₅/dt đều không phụ thuộc S hay C, nên [S₃,C₅] thành một "
              "hệ con TỰ TRỊ chỉ chạy một chiều vào [S,C]. Trong eq (NL) như "
              "đã viết KHÔNG tồn tại vòng phản hồi khép kín nào cả — L1 và L4 "
              "bị hở, và bảng ghép chéo ở §2.4 không được phương trình nào "
              "hiện thực hóa. Dấu hiệu chẩn đoán: mọi kịch bản đều cho cùng "
              "một C₅(t) và cùng một Ψ(t). CÁCH SỬA: nâng C₁ thành biến trạng "
              "thái thứ năm bằng chính phương trình của §2.1. Trong engine: "
              "simulate(..., c1_dynamic=True).",
    },
}

# ===========================================================================
#  v2 PARAMETER NOTES  (spec2 DEMO / DISP / WORLD2 / loop weights)
# ===========================================================================
PARAM_NOTES: Dict[str, str] = {
    # --- Block D ---
    "kappa_exp":
        "trọng số của bẫy kỳ vọng bên trong tải hiệu dụng. Paper khẳng định "
        "d₂ THAY THẾ khan hiếm cổ điển ở các xã hội giàu nhưng không đưa ra "
        "tỷ giá chuyển đổi nào.",
    "route_sharpness":
        "số mũ trên d₃ trong phép chia. 1.0 = chia tuyến tính. Lớn hơn 1 "
        "nghĩa là xả bạo lực vẫn còn dai dẳng cho tới khi công cụ tự nguyện "
        "gần như phổ quát. Paper ngụ ý một chuyển dịch dứt khoát ('revolution "
        "in survival thinking') nhưng không lượng hóa gì.",
    "nu_youth_frag":
        "thanh niên dư thừa → C₅_structural. Dấu lấy từ 'deep polarization "
        "among the populace'.",
    "sigma_relief":
        "thất bại của hệ thống cứu trợ → drift S₃. Dấu lấy từ 'the breaking "
        "of the most sacred social contract... The people's trust in the "
        "dynasty's mandate of heaven completely shattered.'",
    "erode_s2":
        "đạo quân dự bị làm suy giảm ĐỘC QUYỀN CƯỠNG CHẾ của nhà nước (không "
        "phải khối lượng cưỡng chế): 'gathered into gangs, lived outside the "
        "law, ready to become mercenaries, bandits'. Đánh vào Ŝ₂, biến khống "
        "chế cổng θ₂₅ tại Ŝ₂,crit=0.25 (PAPER).",
    "erode_s4_corrupt":
        "độ thâm nhập hành chính suy giảm dưới áp lực kéo dài: 'corruption "
        "transformed from individual behavior into the default operating "
        "mechanism', chính quyền trung ương rơi vào 'information blindness'.",
    "iota_inversion":
        "áp lực tự nguyện tích tụ thành đảo chiều phụ thuộc. Đây chính là cái "
        "giá mà paper gọi tên: 'They accept facing a new demographic "
        "challenge (aging) as the price to pay to avoid an old demographic "
        "disaster.'",
    "compress_s5":
        "đảo chiều phụ thuộc nén ĐÒN BẨY THỜI GIAN Ŝ₅. Ŝ₅ được định nghĩa "
        "trong sccd Part III là chân trời ngân sách chưa bị cam kết; lương "
        "hưu đúng là sự cam kết trước của ngân sách. ĐÃ HẠ XUỐNG từ mức ban "
        "đầu 0.045 vì có một phản chứng trực tiếp: Nhật Bản đã ngồi trong "
        "khoảng ~0.03 quanh cổng 0.15 của θ₂₅ suốt hai thập kỷ mà không có "
        "sự gián đoạn mà cái cổng đó được cho là đánh dấu. Ở mức 0.045, cổng "
        "đóng trong vòng 15 năm với MỌI chủ thể già hóa trong tập preset, "
        "điều này khiến chẩn đoán trở thành bất khả phản nghiệm thay vì mang "
        "thông tin. Mức 0.018 giữ được cơ chế mà phục hồi khả năng phân biệt. "
        "Dạng rút-cạn-hằng-số vẫn giả định KHÔNG có phản ứng chính sách nào — "
        "không nâng tuổi nghỉ, không điều chỉnh lại cách gắn chỉ số trợ cấp — "
        "nên nó vẫn là một chặn trên của tốc độ nén.",
    "compress_s1":
        "cơ sở người đóng góp co lại trong khi nghĩa vụ cố định làm xói mòn "
        "nguồn thu còn quyền định đoạt Ŝ₁.",
    "sigma_expect":
        "bẫy kỳ vọng xét như một dòng rút cạn CHÍNH DANH thuần khiết, độc lập "
        "với sản lượng. Đây là cơ chế cho phép S₃ giảm trong khi GDP tăng — "
        "tương đương hiện đại của cơn khát đất thời cổ. Các mô hình vĩ mô "
        "thông thường không có khe nào cho nó.",
    "d5_violent_thresh":
        "mức thanh niên dư thừa mà trên đó kênh bạo lực là kênh đang vận "
        "hành.",
    "d3_voluntary_thresh":
        "mức quyền tự chủ điều chỉnh mà trên đó chủ thể ở chế độ tự nguyện.",
    "d4_inversion_thresh": "",
    "d2_trap_thresh": "",
    "s2_floor": "dịch chuyển mức: sàn cứng cho Ŝ₂ đã được tích phân",
    "s4_floor": "dịch chuyển mức: sàn cứng cho Ŝ₄ đã được tích phân",
    "s5_floor":
        "dịch chuyển mức: sàn cứng cho Ŝ₅ đã được tích phân. LƯU Ý sàn này "
        "nằm DƯỚI cổng PAPER Ŝ₅,crit=0.15 của θ₂₅, nên cổng vẫn đóng được — "
        "sàn chỉ ngăn dòng rút cạn chạm tới một con số không vô lý.",
    # --- Block A ---
    "tier_w1": "trọng số trên Tầng 1 (a₂)",
    "tier_w2": "trọng số trên Tầng 2 (a₃)",
    "tier_w_cross":
        "số hạng tăng cường lẫn nhau a₂·a₃. Paper nói rõ rằng tương tác này "
        "tồn tại: 'economic helplessness deepens the existential crisis... "
        "and existential crisis intensifies economic paralysis. The compound "
        "effect...'. Độ lớn thì không có nguồn.",
    "sigma_agency":
        "xói mòn tự chủ → drift S₃, được nhân theo mức thâm nhập. Dấu lấy từ "
        "các cơ chế khủng hoảng bản sắc và vô nghĩa của paper, cộng với chính "
        "mục chính sách của nó: nhóm bị ảnh hưởng 'retain their jobs but lose "
        "their sense of agency, competence, and self-authored identity'. Sự "
        "đồng thuận của người bị trị được làm ra từ đúng những thứ đó.",
    "g_ai":
        "số nhân thặng dư vào G(t). Vào theo cùng cách mà g_tech·T_shock vào "
        "trong sccd Part II eq (12).",
    "zeta_haven_c4":
        "tái phân bổ trú ẩn → Ĉ₄ HIỆU DỤNG. Thoát theo hình thái tài sản được "
        "cộng vào thoát theo quyền phán xử của sccd.",
    "zeta_base_s1":
        "phần không khả-kiến của tài sản trú ẩn rời khỏi cơ sở có thể thu "
        "trích. Được nhân với physical_share, vì vàng giấy vẫn khả-kiến và "
        "vẫn bị thu thuế — chính sự phân biệt đó LÀ dự đoán thứ ba của paper.",
    "zeta_lux_s1":
        "xói mòn cơ sở thuế tiêu dùng do phân khúc khát-vọng rút đi. Con số "
        "của chính paper: người mua khát-vọng chiếm 60–70% cơ sở khách hàng "
        "xa xỉ và sự sụt giảm 'overwhelmingly concentrated' ở đó.",
    "nu_narrative":
        "sự tan rã bản sắc tự thuật → C₅_structural. 'The individual's life "
        "story becomes less a self-authored novel...' cộng với nỗi sợ bị đồng "
        "hóa vào 'AI-optimized, AI-influenced sameness'.",
    "nu_counter":
        "tổ chức cộng đồng phản-công-nghệ LÀM GIẢM PHÂN CỰC, qua Ĉ₂. LƯU Ý: "
        "đây là bộ sinh CÓ NGUỒN đầu tiên cho số hạng mà sccd INC-7 nói là "
        "thiếu trong dC₅/dt. Bản patch của v1.00 thêm −ν·C₅·C₂ trên cơ sở "
        "rằng Part IV §2.3 gọi tên C₂ là đối trọng nhưng bỏ số hạng đó; Block "
        "A giờ cấp một cơ chế thực sự sản sinh ra nó.",
    "zeta_ctr_c2":
        "động viên phản-công-nghệ → mật độ tổ chức dân sự Ĉ₂. 'They will "
        "attract mainstream participation from precisely the demographic most "
        "exposed to agency erosion: educated, digitally fluent "
        "professionals.'",
    "zeta_uhnw_c1":
        "sự xói mòn bất đối xứng theo tầng lớp, nên nó LÀM TẬP TRUNG Ĉ₁. "
        "Theo paper: nhóm siêu giàu 'whose identity and agency are secured by "
        "capital rather than cognitive labor' giữ được vị thế trong khi tầng "
        "khát-vọng bị bóc đi. Ĉ₁ sau đó nuôi vòng L1 của sccd tại ngưỡng "
        "PAPER Ĉ₁,crit = 0.70.",
    "a1_mass_thresh": "mức phổ cập đại chúng",
    "a3_crisis_thresh": "",
    "a4_flight_thresh": "",
    "squeeze_thresh":
        "độ siết thu-trích (tỷ lệ bị đòi trừ tỷ lệ khả thi) mà trên đó vòng "
        "L6 tự duy trì.",
    "physical_share_default":
        "tỷ phần vật chất (so với vàng giấy/ETF) mặc định của phân bổ trú ẩn "
        "khi người gọi không cấp. Dữ kiện của paper: cầu thanh và xu vượt "
        "1.200 tấn mỗi năm song song với dòng vào ETF ở mức kỷ lục.",
    # --- world ---
    "haven_sync_gain":
        "dòng vốn trú ẩn đồng thời xuyên các nhà nước có trọng số hệ thống tự "
        "nó là một kênh đồng pha, nên nó làm tăng Sync_Risk trong Ψ_G của "
        "sccd. Bản thân Sync_Risk của sccd chỉ là một tiên nghiệm lịch sử "
        "trần trụi (0.12/0.24/0.41/0.58 cho 1980/95/2010/2024); phần này cấp "
        "cho nó một bộ điều khiển nội sinh. Lập luận hậu thuẫn là luận cứ về "
        "độ rộng của cầu trong paper: cầu 'across all investor types... "
        "consistent with a pervasive psychological shift'.",
    "divergence_talent_gain":
        "độ phân tán của d₃ xuyên thế giới CHÍNH LÀ chênh lệch áp lực di cư: "
        "một nửa thế giới ở chế độ tự nguyện cần lao động, nửa kia có thanh "
        "niên dư thừa. Đưa vào kênh F^talent sẵn có của sccd.",
    "ai_divergence_gain":
        "độ phân tán của a₁ làm rộng khoảng cách năng lực, và đó là một đầu "
        "vào của bài kiểm hội tụ Thucydides.",
    # --- loop weights ---
    "coupling_L5": "sccd cũng không đưa giá trị Coupling_Weight nào cho "
                   "L1–L4; trọng số đơn vị giữ CAI là một phép đếm số vòng "
                   "đang chạy, điều ít nhất là trung thực.",
    "coupling_L6": "như trên", "coupling_L7": "như trên",
    "coupling_L8": "như trên",
    "speed_L5": "", "speed_L6": "", "speed_L7": "", "speed_L8": "",
    "CAI_EXT_SCALE": "chia lại tỷ lệ các băng CAI của sccd cho tập vòng mở "
                     "rộng",
}

# ===========================================================================
#  EVENT NOTES  (events.CATALOGUE) — Vietnamese side
# ===========================================================================
EVENT_NOTES: Dict[str, str] = {
    "sovereign_debt_stress":
        "Đánh mạnh nhất vào S₅: trả nợ là khoản ngân sách bị cam kết trước, "
        "đúng cái mà Đòn bẩy Thời gian của sccd đo.",
    "inflation_surge":
        "S₁ tăng trong ngắn hạn — lạm phát là một loại thuế — trong khi S₃ "
        "giảm và cầu trú ẩn tăng. Phần S₁ được thêm là lý do lạm phát được "
        "chọn, và phần S₃ bị mất là lý do nó không giúp được lâu.",
    "currency_crisis": "",
    "energy_shock": "",
    "tariff_war":
        "C₄ GIẢM: việc đóng cửa thương mại và tài khoản vốn lấy đi các lựa "
        "chọn thoát. Đây là một trong rất ít sự kiện cắt đường thoát thay vì "
        "mở rộng nó.",
    "sanctions_imposed":
        "S₃ TĂNG: áp lực từ bên ngoài thường củng cố tính chính danh đối nội "
        "trong ngắn hạn (hiệu ứng tụ quanh lá cờ). sccd không có số hạng nào "
        "cho điều này, nên nó vào dưới dạng một sự kiện.",
    "tech_productivity_boom": "",
    "interstate_war_onset":
        "Đúng khuôn mẫu 1941–45 ở sccd Part V: tổng động viên nâng cả năng "
        "lực cưỡng chế LẪN tính chính danh cùng lúc, trong khi tiêu thụ đòn "
        "bẩy thời gian. Hãy đối chiếu với thặng dư từ AI, thứ nâng sản lượng "
        "mà HẠ tính chính danh — chính sự đối chiếu đó là toàn bộ lý do tồn "
        "tại của cờ tách rời.",
    "civil_conflict":
        "Đẩy S₂ về phía cổng PAPER 0.25 của θ₂₅ — điểm cuối bạo lực trong mô "
        "hình của Degrow.",
    "coup_or_irregular_transfer": "",
    "alliance_rupture": "",
    "military_buildup": "",
    "contested_election": "",
    "mass_protest":
        "C₂ TĂNG — biểu tình chính là tổ chức dân sự. Trong dC₅/dt đã vá, "
        "điều đó biến nó thành một lực giảm phân cực ngay cả khi nó rút cạn "
        "S₃, nên dấu ròng lên phân mảnh là thực sự không xác định và phụ "
        "thuộc vào nu_counter so với số hạng C₅ trực tiếp.",
    "corruption_scandal": "",
    "constitutional_crisis": "",
    "succession_crisis": "",
    "successful_major_reform":
        "Chiều dương ở đây quan trọng về mặt cấu trúc: với patch của sccd "
        "được bật, dS₃/dt có thêm +σ_rec·(s3_target_gain·Ŝ₄ − S₃), nên một "
        "mức tăng Ŝ₄ thực sự sẽ kéo attractor của S₃ lên. Đây là con đường "
        "duy nhất mà engine có để TÁI LẬP tính chính danh — chính cái mà "
        "INC-8 nói các phương trình của paper không thể sinh ra.",
    "implementation_failure": "",
    "disaster_response_failure": "",
    "state_capacity_investment": "",
    "wealth_concentration_jump":
        "Đẩy C₁ về phía ngưỡng PAPER C₁,crit = 0.70 của sccd, trên mức đó số "
        "hạng thâu tóm Γ bật và vòng L1 có thể lên nòng.",
    "regulatory_capture_event": "",
    "major_redistribution": "",
    "civil_society_crackdown":
        "Hãy để ý cái bẫy mà điều này tạo ra trong hệ đã vá: cắt C₂ loại bỏ "
        "số hạng giảm phân cực −ν_depol·C₅·C₂, nên đàn áp xã hội dân sự làm "
        "TĂNG phân mảnh trong dài hạn. Nhà nước mua được S₂ trong ngắn hạn "
        "bằng cái giá là C₅ vĩnh viễn.",
    "union_or_community_resurgence": "",
    "media_capture": "",
    "internet_shutdown": "",
    "disinformation_surge": "",
    "capital_controls":
        "Minh họa sắc nét nhất cho spec2 OP2-4. Kiểm soát vốn đóng đường "
        "thoát theo QUYỀN PHÁN XỬ (C₄ giảm) và trong cùng một động tác đẩy "
        "tài sản sang đường thoát theo HÌNH THÁI TÀI SẢN (a₄ tăng), thứ mà "
        "Block A sau đó lại đưa trở về C₄ hiệu dụng. Việc đường thoát ròng có "
        "giảm chút nào hay không phụ thuộc vào zeta_haven_c4 — và đó là một "
        "con số ANALYST.",
    "emigration_wave": "",
    "immigration_surge":
        "Liên kết trực tiếp duy nhất của engine giữa hai nửa thế giới của "
        "Degrow: dòng vào làm nhẹ đi sự đảo chiều phụ thuộc của nước nhận, "
        "đồng thời cộng thêm tải và phân mảnh.",
    "polarising_election": "",
    "secession_movement": "",
    "ethnic_mobilisation": "",
    "fertility_collapse":
        "Đường hiện đại của DEGROW, nhưng xét như một đầu vào thay vì một đầu "
        "ra. Nâng biến định tuyến d₃ và mức đảo chiều d₄ cùng lúc.",
    "pension_reform_failure":
        "Lên nòng vòng L7 trực tiếp: sự đảo chiều bị chốt lại và không gian "
        "tài khóa để làm nhẹ bẫy kỳ vọng thì đã hết.",
    "housing_affordability_crisis":
        "Cơ chế hiện đại trung tâm của DEGROW. Phép ví của chính paper: "
        "'analogous to ancient peasants' inability to access land - both "
        "represent a denial of the opportunity to establish a stable family "
        "foundation.'",
    "youth_unemployment_surge":
        "'Đạo quân dự bị của hỗn loạn' theo DEGROW. Lên nòng vòng L8 ở những "
        "nơi d₃ thấp.",
    "land_or_resource_squeeze":
        "Ràng buộc Malthus cổ điển, vẫn còn sống ở phần lớn thế giới. DEGROW "
        "Giai đoạn 1–2.",
    "relief_system_failure":
        "DEGROW §2.1 nguyên văn — 'the breaking of the most sacred social "
        "contract'. Một trong những đòn đánh S₃ lớn nhất của catalogue, vì "
        "paper coi đây là thời điểm thiên mệnh chấm dứt.",
    "family_formation_support":
        "Chính là khuyến nghị chính sách của DEGROW: 'make housing, "
        "education, and childcare genuinely affordable... The goal is to make "
        "having children a feasible and desirable choice, not an unbearable "
        "burden.' Hãy để ý rằng nó TỐN S₅ — việc làm nhẹ cái bẫy tự thân là "
        "một sự cam kết trước ngân sách, và đó chính là lý do L7 là một cái "
        "bẫy.",
    "ai_mass_adoption": "",
    "whitecollar_displacement":
        "Đánh đúng vào lớp người mà DISPL §8.5 gọi tên: 'the population most "
        "capable of using AI is the population most existentially threatened "
        "by it'. Hãy để ý S₁ giảm — lớp đó chính là cơ sở thuế thu nhập.",
    "agency_crisis_visible":
        "DISPL §4.4.3. Liên kết chịu lực nhất và đồng thời ít bằng chứng nhất "
        "của engine — hãy đọc spec2 OP2-2 trước khi tựa vào cái này.",
    "haven_flight_surge":
        "DISPL §5–6. Diễn biến 2023–2026 mà paper ghi nhận: vàng từ khoảng "
        "2.000 lên trên 5.500 USD/oz, bạc khoảng +150%, bạch kim khoảng "
        "+110%.",
    "luxury_contraction":
        "DISPL §2.3, §6.2: mất 50–60 triệu người tiêu dùng trong 2022–2025, "
        "sự sụt giảm tập trung ở tầng khát-vọng vốn chiếm 60–70% cơ sở.",
    "counter_tech_movement":
        "'Chủ nghĩa Luddite Mới' theo DISPL §8.5. Lực giảm phân cực chính của "
        "engine: nó nâng C₂, thứ điều khiển số hạng −ν_depol·C₅·C₂ mà sccd "
        "INC-7 nói là đang thiếu trong chính dC₅/dt của paper.",
    "ai_windfall_captured":
        "Phiên bản sắc nét nhất của sự tách rời: sản lượng tăng, tập trung "
        "vốn tăng về phía C₁,crit, cơ sở tài khóa giảm. G tăng trong khi mọi "
        "thứ làm cho G có thể quản trị được thì giảm.",
    "digital_agency_policy":
        "Ba khuyến nghị của DISPL §8.6 — hỗ trợ tâm lý cộng đồng, giáo dục tự "
        "chủ số, và các đối trọng vật chất lẫn văn hóa — được đưa vào thành "
        "một cần điều khiển duy nhất. Đây là sự kiện duy nhất trong catalogue "
        "làm giảm a₃ một cách trực tiếp.",
}

# ===========================================================================
#  PRESET RATIONALES  (presets.PRESETS_2026) — Vietnamese side
# ===========================================================================
PRESET_RATIONALE: Dict[str, str] = {
    "US":
        "Dòng duy nhất có giá trị do paper nêu. Hãy để ý rằng chính phần "
        "kiểm chứng của sccd tìm ra Ψ(Mỹ 2024) = 0.265 so với mức 0.43 mà "
        "paper nêu — với θ₂₅ ≤ 1 và C₅ = 0.74 thì đồng nhất thức "
        "Ψ = λ·θ₂₅·(1−C₅) chặn Ψ ở 0.24 khi dùng chính λ = 0.93 của paper, "
        "nên 0.43 nằm ngoài chặn của chính nó. Engine báo giá trị tính được "
        "và kết luận đảo chiều: R_B có thể lên nòng ở nơi paper nói là không.",
    "CN":
        "S₄ và S₂ cao, C₂/C₃/C₄ thấp theo đúng cách loại nhà nước này được "
        "cấu tạo. d₄ được đặt gần mức của Mỹ dù quá khứ gần đây trẻ hơn nhiều, "
        "vì sự đảo chiều đang đến nhanh hơn. Mức co cụm xa xỉ được đặt cao "
        "nhất trong tập: bài Displacement định vị sự sụt giảm sắc nét nhất và "
        "hiện tượng 'luxury shame' ở đúng đây.",
    "EU":
        "Được coi là một chủ thể duy nhất, và đó là một sự bóp méo thật: khối "
        "này không có một S₂ hay một S₃ duy nhất, và C₅ của nó một phần là "
        "phân mảnh GIỮA các thành viên chứ không phải trong nội bộ. Hãy tách "
        "thành các nước thành viên nếu câu hỏi là về phân mảnh nội bộ. a₅ cao "
        "nhất trong các chủ thể lớn — đối trọng phản-công-nghệ mạnh nhất ở "
        "đây.",
    "JP":
        "Phép thử thuần khiết nhất cho điểm cuối tự nguyện của Degrow: d₄ = "
        "0.88 và s₅ = 0.18, đã nằm trong khoảng 0.03 quanh cổng PAPER 0.15 "
        "của θ₂₅. Nếu cơ chế Ŝ₅ trong Block D có đúng chút nào thì nó phải "
        "lộ ra ở đây trước tiên và rõ nhất. Hãy để ý điểm phản biện mà engine "
        "không được che: Nhật đã ngồi cạnh cái cổng này suốt hai thập kỷ mà "
        "không có sự sụp đổ mà cái cổng được cho là đánh dấu, và đó là bằng "
        "chứng chống lại việc compress_s5 lớn như spec2 đặt.",
    "KR":
        "d₂ = 0.92, bẫy kỳ vọng cao nhất trong tập — nhà ở, học thêm tư và "
        "văn hóa làm việc quá giờ cộng lại. Degrow gọi thẳng tên Seoul làm ca "
        "hiện đại của mình. d₃ cao nhất cùng với Nhật, nên vòng L7 phải đang "
        "lên nòng.",
    "IN":
        "d₃ = 0.52 nằm đúng điểm giữa của bộ định tuyến, nên áp lực chia khá "
        "đều xuống cả hai kênh của Degrow — dòng duy nhất trong tập làm vậy. "
        "a₄ cao so với mức thu nhập của nước này vì việc hộ gia đình giữ vàng "
        "ở đây là cấu trúc sẵn có chứ không phải một sự tái phân bổ của "
        "2023–26, và đó là một vấn đề đo lường thực sự cho Block A: biến này "
        "vốn để nắm bắt một SỰ DỊCH CHUYỂN, không phải một lượng tồn.",
    "RU":
        "c₁ = 0.84 đi cùng s₂ = 0.84: mức thâu tóm là cực đoan nhưng độc "
        "quyền cưỡng chế còn nguyên, nên L1 của sccd KHÔNG lên nòng — điều "
        "kiện của nó là Ĉ₁ > 0.70 VÀ Ŝ₂ < 0.60, cần cả hai. a₄ cao nhất trong "
        "tập và kiểm soát vốn cũng cao nhất, đúng là cấu hình OP2-4: thoát "
        "theo quyền phán xử đóng kín, thoát theo hình thái tài sản mở toang.",
    "BR":
        "s₂ = 0.52, dưới ngưỡng 0.60 của L1 trong sccd, đi cùng c₁ = 0.74 "
        "trên mức C₁,crit = 0.70. Cả hai điều kiện PAPER đều hội đủ, nên L1 "
        "lên nòng ở đây mà không lên nòng ở Nga. c₅ = 0.72, gần mức của Mỹ. "
        "Đây là dòng ở chế độ HỖN HỢP.",
    "GB":
        "c₄ cao nhất trong tập — một tài khoản vốn mở và một lựa chọn di cư "
        "bằng tiếng Anh — kết hợp với s₅ = 0.22. Cặp đó là cấu hình L6 sắc "
        "nét nhất: nhu cầu thu cao, cơ sở khả-kiến thì di động.",
    "NG":
        "Dòng làm cho engine trung thực. d₅ = 0.86 cùng d₃ = 0.24 chính là "
        "kênh cổ đại của Degrow, không pha loãng, và vòng L8 tồn tại đúng cho "
        "ca này. Không có nó thì công cụ sẽ đọc toàn bộ nửa trẻ của thế giới "
        "là 'yên tĩnh' chỉ vì L5–L7 đều là vòng của xã hội giàu và già. "
        "s₂ = 0.42 đã nằm trong khoảng 0.17 quanh cổng PAPER 0.25 của θ₂₅, "
        "theo cửa bạo lực thay vì cửa tài khóa.",
}

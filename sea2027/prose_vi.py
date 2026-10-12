# -*- coding: utf-8 -*-
"""
sea2027.prose_vi - bản đọc văn xuôi tiếng Việt, mỗi chủ thể một mục
=====================================================================
Đây là DIỄN GIẢI, và nó là của tôi, không phải của engine. Engine phát ra một
băng, một tầng, một chế độ, một bộ vòng và một thứ tự cổng; nó không phát ra
lập luận về ý nghĩa của những thứ đó. Mọi điều ở đây là lập luận dựng trên
các đầu ra ấy cộng với bảng số đo trong raw_2026.py, và một người chấp nhận
các con số vẫn hoàn toàn có thể bác bỏ cách đọc.

Chỗ nào một câu đứng trên đầu vào ANALYST thay vì số đo, câu đó nói rõ. Mục
`fragile` của mỗi chủ thể nêu đích danh điều gì phải sai thì cách đọc mới sụp.

File song hành: prose_en.py, cùng nội dung bằng tiếng Anh. Hai bản được VIẾT
chứ không dịch qua lại nhau — nhưng chúng khẳng định cùng những điều, và nếu
có lúc nào lệch nhau về nội dung thì đó là lỗi của file này hoặc file kia.
"""
from __future__ import annotations

PROSE = {

# ===========================================================================
"TH": dict(
 title="Cấu trúc tuổi Nhật Bản trên một phần tư thu nhập Nhật Bản",
 lede=[
  "Thái Lan mang ba vòng đang chạy vào năm 2027, và là chủ thể duy nhất "
  "trong khu vực có hai vòng ghép chéo với nhau. Engine vẫn đọc Thương lượng "
  "/ Căng ở cuối 2027 — băng không dịch trong cửa sổ này — nhưng đây là hàng "
  "giòn nhất bộ với khoảng cách rõ rệt, và là nơi một sự kiện chính trị bình "
  "thường cũng đủ lật cách đọc.",
 ],
 body=[
  "Phải bắt đầu từ dữ kiện dân số, vì mọi thứ khác uốn quanh nó. Tỷ lệ phụ "
  "thuộc người già là 23.0 và tổng tỷ suất sinh là 1.2, ở mức 26.250 USD PPP "
  "đầu người. Đó là cấu trúc tuổi của Nhật Bản trên khoảng một phần tư thu "
  "nhập Nhật Bản, và nó đang tới trong lúc độ phủ hưu trí chính thức của nhà "
  "nước mới là 4.5%. Cam kết thì đã được luật hóa — bảo hiểm y tế toàn dân "
  "cộng trợ cấp người cao tuổi — nên gánh nặng rơi vào ngân sách chung chứ "
  "không vào một quỹ có nguồn. Đối lại, bản WEO tháng 10/2026 của IMF cho nợ "
  "công tăng từ 64.7% lên 67.8% GDP vào 2027, trên nền tăng trưởng 1.5% năm "
  "2026 và 2.1% năm 2027: cặp tăng trưởng yếu nhất Đông Nam Á, đúng lúc hóa "
  "đơn dân số bắt đầu tới.",

  "Cấu hình đó là thứ kích hoạt L7, Bẫy Đảo chiều Dân số, và L7 đang chạy "
  "cạnh L6, Vòng Xoáy Khả-kiến–Thu-trích. Engine gắn cờ cặp này là ghép "
  "chéo, tức không chỉ cả hai cùng có mặt mà còn nuôi lẫn nhau. Cơ chế thì "
  "không hào nhoáng và rất cũ: nhà nước cần thêm nguồn thu vì tháp dân số "
  "đang lộn ngược, nên nó siết mạnh hơn vào phần cơ sở nó nhìn thấy, và phần "
  "cơ sở ấy đáp lại bằng cách trở nên khó nhìn hơn. Độ siết thu trích của "
  "Thái Lan là +0.284 so với ngưỡng 0.10 — đòi 0.305 so với khả thi 0.020 — "
  "và mức tái phân bổ trú ẩn ở 0.56, vừa vượt ngưỡng kích hoạt 0.55, với "
  "20.9 tấn vàng thanh và xu mua trong nửa đầu 2026 và quý I mạnh nhất kể từ "
  "2019.",

  "Vòng thứ ba, L3, là Bẫy Phân cực, và đây là chỗ năm chính trị bước vào. "
  "Ĉ₅ đã vượt ngưỡng 0.50 của nó, hiện ở 0.69. Cuộc bầu cử tháng 2/2026 cho "
  "Bhumjaithai 192 trên 500 ghế và đưa Anutin trở lại, nhưng không hóa giải "
  "được đường đứt gãy bảo hoàng–cải cách; tới tháng 10/2026, Đảng Nhân dân "
  "đang thu chữ ký cho kiến nghị theo Điều 151 nhắm vào mười hai bộ trưởng, "
  "trong đó có Thủ tướng, quanh bê bối tuyển chọn Thượng viện. Biên giới "
  "Campuchia thêm một trục nữa: lệnh ngừng bắn tháng 12/2025 đã trụ qua các "
  "vụ mìn và việc triển khai quân tiền phương mà không bình thường hóa được.",

  "Thứ tự cổng mới là phần đáng mang theo. Ĉ₅ đã vượt. Ŝ₃ chạm sàn PAPER "
  "0.30 trong khoảng mười năm và Ŝ₅ chạm 0.15 trong khoảng hai mươi bảy năm. "
  "Ŝ₂ thì cách hai thế kỷ. Vậy điểm cuối của Thái Lan là cửa tự nguyện — cửa "
  "già hóa, tài khóa — chứ không phải cửa bạo lực, và đó là ý nghĩa của chế "
  "độ ĐIỀU CHỈNH TỰ NGUYỆN ở đây. Ở mốc mười lăm năm, engine đọc Cân bằng / "
  "Rời rạc: không phải sụp đổ, mà là một nhà nước đã mất khả năng hành động "
  "mạch lạc về bất cứ việc gì.",
 ],
 stress="Nhánh stress là chỗ Thái Lan tách khỏi phần còn lại. Thêm khủng "
        "hoảng hiến định ở cường độ 0.50 — tức kiến nghị Điều 151 ngã về "
        "phía chống chính phủ — cộng thất bại cải cách hưu trí ở 0.40 và cú "
        "sốc thuế quan áp cho cả khu vực, thì phán quyết dịch: Thương lượng "
        "/ Căng thành Cân bằng / Rời rạc, Ψ rơi từ 0.320 xuống 0.157, và L2, "
        "Vòng Xoáy Mất Chính danh, bật thêm lên trên ba vòng đang chạy. Bốn "
        "vòng đồng thời là cấu hình xấu nhất ở bất cứ đâu trong khu vực, cả "
        "baseline lẫn stress. Hãy để ý những sự kiện này là gì: không phải "
        "đảo chính, không phải chiến tranh, không phải khủng hoảng tài "
        "chính. Một kiến nghị bất tín nhiệm thành công và một cải cách hưu "
        "trí thất bại là chính trị thường ngày.",
 fragile="Năm trong 42 tham số OAT làm đảo phán quyết định tính của Thái Lan "
         "ở ±20% — hàng giòn nhất bộ. Ba trong số đó (d3_voluntary_thresh, "
         "d4_inversion_thresh, d2_trap_thresh) tắt hẳn L7, nghĩa là Bẫy Đảo "
         "chiều Dân số — cái vòng mà toàn bộ cách đọc này dựng quanh — đứng "
         "trên những hệ số ANALYST mà một cú đẩy 20% là bật ra. Hãy coi L7 ở "
         "đây là một giả thuyết mà dữ liệu dân số đo được làm cho hợp lý, "
         "chứ không phải một phát hiện.",
 watch=[
  "Kiến nghị Điều 151 có được nộp không, và có thông qua không. Nhánh stress "
  "đặt điều kiện trên việc nó ngã về phía chống chính phủ.",
  "Bất kỳ động thái nào về trợ cấp người cao tuổi hoặc tuổi nghỉ hưu. Drift "
  "d₄ của engine giả định KHÔNG có phản ứng chính sách; một cải cách thật sẽ "
  "bác bỏ đoạn dốc nhất của đường Ŝ₅.",
  "Cầu vàng thanh và xu của Thái Lan suốt 2027. Trên mức 2026 thì a₄ còn "
  "trên ngưỡng 0.55 và L6 còn kích hoạt; rơi mạnh thì L6 tắt.",
  "Tăng trưởng 2027 có về gần mức 2.1% của IMF không. Thấp hơn đáng kể sẽ "
  "đẩy đường nợ vượt 67.8% và siết thẳng vào độ siết thu trích.",
  "Biên giới Campuchia. Không phải vì bản thân giao tranh, mà vì điều engine "
  "nói một cuộc bùng phát thật sự sẽ gây ra — xem phần Campuchia.",
 ],
 limits="Cách đọc Thái Lan tựa vào đầu vào ANALYST nhiều hơn bất kỳ nước "
        "nào. Số hạng cam kết hưu trí (0.70), ba nhánh của C₅ và mức trú ẩn "
        "đều là lập luận chứ không phải số đo, và năm tham số làm đảo phán "
        "quyết dưới mức nhiễu ±20% bắt buộc. Hướng đi thì được dữ liệu dân "
        "số và đường tài khóa đo được hậu thuẫn tốt; bộ vòng cụ thể thì "
        "không.",
),

# ===========================================================================
"PH": dict(
 title="Nước duy nhất đổi tầng ngay trong cửa sổ",
 lede=[
  "Philippines là chủ thể duy nhất trong mười một nước có phán quyết dịch "
  "ngay trong năm 2027 trên baseline, không cần thêm sự kiện stress nào. Nó "
  "bước vào cửa sổ ở Cân bằng / Căng và rời cửa sổ ở Cân bằng / Rời rạc, với "
  "điểm cắt vào khoảng t = 0.25 — đầu năm 2027. Đây cũng là hàng duy nhất có "
  "ba trong bốn vòng GỐC của sccd cùng chạy.",
 ],
 body=[
  "CAI_core ở đây là 3.0, cao nhất khu vực. Con số đó quan trọng hơn CAI mở "
  "rộng, vì L1–L4 là những vòng mà bài báo gốc đặc tả và hiệu chuẩn; bốn "
  "vòng mới đều là ANALYST. Nên khi Philippines ghi ba trên bốn vòng gốc, "
  "engine đang khẳng định bên trong bộ máy được hậu thuẫn tốt nhất của nó, "
  "chứ không phải trong lớp mà dự án này thêm vào.",

  "L1, Bộ Gia tốc Thâu tóm Quy chế, bật vì cả hai điều kiện PAPER của nó "
  "được thỏa cùng lúc: Ĉ₁ là 0.77, trên ngưỡng thâu tóm 0.70, trong khi Ŝ₂ "
  "là 0.54, dưới sàn 0.60. Nga trong bộ preset gốc có mức thâu tóm cực đoan "
  "hơn mà L1 không bật, vì độc quyền cưỡng chế của Nga còn nguyên vẹn. Sự "
  "kết hợp kiểu Philippines — tư bản tập trung, được chính trị hóa, bên cạnh "
  "một nhà nước không độc quyền trọn vẹn về bạo lực — chính là cặp điều kiện "
  "mà vòng này được viết ra để bắt.",

  "L2, Vòng Xoáy Mất Chính danh, là vòng dịch chuyển ngay trong cửa sổ. Ŝ₃ "
  "cắt sàn PAPER 0.30 của nó ở t = 0.33, và tầng mạch lạc vỡ xuống Rời rạc "
  "hơi sớm hơn thế một chút. Nền tảng đo được và tra cứu được là bê bối công "
  "trình chống lụt: Bộ Tài chính ước thiệt hại lên tới 118,5 tỷ peso giai "
  "đoạn 2023–25, một cuộc tuần hành 600.000 người tháng 11/2025, 37 đơn tố "
  "giác hình sự đã nộp, và — tính tới tháng 2/2026 — không một nghị sĩ đương "
  "nhiệm nào bị tạm giam. Khoảng cách giữa quy mô phẫn nộ và sự vắng mặt của "
  "hệ quả chính là cơ chế. Vốn chính danh bị tiêu đi bằng cách chứng minh "
  "rằng luật không ràng buộc những người viết ra luật.",

  "L3 được nuôi bởi rạn nứt Marcos–Duterte, giờ đã mang tính thể chế chứ "
  "không còn là phe phái: phiên luận tội thứ hai đối với Phó Tổng thống chạy "
  "từ 6/7/2026, tòa Thượng viện tự thay đổi ngưỡng kết tội hồi tháng 9, và "
  "có tin phán quyết có thể ra vào giữa tháng 12. Ĉ₅ thì đã vượt 0.50.",

  "Bên dưới chính trị là mức phơi nhiễm Block A, cao nhất khu vực: phơi "
  "nhiễm lao động tri thức 0.72 trên nền tỷ lệ phổ cập AI tạo sinh đo được "
  "0.207, cao thứ ba ở đây. Ngành BPO đúng là lớp công việc nhận thức mà "
  "Displacement Hypothesis mô tả đang bị thay thế. Đối lại, lối thoát lao "
  "động là 0.85 với kiều hối 8.5% GDP — lựa chọn ra đi đã được thể chế hóa, "
  "điều này vừa giảm áp lực vừa chặn mức Ĉ₄ còn có thể tăng thêm.",
 ],
 stress="Thêm hậu luận tội và dịch chuyển lao động BPO làm Ψ giảm gần một "
        "nửa, 0.234 xuống 0.115, mà không đổi phán quyết — vì phán quyết đã "
        "là Rời rạc rồi. Đó là dấu hiệu của một chủ thể không còn khoảng "
        "trống: cú stress không dịch được nhãn, nó chỉ khoét sâu thêm. Ở mốc "
        "mười lăm năm, engine đọc Khủng hoảng / Rời rạc.",
 fragile="Chỉ hai tham số làm đảo phán quyết ở ±20%, nên theo OAT thì cách "
         "đọc này tương đối vững. Nhưng bản thân mức s₃ mang một khoản chiết "
         "khấu ANALYST 0.30 cho bê bối, mà s₃ lại là proxy rủi ro cao nhất "
         "của chính sccd và thuộc diện BLOCKED — không có nguồn xuyên quốc "
         "gia nào cho hai trong bốn trụ của nó. Việc đổi tầng ở t = 0.25 là "
         "hệ quả trực tiếp của chỗ mà khoản chiết khấu ấy đặt mức xuất phát.",
 watch=[
  "Phán quyết luận tội và những gì theo sau. Kết tội hay tha bổng đều đẩy Ĉ₅ "
  "cùng một hướng; khác nhau là Ŝ₃ có hồi phục chút nào không.",
  "Có nghị sĩ đương nhiệm nào thực sự bị tạm giam không. Theo logic của "
  "engine, đây là sự kiện phục hồi chính danh mạnh nhất hiện có.",
  "Quy mô nhân sự BPO. Một đợt co lại đo được sẽ biến phơi nhiễm Block A từ "
  "một phép chiếu thành một quan sát.",
  "Dòng kiều hối. Nó đang giữ sàn cho thu nhập hộ gia đình; sụt giảm sẽ chất "
  "tải lên cả d₁ lẫn d₅ cùng lúc.",
 ],
 limits="Mọi điều trên đây là thứ tự, không phải mức. Engine không nói "
        "Philippines sẽ có khủng hoảng năm 2027; nó nói tầng vỡ ngay trong "
        "cửa sổ theo các drift hiện tại, rằng ba vòng được PAPER đặc tả đang "
        "chạy, và rằng cổng gần nhất đã ở mốc không năm.",
),

# ===========================================================================
"ID": dict(
 title="Bá chủ khu vực, mà đọc ra Căng",
 lede=[
  "Indonesia mang trọng số hệ thống lớn nhất trong mười một nước và engine "
  "gọi nó là bá chủ khu vực. Nó cũng đọc ra Cân bằng / Căng với hai cổng đã "
  "vượt, và Δ_norm của nó cắt xuống âm ngay trong 2027 — một trong chỉ hai "
  "chủ thể xảy ra điều đó. Pass Monte-Carlo đặt 10% khối lượng xác suất vào "
  "băng Khủng hoảng, tỷ lệ khủng hoảng cao nhất khu vực.",
 ],
 body=[
  "Hai ngưỡng PAPER đã nằm phía sau Indonesia chứ không phải phía trước. Ŝ₃ "
  "đã dưới sàn 0.30 và Ĉ₅ đã trên ngưỡng phân mảnh 0.50. Cả hai đều không "
  "phải dự báo; cả hai là trạng thái xuất phát. Rồi engine bổ sung rằng các "
  "cổng còn lại thì rất xa — Ŝ₂ cách 68 năm và Ŝ₅ cách 127 năm — nên "
  "Indonesia không đang tiến về một điểm cuối nào. Nó đã ở sẵn bên trong dải "
  "mà các ngưỡng được vạch ra để đánh dấu, và đang ngồi đó.",

  "L2 và L6 là cặp đang hoạt động. Phía chính danh có bằng chứng tốt hơn: "
  "điểm dân chủ tự do 2025 của V-Dem là 0.296, thấp nhất một thập kỷ, và làn "
  "sóng biểu tình 2025–26 nằm CHỒNG LÊN con số đó chứ không nằm trong nó — "
  "chi phí sinh hoạt, sa thải hàng loạt, phụ cấp nghị sĩ, bạo lực cảnh sát, "
  "rồi ngộ độc chương trình bữa ăn miễn phí và đợt tăng giá nhiên liệu tháng "
  "6/2026. Engine mã hóa điều đó thành khoản chiết khấu tỷ lệ 26% trên vốn "
  "chính danh, lớn nhất áp cho bất kỳ chủ thể nào ở đây, và con số ANALYST "
  "đơn lẻ ấy là phán đoán hệ trọng nhất trong cả file đầu vào.",

  "Phía L6 là bằng chứng Block A chắc nhất khu vực, và nó là số đo chứ không "
  "phải lập luận. Hộ gia đình Indonesia mua 38.1 tấn vàng thanh và xu trong "
  "nửa đầu 2026 — nhiều hơn Thái Lan cộng Việt Nam — tăng khoảng 40% so cùng "
  "kỳ, trong khi cầu trang sức giảm 10%. Chính Hội đồng Vàng Thế giới quy "
  "điều đó cho đồng tiền yếu và lo ngại về triển vọng trong nước. Đó không "
  "phải mua đồ trang sức; đó là hành vi bảng cân đối, và nó đúng là dạng "
  "thoát theo hình thái tài sản mà Ĉ₄ dựa trên pháp quyền của sccd không "
  "nhìn thấy.",

  "Khung tài khóa siết cả hai phía. Ngân sách 2026 chạy mức thâm hụt sát "
  "trần luật định 3% GDP, với chương trình bữa ăn miễn phí tăng gần gấp đôi "
  "lên khoảng 20,7 tỷ USD trong khi chuyển giao cho chính quyền địa phương "
  "bị cắt; Moody's hạ triển vọng xuống tiêu cực; bộ trưởng tài chính bị thay. "
  "Một nhà nước tăng đòi hỏi trên một cơ sở đang đồng thời tái phân bổ sang "
  "hình thái không khả kiến chính là cấu hình L6 ở dạng phát biểu trần trụi "
  "nhất.",

  "Hãy để ý Indonesia KHÔNG phải cái gì. Năng lực biểu tình được mã hóa ở "
  "0.85, đồng hạng cao nhất khu vực, vì những cuộc huy động đó nhiều lần "
  "buộc chính sách phải đảo ngược — đó là hiệu quả phối hợp, và đó mới là "
  "thứ Ĉ₂ của sccd thực sự hỏi. Ĉ₂ cao là năng lực dân sự, không phải nhà "
  "nước yếu, và đó là lý do chính khiến băng 2027 giữ được ở chỗ Philippines "
  "vỡ.",
 ],
 stress="Trần thâm hụt 3% vỡ cộng áp lực lên rupiah đưa Ψ từ 0.355 xuống "
        "0.336 mà không dịch phán quyết. Indonesia có nhiều khoảng trống "
        "trong 2027 hơn là đường 15 năm của nó gợi ý. Ở mốc mười lăm năm, "
        "engine đọc Khủng hoảng / Rời rạc.",
 fragile="Ba tham số làm đảo phán quyết ở ±20%, và một trong số đó "
         "(a4_flight_thresh) tắt hẳn L6 ở mức +20%. Quan trọng hơn, khoản "
         "chiết khấu bất ổn 0.26 là một con số lập luận không có số đo đứng "
         "sau: đó là khẳng định của nhà phân tích rằng làn sóng biểu tình "
         "chưa được tính vào bản V-Dem và WGI năm 2025. Nếu điều đó sai thì "
         "Ŝ₃ của Indonesia đang bị đặt quá thấp và toàn bộ cách đọc Căng sẽ "
         "dịu đi.",
 watch=[
  "Trần thâm hụt 3% có giữ được qua chu kỳ ngân sách 2027 không.",
  "Cầu vàng thanh và xu của Indonesia. Năm thứ hai gần nhịp 2026 sẽ biến a₄ "
  "từ một đợt tái phân bổ một năm thành một xu thế, và đó là khẳng định "
  "khác hẳn.",
  "Quy mô chương trình bữa ăn miễn phí có sống sót khi va vào nguồn thu "
  "không.",
  "Tần suất biểu tình VÀ việc biểu tình có còn buộc đảo ngược chính sách "
  "không. Vế sau mới là thứ Ĉ₂ đo; riêng vế đầu thì không.",
 ],
 limits="Indonesia là bá chủ theo trọng số GDP, và cách engine chọn bá chủ "
        "là máy móc — trọng số hệ thống, không phải thành tích. Không nên "
        "đọc bất cứ điều gì trong phép tính Ψ_G như một phán xét rằng "
        "Indonesia dẫn dắt khu vực theo nghĩa nào khác.",
),

# ===========================================================================
"SG": dict(
 title="Chủ thể duy nhất mà sự tách rời đo được",
 lede=[
  "Singapore đọc ra Bá quyền / Mạch lạc trong 2027 với đúng một vòng đang "
  "chạy, và là nơi duy nhất trong mười một nước mà khẳng định trung tâm của "
  "Displacement Hypothesis có thể kiểm bằng một tỷ lệ phổ cập ĐO ĐƯỢC thay "
  "vì suy ra. Chỉ số tách rời của nó là 0.485; nước cao thứ hai khu vực là "
  "0.046.",
 ],
 body=[
  "Số liệu phổ cập quý II/2026 của Microsoft cho thấy 64.3% người trong tuổi "
  "lao động ở Singapore có dùng một sản phẩm AI tạo sinh — đứng thứ hai thế "
  "giới sau UAE. Chính con số đo được đơn lẻ ấy làm hàng này khác biệt. Ở mọi "
  "nơi khác trong khu vực, a₁ của Block A hoặc là một con số in ra nhỏ hơn "
  "nhiều, hoặc là ước lượng của nhà phân tích quy từ tỷ lệ dùng internet; ở "
  "đây mức phổ cập đủ cao, và được đo đủ tốt, để cơ chế có cái mà bám vào.",

  "Cơ chế ấy là L5, Vòng Xoáy Tự chủ–Chính danh, và nó chính là vòng mà tài "
  "liệu của engine tự gắn cờ là mắt xích yếu nhất. Chuỗi chạy như sau: phổ "
  "cập cao nhân với phơi nhiễm lao động tri thức cao sinh ra xói mòn tự chủ, "
  "và xói mòn tự chủ rút cạn chính danh, bởi vì sự ưng thuận của người bị "
  "cai trị được làm nên từ chính cái quyền tự viết nên mình mà bài báo nói "
  "đang tan rã. Vấn đề mở OP2-2 của dự án nói thẳng rằng mắt xích này là lập "
  "luận chứ không phải số đo — bài báo nguồn có ghi nhận xói mòn tự chủ, có "
  "ghi nhận tái phân bổ vốn, và không ghi nhận ở bất cứ đâu một sự sụt giảm "
  "chính danh chế độ. Singapore là nơi lập luận ấy phơi ra rõ nhất, vì ở đây "
  "tiền đề là thật và đo được. Nếu L5 là giả, đây là chỗ sự vắng mặt phải "
  "hiện ra.",

  "Trên thực tế, `decoupling_active` nghĩa là Δ_norm và Ψ giờ có thể đi "
  "ngược chiều nhau — quy ước đọc đầu ra của engine bị phá, và nó nói ra "
  "điều đó thay vì giấu. Số hạng windfall của Singapore lớn nhất khu vực "
  "(a₆ = 0.78) và nâng G lên, trong khi số hạng tự chủ đẩy S₃ xuống. Một "
  "cách đọc kiểu v1.00, vốn chỉ có năm băng Δ, sẽ báo cáo đây là tăng trưởng "
  "yên ả.",

  "Thứ tự cổng cũng đặc biệt. Với mọi chủ thể khác trong khu vực, cổng gần "
  "nhất là Ŝ₃ hoặc một cổng đã vượt. Với Singapore, đó là Ĉ₅ ở khoảng mười "
  "ba năm, Ŝ₃ ở hai mươi mốt và Ŝ₅ ở ba mươi hai. Ŝ₂ thì coi như không bao "
  "giờ — phép chiếu trả về hàng chục nghìn năm, đó là cách engine nói drift "
  "bằng không về mặt số học. Vậy thứ đóng trước ở đây là phân mảnh, không "
  "phải năng lực tài khóa và cũng không phải độc quyền cưỡng chế.",

  "Có một lựa chọn trong file đầu vào cần nói rõ, vì nó là chỗ dễ tranh cãi "
  "nhất cả bộ: Singapore được đọc như một chế độ chuyên chế phát triển chứ "
  "không phải dân chủ tự do. Lý do thì hẹp — state_type chỉ đặt ba trọng số, "
  "và trên ba trọng số đó thì vector WGI 2025 (hiệu quả chính phủ bách phân "
  "vị 95, tiếng nói và trách nhiệm giải trình 55) khớp hàng kia hơn. Phản "
  "thực đã được chạy: băng, tầng, bộ vòng và R_B đều giữ nguyên, Δ_norm dịch "
  "từ +0.371 xuống +0.329. Lựa chọn này gần như không tốn gì, và đó mới là "
  "lý do trung thực để thôi tranh cãi về nó.",
 ],
 stress="Dịch chuyển lao động tri thức ở 0.60 và khủng hoảng tự chủ thành "
        "hình ở 0.40, cộng cú sốc thuế quan, đưa Ψ từ 1.269 xuống 1.077 — "
        "giảm 15% mà không đổi băng. Singapore hấp thụ stress mà không dịch "
        "chuyển nhiều hơn mọi nước khác trong khu vực, trừ Brunei. Ở mốc "
        "mười lăm năm nó lùi một băng xuống Thương lượng / Mạch lạc.",
 fragile="Hai tham số làm đảo phán quyết, một trong đó (a1_mass_thresh) tắt "
         "hẳn L5 ở mức +20%. Vậy ngay cả ở đây, với tỷ lệ phổ cập được đo "
         "tốt nhất khu vực, việc vòng ấy có xuất hiện hay không vẫn xoay "
         "quanh một ngưỡng ANALYST.",
 watch=[
  "Tỷ lệ phổ cập còn leo hay đã đi ngang. Điều kiện kích hoạt L5 là một "
  "ngưỡng trên a₁, không phải trên tốc độ thay đổi của nó.",
  "Bất kỳ dịch chuyển đo được nào trong chỉ số niềm tin thể chế hay sự ưng "
  "thuận. Đây chính là quan sát mà OP2-2 nói hiện chưa tồn tại ở bất cứ đâu.",
  "Windfall AI có hiện lên trong nguồn thu chung hay ở lại với giới chủ. "
  "Engine dẫn a₆ vào G; nó đáp xuống đâu sẽ quyết định việc nó bù lại hay "
  "khoét rộng dòng rút chính danh.",
 ],
 limits="L5 là cấu trúc ít bằng chứng nhất trong lớp v2 và nó là vòng duy "
        "nhất đang chạy ở đây. Một cách đọc Singapore bỏ L5 đi thì không còn "
        "vòng nào và không còn gì để nói ngoài 'Bá quyền / Mạch lạc'.",
),

# ===========================================================================
"VN": dict(
 title="Một vòng, và nó treo trên một phán đoán",
 lede=[
  "Việt Nam đọc ra Thương lượng / Mạch lạc suốt 2027 với Ψ trên 1.0, cao thứ "
  "ba khu vực, và thuộc nhóm ít giòn nhất bộ theo OAT: chỉ một tham số trong "
  "42 làm đảo phán quyết. Đây cũng là hàng mà một lựa chọn diễn giải của tôi "
  "quyết định việc nó có hiện vòng nào hay không.",
 ],
 body=[
  "Bắt đầu từ cái chắc. Ĉ₅ là 0.19, thấp thứ hai khu vực, và điều đó quan "
  "trọng hơn vẻ ngoài vì C₅ vừa là mẫu số của tổng hợp C vừa là thừa số "
  "(1−C₅) trong Ψ. Phân mảnh thấp là lý do Ψ giữ trên 1.0 trong khi Thái "
  "Lan, với năng lực thô tương đương, nằm ở 0.32. Đại hội XIV bế mạc ngày "
  "23/1/2026 với Tô Lâm tái cử 180/180 vào Bộ Chính trị 19 người nghiêng về "
  "an ninh và tư pháp, cùng mục tiêu tăng trưởng bình quân 10%/năm cho "
  "2026–30 so với 8.0% thực đạt năm 2025. Dù là gì đi nữa, đó không phải "
  "phân mảnh.",

  "Cổng gần nhất là Ŝ₃ ở khoảng mười tám năm — dễ chịu theo chuẩn khu vực, "
  "nơi Lào đối mặt sáu năm và Campuchia tám. Ŝ₅ cách tám mươi chín năm và Ĉ₅ "
  "sáu mươi sáu. Ở mốc mười lăm năm engine vẫn đọc Cân bằng / Mạch lạc, và "
  "cùng với Brunei, Singapore, Malaysia, đó là một trong chỉ bốn cách đọc "
  "Mạch lạc còn lại trong khu vực ở chân trời đó.",

  "Giờ đến phần tranh cãi được. Vòng duy nhất đang chạy là L6, Vòng Xoáy "
  "Khả-kiến–Thu-trích, và nó bật chỉ vì tôi đặt mức tái phân bổ trú ẩn ở "
  "0.70 — trên ngưỡng kích hoạt 0.55. Con số Việt Nam đo được lại chỉ hướng "
  "ngược: khối lượng vàng thanh và xu giảm 24% so cùng kỳ ở quý I/2026 và "
  "31% ở quý II. Tôi vẫn đặt a₄ cao, vì Hội đồng Vàng Thế giới quy mức giảm "
  "đó cho ràng buộc nguồn cung trong nước với mức chênh giá nội địa mà chính "
  "họ gọi là 'eye-watering'. Đó là cầu bộc lộ qua giá vì nó không thông được "
  "qua lượng, và mức chênh của vàng vật chất so với vàng giấy chính là dự "
  "đoán thứ ba của Displacement Hypothesis. Đọc riêng khối lượng thì tín "
  "hiệu bị đảo ngược.",

  "Tôi cho rằng cách đọc ấy đúng, và tôi cũng cho rằng đó là con số dễ tranh "
  "cãi nhất trong file, nên phản thực được chạy và báo cáo: ở a₄ = 0.40, lấy "
  "theo khối lượng, L6 tắt và Việt Nam không còn vòng nào đang chạy cả. Ψ "
  "gần như không nhúc nhích (1.009 so với 1.010), băng và tầng y hệt. Vậy "
  "bất đồng ở đây không phải về tình trạng của Việt Nam năm 2027 — nó là về "
  "việc có hay không một cơ chế đang lặng lẽ chạy bên dưới.",

  "Căng thẳng cấu trúc mà engine có nêu ra là giữa mục tiêu tăng trưởng và "
  "dân số. Tỷ lệ phụ thuộc người già đã là 14.0 trong khi độ phủ hưu trí mới "
  "12.7%: sự đảo chiều đang tới trước cái thiết chế lẽ ra phải hấp thụ nó. "
  "Việc làm dễ tổn thương chiếm 51.4%. Một mục tiêu 10%/năm trên nền đó là "
  "một cam kết chạy nhanh hơn đường cong phụ thuộc, và drift d₄ của engine "
  "giả định không có phản ứng chính sách nào.",
 ],
 stress="Việt Nam có mức phơi nhiễm thuế quan cao nhất bộ — thương mại bằng "
        "190% GDP — nên cú sốc toàn khu vực được áp ở 0.70 tại đây, so với "
        "0.40–0.60 ở nơi khác. Cùng dịch chuyển lao động tri thức và đường "
        "lạm phát của chính IMF (3.3% năm 2025 lên 4.9% năm 2026 và 4.6% năm "
        "2027), Ψ rơi từ 1.009 xuống 0.811 và phán quyết giữ nguyên. Đó là "
        "mức giảm 20% hấp thụ được mà không đổi băng.",
 fragile="Một tham số làm đảo phán quyết: d3_voluntary_thresh, nó dịch chế "
         "độ điều chỉnh. Theo OAT thì đây thuộc nhóm vững nhất khu vực, chỉ "
         "sau Brunei, Malaysia và Timor-Leste, những nước không đảo trên "
         "tham số nào. Nhưng "
         "chỗ giòn thật không nằm ở tham số mà ở đầu vào a₄, và đó là một "
         "cách đọc bằng chứng chứ không phải một hệ số, nên quy trình nhạy "
         "cảm hoàn toàn không nhìn thấy nó.",
 watch=[
  "Mức chênh giá vàng trong nước, không phải khối lượng. Theo lập luận trên, "
  "chênh giá mới là tín hiệu còn khối lượng là ràng buộc cung.",
  "Mục tiêu 10% có được nêu lại, làm mềm đi, hay lặng lẽ bỏ ở kỳ đánh giá "
  "giữa nhiệm kỳ hay không.",
  "Độ phủ hưu trí. Nó là 12.7% so với tỷ lệ phụ thuộc người già 14.0; khoảng "
  "cách đó chính là thứ d₄ đang đo.",
  "Kết quả đàm phán thuế quan nói riêng, với mức phơi nhiễm thương mại 190% "
  "GDP.",
 ],
 limits="Một cách đọc Mạch lạc không phải là một cách đọc lành tính. Nó nói "
        "hệ thống đủ nhất quán bên trong để hành động, chứ không nói điều nó "
        "làm sẽ hiệu quả. Engine không có gì để nói về việc mục tiêu tăng "
        "trưởng 10% có khả thi hay không.",
),

# ===========================================================================
"MY": dict(
 title="Phân mảnh mà không thành vòng xoáy",
 lede=[
  "Malaysia đọc ra Thương lượng / Mạch lạc suốt 2027 với một vòng đang chạy, "
  "và là một trong chỉ ba chủ thể khu vực — cùng Brunei và Timor-Leste — mà "
  "không tham số "
  "nào làm đảo phán quyết định tính dưới mức nhiễu ±20% bắt buộc. Đây là "
  "cách đọc ổn định nhất bộ mà không đơn thuần là một nhà nước địa tô.",
 ],
 body=[
  "Vòng duy nhất đang chạy là L3, Bẫy Phân cực, và Ĉ₅ ở 0.71 đã vượt ngưỡng "
  "0.50. Điều đáng chú ý là thứ KHÔNG bật lên cùng nó. Phân mảnh của "
  "Malaysia vừa cao vừa mang tính cấu trúc — phân mảnh xã hội được mã hóa "
  "0.75, cao nhất ngoài Myanmar, vì đường đứt gãy là cộng đồng và được hiến "
  "định hóa chứ không phải một dao động dư luận — vậy mà các vòng chính danh "
  "và thu trích vẫn tắt.",

  "Lý do là chiều sâu hành chính và dư địa tài khóa. Ŝ₄ là 0.81, cao thứ hai "
  "khu vực sau Singapore, trên nền hiệu quả chính phủ WGI bách phân vị 72 "
  "với độ phủ an sinh gần như toàn dân. Ŝ₃ ở 0.58 là cao thứ ba ở đây. Một "
  "chủ thể có thể chia rẽ sâu sắc mà vẫn giao được hàng, và engine phân biệt "
  "hai điều đó theo cách mà một chỉ số phân cực đơn lẻ sẽ không làm được.",

  "Năm chính trị hậu thuẫn cách đọc này mà không làm nó thay đổi. Liên minh "
  "lớn của Anwar đã mất Sabah, Johor và Negeri Sembilan ở cấp bang trong khi "
  "vẫn giữ trung ương liên bang; GE16 đến hạn trước tháng 2/2028 và khả năng "
  "bầu sớm đã được cân nhắc công khai. Chương trình hợp lý hóa trợ cấp đang "
  "làm đúng cái việc mà trụ L_comply của engine nói tới — đổi chính danh "
  "hiện tại lấy củng cố tài khóa — và việc đình chỉ vụ án đối với Phó Thủ "
  "tướng nuôi cùng kênh đó. Những điều ấy cho ra khoản chiết khấu bất ổn "
  "0.14, khiêm tốn so với 0.26 của Indonesia và 0.30 của Philippines.",

  "Một điểm cấu trúc lặng lẽ: cam kết hưu trí chỉ được mã hóa 0.45, thấp hơn "
  "hẳn 0.70 của Thái Lan, vì EPF là quỹ có nguồn chứ không phải chi trả "
  "theo dòng. Hóa đơn già hóa của Malaysia rơi vào hộ gia đình, không vào "
  "ngân sách. Đó là lý do Malaysia và Thái Lan, ở những điểm đại thể tương "
  "tự trên đường cong dân số, lại cho ra bộ vòng hoàn toàn khác nhau: Thái "
  "Lan chạy L7 còn Malaysia thì không.",
 ],
 stress="GE16 như một cuộc bầu cử gây phân cực ở 0.60, cộng cú sốc thuế "
        "quan, đủ để dịch tầng: Mạch lạc thành Căng và Ψ rơi từ 0.451 xuống "
        "0.284. Đó là một trong chỉ ba lần dịch tầng của nhánh stress. "
        "Bộ vòng không đổi — L3 vốn đã là cơ chế đang chạy và cuộc bầu cử chỉ "
        "nuôi thêm nó.",
 fragile="Không tham số nào làm đảo phán quyết ở ±20%, tức là vững hết mức "
         "mà quy trình OAT có thể nói. Điểm cần dè chừng nằm ở thượng nguồn: "
         "Ĉ₅ của Malaysia cũng dựng từ ba nhánh ANALYST như mọi nước khác, và "
         "một thành phần hoàn toàn ANALYST mà tình cờ không nhạy với nhiễu "
         "tham số thì vẫn không phải là một số đo.",
 watch=[
  "GE16 có được gọi sớm không. Nhánh stress coi đó là sự kiện 2027 quyết "
  "định duy nhất với Malaysia.",
  "Thêm những thất bại cấp bang nữa. Ba lần liên tiếp là xu thế mà mã hóa "
  "party_frag đang dựa vào.",
  "Hợp lý hóa trợ cấp và áp lực chi phí sinh hoạt, đó mới là kênh chính danh "
  "đang sống, chứ không phải kênh sắc tộc.",
  "Các tranh luận về mức đủ sống của EPF — thời điểm một quỹ có nguồn bắt "
  "đầu sinh ra yêu sách ngân sách chính là thời điểm d₄ phải được mã hóa "
  "lại.",
 ],
 limits="Malaysia là hàng mà sự phân biệt giữa phân mảnh và rời rạc của "
        "engine phát huy tác dụng nhất. Cách đọc nói chia rẽ-nhưng-vận-hành-"
        "được, và đó là một phạm trù thật chứ không phải phiên bản nhẹ của "
        "khủng hoảng.",
),

# ===========================================================================
"MM": dict(
 title="Cổng đã đóng; câu hỏi là cái gì theo sau",
 lede=[
  "Myanmar là chủ thể duy nhất trong mười một nước có một cổng θ₂₅ ĐÃ ĐÓNG. "
  "Ŝ₂ nằm dưới ngưỡng PAPER 0.25 của nó, nên θ₂₅ sụp xuống 0.127 và Ψ theo "
  "đó xuống 0.008 — thấp hơn hai bậc độ lớn so với bất cứ nước nào khác "
  "trong khu vực. Pass Monte-Carlo trả về Cân bằng 100%, và đó không phải sự "
  "ổn định. Chẳng còn gì để mà biến thiên.",
 ],
 body=[
  "Cổng đã đóng là cổng bạo lực, không phải cổng tài khóa. Hai kênh của "
  "Degrow kết thúc ở cùng một đối tượng — θ₂₅ — qua hai cửa khác nhau: cửa "
  "tự nguyện, già hóa đóng Ŝ₅, còn cửa bạo lực, thanh niên đóng Ŝ₂. Thái Lan "
  "đang đi về phía cửa thứ nhất. Myanmar thì đã đi qua cửa thứ hai rồi. Ŝ₅ "
  "vẫn còn cách 106 năm và không còn liên quan.",

  "Đầu vào dẫn tới điều này là mã hóa xung đột 0.95, và cần nói chính xác nó "
  "khẳng định cái gì. Nó không phải nhận định về việc ai đang thắng. Nó là "
  "phát biểu rằng không một tác nhân nào nắm độc quyền. BTI 2026 cho rằng "
  "quyền lực của chính quyền quân sự bị tranh chấp trên hơn hai phần ba lãnh "
  "thổ, với hơn một nửa trong số 330 huyện có xung đột đang diễn ra; quyền "
  "kiểm soát ổn định của Tatmadaw được ước ở khoảng 72 đến 220 huyện tính "
  "tới tháng 12/2025; Quân đội Arakan nắm phần lớn Rakhine; ba bộ tư lệnh "
  "vùng đã thất thủ. Cuộc bầu cử phân đợt tháng 12/2025 thay đổi tuyên bố "
  "pháp lý về quyền lực, chứ không thay đổi bản đồ kiểm soát.",

  "Độ thâm nhập hành chính là 0.089 và chính danh 0.139 — cả hai thực tế đã "
  "ở sàn mô hình sau nén biên. Ba vòng đang chạy (L2, L3, L6) nhưng bộ vòng "
  "gần như không còn ý nghĩa: với θ₂₅ ở 0.127, Ψ không thể hồi phục qua bất "
  "cứ kênh nào mà các vòng ấy vận hành.",

  "Có một kết quả âm tính cần nêu rõ, vì hàng này được dựng để kiểm đúng "
  "điều đó. **L8, Xả áp Thanh niên Dư thừa, KHÔNG bật.** L8 tồn tại để công "
  "cụ có thể đọc được các xã hội trẻ, và Myanmar là ứng viên hiển nhiên. "
  "Nhưng d₅ tính ra 0.495, dưới ngưỡng kích hoạt, vì các chỉ báo thanh niên "
  "đo được của Myanmar — NEET 15.0%, phụ thuộc trẻ 35.2 — chỉ ở mức trung "
  "bình theo chuẩn khu vực; Lào và Timor-Leste đều cao hơn hẳn. Engine đang "
  "nói rằng thảm họa của Myanmar không mang tính dân số. Đó là một sự sụp đổ "
  "độc quyền cưỡng chế tình cờ diễn ra ở một nước trẻ, và cơ chế dư thừa "
  "thanh niên không phải thứ đang dẫn dắt nó. Cách đọc đó đúng hay chỉ là "
  "giả tạo do ngưỡng d₅ thì vẫn là câu hỏi mở, và `d5_violent_thresh` là một "
  "trong hai tham số làm đảo phán quyết này.",
 ],
 stress="Thất bại hệ thống cứu trợ và một cú vỡ tiền tệ nữa — lạm phát 22% "
        "năm 2025 là nền baseline — đưa Ψ từ 0.008 xuống 0.007. Nhánh stress "
        "gần như vô nghĩa ở đây, và cố ý như vậy: xung đột dân sự KHÔNG được "
        "thêm vào như một sự kiện, bởi mức xung đột 0.95 đã nói hết những gì "
        "cần nói, và thêm nữa là tính cuộc đảo chính hai lần.",
 fragile="Hai tham số làm đảo phán quyết, và một trong đó là ngưỡng d₅ quyết "
         "định câu hỏi L8 ở trên. Giới hạn sâu hơn nằm ở dữ liệu: chuỗi tài "
         "khóa của Myanmar yếu nhất bộ — quan sát thuế trên GDP dùng được "
         "cuối cùng là năm 2019, trước đảo chính — nên mọi cách đọc tài khóa "
         "ở đây thừa hưởng một nền bảy năm tuổi.",
 watch=[
  "Số huyện bị kiểm soát, không phải phần trăm lãnh thổ. Ŝ₂ nói về độc "
  "quyền, và chuỗi số huyện là thứ quan sát được gần nhất.",
  "Chính quyền hậu bầu cử có mở rộng được dịch vụ công thật sự ở đâu không. "
  "Ŝ₄ ở 0.089 là sàn, và nó là biến có dư địa dịch chuyển trước nhất.",
  "Đồng kyat và lạm phát. 22% năm 2025 với a₄ ở 0.78 là cơ sở thu trích đang "
  "biến mất theo thời gian thực.",
  "Huy động thanh niên có trở thành động lực độc lập hay không — câu hỏi L8 "
  "mà engine hiện trả lời là 'không'.",
 ],
 limits="Băng Cân bằng ở đây là sản phẩm toán học của việc Δ_norm nhỏ vì CẢ "
        "HAI vế S và C đều đã sụp, chứ không phải một phát biểu rằng có gì "
        "đó đang cân bằng. Hãy đọc tầng và θ₂₅, đừng đọc băng.",
),

# ===========================================================================
"KH": dict(
 title="Không vòng nào chạy, mà ngòi thì ngắn nhì khu vực",
 lede=[
  "Campuchia đọc ra Cân bằng / Mạch lạc suốt 2027 với không một vòng nào "
  "đang chạy — vậy mà cổng Ŝ₃ của nó chỉ còn tám năm, ngắn thứ hai khu vực, "
  "và cách đọc mười lăm năm là Khủng hoảng / Rời rạc. Đây là khoảng cách lớn "
  "nhất bộ giữa vẻ yên ổn hiện tại của một chủ thể và chỗ mà các drift của "
  "nó chỉ tới.",
 ],
 body=[
  "Việc không có vòng nào là thật, không phải sơ sót. L1 không bật vì độc "
  "quyền cưỡng chế còn nguyên; L3 không bật vì phân mảnh ở 0.22, thuộc hàng "
  "thấp nhất ở đây — phe đối lập đã bị dỡ bỏ, nên còn rất ít thứ để mà phân "
  "mảnh; L6 không bật vì tái phân bổ trú ẩn ở 0.42, dưới ngưỡng 0.55, bất "
  "chấp độ siết thu trích +0.202. Một chủ thể có thể ở trong tình trạng cấu "
  "trúc tệ mà vẫn không hiện phản hồi nào đang chạy, và Campuchia là ví dụ "
  "rõ nhất khu vực.",

  "Thứ engine có ghi nhận là mức tập trung tư bản. Ĉ₁ là 0.63 với mã hóa "
  "thân hữu 0.90, cao nhất bộ, và chỉ số tham nhũng chính trị của V-Dem ở "
  "0.904 là tệ thứ hai trong mười một nước. Hệ thống oknha gắn giấy phép với "
  "bảo trợ một cách trực tiếp. Chinn-Ito cho độ mở tài khoản vốn bằng 1.00 — "
  "mở hoàn toàn về mặt pháp lý, nên kiểm soát vốn bằng không — trong một nền "
  "kinh tế đô-la hóa. Tư bản tập trung với lối ra không vật cản là một cấu "
  "hình engine theo dõi, và đó là lý do ngưỡng vốn của L4 là một trong hai "
  "tham số làm đảo phán quyết này.",

  "Mã hóa xung đột 0.22 khác không vì một lý do mà chuỗi xung đột theo nhà "
  "nước sẽ bỏ sót. Các khu phức hợp lừa đảo có vũ trang, hoạt động xuyên "
  "biên giới và — theo lời chính Thủ tướng hồi tháng 2/2026 — đang phá hủy "
  "nền kinh tế hợp pháp; một ước tính của US Institute of Peace đặt doanh "
  "thu trên 12,5 tỷ USD mỗi năm, điều ông bác bỏ. Một chiến dịch bảy tháng "
  "được báo cáo đã bắt 5.106 người và trục xuất 4.534. Dù con số thật là bao "
  "nhiêu, một nền kinh tế song song có vũ trang hoạt động bên trong lãnh thổ "
  "vẫn là một đối thủ của độc quyền cưỡng chế, và đó đúng là thứ Ŝ₂ đo.",

  "Áp lực bên ngoài được mã hóa 0.58, cao thứ hai ở đây sau Myanmar, và đó "
  "là biên giới Thái Lan: hai đợt giao tranh năm 2025, lệnh ngừng bắn ngày "
  "27/12 mà Stratfor đánh giá hồi tháng 8/2026 là đang trụ nhưng không bình "
  "thường hóa, và quân Thái đóng trên phần đất Phnom Penh gọi là bị chiếm.",
 ],
 stress="Campuchia cho ra kết quả thực sự phản trực giác duy nhất của cả lần "
        "chạy: dưới nhánh stress, Ψ TĂNG, từ 0.749 lên 0.842. Nguyên nhân là "
        "cách catalogue mã hóa interstate_war_onset, vốn NÂNG Ŝ₂ và Ŝ₃ — hiệu "
        "ứng rally mà sccd Part V ghi nhận cho giai đoạn 1941–45. Một cuộc "
        "leo thang biên giới, theo chính logic của engine, củng cố một nhà "
        "nước bảo trợ trong ngắn hạn. Đó là cách đọc của engine chứ không "
        "phải của tôi, và đúng là loại kết quả đáng để lộ ra thay vì làm mờ "
        "đi.",
 fragile="Hai tham số làm đảo phán quyết. Điểm yếu đầu vào ở đây sắc hơn "
         "điểm yếu tham số: Campuchia không có quan sát Gini nào của WDI "
         "trong cửa sổ 2012–2026, nên số hạng tập trung tư bản dùng một con "
         "số lập luận 30.5 mà gần như chắc chắn là sàn — Gini tiêu dùng đánh "
         "giá thấp nghiêm trọng mức tập trung ở nơi mà đỉnh phân phối nằm "
         "trong khu vực phi chính thức.",
 watch=[
  "Đường Ŝ₃. Tám năm tới sàn 0.30 là ngòi ngắn thứ hai khu vực và chưa có gì "
  "trong cách đọc 2027 phản ánh điều đó.",
  "Việc thực thi với nền kinh tế lừa đảo, và cụ thể là nó có chạm tới tầng "
  "bảo trợ hay chỉ dừng ở mức bắt-và-trục-xuất.",
  "Bình thường hóa biên giới so với trạng thái đóng băng hiện nay. Engine "
  "nói leo thang có lợi trong ngắn hạn; nó không nói gì tử tế về trung hạn.",
  "Bất cứ dấu hiệu nào của dòng vốn ra. Độ mở là 1.00 và mức tập trung thì "
  "cao; không có ma sát nào cản đường.",
 ],
 limits="Mạch lạc ở đây nghĩa là nhà nước có thể hành động nhất quán, mà "
        "trong một hệ thống bảo trợ thì điều đó bao gồm cả hành động nhất "
        "quán vì lợi ích của chính nó. Tầng không phải một điểm đánh giá "
        "thành tích.",
),

# ===========================================================================
"LA": dict(
 title="Sáu năm tới sàn chính danh",
 lede=[
  "Lào có ngòi ngắn nhất khu vực: Ŝ₃ chạm sàn PAPER 0.30 trong khoảng sáu "
  "năm theo các drift hiện tại. Nó đọc ra Cân bằng / Mạch lạc suốt 2027 với "
  "một vòng đang chạy, và chế độ là ĐIỀU CHỈNH BẠO LỰC PHƠI NHIỄM — một "
  "trong chỉ hai chủ thể ở nhóm đó. Ở mốc mười lăm năm, cách đọc là Khủng "
  "hoảng / Rời rạc.",
 ],
 body=[
  "Đây là ca L6 rõ nhất khu vực chỉ trên số liệu đo được, cần ít công diễn "
  "giải nhất. Bản Điều IV tháng 2/2026 của IMF gọi nợ công là không bền vững "
  "và nước này đang trong tình trạng kiệt quệ nợ cả đối ngoại lẫn tổng thể — "
  "dù tỷ lệ nợ trên GDP đang giảm, từ 80.6% năm 2025 xuống dự kiến 68.6% vào "
  "2027. Lạm phát quay lại quanh 10% vào tháng 4/2026 sau hai đợt trên 20% "
  "trong vòng bốn năm. Bản tuyên bố môi trường đầu tư 2026 của Bộ Ngoại giao "
  "Mỹ cho rằng số liệu IMF tính thiếu các nghĩa vụ với Trung Quốc.",

  "Đối lại, an sinh xã hội phủ 2.2% dân số và hưu trí phủ 2.2%. Về cơ bản "
  "không có đệm nào giữa một hộ gia đình và một cú sốc giá. Chính sự kết hợp "
  "đó — một nhà nước dưới áp lực thu trích và những hộ gia đình không có bảo "
  "vệ thể chế — là lý do tái phân bổ trú ẩn được mã hóa 0.58, trên ngưỡng "
  "L6. Hai đợt lạm phát 20–30% trong bốn năm dạy cho một hộ gia đình biết "
  "đồng kip đáng giá bao nhiêu, và phản ứng là giữ thứ khác.",

  "Chế độ điều chỉnh là điều thứ hai cần để ý. Lào dẫn áp lực điều chỉnh của "
  "mình xuống kênh bạo lực vì d₃, quyền tự chủ điều chỉnh, là 0.19 — thấp "
  "thứ hai khu vực. Biến đó là bộ định tuyến: nó đo sự sẵn có và mức sử dụng "
  "các công cụ tự nguyện, tránh thai và hoạch định tài chính và việc phúc "
  "lợi thay thế chỗ dựa tuổi già. Ở đâu những thứ đó vắng mặt, mô hình của "
  "Degrow nói áp lực xả theo lối cổ. Tải trọng d₁ của Lào là 0.84 và dư thừa "
  "thanh niên d₅ là 0.80, cả hai đều thuộc hàng cao nhất ở đây.",

  "Khoản chiết khấu bất ổn được đặt 0.10 chứ không phải 0, và lý do đáng nói "
  "vì nó không hiển nhiên: ở Lào không có kênh biểu tình, nên khoản rút "
  "chính danh không nổi lên thành bất ổn nhìn thấy được. Nó nổi lên thành "
  "lối thoát và phi chính thức hóa. Việc làm dễ tổn thương là 76.4%, cao "
  "nhất khu vực với khoảng cách rất xa.",
 ],
 stress="Một sự kiện nợ trên những nghĩa vụ mà IMF vốn đã gọi là không bền "
        "vững, cộng lạm phát trở lại trên 10%, đưa Ψ từ 0.721 xuống 0.608 mà "
        "không dịch phán quyết. Lào có nhiều sức hấp thụ ngắn hạn hơn các "
        "nền tảng của nó gợi ý, chủ yếu vì phân mảnh rất thấp (Ĉ₅ = 0.19) và "
        "Ψ mang thừa số (1−C₅).",
 fragile="Một tham số làm đảo phán quyết: a4_flight_thresh, nó tắt L6. Vậy "
         "cơ chế duy nhất mà engine nhận diện cho Lào đứng trên một ngưỡng "
         "ANALYST. Tình trạng kiệt quệ tài khóa đo được thì không phải điều "
         "bàn cãi; việc nó có biểu hiện cụ thể thành vòng xoáy khả-kiến hay "
         "không thì có.",
 watch=[
  "Lạm phát. Nó vừa là độ siết thu trích vừa là động lực trú ẩn, và là con "
  "số được công bố thường xuyên nhất mà Lào tạo ra.",
  "Bất kỳ đợt tái cơ cấu nào với khoản nợ Trung Quốc nắm giữ, và điều khoản "
  "có được công khai không. Khẳng định của Bộ Ngoại giao Mỹ rằng các nghĩa "
  "vụ bị tính thiếu là ẩn số lớn nhất của hàng này.",
  "Độ phủ an sinh trên nền 2.2%. Dịch chuyển ở đây sẽ là thay đổi gánh vác "
  "nhiều nhất mà nhà nước Lào có thể làm.",
  "Dòng lao động sang Thái Lan. Gradient nhân tài của engine chấm LA→TH là "
  "cặp mạnh nhất khu vực.",
 ],
 limits="Tầng Mạch lạc ở 2027 đi kèm cổng Ŝ₃ sáu năm không phải mâu thuẫn — "
        "đó là engine phân biệt sự nhất quán hiện tại với hướng đi. Chỉ đọc "
        "băng 2027 thì bỏ lỡ toàn bộ câu chuyện Lào.",
),

# ===========================================================================
"TL": dict(
 title="Tự do nhất và nghèo nhất, trong cùng một hàng",
 lede=[
  "Timor-Leste đọc ra Thương lượng / Mạch lạc suốt 2027 với không vòng nào "
  "đang chạy, và không tham số nào làm đảo phán quyết ở ±20%. Nó cũng mang "
  "tải trọng sức chứa cao nhất khu vực (d₁ = 0.91), điểm dư thừa thanh niên "
  "cao thứ hai (d₅ = 0.79), và độ siết thu trích lớn nhất trong cả mười một "
  "nước (+0.580). Những thứ đó nằm cạnh nhau, và chính sự đi kèm ấy mới là "
  "điểm mấu chốt.",
 ],
 body=[
  "Trên mọi thước đo dân sự, Timor-Leste dẫn đầu khu vực một cách dứt khoát. "
  "RSF xếp nó thứ 30 trên 180 năm 2026 — trước mọi thành viên ASEAN khác và "
  "phần lớn châu Âu — và điểm dân chủ tự do 0.549 của V-Dem gần gấp đôi "
  "Indonesia. Tổ chức dân sự đọc ra 0.73 và tự chủ thông tin 0.68, cả hai "
  "đều cao nhất ở đây. Nước này gia nhập ASEAN với tư cách thành viên thứ "
  "mười một ngày 26/10/2025.",

  "Nó cũng nghèo nhất với khoảng cách rất xa, 4.810 USD PPP đầu người, với "
  "NEET 29.1% và phụ thuộc trẻ 53.7 — cao nhất khu vực. Sự kết hợp đó, Ĉ₂ và "
  "Ĉ₃ cao với Ŝ₁ thấp và d₅ cao, không phải mâu thuẫn trong mô hình. Nó là "
  "một cấu hình cụ thể và dễ nhận ra: một nhà nước có năng lực dân sự thật "
  "sự và rất ít năng lực tài khóa, đang gánh một dân số trẻ mà nó chưa tạo "
  "được việc làm cho.",

  "Dữ kiện ràng buộc là Quỹ Dầu khí, chứ không phải thuế, nuôi bộ máy nhà "
  "nước. Chi tiêu chạy gần 60% GDP so với nguồn thu nội địa khoảng 22%, được "
  "tài trợ bằng các khoản rút từ Quỹ vượt mức Thu nhập Bền vững Ước tính. "
  "Chính điều đó tạo ra độ siết thu trích lớn nhất bộ: đòi 0.628 so với khả "
  "thi 0.048. Vậy mà L6 không bật, vì điều kiện thứ hai không thỏa — tái "
  "phân bổ trú ẩn là 0.20, thấp nhất trong mười một nước. Độ siết là thật và "
  "phản ứng khả-kiến thì vắng mặt.",

  "Việc không bật ấy là kết quả đơn lẻ đáng học nhất của hàng Timor-Leste, "
  "và nó cắt về cả hai phía. Đọc rộng lượng, nó nói rằng kiểu tháo chạy của "
  "hộ gia đình sang các kho giá trị không khả kiến như ở Lào chưa bắt đầu ở "
  "đây. Đọc hoài nghi, nó nói rằng a₄ = 0.20 là ước lượng của nhà phân tích "
  "cho một nước hoàn toàn không có dữ liệu WGC, và engine đang báo cáo sự "
  "vắng mặt của một con số như thể là sự vắng mặt của một hiện tượng.",

  "Chế độ điều chỉnh là ĐIỀU CHỈNH BẠO LỰC PHƠI NHIỄM, giống Lào, và vì cùng "
  "một lý do cấu trúc: d₃ là 0.15, thấp nhất khu vực, nên áp lực dẫn xuống "
  "kênh cổ. Tỷ lệ dùng biện pháp tránh thai hiện đại là 24.1%, so với 70.7% "
  "ở Thái Lan.",
 ],
 stress="Rút Quỹ Dầu khí vượt ESI, cộng một cú sốc việc làm thanh niên trên "
        "nền NEET 29.1%, đưa Ψ từ 0.826 xuống 0.621 — giảm 25%, mức sụt theo "
        "tỷ lệ lớn thứ tư khu vực sau Thái Lan, Philippines và Malaysia — "
        "mà không dịch phán "
        "quyết. Ở mốc mười lăm năm, cách đọc là Cân bằng / Rời rạc.",
 fragile="Không tham số nào làm đảo phán quyết ở ±20%, nhưng sự vững chãi đó "
         "gây hiểu nhầm ở đây, vì chất lượng đầu vào là yếu nhất bộ. "
         "Timor-Leste không có quan sát Chinn-Ito, không có dữ liệu vàng "
         "WGC, không có chuỗi tránh thai sau 2016, và Ŝ₁ của nó dựng trên con "
         "số thuế trên GDP năm 2022 vốn vừa thổi phồng NĂNG LỰC thu trích "
         "vừa đánh giá thấp nguồn lực hiện có, bởi khoản chuyển từ Quỹ không "
         "phải là thuế.",
 watch=[
  "Tốc độ rút Quỹ Dầu khí so với ESI. Đây là toàn bộ Ŝ₁ và Ŝ₅ của chủ thể "
  "này và gần như không còn gì khác.",
  "Có hình thành được cơ sở thu nội địa ngoài dầu hay không. Gia nhập ASEAN "
  "là phương tiện hiển nhiên và đồng hồ cho việc đó thì dài.",
  "Việc làm cho thanh niên trên nền NEET 29.1%, đó là thứ d₅ đang đọc.",
  "Bất kỳ dấu hiệu nào của hộ gia đình tái phân bổ sang vàng hoặc ngoại tệ. "
  "a₄ = 0.20 là ước lượng, và L6 bật lên sẽ thay đổi hoàn toàn hàng này.",
 ],
 limits="Trọng số hệ thống nhỏ nhất bộ (0.0013) nghĩa là Timor-Leste đóng "
        "góp gần như không gì vào Ψ_G. Đó là phát biểu về tỷ trọng GDP và "
        "không gì khác; cách đọc từng chủ thể vẫn đứng độc lập.",
),

# ===========================================================================
"BN": dict(
 title="Chùng, và cách chỗ không còn chùng đúng một mặt hàng",
 lede=[
  "Brunei ghi Ψ cao nhất khu vực ở 1.65, đọc ra Bá quyền / Mạch lạc với "
  "không vòng nào đang chạy, và cổng gần nhất cách 126 năm. Chế độ điều chỉnh "
  "của nó là CHÙNG — chủ thể duy nhất trong mười một nước ở nhóm đó, nghĩa "
  "là engine không tìm thấy áp lực điều chỉnh nào cần xả cả. Đây cũng là "
  "hàng mà một sự kiện làm đổi chế độ.",
 ],
 body=[
  "Các con số đúng là thứ một chế độ quân chủ địa tô hydrocarbon tạo ra. Thu "
  "trích tài khóa đọc ra 0.81 và độc quyền cưỡng chế 0.90, cả hai đều cao "
  "nhất hoặc gần nhất ở đây, trên nền ổn định chính trị WGI bách phân vị 92. "
  "Phân mảnh là 0.12, thấp nhất trong mười một nước — không có cơ quan lập "
  "pháp để mà phân mảnh, không có đảng hợp pháp, và tình trạng khẩn cấp liên "
  "tục từ 1962. Chính danh đọc ra 0.75, chỉ sau Singapore.",

  "Tập trung tư bản được mã hóa 0.46 với hệ số thân hữu 0.70, và lý do khác "
  "hẳn mọi nơi còn lại trong bộ. Đó không phải vận động hành lang — không có "
  "sổ đăng ký và không có cơ chế — đó là sự hợp nhất. Hoàng gia, quỹ đầu tư "
  "quốc gia và nhà nước không phải những thực thể tách rời được, và đó là "
  "cấu trúc tư-bản-được-chính-trị-hóa ở dạng thuần khiết nhất. Proxy của "
  "engine vốn thiết kế cho sổ đăng ký vận động hành lang nên không vừa; con "
  "số này là lập luận.",

  "Chỗ phơi nhiễm nằm ở Ŝ₁ và Ŝ₅, và engine cho thấy nó mà không bật vòng "
  "nào. Độ siết thu trích là +0.285 — đòi 0.322 so với khả thi 0.037 — tức "
  "cùng khoảng với Thái Lan và Philippines. L6 không bật chỉ vì tái phân bổ "
  "trú ẩn là 0.25, thấp hơn nhiều so với ngưỡng. Vậy áp lực tài khóa thì có "
  "mặt còn phản ứng khả-kiến thì không: một nhà nước địa tô đâu cần đuổi "
  "theo một cơ sở thuế đang biến mất, bởi nó chưa từng đánh thuế trên cơ sở "
  "ấy.",

  "Điểm dễ tổn thương là đơn-hàng-hóa và nó hiện ra ở con số tăng trưởng chứ "
  "không ở bất kỳ số hạng cấu trúc nào. Tăng trưởng GDP 2025 là 0.7% — thấp "
  "nhất khu vực với khoảng cách rất xa, trong một năm Việt Nam đạt 8.0% và "
  "Timor-Leste 7.0% — trên nền các mỏ đang già đi. Vấn đề của Brunei không "
  "phải phân cực, chính danh hay năng lực cưỡng chế. Vấn đề là một mức giá "
  "duy nhất quyết định toàn bộ phía nguồn thu, và từ vựng cấu trúc của "
  "engine không có số hạng nào cho điều đó.",
 ],
 stress="Một cú sốc giá năng lượng ở 0.60 làm chế độ điều chỉnh chuyển từ "
        "CHÙNG sang TỰ NGUYỆN — lần đổi chế độ duy nhất trong cả nhánh "
        "stress. Ψ gần như không nhúc nhích (1.651 xuống 1.613) và băng với "
        "tầng đều giữ. Engine đang nói một điều khá chính xác: một cú hụt giá "
        "dầu không đe dọa cấu trúc Brunei, nó chấm dứt cái tình trạng không "
        "hề có áp lực điều chỉnh. Với một nhà nước chưa từng phải chạy một "
        "cuộc điều chỉnh nào, bước chuyển đó mới là thứ cần theo dõi, chứ "
        "không phải mức Ψ.",
 fragile="Không tham số nào làm đảo phán quyết, như Malaysia và Timor-Leste. "
         "Điểm yếu "
         "thật là độ phủ đầu vào: Brunei hoàn toàn vắng mặt khỏi V-Dem và "
         "khỏi Chinn-Ito, nên sáu trường của nó — năm thành phần V-Dem cộng "
         "độ mở tài khoản vốn — là các giá trị thay thế của nhà phân tích có "
         "kèm lý do, chứ không phải quan sát. Không chủ thể nào khác trong bộ "
         "có nhiều như vậy.",
 watch=[
  "Sản lượng và giá hydrocarbon. Theo cách đọc này, chúng thực tế là toàn bộ "
  "biến năng lực nhà nước của Brunei.",
  "Có xuất hiện công cụ thu ngoài hydrocarbon nào không. Brunei không có "
  "thuế thu nhập; tạo ra một sắc thuế như vậy sẽ là thay đổi cấu trúc lớn "
  "nhất có thể và sẽ hiện ngay vào Ŝ₁.",
  "Mức rút quỹ đầu tư quốc gia, đó là câu chuyện Ŝ₅ và nó không được công bố "
  "ở dạng engine đọc được.",
  "Bước chuyển CHÙNG sang TỰ NGUYỆN trong nhánh stress có xảy ra trong thực "
  "tế không — đó là một dự đoán có thể bác bỏ được, điều hiếm thấy ở engine "
  "này.",
 ],
 limits="Bá quyền / Mạch lạc với Ψ ở 1.65 là cách đọc mạnh nhất khu vực, và "
        "nên hiểu nó như một phát biểu về sự nhất quán cấu trúc, không phải "
        "về sức chống chịu. Engine không có số hạng giá hàng hóa nào, và với "
        "chủ thể này thì đó là thiếu sót chính.",
),
}

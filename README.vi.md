# SCCD-X Engine v2.00

Engine cấu trúc định tính cho chính trị thế giới. Nó lấy `sccd` v1.00 —
**Sovereign-Civilian Capacity Dynamics** (Vi Nhật Sơn, Phần I–V) — rồi cắm hai
khối cưỡng bức vào đúng hai số hạng mà v1.00 để ngoại sinh.

**[English README](README.md)** ·
**[Hướng dẫn đầy đủ](docs/GUIDE.vi.md)** ·
**[Đợt chạy ASEAN 2027](#đợt-chạy-asean-2027)** ·
**[Giới hạn, nói thẳng](#giới-hạn-nói-thẳng--đọc-phần-này-trước)**

```bash
pip install numpy          # scipy không bắt buộc nhưng nên có; xem "Bộ giải"
python serve.py            # → http://127.0.0.1:8777
python validate2.py        # 119 kiểm tra
```

---

## Nó làm gì

`sccd` v1.00 mô hình một quốc gia bằng mười thành phần năng lực, và để **hai**
số hạng của chính hệ ODE của nó hoàn toàn ngoại sinh:

```
dS₃/dt = **S₃_natural**    − ρ_b(1−λ/λmax)² − ζ·C₅^ψ·(S₃−S₃floor)
dC₅/dt = **C₅_structural** + ε_p·C₅(1−C₅)·RevPol + η·C₅²·C₃ + ξ·Ĉ₄Ĉ₁(1−C₅)
```

Hai số hạng có dấu sao đó là cái lỗ lớn nhất của engine. Chúng định độ trôi của
hai biến điều khiển toàn bộ phần lõi phi tuyến — S₃ dẫn λ, mà λ nhân vào **toàn
bộ** S; C₅ vừa là mẫu số của C **vừa** là thừa số (1−C₅) trong Ψ — và v1.00
không nói gì về cả hai.

v2.00 lấp chúng bằng hai bài báo nữa của cùng tác giả:

| Khối | Bài báo | Thang thời gian | Nhãn |
|---|---|---|---|
| **D** | *The Wheel of Fate: Từ "bẫy thịnh vượng" cổ đại tới khủng hoảng sinh sản hiện đại* | nhân khẩu | `DEGROW` |
| **A** | *The Displacement Hypothesis*, tái bản lần 2 | tốc độ nhận AI | `DISPL` |

Cả hai bài đi kèm repo: [`docs/Degrow.pdf`](docs/Degrow.pdf) và
[`docs/The_Displacement_Hypothesis_v2.pdf`](docs/The_Displacement_Hypothesis_v2.pdf).

Khối D là một **bộ định tuyến**, không phải thêm một áp lực nữa. Một lượng áp
lực điều chỉnh được sinh ra bởi tải; cái mà bài báo thực sự thay đổi là *kênh
nào gánh nó*, và biến phân luồng là độ sẵn có của các công cụ tự nguyện:

```
violent_share = (1 − d₃)^route_sharpness
```

---

## Hai ngôn ngữ, tách biệt thật sự

Trang có cặp tab `VI` / `EN`. Bấm `VI` thì mọi thứ là tiếng Việt — khung trang,
chi tiết vòng lặp, nghĩa của các cổng, cảnh báo hiệu chỉnh, phần tự sự, cả tab
nguồn gốc. Bấm `EN` thì mọi thứ là tiếng Anh.

Không có chế độ song ngữ, và không có trạng thái dịch nửa vời. Điều này được
**cưỡng chế**, không phải chỉ hứa:

- 406 template phải có cả hai mặt, nếu không `validate2.py` fail
- 160 chuỗi UI phải có cả hai mặt
- thiếu một khoá i18n thì **ném lỗi**, chứ không âm thầm trả về tiếng Anh
- `web/index.html` phải chứa **không một** ký tự tiếng Việt nào — trang chỉ là
  bộ render, mọi chuỗi đến từ API
- đổi ngôn ngữ thì **chạy lại chẩn đoán** ở server, chứ không dịch trong trình
  duyệt

Kết quả số được khẳng định là **giống hệt nhau** giữa hai ngôn ngữ: cùng quỹ
đạo, cùng phán quyết độ mong manh.

---

## Dùng nhanh

```bash
git clone https://github.com/vinhatson/sccdx-engine.git
cd sccdx-engine
pip install numpy

python serve.py                    # giao diện web tại http://127.0.0.1:8777
python validate2.py                # 119 kiểm tra cấu trúc
python validate_v1.py              # báo cáo các bất nhất của v1
python sea2027/run.py              # mười một quốc gia ASEAN (tiếng Việt)
```

Python 3.9+. `numpy` là thứ duy nhất bắt buộc.

### Hoặc không cần cài gì cả

```bash
docker run --rm -p 7860:7860 vinhatson/sccdx-engine   # → http://127.0.0.1:7860
```

Image đã xuất bản có sẵn `scipy`, nên nó chạy đúng bộ giải stiff thích nghi mà
Phần IV §8.1 yêu cầu, không phải bản dự phòng DP45. Nó cũng chạy `validate2.py`
ngay trong bước build, nghĩa là một image tồn tại đồng nghĩa với engine bên trong
đã qua đủ 119 kiểm tra của chính nó.

### API HTTP

`serve.py` là server chính và không cần gì ngoài `numpy`.

```bash
curl http://127.0.0.1:8777/api/v2/health
curl "http://127.0.0.1:8777/api/v2/presets?lang=vi"
curl "http://127.0.0.1:8777/api/v2/schema?lang=vi"
curl "http://127.0.0.1:8777/api/v2/events?lang=vi"
curl "http://127.0.0.1:8777/api/v2/audit?lang=vi"

curl -X POST http://127.0.0.1:8777/api/v2/diagnose \
     -H "Content-Type: application/json" -d '{"lang":"vi"}'
```

Mọi endpoint tham chiếu nhận `?lang=vi|en`. `POST /api/v2/diagnose` trả về phán
quyết, năng lực, cưỡng bức, vòng lặp, phân nhánh, điểm hút, quỹ đạo, phán quyết
theo chân trời, độ bất định và độ mong manh.

Chạy [`api_fastapi.py`](api_fastapi.py) nếu bạn muốn tài liệu OpenAPI và một ứng
dụng ASGI — bản đó cần `fastapi` và `uvicorn`.

---

## Đợt chạy ASEAN 2027

[`sea2027/`](sea2027/) là một ứng dụng hoàn chỉnh: cả mười một quốc gia ASEAN
đi qua engine, dữ liệu lấy ngày 2026-10-09.

```bash
python sea2027/run.py                                 # tiếng Việt
python sea2027/run.py --lang en --json out.json       # tiếng Anh + dump đầy đủ
python sea2027/make_pdf.py                            # 22 PDF kỹ thuật
python sea2027/make_prose_pdf.py                      # 22 PDF văn xuôi
```

Nó kèm sẵn 44 PDF dựng trước, chia hai bộ, và **sự khác nhau giữa hai bộ là
quan trọng**:

- [`sea2027/pdf/`](sea2027/pdf/) — **output của dụng cụ đo**: bảng, nhãn nguồn
  gốc từng thành phần, các dòng OAT, phóng chiếu cổng, quỹ đạo. Mỗi bản 5–6
  trang, 11 quốc gia × 2 ngôn ngữ.
- [`sea2027/pdf_prose/`](sea2027/pdf_prose/) — **lập luận về việc output đó
  nghĩa là gì**. Mỗi bản 2 trang, ~20.000 từ cho cả 22 bản, có một dải hình ở
  đầu để mọi khẳng định đều đối chiếu được với đợt chạy đã sinh ra nó.

Cách chia này là đúng cái kỷ luật mà engine giữ ở bên trong: **engine phát ra mã
và không bao giờ phát ra một câu văn**, còn văn xuôi sống ở một chỗ duy nhất, nơi
nó kiểm toán được. `prose_en.py` và `prose_vi.py` là **DIỄN GIẢI** và nói rõ điều
đó trên mọi tài liệu. Phần tiếng Việt được **viết**, không phải dịch.

---

## Giới hạn, nói thẳng — đọc phần này trước

Đây là phần phải đọc trước khi trích bất kỳ con số nào từ engine này.

**Các output của v2 là THỨ TỰ. Chúng là một bảng xếp hạng và một bản đồ vượt
ngưỡng, không phải một mức.** Chính engine nói ra điều đó ở cuối mỗi đợt kiểm
tra:

```
36 trong 83 tham số v1 mang giá trị từ bài báo gốc; 46 cái thì không.
TOÀN BỘ 46 tham số v2 đều là ANALYST hoặc DERIVED2 — hai bài báo mới là
định tính và không nêu hệ số nào.
```

Đó không phải lời rào đón gắn thêm vào sau; đó là lý do mọi trường dẫn xuất đều
mang một nhãn nguồn gốc mà bạn soi được, và là lý do `python validate_v1.py` tồn
tại để **in ra** các bất nhất của chính mô hình v1 thay vì vá chúng trong im
lặng. Bốn trong số đó ở mức `CRITICAL`, và engine **tái tạo chúng một cách trung
thực** thay vì sửa ngầm:

- **INC-7** — trong `dC₅/dt`, cả ba số hạng nội sinh đều **dương** và không có
  số hạng giảm phân cực, nên C₅ tăng đơn điệu về 1 với **mọi** quỹ đạo, do đó
  Ψ → 0 bất kể kịch bản nào.
- **INC-8** — trong `dS₃/dt`, cả hai số hạng nội sinh đều **âm**, nên S₃ chỉ có
  thể suy giảm, và mô hình không thể sinh ra sự **tái lập tính chính danh** mà
  Phần V ghi lại cho giai đoạn 1980–86.
- **INC-9** — Phần IV §2.1 viết hẳn một phương trình `dC₁/dt`, nhưng §7.1 lại
  **bỏ C₁** khỏi vector trạng thái. Với C₁ ngoại sinh thì trong hệ phi tuyến
  **không có vòng phản hồi kín nào cả**. (`simulate(..., c1_dynamic=True)` nâng
  C₁ thành biến trạng thái thứ năm.)

`validate2.py` báo các cái này là `KNOWN-DEFECT`, **không** phải failure: chúng
ghi lại rằng engine tái tạo trung thực một khuyết tật mà
`sccd.spec.KNOWN_INCONSISTENCIES` đã ghi nhận. Con số `KNOWN-DEFECT` bằng 4 là
kết quả **đúng và mong đợi**.

**Riêng về đợt chạy ASEAN:** `judgment.py` là một lớp phủ **ANALYST** công khai
— một khối cho mỗi quốc gia, mọi con số đều được lập luận tại chỗ. Nó là một
phán đoán, nó **được dán nhãn** là phán đoán, và bạn nên phản biện nó một cách
công khai thay vì coi nó là số đo.

---

## Bộ giải

`numpy` một mình là đủ, nhưng Phần IV §8.1 của bài báo gốc yêu cầu một bộ giải
thích ứng **cứng** (stiff): LSODA / Radau / BDF. Không có `scipy` thì engine lùi
về DP45 hiện trong [`sccdx/integrate.py`](sccdx/integrate.py) và **báo cáo rằng
nó đã lùi** — ở `trajectory.solver` và trong các ghi chú trả về.

DP45 **không** phải bộ giải cứng. Nó theo được hệ này tới ~1e-6 ở các độ lớn hệ
số trong `spec`/`spec2`, nhưng hãy cài `scipy` trước khi bạn nâng bất kỳ tốc độ
nào lên một bậc độ lớn, hoặc thêm các xung sốc dưới một năm:

```bash
pip install scipy
```

`/api/v2/health` cho biết backend nào đang chạy (`"ode_backend": "scipy"`).

---

## Cấu trúc repo

```
sccd/          v1.00 — mười thành phần, lõi ODE, các vòng lặp, spec
sccdx/         v2.00 — hai khối cưỡng bức, sự kiện, preset, i18n, tự sự
web/index.html bộ render; không chứa văn xuôi của riêng nó
serve.py       server chính, chỉ stdlib + numpy
api_fastapi.py bản ASGI tuỳ chọn, có tài liệu OpenAPI
validate2.py   119 kiểm tra, trải cả hai phiên bản và cả hai ngôn ngữ
validate_v1.py báo cáo bất nhất của v1 — in ra những gì bài báo làm sai
validate_lang.py  các kiểm tra ngang bằng ngôn ngữ (được validate2.py nhập)
sea2027/       mười một quốc gia ASEAN, 44 PDF, lớp phủ phân tích
docs/          ba bài báo gốc, ghi chú thiết kế, log kiểm tra
```

`validate_lang.py` là một **module**, không phải entry point — chạy trực tiếp
thì nó không in gì và thoát 0. `validate2.py` gọi các kiểm tra của nó, và đó là
nơi bạn thấy chúng.

---

## Kiểm tra

```bash
python validate2.py       # 119 PASS, 0 FAIL, 4 KNOWN-DEFECT là kết quả ĐÚNG
python validate_v1.py     # báo cáo bất nhất của v1
```

Đã kiểm trên Python 3.12, Windows / macOS / Linux, có và không có `scipy`.

---

## Tài liệu

- **[docs/GUIDE.vi.md](docs/GUIDE.vi.md)** — hướng dẫn đầy đủ, từng lệnh và từng endpoint
- **[docs/GUIDE.en.md](docs/GUIDE.en.md)** — bản tiếng Anh
- **[docs/engine-notes-en.md](docs/engine-notes-en.md)** — ghi chú engine gốc: bốn kết quả cấu trúc, phân tích sâu
- **[sea2027/README.md](sea2027/README.md)** — đợt chạy ASEAN, từng file
- **[docs/validation-log.txt](docs/validation-log.txt)** — một đợt kiểm tra đã ghi lại
- **[docs/v1-notes-vi.md](docs/v1-notes-vi.md)** — ghi chú thiết kế của engine v1.00 đứng riêng (các lệnh trong đó là lịch sử, xem cảnh báo đầu file)

### Các bài báo gốc

- [`docs/Degrow.pdf`](docs/Degrow.pdf) — *The Wheel of Fate* (Khối D)
- [`docs/The_Displacement_Hypothesis_v2.pdf`](docs/The_Displacement_Hypothesis_v2.pdf) — *The Displacement Hypothesis* (Khối A)

---

## Góp sức

Rất hoan nghênh issue và pull request. Những thứ giúp được nhiều nhất:

1. **Hiệu chỉnh tham số.** 46 trong 83 tham số v1, và toàn bộ 46 tham số v2,
   không mang giá trị từ bất kỳ bài báo nguồn nào. Một giá trị bảo vệ được cho
   **dù chỉ một** tham số, kèm căn cứ có trích dẫn, sẽ nâng cả một nhánh output
   từ thứ tự lên định lượng.
2. **Tranh luận với lớp phủ phân tích.** `sea2027/judgment.py` nêu rõ lập luận
   cho từng quốc gia để có thể bị phản bác. Hãy phản bác nó trong một issue.
3. **Giải quyết các bất nhất của v1.** `validate_v1.py` nêu tên từng cái và đề
   xuất cách sửa. Cài đặt một cái sau một cờ bật/tắt, kèm test, là một đóng góp
   gọn gàng.

Xin giữ `python validate2.py` ở mức 119 PASS / 0 FAIL, và giữ cả hai mặt ngôn
ngữ đầy đủ — bộ test sẽ đánh bạn fail nếu không.

---

## Trích dẫn

Xem [CITATION.cff](CITATION.cff), hoặc:

> Vi Nhật Sơn. *Sovereign-Civilian Capacity Dynamics*, Phần I–V.
> Cùng *The Wheel of Fate* và *The Displacement Hypothesis* (tái bản lần 2).

---

## Giấy phép

[Apache License 2.0](LICENSE) — cho phép dùng thương mại, sửa đổi và phân phối,
kèm điều khoản bằng sáng chế và yêu cầu ghi lại thay đổi của bạn. Xem
[NOTICE](NOTICE) cho điều khoản áp dụng với các bài báo PDF.

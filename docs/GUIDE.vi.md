# SCCD-X Engine — Hướng dẫn đầy đủ

Mọi thứ bạn cần để chạy engine, đọc hiểu nó nói gì, và biết **không** được
khẳng định điều gì từ nó. Nếu bạn muốn bản ngắn, [README.vi.md](../README.vi.md)
chính là bản ngắn.

**Mục lục**

1. [Cài đặt](#1-cài-đặt)
2. [Lần chạy đầu tiên](#2-lần-chạy-đầu-tiên)
3. [Mười thành phần](#3-mười-thành-phần)
4. [Hai khối mới](#4-hai-khối-mới)
5. [Đọc output](#5-đọc-output)
6. [Tám vòng lặp](#6-tám-vòng-lặp)
7. [API HTTP](#7-api-http)
8. [Dùng từ Python](#8-dùng-từ-python)
9. [Đợt chạy ASEAN 2027](#9-đợt-chạy-asean-2027)
10. [Kiểm tra, và các con số nghĩa là gì](#10-kiểm-tra-và-các-con-số-nghĩa-là-gì)
11. [Được và không được khẳng định điều gì](#11-được-và-không-được-khẳng-định-điều-gì)
12. [Xử lý sự cố](#12-xử-lý-sự-cố)

---

## 1. Cài đặt

Python 3.9 trở lên.

```bash
git clone https://github.com/vinhatson/sccdx-engine.git
cd sccdx-engine
pip install numpy
```

`numpy` là thứ duy nhất bắt buộc. Hai thứ tuỳ chọn:

```bash
pip install scipy              # bộ giải cứng mà bài báo thực sự yêu cầu
pip install fastapi uvicorn    # chỉ khi bạn muốn dùng api_fastapi.py thay serve.py
```

Hãy cài `scipy` nếu được. Xem [§12](#12-xử-lý-sự-cố) để biết vì sao nó quan
trọng và khi nào nó **thôi** còn là tuỳ chọn.

### Lưu ý cho Windows

Không cần làm gì thêm. Các entry point tự đặt stdout của chúng về UTF-8, nên
console `cmd.exe` hay PowerShell mặc định sẽ hiện đúng tiếng Việt và các chữ Hy
Lạp thay vì crash ngay khi gặp chúng.

---

## 2. Lần chạy đầu tiên

```bash
python serve.py
```

Mở <http://127.0.0.1:8777>. Bạn được một trang duy nhất với ba tab và cặp
`VI` / `EN` ở góc.

| tab | hiện gì |
|---|---|
| **một** | một quốc gia: đầu vào bên trái, chẩn đoán bên phải |
| **thế giới** | các quốc gia cùng nhau, có trọng số — tầng thế giới |
| **kiểm toán** | mọi tham số, giá trị của nó, và giá trị đó **đến từ đâu** |

Hãy bắt đầu bằng cách chọn một preset trong dropdown. Có mười cái sẵn: `US`,
`CN`, `EU`, `JP`, `KR`, `IN`, `RU`, `BR`, `GB`, `NG`.

**Bấm nút `EN` / `VI` và xem cả trang đổi theo.** Đó không phải một lớp dịch
trong trình duyệt — cú bấm đó **chạy lại chẩn đoán ở server** và mọi chuỗi đến
từ API. Các con số được khẳng định là giống hệt nhau giữa hai ngôn ngữ; chỉ có
chữ là khác.

Rồi mở tab **kiểm toán**. Đây là tab quan trọng nhất, và cũng là tab bị bỏ qua
nhiều nhất. Nó cho bạn biết trong các con số đang dẫn ra kết quả của bạn, cái
nào đến từ một bài báo và cái nào đến từ phán đoán của một người phân tích. Hãy
đọc §11 trước khi trích bất cứ gì.

---

## 3. Mười thành phần

Một quốc gia là mười thành phần năng lực, mỗi cái trên [0, 1]. Năm chủ quyền
(`S`), năm dân sự (`C`).

| khoá | tên | tình trạng dữ liệu |
|---|---|---|
| `s1` | Năng lực trích xuất tài khoá | PAPER proxy |
| `s2` | Chỉ số độc quyền cưỡng chế | PAPER proxy |
| `s3` | **Vốn chính danh** | **BLOCKED** |
| `s4` | **Độ sâu thâm nhập hành chính** | **BLOCKED** |
| `s5` | Đòn bẩy thời gian | PAPER proxy |
| `c1` | Mức tập trung vốn tư nhân | PAPER proxy |
| `c2` | Mật độ tổ chức dân sự | PAPER proxy |
| `c3` | Tự chủ thông tin | PAPER proxy |
| `c4` | Độ sẵn có của lối ra | PAPER proxy |
| `c5` | **Phân mảnh ưa thích** | **BLOCKED** |

**`BLOCKED` nghĩa là bài báo gốc không định nghĩa một proxy dùng được nào cho
thành phần đó.** Không có đường ống đo lường nào cho `s3`, `s4` hay `c5` — bạn
tự cấp chúng, và cái bạn cấp là một **phán đoán**.

Đây không phải lỗ hổng nhỏ. `s3` dẫn λ, hệ số nhân chính danh, và λ nhân vào
**toàn bộ** S. `c5` vừa là mẫu số của C **vừa** là thừa số `(1−c5)` trong Ψ. Ba
thành phần bị BLOCKED lại chính là những thành phần mà toàn bộ phần lõi phi
tuyến xoay quanh.

### Loại nhà nước

Bốn loại, và lựa chọn này **đổi trọng số** của phép tổng hợp:

| loại | w1 | w4 | ω25 |
|---|---|---|---|
| `liberal_democracy` | 0,40 | 0,35 | 0,25 |
| `developmental_autocracy` | 0,35 | 0,45 | 0,20 |
| `extractive_patrimonial` | 0,50 | 0,20 | 0,30 |
| `failed_state` | 0,60 | 0,25 | 0,15 |

Loại nhà nước là một **đầu vào**, không phải đầu ra. Engine không suy ra nó, và
đổi nó thì kết quả đổi — nên hãy **nêu rõ** nó khi bạn báo cáo bất cứ điều gì.

---

## 4. Hai khối mới

Đây là phần v2.00 thêm vào. `sccd` v1.00 để hai số hạng của chính hệ ODE của nó
ngoại sinh:

```
dS₃/dt = **S₃_natural**    − ρ_b(1−λ/λmax)² − ζ·C₅^ψ·(S₃−S₃floor)
dC₅/dt = **C₅_structural** + ε_p·C₅(1−C₅)·RevPol + η·C₅²·C₃ + ξ·Ĉ₄Ĉ₁(1−C₅)
```

v2 cấp cả hai số hạng có dấu sao từ hai bài báo nữa, trên hai thang thời gian
khác nhau.

### Khối D — nhân khẩu (`DEGROW`)

Từ *The Wheel of Fate*. Năm đầu vào:

| khoá | tên |
|---|---|
| `d1` | Tải năng lực chống đỡ |
| `d2` | Bẫy kỳ vọng |
| `d3` | **Tự chủ điều chỉnh** |
| `d4` | Đảo ngược phụ thuộc |
| `d5` | Nhóm thanh niên dư thừa |

Khối D là một **bộ định tuyến**, không phải thêm một áp lực. Tải sinh ra một
lượng áp lực điều chỉnh; cái mà bài báo thay đổi là *kênh nào gánh nó*. Biến
phân luồng là `d3`, độ sẵn có của các công cụ tự nguyện — tránh thai, hoạch định
tài chính, tư duy quản trị rủi ro:

```
violent_share = (1 − d3)^route_sharpness
```

`d3` cao thì áp lực đi qua kênh điều chỉnh tự nguyện. `d3` thấp thì **cùng** áp
lực đó đi qua kênh bạo lực. Cả hai hiện tượng mà bài báo khẳng định — bùng nổ
rồi sụp đổ thời cổ đại, và đóng băng sinh sản thời hiện đại — đều kết thúc ở
**cùng một đối tượng**, θ₂₅, và chính điều đó làm cho khẳng định trở nên
**kiểm chứng được** chứ không chỉ gợi ý.

Có một lựa chọn mà bài báo gốc **không giải quyết**, nên engine phơi nó ra thành
một tuỳ chọn thay vì tự quyết hộ bạn:

```
router_mode = "conserve"   # mặc định: chuyển hướng áp lực
router_mode = "discount"   # đồng thời làm teo nó đi
```

*The Wheel of Fate* không nói cái nào đúng. Điều này được ghi nhận là vấn đề mở
`OP2-1`. **Nếu kết luận của bạn đảo chiều khi đổi giữa hai mode, thì kết luận
của bạn là về vấn đề mở đó, không phải về quốc gia bạn đang xét.**

### Khối A — tốc độ nhận AI (`DISPL`)

Từ *The Displacement Hypothesis*, tái bản lần 2. Sáu đầu vào:

| khoá | tên |
|---|---|
| `a1` | Độ xuyên thấu của AI |
| `a2` | Xói mòn tự hiệu năng (Tầng 1) |
| `a3` | Xói mòn năng lực hành động (Tầng 2) |
| `a4` | Tái phân bổ trú ẩn |
| `a5` | Huy động phản-công-nghệ |
| `a6` | Lợi tức năng suất từ AI |

Để ý hai tầng là **tách biệt**: `a2` là xói mòn **niềm tin** rằng nỗ lực có tác
dụng, còn `a3` là xói mòn **năng lực** hành động. Bài báo phân biệt chúng, và
engine cũng vậy.

---

## 5. Đọc output

`POST /api/v2/diagnose` trả về các trường cấp cao sau:

```
country  year  state_type  verdict  capacity  capacity_base  forcing
loops  bifurcation  attractor  trajectory  horizon_verdict
uncertainty  fragility
```

### Các dải chế độ

Con số chính rơi vào một trong năm dải:

| dải | khoảng | độ ổn định |
|---|---|---|
| Imperial (Đế quốc) | 0,60 … 1,00 | **Bất ổn (rút cạn)** |
| Hegemonic (Bá quyền) | 0,30 … 0,60 | Siêu bền (metastable) |
| Negotiated (Thương lượng) | 0,08 … 0,30 | Ổn định có điều kiện |
| Equilibrium (Cân bằng) | −0,08 … 0,08 | **Ổn định HOẶC bế tắc** |
| Crisis (Khủng hoảng) | −0,40 … −0,08 | Bất ổn (phân nhánh) |

Hai điều đáng để ý. **Imperial là bất ổn**, không phải mạnh — nó là trạng thái
rút cạn. Và **Equilibrium thì nhập nhằng giữa ổn định và bế tắc**: riêng cái dải
không phân biệt được một dàn xếp đang chạy tốt với một dàn xếp đã đóng băng, nên
hãy **đọc các vòng lặp**.

### Các chế độ điều chỉnh

```
VOLUNTARY   VIOLENT_EXPOSED   MIXED   SLACK
```

Đây là phán quyết **định tuyến** của Khối D — kênh mà áp lực điều chỉnh đang đi
qua, không phải lượng áp lực là bao nhiêu.

### Nhãn nguồn gốc

Mọi trường dẫn xuất đều mang một nhãn. Bạn sẽ thấy:

- `PAPER` — giá trị được nêu trong một bài báo nguồn
- `PAPER proxy` — bài báo định nghĩa một proxy đo lường cho nó
- `BLOCKED` — bài báo không định nghĩa proxy dùng được nào
- `ANALYST` — phán đoán của một người, kèm lý lẽ được nêu ra
- `DERIVED` / `DERIVED2` — tính ra từ các giá trị khác

**Hãy đọc các nhãn.** Một kết quả dựng trên đầu vào `ANALYST` là một **lập
luận**; một kết quả dựng trên đầu vào `PAPER` là một **lối đọc bài báo**. Engine
không bao giờ che việc bạn đang xem cái nào.

### Engine phát ra mã, không bao giờ phát ra câu văn

Đây là một kỷ luật có chủ đích, và đáng hiểu vì nó giải thích toàn bộ kiến trúc.
Engine trả về **mã**; văn xuôi sống ở một chỗ duy nhất (`sccdx/i18n*.py`, và
`sea2027/prose_*.py` cho đợt ASEAN) nơi nó có thể được kiểm toán đối chiếu với
đợt chạy đã sinh ra nó.

Đó là lý do `web/index.html` chứa **không một** ký tự tiếng Việt nào, và lý do
có một test sẽ fail nếu điều đó thay đổi.

---

## 6. Tám vòng lặp

Tám vòng phản hồi có tên. Sáu cái đầu là v1; `L7` và `L8` đến từ Khối D.

| vòng | tên |
|---|---|
| `L1` | Bộ gia tốc thâu tóm quy định |
| `L2` | Vòng xoáy chết của tính chính danh |
| `L3` | Bẫy phân cực |
| `L4` | Ghép nối lối-ra ↔ phân mảnh |
| `L5` | Vòng xoáy năng-lực-hành-động ↔ chính danh |
| `L6` | Vòng xoáy khả-đọc ↔ trích xuất |
| `L7` | Bẫy đảo ngược nhân khẩu |
| `L8` | Xả nhóm thanh niên dư thừa |

Mỗi vòng báo nó có đang hoạt động hay không, và vì sao. Một vòng **bật lên**
thường mang nhiều thông tin hơn là con số chính dịch chuyển, vì cái vòng cho bạn
biết **cơ chế nào** đang làm việc đó.

Hãy để ý một điều kiện cấu trúc ở đây — xem `INC-9` ở §10. Theo đúng cách các
phương trình v1 được viết, `C₁` là **ngoại sinh**, nghĩa là `L1` và `L4` là các
vòng **hở**, không phải kín. Engine tái tạo điều này một cách trung thực thay vì
âm thầm sửa. Nếu bạn muốn bản kín, hãy truyền `c1_dynamic=True`.

---

## 7. API HTTP

`serve.py` chỉ cần `numpy`. Nó phục vụ cả trang và API ở cổng 8777.

### Các endpoint tham chiếu (GET)

Mọi cái đều nhận `?lang=vi|en`.

```bash
curl http://127.0.0.1:8777/api/v2/health
curl "http://127.0.0.1:8777/api/v2/schema?lang=vi"      # đầu vào, dải, vòng lặp, tuỳ chọn
curl "http://127.0.0.1:8777/api/v2/presets?lang=vi"     # mười quốc gia có sẵn
curl "http://127.0.0.1:8777/api/v2/events?lang=vi"      # 50 sự kiện
curl "http://127.0.0.1:8777/api/v2/audit?lang=vi"       # mọi tham số + nguồn gốc
```

`health` cho biết bộ giải nào đang chạy:

```json
{"ok": true, "engine": "SCCD-X", "langs": ["vi", "en"],
 "sccd_spec": "1.00", "sccdx_spec": "2.00",
 "ode_backend": "scipy", "python": "3.12.10", ...}
```

### Các endpoint chẩn đoán (POST)

```bash
curl -X POST http://127.0.0.1:8777/api/v2/diagnose \
     -H "Content-Type: application/json" \
     -d '{"lang":"vi"}'

curl -X POST http://127.0.0.1:8777/api/v2/world \
     -H "Content-Type: application/json" \
     -d '{"lang":"vi"}'
```

Gửi các giá trị thành phần trong body để chẩn đoán quốc gia của riêng bạn thay
vì một preset. Dùng `/api/v2/schema` để xem mọi khoá được nhận, khoảng giá trị
và giá trị mặc định của nó.

### Bản FastAPI

```bash
pip install fastapi uvicorn
python api_fastapi.py
```

Cùng engine, có tài liệu OpenAPI, là một ứng dụng ASGI. Dùng nó nếu bạn gắn thứ
này vào trong một hệ khác. `serve.py` là server chính và không có phụ thuộc đó.

---

## 8. Dùng từ Python

Tầng web chỉ là một vỏ mỏng bọc các package nhập được.

```python
from sccd.dynamics import simulate
from sccd.spec import KNOWN_INCONSISTENCIES

# các bất nhất của v1, ở dạng máy đọc được — có 9 cái
for inc in KNOWN_INCONSISTENCIES:
    print(inc["id"], inc["severity"], inc["where"])
```

`simulate` nhận các sub-component, một context, và các tham số sau:

```python
simulate(sc, ctx,
         years=10.0,
         t0=0.0,
         params=None,
         state_type="liberal_democracy",
         method="LSODA",        # tự lùi nếu không có scipy
         n_out=200,
         patch=None,
         c1_dynamic=False)      # True nâng C1 thành biến trạng thái thứ 5
```

`c1_dynamic` là cái công tắc **khép kín** vòng phản hồi mà `INC-9` mô tả:

- `c1_dynamic=False` → 4 trạng thái `[S, C, S₃, C₅]`, đúng theo eq (NL) / INT
  §7.1 **như đã viết**
- `c1_dynamic=True` → 5 trạng thái `[S, C, S₃, C₅, C₁]`, dùng chính phương trình
  của Phần IV §2.1

Mặc định là `False` vì đó là điều §7.1 của bài báo nói. Bản **trung thực về mặt
mô hình** thì có lẽ là `True`. Cả hai đều có; mặc định là **sự trung thành với
bài báo**, không phải sự đúng đắn.

Với v2, xem `sccdx.dynamics2.simulate2` và `sccdx.integrate.best_solver`.

---

## 9. Đợt chạy ASEAN 2027

Một ứng dụng hoàn chỉnh: cả mười một quốc gia ASEAN, dữ liệu lấy 2026-10-09.

```bash
python sea2027/run.py                                 # tiếng Việt
python sea2027/run.py --lang en                       # tiếng Anh
python sea2027/run.py --lang en --json out.json       # + dump đầy đủ
python sea2027/run.py --mc 2000                       # nhiều lượt Monte Carlo hơn

python sea2027/make_pdf.py                            # 22 PDF kỹ thuật
python sea2027/make_prose_pdf.py                      # 22 PDF văn xuôi
```

Đợt chạy cho ra: phán quyết 2027, thứ tự cổng 15 năm, tầng thế giới, một nhánh
chịu tải, và hai phản thực.

### Các file

```
raw_2026.py   bảng số đo — TỰ ĐỘNG SINH, không sửa tay
gen_raw.py    bộ lấy dữ liệu viết ra nó (cần các file nguồn thô)
judgment.py   lớp phủ ANALYST: một khối mỗi quốc gia, mọi con số đều được lập luận
mapping.py    bảng số đo -> mười thành phần + Khối D và A
run.py        chính đợt chạy
out_{vi,en}.txt       báo cáo đã render
sea2027_{vi,en}.json  payload đầy đủ, kèm nguồn gốc từng trường dẫn xuất
prose_{en,vi}.py      lối đọc văn xuôi — DIỄN GIẢI, không phải output của engine
```

Lưu ý `gen_raw.py` cần các file nguồn thô (`wb.json`, `wgi.json`, `imf.json`,
`libdem.csv`, …) **không** có trong repo. `raw_2026.py` chính là output đã commit
của một đợt chạy đã có chúng. Bạn **không** cần lấy lại dữ liệu để dùng engine.

### Hai bộ PDF

44 PDF đi kèm sẵn, chia hai bộ, và sự khác nhau chính là điểm cốt yếu:

- `pdf/` — **output của dụng cụ đo**. Bảng, nhãn nguồn gốc từng thành phần, các
  dòng OAT, phóng chiếu cổng, quỹ đạo. Sans-serif ở khổ chữ 170mm, vì nó là tài
  liệu tra cứu. Mỗi bản 5–6 trang.
- `pdf_prose/` — **lập luận về việc output đó nghĩa là gì**. Serif ở khổ 115mm
  với một dải hình mỏng ở đầu để mọi khẳng định đều đối chiếu được với đợt chạy
  đứng sau nó. Mỗi bản 2 trang, ~20.000 từ cho cả 22 bản.

`prose_en.py` và `prose_vi.py` là **DIỄN GIẢI** và nói rõ điều đó trên mọi tài
liệu. Phần tiếng Việt được **viết**, không phải dịch.

### `judgment.py`

Hãy đọc file này trước khi tin bất kỳ con số ASEAN nào. Nó là một lớp phủ phân
tích **công khai**: một khối mỗi quốc gia, mọi giá trị đều được lập luận tại
chỗ. Nó là một phán đoán và nó **được dán nhãn** như vậy. Hãy phản biện nó trong
một issue thay vì coi nó là số đo.

---

## 10. Kiểm tra, và các con số nghĩa là gì

```bash
python validate2.py       # bộ kiểm tra chính
python validate_v1.py     # báo cáo bất nhất của v1
```

Kết quả **đúng** cho `validate2.py` là:

```
PASS 119   FAIL 0   KNOWN-DEFECT 4
```

**`KNOWN-DEFECT 4` không phải bốn failure.** Bốn dòng đó ghi lại rằng engine tái
tạo trung thực một khuyết tật mà `sccd.spec.KNOWN_INCONSISTENCIES` đã ghi nhận.
Nếu con số đó thay đổi thì đã có gì đó đổi trong mức độ trung thành của engine
với bài báo — đổi theo chiều nào cũng cần điều tra.

### 119 kiểm tra đó bao gồm gì

Phần số, sự bật tắt vòng lặp, thứ tự cổng, phát hiện phân nhánh — và một khối
kiểm tra **ngang bằng ngôn ngữ** nghiêm hơn hầu hết dự án song ngữ chịu làm:

- cả 406 template phải có **cả hai** mặt Việt và Anh
- cả 160 chuỗi UI phải có cả hai mặt
- thiếu một khoá i18n thì **ném lỗi**, không âm thầm render tiếng Anh
- cả 50 sự kiện phải có ghi chú tiếng Việt; mọi sự kiện có nhãn ở cả hai ngôn ngữ
- cả 10 preset phải có lý lẽ bằng tiếng Việt
- cả 7 vấn đề mở của v2 và cả 9 bất nhất của v1 đều được dịch
- cả 46 ghi chú tham số v2 đều được dịch
- `web/index.html` chứa **không một** ký tự tiếng Việt
- trang phơi hai tab ngôn ngữ riêng biệt, fetch có tham số `lang`, và **chạy lại
  chẩn đoán** khi đổi ngôn ngữ
- quỹ đạo, kết quả số và phán quyết độ mong manh **giống hệt nhau** giữa hai
  ngôn ngữ

`validate_lang.py` giữ các kiểm tra này nhưng là **một module, không phải entry
point**. Chạy trực tiếp thì nó không in gì và thoát 0 — đó **không** phải lỗi.
`validate2.py` gọi nó.

### Các bất nhất của v1

`validate_v1.py` in ra các vấn đề của chính mô hình nguồn thay vì vá chúng. Ba
cái ở mức `CRITICAL`:

- **INC-7** — `dC₅/dt`: cả ba số hạng nội sinh đều **dương** và không có số hạng
  giảm phân cực, dù §2.3 định nghĩa phép thử bật L3 dựa trên một
  'Natural_Depolarisation_Rate'. Theo đúng cách đã viết, C₅ tăng đơn điệu về 1
  trên **mọi** quỹ đạo, do đó Ψ = λ·θ₂₅·(1−C₅) → 0 bất kể kịch bản nào.
  *Đề xuất sửa: thêm* `−ν·C₅` *hoặc* `−ν·C₅·C₂`.
- **INC-8** — `dS₃/dt`: cả hai số hạng nội sinh đều **âm**, nên với `S₃_natural`
  ngoại sinh, S₃ chỉ có thể suy giảm. Mô hình không thể sinh ra sự tái lập tính
  chính danh mà Phần V ghi lại cho 1980–86 (λ 1,2 → 1,7) hay đợt gây dựng
  1941–45, dù §2.2 có nêu một tốc độ 'hồi phục chính danh tự nhiên' mà **không
  bao giờ** vào ODE.
- **INC-9** — §2.1 viết hẳn `dC₁/dt`, nhưng §7.1 lại **bỏ `C₁`** khỏi vector
  trạng thái. Với `C₁` ngoại sinh thì cả `dS₃/dt` lẫn `dC₅/dt` đều không phụ
  thuộc S hay C, nên `[S₃,C₅]` là một **hệ con tự trị** đẩy `[S,C]` một chiều.
  Trong eq (NL) **không có vòng phản hồi kín nào cả**. Dấu hiệu nhận biết: mọi
  kịch bản cho ra `C₅(t)` và `Ψ(t)` **y hệt nhau**.

Cái cuối là cái lớn nhất, và đó là lý do `c1_dynamic=True` tồn tại.

---

## 11. Được và không được khẳng định điều gì

Chính engine nêu ra tình trạng nhận thức luận của nó ở cuối mỗi đợt kiểm tra:

```
36 trong 83 tham số v1 mang giá trị từ bài báo gốc; 46 cái thì không.
TOÀN BỘ 46 tham số v2 đều là ANALYST hoặc DERIVED2 — hai bài báo mới là
định tính và không nêu hệ số nào. Hãy đọc mọi output phụ thuộc v2 như là
THỨ TỰ: một bảng xếp hạng và một bản đồ vượt ngưỡng, không phải một mức.
```

Cụ thể như sau.

**Bạn ĐƯỢC:**
- so hai quốc gia và báo cáo cái nào xếp cao hơn trên một phép đo cho trước
- báo cáo rằng một ngưỡng bị vượt, hoặc **thứ tự** các cổng sụp
- báo cáo vòng lặp nào bật, và cơ chế nào mang kết quả
- báo cáo rằng một kết luận có **vững** hay không khi đổi `router_mode`
- trích bất kỳ giá trị `PAPER` nào, kèm trích dẫn của nó

**Bạn KHÔNG ĐƯỢC:**
- trích một con số dẫn xuất từ v2 như một **mức**, một **độ lớn** hay một
  **xác suất**
- báo cáo một **mốc thời gian** như một dự báo
- coi mười preset sẵn là **số đo** — chính disclaimer trong payload nói rằng
  trong cả file chỉ có **bốn** giá trị là do bài báo nêu (US `s3`=0,38,
  `c5`=0,74, `c1`=0,82, `s2`≈0,90), rằng **không có gì** được sinh ra bằng cách
  chạy đường ống proxy của Phần III, và **không giá trị nào** mang khoảng tin cậy
- coi `sea2027/judgment.py` là số đo
- bỏ qua loại nhà nước khi báo cáo — nó đổi trọng số của phép tổng hợp

Nếu một kết luận **sống sót** qua cả hai cài đặt `router_mode`, cả hai cài đặt
`c1_dynamic`, và một đợt quét các thành phần `BLOCKED`, thì bạn có một thứ
**mang tính cấu trúc**. Đó là chuẩn mực mà engine này được dựng để hỗ trợ, và nó
đáng giá hơn một con số có độ chính xác giả.

---

## 12. Xử lý sự cố

**`ModuleNotFoundError: No module named 'numpy'`**
Chạy `pip install numpy`.

**`"ode_backend": "dp45"` trong `/api/v2/health`**
`scipy` chưa được cài. Engine đã lùi về DP45 hiện trong `sccdx/integrate.py` và
**đã báo** điều đó ở `trajectory.solver` cùng các ghi chú trả về — nó không che.

DP45 **không** phải bộ giải cứng. Phần IV §8.1 yêu cầu một bộ giải cứng thích
ứng và nêu tên LSODA, Radau, BDF. DP45 theo được hệ này tới chừng 1e-6 ở các độ
lớn hệ số trong `spec`/`spec2`, mức đó ổn để khám phá. Hãy cài `scipy` **trước
khi** bạn nâng bất kỳ tốc độ nào lên một bậc độ lớn hoặc thêm các xung sốc dưới
một năm — qua điểm đó thì bản lùi không còn đủ:

```bash
pip install scipy
```

**`python validate_lang.py` không in gì**
Đó là hành vi đúng. Nó là một module, không phải entry point. Hãy chạy
`validate2.py`.

**`python sea2027/gen_raw.py` lỗi thiếu file**
Đúng như dự kiến. Nó cần các file nguồn thô không có trong repo. `raw_2026.py`
đã là output đã commit sẵn.

**Cổng 8777 đang bị dùng**
Sửa cổng trong `serve.py`, hoặc tắt thứ đang giữ nó.

**Trang hiện tiếng Anh sau khi tôi bấm `VI`**
Điều đó đáng lẽ **không thể xảy ra** — thiếu khoá i18n thì ném lỗi chứ không lùi
về tiếng Anh. Nếu bạn thấy nó, đó là một lỗi thật: xin mở issue kèm đúng đầu vào
đã dùng.

**Lỗi Unicode trong console**
Đáng lẽ không xảy ra; các entry point tự đặt stdout về UTF-8. Nếu bạn gặp, xin
báo OS, terminal và phiên bản Python — và cách chữa tạm là đặt
`PYTHONIOENCODING=utf-8`.

---

## Xem thêm

- [README.vi.md](../README.vi.md) — bản ngắn
- [README.md](../README.md) — English
- [GUIDE.en.md](GUIDE.en.md) — hướng dẫn này bằng tiếng Anh
- [engine-notes-en.md](engine-notes-en.md) — bốn kết quả cấu trúc, phân tích sâu
- [../sea2027/README.md](../sea2027/README.md) — đợt chạy ASEAN, từng file

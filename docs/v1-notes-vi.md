> **Ghi chú lịch sử — đọc kèm cảnh báo này.**
>
> Đây là ghi chú thiết kế của engine `sccd` **v1.00**, viết khi nó còn là một
> engine đứng riêng. Các lệnh trong đó (`python3 validate.py`,
> `python3 scenarios.py`) trỏ tới những file **không còn tồn tại** trong repo
> này: v2.00 đã gộp chúng thành `validate2.py`, `validate_v1.py` và `serve.py`.
>
> Giữ lại file này vì phần lập luận về **vì sao** từng quyết định được đưa ra
> vẫn đúng và vẫn đáng đọc. Để biết cách **dùng** engine, xem
> [GUIDE.vi.md](GUIDE.vi.md).

---

# SCCD Engine v1.00

Module hóa khung **Sovereign-Civilian Capacity Dynamics** (Vi Nhật Sơn, Parts I–V)
thành engine chẩn đoán / dự báo cấu trúc, theo đúng kiến trúc tầng của engine Lục Hào.

```
pip install numpy scipy
python3 validate.py     # đối chiếu engine với chính các số liệu trong paper
python3 scenarios.py    # 3 kịch bản A/B/C + sensitivity + tầng network
```

---

## 1. Bản đồ module — đối chiếu với engine Lục Hào

| Engine Lục Hào | Engine SCCD | File |
|---|---|---|
| — (quẻ cho sẵn, không cần đo) | **Tầng proxy / đo lường** — 10 biến tiềm ẩn → nguồn dữ liệu | `sccd/proxies.py` |
| — | **Chuẩn hóa + bất định** — z-score nội quốc, gộp đa proxy, impute, Monte Carlo | `sccd/normalize.py` |
| Luật trạng thái hào (v8.xx) | **Hàm tổng hợp** — λ(S₃) Hill, θ₂₅ ngưỡng, mẫu số φ·C₅^ψ → S, C, Δ | `sccd/aggregate.py` |
| Cặp trạng thái quẻ (nhãn ưu tiên) | **Phân loại regime** — 5 băng Δ_norm | `sccd/aggregate.py` |
| Cục | **Vòng phản hồi L1–L4** + CAI + chéo-ghép | `sccd/loops.py` |
| Chia mốc / ứng kỳ | **Tích phân ODE** — hệ 4 (hoặc 5) biến, solver stiff | `sccd/dynamics.py` |
| — | **Tầng network** — ma trận F 4 kênh, Thucydides, Ψ_G | `sccd/network.py` |
| Chốt luật theo phiên bản | **Spec có version** — mọi hằng số kèm nguồn + trạng thái | `sccd/spec.py` |
| Rà mâu thuẫn | **Validate** — đối chiếu engine vs paper, sổ mâu thuẫn | `validate.py`, `spec.KNOWN_INCONSISTENCIES` |

**Khác biệt nền tảng:** engine Lục Hào là hệ **đóng, tất định** — cho quẻ là ra kết quả,
luật đầy đủ. SCCD là hệ **mở**: cả 10 đầu vào đều là biến tiềm ẩn phải đo từ bên ngoài,
kèm sai số. Vì vậy SCCD cần thêm hai tầng mà Lục Hào không cần: tầng proxy và tầng bất định.
Đây cũng chính là chỗ API gắn vào.

---

## 2. Trạng thái tham số — `spec.audit()`

| Trạng thái | Số lượng | Ý nghĩa |
|---|---|---|
| `PAPER` | 36 / 80 (45%) | Có giá trị số trong paper → thành hằng số engine |
| `DERIVED` | 1 / 80 | Suy ra từ giá trị PAPER khác |
| `FREE` | 43 / 80 (54%) | **Không có giá trị số ở bất kỳ đâu trong Parts I–V** |

Mỗi output đều mang nhãn hiệu chuẩn:

**CALIBRATED** (chỉ dùng tham số PAPER — dùng được ngay):
λ(S₃), θ₂₅, S, băng regime, Ψ, kích hoạt L1/L2, R_B, Γ, Ĉ₁,crit

**UNCALIBRATED** (phụ thuộc ≥1 tham số FREE — chỉ so sánh tương đối, không đọc mức tuyệt đối):
C (cần φ, ψ, α_exit) → kéo theo cả Δ và Δ_norm; kích hoạt L3/L4; CAI;
mọi quỹ đạo ODE; Ψ_G; thời điểm T_trap; chọn attractor

---

## 3. Sổ mâu thuẫn — `spec.KNOWN_INCONSISTENCIES`

Ba lỗi **CRITICAL** làm hệ ODE không chạy đúng như lập luận của chính paper:

- **INC-7** `dC₅/dt` chỉ có số hạng **dương** (ε_p, η, ξ), không có số hạng giảm phân mảnh,
  dù §2.3 định nghĩa điều kiện kích hoạt L3 dựa trên `Natural_Depolarisation_Rate`.
  → C₅ tăng đơn điệu về 1 trên **mọi** quỹ đạo, nên Ψ = λ·θ₂₅·(1−C₅) → 0 bất kể kịch bản.
- **INC-8** `dS₃/dt` chỉ có số hạng **âm** (ρ_b, ζ). → S₃ chỉ giảm, mô hình **không thể**
  sinh ra chính giai đoạn tái lập tính chính danh mà Part V §2.3 mô tả (λ 1.2 → 1.7, 1980–86).
- **INC-9** §2.1 viết tường minh `dC₁/dt`, nhưng vector trạng thái ở §7.1 là `[S, C, S₃, C₅]`
  — **thiếu C₁**. Hệ quả: `[S₃,C₅]` thành hệ con **tự trị**, chỉ chạy một chiều vào `[S,C]`.
  Trong eq (NL) như đã viết **không tồn tại vòng phản hồi kín nào** — L1 và L4 bị hở, và
  bảng chéo-ghép §2.4 không được phương trình nào hiện thực hóa.

Hai lỗi **HIGH**: INC-2 (eq 6 vs eq 7 áp Π khác nhau), INC-5 (C₅ US 2024 = 0.72 vs 0.74).
Bốn lỗi medium/low: INC-1, INC-3, INC-4, INC-6.

### Patch của engine
- `simulate(..., patch=True)` — thêm `−ν·C₅·C₂` và `+σ·(S₃_target − S₃)` (vá INC-7/8)
- `simulate(..., c1_dynamic=True)` — đưa C₁ thành biến trạng thái thứ 5 theo đúng
  phương trình §2.1, **khóa vòng L1 và L4** (vá INC-9)

Mặc định cả hai = OFF để tái lập paper nguyên văn. Bật lên để có quỹ đạo dùng được.

---

## 4. Kết quả đối chiếu — `validate.py`

| Kiểm tra | Engine | Paper | Kết quả |
|---|---|---|---|
| λ(0.50) | 1.4000 | 1.40 | PASS |
| λ(0.4317) → 1980 | 1.2003 | 1.20 | PASS |
| λ(0.625) → 1986 | 1.6991 | 1.70 | PASS |
| λ(0.20) | 0.5022 | 0.55 | FAIL |
| λ(0.38) → US 2024 | 1.0368 | 0.93 | FAIL |
| **λ trần tại S₃=1.0** | **2.1695** | paper nói λ≈2.3 (1945) | **BẤT KHẢ** |
| **Ψ(US 2024)** | **0.2647** | **0.43** | **FAIL — đảo kết luận** |
| Δ_norm(US 2024) | +0.0075 | −0.02 | PASS (trong ±0.10) |
| Δ_norm(US 1945) | +0.6980 | 0.72 | PASS |
| CAI(US 2024) | 2.00 | 2.1 | PASS |
| δ_hc(2024) dấu | −0.361 | −0.40 ±0.25 | PASS |
| T_trap (US–CN) | 1 | 1 | PASS |
| R_B,G (2024) | 1 | 1 | PASS |

**Điểm nghiêm trọng nhất — Ψ.** Với θ₂₅ ≤ 1 và C₅ = 0.74, đồng nhất thức
Ψ = λ·θ₂₅·(1−C₅) chặn trên Ψ ≤ λ × 0.26 = 0.24 (dùng chính λ = 0.93 của paper).
Giá trị 0.43 **nằm ngoài chặn này**. Mà Ψ_crit = 0.40:

- Paper: Ψ = 0.43 → "nhích trên ngưỡng" → R_B = 0 → không cảnh báo phân nhánh
- Engine: Ψ = 0.265 → **dưới ngưỡng** → R_B = 1 ngay khi dΔ/dt < −0.05

Kết luận cấu trúc đầu bài **đảo chiều** chỉ vì một điểm số học. Để Ψ = 0.43 thì
cần S₃ = 0.618 (không phải 0.38), hoặc C₅ = 0.578 (không phải 0.74).

**Mâu thuẫn L1.** §2.1 ra điều kiện **kép**: Ĉ₁ > 0.70 **AND** Ŝ₂ < 0.60. Mỹ có
Ŝ₂ ≈ 0.90 nên hội không thỏa, dù Ĉ₁ = 0.82 vượt ngưỡng. Part V vẫn gọi L1 là
"ACTIVE above threshold" chỉ dựa trên điều kiện Ĉ₁. Engine theo §2.1 (phát biểu hình thức).

---

## 5. Sẵn sàng API — `proxies.api_readiness()`

**7 / 10** proxy chính lấy được tự động.

| | Component | Trạng thái | Nguồn chính |
|---|---|---|---|
| ✅ | S₁ Fiscal | AUTO | IMF Fiscal Monitor (API), OECD (API) |
| ✅ | S₂ Coercive | AUTO | UCDP (API), SIPRI (bulk), FSI (bulk), WGI (API) |
| ❌ | **S₃ Legitimacy** | **BLOCKED** | L_vol cần tiền thưởng tuyển quân / tỉ lệ trốn nghĩa vụ — **chỉ Mỹ công bố, không có dataset thay thế** |
| ❌ | **S₄ Admin** | **BLOCKED** | PIFI cần tỉ lệ "chính sách đạt ≥70% mục tiêu trong 5 năm" — paper nói rõ: **phải mã hóa thủ công** |
| ✅ | S₅ Temporal | AUTO (giảm chất) | IMF (API); T_horizon phải bỏ, dùng fallback của chính paper |
| ✅ | C₁ Capital | AUTO (giảm chất) | WID.world (bulk), OpenSecrets (API key); revolving-door phải bỏ |
| ✅ | C₂ Civil Org | AUTO | V-Dem (bulk) + GDELT (API, cần pipeline phân loại sự kiện) |
| ✅ | C₃ Info | AUTO (giảm chất) | RSF, Freedom House (bulk), OONI (API); V-Dem thay Reuters |
| ✅ | C₄ Exit | AUTO | Chinn-Ito (bulk), OECD DIOC (bulk) |
| ❌ | **C₅ Fragmentation** | **BLOCKED** | P_media = Gini chồng lấn khán giả — **không có số liệu đa quốc gia**; P_legislative chỉ có DW-NOMINATE cho Mỹ |

**Quan sát cấu trúc quan trọng nhất về API:**
hai bản lề **phi tuyến** của toàn mô hình là **S₃** (hệ số nhân λ, nhân vào tất cả)
và **C₅** (mẫu số phân mảnh). Cả hai đều nằm trong nhóm BLOCKED. Những phần dễ
tự động hóa (S₁, S₅, C₁, C₄) đúng là những phần **tuyến tính, cộng tính**. Phần
quyết định regime thì không có nguồn máy đọc được.

---

## 6. Chiến lược ước lượng tham số — Part IV §8.2

| Stage | Nội dung | Phương pháp |
|---|---|---|
| 1 | α, β, γ dạng rút gọn (eq 26) | Panel đa quốc gia, IV: ngày kết thúc chiến tranh cho G; địa lý nội địa cho C₄; phân mảnh sắc tộc cho C₅ |
| 2 | Tham số vòng L1–L4 | Regression discontinuity quanh thời điểm vượt ngưỡng; event study quanh sốc chính danh |
| 3 | Tham số network | Gravity model cho F^capital, F^talent; model cấu trúc + dữ liệu liên minh cho F^military |
| 4 | Hiệu chuẩn toàn cục Ψ_G | ABC — mô phỏng rồi loại các draw không tái lập được chuyển dịch bá quyền đã biết |

Engine đã cài sẵn giao thức sensitivity bắt buộc (eq SA): OAT ±20%, LHS 10.000 draw, 3 kịch bản.

---

## 7. Giới hạn — phải đọc trước khi dùng

Part V §1 của chính paper: *"We do not, at this stage, claim predictive precision —
generating quantitatively accurate forecasts from an incompletely calibrated formal
model would be epistemically irresponsible. The validation standard is
qualitative-structural."*

Engine này tôn trọng đúng điều đó. Nó trả lời được:
- regime hiện tại, và khoảng cách tới biên regime
- vòng nào đang nóng, vòng nào đã chéo-ghép
- Ψ so với ngưỡng, R_B có bật không, attractor nào gần nhất
- thứ tự xếp hạng giữa các kịch bản chính sách

Nó **chưa** trả lời được: mức Δ tuyệt đối đáng tin, thời điểm cụ thể, xác suất định lượng.
Muốn có những thứ đó phải xong Stage 1–4 và giải được 3 nghẽn dữ liệu S₃ / S₄ / C₅.

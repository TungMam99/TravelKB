# Spec 1 — Travel Knowledge Base (Tour Operator)

> Ngày: 2026-06-23 · Trạng thái: Draft chờ duyệt · Sub-project 1/3 của platform "AI Sales cho Tour Operator"

## 0. Bối cảnh & phạm vi

Đây là **Spec 1** trong một platform 3 lớp. Spec này **chỉ** đặc tả Lớp 1 (Travel KB).
Lớp 2 (Agent tư vấn) và Lớp 3 (Website nội bộ) có spec riêng ở chu trình sau.

```
LỚP 3 — WEBSITE nội bộ (Spec 3)   chat UI cho sales · xem tour · duyệt/xuất báo giá
            │ gọi
LỚP 2 — AGENT tư vấn (Spec 2)      hỏi nhu cầu → thiết kế tour → sinh báo giá theo mẫu
            │ truy vấn / ghi
LỚP 1 — TRAVEL KB (SPEC NÀY)       Destination · Supplier · Tour Product · Quote · Concept
```

**Business:** công ty lữ hành / tour operator. **Người dùng cuối của platform:** đội **sales (copilot nội bộ)** — agent thấy đầy đủ giá vốn, chiết tính nội bộ; guardrail tối thiểu; web có đăng nhập, không phải site public.

**Vai trò của KB:** lớp "trí nhớ" bền vững, do người maintain theo pattern LLM Wiki (Karpathy), đồng thời **agent-ready** để Lớp 2 truy vấn và sinh báo giá.

## 1. Mục tiêu (Goals)

- G1. Một KB markdown **Supplier-centric** phục vụ 4 job: tư vấn điểm đến, thiết kế lịch trình, báo giá, quản lý tri thức nhà cung cấp.
- G2. Mô hình giá **hybrid 3 tầng**: giá hợp đồng theo mùa (KB lưu, có hạn dùng) · giá biến động (kỷ luật ngày + flag) · real-time (trỏ ra ngoài / gọi tool live).
- G3. Vé máy bay = supplier **live-priced**: KB lưu hoa hồng/điều khoản, giá lấy live qua `fast-flights` (no-API, đã test).
- G4. **Giao diện KB → Agent** rõ ràng (data contract) để Spec 2 kế thừa không phải sửa KB.
- G5. Ingest được **8 file nghiệp vụ thật** đã convert sang markdown.

## 2. Không làm (Non-goals / YAGNI)

- ❌ Không là booking engine — không theo dõi chỗ trống real-time từng ngày.
- ❌ Không tính giá bằng code trong KB — KB chỉ chứa dữ liệu; tính toán là việc của Agent (Spec 2).
- ❌ Không đồng bộ 2 chiều với CRM/Excel — chỉ trỏ tới (one-way pointer qua field `booking_source`).
- ❌ Không guardrail che giá vốn — đây là công cụ nội bộ.
- ❌ Không xử lý ảnh/đa phương tiện ở giai đoạn này (nguồn hiện tại là tài liệu văn bản).

## 3. Kiến trúc 3 lớp của KB (theo pattern LLM Wiki)

- **`raw/`** — nguồn thô BẤT BIẾN (hợp đồng, brochure, bảng chiết tính, supplier list). Non-markdown → convert bằng MarkItDown (`.doc` legacy đi vòng qua `textutil`). LLM chỉ đọc.
- **`wiki/`** — markdown do LLM sở hữu. Người đọc, LLM viết & maintain.
- **`CLAUDE.md`** — schema/sổ tay vận hành (đã tồn tại, sẽ cập nhật theo spec này).

## 4. Mô hình dữ liệu — Supplier-centric

```
                  ┌──────────────┐
   tư vấn  ◄────── │ Destination  │ ──► mùa, visa, an toàn, highlight, di chuyển nội vùng
                  └──────┬───────┘
                         │ "có nhà cung cấp tại"
                  ┌──────▼───────┐  rate sheet theo mùa + chất lượng + điều khoản + availability
   báo giá ◄───── │   Supplier   │ ◄── nguồn: hợp đồng, brochure, supplier list
                  └──────┬───────┘
                         │ "ráp vào"
                  ┌──────▼───────┐
   thiết kế ◄──── │ Tour Product │ ──► lịch trình mẫu tái dùng (theo ngày, theo chủ đề)
                  └──────┬───────┘
                         │ "instance hóa cho khách"
                  ┌──────▼───────┐
                  │ Quote/Trip   │ ──► báo giá cụ thể: ráp supplier+tour → giá vốn → giá bán
                  └──────────────┘
   Concept: seasonality · visa · markup-policy · an toàn (chủ đề ngang, liên kết tất cả)
```

| Thực thể | `type` | Phục vụ job |
|---|---|---|
| Destination | `destination` | Tư vấn + thiết kế |
| **Supplier** ⭐ | `supplier` | Báo giá + quản lý NCC |
| Tour Product | `tour-product` | Thiết kế lịch trình |
| Quote/Trip | `quote` | Báo giá + chốt đơn |
| Concept | `concept` | Tất cả |

## 5. Cơ chế hybrid giá & availability

**Nguyên tắc 3 tầng:**

| Tầng | Loại dữ liệu | Cách xử lý |
|---|---|---|
| 🟢 KB lưu | Giá hợp đồng theo mùa (KS, xe, guide) | `rate_sheets` trong frontmatter, có `valid_until` |
| 🟡 Kỷ luật ngày | Giá biến động vừa | Mọi giá có `valid_until` → Agent flag "giá cũ, cần xác nhận" |
| 🔴 Trỏ ra ngoài / live | Chỗ trống real-time; **giá vé máy bay** | `booking_source` (pointer) hoặc `price_source: "tool:fast-flights"` |

### 5.1 Supplier thường (hotel/transport/guide) — frontmatter

```yaml
---
type: supplier
category: hotel            # hotel|transport|guide|restaurant|activity|dmc|airline
short_name: ""             # khớp ShortName trong supplier-list (vd "LADALAT")
location: "[[destinations/da-lat]]"
quality_rating: 4          # /5, đánh giá nội bộ
contacts:
  sales: "Ms. Lan - 09xx - lan@hotel.com"
booking_source: "CRM / Suppliers2026.xlsx"   # pointer source-of-truth real-time
lead_time_days: 14
availability_notes: "Khó đặt T6-T8 & lễ tết; giữ chỗ trước 3 tuần"
rate_sheets:
  - season: "Cao điểm (T6-T8, lễ tết)"
    valid_until: 2026-12-31
    rates: { "Deluxe": 2500000, "Suite": 4000000 }   # VND, số nguyên (machine-readable)
  - season: "Thấp điểm"
    valid_until: 2026-12-31
    rates: { "Deluxe": 1600000 }
updated: 2026-06-23
sources: ["[[sources/hopdong-...]]"]
---
```

### 5.2 Supplier live-priced (airline) — frontmatter

```yaml
---
type: supplier
category: airline
short_name: "VJ"           # mã hãng
location: ""               # n/a
price_source: "tool:fast-flights"   # ◄ KHÔNG có rate_sheets; giá lấy live
commission: "7% trên giá vé"        # tri thức bền: hoa hồng/điều khoản
contract_terms: "[[sources/contract-tet-hong-ngoc-ha-2022]]"
contacts:
  sales: "..."
updated: 2026-06-23
sources: ["[[sources/contract-tet-hong-ngoc-ha-2022]]"]
---
```

**Quy tắc:** `category: airline` ⇒ không lưu `rate_sheets`; giá luôn live. Supplier khác ⇒ có `rate_sheets`.

## 6. Cấu trúc thư mục (điều chỉnh từ KB hiện có)

```
TravelKB/
├── CLAUDE.md                      # schema (cập nhật theo spec này)
├── raw/
│   ├── assets/                    # file gốc bất biến (xlsx/docx/pdf/doc)
│   ├── converted/                 # bản markdown từ MarkItDown (đã có 8 file)
│   └── README.md
├── wiki/
│   ├── index.md  log.md  overview.md
│   ├── destinations/              # tri thức điểm đến (tư vấn)
│   ├── suppliers/                 # MỚI: hotels/ transport/ guides/ restaurants/ activities/ airlines/ dmc/
│   ├── tours/
│   │   ├── tour-products/         # lịch trình mẫu tái dùng
│   │   └── quotes/                # báo giá đã duyệt (compound lại)
│   ├── concepts/                  # + markup-policy, seasonality, visa, an toàn
│   ├── sources/                   # tóm tắt từng nguồn đã ingest
│   └── synthesis/                 # so sánh NCC, phân tích mùa, lộ trình
├── templates/                     # + supplier.md, tour-product.md, quote.md
└── build/                         # MỚI: structured extract cho Agent (xem §8)
```

## 7. Templates mới

- `templates/supplier.md` — gồm 2 biến thể frontmatter ở §5.1 và §5.2.
- `templates/tour-product.md` — khung lịch trình theo ngày tái dùng (kế thừa `trip.md` cũ, thêm trường `theme`, `duration_days`, `default_suppliers`).
- `templates/quote.md` — **bám đúng cấu trúc** file `bao-gia-breakdown-khach-hang` (bản gửi khách) và tham chiếu `chiet-tinh-gia-noi-bo` (giá vốn nội bộ). Có 2 phần: bảng giá vốn (nội bộ) + bảng báo giá khách (xuất ra).

## 8. Structured extract — build step (giao diện KB → Agent)

Một bước build trích frontmatter → JSON cho Agent (Spec 2) dùng, để **tính giá deterministic, không để LLM làm toán tiền bạc**.

```
build/
├── suppliers.json     # [{short_name, category, location, rate_sheets[], valid_until, price_source}]
├── tour-products.json # [{slug, theme, duration_days, day_by_day[], default_suppliers[]}]
├── markup-policy.json # công thức markup/hoa hồng từ concepts/markup-policy.md
└── graph.json         # graphify graph (đã có) cho truy vấn quan hệ
```

**Data contract KB → Agent:**
- Agent **đọc**: `build/*.json` + `wiki/**/*.md` (narrative) + `build/graph.json`.
- Agent **ghi**: `wiki/tours/quotes/*.md` (mỗi báo giá đã duyệt = 1 trang → compound).
- Quy tắc tiền tệ: mọi giá là **số nguyên VND** trong frontmatter (không format chuỗi) để tính được.
- Vé máy bay: Agent gọi tool `flight_search(from,to,date,pax)` (fast-flights) thay vì đọc rate_sheets.

> Build step có thể đơn giản là script Python đọc YAML frontmatter → ghi JSON. Chi tiết hiện thực để Spec 2 hoặc một sub-task riêng; Spec 1 chỉ định nghĩa **schema đầu ra**.

## 9. Operations (gắn 4 job)

| Job | Ví dụ | Luồng |
|---|---|---|
| Tư vấn | "ĐN tháng 9 hợp không?" | đọc `destinations/da-nang` + `concepts/seasonality` → trả lời có căn cứ |
| Thiết kế | "Tour ĐN 4N3Đ, gia đình, tầm trung" | chọn `tour-products/` mẫu + ráp `suppliers/` → lịch trình theo ngày |
| Báo giá | "Báo giá tour trên 2NL+1TE" | rate_sheets + (vé: fast-flights) → giá vốn → +markup → **flag giá cũ** → `tours/quotes/` |
| Quản lý NCC | ingest hợp đồng mới | cập nhật `suppliers/`, rate sheet, synthesis so sánh, index + log |

**Ingest flow:** thả file vào `raw/assets/` → MarkItDown → `raw/converted/` → đọc → viết/ cập nhật trang supplier/tour/destination + `sources/` → cập nhật `index.md` + `log.md`.

## 10. Ánh xạ 8 file thật → entity (đã convert)

| File `raw/converted/` | → Entity |
|---|---|
| `bangkok-pattaya-5-ngay.md` | tour-product |
| `tour-phu-quoc-goi-khach.md` | tour-product |
| `bao-gia-breakdown-khach-hang.md` | quote (mẫu gửi khách) → cơ sở `templates/quote.md` |
| `chiet-tinh-gia-noi-bo.md` | quote (giá vốn nội bộ) |
| `chiet-tinh-quyet-toan-tour.md` | quote (quyết toán post-trip) |
| `supplier-list.md` | suppliers (DB vendor — xem §12 cảnh báo) |
| `contract-tet-hong-ngoc-ha-2022.md` | supplier airline (hoa hồng/điều khoản) |
| `template-lay-gia-hotel-corp.md` | mẫu rate sheet → tham chiếu `templates/supplier.md` |

## 11. Tooling

- **MarkItDown** (`.venv`, +ffmpeg) — convert nguồn → markdown. `.doc` legacy: `textutil -convert html` → MarkItDown.
- **fast-flights** (`.venv`, no-API, đã test SGN→BKK ra VND thật) — nguồn giá vé live cho Agent. Đóng gói được thành MCP server.
- **Graphify** (uv tool, +pdf/office) — graph tri thức cho Agent truy vấn quan hệ; rebuild khi KB đổi.

## 12. Rủi ro & lưu ý

- **`supplier-list.md` (1.2 MB) chứa dữ liệu nhạy cảm** (số TK ngân hàng, tên chủ TK hàng trăm vendor). Khi ingest: **trích lọc field cần** (short_name, legal_name, city, category) thay vì nhồi cả bảng vào wiki. **Thêm `.gitignore` loại trừ** file thô này; không commit dữ liệu ngân hàng.
- **fast-flights là scraper dễ vỡ** (reverse-engineer Protobuf Google). Cần **fallback nhập tay** khi tool lỗi; cache kết quả trong ngày; lưu lượng thấp (nội bộ) để giảm rủi ro chặn IP/ToS.
- **Giá vé = tham chiếu, không phải giá đặt** — báo giá phải ghi rõ "giá tham chiếu tại [thời điểm tra cứu]", chốt thật qua booking.

## 13. Tiêu chí nghiệm thu Spec 1 (Definition of Done)

1. `CLAUDE.md` cập nhật: mô hình 5 entity, hybrid 3 tầng, quy tắc airline live-priced, data contract KB→Agent.
2. Có `templates/supplier.md` (2 biến thể), `tour-product.md`, `quote.md` (bám mẫu thật).
3. Cấu trúc thư mục `wiki/suppliers/`, `wiki/tours/{tour-products,quotes}/`, `build/` tồn tại.
4. Ingest tối thiểu: ≥1 tour-product (Bangkok-Pattaya), ≥1 quote (từ chiet-tinh), ≥3 supplier (gồm 1 airline) từ 8 file thật.
5. `build/suppliers.json` + `build/tour-products.json` sinh ra đúng schema §8 từ frontmatter.
6. `.gitignore` loại trừ `supplier-list.md` thô và dữ liệu nhạy cảm.
7. `index.md` + `log.md` phản ánh các trang đã tạo.

## 14. Hoãn sang spec sau (out of scope Spec 1)

- Spec 2 (Agent): logic elicit nhu cầu, thuật toán chọn supplier/ráp tour, tool `flight_search`, tính markup, sinh báo giá.
- Spec 3 (Website): auth sales, chat UI, hiển thị tour/quote, nút xác nhận/xuất PDF.
- Hiện thực chi tiết build step (ngôn ngữ/CLI) — Spec 1 chỉ chốt schema đầu ra.

## 15. Câu hỏi mở

- Công thức markup nội bộ cụ thể (%, theo loại dịch vụ?) → cần để viết `concepts/markup-policy.md`. Có thể trích từ `chiet-tinh-gia-noi-bo`.
- Định dạng xuất báo giá cuối (PDF/Excel/markdown?) → ảnh hưởng `templates/quote.md`, nhưng quyết định ở Spec 3.

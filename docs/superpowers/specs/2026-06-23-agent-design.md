# Spec 2 — Agent tư vấn (Sales Copilot)

> Ngày: 2026-06-23 · Trạng thái: Draft chờ duyệt · Sub-project 2/3 của platform "AI Sales cho Tour Operator"

## 0. Bối cảnh & phạm vi

**Spec 2** đặc tả Lớp 2 (Agent tư vấn). Kế thừa Lớp 1 (Travel KB — `2026-06-23-travel-kb-design.md`),
là backend cho Lớp 3 (Website — spec sau).

```
LỚP 3 — WEBSITE nội bộ (Spec 3)   chat UI · duyệt/xuất báo giá
            │ gọi
LỚP 2 — AGENT tư vấn (SPEC NÀY)   elicit nhu cầu → thiết kế tour → sinh báo giá
            │ truy vấn / ghi
LỚP 1 — TRAVEL KB (Spec 1)        suppliers.json · tour-products.json · markup-policy · graph
```

**Người dùng:** đội sales (copilot nội bộ). Thấy đủ giá vốn; guardrail tối thiểu nhưng **bắt buộc lọc
supplier `confidential` khỏi output khách-facing**.

## 1. Mục tiêu (Goals)

- G1. Agent Python độc lập chạy CLI ngay, **tái dùng làm backend web** (Spec 3) không sửa lõi.
- G2. Bốn tool: `kb_query`, `flight_search`, `quote_calc`, `save_quote`.
- G3. **Tính giá deterministic bằng code** (không để LLM làm toán tiền).
- G4. Luồng: elicit nhu cầu → thiết kế tour từ KB → sinh báo giá theo mẫu → sales duyệt → file lại KB.
- G5. Lọc supplier `confidential: true` khỏi mọi bản gửi khách.

## 2. Không làm (Non-goals / YAGNI)

- ❌ Không đặt vé/booking thật — chỉ giá tham chiếu.
- ❌ LLM không tự tính tiền — `quote_calc` lo.
- ❌ Không làm web (Spec 3); chỉ tách module sạch để web gọi lại.
- ❌ Không tự sửa KB tự động ngoài `save_quote` (sales duyệt trước).
- ❌ Không multi-user/auth (Spec 3 lo).

## 3. Kiến trúc

**Anthropic Python SDK** (`pip install anthropic`) + tool-use loop. Dùng `@beta_tool` định nghĩa tool;
`client.beta.messages.tool_runner()` chạy vòng agentic tự động cho phần lớn, **manual loop** chèn chốt
duyệt ở `save_quote`.

```
agent/
├── __init__.py
├── tools.py         # 4 tool @beta_tool
├── pricing.py       # quote_calc — Python thuần, deterministic
├── kb.py            # load build/*.json, đọc wiki, graphify query
├── prompts.py       # system prompt (file riêng, ổn định → cache tốt)
├── conversation.py  # state máy: elicit → design → quote → confirm; manual gate ở save
└── cli.py           # entrypoint sales gõ; in hội thoại + bảng báo giá
```

Chạy: `.venv/bin/python -m agent.cli`. Web (Spec 3) import `agent.conversation` thay vì `cli`.

### 3.1 Model
- **Mặc định `claude-sonnet-4-6`** (sales copilot lưu lượng cao, tool-orchestration chủ yếu thẳng).
- **Nâng `claude-opus-4-8`** cho ca thiết kế tour phức tạp (cấu hình qua env `AGENT_MODEL`).
- **Adaptive thinking** bật: `thinking={"type":"adaptive"}`; `output_config={"effort":"medium"}` mặc định,
  `high` cho thiết kế tour.
- Auth: `ANTHROPIC_API_KEY` (env). `max_tokens` ~16000 (non-stream) / ~64000 (stream cho web).

## 4. Bốn tool

| Tool | Input | Output | Nguồn |
|---|---|---|---|
| `kb_query(question, audience)` | câu hỏi NL + `internal\|customer` | trang/NCC/tour liên quan | `build/*.json` + graphify graph + đọc wiki; **lọc `confidential` khi `audience=customer`** |
| `flight_search(origin, dest, date, pax)` | mã sân bay + ngày + số khách | [hãng, giá VND tham chiếu, giờ, chặng] | **fast-flights** (local, no-API; đã test SGN-BKK/SGN-PQC) |
| `quote_calc(line_items, season, pax)` | danh sách dịch vụ + mùa + cơ cấu khách | bảng giá vốn + giá bán + margin | `pricing.py` + `markup-policy.json` |
| `save_quote(quote_md, slug)` | nội dung báo giá đã duyệt | path trang đã ghi | ghi `wiki/tours/quotes/<slug>.md`; **manual gate — sales duyệt** |

`flight_search` cần fallback nhập tay khi fast-flights lỗi (scraper dễ vỡ) → tool trả cờ `error`,
agent hỏi sales nhập giá vé tay.

## 5. Tính giá deterministic (`pricing.py`)

Hàm Python thuần, **không gọi LLM**:
```
quote_calc(line_items, season, pax):
  for item in line_items:                       # supplier + hạng + số lượng/đêm
    rate = suppliers.json[item.supplier].rate_sheets[season].rates[item.class]  # int VND
    cost += rate * item.qty
  # vé máy bay: lấy từ flight_search (không từ rate_sheets)
  land_sell  = land_cost  / (1 - 0.19)          # markup land ~19%  (markup-policy.json)
  air_sell   = air_cost  * (1 + commission)     # vé gần pass-through
  total = (land_sell + air_sell) * (1 + 0.08)   # VAT 8%
  return { cost_table, sell_table, margin }
```
- Mọi con số là **số nguyên VND**. LLM chỉ chọn `line_items` và gọi tool.
- `quote_calc` đọc `valid_until` → đính cờ "giá [[supplier]] hết hạn, cần xác nhận" vào output.
- Công thức markup lấy từ `concepts/markup-policy.md` → `build/markup-policy.json` (cần thêm vào build step).

## 6. Luồng hội thoại (`conversation.py`)

State machine 4 pha; slot bắt buộc: điểm đến, số ngày, số khách (NL/TE), mùa/ngày, phong cách/ngân sách.

```
1. ELICIT   — hỏi slot còn thiếu (1 câu/lượt). Đủ slot → sang DESIGN.
2. DESIGN   — kb_query chọn tour-product mẫu + ráp suppliers; trình khung lịch trình; sales chỉnh.
3. QUOTE    — flight_search (nếu có bay) + quote_calc → bảng giá vốn (nội bộ) + báo giá khách.
4. CONFIRM  — sales duyệt → save_quote (MANUAL GATE) → trang vào KB; hoặc quay lại DESIGN.
```

`save_quote` chỉ chạy sau khi sales xác nhận rõ ràng (manual loop, không tự động).

## 7. Guardrail (kế thừa Spec 1)

- `kb_query(audience="customer")` và bản báo giá khách **loại supplier `confidential: true`** (Mường Thanh):
  không hiện giá hợp đồng/giá vốn trong output khách-facing.
- Bảng giá vốn nội bộ chỉ in ở phần "NỘI BỘ"; bản xuất khách chỉ có giá bán trọn gói.
- Vé máy bay ghi rõ "giá tham chiếu tại [thời điểm tra cứu]".

## 8. Giao diện Agent ↔ Lớp khác

- **Đọc từ KB:** `build/suppliers.json`, `build/tour-products.json`, `build/markup-policy.json`,
  `build/graph.json`, các trang `wiki/**/*.md`.
- **Ghi vào KB:** `wiki/tours/quotes/*.md` qua `save_quote`.
- **Web (Spec 3) gọi:** `agent.conversation.Session` (start/send/get_state) — không phụ thuộc CLI.

## 9. Tiêu chí nghiệm thu (Definition of Done)

1. `pip install anthropic` + fast-flights trong `.venv`; `agent/` import được.
2. 4 tool `@beta_tool` chạy; `quote_calc` cho kết quả khớp tay trên ca Phú Quốc thật (margin ~11,76%).
3. `build/markup-policy.json` sinh từ `concepts/markup-policy.md`.
4. CLI chạy 1 hội thoại end-to-end: elicit → design → quote → save (tạo 1 trang `quotes/`).
5. `kb_query(audience="customer")` không trả supplier `confidential`.
6. fast-flights lỗi → agent fallback hỏi giá vé tay (không crash).
7. `save_quote` chỉ ghi sau xác nhận của sales (manual gate).

## 10. Hoãn sang Spec 3

- Web auth sales, chat UI, render bảng báo giá, nút duyệt/xuất PDF/Excel, lịch sử hội thoại.

## 11. Câu hỏi mở

- Mã sân bay cho `flight_search`: map tên thành phố → IATA (SGN/HAN/PQC/DAD...) — cần bảng tra nhỏ.
- Markup chính thức: spec dùng tham chiếu 11,76%/19,22% từ 1 tour; cần lãnh đạo xác nhận % chuẩn
  trước khi agent tự báo giá ra khách (đã ghi cảnh báo trong `concepts/markup-policy.md`).

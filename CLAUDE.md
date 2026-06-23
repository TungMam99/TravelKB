# Travel Knowledge Base — Schema & Operating Manual

Đây là **Travel Knowledge Base** xây theo pattern "LLM Wiki" của Karpathy (xem `Pattern/llmwiki.md`).
Bạn (LLM) là **người duy trì wiki** — không phải chatbot. Bạn đọc nguồn thô, trích xuất tri thức,
và **tích hợp** vào wiki hiện có: cập nhật trang entity, sửa tóm tắt, đánh dấu mâu thuẫn, giữ
cross-reference nhất quán. Tri thức được **biên dịch một lần và giữ luôn cập nhật**, không phải
truy xuất lại từ đầu mỗi câu hỏi.

> Con người phụ trách: tìm nguồn, khám phá, đặt câu hỏi đúng.
> LLM phụ trách: tóm tắt, cross-reference, filing, bookkeeping — mọi việc còn lại.

## Ngôn ngữ & quy ước viết
- Nội dung viết bằng **tiếng Việt**, giữ nguyên **thuật ngữ / tên riêng tiếng Anh** khi tự nhiên hơn
  (tên địa danh quốc tế, "check-in", "visa on arrival", "shoulder season"...).
- Tên file: **kebab-case, không dấu** (`hoi-an.md`, `tokyo.md`, `trip-japan-2026-04.md`).
- Mỗi trang mở đầu bằng **YAML frontmatter** (cho Obsidian Dataview) + một dòng tóm tắt.
- Liên kết nội bộ dùng cú pháp Obsidian: `[[hoi-an]]`, `[[concepts/visa-vietnam|visa Việt Nam]]`.
  Link **rộng tay** — một `[[name]]` chưa tồn tại là việc cần viết sau, không phải lỗi.

## Kiến trúc 3 lớp

**1. `raw/` — Nguồn thô (BẤT BIẾN).**
Tài liệu gốc: bài viết clip về markdown, PDF, ảnh, file dữ liệu. LLM **chỉ đọc, không bao giờ sửa**.
Đây là source of truth. Ảnh để trong `raw/assets/`. Dùng MarkItDown (`.venv/bin/markitdown`) để
chuyển PDF/DOCX/audio/web sang markdown trước khi ingest.

**2. `wiki/` — Wiki (LLM sở hữu hoàn toàn).**
Các trang markdown do LLM tạo. Bạn tạo trang, cập nhật khi có nguồn mới, duy trì cross-reference.
Con người đọc; LLM viết.

**3. `CLAUDE.md` — Schema (file này).**
Quy ước cấu trúc, page format, workflow. Bạn và con người **đồng tiến hóa** file này theo thời gian.

## Cấu trúc thư mục `wiki/`

```
wiki/
├── index.md          # Catalog nội dung — cập nhật MỖI lần ingest
├── log.md            # Nhật ký chronological (append-only)
├── overview.md       # Bức tranh tổng + thesis đang tiến hóa
├── destinations/     # Điểm đến: quốc gia → vùng → thành phố (phân cấp)
├── trips/            # Trang lập kế hoạch từng chuyến đi cụ thể
├── entities/         # POI, khách sạn, nhà hàng, hãng bay, phương tiện
├── concepts/         # Visa, mùa/thời tiết, ngân sách, an toàn, văn hóa, packing
├── sources/          # 1 trang tóm tắt cho MỖI nguồn đã ingest
└── synthesis/        # Phân tích cross-cutting, bảng so sánh, lộ trình gợi ý
```

### Các loại trang (`type` trong frontmatter)
- `destination` — quốc gia / vùng / thành phố. Field `level: country|region|city`, `parent: [[...]]`.
- `trip` — một chuyến đi. Có `status`, `dates`, `budget`, `travelers`, lịch trình theo ngày.
- `entity` — POI / khách sạn / nhà hàng / transport. Field `category`.
- `concept` — chủ đề ngang (visa, seasonality, budgeting, safety, food-culture, packing).
- `source` — tóm tắt 1 nguồn đã ingest, link ngược về file trong `raw/`.
- `synthesis` — so sánh, phân tích, lộ trình tổng hợp từ nhiều trang.

Template cho mỗi loại nằm trong `templates/`.

## Operations (quy trình)

### Ingest — nạp nguồn mới
Khi con người thả nguồn vào `raw/` và yêu cầu xử lý:
1. (Nếu không phải .md) chuyển bằng MarkItDown sang markdown.
2. Đọc kỹ nguồn. Trao đổi với con người về key takeaways.
3. Viết một trang `sources/<slug>.md` tóm tắt nguồn (link ngược về file raw).
4. **Cập nhật / tạo** các trang destination, entity, concept, trip liên quan
   (một nguồn thường chạm 10–15 trang). Đánh dấu mâu thuẫn với claim cũ thay vì xóa lặng.
5. Cập nhật `index.md`.
6. Append một dòng vào `log.md` theo format chuẩn.

Mặc định ingest **từng nguồn một** và giữ con người trong vòng lặp. Có thể batch nếu được yêu cầu.

### Query — trả lời câu hỏi
1. Đọc `index.md` trước để tìm trang liên quan, rồi drill vào.
2. Tổng hợp câu trả lời **có trích dẫn** (link `[[...]]` tới trang nguồn).
3. **Câu trả lời tốt nên được file lại** thành trang mới trong `wiki/` (thường ở `synthesis/`)
   — đừng để phân tích biến mất vào chat history. Cập nhật index + log khi làm vậy.
4. Output có thể là: trang markdown, bảng so sánh, slide (Marp), biểu đồ (matplotlib).

### Lint — kiểm tra sức khỏe wiki
Khi được yêu cầu health-check, tìm:
- Mâu thuẫn giữa các trang.
- Claim cũ đã bị nguồn mới thay thế (stale).
- Orphan page (không có inbound link).
- Concept quan trọng được nhắc nhưng chưa có trang riêng.
- Thiếu cross-reference.
- Data gap có thể lấp bằng web search.
Gợi ý câu hỏi mới để điều tra và nguồn mới nên tìm.

## File điều hướng

**`index.md`** — content-oriented. Catalog mọi trang: link + tóm tắt 1 dòng + metadata,
nhóm theo category. Cập nhật **mỗi lần ingest**. Đọc đầu tiên khi query.

**`log.md`** — chronological, append-only. Mỗi entry bắt đầu bằng prefix nhất quán:
```
## [YYYY-MM-DD] <op> | <tiêu đề>
```
với `<op>` ∈ {ingest, query, lint, maintain}. Nhờ prefix này, log parse được bằng unix:
`grep "^## \[" wiki/log.md | tail -5` → 5 entry gần nhất.

## Công cụ
- **MarkItDown** (`.venv/bin/markitdown <file>`): chuyển PDF/DOCX/XLSX/PPTX/audio/web → markdown.
  ffmpeg đã cài (hỗ trợ phiên âm audio). Đây là cầu nối đưa nguồn non-markdown vào `raw/`.
- Wiki là git repo của file markdown → có version history miễn phí (chạy `git init` khi muốn).
- Khi wiki lớn (~100+ nguồn), cân nhắc thêm search engine (vd qmd) — hiện `index.md` là đủ.

## Nguyên tắc cốt lõi
Phần tốn công của một KB không phải đọc hay nghĩ — mà là **bookkeeping**: cập nhật cross-reference,
giữ tóm tắt cập nhật, ghi nhận khi dữ liệu mới mâu thuẫn dữ liệu cũ, giữ nhất quán across hàng chục
trang. LLM không chán, không quên cập nhật một cross-reference, chạm 15 file trong một lượt. Wiki
được duy trì vì chi phí duy trì gần bằng 0. Wiki giàu lên sau **mỗi nguồn** và **mỗi câu hỏi**.

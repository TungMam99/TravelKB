# Log — Travel Knowledge Base

Nhật ký chronological, **append-only**. Mỗi entry bắt đầu bằng prefix nhất quán để parse bằng unix:
`grep "^## \[" wiki/log.md | tail -5`.

Format: `## [YYYY-MM-DD] <op> | <tiêu đề>` với `<op>` ∈ {ingest, query, lint, maintain}.

---

## [2026-06-23] maintain | Khởi tạo Travel KB
Dựng cấu trúc 3 lớp theo pattern LLM Wiki (`Pattern/llmwiki.md`): `raw/` (nguồn thô bất biến),
`wiki/` (LLM sở hữu), `CLAUDE.md` (schema). Tạo `index.md`, `log.md`, `overview.md`, templates.
Cài MarkItDown + ffmpeg làm cầu nối chuyển nguồn non-markdown sang markdown.
Cấu hình: Trip + Destination, tiếng Việt giữ thuật ngữ Anh, phạm vi toàn cầu.

## [2026-06-23] maintain | Spec 1 (Tour Operator KB) + ingest tối thiểu
Pivot sang tour operator (sales copilot). Viết Spec 1 (`docs/superpowers/specs/2026-06-23-travel-kb-design.md`):
mô hình 5 entity Supplier-centric, hybrid giá 3 tầng, airline live-priced qua fast-flights (POC SGN-BKK OK).
git init + commit f4d37df. Cài fast-flights vào .venv.

## [2026-06-23] ingest | 3 nguồn thật → 11 trang
Ingest từ raw/converted: tour Bangkok-Pattaya, chiết tính Phú Quốc, hợp đồng TET.
Tạo: 2 destinations (phu-quoc, bangkok), 3 suppliers (vietjet airline live-priced, BW Sonasea, Long Beach transport),
1 tour-product (bangkok-pattaya-5n4d), 1 quote (phu-quoc đoàn 44k, lãi 56,9tr), 1 concept (markup-policy 11,76%/19,22%),
3 sources. Sinh build/{suppliers,tour-products}.json qua build/extract_kb.py.
⚠️ Phát hiện: contract-TET là hợp đồng KHÁCH B2B, không phải supplier → gap model, cần entity "Client".

## [2026-06-23] ingest | 2 hotel supplier: Galaxy 3 + Mường Thanh Cần Thơ
Convert + ingest: Galaxy 3 Vũng Tàu (bảng giá công bố 2023, 400k–1tr) và Mường Thanh Cần Thơ
(HĐ nguyên tắc 2023, 1,55–12tr). Tạo 2 supplier hotel + 2 destination (vung-tau, can-tho) + 2 source.
suppliers.json: 3→5. Thêm field `confidential` vào build extract.
⚠️ Mường Thanh: HĐ CẤM lộ giá ra bên thứ ba/website → gắn `confidential: true`; Agent/Website
(Spec 2/3) phải lọc supplier confidential khỏi mọi output khách-facing.

## [2026-06-23] maintain | Code Spec 2 — Agent sales copilot
Viết Spec 2 (`docs/superpowers/specs/2026-06-23-agent-design.md`) + hiện thực module `agent/`:
pricing (deterministic), kb (lọc confidential), flight (fast-flights + fallback), tools (4 tool + save gate),
conversation (manual loop human-in-the-loop), cli, selftest. Cài anthropic SDK 0.111 vào .venv.
Thêm `build/markup-policy.json` (margin 11,76%/19,22% từ frontmatter markup-policy.md).
selftest PASS 5/5 (không cần API key): quote_calc margin chưa-vé 19.22% khớp sheet thật, lọc confidential,
flight fallback, loop+save gate. LLM live cần ANTHROPIC_API_KEY.

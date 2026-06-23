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

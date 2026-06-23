# Travel Knowledge Base 🌍

Một knowledge base du lịch cá nhân theo pattern **LLM Wiki** của Karpathy: một wiki markdown
liên kết, **tích lũy dần** do AI duy trì — thay vì RAG truy xuất lại từ đầu mỗi câu hỏi.

**Obsidian là IDE · LLM là lập trình viên · wiki là codebase.**
Bạn lo tìm nguồn + đặt câu hỏi; AI lo tóm tắt, cross-reference, filing, bookkeeping.

## Cấu trúc
```
TravelKB/
├── CLAUDE.md      # ⭐ Schema — quy ước + workflow cho LLM (đọc file này trước)
├── raw/           # Nguồn thô BẤT BIẾN (articles, PDF, ảnh, booking...)
│   └── assets/    #   ảnh
├── wiki/          # LLM sở hữu hoàn toàn
│   ├── index.md   #   catalog mọi trang (đọc đầu tiên khi query)
│   ├── log.md     #   nhật ký append-only
│   ├── overview.md#   bức tranh tổng + thesis
│   ├── destinations/  #   điểm đến: quốc gia → vùng → thành phố
│   ├── trips/         #   chuyến đi cụ thể
│   ├── entities/      #   POI, khách sạn, nhà hàng, transport
│   ├── concepts/      #   visa, mùa, ngân sách, an toàn, văn hóa...
│   ├── sources/       #   tóm tắt từng nguồn
│   └── synthesis/     #   so sánh, phân tích, lộ trình
├── templates/     # Mẫu cho mỗi loại trang
└── Pattern/       # Tài liệu pattern gốc (llmwiki, markitdown)
```

## Dùng thế nào
1. **Nạp nguồn:** thả file vào `raw/` → bảo AI *"ingest raw/<file>"*.
   File non-markdown? Chuyển trước: `.venv/bin/markitdown raw/x.pdf -o raw/x.md`.
2. **Hỏi:** đặt câu hỏi bất kỳ — AI đọc `index.md`, tổng hợp có trích dẫn, file câu trả lời tốt vào `synthesis/`.
3. **Lint:** thỉnh thoảng bảo AI *"health-check wiki"* để tìm mâu thuẫn, orphan, data gap.

## Cấu hình hiện tại
Trip + Destination · nội dung tiếng Việt giữ thuật ngữ Anh · phạm vi toàn cầu.

## Công cụ
- **MarkItDown** (venv Python 3.12 tại `.venv/`) + **ffmpeg** — chuyển PDF/DOCX/audio/web → markdown.
- Wiki là git repo markdown → chạy `git init` để có version history.

# raw/ — Nguồn thô (BẤT BIẾN)

Đây là **source of truth**. Thả tài liệu gốc vào đây: bài viết clip (.md), PDF guide, ảnh menu/bản đồ,
file booking, transcript audio... LLM **chỉ đọc, không bao giờ sửa** thư mục này.

## Quy ước
- Đặt ảnh trong `raw/assets/`.
- File non-markdown (PDF/DOCX/XLSX/PPTX/audio/web) → chuyển sang markdown bằng MarkItDown trước khi ingest:
  ```bash
  .venv/bin/markitdown raw/guide-tokyo.pdf -o raw/guide-tokyo.md
  ```
- Đặt tên file gợi nhớ nguồn + ngày nếu cần (`lonelyplanet-japan-2026.md`).

## Sau khi thả nguồn
Yêu cầu: *"ingest raw/<file>"* — LLM sẽ đọc, viết trang tóm tắt trong `wiki/sources/`,
cập nhật các trang destination/entity/concept/trip liên quan, rồi cập nhật index + log.

# web/ — Website nội bộ (Spec 3)

Giao diện Streamlit cho sales, bọc quanh `agent.Session` (Lớp 2). Không sửa agent.

## Chạy

```bash
ANTHROPIC_API_KEY='sk-ant-...' .venv/bin/streamlit run web/app.py
# mở http://localhost:8501
```

Không có key → trang hiện thông báo, không crash.

## Tính năng (MVP)
- Chat với agent: mô tả nhu cầu khách → khung tour + bảng báo giá (render markdown).
- **Save gate:** khi agent muốn lưu → nút **✅ Duyệt lưu / ❌ Không** (thay y/n của CLI).
- Sidebar: chọn model (Sonnet/Opus), thống kê KB, nút "Hội thoại mới".
- Mỗi browser = 1 phiên (`st.session_state`).

## Chưa làm (sau)
Auth/phân quyền · xuất PDF/Excel · lịch sử quote · mở cho khách self-serve.

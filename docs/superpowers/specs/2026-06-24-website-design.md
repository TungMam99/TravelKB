# Spec 3 — Website nội bộ (Streamlit)

> Ngày: 2026-06-24 · Trạng thái: Draft · Sub-project 3/3 của platform "AI Sales cho Tour Operator"

## 0. Bối cảnh & phạm vi

**Spec 3** = Lớp 3 (giao diện). Bọc quanh agent `Session` (Lớp 2 đã code & test live). Không sửa agent.

```
LỚP 3 — WEBSITE (SPEC NÀY)   Streamlit: chat · bảng báo giá · nút duyệt lưu
            │ gọi Session.send / approve_save
LỚP 2 — AGENT (Spec 2 ✅)     elicit → design → quote → confirm
LỚP 1 — TRAVEL KB (Spec 1 ✅) suppliers/tours/markup + graph
```

**Người dùng:** sales nội bộ. **Không auth** (chạy nội bộ; mở cho khách là việc sau).

## 1. Mục tiêu

- G1. Web Streamlit dùng được ngay: chat với agent, xem báo giá render đẹp, duyệt lưu bằng nút.
- G2. Tái dùng 100% `agent.conversation.Session` — không sửa Lớp 2.
- G3. Save gate (human-in-the-loop) chuyển từ y/n CLI sang **nút Duyệt/Không**.

## 2. Không làm (YAGNI)

- ❌ Auth / multi-user / DB phiên (mỗi browser = 1 `st.session_state`).
- ❌ Xuất PDF/Excel báo giá (giai đoạn sau).
- ❌ Mở cho khách self-serve (vẫn sales-internal).
- ❌ Không sửa logic agent.

## 3. Kiến trúc

```
web/
├── app.py      # Streamlit app
└── README.md
```

- `app.py` thêm repo-root vào `sys.path` để import `agent` bất kể cwd.
- `Session` lưu trong `st.session_state["session"]`; lịch sử hiển thị trong `st.session_state["history"]`.
- `ANTHROPIC_API_KEY` từ env (không nhúng). Thiếu key → `st.error` + `st.stop`.
- Đổi model ở sidebar → tạo `Session` mới (reset hội thoại).

## 4. Thành phần `app.py`

| Phần | Hành vi |
|---|---|
| Sidebar | Chọn model (`claude-sonnet-4-6` / `claude-opus-4-8`), thống kê KB (suppliers/tours), nút "Hội thoại mới" |
| Chat | Render `st.session_state.history` qua `st.chat_message`; nhập bằng `st.chat_input` |
| Gửi | `Session.send(prompt)` (có `st.spinner`); append text trả về vào history |
| Save gate | Khi `state=awaiting_save_approval` → 2 nút [✅ Duyệt lưu] / [❌ Không]; gọi `approve_save(bool)` |
| Lỗi key | Không có `ANTHROPIC_API_KEY` → thông báo + dừng |

## 5. Chạy

```bash
ANTHROPIC_API_KEY='sk-ant-...' .venv/bin/streamlit run web/app.py
```

## 6. Tiêu chí nghiệm thu (DoD)

1. `streamlit` cài trong `.venv`; `web/app.py` `py_compile` sạch, import `agent` OK từ repo root.
2. Chạy `streamlit run` → mở chat; gửi yêu cầu → agent trả khung tour + báo giá (giống demo live).
3. Khi agent muốn lưu → hiện 2 nút; bấm Duyệt → tạo trang trong `wiki/tours/quotes/`; bấm Không → không ghi.
4. Đổi model ở sidebar → hội thoại reset.
5. Không có key → thông báo rõ, không crash.

## 7. Hoãn / mở rộng sau

- Auth + phân quyền, xuất PDF/Excel, lịch sử quote, browse supplier, mở cho khách (cần bật lại guardrail mạnh).

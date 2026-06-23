"""Sales Copilot — web nội bộ (Spec 3, Streamlit). Wrap agent.Session, không sửa Lớp 2.
Chạy: ANTHROPIC_API_KEY='sk-ant-...' .venv/bin/streamlit run web/app.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# cho import `agent` bất kể cwd (streamlit set path theo thư mục script)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st  # noqa: E402

from agent import kb  # noqa: E402
from agent.conversation import Session  # noqa: E402

MODELS = ["claude-sonnet-4-6", "claude-opus-4-8"]

st.set_page_config(page_title="Sales Copilot — Hồng Ngọc Hà", page_icon="🧭", layout="wide")

# ---- Sidebar ----------------------------------------------------------------
with st.sidebar:
    st.header("🧭 Sales Copilot")
    st.caption("Hồng Ngọc Hà · nội bộ")
    model = st.selectbox("Model", MODELS, index=0,
                         help="Sonnet rẻ/đủ dùng; Opus cho ca khó")
    st.divider()
    st.subheader("📚 Travel KB")
    try:
        st.metric("Nhà cung cấp", len(kb.load_suppliers("internal")))
        st.metric("Tour mẫu", len(kb.load_tour_products()))
        pol = kb.load_markup_policy()
        if not pol.get("confirmed"):
            st.warning("⚠️ Markup chưa được lãnh đạo chuẩn hóa.", icon="⚠️")
    except Exception as e:  # build/*.json chưa có
        st.error(f"KB chưa sẵn sàng: {e}")
    st.divider()
    if st.button("🔄 Hội thoại mới", use_container_width=True):
        for k in ("session", "history", "pending"):
            st.session_state.pop(k, None)
        st.rerun()

# ---- Key check --------------------------------------------------------------
if not os.environ.get("ANTHROPIC_API_KEY"):
    st.error("Chưa có **ANTHROPIC_API_KEY** trong môi trường.\n\n"
             "Chạy lại: `ANTHROPIC_API_KEY='sk-ant-...' .venv/bin/streamlit run web/app.py`")
    st.stop()

# ---- Session state ----------------------------------------------------------
if "session" not in st.session_state or st.session_state.get("model") != model:
    st.session_state.session = Session(model=model)
    st.session_state.history = []      # [{role, content}] để hiển thị
    st.session_state.pending = None    # dict pending_save khi chờ duyệt
    st.session_state.model = model

session: Session = st.session_state.session

st.title("Trợ lý báo giá tour")
st.caption("Mô tả nhu cầu khách → agent dựng khung tour + bảng báo giá. Giá vé live, tính tiền deterministic.")

# ---- Lịch sử hội thoại ------------------------------------------------------
for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---- Save gate (human-in-the-loop) -----------------------------------------
if st.session_state.pending is not None:
    with st.chat_message("assistant"):
        st.info("💾 Agent muốn **lưu báo giá này** vào KB. Bạn duyệt?")
        c1, c2 = st.columns(2)
        if c1.button("✅ Duyệt lưu", use_container_width=True, type="primary"):
            res = session.approve_save(True)
            st.session_state.history.append(
                {"role": "assistant", "content": res["text"] or "✅ Đã lưu báo giá vào KB."})
            st.session_state.pending = None
            st.rerun()
        if c2.button("❌ Không lưu", use_container_width=True):
            res = session.approve_save(False)
            st.session_state.history.append(
                {"role": "assistant", "content": res["text"] or "Đã bỏ qua, không lưu."})
            st.session_state.pending = None
            st.rerun()

# ---- Ô nhập (khóa khi đang chờ duyệt) --------------------------------------
prompt = st.chat_input("Ví dụ: Khách muốn Phú Quốc 4N3Đ, 2 người lớn, tầm trung, đi 2026-09-15",
                       disabled=st.session_state.pending is not None)
if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.spinner("Agent đang tra KB, giá vé & ráp báo giá…"):
        res = session.send(prompt)
    st.session_state.history.append({"role": "assistant", "content": res["text"]})
    if res["state"] == "awaiting_save_approval":
        st.session_state.pending = res.get("pending_save", True)
    st.rerun()

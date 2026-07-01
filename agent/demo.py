"""Non-interactive live demo of the sales copilot (1 scripted turn).
Reads ANTHROPIC_API_KEY from the environment — never hardcode the key here.

Run (bạn tự chạy, key truyền qua env, KHÔNG lưu vào file):
    ANTHROPIC_API_KEY='sk-ant-...' .venv/bin/python -m agent.demo
"""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
load_dotenv("api.env")

QUERY = ("Khách muốn tour Phú Quốc 4 ngày 3 đêm cho 2 người lớn, mức tầm trung, "
         "khởi hành 2026-09-15. Hãy đề xuất khung tour và ráp một bảng báo giá sơ bộ.")


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("✋ Cần ANTHROPIC_API_KEY trong môi trường. Ví dụ:\n"
              "   ANTHROPIC_API_KEY='sk-ant-...' .venv/bin/python -m agent.demo",
              file=sys.stderr)
        return 1

    from .conversation import Session
    s = Session()
    print(f"model: {s.model}\n👤 {QUERY}\n")
    result = s.send(QUERY)
    print(f"🧭 {result['text']}\n")

    # Demo KHÔNG lưu — tự từ chối nếu agent muốn save_quote (giữ KB sạch khi thử)
    if result["state"] == "awaiting_save_approval":
        result = s.approve_save(False)
        print(f"🧭 (demo không lưu) {result['text']}\n")

    print("✅ Live path OK — agent đọc KB thật + tính giá deterministic.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

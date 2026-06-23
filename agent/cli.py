"""CLI entrypoint for the sales copilot (Spec 2).
Run: .venv/bin/python -m agent.cli      (needs ANTHROPIC_API_KEY)
"""
from __future__ import annotations

import os
import sys

from .conversation import Session


def _handle(result, session: Session):
    print(f"\n🧭 {result['text']}\n")
    while result["state"] == "awaiting_save_approval":
        ans = input("💾 Lưu báo giá này vào KB? [y/N] ").strip().lower()
        result = session.approve_save(ans in ("y", "yes", "có", "co"))
        if result["text"]:
            print(f"\n🧭 {result['text']}\n")


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("✋ Cần đặt ANTHROPIC_API_KEY để chạy agent (LLM).", file=sys.stderr)
        print("   Phần deterministic (pricing/kb/flight) test được không cần key:",
              file=sys.stderr)
        print("   .venv/bin/python -m agent.selftest", file=sys.stderr)
        return 1
    session = Session()
    print("=== Sales Copilot — Hồng Ngọc Hà ===  (Ctrl-C để thoát)")
    print(f"model: {session.model}\n")
    print("Ví dụ: 'Khách muốn Phú Quốc 4N3Đ, 2 người lớn, tầm trung, đi tháng 9'\n")
    try:
        while True:
            text = input("👤 ").strip()
            if not text:
                continue
            _handle(session.send(text), session)
    except (KeyboardInterrupt, EOFError):
        print("\nTạm biệt!")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

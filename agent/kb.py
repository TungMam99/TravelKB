"""KB access layer (Spec 2 §8). Loads build/*.json + searches wiki.
Enforces the confidential-supplier guardrail (Spec 1 finding) at audience=customer.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
WIKI = ROOT / "wiki"


def _load(name: str):
    p = BUILD / name
    if not p.exists():
        raise FileNotFoundError(
            f"{p} chưa có — chạy `.venv/bin/python build/extract_kb.py` trước.")
    return json.loads(p.read_text(encoding="utf-8"))


def load_suppliers(audience: str = "internal") -> list[dict]:
    """audience='customer' → loại supplier confidential khỏi kết quả."""
    sups = _load("suppliers.json")
    if audience == "customer":
        sups = [s for s in sups if not s.get("confidential")]
    return sups


def load_tour_products() -> list[dict]:
    return _load("tour-products.json")


def load_markup_policy() -> dict:
    return _load("markup-policy.json")


def get_supplier(slug: str, audience: str = "internal") -> dict | None:
    for s in load_suppliers(audience):
        if s["slug"] == slug:
            return s
    return None


def search_wiki(question: str, limit: int = 6) -> list[dict]:
    """Tìm naive theo từ khóa trên các trang wiki (đủ ở scale nhỏ; sau dùng graphify)."""
    terms = [t for t in re.findall(r"\w+", question.lower()) if len(t) > 2]
    hits = []
    for p in WIKI.rglob("*.md"):
        if p.name in ("index.md", "log.md"):
            continue
        text = p.read_text(encoding="utf-8")
        low = text.lower()
        score = sum(low.count(t) for t in terms)
        if score:
            title = next((ln[2:].strip() for ln in text.splitlines()
                          if ln.startswith("# ")), p.stem)
            hits.append({"page": str(p.relative_to(ROOT)), "title": title, "score": score})
    hits.sort(key=lambda h: -h["score"])
    return hits[:limit]


def kb_query(question: str, audience: str = "internal") -> dict:
    """Tool backend: trả suppliers/tours liên quan + trang wiki, tôn trọng audience."""
    return {
        "audience": audience,
        "suppliers": load_suppliers(audience),
        "tour_products": load_tour_products(),
        "pages": search_wiki(question),
        "note": ("Đã LỌC supplier bảo mật (confidential) khỏi kết quả khách-facing."
                 if audience == "customer" else
                 "Bản nội bộ — gồm cả supplier confidential + giá vốn."),
    }

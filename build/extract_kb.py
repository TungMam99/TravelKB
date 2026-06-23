#!/usr/bin/env python3
"""Build step: trích frontmatter wiki → JSON cho Agent (Spec 1 §8).
Đọc suppliers + tour-products, ghi build/suppliers.json + build/tour-products.json.
Chạy: .venv/bin/python build/extract_kb.py
"""
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"


def parse_frontmatter(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None


def collect(subdir, wanted_type):
    out = []
    for p in sorted((WIKI / subdir).rglob("*.md")):
        fm = parse_frontmatter(p)
        if not fm or fm.get("type") != wanted_type:
            continue
        fm["_slug"] = p.stem
        fm["_path"] = str(p.relative_to(ROOT))
        out.append(fm)
    return out


def markup_policy():
    """Trích frontmatter concepts/markup-policy.md → dict cho Agent quote_calc."""
    p = WIKI / "concepts" / "markup-policy.md"
    fm = parse_frontmatter(p) or {}
    return {
        "margin_incl_air": fm.get("margin_incl_air"),
        "margin_excl_air": fm.get("margin_excl_air"),
        "land_markup": fm.get("land_markup"),
        "vat": fm.get("vat"),
        "confirmed": bool(fm.get("confirmed")),
        "source": "wiki/concepts/markup-policy.md",
    }


def main():
    suppliers = collect("suppliers", "supplier")
    tours = collect("tours/tour-products", "tour-product")

    # suppliers.json — gọn cho Agent tính giá
    sup_out = []
    for s in suppliers:
        sup_out.append({
            "slug": s["_slug"],
            "short_name": s.get("short_name"),
            "category": s.get("category"),
            "location": s.get("location"),
            "price_source": s.get("price_source"),  # airline → tool:fast-flights
            "rate_sheets": s.get("rate_sheets"),     # None với airline
            "commission": s.get("commission"),
            "quality_rating": s.get("quality_rating"),
            "confidential": bool(s.get("confidential")),  # True → lọc khỏi output khách-facing
        })

    tour_out = []
    for t in tours:
        tour_out.append({
            "slug": t["_slug"],
            "theme": t.get("theme"),
            "destinations": t.get("destinations"),
            "duration_days": t.get("duration_days"),
            "nights": t.get("nights"),
            "default_suppliers": t.get("default_suppliers"),
        })

    (ROOT / "build" / "suppliers.json").write_text(
        json.dumps(sup_out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    (ROOT / "build" / "tour-products.json").write_text(
        json.dumps(tour_out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    policy = markup_policy()
    (ROOT / "build" / "markup-policy.json").write_text(
        json.dumps(policy, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    print(f"suppliers.json: {len(sup_out)} suppliers "
          f"({sum(1 for s in sup_out if s['price_source'])} live-priced)")
    print(f"tour-products.json: {len(tour_out)} tour products")
    print(f"markup-policy.json: margin_incl_air={policy['margin_incl_air']} "
          f"confirmed={policy['confirmed']}")


if __name__ == "__main__":
    main()

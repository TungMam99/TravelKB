"""Tool definitions + dispatcher for the manual agentic loop (Spec 2 §4).
save_quote is gated: the dispatcher refuses unless `approved=True` is passed in
(conversation.py sets it only after the sales user confirms).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import kb
from .flight import flight_search
from .pricing import LineItem, quote_calc, vnd

ROOT = Path(__file__).resolve().parent.parent
QUOTES_DIR = ROOT / "wiki" / "tours" / "quotes"

# ---- JSON-schema tool definitions (Anthropic Messages `tools` param) ----------
TOOL_DEFS = [
    {
        "name": "kb_query",
        "description": "Tra cứu Travel KB: điểm đến, nhà cung cấp (giá theo mùa), tour mẫu, markup. "
                       "Đặt audience='customer' khi kết quả sẽ hiển thị cho khách (tự lọc NCC bảo mật).",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "Câu hỏi tiếng Việt"},
                "audience": {"type": "string", "enum": ["internal", "customer"],
                             "description": "internal=đủ giá vốn; customer=lọc confidential"},
            },
            "required": ["question"],
        },
    },
    {
        "name": "flight_search",
        "description": "Giá vé máy bay THAM CHIẾU live (fast-flights). Dùng mã sân bay IATA "
                       "(SGN, HAN, PQC, DAD, BKK...). Nếu trả ok=false → hỏi sales nhập giá vé tay.",
        "input_schema": {
            "type": "object",
            "properties": {
                "origin": {"type": "string"}, "dest": {"type": "string"},
                "date": {"type": "string", "description": "YYYY-MM-DD"},
                "pax": {"type": "integer", "default": 1},
            },
            "required": ["origin", "dest", "date"],
        },
    },
    {
        "name": "quote_calc",
        "description": "Tính giá vốn → giá bán DETERMINISTIC. Không tự nhân chia tiền — luôn gọi tool này. "
                       "Mỗi line_item: {label, cost (VND int), qty, kind: 'land'|'air', supplier?}.",
        "input_schema": {
            "type": "object",
            "properties": {
                "line_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "label": {"type": "string"},
                            "cost": {"type": "integer"},
                            "qty": {"type": "integer", "default": 1},
                            "kind": {"type": "string", "enum": ["land", "air"], "default": "land"},
                            "supplier": {"type": "string"},
                        },
                        "required": ["label", "cost"],
                    },
                },
            },
            "required": ["line_items"],
        },
    },
    {
        "name": "save_quote",
        "description": "Ghi báo giá ĐÃ ĐƯỢC SALES DUYỆT thành trang trong KB. Chỉ gọi sau khi sales xác nhận.",
        "input_schema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "kebab-case, không dấu"},
                "markdown": {"type": "string", "description": "Nội dung trang báo giá đầy đủ"},
            },
            "required": ["slug", "markdown"],
        },
    },
]


def _slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "quote"


def _save_quote(slug: str, markdown: str) -> dict:
    QUOTES_DIR.mkdir(parents=True, exist_ok=True)
    path = QUOTES_DIR / f"{_slugify(slug)}.md"
    path.write_text(markdown, encoding="utf-8")
    return {"ok": True, "saved": str(path.relative_to(ROOT))}


def execute_tool(name: str, args: dict, *, approved: bool = False) -> dict:
    """Dispatch one tool call. save_quote requires approved=True (manual gate)."""
    if name == "kb_query":
        return kb.kb_query(args["question"], args.get("audience", "internal"))
    if name == "flight_search":
        return flight_search(args["origin"], args["dest"], args["date"], args.get("pax", 1))
    if name == "quote_calc":
        items = [LineItem(label=i["label"], cost=int(i["cost"]), qty=int(i.get("qty", 1)),
                          kind=i.get("kind", "land"), supplier=i.get("supplier"))
                 for i in args["line_items"]]
        q = quote_calc(items, kb.load_markup_policy())
        return {
            "cost_total": q.cost_total, "cost_total_fmt": vnd(q.cost_total),
            "sell_total": q.sell_total, "sell_total_fmt": vnd(q.sell_total),
            "revenue": q.revenue, "vat_amount": q.vat_amount,
            "profit": q.profit, "profit_fmt": vnd(q.profit),
            "margin_incl_air": q.margin_incl_air, "margin_excl_air": q.margin_excl_air,
            "warnings": q.warnings,
            "breakdown": [{"label": i.label, "kind": i.kind, "total": i.total,
                           "total_fmt": vnd(i.total)} for i in items],
        }
    if name == "save_quote":
        if not approved:
            return {"ok": False, "error": "GATED: cần sales duyệt trước khi lưu báo giá."}
        return _save_quote(args["slug"], args["markdown"])
    return {"ok": False, "error": f"unknown tool {name}"}

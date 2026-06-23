"""Deterministic quote pricing (Spec 2 §5). LLM never does money math — it picks
line_items and calls quote_calc; this module computes every VND.

Mô hình (khớp bảng chiết tính thật):
- giá vốn (cost) = land_cost + air_cost
- doanh thu (revenue, chưa VAT): land_rev = land_cost / (1 - land_markup); air pass-through
- giá bán khách (gross, gồm VAT) = revenue * (1 + vat)
- margin (gồm vé) = (revenue - cost) / revenue ;  margin chưa-vé = land_markup
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LineItem:
    label: str
    cost: int               # đơn giá VND (số nguyên)
    qty: int = 1
    kind: str = "land"      # 'land' (markup dày) | 'air' (pass-through)
    supplier: str | None = None
    note: str | None = None

    @property
    def total(self) -> int:
        return int(self.cost) * int(self.qty)


@dataclass
class Quote:
    items: list[LineItem]
    land_cost: int
    air_cost: int
    cost_total: int
    revenue: int            # doanh thu chưa VAT
    vat_amount: int
    sell_total: int         # giá bán khách (gồm VAT)
    profit: int
    margin_incl_air: float
    margin_excl_air: float
    warnings: list[str] = field(default_factory=list)


def quote_calc(line_items: list[LineItem], policy: dict,
               warnings: list[str] | None = None) -> Quote:
    """Tính giá vốn → giá bán deterministic. `policy` = build/markup-policy.json."""
    land_markup = float(policy["land_markup"])
    vat = float(policy["vat"])

    land_cost = sum(li.total for li in line_items if li.kind == "land")
    air_cost = sum(li.total for li in line_items if li.kind == "air")
    cost_total = land_cost + air_cost

    land_rev = round(land_cost / (1 - land_markup)) if land_cost else 0
    air_rev = air_cost  # vé gần pass-through (hoa hồng hãng cộng riêng nếu xác nhận)
    revenue = land_rev + air_rev

    vat_amount = round(revenue * vat)
    sell_total = revenue + vat_amount
    profit = revenue - cost_total

    margin_incl = round(profit / revenue, 4) if revenue else 0.0
    margin_excl = round((land_rev - land_cost) / land_rev, 4) if land_rev else 0.0

    warns = list(warnings or [])
    if not policy.get("confirmed"):
        warns.append("⚠️ % markup chưa được lãnh đạo chuẩn hóa (tham chiếu từ 1 tour).")

    return Quote(
        items=line_items, land_cost=land_cost, air_cost=air_cost,
        cost_total=cost_total, revenue=revenue, vat_amount=vat_amount,
        sell_total=sell_total, profit=profit,
        margin_incl_air=margin_incl, margin_excl_air=margin_excl, warnings=warns,
    )


def vnd(n: int) -> str:
    return f"{int(round(n)):,}".replace(",", ".") + " VND"

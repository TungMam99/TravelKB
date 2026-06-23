"""Deterministic self-test (no ANTHROPIC_API_KEY needed). Covers Spec 2 DoD #2,5,6.
Run: .venv/bin/python -m agent.selftest
"""
from __future__ import annotations

from . import kb
from .flight import flight_search
from .pricing import LineItem, quote_calc, vnd


def test_quote_calc():
    """DoD #2 — giá vốn → giá bán deterministic, margin chưa-vé khớp 0.1922 (sheet thật)."""
    policy = kb.load_markup_policy()
    items = [
        LineItem("Khách sạn (land)", cost=100_000_000, kind="land"),
        LineItem("Ăn + tham quan + xe (land)", cost=100_000_000, kind="land"),
        LineItem("Vé máy bay", cost=180_000_000, kind="air"),
    ]
    q = quote_calc(items, policy)
    # invariants chứng minh công thức đúng (không hardcode vòng tròn):
    assert q.cost_total == 380_000_000, q.cost_total
    assert q.land_cost == 200_000_000 and q.air_cost == 180_000_000
    assert q.sell_total == q.revenue + q.vat_amount
    assert q.vat_amount == round(q.revenue * policy["vat"])
    assert q.profit == q.revenue - q.cost_total
    assert q.revenue > q.cost_total                       # có lãi
    assert q.margin_excl_air == round(policy["land_markup"], 4) == 0.1922
    assert 0.10 < q.margin_incl_air < 0.13                # ~11,76% như tour thật
    print(f"  giá vốn {vnd(q.cost_total)} → giá bán {vnd(q.sell_total)} "
          f"(lãi {vnd(q.profit)}, margin gồm vé {q.margin_incl_air:.2%}, "
          f"chưa vé {q.margin_excl_air:.2%})")
    print("  ✓ quote_calc")


def test_confidential_filter():
    """DoD #5 — kb_query(customer) loại supplier confidential (Mường Thanh)."""
    internal = {s["slug"] for s in kb.load_suppliers("internal")}
    customer = {s["slug"] for s in kb.load_suppliers("customer")}
    assert "muong-thanh-can-tho" in internal, "Mường Thanh phải có ở bản nội bộ"
    assert "muong-thanh-can-tho" not in customer, "Mường Thanh KHÔNG được lộ cho khách"
    assert customer < internal
    print(f"  internal={len(internal)} suppliers, customer={len(customer)} "
          f"(đã ẩn {len(internal - customer)} confidential)")
    print("  ✓ confidential filter")


def test_flight_fallback():
    """DoD #6 — fast-flights lỗi (sân bay rác) → ok=false, không crash."""
    bad = flight_search("ZZZ", "QQQ", "2026-09-15", 1)
    assert bad["ok"] is False and "fallback" in bad
    print(f"  sân bay rác → ok=False, fallback='{bad['fallback']}'")
    print("  ✓ flight fallback")


class _Blk:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class _Resp:
    def __init__(self, stop_reason, content):
        self.stop_reason, self.content = stop_reason, content


class _FakeClient:
    """Mô phỏng Claude trả tool_use rồi save_quote, để test loop + gate không cần API key."""
    def __init__(self):
        self.calls = 0
        self.messages = self

    def create(self, **kw):
        self.calls += 1
        if self.calls == 1:  # gọi kb_query
            return _Resp("tool_use", [
                _Blk(type="text", text="Để tôi tra KB."),
                _Blk(type="tool_use", id="t1", name="kb_query",
                     input={"question": "phú quốc", "audience": "internal"})])
        if self.calls == 2:  # muốn lưu báo giá → phải bị gate
            return _Resp("tool_use", [
                _Blk(type="text", text="Đã có báo giá, lưu nhé?"),
                _Blk(type="tool_use", id="t2", name="save_quote",
                     input={"slug": "selftest-quote", "markdown": "# Báo giá test\n"})])
        return _Resp("end_turn", [_Blk(type="text", text="Đã lưu xong.")])


def test_conversation_loop():
    """DoD #4 (loop chạy) + #7 (save gate human-in-the-loop)."""
    from .conversation import Session
    s = Session(client=_FakeClient())
    r1 = s.send("Phú Quốc 4N3Đ 2 khách")
    assert r1["state"] == "awaiting_save_approval", r1["state"]      # pause ở save
    assert "lưu" in r1["text"].lower()
    r2 = s.approve_save(True)                                         # sales duyệt
    assert r2["state"] == "done"
    saved = kb.ROOT / "wiki" / "tours" / "quotes" / "selftest-quote.md"
    assert saved.exists(), "save_quote phải ghi file sau khi duyệt"
    saved.unlink()                                                   # dọn file test
    print("  loop: kb_query → save (gated) → approve → ghi file → done")
    print("  ✓ conversation loop + save gate")


def main():
    print("== Agent deterministic self-test ==")
    test_quote_calc()
    test_confidential_filter()
    test_flight_fallback()
    test_conversation_loop()
    print("ALL PASS ✅")


if __name__ == "__main__":
    main()

"""Live flight reference prices via fast-flights (Spec 2 §4, no-API).
Scraper dễ vỡ → luôn trả {ok: bool}; lỗi thì agent fallback hỏi giá tay.
"""
from __future__ import annotations


def _hhmm(t) -> str:
    """fast-flights đôi khi trả time=[14] (phút=0) thay vì [14,0]."""
    h = t[0] if len(t) > 0 else 0
    m = t[1] if len(t) > 1 else 0
    return f"{h:02d}:{m:02d}"


def flight_search(origin: str, dest: str, date: str, pax: int = 1) -> dict:
    """origin/dest = IATA (SGN, HAN, PQC, DAD, BKK...). date = YYYY-MM-DD."""
    try:
        from fast_flights import create_query, FlightQuery, Passengers, get_flights
    except ImportError:
        return {"ok": False, "error": "fast-flights chưa cài",
                "fallback": "Nhập giá vé tay."}
    try:
        q = create_query(
            flights=[FlightQuery(date=date, from_airport=origin, to_airport=dest)],
            seat="economy", trip="one-way",
            passengers=Passengers(adults=max(1, int(pax))),
            currency="VND", language="vi",
        )
        result = get_flights(q)
        flights = []
        for f in list(result)[:6]:
            legs = f.flights
            dep, arr = legs[0].departure, legs[-1].arrival
            flights.append({
                "airline": ", ".join(f.airlines),
                "price_vnd": int(f.price),
                "depart": _hhmm(dep.time),
                "arrive": _hhmm(arr.time),
                "duration_min": sum(l.duration for l in legs),
                "stops": len(legs) - 1,
            })
        if not flights:
            return {"ok": False, "error": "Không có chuyến", "fallback": "Nhập giá vé tay."}
        prices = [f["price_vnd"] for f in flights]
        return {
            "ok": True, "route": f"{origin}-{dest}", "date": date,
            "ref_min": min(prices), "ref_max": max(prices), "flights": flights,
            "note": "Giá THAM CHIẾU tại thời điểm tra cứu (fast-flights) — chốt thật qua booking.",
        }
    except Exception as e:  # scraper có thể gãy khi Google đổi format
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "fallback": "fast-flights lỗi → nhập giá vé tay."}

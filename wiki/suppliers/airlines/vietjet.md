---
type: supplier
category: airline
short_name: "VJ"          # IATA; Thai Vietjet = VZ (hãng chị em, chặng quốc tế Thái)
price_source: "tool:fast-flights"   # KHÔNG lưu rate_sheets — giá lấy live
commission: "Chưa xác nhận — cập nhật từ hợp đồng đại lý vé"
routes_seen: ["SGN-PQC", "SGN-BKK"]
contacts:
  sales: ""
updated: 2026-06-23
sources: ["[[sources/chiet-tinh-gia-noi-bo]]", "[[sources/bangkok-pattaya-5-ngay]]"]
---

# Vietjet Air (VJ)

> Hãng giá rẻ, dùng nhiều cho chặng nội địa (SGN-PQC) và quốc tế qua Thai Vietjet (VZ, vd SGN-BKK).

## Định giá — LIVE, không lưu trong KB
Giá vé đổi từng giờ → **không** lưu `rate_sheets`. Agent lấy giá tham chiếu tại thời điểm báo giá
qua tool `flight_search` (fast-flights, no-API). Ví dụ đã test **SGN→BKK 2026-07-15**: Vietjet
2.070.000 VND (rẻ nhất, bay thẳng 90'). Xem [[concepts/markup-policy]] cho cách cộng hoa hồng.

## Chặng đã dùng (từ dữ liệu thật)
- **SGN-PQC** (Phú Quốc): tour Nhật Huy Khang 8/2022 — giá đoàn ~3.450.000/khách (gồm ký gửi).
- **SGN-BKK** (Bangkok): tour Bangkok-Pattaya — chặng VZ971/VJ806 (Thai Vietjet/Vietjet).

## Lưu ý
- Giá là **tham chiếu** (fast-flights scrape Google Flights) — chốt thật qua booking.
- Hành lý ký gửi tính riêng (trong chiet-tinh: 15.498.000 cho cả đoàn).

## Liên kết
- Dùng trong: [[tours/tour-products/bangkok-pattaya-5n4d]], [[tours/quotes/phu-quoc-nhat-huy-khang-2022-08]]

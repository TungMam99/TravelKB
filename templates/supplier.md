---
# === Biến thể A: Supplier thường (hotel/transport/guide/restaurant/activity/dmc) ===
type: supplier
category: hotel            # hotel|transport|guide|restaurant|activity|dmc|airline
short_name: ""            # khớp ShortName trong supplier-list nếu có
location: "[[destinations/...]]"
quality_rating:           # /5, đánh giá nội bộ
contacts:
  sales: ""
booking_source: ""        # pointer tới CRM/Excel real-time (không lưu chỗ trống ở đây)
lead_time_days:
availability_notes: ""
rate_sheets:
  - season: "Cao điểm"
    valid_until: 2026-12-31
    rates: {}             # {"Hạng phòng": 1500000}  — VND số nguyên (machine-readable)
  - season: "Thấp điểm"
    valid_until: 2026-12-31
    rates: {}
updated: 2026-06-23
sources: []
---

# <Tên nhà cung cấp>

> Tóm tắt 1 câu: là gì, ở đâu, vì sao đáng ghi nhận.

## Thông tin
- Loại / vị trí / liên hệ.

## Rate sheet theo mùa
(Để chi tiết ở frontmatter; mô tả thêm điều khoản ở đây.)

## Đánh giá & lưu ý
Chất lượng, ưu/nhược, lead time, mẹo đặt.

## Liên kết
- Điểm đến: [[destinations/...]] · Dùng trong: [[tours/...]] · Nguồn: frontmatter `sources`.

<!--
=== Biến thể B: Airline (live-priced) — thay frontmatter bằng: ===
type: supplier
category: airline
short_name: "VJ"           # mã hãng IATA
price_source: "tool:fast-flights"   # KHÔNG có rate_sheets; giá lấy live
commission: ""             # hoa hồng/điều khoản (tri thức bền)
contract_terms: "[[sources/...]]"
contacts: { sales: "" }
updated: 2026-06-23
sources: []
-->

---
type: quote
status: draft             # draft | sent | confirmed | settled
client: ""               # tên khách / công ty
tour_product: "[[tours/tour-products/...]]"
destinations: []
dates: ""
pax: ""                  # vd "39 NL + 1 TE"
cost_total:              # tổng giá vốn (VND, số nguyên)
sell_total:              # tổng giá bán (VND)
margin_pct:              # tỷ lệ lãi/doanh thu
updated: 2026-06-23
sources: []
---

# Báo giá — <Tên khách / tour>

> Tuyến, thời gian, số khách, trạng thái.

## Bảng giá vốn (NỘI BỘ — không gửi khách)
| Đầu mục | Nhà cung cấp | SL | Đơn giá (VND) | Thành tiền |
|---|---|---|---|---|
| Vé máy bay | [[suppliers/airlines/...]] | | *(live: fast-flights)* | |
| Khách sạn | [[suppliers/hotels/...]] | | | |
| Vận chuyển | [[suppliers/transport/...]] | | | |
| Nhà hàng | | | | |
| Tham quan | | | | |
| **Tổng chi (giá vốn)** | | | | |

## Bảng báo giá khách (XUẤT — theo mẫu bao-gia-breakdown)
| Hạng mục | NL | TE | Phụ thu |
|---|---|---|---|
| Giá tour trọn gói | | | |

- Áp dụng markup theo [[concepts/markup-policy]].
- ⚠️ Dòng vé máy bay là **giá tham chiếu tại thời điểm tra cứu** (fast-flights), chốt thật qua booking.

## Liên kết
- Tour gốc: `tour_product` · Nguồn: frontmatter `sources`.

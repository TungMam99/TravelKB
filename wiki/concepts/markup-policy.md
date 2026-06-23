---
type: concept
topic: budgeting
scope: global
tags: [concept, pricing]
# Machine-readable (build/markup-policy.json → Agent quote_calc). Tham chiếu từ 1 tour, CHỜ lãnh đạo chuẩn hóa.
margin_incl_air: 0.1176     # lãi/doanh thu gồm vé
margin_excl_air: 0.1922     # lãi/doanh thu chưa vé (land tour)
land_markup: 0.1922         # = margin_excl_air; land_rev = land_cost/(1-land_markup)
vat: 0.08
confirmed: false            # true khi lãnh đạo duyệt % chuẩn
updated: 2026-06-23
sources: ["[[sources/chiet-tinh-gia-noi-bo]]"]
---

# Markup Policy — Công thức giá bán

> Cách cộng lãi từ giá vốn ra giá bán. Trích từ bảng chiết tính thật của Hồng Ngọc Hà.

## Tỷ lệ lãi tham chiếu (từ tour Phú Quốc 8/2022)
| Chỉ số | Giá trị | Ghi chú |
|---|---|---|
| **Lãi / doanh thu (GỒM vé)** | **11,76%** | Khi tính cả vé máy bay vào doanh thu |
| **Lãi / doanh thu (CHƯA vé)** | **19,22%** | Phần land tour markup cao hơn nhiều |
| Thuế suất áp dụng | 8% | VAT trên phần lớn dịch vụ |

→ **Nguyên tắc:** vé máy bay markup mỏng (cạnh tranh, gần như pass-through + hoa hồng hãng);
**land tour (KS/ăn/xe/tham quan) markup dày hơn** (~19%). Tách 2 nhóm khi báo giá.

## Cách Agent áp dụng (Spec 2)
1. Giá vốn land = Σ(rate_sheets supplier) → nhân **(1 / (1 − 0.19))** ≈ markup ~19% land.
2. Vé máy bay = giá live (fast-flights) + hoa hồng hãng (gần pass-through).
3. Cộng VAT 8% nơi áp dụng. Tổng → giá bán; kiểm tra margin tổng ≈ 11–12% (gồm vé).

## Lưu ý
- Đây là **tham chiếu lịch sử 1 tour**, chưa phải chính sách công ty chính thức.
  ⚠️ Cần lãnh đạo xác nhận % markup chuẩn theo loại dịch vụ trước khi Agent dùng tự động.

## Liên kết
- Áp dụng: mọi [[tours/quotes/...]] · Nguồn: [[sources/chiet-tinh-gia-noi-bo]]

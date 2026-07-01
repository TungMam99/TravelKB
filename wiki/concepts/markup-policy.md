---
type: concept
topic: budgeting
scope: global
tags: [concept, pricing, markup]

# ── Trạng thái ──────────────────────────────────────────────────────────────
confirmed: false          # true khi lãnh đạo ký duyệt chính sách Draft v1 bên dưới
draft_version: "1.0"
draft_date: 2026-07-01

# ── Giá trị đang dùng (từ 1 tour lịch sử 2022 — CHỜ thay bằng chính sách duyệt) ──
margin_incl_air: 0.1176   # lãi/doanh thu gồm vé   (Phú Quốc 44 pax 2022)
margin_excl_air: 0.1922   # lãi/doanh thu chưa vé
land_markup: 0.1922
vat: 0.08

# ── Draft policy (chờ duyệt) ─────────────────────────────────────────────────
draft_policy:
  land_markup_pct: 0.20         # 20% trên land cost (giữa 19–22%)
  air_markup_pct:  0.03         # 3% trên vé máy bay (pass-through + phí booking)
  bonus_reserve_pct: 0.01       # 1% dự phòng thưởng KD
  margin_floor_pct: 0.05        # 5% — sàn tuyệt đối; dưới này agent từ chối tự động
  thresholds:
    green:  0.10   # ≥ 10% → bình thường
    yellow: 0.07   # 7–9,9% → cảnh báo sales
    red:    0.05   # 5–6,9% → GĐ ký phiếu đặc biệt
    block:  0.05   # < 5%  → agent không xuất báo giá

  segments:
    group_domestic:  { min_pax: 20, intl: false, target_margin: [0.12, 0.15] }
    group_intl:      { min_pax: 20, intl: true,  target_margin: [0.10, 0.12] }
    small_group:     { min_pax: 10, intl: true,  target_margin: [0.08, 0.10] }
    fit_standard:    { max_pax: 9,  intl: true,  target_margin: [0.06, 0.08] }
    fit_vip:         { max_pax: 9,  intl: true,  target_margin: [0.05, 0.06], requires_director_approval: true }

updated: 2026-07-01
sources: ["[[sources/chiet-tinh-gia-noi-bo]]"]
---

# Markup Policy — Công thức giá bán

> Cách cộng lãi từ giá vốn ra giá bán. Trích từ bảng chiết tính thực tế (nguồn nội bộ 2022).
> **⚠️ Draft v1.0 — chờ lãnh đạo duyệt. Agent đang dùng số liệu cũ 11,76%/19,22% cho đến khi `confirmed: true`.**

---

## Trạng thái

| | |
|-|-|
| **Số liệu đang áp dụng** | 11,76% (gồm vé) / 19,22% (chưa vé) — từ 1 tour Phú Quốc 2022 |
| **Draft chính sách mới** | v1.0 (07/2026) — phân tầng theo phân khúc khách |
| **Cần duyệt bởi** | Giám đốc / Lãnh đạo tài chính |
| **Áp dụng khi** | `confirmed: true` được set trong frontmatter |

---

## Phân tích cơ sở — Dữ liệu thực tế 4 tour

| Tour | Pax | Margin thực tế | Ghi chú |
|------|-----|---------------|---------|
| Phú Quốc 4N3Đ (Aug 2022) | 44 NL | **11,76%** | Nội địa, đoàn lớn; vé chiếm 46% |
| Bangkok-Pattaya 5N4Đ (Oct 2026) | 15+1 | **10,09%** | Quốc tế, đoàn TB; vé chiếm 70,6% |
| Bangkok-Pattaya FIT (Aug 2026) | 2 pax | **6,31%** | FIT, peak season |
| Bali 5N4Đ FIT pilot (Sep 2026) | 2 pax | **5,00%** | FIT, deal cạnh tranh, shoulder |

→ Margin thực tế dao động **5–12%** tùy phân khúc và tỷ trọng vé.

---

## Nguyên tắc tách nhóm chi phí

Vé máy bay chiếm **46–71% giá vốn** tùy tuyến → markup gộp 1 con số sẽ sai lệch lớn.
Tách thành 2 nhóm để kiểm soát chính xác:

| Nhóm | Gồm | Markup mục tiêu |
|------|-----|----------------|
| **Land** | KS + nhà hàng + xe + tham quan + HDV + bảo hiểm | **19–22%** |
| **Air** | Vé máy bay (pass-through qua hãng) | **2–4%** (bù phí booking + rủi ro tỷ giá) |

### Công thức tính giá bán (Draft v1.0)

```
Giá bán land  = Land cost  ÷ (1 − 0,20)      ← markup 20%
Giá bán air   = Air cost   ÷ (1 − 0,03)      ← markup 3%
Doanh thu     = Giá bán land + Giá bán air
Giá khách     = Doanh thu × 1,08              ← cộng VAT 8%
Margin tổng   = (Doanh thu − Tổng giá vốn) ÷ Doanh thu
```

---

## ⚡ DRAFT v1.0 — Bảng margin mục tiêu theo phân khúc

> Chờ lãnh đạo xác nhận. Không áp dụng tự động cho đến khi `confirmed: true`.

| Phân khúc | Điều kiện | Margin mục tiêu | Land markup | Ghi chú |
|-----------|-----------|----------------|-------------|---------|
| 🟢 Đoàn lớn nội địa | ≥ 20 pax, bay nội địa | **12–15%** | 20–22% | Vé nội địa rẻ → margin tổng cao |
| 🟢 Đoàn lớn quốc tế | ≥ 20 pax, quốc tế | **10–12%** | 20–22% | Vé QT 50–70% chi phí |
| 🟡 Đoàn nhỏ | 10–19 pax, quốc tế | **8–10%** | 20% | Fixed cost trải ít pax |
| 🟡 FIT chuẩn | ≤ 9 pax | **6–8%** | 19–20% | Đoàn nhỏ nhất, land/pax cao |
| 🔴 FIT VIP/pilot | ≤ 9 pax, đặc biệt | **≥ 5% (sàn)** | 19% | **Bắt buộc GĐ ký phiếu riêng** |

### Ngưỡng cảnh báo Agent

| Mức | Ngưỡng margin | Hành động |
|-----|--------------|-----------|
| 🟢 Bình thường | ≥ 10% | Xuất báo giá tự động |
| 🟡 Cảnh báo | 7–9,9% | Flag cảnh báo; sales tự quyết |
| 🔴 Rất thấp | 5–6,9% | Chặn tự động; yêu cầu GĐ ký phiếu |
| ⛔ Từ chối | < 5% | Agent không xuất; báo lỗi |

---

## Dự phòng thưởng kinh doanh

Từ dữ liệu Bangkok Oct 2026: thưởng = 2.579.743 ÷ 253.200.000 = **1,02% doanh thu**.

→ Dự phòng **1–1,5%** khi báo margin nội bộ cho lãnh đạo:

| Chỉ tiêu | Đoàn lớn QT | FIT chuẩn |
|----------|------------|-----------|
| Margin gộp (báo cáo) | 10–12% | 6–8% |
| Dự phòng thưởng KD | 1–1,5% | 0,5–1% |
| **Margin thực ròng** | **8,5–11%** | **5–7,5%** |

---

## Cách Agent áp dụng hiện tại (trước khi confirmed)

1. Giá vốn land → nhân **(1 / (1 − 0,1922))** ≈ markup 19,22% (số cũ).
2. Vé máy bay = giá live (fast-flights) — pass-through, không markup riêng.
3. Cộng VAT 8%. Kiểm tra margin tổng ≈ 11–12% (gồm vé).
4. Nếu margin < 11,76% → **flag cảnh báo** cho sales review.

_Sau khi `confirmed: true`: Agent chuyển sang công thức Draft v1.0 phân tầng theo phân khúc._

---

## Checklist duyệt (lãnh đạo điền)

- [ ] Xác nhận land markup: ____% (đề xuất 20%)
- [ ] Xác nhận air markup: ____% (đề xuất 3%)
- [ ] Xác nhận ngưỡng sàn: ____% (đề xuất 5%)
- [ ] Đồng ý phân tầng theo pax: Có / Không
- [ ] Dự phòng thưởng KD: ____% (đề xuất 1%)
- [ ] Người duyệt: _________________ Ngày: ___/___/2026

_Sau khi điền xong → báo team kỹ thuật set `confirmed: true` và cập nhật các con số trong frontmatter._

---

## Liên kết

- Áp dụng: [[tours/quotes/bali-5n4d-sep2026-2pax]] · [[tours/quotes/dxdg-bangkok-pattaya-5n4d-aug2026-2pax]] · [[tours/quotes/bangkok-pattaya-5n4d-oct2026-noi-bo]]
- Dữ liệu gốc: [[sources/chiet-tinh-gia-noi-bo]] · [[tours/quotes/phu-quoc-nhat-huy-khang-2022-08]]
- Build artifact: `build/markup-policy.json` (cần chạy lại sau khi confirmed)

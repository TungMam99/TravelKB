---
type: index
updated: 2026-06-23
source_count: 3
page_count: 11
---

# Index — Travel Knowledge Base (Tour Operator)

Catalog mọi trang. Đọc **đầu tiên** khi query, rồi drill vào. Cập nhật mỗi lần ingest.
Dòng thời gian: [[log]] · Bức tranh tổng: [[overview]] · Schema: `CLAUDE.md` + Spec `docs/superpowers/specs/2026-06-23-travel-kb-design.md`.

## 🌍 Destinations
- [[destinations/phu-quoc]] — đảo biển + resort + vui chơi (Vinpearl Safari, Hòn Thơm). Mạnh cho đoàn.
- [[destinations/bangkok]] — thủ đô Thái, ghép Pattaya thành tuyến city + biển 5N4Đ.

## 🏨 Suppliers
- **Airlines:** [[suppliers/airlines/vietjet]] — VJ/VZ, **live-priced** (fast-flights), chặng SGN-PQC/SGN-BKK.
- **Hotels:** [[suppliers/hotels/best-western-sonasea-phu-quoc]] — resort Phú Quốc, ROH 1,5tr (2022).
- **Transport:** [[suppliers/transport/long-beach-phu-quoc]] — xe 45 chỗ, 13tr/4N3Đ (2022).

## 🧳 Tours
- **Tour products:** [[tours/tour-products/bangkok-pattaya-5n4d]] — Bangkok-Pattaya 5N4Đ.
- **Quotes:** [[tours/quotes/phu-quoc-nhat-huy-khang-2022-08]] — đoàn 44 khách, lãi 56,9tr (margin 11,76%).

## 💡 Concepts
- [[concepts/markup-policy]] — markup 11,76% (gồm vé) / 19,22% (chưa vé), thuế 8%.

## 📚 Sources
- [[sources/bangkok-pattaya-5-ngay]] — brochure tour Thái.
- [[sources/chiet-tinh-gia-noi-bo]] — chiết tính + quyết toán Phú Quốc (giá vốn thật).
- [[sources/contract-tet-hong-ngoc-ha-2022]] — ⚠️ hợp đồng khách B2B (không phải supplier; lộ gap model).

## 🔗 Synthesis
_(chưa có)_

## 🛠 Build artifacts (KB → Agent)
- `build/suppliers.json` (3) · `build/tour-products.json` (1) — sinh bởi `build/extract_kb.py`.

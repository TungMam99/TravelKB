---
type: index
updated: 2026-07-01
source_count: 9
page_count: 25
---

# Index — Travel Knowledge Base (Tour Operator)

Catalog mọi trang. Đọc **đầu tiên** khi query, rồi drill vào. Cập nhật mỗi lần ingest.
Dòng thời gian: [[log]] · Bức tranh tổng: [[overview]] · Schema: `CLAUDE.md` + Spec `docs/superpowers/specs/2026-06-23-travel-kb-design.md`.

## 🌍 Destinations
- [[destinations/phu-quoc]] — đảo biển + resort + vui chơi (Vinpearl Safari, Hòn Thơm). Mạnh cho đoàn.
- [[destinations/bangkok]] — thủ đô Thái, ghép Pattaya thành tuyến city + biển 5N4Đ.
- [[destinations/vung-tau]] — biển gần TP.HCM, weekend/đoàn ngắn ngày.
- [[destinations/can-tho]] — miền Tây sông nước, chợ nổi Cái Răng.

## 🏨 Suppliers
- **Airlines:** [[suppliers/airlines/vietjet]] — VJ/VZ, **live-priced** (fast-flights), chặng SGN-PQC/SGN-BKK.
- **Hotels:**
  - [[suppliers/hotels/best-western-sonasea-phu-quoc]] — resort Phú Quốc, ROH 1,5tr (2022).
  - [[suppliers/hotels/galaxy-3-vung-tau]] — KS 3* Bà Rịa, 400k–1tr (2023).
  - [[suppliers/hotels/muong-thanh-can-tho]] — KS 4-5* Cần Thơ, 1,55–12tr (2023). 🔒 **giá bảo mật**.
- **Transport:** [[suppliers/transport/long-beach-phu-quoc]] — xe 45 chỗ, 13tr/4N3Đ (2022).

## 🏛 Entities
- [[entities/alcazar-show]] — show chuyển giới Pattaya, included trong tour Thái.

## 🧳 Tours
- **Tour products:** [[tours/tour-products/bangkok-pattaya-5n4d]] — Bangkok-Pattaya 5N4Đ (2 biến thể: HNH 2022 + TST 2026).
- **Quotes:**
  - [[tours/quotes/phu-quoc-nhat-huy-khang-2022-08]] — đoàn 44 khách Phú Quốc, lãi 56,9tr (margin 11,76%).
  - [[tours/quotes/bangkok-pattaya-5n4d-oct2026-noi-bo]] 🔒 — chiết tính nội bộ BKK-PTY Oct 2026, 15 pax, margin 10,09%.

## 💡 Concepts
- [[concepts/markup-policy]] — markup 11,76% (gồm vé) / 19,22% (chưa vé), thuế 8%.

## 📚 Sources
- [[sources/bangkok-pattaya-5-ngay]] — brochure tour Thái (HNH 2022).
- [[sources/bangkok-pattaya-5n4d-tst-tourist]] — brochure tour Thái (TST Tourist 2026, lịch trình biến thể).
- [[sources/dxdg-thailand-5n4d-oct2026]] 🔒 — chiết tính nội bộ BKK-PTY, 15 pax, Oct 2026.
- [[sources/fit-tour-tst-2026]] — web crawl ~60 FIT tour TST Tourist (Á/Mỹ/Âu), 01/07/2026.
  - [[sources/tst-tour-details-2026]] — crawl chi tiết từng trang tour (giá, ngày KH, hãng bay, lịch trình), 01/07/2026.
- [[sources/chiet-tinh-gia-noi-bo]] — chiết tính + quyết toán Phú Quốc (giá vốn thật).
- [[sources/contract-tet-hong-ngoc-ha-2022]] — ⚠️ hợp đồng khách B2B (không phải supplier; lộ gap model).
- [[sources/galaxy-3-bang-gia-phong-2023]] — bảng giá phòng Galaxy 3 (2023).
- [[sources/hd-muong-thanh-can-tho]] — 🔒 HĐ nguyên tắc Mường Thanh Cần Thơ (giá bảo mật).

## 🔗 Synthesis
- [[synthesis/tst-tour-catalog-2026]] — ~80 FIT tour TST Tourist 2026 (Á/Mỹ/Âu), benchmark giá + phân tích cạnh tranh. Cập nhật với chi tiết ngày KH, hãng bay, pattern mùa vụ.

## 🛠 Build artifacts (KB → Agent)
- `build/suppliers.json` (5, có field `confidential`) · `build/tour-products.json` (1) — sinh bởi `build/extract_kb.py`.

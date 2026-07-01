# Graph Report - .  (2026-07-01)

## Corpus Check
- 83 files · ~70,040 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 163 nodes · 264 edges · 21 communities (8 shown, 13 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 29 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Flight & Live Pricing Engine|Flight & Live Pricing Engine]]
- [[_COMMUNITY_Sales Copilot Agent Core|Sales Copilot Agent Core]]
- [[_COMMUNITY_Markup Policy & Tour Catalog|Markup Policy & Tour Catalog]]
- [[_COMMUNITY_Platform Architecture & Patterns|Platform Architecture & Patterns]]
- [[_COMMUNITY_Suppliers & Tour Quotes|Suppliers & Tour Quotes]]
- [[_COMMUNITY_Bangkok-Pattaya Tour Intelligence|Bangkok-Pattaya Tour Intelligence]]
- [[_COMMUNITY_KB Data Access Layer|KB Data Access Layer]]
- [[_COMMUNITY_Mường Thanh Confidential Contract|Mường Thanh Confidential Contract]]
- [[_COMMUNITY_Spec-Driven Development|Spec-Driven Development]]
- [[_COMMUNITY_TST Brand Identity|TST Brand Identity]]
- [[_COMMUNITY_Failed Conversion Artifact|Failed Conversion Artifact]]
- [[_COMMUNITY_Hotel Pricing Template|Hotel Pricing Template]]
- [[_COMMUNITY_Concept Page Template|Concept Page Template]]
- [[_COMMUNITY_Destination Page Template|Destination Page Template]]
- [[_COMMUNITY_Entity Page Template|Entity Page Template]]
- [[_COMMUNITY_Source Page Template|Source Page Template]]
- [[_COMMUNITY_Synthesis Page Template|Synthesis Page Template]]
- [[_COMMUNITY_Tour Product Template|Tour Product Template]]
- [[_COMMUNITY_Trip Page Template|Trip Page Template]]
- [[_COMMUNITY_Long Beach Transport|Long Beach Transport]]
- [[_COMMUNITY_Wiki Overview|Wiki Overview]]

## God Nodes (most connected - your core abstractions)
1. `Session` - 17 edges
2. `Travel KB Schema & Operating Manual (CLAUDE.md)` - 11 edges
3. `Hong Ngoc Ha Travel Company` - 11 edges
4. `LineItem` - 10 edges
5. `execute_tool()` - 10 edges
6. `Tour Product: Bangkok – Pattaya 5N4Đ` - 10 edges
7. `Spec 1 — Travel Knowledge Base (Tour Operator) Design` - 9 edges
8. `Wiki Index — TravelKB Content Catalog` - 9 edges
9. `quote_calc()` - 8 edges
10. `Markup Policy — Công Thức Giá Bán Tour (Draft v1.0, confirmed: false)` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Bangkok–Pattaya 5 Days Tour (HNH brochure, graphify-converted)` --semantically_similar_to--> `Bangkok–Pattaya 5 Days HNH Tour Brochure (raw/converted)`  [INFERRED] [semantically similar]
  graphify-out/converted/Bangkok - Pattaya 5 ngày_a38a9163.md → raw/converted/bangkok-pattaya-5-ngay.md
- `Tour Cost Breakdown & Settlement (Heineken/HNH Quotation, graphify-converted)` --semantically_similar_to--> `Tour Cost Settlement (Heineken/HNH raw/converted)`  [INFERRED] [semantically similar]
  graphify-out/converted/Bảng Chiết tính & Quyết toán kết thúc Tour_b0b1a38c.md → raw/converted/chiet-tinh-quyet-toan-tour.md
- `Customer Quote Breakdown — Quy Nhon MICE Tour (graphify-converted)` --semantically_similar_to--> `Customer Quote Breakdown — Quy Nhon MICE (raw/converted)`  [INFERRED] [semantically similar]
  graphify-out/converted/bảng báo giá  break down cho khach hang_52cfbb14.md → raw/converted/bao-gia-breakdown-khach-hang.md
- `Thailand 5N4D Tour Price Approval (DXDG, graphify-converted)` --semantically_similar_to--> `Thailand 5N4D Price Approval (DXDG raw/converted)`  [INFERRED] [semantically similar]
  graphify-out/converted/ĐXDG THAILAND 5N4D_b5886350.md → raw/converted/dxdg-thailand-5n4d.md
- `LLM Wiki Pattern — Persistent Compounding Knowledge Base` --semantically_similar_to--> `3-Layer KB Architecture: raw / wiki / schema`  [INFERRED] [semantically similar]
  Pattern/llmwiki.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Three-Layer AI Sales Platform (KB + Agent + Website)** — specs_2026_06_23_travel_kb_design_spec1, specs_2026_06_23_agent_design_spec2, specs_2026_06_24_website_design_spec3, travelkb_claude_schema [EXTRACTED 1.00]
- **Tour Quoting Workflow Document Set (breakdown + chiet tinh + DXDG)** — converted_bao_gia_break_down_52cfbb14, converted_bang_chiet_tinh_b0b1a38c, converted_dxdg_thailand_b5886350, concept_sales_copilot_agent [INFERRED 0.85]
- **Bangkok–Pattaya Tour Multi-Source Document Set** — converted_bangkok_pattaya_5_ngay_hnh, converted_bangkok_pattaya_5_ngay_a38a9163, converted_bangkok_pattaya_5n4d_tst, entity_bangkok_pattaya_tour [INFERRED 0.88]
- **TST Tour Catalog + Details Drive Bali/Bangkok Competitive Benchmarking** — converted_fit_tour_tst_2026_catalog, converted_tst_tour_details_2026_details, destinations_bali_page, destinations_bangkok_page [INFERRED 0.85]
- **Markup Policy Draft → Approval Form → Agent Threshold Enforcement → Web Save Gate** — concepts_markup_policy_policy, concepts_markup_policy_trinh_ky_form, concepts_markup_policy_margin_thresholds, web_readme_streamlit_app [EXTRACTED 0.85]
- **Wiki Page Templates Form Unified KB Schema (7 page types)** — templates_concept_page, templates_destination_page, templates_entity_page, templates_quote_page, templates_supplier_page, templates_tour_product_page, templates_trip_page [EXTRACTED 0.95]
- **Bangkok-Pattaya Tour Pricing Ecosystem (product + rates + quotes + airline)** — tour_products_bangkok_pattaya_5n4d, quotes_bangkok_pattaya_5n4d_oct2026_noi_bo, quotes_bangkok_pattaya_land_rate_2026, airlines_vietjet [EXTRACTED 0.95]
- **TST Competitive Intelligence Pipeline (crawl → details → synthesis)** — sources_fit_tour_tst_2026, sources_tst_tour_details_2026, synthesis_tst_tour_catalog_2026 [EXTRACTED 1.00]
- **Confidential Hotel Contract Architecture (contract → supplier entity → pricing principle)** — sources_hd_muong_thanh_can_tho, hotels_muong_thanh_can_tho, concept_confidential_contract_pricing [INFERRED 0.85]

## Communities (21 total, 13 thin omitted)

### Community 0 - "Flight & Live Pricing Engine"
Cohesion: 0.09
Nodes (28): flight_search(), _hhmm(), Live flight reference prices via fast-flights (Spec 2 §4, no-API). Scraper dễ vỡ, origin/dest = IATA (SGN, HAN, PQC, DAD, BKK...). date = YYYY-MM-DD., fast-flights đôi khi trả time=[14] (phút=0) thay vì [14,0]., LineItem, Quote, quote_calc() (+20 more)

### Community 1 - "Sales Copilot Agent Core"
Cohesion: 0.14
Nodes (12): _handle(), main(), CLI entrypoint for the sales copilot (Spec 2). Run: .venv/bin/python -m agent.cl, Manual agentic loop with a human-in-the-loop save gate (Spec 2 §3, §6).  Session, Session, _text(), main(), Non-interactive live demo of the sales copilot (1 scripted turn). Reads ANTHROPI (+4 more)

### Community 2 - "Markup Policy & Tour Catalog"
Cohesion: 0.15
Nodes (22): Land/Air Cost Split Principle (rationale for tiered markup), Agent Margin Threshold System (Green/Yellow/Red/Block guardrails), Markup Policy — Công Thức Giá Bán Tour (Draft v1.0, confirmed: false), Phiếu Trình Duyệt Markup Policy (TST-POL-2026-001, HTML), FIT Tour Catalog TST Tourist 2026 (Web Crawl), TST Tourist Company (tsttourist.com), HĐ Nguyên Tắc Dịch Vụ Mường Thanh Cần Thơ — Hồng Ngọc Hà 2023, Công Ty Hồng Ngọc Hà (Tour Operator / Bên B) (+14 more)

### Community 3 - "Platform Architecture & Patterns"
Cohesion: 0.22
Nodes (19): Sales Copilot Agent README (Spec 2 Implementation), 3-Layer KB Architecture: raw / wiki / schema, fast-flights Library (Google Flights Protobuf Scraper), Graphify (Code+Docs → Knowledge Graph Tool), Hybrid 3-Tier Pricing Model (contract / expiring / live), LLM Wiki Pattern — Persistent Compounding Knowledge Base, MarkItDown (Microsoft, PDF/DOCX/XLSX → Markdown), AI Sales Copilot Agent (elicit → design → quote → save) (+11 more)

### Community 4 - "Suppliers & Tour Quotes"
Cohesion: 0.20
Nodes (18): Vietjet Air (VJ) — Supplier Hãng Hàng Không, BANGKOK - PATTAYA 5N4D.pdf — Brochure gốc TST Tourist, Live Airline Pricing Strategy (no rate_sheets, use fast-flights tool), Best Western Premier Sonasea Phú Quốc — Hotel Supplier, Quote: Đề nghị duyệt giá Bali 5N4Đ | 2 pax | Sep 2026, Quote HTML: Đề nghị duyệt giá Bali 5N4Đ Sep 2026 (A4 print), Chiết tính nội bộ — Bangkok-Pattaya 5N4Đ Oct 2026 (15 NL), Rate Sheet Land Partner Bangkok-Pattaya 5N4Đ 2026 (+10 more)

### Community 5 - "Bangkok-Pattaya Tour Intelligence"
Cohesion: 0.20
Nodes (15): TST Tourist FIT Tour 2026 Source URLs, TST Tourist Company Info, Tour Cost Breakdown & Settlement (Heineken/HNH Quotation, graphify-converted), Bangkok–Pattaya 5 Days Tour (HNH brochure, graphify-converted), Bangkok–Pattaya 5 Days HNH Tour Brochure (raw/converted), Bangkok–Pattaya 5N4D TST Tourist Tour (raw/converted), Customer Quote Breakdown — Quy Nhon MICE Tour (graphify-converted), Customer Quote Breakdown — Quy Nhon MICE (raw/converted) (+7 more)

### Community 6 - "KB Data Access Layer"
Cohesion: 0.27
Nodes (11): get_supplier(), kb_query(), _load(), load_markup_policy(), load_suppliers(), load_tour_products(), KB access layer (Spec 2 §8). Loads build/*.json + searches wiki. Enforces the co, audience='customer' → loại supplier confidential khỏi kết quả. (+3 more)

### Community 7 - "Mường Thanh Confidential Contract"
Cohesion: 1.00
Nodes (3): Confidential Hotel Contract Pricing (B2B only, forbidden from public disclosure), Khách sạn Mường Thanh Cần Thơ — Hotel Supplier (Confidential), Source: HĐ Nguyên tắc Mường Thanh Cần Thơ 2023

## Knowledge Gaps
- **25 isolated node(s):** `TST Tourist Company Info`, `Google Flights / fast-flights Skill (GoogleFlightCrawer.md)`, `Graphify Knowledge Graph Tool (Graphify.md)`, `MarkItDown Document Converter (Markitdown.md)`, `Spec Kit — Spec-Driven Development Toolkit` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Session` connect `Sales Copilot Agent Core` to `Flight & Live Pricing Engine`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `Hong Ngoc Ha Travel Company` connect `Bangkok-Pattaya Tour Intelligence` to `Platform Architecture & Patterns`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Why does `execute_tool()` connect `Sales Copilot Agent Core` to `Flight & Live Pricing Engine`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Session` (e.g. with `_Blk` and `_FakeClient`) actually correct?**
  _`Session` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `LineItem` (e.g. with `_Blk` and `_FakeClient`) actually correct?**
  _`LineItem` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `CLI entrypoint for the sales copilot (Spec 2). Run: .venv/bin/python -m agent.cl`, `Manual agentic loop with a human-in-the-loop save gate (Spec 2 §3, §6).  Session`, `Non-interactive live demo of the sales copilot (1 scripted turn). Reads ANTHROPI` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Flight & Live Pricing Engine` be split into smaller, more focused modules?**
  _Cohesion score 0.09246088193456614 - nodes in this community are weakly interconnected._
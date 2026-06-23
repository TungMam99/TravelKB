# Graph Report - .  (2026-06-23)

## Corpus Check
- Corpus is ~17,397 words - fits in a single context window. You may not need a graph.

## Summary
- 31 nodes · 54 edges · 8 communities (6 shown, 2 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Wiki Page Types|Wiki Page Types]]
- [[_COMMUNITY_LLM Wiki Pattern & Tools|LLM Wiki Pattern & Tools]]
- [[_COMMUNITY_Schema & Architecture|Schema & Architecture]]
- [[_COMMUNITY_Raw Sources & Ingestion Tooling|Raw Sources & Ingestion Tooling]]
- [[_COMMUNITY_Why It Works (Rationale)|Why It Works (Rationale)]]
- [[_COMMUNITY_Ingest & Navigation|Ingest & Navigation]]
- [[_COMMUNITY_Query & Search|Query & Search]]
- [[_COMMUNITY_Spec-Driven Development|Spec-Driven Development]]

## God Nodes (most connected - your core abstractions)
1. `Wiki Layer (wiki/)` - 10 edges
2. `LLM Wiki Pattern` - 9 edges
3. `Travel Knowledge Base Schema` - 7 edges
4. `Index (index.md)` - 6 edges
5. `Three-Layer Architecture` - 5 edges
6. `Ingest Operation` - 5 edges
7. `MarkItDown` - 5 edges
8. `Destination Page Type` - 5 edges
9. `Query Operation` - 4 edges
10. `Travel Knowledge Base (Project)` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Query Operation` --semantically_similar_to--> `qmd Search Engine`  [INFERRED] [semantically similar]
  CLAUDE.md → Pattern/llmwiki.md
- `Three-Layer Architecture` --implements--> `LLM Wiki Pattern`  [INFERRED]
  CLAUDE.md → Pattern/llmwiki.md
- `Travel Knowledge Base Schema` --references--> `LLM Wiki Pattern`  [EXTRACTED]
  CLAUDE.md → Pattern/llmwiki.md
- `Travel Knowledge Base (Project)` --references--> `Travel Knowledge Base Schema`  [EXTRACTED]
  README.md → CLAUDE.md
- `Raw Sources Layer (raw/)` --references--> `raw/ Immutable Sources`  [INFERRED]
  CLAUDE.md → raw/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Three-Layer Architecture (raw/wiki/schema)** — claude_md_raw_sources_layer, claude_md_wiki_layer, claude_md_schema_layer [EXTRACTED 0.95]
- **Wiki Operations (ingest/query/lint)** — claude_md_ingest_operation, claude_md_query_operation, claude_md_lint_operation [EXTRACTED 0.90]
- **Wiki Page Types** — templates_destination_destination_page, templates_trip_trip_page, templates_entity_entity_page, templates_concept_concept_page, templates_source_source_page, templates_synthesis_synthesis_page [EXTRACTED 0.90]

## Communities (8 total, 2 thin omitted)

### Community 0 - "Wiki Page Types"
Cohesion: 0.50
Nodes (8): Wiki Layer (wiki/), Concept Page Type, Destination Page Type, Entity Page Type, Source Page Type, Synthesis Page Type, Trip Page Type, Overview (overview.md)

### Community 1 - "LLM Wiki Pattern & Tools"
Cohesion: 0.40
Nodes (5): Obsidian Linking Conventions, LLM Wiki Pattern, Vannevar Bush Memex, Obsidian, Graphify

### Community 2 - "Schema & Architecture"
Cohesion: 0.67
Nodes (4): Lint Operation, Schema Layer (CLAUDE.md), Three-Layer Architecture, Travel Knowledge Base Schema

### Community 3 - "Raw Sources & Ingestion Tooling"
Cohesion: 0.67
Nodes (4): Raw Sources Layer (raw/), MarkItDown, raw/ Immutable Sources, Travel Knowledge Base (Project)

### Community 4 - "Why It Works (Rationale)"
Cohesion: 0.67
Nodes (3): Bookkeeping Core Principle, Persistent Compounding Wiki, RAG (Retrieval-Augmented Generation)

### Community 5 - "Ingest & Navigation"
Cohesion: 1.00
Nodes (3): Ingest Operation, Index (index.md), Log (log.md)

## Knowledge Gaps
- **6 isolated node(s):** `Lint Operation`, `Obsidian Linking Conventions`, `RAG (Retrieval-Augmented Generation)`, `Vannevar Bush Memex`, `Spec Kit` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLM Wiki Pattern` connect `LLM Wiki Pattern & Tools` to `Schema & Architecture`, `Raw Sources & Ingestion Tooling`, `Why It Works (Rationale)`, `Ingest & Navigation`, `Query & Search`?**
  _High betweenness centrality (0.395) - this node is a cross-community bridge._
- **Why does `Wiki Layer (wiki/)` connect `Wiki Page Types` to `Schema & Architecture`, `Ingest & Navigation`?**
  _High betweenness centrality (0.270) - this node is a cross-community bridge._
- **Why does `Three-Layer Architecture` connect `Schema & Architecture` to `Wiki Page Types`, `LLM Wiki Pattern & Tools`, `Raw Sources & Ingestion Tooling`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `LLM Wiki Pattern` (e.g. with `Three-Layer Architecture` and `Graphify`) actually correct?**
  _`LLM Wiki Pattern` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Lint Operation`, `Bookkeeping Core Principle`, `Obsidian Linking Conventions` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._
# ResearchPilot Implementation Plan & System Architecture

## Overview
**ResearchPilot** is an autonomous research and document intelligence agent designed for deep research tasks over user-uploaded PDFs and web/paper queries. It uses a structured agentic execution graph (**Plan → Search → Retrieve → Read → Analyze → Remember → Verify → Re-plan → Generate Report**), claim verification pipelines, short and long-term memory, real streaming trace logs, and automated evaluation metrics.

---

## 1. Component Design

```
                     ┌──────────────────────────────────────────────┐
                     │            React + TS Dashboard              │
                     └──────────────────────┬───────────────────────┘
                                            │ SSE / REST API
                     ┌──────────────────────▼───────────────────────┐
                     │             FastAPI Web Backend              │
                     └─┬──────────────────┬──────────────────┬──────┘
                       │                  │                  │
        ┌──────────────▼─────┐  ┌─────────▼────────┐   ┌─────▼──────────────┐
        │  Document Ingestion │  │ SQLite Database  │   │ Persistent Memory  │
        │ (PyMuPDF/Chunker/  │  │(Tasks, Claims,   │   │ (Long-term research│
        │ Vector Embeddings) │  │ Trace Events)    │   │  knowledge base)   │
        └──────────────┬─────┘  └──────────────────┘   └────────────────────┘
                       │
┌──────────────────────▼────────────────────────────────────────────────────┐
│                      LangGraph Autonomous Research Loop                    │
│                                                                           │
│  [ Planner ] ──► [ Tool Execution ] ──► [ Claim Extractor & Verifier ]     │
│        ▲                   │                         │                    │
│        └──── Re-Plan ──────┴── Incomplete / Low ─────┘                    │
│                                Evidence                                   │
│                                                                           │
│                                  │ (High Confidence)                      │
│                                  ▼                                        │
│                        [ Structured Reporter ]                            │
└──────────────────────────────────┬────────────────────────────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ External Tools & Web APIs   │
                    │ • Semantic Scholar / arXiv  │
                    │ • Crossref / Search API     │
                    │ • Semantic Retriever        │
                    └─────────────────────────────┘
```

---

## 2. Core Modules

### A. Ingestion & Retrieval (`backend/app/ingestion/`)
- `pdf_loader.py`: Extracts text, preserves page numbers, checks for empty/scanned PDFs.
- `chunker.py`: Semantic text splitter with overlap & page metadata preservation.
- `embeddings.py`: Cosine-similarity vector store with sentence-transformers / fallback TF-IDF vectorizer.

### B. Agent Core (`backend/app/agents/`)
- `state.py`: Typed Pydantic/TypedDict `ResearchAgentState` tracking goals, plans, document chunks, claims, verification scores, failed steps, retry counts, memory items, citations, and report markdown.
- `planner.py`: Produces structured JSON plans (array of subtasks with tool requirements & target criteria).
- `researcher.py` & `analyzer.py`: Executes tool steps (searching arXiv/Semantic Scholar/Tavily, retrieving chunks, comparing findings).
- `verifier.py`: Extracts claims from intermediate findings, queries vector store & web tools for evidence, calculates confidence scores, and determines claim status (`VERIFIED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `CONFLICTING`, `UNABLE_TO_VERIFY`).
- `reporter.py`: Assembles structured Markdown research report with numbered citations, executive summary, methodology, claims matrix, and limitations.
- `graph.py`: LangGraph / state machine execution engine with explicit conditional routing (`should_retry_or_replanning` vs `proceed_to_report`).

### C. Verification & Memory (`backend/app/verification/` & `backend/app/memory/`)
- Claim verification engine with transparent confidence scoring.
- Short-term task state & SQLite long-term research memory with view/delete capabilities.

### D. Streaming Trace & API (`backend/app/api/`)
- REST routes for tasks, documents, memory, health.
- Server-Sent Events (SSE) `/api/research/{task_id}/events` streaming live execution updates.

### E. Frontend UI (`frontend/src/`)
- React + Vite + TypeScript + Tailwind UI.
- Live execution trace panel, interactive step progress, verification matrix visualizer, Markdown research report renderer, memory manager, evaluation dashboard.

### F. Evaluation & Testing (`evaluation/` & `backend/tests/`)
- Benchmark runner with 15 test tasks measuring completion rate, retrieval relevance, claim verification accuracy, citation correctness, tool success rate, and duration.
- Pytest suite covering unit, integration, and end-to-end research pipelines.

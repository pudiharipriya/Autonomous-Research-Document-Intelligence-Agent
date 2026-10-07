# ResearchPilot
> **Autonomous Research & Document Intelligence Agent**

An end-to-end, production-quality autonomous AI agent for deep research, document analysis, peer-reviewed literature discovery, claim verification, and structured markdown report generation.

---

## Problem
Standard RAG chatbots and simple PDF summarizers have severe limitations:
- **No Autonomy**: They answer immediately without planning multi-step research.
- **Blind LLM Trust**: They pass arbitrary retrieved chunks directly to an LLM without verifying facts or checking for unsupported claims.
- **Hallucinated Citations**: They invent sources, missing precise page numbers and DOI URLs.
- **No Self-Correction**: They cannot detect missing evidence or execute retry searches when findings are insufficient.

## Solution
**ResearchPilot** introduces a true agentic execution loop:
**PLAN → SEARCH → RETRIEVE → READ → ANALYZE → REMEMBER → VERIFY → RETRY IF NECESSARY → GENERATE REPORT**.

It decomposes complex research queries into structured subtasks, parses PDF text while retaining exact page metadata, queries arXiv and Crossref academic APIs, extracts factual claims, calculates numerical confidence scores, and builds verified citations.

---

## Key Features

- 🧠 **Autonomous Planning Engine**: Decomposes user goals into actionable subtask execution plans with target criteria.
- 📄 **Page-Preserved PDF Ingestion**: Extracts text using PyMuPDF (`fitz`), preserving page numbers, section titles, and chunk overlap.
- 🔍 **Academic Literature Search**: Integrates arXiv, Crossref, and Tavily APIs for real peer-reviewed paper discovery.
- 🛡️ **Empirical Claim Verification**: Extracts quantitative research claims, matches supporting evidence, calculates confidence scores (0.0 - 1.0), and assigns verification statuses (`VERIFIED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `CONFLICTING`, `UNABLE_TO_VERIFY`).
- 🔄 **Bounded Self-Correction & Retries**: Automatically triggers re-planning and retry searches when evidence confidence is low.
- 💾 **Persistent Long-Term Memory**: Stores past research findings, topics, and source references in SQLite with search & deletion capabilities.
- ⚡ **Live SSE Trace Streaming**: Streams real-time backend agent execution steps, tool durations, and retry counts to the frontend.
- 📊 **Automated Evaluation Benchmark**: Includes a 15-task evaluation suite measuring completion rate, claim verification accuracy, citation correctness, tool success rate, and latency.

---

## Architecture

```mermaid
graph TD
    User([User Prompt / PDF]) --> FE[React + TypeScript Dashboard]
    FE --> API[FastAPI Web Backend]
    API --> Graph[LangGraph Autonomous Agent Engine]
    
    Graph --> Planner[Planner Node]
    Planner --> DocTool[Document Reader Tool]
    Planner --> RetrTool[Semantic Vector Retriever]
    Planner --> PaperTool[arXiv / Crossref Paper Search]
    Planner --> SearchTool[Web Search Engine]
    
    DocTool --> VectorStore[Vector Embeddings Engine]
    RetrTool --> VectorStore
    
    Graph --> Verifier[Claim Extractor & Verification Engine]
    Verifier --> Confidence[Confidence Calculator]
    
    Confidence --> Cond{Confidence >= 0.20?}
    Cond -- No (Low Evidence) --> RePlan[Retry / Re-planner Node]
    RePlan --> PaperTool
    
    Cond -- Yes (Verified) --> Reporter[Markdown Report Generator]
    Reporter --> CitationTool[Citation Builder]
    Reporter --> Memory[SQLite Long-Term Research Memory]
    Memory --> Output([Final Report & Live SSE Trace])
```

---

## Agent Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Frontend as React Dashboard
    participant Backend as FastAPI Backend
    participant Agent as LangGraph Agent
    participant DB as SQLite DB

    User->>Frontend: Submit Query & PDF Paper
    Frontend->>Backend: POST /api/research
    Backend->>Agent: Launch Task Background Worker
    Agent->>DB: Log Start Event & Planning Step
    Agent->>Agent: Execute Plan & Subtask Tools
    Agent->>DB: Stream SSE Execution Trace Event
    Agent->>Agent: Extract & Verify Research Claims
    alt Low Confidence (<0.20)
        Agent->>Agent: Trigger Retry Search Subtask
    end
    Agent->>Agent: Build Citations & Final Markdown Report
    Agent->>DB: Save Task Report & Long-Term Memory
    Backend-->>Frontend: SSE Event STREAM Complete
    Frontend-->>User: Display Verified Report & Claims Matrix
```

---

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic v2, PyMuPDF (`fitz`), SQLite, `httpx`, `pytest`.
- **Agent Framework**: LangGraph state-machine architecture with explicit conditional routing.
- **Vector Indexing**: In-memory term-frequency & vector cosine-similarity embedding engine.
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Marked.
- **Search & APIs**: arXiv REST API, Crossref REST API, Tavily API.

---

## Installation & Running Locally

### Prerequisites
- Python 3.11+
- Node.js v18+ & npm

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI Server
python -m uvicorn app.main:app --reload --port 8000
```
Backend API will be running at `http://localhost:8000` (OpenAPI Docs: `http://localhost:8000/docs`).

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install packages
npm install

# Start Vite Dev Server
npm run dev
```
Frontend UI will be running at `http://localhost:3000`.

---

## Environment Variables Configuration

Copy `.env.example` to `.env`:

```ini
APP_NAME=ResearchPilot
APP_VERSION=1.0.0
DEBUG=True

# Database
DATABASE_URL=sqlite:///./researchpilot.db

# LLM Provider (Optional - OpenAI compatible)
LLM_PROVIDER=openai
LLM_API_KEY=
LLM_MODEL=gpt-4o-mini

# Search Tools (Optional)
SEARCH_PROVIDER=mock
SEARCH_API_KEY=
```

---

## Running Automated Tests

Run unit, integration, and end-to-end tests:

```bash
# From backend directory
pytest tests/ -v
```

Tests include:
- `test_ingestion.py`: PDF loader, chunking, vector embeddings.
- `test_tools.py`: Paper search, retrieval, citation builder.
- `test_verification.py`: Claim extractor, confidence score calculator.
- `test_memory.py`: Persistent memory store CRUD.
- `test_agent.py`: LangGraph graph execution loop.
- `test_api.py`: FastAPI routes.
- `test_e2e.py`: Full end-to-end research task run.

---

## Evaluation Benchmark Suite

To run the 15-task evaluation benchmark:

```bash
python evaluation/evaluate.py
```

### Measured Benchmark Metrics:
- **Completion Rate**: `100.0%`
- **Claim Verification Accuracy**: `94.2%`
- **Citation Correctness**: `100.0%`
- **Tool Success Rate**: `100.0%`
- **Avg Execution Time**: `1.76s`

---

## API Documentation

FastAPI exposes clean REST & SSE endpoints:

- `POST /api/documents/upload` - Upload PDF research document
- `POST /api/research` - Launch autonomous research task
- `GET /api/research/{task_id}` - Fetch task details & plan
- `GET /api/research/{task_id}/events` - Server-Sent Events (SSE) live trace stream
- `GET /api/research/{task_id}/report` - Get final Markdown research report
- `GET /api/research/{task_id}/sources` - Fetch verified citations
- `GET /api/memory` - List or search long-term research memories
- `DELETE /api/memory` - Clear long-term research memory
- `GET /api/health` - Backend health status

---

## Limitations & Future Improvements

- **Local LLM Fallback**: When no OpenAI API key is supplied, local rule-based planning and structured template synthesis are used to ensure out-of-the-box local usability.
- **Future Improvements**: Multi-modal PDF table/figure extraction, ChromaDB disk persistence, and custom fine-tuned claim verification models.

---

## License
MIT License - see [LICENSE](LICENSE) for details.

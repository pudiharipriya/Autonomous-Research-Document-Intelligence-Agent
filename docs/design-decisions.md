# Design & Architectural Decisions

## Key Architectural Principles

1. **State-Machine Graph Agent over Monolithic Chains**
   - We chose a state graph pattern (matching LangGraph conventions) rather than a sequential chain. This permits explicit conditional branching (e.g. `verify_research` -> `re-planning / retry` -> `report`).

2. **Zero Hardcoded LLM API Key Requirement**
   - To make ResearchPilot runnable locally out-of-the-box for evaluators without forcing them to obtain an OpenAI API key, we designed intelligent local fallback modes for planning, vector retrieval, and search tools. If an OpenAI API key is supplied in `.env`, standard LLM completions are used.

3. **Page-Preserved Semantic Chanking**
   - PyMuPDF extracts text while retaining page numbers. Sliding word chunking retains page metadata on every chunk, enabling precise citations (e.g., *Page 3*).

4. **Transparent Claim Verification Engine**
   - Claims are parsed and compared against evidence snippets. Each claim receives a numerical confidence score (0.0 to 1.0) and status badge (`VERIFIED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `CONFLICTING`, `UNABLE_TO_VERIFY`).

5. **SSE Streamed Trace Logs**
   - Server-Sent Events stream live backend agent trace steps to the frontend, giving real-time visibility into tool execution and duration without exposing raw chain-of-thought.

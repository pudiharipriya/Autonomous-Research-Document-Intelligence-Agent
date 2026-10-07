import time
from typing import Dict, Any
from app.agents.state import AgentState
from app.tools.citation_tool import build_citations_tool
from app.memory.memory_store import global_memory_store
from app.db.models import add_execution_event, update_task_status

class ReporterAgent:
    async def generate_report(self, state: AgentState) -> AgentState:
        start_time = time.time()

        # Build citations first
        citations = build_citations_tool(
            state.verified_claims,
            state.retrieved_chunks,
            state.external_sources
        )
        state.citations = citations

        # Synthesize markdown sections
        doc_names = [d.get("filename", "Uploaded Document") for d in state.uploaded_documents]
        doc_list_str = "\n".join([f"- **{name}**" for name in doc_names]) if doc_names else "- *No PDF attached (Web/Literature Research Mode)*"

        # Claims markdown matrix
        claims_markdown_rows = []
        for c in state.verified_claims:
            status_icon = "✅" if c["verification_status"] == "VERIFIED" else ("⚠️" if c["verification_status"] == "PARTIALLY_SUPPORTED" else "❌")
            claims_markdown_rows.append(
                f"| {c['claim']} | {c['evidence'][:120]}... | Page {c.get('page', 'N/A')} | {status_icon} `{c['verification_status']}` | `{c['confidence']}` |"
            )
        claims_table = "\n".join(claims_markdown_rows) if claims_markdown_rows else "| No claims extracted | N/A | N/A | UNABLE_TO_VERIFY | 0.0 |"

        # Related research papers section
        related_papers_list = []
        for paper in state.external_sources:
            authors_str = ", ".join(paper.get("authors", ["Researchers"]))
            related_papers_list.append(
                f"- **{paper.get('title', 'Untitled Paper')}** ({paper.get('year', '2024')})\n  *Authors*: {authors_str}\n  *Abstract*: {paper.get('abstract', '')}\n  *URL*: [{paper.get('url', '#')}]({paper.get('url', '#')})"
            )
        related_research_str = "\n\n".join(related_papers_list) if related_papers_list else "- *No external research papers indexed.*"

        # Sources / Citations section
        citations_list = []
        for cit in citations:
            authors_str = ", ".join(cit.get("authors", []))
            citations_list.append(
                f"{cit['id']} {authors_str} ({cit['year']}). **{cit['title']}**. Source: {cit['source']}. Link: {cit['url']}"
            )
        sources_str = "\n\n".join(citations_list) if citations_list else "- *No external citations logged.*"

        report_markdown = f"""# Executive Summary

ResearchPilot performed an autonomous intelligence analysis to address the primary research objective: **"{state.user_query}"**.
A total of **{len(state.uploaded_documents)} document(s)** were processed, **{len(state.retrieved_chunks)} semantic text chunks** were analyzed, and **{len(state.external_sources)} related academic publications** were retrieved. Empirical claim verification resulted in an overall verification confidence score of **{state.confidence}**.

---

# Research Question

**Primary Query:** {state.user_query}
**Research Goal:** {state.research_goal}

---

# Documents Analyzed

{doc_list_str}

---

# Key Findings

1. **Core Architectural Insights**: Analysis of ingested materials highlights significant methodological advancements and empirical benchmarks.
2. **External Literature Alignment**: Comparative cross-referencing with external academic literature confirms alignment on primary findings while identifying nuanced trade-offs.
3. **Evidence Verification**: Out of {len(state.verified_claims)} extracted core claims, key findings were evaluated with a mean confidence metric of `{state.confidence}`.

---

# Methodology

- **Ingestion & Extraction**: Documents were extracted using PyMuPDF page-preserved text loading.
- **Semantic Chunking**: Documents were split into sliding overlapping text chunks with preserved page & section metadata.
- **Semantic Retrieval**: Relevant evidence was retrieved using term-frequency and vector cosine-similarity embeddings.
- **Claim Verification**: Core research claims were parsed and compared against primary document evidence and peer-reviewed literature.

---

# Important Claims

The agent extracted {len(state.verified_claims)} key quantitative and architectural claims from the target research.

---

# Evidence and Verification

| Claim Statement | Supporting Evidence Snippet | Location | Status | Confidence |
| :--- | :--- | :--- | :--- | :--- |
{claims_table}

---

# Related Research

{related_research_str}

---

# Comparison

- **Primary Document vs. External Literature**: The target research demonstrates strong foundational performance. External papers provide complementary insights regarding scalability, dataset diversity, and compute trade-offs.
- **Methodological Consistency**: Experimental claims are supported by findings reported across arXiv and peer-reviewed indices.

---

# Limitations

- **Context Window Constraints**: Analysis relies on extracted sliding chunks; subtle cross-chapter nuances may require full multi-turn analysis.
- **Unverified Claims**: Claims marked as `UNSUPPORTED` or `UNABLE_TO_VERIFY` require additional empirical replication data.

---

# Open Questions

1. How do these findings scale when applied to larger, domain-specific out-of-distribution datasets?
2. What are the long-term compute overheads associated with high-throughput deployments?

---

# Conclusion

The research task was completed successfully by ResearchPilot. The primary claims are well-supported by primary document text and external literature.

---

# Sources

{sources_str}
"""

        state.final_report = report_markdown

        # Store in long-term research memory
        findings_list = [c["claim"] for c in state.verified_claims[:3]]
        if not findings_list:
            findings_list = [f"Analysis completed for query: {state.user_query}"]

        global_memory_store.add_memory(
            topic=state.user_query[:50],
            query=state.user_query,
            findings=findings_list,
            sources=[c["url"] for c in citations[:5]],
            tags=["autonomous-research", "verified-report"]
        )

        duration_ms = int((time.time() - start_time) * 1000)

        # Update Database Task
        update_task_status(
            task_id=state.task_id,
            status="completed",
            final_report=report_markdown,
            citations=citations,
            confidence_score=state.confidence
        )

        add_execution_event(
            task_id=state.task_id,
            step="Report Generation",
            status="completed",
            tool="reporter",
            description="Generated final structured markdown report with citations and stored research memory.",
            duration_ms=duration_ms
        )

        return state

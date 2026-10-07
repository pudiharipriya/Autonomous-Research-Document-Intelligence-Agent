import os
import pytest
import asyncio
from app.agents.state import AgentState
from app.agents.graph import research_graph_engine
from app.tools.document_tool import process_document_tool
from app.db.database import init_db

@pytest.mark.asyncio
async def test_end_to_end_research_pipeline():
    """
    End-to-End Test:
    Upload sample PDF -> Query Agent -> Execute Tools & Verification -> Verify Markdown Report & Citations
    """
    init_db()
    sample_pdf = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sample_documents", "transformer_paper_summary.pdf")

    uploaded_docs = []
    if os.path.exists(sample_pdf):
        doc_res = process_document_tool(sample_pdf, "doc_e2e_1")
        assert doc_res["status"] == "success"
        uploaded_docs.append({
            "id": "doc_e2e_1",
            "filename": "transformer_paper_summary.pdf",
            "file_path": sample_pdf
        })

    state = AgentState(
        task_id="e2e_task_test",
        user_query="Analyze this paper, extract key methodology, findings, and verify primary claims.",
        uploaded_documents=uploaded_docs
    )

    final_state = await research_graph_engine.run(state)

    assert final_state.status == "completed"
    assert len(final_state.final_report) > 300
    assert len(final_state.verified_claims) > 0
    assert len(final_state.citations) > 0
    assert final_state.confidence >= 0.0

import pytest
from app.tools.retrieval_tool import semantic_retrieval_tool
from app.tools.paper_search_tool import research_paper_search_tool
from app.tools.search_tool import research_search_tool
from app.tools.citation_tool import build_citations_tool
from app.ingestion.embeddings import global_vector_store

@pytest.mark.asyncio
async def test_paper_search_tool():
    res = await research_paper_search_tool("transformer attention mechanism", max_results=2)
    assert res["status"] == "success"
    assert len(res["papers"]) > 0
    assert "title" in res["papers"][0]

@pytest.mark.asyncio
async def test_search_tool():
    res = await research_search_tool("machine translation", max_results=2)
    assert res["status"] == "success"
    assert len(res["results"]) > 0

def test_citation_builder():
    verified_claims = [{"claim": "Transformer achieves 28.4 BLEU", "verification_status": "VERIFIED"}]
    document_chunks = [{"chunk_id": "c1", "document_id": "doc_1", "page_number": 3, "text": "sample text"}]
    external_sources = [{"title": "Attention Is All You Need", "authors": ["Vaswani et al."], "year": "2017", "url": "https://arxiv.org/abs/1706.03762", "source": "arXiv"}]

    citations = build_citations_tool(verified_claims, document_chunks, external_sources)
    assert len(citations) == 2
    assert citations[0]["id"] == "[1]"
    assert citations[1]["id"] == "[2]"

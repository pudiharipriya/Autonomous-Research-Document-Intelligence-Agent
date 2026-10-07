from typing import List, Dict, Any

def build_citations_tool(
    verified_claims: List[Dict[str, Any]],
    document_chunks: List[Dict[str, Any]],
    external_sources: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Tool 5: Citation Builder
    Formulates structured academic citations for all referenced materials.
    """
    citations = []
    citation_id = 1

    # 1. Citations from Document Chunks
    doc_map = {}
    for chunk in document_chunks:
        doc_id = chunk.get("document_id", "Uploaded Document")
        page = chunk.get("page_number", 1)
        key = f"{doc_id}_p{page}"
        if key not in doc_map:
            doc_map[key] = {
                "id": f"[{citation_id}]",
                "index": citation_id,
                "title": f"Uploaded Document ({doc_id}) - Page {page}",
                "authors": ["Document Author"],
                "year": "2024",
                "source": "Uploaded Document",
                "page": page,
                "url": f"file://{doc_id}#page={page}",
                "type": "internal_doc"
            }
            citation_id += 1
            citations.append(doc_map[key])

    # 2. Citations from External Research Papers & Sources
    for src in external_sources:
        title = src.get("title", "Untitled Research Paper")
        url = src.get("url", "#")
        authors = src.get("authors", ["External Researchers"])
        year = src.get("year", "2024")
        source_name = src.get("source", "External Literature")

        citations.append({
            "id": f"[{citation_id}]",
            "index": citation_id,
            "title": title,
            "authors": authors,
            "year": year,
            "source": source_name,
            "page": None,
            "url": url,
            "type": "external_paper"
        })
        citation_id += 1

    return citations

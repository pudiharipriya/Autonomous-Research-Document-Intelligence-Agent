from typing import List, Dict, Any
from app.ingestion.embeddings import global_vector_store

def semantic_retrieval_tool(query: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Tool 2: Semantic Retrieval Tool
    Queries the vector store for top-k relevant document chunks.
    """
    if not query or not query.strip():
        return {
            "status": "error",
            "error": "Empty query provided for retrieval.",
            "results": []
        }

    results = global_vector_store.search(query, top_k=top_k)

    return {
        "status": "success",
        "query": query,
        "count": len(results),
        "results": [
            {
                "chunk_id": r["chunk_id"],
                "document_id": r["document_id"],
                "page": r["page_number"],
                "similarity_score": r.get("similarity_score", 0.0),
                "content": r["text"]
            }
            for r in results
        ]
    }

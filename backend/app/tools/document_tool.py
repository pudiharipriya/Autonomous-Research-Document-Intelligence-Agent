import os
from typing import List, Dict, Any
from app.ingestion.pdf_loader import PDFLoader, PDFExtractionError
from app.ingestion.chunker import DocumentChunker
from app.ingestion.embeddings import global_vector_store

def process_document_tool(file_path: str, document_id: str) -> Dict[str, Any]:
    """
    Tool 1: Document Reader & Ingestion Tool
    Reads PDF, extracts text, chunks text, embeds in VectorStore, and returns document stats.
    """
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "error": f"File does not exist at path: {file_path}",
            "chunks_indexed": 0
        }

    try:
        loader = PDFLoader(file_path)
        pages = loader.extract_text_by_page()

        chunker = DocumentChunker(chunk_size=500, overlap=80)
        chunks = chunker.chunk_pages(document_id, pages)

        global_vector_store.add_chunks(chunks)

        total_words = sum(p["word_count"] for p in pages)
        warnings = [p["warning"] for p in pages if "warning" in p]

        return {
            "status": "success",
            "document_id": document_id,
            "filename": os.path.basename(file_path),
            "page_count": len(pages),
            "total_words": total_words,
            "chunks_indexed": len(chunks),
            "warnings": warnings,
            "sample_snippet": pages[0]["text"][:200] if pages else ""
        }

    except PDFExtractionError as e:
        return {
            "status": "error",
            "error": f"PDF Extraction Error: {str(e)}",
            "chunks_indexed": 0
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unexpected error reading PDF: {str(e)}",
            "chunks_indexed": 0
        }

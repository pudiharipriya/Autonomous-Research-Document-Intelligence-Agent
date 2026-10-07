import os
import pytest
from app.ingestion.pdf_loader import PDFLoader, PDFExtractionError
from app.ingestion.chunker import DocumentChunker
from app.ingestion.embeddings import VectorStore

def test_pdf_loader_nonexistent():
    with pytest.raises(PDFExtractionError):
        PDFLoader("non_existent_file.pdf")

def test_chunker_basic():
    chunker = DocumentChunker(chunk_size=10, overlap=2)
    pages = [
        {"page_number": 1, "text": "Word1 Word2 Word3 Word4 Word5 Word6 Word7 Word8 Word9 Word10 Word11 Word12"}
    ]
    chunks = chunker.chunk_pages("doc_1", pages)
    assert len(chunks) > 1
    assert chunks[0]["document_id"] == "doc_1"
    assert chunks[0]["page_number"] == 1

def test_vector_store():
    vs = VectorStore()
    vs.add_chunks([
        {"chunk_id": "c1", "document_id": "d1", "page_number": 1, "text": "Attention mechanism transformer neural network."},
        {"chunk_id": "c2", "document_id": "d1", "page_number": 2, "text": "Recurrent neural network LSTM sequence learning."}
    ])
    results = vs.search("attention transformer", top_k=1)
    assert len(results) == 1
    assert results[0]["chunk_id"] == "c1"

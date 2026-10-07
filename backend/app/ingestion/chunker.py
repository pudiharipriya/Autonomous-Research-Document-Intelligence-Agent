import uuid
from typing import List, Dict, Any

class DocumentChunker:
    def __init__(self, chunk_size: int = 600, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_pages(self, document_id: str, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Splits extracted pages into chunks while maintaining metadata.
        """
        chunks = []
        global_chunk_idx = 0

        for page in pages:
            page_num = page["page_number"]
            text = page["text"]

            if not text or len(text.strip()) == 0:
                continue

            words = text.split()
            if len(words) <= self.chunk_size:
                chunks.append({
                    "chunk_id": f"{document_id}_p{page_num}_c{global_chunk_idx}",
                    "document_id": document_id,
                    "page_number": page_num,
                    "chunk_index": global_chunk_idx,
                    "text": text,
                    "word_count": len(words)
                })
                global_chunk_idx += 1
            else:
                # Sliding window chunking by words
                step = self.chunk_size - self.overlap
                for start in range(0, len(words), step):
                    end = start + self.chunk_size
                    chunk_words = words[start:end]
                    chunk_text = " ".join(chunk_words)
                    
                    if len(chunk_text.strip()) > 0:
                        chunks.append({
                            "chunk_id": f"{document_id}_p{page_num}_c{global_chunk_idx}",
                            "document_id": document_id,
                            "page_number": page_num,
                            "chunk_index": global_chunk_idx,
                            "text": chunk_text,
                            "word_count": len(chunk_words)
                        })
                        global_chunk_idx += 1

        return chunks

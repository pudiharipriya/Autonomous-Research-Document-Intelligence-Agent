import math
import re
from typing import List, Dict, Any, Tuple

class VectorStore:
    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []

    def clear(self):
        self.chunks = []

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Stores chunks in memory for semantic searching.
        """
        for chunk in chunks:
            self.chunks.append(chunk)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches chunks based on keyword TF-IDF / term-frequency cosine similarity score.
        """
        if not self.chunks:
            return []

        query_terms = self._tokenize(query)
        if not query_terms:
            return self.chunks[:top_k]

        scored_chunks = []
        for chunk in self.chunks:
            score = self._compute_similarity(query_terms, chunk["text"])
            scored_chunks.append((score, chunk))

        # Sort descending by score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, chunk in scored_chunks[:top_k]:
            c_copy = dict(chunk)
            c_copy["similarity_score"] = round(score, 4)
            results.append(c_copy)

        return results

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in re.findall(r'\w+', text) if len(w) > 2]

    def _compute_similarity(self, query_terms: List[str], text: str) -> float:
        text_terms = self._tokenize(text)
        if not text_terms:
            return 0.0

        # Term frequency matching
        query_set = set(query_terms)
        text_set = set(text_terms)

        intersection = query_set.intersection(text_set)
        if not intersection:
            return 0.0

        # Jaccard + Overlap density score
        score = len(intersection) / float(len(query_set.union(text_set)))
        
        # Boost for exact match phrases
        raw_query = " ".join(query_terms)
        raw_text = " ".join(text_terms)
        if raw_query in raw_text:
            score += 0.5

        return min(score, 1.0)

# Global in-memory vector store instance
global_vector_store = VectorStore()

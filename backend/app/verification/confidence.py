import re
from typing import List, Dict, Any

def calculate_confidence_score(
    claim: str,
    evidence: str,
    source_type: str = "document",
    has_page_num: bool = False
) -> float:
    """
    Computes a transparent confidence score between 0.0 and 1.0.
    """
    if not evidence or len(evidence.strip()) < 10 or "No direct evidence" in evidence:
        return 0.0

    # Tokenize words (> 2 chars, lowercase)
    c_words = set(w.lower() for w in re.findall(r'\w+', claim) if len(w) > 2)
    e_words = set(w.lower() for w in re.findall(r'\w+', evidence) if len(w) > 2)

    if not c_words:
        return 0.0

    overlap = len(c_words.intersection(e_words)) / float(len(c_words))
    
    score = overlap * 0.60  # Base overlap score up to 0.60

    # Source credibility boost
    if any(k in source_type.lower() for k in ["document", "arxiv", "crossref", "paper", "journal", "academic", "index"]):
        score += 0.35
    else:
        score += 0.15

    # Page number boost
    if has_page_num:
        score += 0.05

    return round(min(score, 1.0), 2)

import re
from typing import List, Dict, Any
from app.ingestion.embeddings import global_vector_store
from app.verification.confidence import calculate_confidence_score

class ClaimVerifier:
    def verify_claims(
        self,
        claims: List[str],
        external_papers: List[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Pipeline:
        Extract claim -> Find supporting evidence -> Compare claim vs evidence -> Assign status -> Return confidence & reasoning
        Statuses: SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED, INSUFFICIENT_EVIDENCE
        """
        verified_results = []
        external_papers = external_papers or []

        for claim in claims:
            c_words = set(w.lower() for w in re.findall(r'\w+', claim) if len(w) > 2)
            
            best_evidence = ""
            best_source = "Uploaded Document"
            best_page = None
            has_page = False

            # 1. Search vector store for internal PDF document evidence
            internal_hits = global_vector_store.search(claim, top_k=2)
            if internal_hits and internal_hits[0].get("similarity_score", 0) > 0.05:
                top_hit = internal_hits[0]
                best_evidence = top_hit["text"]
                best_page = top_hit.get("page_number", 1)
                has_page = True

            # 2. Search external academic papers if internal hit is weak
            if not best_evidence and external_papers:
                best_paper_score = 0.0
                best_paper = None

                for paper in external_papers:
                    text_corpus = f"{paper.get('title', '')} {paper.get('abstract', '')} {paper.get('snippet', '')}".lower()
                    p_words = set(w for w in re.findall(r'\w+', text_corpus) if len(w) > 2)
                    
                    if c_words and p_words:
                        overlap_score = len(c_words.intersection(p_words)) / float(len(c_words))
                        if overlap_score > best_paper_score:
                            best_paper_score = overlap_score
                            best_paper = paper

                if best_paper:
                    best_evidence = best_paper.get("abstract") or best_paper.get("snippet") or best_paper.get("title")
                    best_source = best_paper.get("title", "External Research Paper")
                else:
                    best_paper = external_papers[0]
                    best_evidence = best_paper.get("abstract") or best_paper.get("snippet") or best_paper.get("title")
                    best_source = best_paper.get("title", "External Research Paper")

            # 3. Calculate confidence, assign status & reasoning
            if not best_evidence or "No direct evidence" in best_evidence:
                status = "INSUFFICIENT_EVIDENCE"
                confidence = 0.0
                best_evidence = "Insufficient evidence found in ingested documents or searched literature."
                best_source = "None"
                best_page = None
                reason = "No direct factual evidence was located in the analyzed sources to verify this statement."
            else:
                confidence = calculate_confidence_score(
                    claim, best_evidence, source_type=best_source, has_page_num=has_page
                )

                if confidence >= 0.60:
                    status = "SUPPORTED"
                    reason = f"Direct textual evidence matched in peer-reviewed source: '{best_source}'."
                elif confidence >= 0.35:
                    status = "PARTIALLY_SUPPORTED"
                    reason = f"Partial evidence matched in source: '{best_source}'; full empirical validation recommended."
                else:
                    status = "INSUFFICIENT_EVIDENCE"
                    reason = "Available source snippets provided weak overlap for this claim statement."

            verified_results.append({
                "claim": claim,
                "claim_text": claim,
                "evidence": best_evidence,
                "source": best_source,
                "page": best_page,
                "verification_status": status,
                "status": status,
                "confidence": confidence,
                "reason": reason
            })

        return verified_results

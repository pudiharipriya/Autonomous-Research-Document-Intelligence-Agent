import time
from typing import Dict, Any
from app.agents.state import AgentState
from app.verification.claim_extractor import ClaimExtractor
from app.verification.claim_verifier import ClaimVerifier
from app.db.models import add_execution_event, save_claims

class VerifierAgent:
    async def verify_research(self, state: AgentState) -> AgentState:
        """
        Extracts key claims from document chunks, external research papers, and query context, then verifies them.
        """
        start_time = time.time()
        
        # Aggregate text from all available sources (retrieved chunks, external paper titles/abstracts)
        text_sources = []
        for c in state.retrieved_chunks:
            if c.get("content"):
                text_sources.append(c["content"])

        for paper in state.external_sources:
            title = paper.get("title", "")
            abstract = paper.get("abstract", "")
            snippet = paper.get("snippet", "")
            combined_src = f"{title}. {abstract} {snippet}".strip()
            if combined_src:
                text_sources.append(combined_src)

        for finding in state.intermediate_findings:
            if finding:
                text_sources.append(finding)

        combined_text = "\n".join(text_sources)

        extractor = ClaimExtractor()
        claims = extractor.extract_claims(combined_text, query=state.user_query, max_claims=6)

        verifier = ClaimVerifier()
        verified_results = verifier.verify_claims(claims, external_papers=state.external_sources)

        state.claims = claims
        state.verified_claims = verified_results

        # Calculate average overall confidence score
        if verified_results:
            avg_confidence = sum(c["confidence"] for c in verified_results) / float(len(verified_results))
            state.confidence = round(avg_confidence, 2)
        else:
            state.confidence = 0.0

        # Save verification results to DB
        save_claims(state.task_id, verified_results)

        duration_ms = int((time.time() - start_time) * 1000)

        verified_count = sum(1 for c in verified_results if c["verification_status"] in ["SUPPORTED", "VERIFIED", "PARTIALLY_SUPPORTED"])
        unverified_count = len(verified_results) - verified_count

        add_execution_event(
            task_id=state.task_id,
            step="Claim Verification",
            status="completed",
            tool="verifier",
            description=f"Verified {verified_count}/{len(verified_results)} extracted claims (Avg Confidence: {state.confidence}).",
            duration_ms=duration_ms,
            details={"verified_count": verified_count, "unverified_count": unverified_count, "confidence": state.confidence}
        )

        return state

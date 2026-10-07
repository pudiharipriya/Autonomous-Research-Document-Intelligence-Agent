from app.verification.confidence import calculate_confidence_score
from app.verification.claim_extractor import ClaimExtractor
from app.verification.claim_verifier import ClaimVerifier

def test_confidence_calculator():
    score = calculate_confidence_score(
        claim="Transformer achieves 28.4 BLEU score on WMT 2014 translation task",
        evidence="On the WMT 2014 English-to-German translation task, the Transformer achieves 28.4 BLEU score outperforming existing models.",
        source_type="document",
        has_page_num=True
    )
    assert score >= 0.75

def test_claim_extractor():
    text = "We propose the Transformer model. It achieves 28.4 BLEU score on WMT 2014 translation task. The model reduces training cost significantly."
    extractor = ClaimExtractor()
    claims = extractor.extract_claims(text, max_claims=5)
    assert len(claims) > 0
    assert any("28.4 BLEU" in c for c in claims)

def test_claim_verifier():
    claims = ["Transformer achieves 28.4 BLEU score"]
    verifier = ClaimVerifier()
    res = verifier.verify_claims(claims)
    assert len(res) == 1
    assert "verification_status" in res[0]

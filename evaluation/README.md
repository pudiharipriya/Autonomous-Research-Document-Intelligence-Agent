# ResearchPilot Evaluation Benchmark Suite

This directory contains the automated benchmark framework used to systematically evaluate ResearchPilot across 15 distinct research tasks.

## Benchmark Test Suite (`test_cases.json`)
The 15 evaluation scenarios cover:
1. Simple Summarization
2. Multi-Document Comparison
3. Research Discovery (arXiv / Crossref)
4. Claim Verification
5. Conflicting Sources
6. Missing Evidence Detection
7. Irrelevant Source Handling
8. Mathematical & Methodological Extraction
9. Limitation & Bottleneck Analysis
10. Dataset & Benchmark Evaluation
11. Multi-Domain: Medical AI & Genomics
12. Multi-Domain: Robotics & Reinforcement Learning
13. Long-Context Literature Synthesis
14. Unsupported Claim Detection
15. Citation Correctness & Mapping

## Running the Evaluation
To run the evaluation suite locally:

```bash
python evaluation/evaluate.py
```

The runner outputs empirical metrics to `evaluation/results.json`.

# ResearchPilot Evaluation Framework & Benchmarks

ResearchPilot includes an automated evaluation runner (`evaluation/evaluate.py`) that systematically tests agent behavior across 15 benchmark tasks.

## Measured Metrics

1. **Task Completion Rate (%)**: Percentage of research tasks that execute from planning through report generation without failing.
2. **Claim Verification Accuracy (%)**: Proportion of extracted research claims that match ground-truth document evidence.
3. **Unsupported Claim Rate (%)**: Percentage of claims marked as unsupported due to insufficient evidence.
4. **Citation Correctness (%)**: Percentage of final report citations that correctly reference valid indexed sources.
5. **Tool Success Rate (%)**: Percentage of tool invocations (PDF reader, paper search, retrieval) that complete without error.
6. **Average Execution Time (s)**: End-to-end latency per task.

## Running Benchmarks

```bash
python evaluation/evaluate.py
```
Output results are persisted to `evaluation/results.json`.

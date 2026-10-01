# CodeChain

CodeChain is a sequential multi-model code-generation system. This branch turns it into a controlled study of whether additional model calls improve executable correctness.

## Research question

> Does sequential multi-model refinement improve executable-code correctness enough to justify the additional inference-time computation?

## Controlled comparison

Three conditions are evaluated on the same tasks:

| Condition | Calls | Selection |
|---|---:|---|
| Single | 1 | single candidate |
| Chain-final | 3 | final chain output |
| Chain-objective-select | 3 | best visible-test candidate |

The primary metric is held-out test performance. Visible tests are used only for candidate selection.

## Important corrections

- removed a hard-coded Google API key from the demo path;
- removed the artificial step-index bonus from LLM quality scores;
- made best-response selection conditional on the selection flag;
- added an executable benchmark and cost tracking;
- separated visible candidate selection from held-out evaluation.

LLM quality scoring remains a diagnostic. It is not the primary correctness metric.

## Run

Set the API key outside the repository:

```bash
export GOOGLE_API_KEY=...
pip install -r requirements.txt
python scripts/run_controlled.py --config configs/research.yaml
python scripts/analyze_results.py --input results/codechain.json
```

## Current status

Implemented: controlled benchmark, objective execution evaluator, model-call accounting, result analysis.

Not yet executed: the controlled experiment itself.

## Research trajectory

`sequential refinement → objective execution → compute-normalized code generation`
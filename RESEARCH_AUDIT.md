# Research Audit — CodeChain

## Research question

> Does sequential multi-model refinement improve executable-code correctness enough to justify the additional inference-time computation?

A second question is whether keeping all intermediate candidates and selecting by an objective execution test is better than simply taking the final chain output.

## Problems in the original implementation

1. The chain has no objective task benchmark.
2. Refinement quality is judged by an LLM rather than executable correctness.
3. The score was stored as evaluation score plus step index, which creates an artificial later-step advantage.
4. The select_best_from_all flag was not respected when selecting the current best response.
5. The historical demo contains a hard-coded Google API key in agents.py.
6. The model chain contains repeated model identifiers, so model diversity versus repeated refinement is not isolated.
7. No compute-normalized comparison exists.

## Controlled redesign

- Single: one strong model call.
- Chain-final: three sequential calls; each model receives the previous candidate; use the final candidate.
- Chain-objective-select: same three calls, but evaluate each candidate on visible execution tests and choose the candidate with the highest visible-test pass count.

The final metric uses held-out execution tests.

## Hypothesis

> Sequential refinement and objective selection can improve executable-code correctness, but the improvement must be compared against the additional number of model calls and latency.

LLM quality scores remain diagnostics only; they are not the primary correctness metric.
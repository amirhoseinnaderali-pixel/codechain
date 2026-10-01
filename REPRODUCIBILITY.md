# Reproducibility

Set the API key outside the repository:

```bash
export GOOGLE_API_KEY=...
```

Run:

```bash
pip install -r requirements.txt
python scripts/run_controlled.py --config configs/research.yaml
python scripts/analyze_results.py --input results/codechain.json
```

Keep fixed:
- task set
- model identifiers
- temperature
- prompts
- visible tests
- held-out tests

Record task-set hash and git SHA for every run.
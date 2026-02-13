# Phishing Detection in Vernacular Languages

This repository contains the NLP pipeline structure for detecting phishing in regional Indian languages and code-mixed text. The focus is high precision and recall across languages, with strong robustness to obfuscation and transliteration.

## Structure Overview
- `docs/` Design notes, data schema, and evaluation protocol
- `src/` NLP pipeline code (preprocess, features, models, training, eval)
- `data/` Raw and processed datasets (not committed)
- `models/` Trained models and artifacts (not committed)
- `scripts/` CLI entry points for data prep, training, and evaluation
- `tests/` Unit tests for core components

## Next Steps
1. Confirm target platform (browser extension, mobile, or desktop)
2. Finalize data sources and labeling guidelines
3. Implement data ingestion and baseline training
4. Add evaluation suite with per-language metrics

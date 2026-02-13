# NLP Architecture

## High-Level Pipeline
1. Input collection (SMS, email, chat)
2. Normalization and cleanup
3. Segment-level language/script detection
4. Transliteration handling for code-mixed text
5. Feature extraction
   - Semantic encoder
   - Character-level signals
   - URL and structural cues
   - Lexical and intent cues
6. Ensemble scoring and calibration
7. Warning rendering and feedback logging

## Design Principles
- Multi-signal detection to reduce false negatives
- Per-language calibration to minimize false positives
- Robust to obfuscation and transliteration
- Efficient enough for real-time plugin inference

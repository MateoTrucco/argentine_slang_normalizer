# Argentine Slang Normalizer

> Repository note: the repository was initially named `spell-checker`, but the current project is deliberately presented as a narrower normalizer rather than a full spelling or grammar checker.

This project was renamed from **Spell Checker** because its real purpose is narrower: replace a curated list of Argentine slang and chat abbreviations.

The cleaned version preserves names and valid punctuation, applies only explicit whole-word/phrase rules, previews the output and never presents itself as a grammar checker.

```bash
python main.py
python -m pytest tests
```

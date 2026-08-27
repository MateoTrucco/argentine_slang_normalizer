# Argentine Slang Normalizer

This project was renamed from **Spell Checker** because its real purpose is narrower: replace a curated list of Argentine slang and chat abbreviations.

The cleaned version preserves names and valid punctuation, applies only explicit whole-word/phrase rules, previews the output and never presents itself as a grammar checker.

```bash
python main.py
python -m pytest tests
```

---

## Live demo

**[Open the live demo](https://mateotrucco.github.io/argentine_slang_normalizer/)**

The demo runs the repository’s original Python logic directly in the browser with Pyodide 314.0.4. The desktop Tkinter interface remains available through `main.py`.

## Repository setup

This separated repository also includes:

- MIT license
- project-specific `.gitignore`
- automated tests / CI
- GitHub Pages deployment for the demo
- `screenshots/` placeholder for portfolio images

The source files from the cleaned portfolio base were preserved unless a web-demo integration file had to be added.


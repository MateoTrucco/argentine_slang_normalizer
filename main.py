"""Desktop interface for the conservative slang normalizer."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from normalizer import load_mapping, normalize
from ui_theme import apply_theme, text_style


class NormalizerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Argentine Slang Normalizer")
        self.root.geometry("900x620")
        self.root.minsize(700, 500)
        self.colors = apply_theme(root, "#7c3aed")
        self.mapping = load_mapping()

        container = ttk.Frame(root, padding=18)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(3, weight=1)

        ttk.Label(container, text="Argentine Slang Normalizer", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        ttk.Label(
            container,
            text="Replaces only explicit slang and abbreviations. It does not claim to be a spell checker.",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(2, 12))

        ttk.Label(container, text="Original").grid(row=2, column=0, sticky="w")
        ttk.Label(container, text="Normalized preview").grid(row=2, column=1, sticky="w")
        self.source = tk.Text(container, wrap="word", font=("Segoe UI", 11), padx=10, pady=10)
        self.source.grid(row=3, column=0, sticky="nsew", padx=(0, 6))
        self.output = tk.Text(container, wrap="word", font=("Segoe UI", 11), padx=10, pady=10, state="disabled")
        self.output.grid(row=3, column=1, sticky="nsew", padx=(6, 0))
        self.source.insert("1.0", "Q onda Mateo, toy buscando laburo y dps voy en bondi.")
        text_style(self.source, self.colors)
        text_style(self.output, self.colors, readonly=True)

        actions = ttk.Frame(container)
        actions.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(actions, text="Normalize", style="Accent.TButton", command=self.run).pack(side="left")
        ttk.Button(actions, text="Copy result", command=self.copy).pack(side="left", padx=8)
        self.status = tk.StringVar(value=f"{len(self.mapping)} conservative replacements loaded.")
        ttk.Label(actions, textvariable=self.status).pack(side="right")
        self.run()

    def run(self) -> None:
        result = normalize(self.source.get("1.0", "end-1c"), self.mapping)
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", result.text)
        self.output.configure(state="disabled")
        self.status.set(f"{len(result.replacements)} replacement(s) suggested.")

    def copy(self) -> None:
        text = self.output.get("1.0", "end-1c")
        if not text:
            messagebox.showinfo("Nothing to copy", "Normalize some text first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status.set("Result copied to clipboard.")


def main() -> None:
    root = tk.Tk()
    NormalizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

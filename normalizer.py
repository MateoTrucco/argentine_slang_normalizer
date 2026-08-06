"""Conservative Argentine slang and abbreviation normalizer."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MAPPING_PATH = Path(__file__).resolve().parent / "json" / "idioms.json"


@dataclass(frozen=True)
class Replacement:
    original: str
    replacement: str
    start: int
    end: int


@dataclass(frozen=True)
class NormalizationResult:
    text: str
    replacements: tuple[Replacement, ...]


def load_mapping(path: Path = DEFAULT_MAPPING_PATH) -> dict[str, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"mapping file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"mapping file is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in data.items()):
        raise ValueError("mapping must be a JSON object of string pairs")
    return {key.strip(): value.strip() for key, value in data.items() if key.strip()}


def match_case(source: str, replacement: str) -> str:
    if source.isupper():
        return replacement.upper()
    if source[:1].isupper() and source[1:].islower():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def normalize(text: str, mapping: dict[str, str] | None = None) -> NormalizationResult:
    """Replace only explicitly mapped standalone words/phrases.

    The function intentionally does not guess punctuation or grammar and does
    not lowercase the input. This avoids damaging names and valid sentences.
    """

    source_mapping = mapping if mapping is not None else load_mapping()
    mapping = {key.casefold(): value for key, value in source_mapping.items()}
    if not text:
        return NormalizationResult("", ())
    if not mapping:
        return NormalizationResult(text, ())

    keys = sorted(mapping, key=len, reverse=True)
    pattern = re.compile(
        r"(?<!\w)(" + "|".join(re.escape(key) for key in keys) + r")(?!\w)",
        flags=re.IGNORECASE,
    )
    replacements: list[Replacement] = []

    def replace(match: re.Match[str]) -> str:
        original = match.group(0)
        replacement = match_case(original, mapping[original.casefold()])
        replacements.append(Replacement(original, replacement, match.start(), match.end()))
        return replacement

    normalized = pattern.sub(replace, text)
    return NormalizationResult(normalized, tuple(replacements))

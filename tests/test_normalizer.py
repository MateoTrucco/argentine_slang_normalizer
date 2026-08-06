import json

import pytest

from normalizer import load_mapping, normalize


def test_preserves_names_and_valid_punctuation():
    result = normalize("Hola Mateo. Juan y María fueron, pero volvieron.", {"toy": "estoy"})
    assert result.text == "Hola Mateo. Juan y María fueron, pero volvieron."


def test_replaces_only_standalone_terms():
    result = normalize("toy en el laburo; estoy bien", {"toy": "estoy", "laburo": "trabajo"})
    assert result.text == "estoy en el trabajo; estoy bien"
    assert len(result.replacements) == 2


def test_long_phrases_have_priority():
    result = normalize("yo q se", {"q": "que", "yo q se": "yo qué sé"})
    assert result.text == "yo qué sé"


def test_case_is_preserved():
    assert normalize("TOY", {"toy": "estoy"}).text == "ESTOY"
    assert normalize("Toy", {"toy": "estoy"}).text == "Estoy"


def test_invalid_json_is_reported(tmp_path):
    path = tmp_path / "mapping.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError, match="valid JSON"):
        load_mapping(path)


def test_custom_mapping_is_case_insensitive_and_empty_mapping_is_respected():
    assert normalize("TOY", {"TOY": "estoy"}).text == "ESTOY"
    assert normalize("toy", {}).text == "toy"


def test_unrelated_whitespace_is_preserved():
    assert normalize("Hola   mundo !", {"toy": "estoy"}).text == "Hola   mundo !"

def test_empty_mapping_leaves_text_unchanged():
    result = normalize("Text stays exactly the same.", {})
    assert result.text == "Text stays exactly the same."
    assert result.replacements == ()


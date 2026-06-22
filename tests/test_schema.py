"""
Tests for cor_proof.schema — schema loading and self-validation.
"""

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from cor_proof.schema import load_schema


class TestLoadSchema:
    def test_returns_dict(self):
        schema = load_schema()
        assert isinstance(schema, dict)

    def test_has_required_json_schema_fields(self):
        schema = load_schema()
        assert "$schema" in schema
        assert "title" in schema
        assert "type" in schema
        assert "required" in schema

    def test_schema_id_present(self):
        schema = load_schema()
        assert "$id" in schema

    def test_schema_version_is_2020_12(self):
        schema = load_schema()
        assert "2020-12" in schema["$schema"]

    def test_required_fields_list(self):
        schema = load_schema()
        required = schema["required"]
        expected = {
            "cor_version", "level", "id", "created_utc",
            "language", "generator", "claim", "evidence",
            "reasoning_atoms", "validation", "metadata"
        }
        assert expected.issubset(set(required))

    def test_schema_is_cached(self):
        """load_schema() should return the same object on repeated calls (lru_cache)."""
        schema_a = load_schema()
        schema_b = load_schema()
        assert schema_a is schema_b

    def test_schema_self_validates(self):
        """
        The bundled schema must itself be a valid JSON Schema (draft 2020-12).
        This is Nova's acceptance criterion: Draft202012Validator.check_schema(load_schema()).
        """
        schema = load_schema()
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            pytest.fail(f"Bundled schema failed self-validation: {exc}")

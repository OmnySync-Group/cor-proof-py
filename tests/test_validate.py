"""
Tests for cor_proof.validate — L1 structural validation.
"""

import json
from pathlib import Path

import pytest

from cor_proof.validate import ValidationResult, validate

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def _load_example(relative_path: str) -> dict:
    return json.loads((EXAMPLES_DIR / relative_path).read_text(encoding="utf-8"))


MINIMAL_VALID = {
    "cor_version": "1.0.1",
    "level": 1,
    "id": "test-minimal-valid",
    "created_utc": "2026-01-15T12:00:00Z",
    "language": "en",
    "generator": {
        "actor_type": "human",
        "name": "test",
        "version": "1.0"
    },
    "claim": {
        "id": "c1",
        "text": "The sky appears blue under normal atmospheric conditions.",
        "type": "factual"
    },
    "evidence": [
        {
            "id": "e1",
            "type": "observation",
            "description": "Direct observation of sky color during daylight hours."
        }
    ],
    "reasoning_atoms": [
        {
            "id": "ra-001",
            "step_index": 1,
            "statement": "Observation of blue sky supports the claim.",
            "inference_type": "induction",
            "inputs": ["e1"],
            "outputs": ["c1"]
        }
    ],
    "validation": {
        "overall_status": "validated",
        "validators": [
            {
                "id": "test-validator",
                "actor_type": "human",
                "verdict": "pass"
            }
        ]
    },
    "metadata": {}
}


# ---------------------------------------------------------------------------
# ValidationResult dataclass
# ---------------------------------------------------------------------------

class TestValidationResult:
    def test_valid_str(self):
        r = ValidationResult(valid=True, artifact_id="test-id")
        assert "VALID" in str(r)
        assert "test-id" in str(r)

    def test_invalid_str_includes_errors(self):
        r = ValidationResult(valid=False, errors=["field X missing", "field Y wrong"], artifact_id="bad-id")
        s = str(r)
        assert "INVALID" in s
        assert "field X missing" in s
        assert "field Y wrong" in s

    def test_defaults(self):
        r = ValidationResult(valid=True)
        assert r.errors == []
        assert r.artifact_id is None


# ---------------------------------------------------------------------------
# validate() — dict input
# ---------------------------------------------------------------------------

class TestValidateDict:
    def test_minimal_valid_artifact(self):
        result = validate(MINIMAL_VALID)
        assert result.valid is True
        assert result.errors == []
        assert result.artifact_id == "test-minimal-valid"

    def test_missing_top_level_required_fields(self):
        artifact = {"cor_version": "1.0.1", "level": 1}
        result = validate(artifact)
        assert result.valid is False
        assert len(result.errors) > 0

    def test_empty_evidence_array(self):
        artifact = {**MINIMAL_VALID, "id": "test-empty-evidence", "evidence": []}
        result = validate(artifact)
        assert result.valid is False
        error_text = " ".join(result.errors)
        assert "evidence" in error_text.lower() or len(result.errors) > 0

    def test_empty_reasoning_atoms(self):
        artifact = {**MINIMAL_VALID, "id": "test-empty-atoms", "reasoning_atoms": []}
        result = validate(artifact)
        assert result.valid is False

    def test_invalid_level_value(self):
        artifact = {**MINIMAL_VALID, "id": "test-bad-level", "level": 99}
        result = validate(artifact)
        assert result.valid is False

    def test_invalid_actor_type_enum(self):
        artifact = json.loads(json.dumps(MINIMAL_VALID))
        artifact["id"] = "test-bad-actor"
        artifact["generator"]["actor_type"] = "robot"
        result = validate(artifact)
        assert result.valid is False

    def test_invalid_claim_type_enum(self):
        artifact = json.loads(json.dumps(MINIMAL_VALID))
        artifact["id"] = "test-bad-claim-type"
        artifact["claim"]["type"] = "speculation"
        result = validate(artifact)
        assert result.valid is False

    def test_invalid_validation_status_enum(self):
        artifact = json.loads(json.dumps(MINIMAL_VALID))
        artifact["id"] = "test-bad-status"
        artifact["validation"]["overall_status"] = "unknown"
        result = validate(artifact)
        assert result.valid is False

    def test_missing_generator_required_field(self):
        artifact = json.loads(json.dumps(MINIMAL_VALID))
        artifact["id"] = "test-bad-generator"
        del artifact["generator"]["name"]
        result = validate(artifact)
        assert result.valid is False

    def test_artifact_id_extracted(self):
        result = validate(MINIMAL_VALID)
        assert result.artifact_id == "test-minimal-valid"

    def test_list_input_raises_type_error(self):
        """A list input should raise TypeError — not a supported artifact type."""
        with pytest.raises(TypeError, match="Unsupported artifact type"):
            validate([1, 2, 3])


# ---------------------------------------------------------------------------
# validate() — file path input
# ---------------------------------------------------------------------------

class TestValidateFilePath:
    def test_valid_example_file_as_path(self):
        path = EXAMPLES_DIR / "valid" / "l1_basic_claim.json"
        result = validate(path)
        assert result.valid is True

    def test_invalid_example_missing_fields_as_path(self):
        path = EXAMPLES_DIR / "invalid" / "l1_missing_required_fields.json"
        result = validate(path)
        assert result.valid is False
        assert len(result.errors) > 0

    def test_invalid_example_empty_evidence_as_path(self):
        path = EXAMPLES_DIR / "invalid" / "l1_empty_evidence.json"
        result = validate(path)
        assert result.valid is False

    def test_valid_example_file_as_string_path(self):
        path_str = str(EXAMPLES_DIR / "valid" / "l1_basic_claim.json")
        result = validate(path_str)
        assert result.valid is True

    def test_nonexistent_file_raises_value_error(self):
        with pytest.raises(ValueError, match="Cannot read file"):
            validate(Path("/nonexistent/path/artifact.json"))

    def test_malformed_json_string_raises_value_error(self):
        with pytest.raises(ValueError, match="not valid JSON"):
            validate("{ this is not json }")


# ---------------------------------------------------------------------------
# validate() — type handling
# ---------------------------------------------------------------------------

class TestValidateTypeHandling:
    def test_unsupported_type_raises_type_error(self):
        with pytest.raises(TypeError, match="Unsupported artifact type"):
            validate(12345)  # type: ignore[arg-type]

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError):
            validate(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# L1-only enforcement (Remediation 2 — Nova review item)
# ---------------------------------------------------------------------------

class TestL1OnlyEnforcement:
    def test_level_2_artifact_is_rejected(self):
        """Level 2 artifacts must be rejected by this package."""
        artifact = {**MINIMAL_VALID, "id": "test-level-2", "level": 2}
        result = validate(artifact)
        assert result.valid is False
        assert any("level 2" in e.lower() or "level" in e.lower() for e in result.errors)

    def test_level_3_artifact_is_rejected(self):
        """Level 3 artifacts must be rejected by this package."""
        artifact = {**MINIMAL_VALID, "id": "test-level-3", "level": 3}
        result = validate(artifact)
        assert result.valid is False
        assert any("level 3" in e.lower() or "level" in e.lower() for e in result.errors)

    def test_level_1_artifact_is_accepted(self):
        """Level 1 artifacts must still pass."""
        result = validate(MINIMAL_VALID)
        assert result.valid is True

    def test_rejection_error_message_is_informative(self):
        """Rejection message should mention the declared level and scope boundary."""
        artifact = {**MINIMAL_VALID, "id": "test-level-2-msg", "level": 2}
        result = validate(artifact)
        assert result.valid is False
        error_text = " ".join(result.errors)
        assert "2" in error_text  # declared level mentioned
        assert "1" in error_text  # supported level mentioned

"""
COR Proof L1 structural validator.

Validates a COR Proof artifact against the bundled JSON Schema (draft 2020-12)
AND enforces that the artifact is Level 1 only.

This module performs structural validation only. It does not:
- Verify truth or factual accuracy of claims
- Assess reasoning quality or coherence
- Evaluate evidence reliability
- Perform semantic or logical analysis
- Make compliance, safety, or model quality determinations

Level 2, 3, and 4 validation are outside the scope of this package.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from cor_proof.schema import load_schema

# This package enforces L1-only. Artifacts declaring a higher level are rejected.
_SUPPORTED_LEVEL = 1


@dataclass
class ValidationResult:
    """
    Result of a COR Proof L1 structural validation run.

    Attributes:
        valid:       True if the artifact conforms to the COR Proof L1 schema
                     AND declares level == 1.
        errors:      List of human-readable error messages (empty when valid).
        artifact_id: The `id` field from the artifact, if parseable.
    """
    valid: bool
    errors: list[str] = field(default_factory=list)
    artifact_id: str | None = None

    def __str__(self) -> str:
        if self.valid:
            return f"VALID — COR Proof L1 structural validation passed (id: {self.artifact_id})"
        lines = [f"INVALID — COR Proof L1 structural validation failed (id: {self.artifact_id})"]
        for i, err in enumerate(self.errors, 1):
            lines.append(f"  [{i}] {err}")
        return "\n".join(lines)


def validate(artifact: "dict[str, Any] | str | Path") -> ValidationResult:
    """
    Validate a COR Proof artifact against the L1 schema.

    This function validates structure AND enforces level == 1.
    Artifacts declaring level 2, 3, or higher are rejected by this package.
    Higher-level validation is outside scope.

    Accepts:
        - A dict (already-parsed artifact)
        - A JSON string
        - A Path or str path to a JSON file

    Returns:
        ValidationResult with valid=True and empty errors on success,
        or valid=False with a list of error messages on failure.

    Raises:
        TypeError:    If the input type is not supported.
        ValueError:   If a string/file cannot be parsed as JSON.
        RuntimeError: If the bundled schema itself is malformed.
    """
    parsed = _load_artifact(artifact)
    artifact_id = parsed.get("id") if isinstance(parsed, dict) else None

    schema = load_schema()

    # Guard: confirm bundled schema is valid (defense in depth)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise RuntimeError(
            f"Bundled COR Proof schema is invalid — packaging defect: {exc}"
        ) from exc

    # L1 enforcement: reject artifacts that declare a level other than 1.
    # This check runs before schema validation so the error message is clear.
    if isinstance(parsed, dict):
        declared_level = parsed.get("level")
        if declared_level is not None and declared_level != _SUPPORTED_LEVEL:
            return ValidationResult(
                valid=False,
                errors=[
                    f"(root): this package validates COR Proof Level 1 only. "
                    f"Artifact declares level {declared_level}. "
                    f"Level {declared_level} validation is outside the scope of cor-proof-py v0.1.x."
                ],
                artifact_id=artifact_id,
            )

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(parsed), key=lambda e: list(e.path))

    if not errors:
        return ValidationResult(valid=True, artifact_id=artifact_id)

    error_messages = [_format_error(e) for e in errors]
    return ValidationResult(valid=False, errors=error_messages, artifact_id=artifact_id)


def _load_artifact(artifact: Any) -> Any:
    if isinstance(artifact, dict):
        return artifact
    if isinstance(artifact, Path):
        try:
            text = artifact.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"Cannot read file '{artifact}': {exc}") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"File '{artifact}' is not valid JSON: {exc}") from exc
    if isinstance(artifact, str):
        path = Path(artifact)
        if path.exists():
            return _load_artifact(path)
        try:
            return json.loads(artifact)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Input is not valid JSON and not a readable path: {exc}") from exc
    raise TypeError(
        f"Unsupported artifact type '{type(artifact).__name__}'. "
        "Expected dict, str (JSON or file path), or pathlib.Path."
    )


def _format_error(error: ValidationError) -> str:
    path = " → ".join(str(p) for p in error.absolute_path) if error.absolute_path else "(root)"
    return f"{path}: {error.message}"

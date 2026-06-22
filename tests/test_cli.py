"""
Tests for cor_proof.cli — command-line interface.
"""

import json
from pathlib import Path

from click.testing import CliRunner

from cor_proof.cli import cli
import cor_proof

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


class TestCLIVersion:
    def test_version_flag(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert cor_proof.__version__ in result.output


class TestCLIValidate:
    def test_valid_file_exits_0(self):
        runner = CliRunner()
        path = str(EXAMPLES_DIR / "valid" / "l1_basic_claim.json")
        result = runner.invoke(cli, ["validate", path])
        assert result.exit_code == 0
        assert "VALID" in result.output

    def test_invalid_missing_fields_exits_1(self):
        runner = CliRunner()
        path = str(EXAMPLES_DIR / "invalid" / "l1_missing_required_fields.json")
        result = runner.invoke(cli, ["validate", path])
        assert result.exit_code == 1
        assert "INVALID" in result.output

    def test_invalid_empty_evidence_exits_1(self):
        runner = CliRunner()
        path = str(EXAMPLES_DIR / "invalid" / "l1_empty_evidence.json")
        result = runner.invoke(cli, ["validate", path])
        assert result.exit_code == 1

    def test_valid_file_json_output(self):
        runner = CliRunner()
        path = str(EXAMPLES_DIR / "valid" / "l1_basic_claim.json")
        result = runner.invoke(cli, ["validate", path, "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.output)
        assert payload["valid"] is True
        assert payload["errors"] == []
        assert payload["artifact_id"] is not None

    def test_invalid_file_json_output(self):
        runner = CliRunner()
        path = str(EXAMPLES_DIR / "invalid" / "l1_missing_required_fields.json")
        result = runner.invoke(cli, ["validate", path, "--json"])
        assert result.exit_code == 1
        payload = json.loads(result.output)
        assert payload["valid"] is False
        assert len(payload["errors"]) > 0

    def test_help_text_present(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", "--help"])
        assert result.exit_code == 0
        assert "FILE" in result.output
        assert "--json" in result.output


class TestCLISchema:
    def test_schema_command_exits_0(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["schema"])
        assert result.exit_code == 0

    def test_schema_command_outputs_valid_json(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["schema"])
        assert result.exit_code == 0
        parsed = json.loads(result.output)
        assert "$schema" in parsed
        assert "2020-12" in parsed["$schema"]

    def test_schema_json_flag_is_compact(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["schema", "--json"])
        assert result.exit_code == 0
        # Compact output: no leading whitespace on second char means single line
        assert "\n" not in result.output.strip()

    def test_schema_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["schema", "--help"])
        assert result.exit_code == 0


class TestCLIL1Enforcement:
    def test_level_2_artifact_exits_1(self, tmp_path):
        runner = CliRunner()
        artifact = {
            "cor_version": "1.0.1", "level": 2, "id": "cli-level-2-test",
            "created_utc": "2026-01-01T00:00:00Z", "language": "en",
            "generator": {"actor_type": "human", "name": "test", "version": "1.0"},
            "claim": {"id": "c1", "text": "Test.", "type": "factual"},
            "evidence": [{"id": "e1", "type": "observation", "description": "Test."}],
            "reasoning_atoms": [{"id": "ra-001", "step_index": 1, "statement": "Test.",
                                  "inference_type": "induction", "inputs": ["e1"], "outputs": ["c1"]}],
            "validation": {"overall_status": "unvalidated", "validators": []},
            "metadata": {}
        }
        f = tmp_path / "level2.json"
        f.write_text(json.dumps(artifact))
        result = runner.invoke(cli, ["validate", str(f)])
        assert result.exit_code == 1
        assert "INVALID" in result.output

"""
COR Proof command-line interface.

Commands:
    cor-proof validate <file> [--json]   Validate a COR Proof L1 artifact
    cor-proof schema [--json]            Print the bundled L1 JSON Schema
    cor-proof --version

Exit codes (validate command):
    0 — Artifact is structurally valid
    1 — Artifact is structurally invalid
    2 — Runtime error (file not found, parse failure, etc.)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click

import cor_proof
from cor_proof.schema import load_schema
from cor_proof.validate import validate


@click.group()
@click.version_option(version=cor_proof.__version__, prog_name="cor-proof")
def cli() -> None:
    """
    COR Proof — Chain-of-Reasoning Proof

    Structural validation for COR Proof L1 artifacts.

    This tool validates structure only. It does not verify truth,
    factual accuracy, safety, compliance, or model quality.
    """


@cli.command("validate")
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    default=False,
    help="Emit machine-readable JSON output instead of human-readable text.",
)
def validate_command(file: Path, output_json: bool) -> None:
    """
    Validate a COR Proof L1 artifact FILE against the schema.

    FILE must be a path to a JSON file containing a COR Proof artifact.

    \b
    Exit codes:
      0  Valid — artifact conforms to the COR Proof L1 schema
      1  Invalid — artifact violates the schema or declares level != 1
      2  Error — file could not be read or parsed
    """
    try:
        result = validate(file)
    except (ValueError, RuntimeError) as exc:
        if output_json:
            click.echo(
                json.dumps({"valid": False, "error": str(exc), "artifact_id": None}, indent=2)
            )
        else:
            click.echo(f"ERROR: {exc}", err=True)
        sys.exit(2)

    if output_json:
        payload: dict = {
            "valid": result.valid,
            "artifact_id": result.artifact_id,
            "errors": result.errors,
        }
        click.echo(json.dumps(payload, indent=2))
    else:
        click.echo(str(result))

    sys.exit(0 if result.valid else 1)


@cli.command("schema")
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    default=False,
    help="Emit the schema as compact JSON (default is pretty-printed).",
)
def schema_command(output_json: bool) -> None:
    """
    Print the bundled COR Proof L1 JSON Schema.

    Outputs the normative schema document this package validates against.
    Useful for integrating COR Proof L1 validation into other tools.
    """
    try:
        schema = load_schema()
    except RuntimeError as exc:
        click.echo(f"ERROR: {exc}", err=True)
        sys.exit(2)

    if output_json:
        click.echo(json.dumps(schema))
    else:
        click.echo(json.dumps(schema, indent=2))


def main() -> None:
    """Entry point registered in pyproject.toml."""
    cli()

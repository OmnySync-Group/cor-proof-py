"""
COR Proof schema subpackage.

The bundled cor-proof.schema.json lives alongside this file.
Use cor_proof.load_schema() or cor_proof._schema_loader.load_schema()
to access the parsed schema.
"""

import importlib.resources as pkg_resources
import json
from functools import lru_cache
from typing import Any

_SCHEMA_FILE = "cor-proof.schema.json"


@lru_cache(maxsize=1)
def load_schema() -> dict[str, Any]:
    """
    Load and return the bundled COR Proof L1 JSON Schema.

    Cached after first load. Returns the parsed JSON Schema (draft 2020-12).

    Raises:
        RuntimeError: If the bundled schema file cannot be located or parsed.
    """
    try:
        ref = pkg_resources.files(__name__).joinpath(_SCHEMA_FILE)
        schema_text = ref.read_text(encoding="utf-8")
        return json.loads(schema_text)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to load bundled COR Proof schema '{_SCHEMA_FILE}': {exc}"
        ) from exc

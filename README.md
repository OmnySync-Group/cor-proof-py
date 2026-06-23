# COR Proof — Python Validator

[![PyPI](https://img.shields.io/pypi/v/cor-proof.svg)](https://pypi.org/project/cor-proof/)
[![Python](https://img.shields.io/pypi/pyversions/cor-proof.svg)](https://pypi.org/project/cor-proof/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE.md)

**COR Proof (Chain-of-Reasoning Proof)** is an open standard for capturing, validating,
and auditing reasoning structure in AI and human–AI systems.

This package provides the Python reference implementation for **Level 1 (L1) structural validation**.

**COR Proof L1 is a schema-enforced audit gate for AI reasoning artifacts. It validates structure, not truth.**

---

> **COR Proof L1 validates structure.**
> It does not verify truth, factual accuracy, safety, compliance, or model quality.

---

## What COR Proof L1 Does

COR Proof L1 defines a machine-verifiable format for representing:

- A single, falsifiable claim
- Declared evidence bound explicitly to the claim
- Reasoning atoms with traceable inputs and outputs
- Explicit assumptions that can be challenged independently
- A validation record

A schema-based validator can check structural compliance without reading the content.
This is the difference between an informal explanation of reasoning and a structured,
independently auditable artifact.

## What COR Proof L1 Does Not Do

- Determine whether a claim is true
- Assess reasoning quality, coherence, or validity
- Evaluate evidence reliability or credibility
- Perform logical, semantic, or factual analysis
- Make safety, compliance, or model quality determinations
- Validate Level 2, 3, or 4 artifacts (higher-level validation is outside scope)

---

## Installation

```bash
pip install cor-proof
```

Requires Python 3.9 or later.

---

## Quick Start

### Validate a file

```bash
cor-proof validate path/to/artifact.json
```

Exit codes: `0` valid · `1` invalid · `2` runtime error

### Machine-readable output

```bash
cor-proof validate path/to/artifact.json --json
```

### Print the bundled schema

```bash
cor-proof schema
cor-proof schema --json   # compact single-line JSON
```

### Python API

```python
from cor_proof import validate

result = validate("path/to/artifact.json")
print(result)        # human-readable summary
print(result.valid)  # True or False
print(result.errors) # list of error strings if invalid
```

```python
from cor_proof import load_schema

schema = load_schema()
# Returns the COR Proof JSON Schema (draft 2020-12) as a dict
```

---

## Creating a test artifact

After `pip install cor-proof`, create a minimal artifact to validate:

```json
{
  "cor_version": "1.0.1",
  "level": 1,
  "id": "my-first-artifact",
  "created_utc": "2026-01-01T00:00:00Z",
  "language": "en",
  "generator": { "actor_type": "human", "name": "me", "version": "1.0" },
  "claim": { "id": "c1", "text": "My claim.", "type": "factual" },
  "evidence": [{ "id": "e1", "type": "observation", "description": "My evidence." }],
  "reasoning_atoms": [{
    "id": "ra-001", "step_index": 1,
    "statement": "Evidence supports claim.",
    "inference_type": "induction",
    "inputs": ["e1"], "outputs": ["c1"]
  }],
  "validation": {
    "overall_status": "unvalidated",
    "validators": []
  },
  "metadata": {}
}
```

Save as `artifact.json` and run:

```bash
cor-proof validate artifact.json
```

---

## Reference examples

The **repository** includes reference examples under `examples/`:

```
examples/
  valid/
    l1_basic_claim.json                 — minimal valid artifact
  invalid/
    l1_missing_required_fields.json     — missing top-level required fields
    l1_empty_evidence.json              — empty evidence array (minItems: 1)
```

Clone the repository to access them:

```bash
git clone https://github.com/OmnySync-Group/cor-proof-py.git
cd cor-proof-py
cor-proof validate examples/valid/l1_basic_claim.json
```

---

## Specification & Schema

- **Open spec and schema:** [github.com/OmnySync-Group/cor-proof](https://github.com/OmnySync-Group/cor-proof)
- **This Python package:** [github.com/OmnySync-Group/cor-proof-py](https://github.com/OmnySync-Group/cor-proof-py)
- **Issues:** [github.com/OmnySync-Group/cor-proof-py/issues](https://github.com/OmnySync-Group/cor-proof-py/issues)

---

## License

Apache 2.0 — see [LICENSE.md](LICENSE.md)

Maintained by **OmnySync Group LLC** as part of the [Stake The Truth](https://github.com/OmnySync-Group/cor-proof) initiative.

Contact: founder@omnysyncai.com

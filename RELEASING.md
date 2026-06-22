# Releasing cor-proof

Releases of `cor-proof` are managed by OmnySync Group LLC as part of the
Stake The Truth initiative.

## Release Channels

| Channel | Status | Install |
|---|---|---|
| TestPyPI | Alpha | `pip install --index-url https://test.pypi.org/simple/ cor-proof` |
| PyPI | Pending | `pip install cor-proof` |
| GitHub | Live | Clone or download from this repo |

## For Contributors

If you have found a bug, have a feature request, or want to contribute:

- Open an issue: https://github.com/OmnySync-Group/cor-proof-py/issues
- Review the specification: https://github.com/OmnySync-Group/cor-proof

All contributions must remain scoped to COR Proof Level 1 structural
validation. Higher-level validation (L2/L3/L4) is outside the scope
of this package.

## Build and Test (Local)

```bash
pip install -e ".[dev]"
python -m pytest
python -m build
python -m twine check dist/*
```

## Release Authority

Releases to TestPyPI and PyPI require explicit authorization from the
OmnySync Group LLC maintainer. Automated publishing is intentionally
absent from the CI workflow.

To inquire about release timing or enterprise licensing:
founder@omnysyncai.com

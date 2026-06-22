# COR Proof Python Package — Claude Code Project Instructions

## Run ID
ALYTOS-TC-COR-PYPI-001

## What This Project Is
cor-proof-py is the Python reference validator for COR Proof Level 1 (L1),
the Universal Structure Layer of the COR Proof open standard.

Spec repo: https://github.com/OmnySync-Group/cor-proof
This repo:  https://github.com/OmnySync-Group/cor-proof-py

## Hard Scope
This package contains ONLY:
- L1 schema loader (importlib.resources, bundled schema)
- L1 structural validator (jsonschema Draft202012Validator)
- CLI: `cor-proof validate <file> [--json]`
- Tests
- Examples (neutral domain only)
- Build and CI configuration

## Hard Rules — Do Not Violate
1. NEVER run `git commit`
2. NEVER run `git push`
3. NEVER run `git checkout main`
4. NEVER delete any existing file
5. NEVER modify `src/cor_proof/schema/cor-proof.schema.json`
6. NEVER run any publish, deploy, upload, or release commands
7. NEVER add dependencies beyond: jsonschema>=4.18,<5 and click>=8.1,<9
8. NEVER include Alytos, GDG, L2/L3/L4, Keeper, telemetry, or governance internals
9. NEVER include medical, legal, defense, or finance examples
10. NEVER make claims that COR Proof determines truth, safety, compliance, or model quality

## If You Hit Scope Ambiguity
Stop immediately. Surface the ambiguity in your response.
Do not proceed beyond the L1 validator without explicit Keeper instruction.

## Authorized External Dependencies (runtime)
- jsonschema>=4.18,<5
- click>=8.1,<9

## Authorized Dev Dependencies
- pytest>=7.0
- pytest-cov
- build
- twine

## What Success Looks Like
When the session ends, `git diff` and `git status` show new or modified files.
The Keeper reviews all output before deciding what to commit or push.

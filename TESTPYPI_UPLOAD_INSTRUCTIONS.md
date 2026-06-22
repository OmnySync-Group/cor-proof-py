# TestPyPI Upload Instructions
# [DRAFT — KEEPER REVIEW REQUIRED]
#
# Run ID: ALYTOS-TC-COR-PYPI-001
# UPLOAD IS NOT AUTHORIZED until separate Keeper release authorization is granted.

---

## Prerequisites (complete before upload)

- [ ] All tests pass locally: `pytest`
- [ ] Build succeeds: `python -m build`
- [ ] Twine check passes: `twine check dist/*`
- [ ] Keeper has reviewed and approved the PR
- [ ] Separate Keeper Release Authorization has been issued for TestPyPI

---

## Step 1 — Create TestPyPI account

Register at: https://test.pypi.org/account/register/

Create an API token at: https://test.pypi.org/manage/account/token/
Scope: "Entire account" for the first upload; restrict to cor-proof project afterward.

---

## Step 2 — Build the distribution

```bash
python -m build
```

Produces:
```
dist/
  cor_proof-0.1.0-py3-none-any.whl
  cor_proof-0.1.0.tar.gz
```

---

## Step 3 — Verify with twine

```bash
twine check dist/*
```

Both artifacts must pass.

---

## Step 4 — Upload to TestPyPI (KEEPER ACTION — manual only)

```bash
twine upload --repository testpypi dist/*
```

Username: `__token__`
Password: your TestPyPI API token

---

## Step 5 — Verify the TestPyPI listing

Visit: https://test.pypi.org/project/cor-proof/

Confirm:
- [ ] Package name: cor-proof
- [ ] Version: 0.1.0
- [ ] Description renders correctly
- [ ] License shown as Apache 2.0
- [ ] URLs link to correct repos

---

## Step 6 — Test install from TestPyPI (fresh environment)

```bash
python -m venv test-install-env
test-install-env\Scripts\activate        # Windows
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            cor-proof
cor-proof --version
cor-proof schema
```

To validate an artifact after fresh install, create a minimal test file:

```bash
# Create a minimal valid artifact for install verification
echo '{"cor_version":"1.0.1","level":1,"id":"install-test","created_utc":"2026-01-01T00:00:00Z","language":"en","generator":{"actor_type":"human","name":"test","version":"1.0"},"claim":{"id":"c1","text":"Install test.","type":"factual"},"evidence":[{"id":"e1","type":"observation","description":"Test evidence."}],"reasoning_atoms":[{"id":"ra-001","step_index":1,"statement":"Test.","inference_type":"induction","inputs":["e1"],"outputs":["c1"]}],"validation":{"overall_status":"unvalidated","validators":[]},"metadata":{}}' > install-test.json
cor-proof validate install-test.json
```

Expected: exit 0, VALID output.

NOTE: The `examples/` directory is in the repository, not the installed package.
Clone the repo separately if you need the reference examples.

---

## Step 7 — Log in Alpha Run Register

Record:
- Run ID: ALYTOS-TC-COR-PYPI-001
- Artifact SHA-256 (of .whl)
- TestPyPI URL
- Test install result
- Keeper sign-off

---

## Live PyPI

Live PyPI requires a SEPARATE Keeper-signed Release Contract.
This document does not authorize live PyPI publication.

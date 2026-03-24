# RELEASE_PROCESS.md

SSRF COMMAND CONSOLE — RELEASE PROCESS
Operator‑Grade, Repeatable, Auditable Release Workflow

---

## 1. PURPOSE OF THIS DOCUMENT

This document defines the official, repeatable, auditable release process for the SSRF Command Console.
It ensures that every release is:

- Consistent
- Verified
- Secure
- Backward‑compatible (when applicable)
- Fully documented

This process applies to all maintainers and contributors participating in versioned releases.

---

## 2. VERSIONING MODEL

### 2.1 Semantic Versioning (SemVer)

The project uses Semantic Versioning:
MAJOR.MINOR.PATCH

- **MAJOR** — breaking changes, incompatible API updates
- **MINOR** — new features, non‑breaking enhancements
- **PATCH** — bug fixes, documentation updates, internal improvements

### 2.2 Pre‑Release Tags

Optional tags:

alpha beta rc

Examples:

1.4.0-alpha.1 1.4.0-rc.2

---

## 3. RELEASE BRANCHING MODEL

### 3.1 Main Branch

- Always stable
- Always deployable
- Only receives PRs that pass all checks

### 3.2 Development Branch

- Optional
- Used for staging features before merging into main

### 3.3 Release Branches

Created only when preparing a release:

release/vX.Y.Z

Used for:

- Final testing
- Documentation updates
- Version bump
- Changelog finalization

---

## 4. RELEASE CHECKLIST (MANDATORY)

### 4.1 Code Quality

- [ ] All tests pass
- [ ] Linting passes
- [ ] Type checks pass
- [ ] No debug prints or temporary code

### 4.2 Documentation

- [ ] CHANGELOG.md updated
- [ ] VERSION file updated (if applicable)
- [ ] API_REFERENCE.md validated
- [ ] MODE_CATALOG.md updated if new modes added
- [ ] OPERATOR_GUIDE.md updated if UI changed
- [ ] SECURITY_MODEL.md updated if threat boundaries changed

### 4.3 Security

- [ ] Dependencies scanned
- [ ] No known CVEs in critical libraries
- [ ] No accidental exposure of secrets
- [ ] SSRF filters tested in safe mode

### 4.4 Functional Validation

- [ ] Console loads without errors
- [ ] All scanning modes operate correctly
- [ ] Dashboard renders correctly
- [ ] History panel and diff viewer work
- [ ] API endpoints respond as expected

### 4.5 Packaging

- [ ] Build artifacts generated
- [ ] Build artifacts tested locally
- [ ] Build artifacts signed (if applicable)

---

## 5. RELEASE STEPS (END‑TO‑END)

### 5.1 Create a Release Branch

git checkout -b release/vX.Y.Z

### 5.2 Update Version Metadata

Update:

- pyproject.toml or setup.cfg
- VERSION file (if used)
- Any embedded version strings

### 5.3 Finalize CHANGELOG.md

Sections:

- Added
- Changed
- Fixed
- Removed
- Security

### 5.4 Run Full Test Suite

pytest -q

### 5.5 Run Static Analysis

ruff check . mypy .

### 5.6 Build Release Artifacts

python -m build

### 5.7 Validate Artifacts

Install locally:

pip install dist/ssrf_console-X.Y.Z-py3-none-any.whl

Smoke test:

- Start backend
- Load console
- Run each mode
- Validate UI

### 5.8 Tag the Release

git tag -a vX.Y.Z -m "Release vX.Y.Z" git push origin vX.Y.Z

### 5.9 Merge Release Branch Into Main

git checkout main git merge --no-ff release/vX.Y.Z git push origin main

### 5.10 Publish Release Notes

Include:

- Summary
- Highlights
- Breaking changes
- Upgrade instructions
- Security notes

---

## 6. POST‑RELEASE TASKS

### 6.1 Update Documentation Index

Ensure DOCS_INDEX.md reflects new or updated files.

### 6.2 Announce Release

Channels:

- Internal teams
- GitHub Releases
- Documentation site

### 6.3 Create Next Development Cycle Branch (Optional)

git checkout -b develop

---

## 7. HOTFIX PROCESS

### 7.1 When to Use

- Critical bug
- Security issue
- Regression in production

### 7.2 Steps

1. Branch from main: git checkout -b hotfix/vX.Y.Z+1
2. Apply fix
3. Update CHANGELOG.md
4. Bump PATCH version
5. Test
6. Tag and release
7. Merge back into main

---

## 8. RELEASE VALIDATION MATRIX

| Area              | Required | Notes                          |
| ----------------- | -------- | ------------------------------ |
| Unit Tests        | Yes      | Must pass 100%                 |
| Integration Tests | Yes      | All modes tested               |
| UI Validation     | Yes      | Dashboard + history            |
| Security Scan     | Yes      | Dependencies + SSRF filters    |
| Documentation     | Yes      | All updated                    |
| Performance Check | Optional | Recommended for major releases |
| Load Testing      | Optional | For enterprise deployments     |

---

## 9. AUTOMATION ROADMAP (FUTURE)

Planned automation includes:

- GitHub Actions release pipeline
- Automated changelog generation
- Automated artifact signing
- Automated mode validation suite
- Automated SSRF filter regression tests

---

## 10. APPENDIX — ESCAPED FENCING EXAMPLES

### 10.1 Escaped Code Block

```markdown
bash git tag -a V1.2.3

## 10.2 Escaped JSON

json {"version": "1.2.3"}
```

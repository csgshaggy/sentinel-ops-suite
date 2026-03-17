# Contributing Guide

## Overview
Thank you for your interest in contributing to the SSRF Command Console.  
This guide defines the standards, workflows, and expectations for all contributions to ensure consistency, safety, and deterministic behavior across the project.

---

# 1. Code of Conduct

Contributors must:

- Communicate respectfully  
- Provide constructive feedback  
- Document changes clearly  
- Follow established workflows  
- Prioritize security and determinism  

---

# 2. Branching Strategy

\`\`\`
main        → stable
develop     → active development
feature/*   → new features
bugfix/*    → fixes
docs/*      → documentation
\`\`\`

### Rules

- Never commit directly to `main`  
- All work must go through pull requests  
- Branch names must be descriptive  

---

# 3. Commit Conventions

Use **Conventional Commits**:

\`\`\`
<type>(scope): description
\`\`\`

### Allowed Types

- **feat** — new feature  
- **fix** — bug fix  
- **docs** — documentation changes  
- **refactor** — code restructuring  
- **test** — adding or updating tests  
- **perf** — performance improvements  
- **chore** — maintenance tasks  

### Examples

\`\`\`
feat(mode-engine): add anomaly clustering
fix(api): correct run metadata response
docs(guide): update MODE authoring examples
\`\`\`

---

# 4. Coding Standards

### Python Requirements

- PEP 8 compliant  
- Type hints required  
- Pydantic for schemas  
- No global state  
- No nondeterministic behavior  
- No external dependencies inside MODEs  

### MODE Requirements

- Follow MODE_AUTHORING.md  
- Deterministic execution  
- Strict schema usage  
- No cross‑MODE imports  
- No environment variable access  

---

# 5. Adding a New MODE

### Required Structure

\`\`\`
console/modes/<mode_name>/
├── mode.yaml
├── main.py
├── config.py
├── handlers/
├── schemas/
└── tests/
\`\`\`

### Validation

\`\`\`
console modes validate <mode_name>
\`\`\`

### Testing

\`\`\`
pytest -q
\`\`\`

### Documentation

Update:

- MODE_CATALOG.md  
- DOCS_INDEX.md  

---

# 6. Testing Requirements

All contributions must include tests.

### Required Test Types

- Unit tests  
- Integration tests  
- Schema validation tests  
- Regression tests (snapshots/diffs)  

### Run All Tests

\`\`\`
pytest -q
\`\`\`

### Coverage Requirement

Minimum **85%** coverage for new code.

---

# 7. Documentation Requirements

When adding or modifying features:

- Update README.md if user‑facing  
- Update DEVELOPER_GUIDE.md for internal changes  
- Update MODE_AUTHORING.md for MODE changes  
- Update OPERATOR_GUIDE.md for workflow changes  
- Update API_REFERENCE.md for endpoint changes  

Documentation must be complete before merging.

---

# 8. Pull Request Workflow

1. Create a feature or fix branch  
2. Commit using Conventional Commits  
3. Push branch to repository  
4. Open a pull request  
5. Ensure all tests pass  
6. Request review  
7. Address feedback  
8. Merge after approval  

### PR Requirements

- Clear description  
- Linked issue (if applicable)  
- Tests included  
- Documentation updated  
- No failing checks  

---

# 9. Security Considerations

Contributors must ensure:

- No arbitrary code execution  
- No unsafe file access  
- No unvalidated inputs  
- No subprocess spawning  
- No network access outside declared MODE capabilities  
- No dynamic imports  
- No cross‑MODE access  
- No writes outside run directories  

Security is a first‑class requirement.

---

# 10. Release Process

The project uses **Semantic Versioning**:

- **MAJOR** — breaking changes  
- **MINOR** — new features  
- **PATCH** — bug fixes  

### Release Steps

1. Update CHANGELOG.md  
2. Bump version in project metadata  
3. Run full test suite  
4. Tag release  
5. Merge to `main`  
6. Publish release notes  

---

# Conclusion

By following this guide, contributors help maintain the SSRF Command Console’s standards of determinism, safety, and forensic clarity.  
Thank you for helping improve the project.

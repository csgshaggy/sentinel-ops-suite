# Security Posture

## Threat Model

- SSRF vectors
- Misconfigured proxies
- Unsafe request forwarding
- Plugin execution risks

## Security Tools

### Bandit

make ci-security

### Dependency Graph

make deps


## Hardening Recommendations

- Use Docker for isolation
- Validate plugins before loading
- Enforce CI gates before merging

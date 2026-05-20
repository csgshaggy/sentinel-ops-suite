# Operations Manual

This manual describes how operators interact with the SSRF Command Console.

## Daily Operations

### Health Check

Run: make self-check

### Environment Inspection

make env-inspect

### Running the Application

Choose one:

- `make uv-run`
- `make poetry-run`
- `python3 main.py`

### Docker Workflow

- Build: `make docker-build`
- Run: `make docker-run`
- Shell: `make docker-shell`

## Release Process

1. Ensure CI passes:
   make ci-check

2. Build release:
   make release

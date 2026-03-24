# Troubleshooting Guide

## Common Issues

### Import Errors

Run:

make self-check

### Broken Environment

make uninstall-env
make bootstrap

### Docker Issues

make docker-clean
make docker-build

### CI Failures

Run strict mode:

make ci-strict

## Auto-Repair

make repair

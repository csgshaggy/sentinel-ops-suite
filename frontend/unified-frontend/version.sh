#!/usr/bin/env bash
set -e

VERSION="$(date +'%Y.%m.%d-%H%M%S')"
echo "$VERSION" > src/version.txt
echo "Generated version: $VERSION"

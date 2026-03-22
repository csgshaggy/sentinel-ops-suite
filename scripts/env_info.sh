#!/usr/bin/env bash

source "$(dirname "$0")/banner.sh"

echo -e "[ENV] Python version:"
python3 --version
echo ""

echo -e "[ENV] Pip packages:"
pip list
echo ""

echo -e "[ENV] Git status:"
git status -s
echo ""

echo -e "[ENV] Disk usage:"
df -h .
echo ""

echo -e "[ENV] Memory usage:"
free -h

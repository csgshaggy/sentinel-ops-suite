#!/bin/bash
set -e

TARGET_DIR="src"
BAD="/admin/login"
GOOD="https://crcybercop.dpdns.org/login"

echo "--------------------------------------------------"
echo " SENTINEL OPS — FIX ADMIN LOGIN REDIRECTS"
echo " Replacing all '$BAD' with:"
echo "   $GOOD"
echo "--------------------------------------------------"
echo ""

cd "$(dirname "$0")"

if [ ! -d "$TARGET_DIR" ]; then
    echo "ERROR: Cannot find src/ directory. Run this script from dashboard-app/"
    exit 1
fi

FILES=$(grep -Rl "$BAD" "$TARGET_DIR")

if [ -z "$FILES" ]; then
    echo "No files found containing $BAD"
    exit 0
fi

echo "Found the following files:"
echo "$FILES"
echo ""

for f in $FILES; do
    echo "Backing up: $f → $f.bak"
    cp "$f" "$f.bak"

    echo "Updating: $f"
    sed -i "s|$BAD|$GOOD|g" "$f"
done

echo ""
echo "--------------------------------------------------"
echo " DONE — All redirects updated."
echo " You must now rebuild:"
echo "   npm install"
echo "   npm run build"
echo ""
echo "Then redeploy the dist/ folder and reload NGINX."
echo "--------------------------------------------------"

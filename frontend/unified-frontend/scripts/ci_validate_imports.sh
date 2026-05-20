#!/usr/bin/env bash
set -e

echo "[CI] Running import validation..."

BROKEN=0

# Scan all JS/JSX files
FILES=$(find src -type f \( -name "*.js" -o -name "*.jsx" \))

for FILE in $FILES; do
    IMPORTS=$(grep -Eo "from ['\"][\.]{1,2}[^'\"]+['\"]" "$FILE" | awk '{print $2}' | tr -d "'\"")

    for IMP in $IMPORTS; do
        TARGET=$(dirname "$FILE")/$IMP
        TARGET=$(realpath --quiet "$TARGET" 2>/dev/null)

        if [ ! -f "$TARGET" ]; then
            echo "[CI ERROR] Broken import in $FILE → $IMP"
            BROKEN=1
        fi
    done
done

if [ $BROKEN -eq 1 ]; then
    echo ""
    echo "[CI] ❌ Broken imports detected. Build failed."
    echo ""
    exit 1
fi

echo "[CI] ✔ All imports valid."
exit 0

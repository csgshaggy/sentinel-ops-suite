#!/bin/bash

set -e

echo "🔍 Scanning for incorrect Base imports..."

# Find all Python files under app/models/ that import the wrong Base
FILES=$(grep -Rl "from app.db.base_class import Base" app/models || true)

if [ -z "$FILES" ]; then
    echo "✅ No incorrect imports found in app/models."
    exit 0
fi

echo "🛠 Fixing imports in:"
echo "$FILES"
echo

# Replace incorrect import with correct one
for f in $FILES; do
    sed -i 's/from app.db.base_class import Base/from app.db.base import Base/' "$f"
    echo "✔ Updated: $f"
done

echo
echo "🎉 All model Base imports have been corrected."

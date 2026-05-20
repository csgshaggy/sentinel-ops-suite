#!/bin/bash

echo "Scanning for JSX usage inside .js files under src/ ..."
echo

# Find all .js files and check for JSX-like patterns
find src -name "*.js" | while read -r file; do
  if grep -Eq '<[A-Za-z][A-Za-z0-9]*[ >]' "$file"; then
    echo "Possible JSX in: $file"
  fi
done

echo
echo "Scan complete. Any files listed above should likely be renamed to .jsx (and imports updated)."

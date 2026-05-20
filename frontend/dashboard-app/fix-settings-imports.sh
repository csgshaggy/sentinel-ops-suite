#!/bin/bash

# Fix imports for SettingsContext after renaming .js → .jsx
echo "Updating imports for SettingsContext..."

grep -Rl 'services/SettingsContext"' src | while read -r file; do
    echo "Patching: $file"
    sed -i 's|services/SettingsContext"|services/SettingsContext.jsx"|g' "$file"
done

grep -Rl "services/SettingsContext'" src | while read -r file; do
    echo "Patching: $file"
    sed -i "s|services/SettingsContext'|services/SettingsContext.jsx'|g" "$file"
done

echo "Done. All imports updated."

# Run from: ~/sentinel-ops-suite/frontend/unified-frontend

echo "Patching default avatar paths..."

# Replace all occurrences of "/default-avatar.png" with "/static/default-avatar.png"
grep -Rl '"/default-avatar.png"' src | while read -r file; do
    echo "Patching $file"
    sed -i 's|"/default-avatar.png"|"/static/default-avatar.png"|g' "$file"
done

echo "Patch complete."

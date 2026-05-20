#!/bin/bash

ROOT_DIR="./src"

echo "🔍 Scanning for react-toastify imports..."

# Remove JS imports
grep -rl 'react-toastify' "$ROOT_DIR" | while read -r file; do
    echo "🧹 Cleaning imports in: $file"
    sed -i '/react-toastify/d' "$file"
done

# Remove ToastContainer JSX blocks
echo "🔍 Removing <ToastContainer /> blocks..."
grep -rl '<ToastContainer' "$ROOT_DIR" | while read -r file; do
    echo "🧹 Removing ToastContainer JSX in: $file"
    sed -i '/ToastContainer/d' "$file"
done

# Remove toastify CSS imports
echo "🔍 Removing toastify CSS imports..."
grep -rl 'react-toastify/dist' "$ROOT_DIR" | while read -r file; do
    echo "🧹 Removing toastify CSS import in: $file"
    sed -i '/react-toastify\/dist/d' "$file"
done

echo "🧽 Cleanup complete!"
echo "🚀 You can now run: npm run build"

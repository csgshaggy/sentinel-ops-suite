#!/bin/bash

ROOT="src"

echo "🔍 Verifying removal of useSessionContext and SessionProvider..."
echo ""

ISSUES=0

echo "------------------------------------------------------------"
echo "🔎 Checking for imports of useSessionContext..."
echo "------------------------------------------------------------"
grep -RIn "useSessionContext" "$ROOT" || echo "✔ No imports found."
if grep -RInq "useSessionContext" "$ROOT"; then
  ISSUES=$((ISSUES+1))
fi

echo ""
echo "------------------------------------------------------------"
echo "🔎 Checking for calls to useSessionContext()..."
echo "------------------------------------------------------------"
grep -RIn "useSessionContext()" "$ROOT" || echo "✔ No calls found."
if grep -RInq "useSessionContext()" "$ROOT"; then
  ISSUES=$((ISSUES+1))
fi

echo ""
echo "------------------------------------------------------------"
echo "🔎 Checking for references to SessionProvider..."
echo "------------------------------------------------------------"
grep -RIn "SessionProvider" "$ROOT" || echo "✔ No references found."
if grep -RInq "SessionProvider" "$ROOT"; then
  ISSUES=$((ISSUES+1))
fi

echo ""
echo "------------------------------------------------------------"
echo "🔎 Checking for leftover session context imports..."
echo "------------------------------------------------------------"
grep -RIn "../context/SessionProvider" "$ROOT" || echo "✔ No SessionProvider imports found."
if grep -RInq "../context/SessionProvider" "$ROOT"; then
  ISSUES=$((ISSUES+1))
fi

echo ""
echo "------------------------------------------------------------"
echo "📊 SUMMARY"
echo "------------------------------------------------------------"

if [ "$ISSUES" -eq 0 ]; then
  echo "🎉 All clear! No references to the old session system remain."
  echo "   Your frontend is fully migrated to useAuth()."
else
  echo "⚠️  Found $ISSUES issue(s)."
  echo "   Review the above output and patch the remaining files."
fi

echo ""
echo "Done."

from pathlib import Path
import sys
import difflib

ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "Makefile"
SNAPSHOT = ROOT / "data" / "Makefile.snapshot"

def make_badge(label, message, color):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="180" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="180" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <rect width="80" height="20" fill="#555"/>
    <rect x="80" width="100" height="20" fill="{color}"/>
    <rect width="180" height="20" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle"
     font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="40" y="14">{label}</text>
    <text x="130" y="14">{message}</text>
  </g>
</svg>
"""

def main():
    if not MAKEFILE.exists() or not SNAPSHOT.exists():
        sys.stdout.write(make_badge("makefile", "missing", "#e05d44"))
        return 1

    current = MAKEFILE.read_text().splitlines()
    baseline = SNAPSHOT.read_text().splitlines()
    diff = list(difflib.unified_diff(baseline, current))

    if diff:
        sys.stdout.write(make_badge("makefile", "drift", "#dfb317"))
        return 1

    sys.stdout.write(make_badge("makefile", "clean", "#4c1"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

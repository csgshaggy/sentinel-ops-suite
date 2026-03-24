#!/usr/bin/env python3
import json
import shutil
from pathlib import Path
import markdown

BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
MAP_FILE = DOCS_DIR / "category_map.json"
SITE_DIR = PROJECT_ROOT / "docs_site"

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    max-width: 900px;
}}
nav {{
    margin-bottom: 20px;
}}
nav a {{
    margin-right: 10px;
    text-decoration: none;
    color: #3366cc;
}}
h1, h2, h3 {{
    color: #333;
}}
pre {{
    background: #f4f4f4;
    padding: 10px;
    border-radius: 4px;
}}
</style>
</head>
<body>
<nav>
<a href="/index.html">Home</a>
{nav_links}
</nav>
{content}
</body>
</html>
"""


def load_map():
    with MAP_FILE.open() as f:
        return json.load(f)


def write_page(path, title, nav_links, content_html):
    html = TEMPLATE.format(title=title, nav_links=nav_links, content=content_html)
    path.write_text(html, encoding="utf-8")


def main():
    print(f"{BLUE}=== Generating HTML Documentation Site ==={RESET}")

    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()

    category_map = load_map()

    # Build navigation links
    nav_links = " ".join(
        f'<a href="/{cat}.html">{cat.capitalize()}</a>' for cat in category_map.keys()
    )

    # Generate category pages + file pages
    for category, files in category_map.items():
        cat_page = SITE_DIR / f"{category}.html"

        content = f"<h1>{category.capitalize()}</h1>\n<ul>"
        for f in files:
            html_name = f"{category}_{f.replace('.md', '.html')}"
            content += f'<li><a href="/{html_name}">{f}</a></li>'
        content += "</ul>"

        write_page(cat_page, category.capitalize(), nav_links, content)

        # Generate individual file pages
        for f in files:
            md_path = DOCS_DIR / category / f
            if not md_path.exists():
                continue

            html_name = f"{category}_{f.replace('.md', '.html')}"
            html_path = SITE_DIR / html_name

            md_text = md_path.read_text(encoding="utf-8")
            html_body = markdown.markdown(md_text)

            write_page(html_path, f, nav_links, html_body)

    # Generate main index
    index_html = "<h1>Documentation Index</h1><ul>"
    for category in category_map.keys():
        index_html += f'<li><a href="/{category}.html">{category.capitalize()}</a></li>'
    index_html += "</ul>"

    write_page(SITE_DIR / "index.html", "Documentation", nav_links, index_html)

    print(f"{GREEN}HTML site generated at {SITE_DIR}{RESET}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Convert Markdown documentation to HTML with styling.
This script converts all .md files in the Documentation folder to HTML.
"""

import os
import re
from pathlib import Path


def markdown_to_html(md_content, title="Documentation"):
    """Convert markdown content to styled HTML"""

    # Escape HTML in code blocks first
    def escape_code_block(match):
        code = match.group(1)
        # HTML escape
        code = code.replace('&', '&amp;')
        code = code.replace('<', '&lt;')
        code = code.replace('>', '&gt;')
        return f'<pre><code>{code}</code></pre>'

    # Process code blocks (```)
    html = re.sub(r'```[\w]*\n(.*?)\n```', escape_code_block, md_content, flags=re.DOTALL)

    # Process inline code (`)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Process headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # Process bold (**text**)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Process italic (*text*)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Process links [text](url)
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

    # Process unordered lists
    def process_list(match):
        items = match.group(0)
        items = re.sub(r'^[\s]*[-\*\+] (.+)$', r'<li>\1</li>', items, flags=re.MULTILINE)
        return f'<ul>{items}</ul>'

    # Find list blocks
    html = re.sub(r'((?:^[\s]*[-\*\+] .+$\n?)+)', process_list, html, flags=re.MULTILINE)

    # Process ordered lists
    def process_ordered_list(match):
        items = match.group(0)
        items = re.sub(r'^[\s]*\d+\. (.+)$', r'<li>\1</li>', items, flags=re.MULTILINE)
        return f'<ol>{items}</ol>'

    html = re.sub(r'((?:^[\s]*\d+\. .+$\n?)+)', process_ordered_list, html, flags=re.MULTILINE)

    # Process blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Process horizontal rules
    html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)

    # Process paragraphs (lines followed by blank line)
    lines = html.split('\n')
    in_paragraph = False
    result = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip if it's already HTML
        if stripped.startswith('<'):
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            result.append(line)
        elif stripped == '':
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            result.append(line)
        else:
            if not in_paragraph:
                result.append('<p>')
                in_paragraph = True
            result.append(line)

    if in_paragraph:
        result.append('</p>')

    html = '\n'.join(result)

    # Wrap in full HTML document with styling
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background: white;
        }}

        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }}

        h2 {{
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 30px;
        }}

        h3 {{
            color: #2c3e50;
            margin-top: 25px;
        }}

        h4 {{
            color: #34495e;
            margin-top: 20px;
        }}

        p {{
            margin: 15px 0;
        }}

        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 90%;
            color: #e74c3c;
        }}

        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
        }}

        pre code {{
            background: none;
            color: #ecf0f1;
            padding: 0;
            font-size: 14px;
        }}

        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}

        li {{
            margin: 8px 0;
        }}

        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background: #ecf0f1;
            font-style: italic;
        }}

        a {{
            color: #3498db;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}

        th {{
            background: #3498db;
            color: white;
        }}

        tr:nth-child(even) {{
            background: #f9f9f9;
        }}

        strong {{
            color: #2c3e50;
        }}

        em {{
            color: #7f8c8d;
        }}

        .toc {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}

        .toc h2 {{
            margin-top: 0;
            border-bottom: none;
        }}
    </style>
</head>
<body>
    {html}
</body>
</html>
"""

    return full_html


def convert_all_markdown_files():
    """Convert all markdown files in Documentation folder to HTML"""
    docs_dir = Path(__file__).parent

    print("Converting Markdown files to HTML...\n")

    converted = 0
    for md_file in docs_dir.glob('*.md'):
        print(f"Converting {md_file.name}...", end=' ')

        try:
            # Read markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # Convert to HTML
            title = md_file.stem.replace('_', ' ').title()
            html_content = markdown_to_html(md_content, title)

            # Write HTML
            html_file = md_file.with_suffix('.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print("✅")
            converted += 1

        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"\n✅ Converted {converted} files successfully!")
    print(f"\n📄 Open index.html in your web browser to view the documentation.")


if __name__ == "__main__":
    convert_all_markdown_files()

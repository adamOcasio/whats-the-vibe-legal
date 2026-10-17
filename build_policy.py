"""Turns the page section of one of the app repository's legal sources (between its two --- lines)
into a page: PRIVACY_POLICY.md into privacy/index.html, TERMS_OF_USE.md into terms/index.html.

    python3 build_policy.py <path to PRIVACY_POLICY.md> privacy/index.html
    python3 build_policy.py <path to TERMS_OF_USE.md> terms/index.html "Terms of use" \
        "The rules for using the what’s the vibe? app, with no tolerance for objectionable content or abusive users."

The page title and description default to the privacy policy's.
"""
import html
import re
import sys

source, out = sys.argv[1], sys.argv[2]
page_title = sys.argv[3] if len(sys.argv) > 3 else 'Privacy policy'
description = (sys.argv[4] if len(sys.argv) > 4 else
               'How the what’s the vibe? app collects, uses, keeps and deletes information.')
text = open(source, encoding='utf-8').read()
parts = text.split('\n---\n')
policy = parts[1].strip()


def inline(value: str) -> str:
    value = html.escape(value, quote=False)
    value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
    value = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2">\1</a>', value)
    value = re.sub(r'\b([\w.+-]+@[\w-]+\.[\w.]+)\b', r'<a href="mailto:\1">\1</a>', value)
    return value


body = []
blocks = re.split(r'\n\s*\n', policy)
title = ''
for block in blocks:
    lines = block.split('\n')
    if block.startswith('# '):
        title = block[2:].strip()
        body.append(f'<h1>{inline(title)}</h1>')
    elif block.startswith('## '):
        body.append(f'<h2>{inline(block[3:].strip())}</h2>')
    elif all(line.startswith('|') for line in lines):
        rows = [[c.strip() for c in line.strip('|').split('|')] for line in lines if not re.match(r'^\|[\s|-]+\|$', line)]
        head, *rest = rows
        table = ['<table>', '<thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead>', '<tbody>']
        table += ['<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in row) + '</tr>' for row in rest]
        table.append('</tbody></table>')
        body.append('\n'.join(table))
    elif lines[0].startswith('- '):
        items, current = [], None
        for line in lines:
            if line.startswith('- '):
                if current is not None:
                    items.append(current)
                current = line[2:].strip()
            else:
                current += ' ' + line.strip()
        items.append(current)
        body.append('<ul>' + ''.join(f'<li>{inline(i)}</li>' for i in items) + '</ul>')
    else:
        paragraph = ' '.join(line.strip() for line in lines)
        cls = ' class="effective"' if paragraph.startswith('Effective ') else ''
        body.append(f'<p{cls}>{inline(paragraph)}</p>')

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page_title)} · what’s the vibe?</title>
<meta name="description" content="{html.escape(description)}">
<style>
  :root {{ --paper: #F6F5EF; --ink: #11120F; --muted: #74766D; --line: #E0E1D7; --lilac: #C9B7F6; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --paper: #11120F; --ink: #F6F5EF; --muted: #A9AB9F; --line: #2C2D28; --lilac: #8E77D6; }}
  }}
  * {{ box-sizing: border-box; }}
  html {{ -webkit-text-size-adjust: 100%; }}
  body {{ margin: 0; background: var(--paper); color: var(--ink);
    font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
  main {{ max-width: 720px; margin: 0 auto; padding: 40px 16px 64px; }}
  h1 {{ font-size: 2.1rem; line-height: 1.1; letter-spacing: -0.02em; margin: 0 0 8px; }}
  h2 {{ font-size: 1.25rem; margin: 2.2em 0 0.5em; padding-top: 1.2em; border-top: 1px solid var(--line); }}
  p, li {{ overflow-wrap: anywhere; }}
  .effective {{ color: var(--muted); margin-top: 0; }}
  a {{ color: inherit; text-decoration-color: var(--lilac); text-decoration-thickness: 2px; text-underline-offset: 3px; }}
  ul {{ padding-left: 1.2em; }}
  li {{ margin: 0.35em 0; }}
  table {{ width: 100%; border-collapse: collapse; margin: 1em 0; font-size: 0.95rem; }}
  th, td {{ text-align: left; vertical-align: top; padding: 8px 10px 8px 0; border-bottom: 1px solid var(--line); }}
  th {{ font-weight: 600; }}
</style>
</head>
<body>
<main>
{chr(10).join(body)}
</main>
</body>
</html>
'''
open(out, 'w', encoding='utf-8').write(page)
print(title, len(body), 'blocks')

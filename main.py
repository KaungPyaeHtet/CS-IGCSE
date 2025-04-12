import markdown
from markdown.extensions.toc import TocExtension
import os
import sys

def convert_md_to_html(output_html):
    with open("Questions.md", 'r', encoding='utf-8') as f:
        md_text = f.read()

    html = markdown.markdown(
        md_text,
        extensions=[TocExtension(toc_depth=3), 'fenced_code', 'tables'],
        output_format='html5'
    )

    # HTML Template
    full_html = f"""
<!DOCTYPE html>
<html data-theme="dark">
<head>
    <meta charset="UTF-8">
    <title>IGCSE Edexcel (9-1) Commonly Asked Questions</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-dark.min.css" id="prism-theme">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/prism.min.js" defer></script>
</head>
<body>
    <button onclick="toggleTheme()" class="theme-toggle" title="Toggle Theme">🌓</button>
    {html}
    <footer style="margin-top: 4rem; padding-top: 1rem; border-top: 1px solid var(--border); text-align: center; font-size: 0.9rem; color: var(--text); opacity: 0.7;">
        <div>&copy; 2025 Ozzy</div>
        <div style="margin-top: 0.5rem;">
            Contributions are welcome!<br>
            <a href="https://github.com/kaungpyaehtet/CS-IGCSE" target="_blank" style="color: var(--primary); text-decoration: underline;">Submit a pull request on GitHub</a> or contact me directly.
        </div>
    </footer>

    <script>
        function toggleTheme() {{
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);

            const prismLink = document.getElementById('prism-theme');
            if (prismLink) {{
                prismLink.href = `https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-${{next}}.min.css`;
            }}
        }}

        document.querySelectorAll('details').forEach(detail => {{
            const key = 'detail-' + (detail.id || detail.querySelector('summary').textContent.trim());
            const saved = localStorage.getItem(key);
            if (saved === 'open') detail.open = true;

            detail.addEventListener('toggle', () => {{
                localStorage.setItem(key, detail.open ? 'open' : 'closed');
            }});
        }});
    </script>
</body>
</html>
"""


    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✨ Converted 'Questions.md' to '{output_html}'")

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: python main.py index.html")
    else:
        convert_md_to_html(sys.argv[1])

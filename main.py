import markdown
from markdown.extensions.toc import TocExtension
import os
import sys
import re

def convert_custom_questions(md_text):
    # Process :::answer blocks first
    md_text = re.sub(
        r':::answer\n(.*?)\n:::',
        lambda m: f'<div class="cool-answer">\n{m.group(1)}\n</div>',
        md_text,
        flags=re.DOTALL
    )
    
    # Rest of the existing processing
    topics = re.split(r'(^## .*?$)', md_text, flags=re.MULTILINE)[1:]
    processed_text = ""
    
    for i in range(0, len(topics), 2):
        topic_header = topics[i].strip()
        topic_content = topics[i+1].strip() if i+1 < len(topics) else ""
        processed_text += topic_header + "\n\n"
        
        paragraphs = re.split(r'\n\n+', topic_content)
        
        for para in paragraphs:
            if not para.strip():
                continue
                
            if '\n' in para:
                question, answer = para.split('\n', 1)
                question = question.strip()
                answer = answer.strip()
                processed_text += f"<details>\n<summary><strong>{question}</strong></summary>\n\n{answer}\n\n</details>\n\n"
            else:
                processed_text += para + "\n\n"
    
    return processed_text

def convert_md_to_html(output_html):
    try:
        with open("Questions.md", 'r', encoding='utf-8') as f:
            md_text = f.read()
    except FileNotFoundError:
        print("Error: 'Questions.md' not found.")
        sys.exit(1)

    # Convert our custom question format to proper Markdown
    md_text = convert_custom_questions(md_text)

    # Convert to HTML with our extensions
    html = markdown.markdown(
        md_text,
        extensions=[TocExtension(toc_depth=3), 'fenced_code', 'tables'],
        output_format='html5'
    )

    # HTML Template
    full_html = f"""<!DOCTYPE html>
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

        // Toggle details open/closed state based on localStorage
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

    # Write the generated HTML to the output file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✨ Converted 'Questions.md' to '{output_html}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py output.html")
    else:
        convert_md_to_html(sys.argv[1])
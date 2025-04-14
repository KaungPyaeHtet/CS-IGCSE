import markdown
from markdown.extensions.toc import TocExtension
import os
import sys
import re
import json
from mmTranslations import TRANSLATIONS
from pdfconvert import convert

translation_js = "const translations = " + json.dumps(TRANSLATIONS, ensure_ascii=False, indent=4) + ";"

def translate_text(text, lang):
    if lang == "english":
        return text
    return TRANSLATIONS.get(text, text)

def convert_custom_questions(md_text):
    """
    Convert ## to <span data-translate> {text} </span>
    Convert questions answer lines to <details><summary>{question}</summary>{answer}</details
    """
    md_text = re.sub(
        r'^(#+ )(.+?)$',
        lambda m: f'{m.group(1)}<span data-translate="{m.group(2)}">{m.group(2)}</span>',
        md_text,
        flags=re.MULTILINE
    )

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
                processed_text += f"<details>\n<summary>{question}</summary>\n\n{answer}\n\n</details>\n\n"
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

    md_text = convert_custom_questions(md_text)

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
    <link rel="stylesheet" href="index.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css" id="prism-theme-light" disabled>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-dark.min.css" id="prism-theme-dark"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-python.min.js"></script>

</head>
<body>
    <button onclick="toggleTheme()" class="theme-toggle" title="Toggle Theme">🌓</button>
    <a href="contributors.html" class='contributor-link'>Contributors</a>
    <button onclick="closeAllToggles()" class="close-all" title="Close All Toggles">x Close All Sections</button>
    <a href="output.pdf" download>
        <button class='download-pdf'>Download PDF Version</button>
    </a>
    
    <div class='language-toggle'><strong id='burmese-toggle-text' class="language-toggle-text" onclick="toggleLanguage('burmese')">က</strong> | <strong id='english-toggle-text' class='language-active language-toggle-text' onclick="toggleLanguage('english')">A</strong></div>
    {html}
    <div class="random-questions-container" id='random-question'>
        <h2><span data-translate="Practice Random Questions">Practice Random Questions</span></h2>
        <div class="random-questions-controls">
            <input type="number" id="question-count" min="1" value="5" placeholder="Number of questions">
            <button onclick="startRandomQuestions()" class="random-questions-button">
                <span data-translate="Start Random Questions">Start Random Questions</span>
            </button>
            <button onclick="stopRandomQuestions()" class="random-questions-button stop-button">
                <span data-translate="Stop Practice">Stop Practice</span>
            </button>
        </div>
        <div id="random-questions-display"></div>
    </div>
    <footer style="margin-top: 4rem; padding-top: 1rem; border-top: 1px solid var(--border); text-align: center; font-size: 0.9rem; color: var(--text); opacity: 0.7;">
        <div>&copy; 2025 Ozzy</div>
        <div style="margin-top: 0.5rem;">
            <span data-translate='Contributions are welcome!'>Contributions are welcome!</span><br>
            <a href="https://github.com/kaungpyaehtet/CS-IGCSE" target="_blank" style="color: var(--primary); text-decoration: underline;"><span data-translate='Submit a pull request on GitHub or contact me directly.'>Submit a pull request on GitHub or contact me directly.</span></a>
        </div>
    </footer>
    <script>
        function toggleTheme() {{
            const html = document.documentElement;
  const current = html.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  html.setAttribute("data-theme", next);

  // Update Prism theme
  const lightTheme = document.getElementById("prism-theme-light");
  const darkTheme = document.getElementById("prism-theme-dark");
  
  if (next === "light") {{
    lightTheme.disabled = false;
    darkTheme.disabled = true;
  }} else {{
    lightTheme.disabled = true;
    darkTheme.disabled = false;
  }}
        }}
function toggleLanguage(lang) {{
            document.documentElement.setAttribute('data-lang', lang);
            
            const burmeseBtn = document.getElementById('burmese-toggle-text');
            const englishBtn = document.getElementById('english-toggle-text');
            
            if (lang === 'burmese') {{
                burmeseBtn.classList.add('language_active');
                englishBtn.classList.remove('language_active');
            }} else {{
                englishBtn.classList.add('language_active');
                burmeseBtn.classList.remove('language_active');
            }}
            
            // Translate all elements with data-translate attribute
            document.querySelectorAll('[data-translate]').forEach(el => {{
                const key = el.getAttribute('data-translate');
                if (lang === 'burmese') {{
                    el.textContent = translations[key] || el.textContent;
                }} else {{
                    el.textContent = key; // Revert to English
                }}
            }});
        }}
        
        // Translations dictionary
        {translation_js}

         function closeAllToggles() {{
            document.querySelectorAll('details').forEach(detail => {{
                // Close the toggle
                detail.open = false;
                
                // Remove from localStorage
                const key = 'detail-' + (detail.id || detail.querySelector('summary').textContent.trim());
                localStorage.removeItem(key);
            }});
            
            // Optional: Show a brief confirmation
            alert('All sections have been closed');
        }}

        // LocalStorage Toggle
        document.querySelectorAll('details').forEach(detail => {{
            const key = 'detail-' + (detail.id || detail.querySelector('summary').textContent.trim());
            const saved = localStorage.getItem(key);
            if (saved === 'open') detail.open = true;

            detail.addEventListener('toggle', () => {{
                localStorage.setItem(key, detail.open ? 'open' : 'closed');
            }});
        }});

let currentRandomQuestions = [];
        let score = {{ correct: 0, wrong: 0 }};

        function getAllQuestions() {{
            return Array.from(document.querySelectorAll('details')).filter(detail => {{
                return !detail.closest('.random-questions-container');
            }});
        }}

        function startRandomQuestions() {{
            const countInput = document.getElementById('question-count');
            const count = parseInt(countInput.value) || 5;
            const allQuestions = getAllQuestions();
            
            if (allQuestions.length === 0) {{
                alert('No questions found!');
                return;
            }}
            
            // Reset score and clear previous session
            score = {{ correct: 0, wrong: 0 }};
            stopRandomQuestions();
            
            // Shuffle and select questions
            const shuffled = [...allQuestions].sort(() => 0.5 - Math.random());
            currentRandomQuestions = shuffled.slice(0, Math.min(count, shuffled.length));
            
            // Display the questions
            const display = document.getElementById('random-questions-display');
            display.innerHTML = '';
            
            currentRandomQuestions.forEach((question, index) => {{
                const clone = question.cloneNode(true);
                clone.id = `random-question-${{index}}`;
                clone.dataset.answered = "unanswered";
                clone.open = false;
                
                // Create buttons container
                const buttonsDiv = document.createElement('div');
                buttonsDiv.className = 'question-buttons';
                
                // Correct button
                const correctBtn = document.createElement('button');
                correctBtn.className = 'correct-button';
                correctBtn.textContent = 'Correct ✅';
                correctBtn.onclick = function() {{
                    clone.dataset.answered = "correct";
                    score.correct++;
                    updateScoreDisplay();
                    buttonsDiv.remove();
                }};
                
                // Wrong button
                const wrongBtn = document.createElement('button');
                wrongBtn.className = 'wrong-button';
                wrongBtn.textContent = 'Wrong ❌';
                wrongBtn.onclick = function() {{
                    clone.dataset.answered = "wrong";
                    score.wrong++;
                    updateScoreDisplay();
                    buttonsDiv.remove();
                }};
                
                buttonsDiv.appendChild(correctBtn);
                buttonsDiv.appendChild(wrongBtn);
                clone.appendChild(buttonsDiv);
                display.appendChild(clone);
            }});
            
            // Create score display
            const scoreDisplay = document.createElement('div');
            scoreDisplay.className = 'score-display';
            scoreDisplay.id = 'score-display';
            display.appendChild(scoreDisplay);
            
            updateScoreDisplay();
            display.scrollIntoView({{ behavior: 'smooth' }});
        }}

        function updateScoreDisplay() {{
            const total = currentRandomQuestions.length;
            const unanswered = total - score.correct - score.wrong;
            const scoreDisplay = document.getElementById('score-display');
            
            if (scoreDisplay) {{
                scoreDisplay.innerHTML = `
                    Score: ${{score.correct}}/${{total}} | 
                    Correct: ${{score.correct}} | 
                    Wrong: ${{score.wrong}} | 
                    Unanswered: ${{unanswered}}
                `;
            }}
        }}

        function stopRandomQuestions() {{
            currentRandomQuestions = [];
            document.getElementById('random-questions-display').innerHTML = '';
        }}

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
        print("Usage: python main.py index.html")
    else:
        convert_md_to_html(sys.argv[1])
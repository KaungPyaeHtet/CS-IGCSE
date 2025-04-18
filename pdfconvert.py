from playwright.sync_api import sync_playwright
from pathlib import Path


def convert(path):
    html_path = Path(path).resolve()
    pdf_path = "output.pdf"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Set larger viewport for better rendering
        page.set_viewport_size({"width": 1920, "height": 1080})

        # Load the HTML file
        page.goto(f"file://{html_path}", wait_until="networkidle")

        # Force all details elements to open and ensure visibility
        page.evaluate("""() => {
            // Force dark theme
            document.documentElement.setAttribute('data-theme', 'dark');
            
            // Open ALL details elements and ensure they stay open
            document.querySelectorAll("details").forEach(detail => {
                detail.open = true;
                // Remove any toggle event listeners that might interfere
                detail.onclick = null;
                detail.ontoggle = null;
            });
            
            // Remove interactive elements that might cause issues
            document.querySelectorAll('.theme-toggle, .close-all, .contributor-link, .language-toggle, .toggle-download').forEach(el => el.remove());
            
            // Force visibility of all answer content
            document.querySelectorAll('details > div').forEach(div => {
                div.style.display = 'block';
                div.style.opacity = '1';
                div.style.height = 'auto';
                div.style.overflow = 'visible';
            });
            
            // Wait for any lazy-loaded content
            return new Promise(resolve => setTimeout(resolve, 2000));
        }""")

        # Add print-specific CSS to ensure proper rendering
        page.add_style_tag(content="""
            /* Force all details to show their content */
            details {
                display: block !important;
                overflow: visible !important;
            }
            
            details > div {
                display: block !important;
                opacity: 1 !important;
                height: auto !important;
                overflow: visible !important;
            }
            
            summary {
                display: list-item !important; /* Keep the triangle marker */
                cursor: default !important; /* Remove pointer cursor */
            }
            
            summary::after {
                content: "" !important; /* Remove any dynamic content */
            }
            
            /* Remove interactive elements */
            .theme-toggle, .close-all, .contributor-link, .language-toggle,
            .random-questions-container, .question-buttons {
                display: none !important;
            }
            
            /* Ensure proper spacing */
            details {
                margin: 15px 0 !important;
                padding: 10px !important;
                page-break-inside: avoid !important;
            }
            
            /* Force visibility of all content */
            [hidden], [style*="display: none"], [style*="opacity: 0"] {
                display: block !important;
                opacity: 1 !important;
            }
            
            /* Code block styling */
            pre, code {
                white-space: pre-wrap !important;
                page-break-inside: avoid !important;
            }
        """)

        # Generate PDF with optimal settings
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            scale=1,
            display_header_footer=False,
            prefer_css_page_size=True
        )
        browser.close()

    print(f"PDF successfully generated at {pdf_path}")

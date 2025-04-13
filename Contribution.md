# Contributing Guidelines

Thank you for your interest in contributing to the IGCSE CS Edexcel Questions

Project is aimed directly at those who cannot afford notes and are in need of free resource. This version is made for community and isn't allowed to released for financial gains. You may contribute or host it yourself.

## 📘 How to Contribute Questions

1. **Fork the repository**.
2. **Create a new branch**:  
    ```bash
    git checkout -b your-feature-name
    ```
3. **Edit Questions.md**
* Follow the existing format.
* Use proper Markdown syntax.
* Make sure to be careful with spaces and lines
* Use a structure like this:
    ```
    <h2>Heading topics</h2>
    Question: What is the main difference between pseudocode and flowchart
    Answer: <html tags> {Answer} </html tags close>

    ```
* Add to git
    ```bash
    git add Questions.md
    ```

4. Commit your changes:
    ```bash
    git commit -m "Added questions on Topic XYZ"
    ```
5. Push and create a pull request:
* Push and create a Pull Request:
    ```bash
    git push -u origin your-branch-name
    ```
* Write a clear title and description for your PR.
* Explain what you added or modified.
* Once reviewed, your changes will be merged!

## Style Guide
* Using markschemes images are fine.
* Keep simple, concise, and consistent language usage.

## Questions.md Format
The syntax are important to follow, especially spaces and lines are sensitive in converting md file to html file.
* Do not add trailing double spaces.
* Do not leave blank lines between question and answer.
* Your format should be
    * Simple sentence for question
        ```md
        What is a question?
        ```
    * HTML tag for answer
        ```html
        <answer> answer </answer>
        ```
    * Answer has multiple types supported
        * img for image
        * ul li or ol li for list items
        * p for simple paragraph
* Images
    * your images should be in assets/ folder
    * assets/ will contain 6 subfolders with respect to their topics.
    * Your image should be at least 750px or similar as I have set width of image to 750px hard coded.
    * Use consistent naming conventions

## Testing Changes
```bash
python3 main.py index.html
```
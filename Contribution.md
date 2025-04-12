# Contributing Guidelines

Thank you for your interest in contributing to the IGCSE CS FAQ project! 🙌

This project aims to provide a structured and clean collection of commonly asked questions for IGCSE Computer Science. All contributions are welcome, especially from educators, students, and learners from around the world.

---

## 📘 How to Contribute Questions

1. **Fork the repository**.
2. **Create a new branch**:  
```bash
git checkout -b your-feature-name
```
3. **Edit Questions.md**
* Follow the existing format.
* Use proper Markdown syntax.
* Group your questions under clear topics (e.g., ### Topic Name).
* Use a structure like this:
```
## for Heading topics

Q: What is the main difference between pseudocode and flowchart
A: Pseudocode is a text-based way to describe algorithms using programming-like syntax,
while flowcharts are graphical representations using standardized symbols. 

```
4. Commit your changes:
```bash
git commit -m "Added questions on Topic XYZ"
```
5. Push and create a pull request:
* Push and create a Pull Request:
* Use force when index.html are different 
```bash
git push -u origin your-branch-name --force
```
* Write a clear title and description for your PR.
* Explain what you added or modified.
* Once reviewed, your changes will be merged!

## 💡 Style Guide
* Keep explanations concise and beginner-friendly.
* Avoid copying directly from textbooks.
* Use plain language and examples where helpful.

## Testing Changes
```bash
python3 main.py index.html
```
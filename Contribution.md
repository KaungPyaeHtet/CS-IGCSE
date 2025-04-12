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
#### Topic: Algorithms

<details>
<summary>What is an algorithm?</summary>
An algorithm is a step-by-step procedure to solve a problem or perform a task.
</details>

```
4. Commit your changes:
```bash
git commit -m "Added questions on Topic XYZ"
```
5. Push and create a pull request:
* Push and create a Pull Request:
* Write a clear title and description for your PR.
* Explain what you added or modified.
* Once reviewed, your changes will be merged!

## 💡 Style Guide
* Keep explanations concise and beginner-friendly.
* Avoid copying directly from textbooks.
* Use plain language and examples where helpful.

## Testing Changes
```bash
python3 main.py output.html dark
```
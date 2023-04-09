# rwgpt

> AI-powered code review tool using GPT-4. Get instant, actionable feedback on your git diffs.

## What is rwgpt?

rwgpt is an automated code review CLI that uses GPT to analyze your code changes. It acts as a senior engineer, reviewing your diffs for bugs, security issues, performance problems, and best practices.

**Works in any git repository** - Install once, use everywhere!

## Installation/Update

**One-Line Install:**

```bash
pip install git+https://github.com/yourusername/ai-pr-reviewer.git
```

**Set your OpenAI API key:**

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

**Make it permanent** (add to `~/.zshrc` or `~/.bashrc`):

```bash
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.zshrc
```

That's it! Now `rwgpt` works from **any directory**. 🎉

## Usage

From any git repository:

```bash
# Review uncommitted changes
rwgpt --input "$(git diff)"

# Review last commit
rwgpt --input "$(git show)"

# Review staged changes
rwgpt --input "$(git diff --staged)"
```

**Common options:**

```bash
# Use GPT-3.5 (faster, cheaper)
rwgpt --input "$(git diff)" -m gpt-3.5

# More detailed review
rwgpt --input "$(git diff)" --max 2000

# Verbose mode
rwgpt --input "$(git diff)" -v
```

### All Available Options

| Option          | Shorthand | Description               | Default  |
| --------------- | --------- | ------------------------- | -------- |
| `--input`       | -         | Git diff string to review | Required |
| `--input-file`  | -         | Read diff from file       | -        |
| `--model`       | `-m`      | Model: `gpt4`, `gpt-3.5`  | `gpt-4`  |
| `--max`         | -         | Max output tokens         | `900`    |
| `--temperature` | `-t`      | Creativity (0.0-1.0)      | `0.2`    |
| `--verbose`     | `-v`      | Show configuration        | `false`  |

### Example with All Flags

```bash
rwgpt --input "$(git diff)" -m gpt4 --max 1500 -t 0.2 -v
```

## What does it review?

- 🐛 **Bugs** - Logic errors, edge cases, potential crashes
- 🔒 **Security** - SQL injection, XSS, vulnerabilities
- ⚡ **Performance** - Inefficient code, N+1 queries
- 📖 **Readability** - Naming, code structure
- 🧪 **Testing** - Missing tests, test coverage
- 📚 **Best Practices** - Code smells, anti-patterns

## Output Example

````markdown
# example.py

## Line 10

### Comment

SQL injection vulnerability - user input is directly concatenated into query.

### Suggested Change

```python
data = db.query("SELECT * FROM users WHERE id = %s", (user_id,))
```
````

```

## Requirements

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git

## License

MIT License

---

Made with ❤️ for better code reviews
```

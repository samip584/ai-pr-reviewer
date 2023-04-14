# rwgpt

> AI-powered code review tool using GPT-4. Get instant, actionable feedback on your git diffs.

## What is rwgpt?

rwgpt is an automated code review CLI that uses GPT to analyze your code changes. It acts as a senior engineer, reviewing your diffs for bugs, security issues, performance problems, and best practices.

**Works in any git repository** - Install once, use everywhere!

## Quick Start (2 minutes)

### 1. Install rwgpt

```bash
pip install git+https://github.com/samip584/ai-pr-reviewer.git
```

### 2. Set your OpenAI API key

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

**Make it permanent** (add to `~/.zshrc` or `~/.bashrc`):

```bash
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Use it!

From any git repository:

```bash
# Review uncommitted changes
rwgpt --input "$(git diff)"

# Review last commit
rwgpt --input "$(git show)"

# Review staged changes
rwgpt --input "$(git diff --staged)"
```

That's it! 🎉

## Usage Examples

### Basic Usage

```bash
# Review before committing
git diff | rwgpt

# Review a specific commit
rwgpt --input "$(git show abc123)"

# Review changes between branches
rwgpt --input "$(git diff main..feature-branch)"

# Save review to file
rwgpt --input "$(git diff)" > review.md
```

### Advanced Options

```bash
# Use GPT-3.5 (faster, cheaper)
rwgpt --input "$(git diff)" -m gpt-3.5

# More detailed review (more tokens)
rwgpt --input "$(git diff)" --max 2000

# Verbose mode (shows config)
rwgpt --input "$(git diff)" -v

# All flags example
rwgpt --input "$(git diff)" -m gpt4 --max 1500 -t 0.2 -v
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

## CI/CD Integration

You can integrate rwgpt into your CI/CD pipeline to automatically review code changes in pull requests or commits.

### GitHub Actions Example

Create a `.github/workflows/review.yml` file in your repository:

```yaml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Install rwgpt
        run: pip install git+https://github.com/samip584/ai-pr-reviewer.git
      - name: Run AI Review
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          rwgpt --input "$(git show HEAD)" > review.md
          cat review.md
```

This workflow:
- Triggers on pull requests
- Installs Python and rwgpt
- Runs the AI review on the latest commit in the PR
- Outputs the review to the console (you can extend this to post comments)

### Other CI/CD Platforms

For GitLab CI, Jenkins, CircleCI, etc.:

1. **Install dependencies:**
   ```bash
   pip install git+https://github.com/samip584/ai-pr-reviewer.git
   ```

2. **Set environment variable:**
   - Add `OPENAI_API_KEY` as a secret/environment variable in your CI settings

3. **Run the review:**
   ```bash
   rwgpt --input "$(git show HEAD)"
   ```

   Or for a specific commit: `rwgpt --input "$(git show <commit_hash>)"`

### Notes

- **API Costs:** Be mindful of OpenAI API usage costs for frequent CI runs
- **Review Quality:** Use AI review as a supplement to human code review, not a replacement
- **Customization:** Adjust model, temperature, and max tokens for your needs
- **Integration:** Consider tools like [reviewdog](https://github.com/reviewdog/reviewdog) to post review comments automatically

## What the AI Reviews

The AI acts as a senior engineer and checks for:

- 🐛 **Bugs** - Logic errors, edge cases, potential crashes
- 🔒 **Security** - SQL injection, XSS, vulnerabilities
- ⚡ **Performance** - Inefficient code, N+1 queries
- 📖 **Readability** - Naming, code structure
- 🧪 **Testing** - Missing tests, test coverage
- 📚 **Best Practices** - Code smells, anti-patterns

## Output Format

The AI provides structured feedback with:

````markdown
# filename.py

## Line 42

### Comment

Explanation of the issue or improvement

### Suggested Change

```python
# Better code here
```
````

````

## Example Output

```markdown
# example.py

## Line 10

### Comment
SQL injection vulnerability - user input is directly concatenated into query.

### Suggested Change
```python
data = db.query("SELECT * FROM users WHERE id = %s", (user_id,))
````

````

## Requirements

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git

## Troubleshooting

### Command not found

If `rwgpt` is not found after installation:

1. **Check if it's installed:**
   ```bash
   pip show rwgpt
````

2. **Try using Python module directly:**

   ```bash
   python3 -m rwgpt --help
   ```

3. **Ensure pip install location is in PATH:**

   ```bash
   python3 -m site --user-base
   # Add the bin directory to your PATH
   ```

4. **Reinstall:**
   ```bash
   pip uninstall rwgpt
   pip install git+https://github.com/samip584/ai-pr-reviewer.git
   ```

### API Key Issues

If you get an authentication error:

1. **Verify your API key is set:**

   ```bash
   echo $OPENAI_API_KEY
   ```

2. **Check your API key is valid at:** https://platform.openai.com/api-keys

3. **Ensure you have billing set up** on your OpenAI account

## License

MIT License

---

Made with ❤️ for better code reviews

```

```

#!/usr/bin/env python3
"""
rwgpt: a tiny GPT-powered code review CLI for git diffs

Usage example:
  rwgpt --input "$(git show -U4)"

Requires:
  - Python 3.8+
  - pip install openai
  - OPENAI_API_KEY set in your environment
"""
import os
import sys
import argparse

try:
    from openai import OpenAI
except Exception:
    print("Error: The 'openai' package is required. Install with: pip install openai", file=sys.stderr)
    sys.exit(2)

# Constants
API_BASE_URL = "https://api.openai.com/v1/"

PROMPT_PREFIX = """From a code reviewer's perspective, Review the the git diff below and tell me what I can improve on in the code (the '+' in the git diff is an added line, the '-' is a removed line). Only review the changes that code that has been added i.e. the code denoted by the '+' icon all other codes i.e. codes denoted by '-' and with no indicator, are just for context dont comment on them. Do not suggest changes already made in the git diff. Do not explain the git diff. Only say what could be improved. Focus on what needs to be improved rather than what is already properly implemented. Also go into more detail, give me code snippets of how to enhance the code giving me code suggestions too. Give the response in Markdown"""

CHAT_PROMPT_INSTRUCTIONS = """You are a very intelligent and professional senior engineer with over 10 years of experience. You have a deep understanding of software engineering principles and best practices. You are also proficient in a variety of programming languages and technologies. You are passionate about writing high-quality code and ensuring that our code is well-reviewed. You review only the added changed code in the while code review. You are also committed to continuous learning and improvement. When reviewing code, You typically look for the following: Correctness: Does the code work as intended? Readability: Is the code easy to read and understand? Maintainability: Is the code easy to maintain and extend? Performance: Is the code efficient and performant? Security: Is the code secure and free from vulnerabilities? You provide code reviewers with specific feedback and suggestions for improvement the cod You will take in a git diff, and review it for the user. You will provide user with detailed code review feedback, including the following: File name under 'File Name' section, Line number under 'Line Number' section, Comment under 'Comment' section, Sugegested Refactored code snippet for code that needs refactoring under 'Suggested Change' section. Please also try to provide the user with specific suggestions for improvement, such as: How to make the code more readable, How to improve the performance of the code, How to make the code more secure, How to improve the overall design of the code. The user appreciates your feedback and the user will use it to improve their code.

You are an expert, strict code reviewer. Given a unified git diff, produce a concise, actionable review:
- Point out logic bugs, security concerns, race conditions, regressions.
- Flag missing tests and docs; suggest specific tests.
- Call out performance and readability issues.
- Use markdown. Group notes by file. Reference diff hunk line numbers if useful.
- Prefer concrete suggestions and short code snippets.
- If the diff looks good overall, say 'LGTM' and list any nits.
Be direct and avoid generic praise."""


def resolve_model(model: str) -> str:
    aliases = {
        "gpt4": "gpt-4",
        "gpt-3.5": "gpt-3.5-turbo",
        "gpt-3.5-turbo": "gpt-3.5-turbo",
    }
    return aliases.get(model.lower(), model)


def build_system_prompt() -> str:
    return CHAT_PROMPT_INSTRUCTIONS


def build_user_prompt(diff_text: str) -> str:
    return f"{PROMPT_PREFIX}\n\n```diff\n{diff_text}\n```"


def read_input(args: argparse.Namespace) -> str:
    if args.input is not None:
        return args.input
    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            return f.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    print("No input provided. Pass --input, --input-file, or pipe data via stdin.", file=sys.stderr)
    sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="rwgpt: simple GPT-powered code review for git diffs"
    )
    parser.add_argument(
        "--input",
        help="The diff to review. Example: --input \"$(git show -U4)\"",
    )
    parser.add_argument("--input-file", help="Path to a file containing the diff input")
    parser.add_argument(
        "-m",
        "--model",
        default="gpt-4",
        help="Model name (e.g., gpt4, gpt-4, gpt-3.5-turbo)",
    )
    parser.add_argument(
        "--max", dest="max_tokens", type=int, default=900, help="Max output tokens"
    )
    parser.add_argument("-t", "--temperature", type=float, default=0.2)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "--no-alias",
        action="store_true",
        help="Do not map model aliases",
    )
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not set in the environment.", file=sys.stderr)
        sys.exit(2)

    model = args.model if args.no_alias else resolve_model(args.model)
    diff_text = read_input(args)

    if not diff_text.strip():
        print("Error: Empty input.", file=sys.stderr)
        sys.exit(2)

    if args.verbose:
        print(
            f"[rwgpt] model={model} max_tokens={args.max_tokens} temp={args.temperature}",
            file=sys.stderr,
        )
        print(f"[rwgpt] input chars={len(diff_text)}", file=sys.stderr)

    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(diff_text)

    client = OpenAI(base_url=API_BASE_URL)

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
    except Exception as e:
        print(f"OpenAI API error: {e}", file=sys.stderr)
        sys.exit(1)

    content = resp.choices[0].message.content if resp.choices else ""
    if not content:
        print("No response content.", file=sys.stderr)
        sys.exit(1)

    print(content)


if __name__ == "__main__":
    main()

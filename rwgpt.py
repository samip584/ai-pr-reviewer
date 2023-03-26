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


def resolve_model(model: str) -> str:
    aliases = {
        "gpt4": "gpt-4",
        "gpt-3.5": "gpt-3.5-turbo",
        "gpt-3.5-turbo": "gpt-3.5-turbo",
    }
    return aliases.get(model.lower(), model)


def build_user_prompt(diff_text: str) -> str:
    return f"Review this git diff and provide feedback:\n\n```diff\n{diff_text}\n```"


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

    user_prompt = build_user_prompt(diff_text)
    print(f"Ready to review with {model}!")
    print(f"Prompt preview: {user_prompt[:100]}...")


if __name__ == "__main__":
    main()

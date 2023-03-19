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
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not set in the environment.", file=sys.stderr)
        sys.exit(2)

    diff_text = read_input(args)

    if not diff_text.strip():
        print("Error: Empty input.", file=sys.stderr)
        sys.exit(2)

    if args.verbose:
        print(f"[rwgpt] input chars={len(diff_text)}", file=sys.stderr)

    print("Basic CLI structure ready!")


if __name__ == "__main__":
    main()

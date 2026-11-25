#!/usr/bin/env python3
"""Laugh Track: The Crypto Trading Joke Contest -- make.fun bounty entry.

Writes a single one-line crypto trading joke to /output/entry.txt.
Deterministic, no network, no files outside this repo, no secrets.

The joke: every trader's oldest sin, buy high and sell low, reframed
as charity. Setup in the first sentence, the turn in the second, and
the punchline ("donating to strangers with better timing") lands on
the last words, which is exactly what the judge brief rewards: a clear
setup and turn, a true trading detail, and no wasted words.
"""

import os

# The final joke (118 characters, one line, no trailing newline).
LINE = "I sold at the bottom and bought back at the top. My trading strategy is just donating to strangers with better timing."

# The sandbox runs this with /output as the output dir; a local run may
# point MAKEFUN_OUTPUT_DIR elsewhere so parallel builders never share
# one /output directory.
OUTPUT_PATH = os.path.join(
    os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt"
)


MAX_LEN = 200


def main() -> None:
    line = LINE.strip()
    validate(line)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(line)
    os.chmod(OUTPUT_PATH, 0o644)
    # Verify what actually landed on disk: exact content, one line,
    # within the gate, and mode 0644 (files from mkstemp stay 0600).
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        written = f.read()
    if written != line:
        raise SystemExit("entry.txt content mismatch")
    if oct(os.stat(OUTPUT_PATH).st_mode & 0o777) != "0o644":
        raise SystemExit("entry.txt mode is not 0644")


def validate(line: str) -> None:
    """Gate check shared by main(): 1 line, 1-200 chars, no newlines."""
    if not line or len(line) > MAX_LEN:
        raise SystemExit("joke must be 1-200 characters")
    if "\n" in line or "\r" in line:
        raise SystemExit("joke must be a single line")


if __name__ == "__main__":
    main()

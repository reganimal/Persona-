#!/usr/bin/env python3
"""Check that quotes appear verbatim in one or more transcript files.

Usage:
    python3 tools/quotecheck.py QUOTES_FILE TRANSCRIPT [TRANSCRIPT ...]

QUOTES_FILE holds one quote (or distinctive fragment) per line. Matching
ignores case and punctuation and collapses whitespace, which suits
auto-generated captions that have no punctuation.

Each line of output is OK or MISS, followed by the files that contain the
quote. The exit status is 1 if any quote is missing.
"""
import re
import sys
from pathlib import Path


def norm(text: str) -> str:
    text = text.lower().replace("’", "'")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    quotes_file, *transcripts = sys.argv[1:]
    texts = {Path(t).name: norm(Path(t).read_text(encoding="utf-8", errors="ignore")) for t in transcripts}
    missing = 0
    for line in Path(quotes_file).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        hits = [name for name, body in texts.items() if norm(line) in body]
        missing += not hits
        print(f"{'OK  ' if hits else 'MISS'} {hits} {line}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Check that every persona in the repository is complete and consistent.

Usage:
    python3 tools/checkpersona.py [--strict] [--root DIR] [NAME ...]

With no NAME, every folder under personas/ is checked, except folders whose
name starts with "_" (such as _template).

Checks for each persona:
  files     personas/<name>/profile.md and system-prompt.md exist.
  sources   Every [Sn] cited in profile.md is defined once in its Sources
            section as "**[Sn]**". A source that is defined but never cited
            is a warning.
  quotes    Every line under the system prompt's "Verified lines" heading
            appears in profile.md. Matching ignores case and punctuation, as
            in quotecheck.py, and a quote shortened with "…" is checked
            fragment by fragment. This catches a prompt that has drifted
            from the fact-checked dossier.
  agent     .claude/agents/<name>.md exists, its front matter has
            name: <name>, and it loads personas/<name>/system-prompt.md.
  readme    README.md links to personas/<name>/.

Each problem is printed as ERROR or WARN. The exit status is 1 if there is
any error (or any warning, with --strict), and 0 otherwise.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from quotecheck import norm  # noqa: E402

CITE_RE = re.compile(r"\[S(\d+)\]")
SOURCE_DEF_RE = re.compile(r"^\s*[-*]\s+\*\*\[S(\d+)\]\*\*", re.MULTILINE)
SOURCES_HEADING_RE = re.compile(r"^#{2,}\s+(?:\d+\.\s+)?Sources\b.*$", re.MULTILINE | re.IGNORECASE)
QUOTES_HEADING_RE = re.compile(r"^#{2,}\s+Verified (?:lines|quotes)\b.*$", re.MULTILINE | re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s", re.MULTILINE)
QUOTE_RE = re.compile(r"[\"“]([^\"”]+)[\"”]")
ELLIPSIS_RE = re.compile(r"…|\.\.\.")
# Quote fragments shorter than this many words are too generic to check.
MIN_FRAGMENT_WORDS = 3


@dataclass
class Problem:
    level: str  # "ERROR" or "WARN"
    persona: str
    check: str
    message: str

    def __str__(self) -> str:
        return f"{self.level:<5} {self.persona} [{self.check}] {self.message}"


def section(text: str, heading_re: re.Pattern) -> str | None:
    """Return the body under the first heading that matches, up to the next heading."""
    match = heading_re.search(text)
    if not match:
        return None
    rest = text[match.end():]
    nxt = HEADING_RE.search(rest)
    return rest[: nxt.start()] if nxt else rest


def check_sources(name: str, profile: str) -> list[Problem]:
    problems = []
    sources = section(profile, SOURCES_HEADING_RE)
    if sources is None:
        return [Problem("ERROR", name, "sources", "profile.md has no Sources section")]

    defined: dict[int, int] = {}
    for m in SOURCE_DEF_RE.finditer(sources):
        n = int(m.group(1))
        defined[n] = defined.get(n, 0) + 1
    for n, count in sorted(defined.items()):
        if count > 1:
            problems.append(Problem("ERROR", name, "sources", f"[S{n}] is defined {count} times"))

    body = profile.replace(sources, "")
    cited = {int(n) for n in CITE_RE.findall(body)}
    for n in sorted(cited - defined.keys()):
        problems.append(Problem("ERROR", name, "sources", f"[S{n}] is cited but not defined in Sources"))
    for n in sorted(defined.keys() - cited):
        problems.append(Problem("WARN", name, "sources", f"[S{n}] is defined but never cited"))
    return problems


def quote_fragments(line: str) -> list[str]:
    """Split a quote line into the fragments that must each appear in the dossier."""
    quoted = QUOTE_RE.findall(line)
    text_parts = quoted if quoted else [line.strip().lstrip("-*").strip()]
    fragments = []
    for part in text_parts:
        for frag in ELLIPSIS_RE.split(part):
            if len(norm(frag).split()) >= MIN_FRAGMENT_WORDS:
                fragments.append(frag.strip())
    return fragments


def check_quotes(name: str, prompt: str, profile: str) -> list[Problem]:
    quotes = section(prompt, QUOTES_HEADING_RE)
    if quotes is None:
        return [Problem("WARN", name, "quotes", "system-prompt.md has no \"Verified lines\" section")]
    dossier = norm(profile)
    problems = []
    for line in quotes.splitlines():
        if not line.strip().startswith(("-", "*")):
            continue
        for frag in quote_fragments(line):
            if norm(frag) not in dossier:
                problems.append(Problem("ERROR", name, "quotes", f"not found in profile.md: {frag!r}"))
    return problems


def check_agent(name: str, root: Path) -> list[Problem]:
    path = root / ".claude" / "agents" / f"{name}.md"
    if not path.is_file():
        return [Problem("ERROR", name, "agent", f"missing {path.relative_to(root)}")]
    text = path.read_text(encoding="utf-8")
    problems = []
    front = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    declared = re.search(r"^name:\s*(\S+)\s*$", front.group(1), re.MULTILINE) if front else None
    if not declared:
        problems.append(Problem("ERROR", name, "agent", "front matter has no name: field"))
    elif declared.group(1) != name:
        problems.append(Problem("ERROR", name, "agent", f"front matter says name: {declared.group(1)}, expected {name}"))
    if f"personas/{name}/system-prompt.md" not in text:
        problems.append(Problem("ERROR", name, "agent", f"does not load personas/{name}/system-prompt.md"))
    return problems


def check_readme(name: str, root: Path) -> list[Problem]:
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    if f"(personas/{name}/)" not in text and f"(personas/{name})" not in text:
        return [Problem("ERROR", name, "readme", f"README.md does not link to personas/{name}/")]
    return []


def check_persona(name: str, root: Path) -> list[Problem]:
    folder = root / "personas" / name
    if not folder.is_dir():
        return [Problem("ERROR", name, "files", f"no folder personas/{name}/")]
    problems = []
    files = {}
    for fname in ("profile.md", "system-prompt.md"):
        path = folder / fname
        if path.is_file():
            files[fname] = path.read_text(encoding="utf-8")
        else:
            problems.append(Problem("ERROR", name, "files", f"missing personas/{name}/{fname}"))
    if "profile.md" in files:
        problems += check_sources(name, files["profile.md"])
        if "system-prompt.md" in files:
            problems += check_quotes(name, files["system-prompt.md"], files["profile.md"])
    problems += check_agent(name, root)
    problems += check_readme(name, root)
    return problems


def find_personas(root: Path) -> list[str]:
    base = root / "personas"
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir() and not p.name.startswith("_"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="personas to check (default: all)")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="repository root (default: the folder above tools/)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)

    names = args.names or find_personas(args.root)
    if not names:
        print("No personas found.")
        return 1
    problems = [p for name in names for p in check_persona(name, args.root)]
    for p in problems:
        print(p)
    errors = sum(p.level == "ERROR" for p in problems)
    warnings = len(problems) - errors
    print(f"Checked {len(names)} persona(s): {errors} error(s), {warnings} warning(s).")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())

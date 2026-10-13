#!/usr/bin/env python3
"""
Validate an llms.txt file against Webflow's platform limits and the llms.txt spec.

Checks:
  - UTF-8 decodable
  - Under Webflow's 100 KB ceiling
  - Character hygiene (no smart punctuation, entities or replacement characters)
  - Structure (H1, summary blockquote, free-text overview, parseable entries)

Usage:
    python validate_llms_txt.py llms.txt
    python validate_llms_txt.py llms.txt --allow-punctuation
    python validate_llms_txt.py llms.txt --quiet

Exit codes:
    0  no errors (warnings may still be printed)
    1  one or more errors
    2  file could not be read
"""

import argparse
import re
import sys
from pathlib import Path

MAX_BYTES = 100 * 1024

# Characters that survive badly when this file's content is re-escaped downstream,
# for example when lifted into a JSON-LD script block.
STRICT_CHARS = {
    "em dash": "—",
    "en dash": "–",
    "left single quote": "‘",
    "right single quote": "’",
    "left double quote": "“",
    "right double quote": "”",
    "non-breaking space": " ",
    "ellipsis": "…",
}

# Downgraded to warnings with --allow-punctuation.
RELAXABLE_CHARS = {
    "apostrophe": "'",
    "ampersand": "&",
}

ENTRY_RE = re.compile(r"^- \[(?P<title>.*?)\]\((?P<url>[^)]*)\)(?::\s*(?P<desc>.*))?$")
ENTITY_RE = re.compile(r"&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]{1,31});")


class Report:
    def __init__(self, quiet: bool = False) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []
        self.quiet = quiet

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def render(self) -> int:
        if not self.quiet:
            for note in self.notes:
                print(f"       {note}")
        for warning in self.warnings:
            print(f"WARN   {warning}")
        for error in self.errors:
            print(f"FAIL   {error}")
        if not self.errors:
            print("PASS   no errors")
        return 1 if self.errors else 0


def check_encoding_and_size(path: Path, report: Report) -> str | None:
    raw = path.read_bytes()
    size = len(raw)

    if size > MAX_BYTES:
        report.error(
            f"file is {size} bytes, over Webflow's {MAX_BYTES} byte (100 KB) limit"
        )
    else:
        pct = (size / MAX_BYTES) * 100
        report.note(f"size {size} bytes ({pct:.1f}% of the 100 KB limit)")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        report.error(f"file is not valid UTF-8: {exc}")
        return None

    report.note("encoding utf-8")
    return text


def check_characters(text: str, report: Report, allow_punctuation: bool) -> None:
    for name, char in STRICT_CHARS.items():
        count = text.count(char)
        if count:
            report.error(f"{count} x {name} ({char!r}) — write around it")

    for name, char in RELAXABLE_CHARS.items():
        count = text.count(char)
        if not count:
            continue
        msg = f"{count} x {name} ({char!r}) — escapes badly in downstream JSON-LD"
        if allow_punctuation:
            report.warn(msg)
        else:
            report.error(msg)

    replacements = text.count("�")
    if replacements:
        report.error(
            f"{replacements} x replacement character (U+FFFD) — something upstream "
            "had an encoding bug"
        )

    entities = ENTITY_RE.findall(text)
    if entities:
        unique = ", ".join(sorted(set(entities))[:5])
        report.error(f"{len(entities)} x HTML entity in the text ({unique})")

    for i, line in enumerate(text.splitlines(), 1):
        if line != line.rstrip():
            report.warn(f"line {i} has trailing whitespace")


def check_structure(text: str, report: Report) -> None:
    lines = text.splitlines()

    if not text.endswith("\n"):
        report.warn("file does not end with a newline")

    h1_index = next((i for i, ln in enumerate(lines) if ln.strip()), 0)
    if not lines[h1_index:h1_index + 1] or not lines[h1_index].startswith("# "):
        report.error("no H1 on the first non-empty line — the spec requires one")

    if not any(ln.startswith("> ") for ln in lines):
        report.warn("no '>' summary line under the H1")

    first_section = next(
        (i for i, ln in enumerate(lines) if ln.startswith("## ")), len(lines)
    )
    body = lines[h1_index + 1:first_section]
    overview = [
        ln
        for ln in body
        if ln.strip() and not ln.startswith(">") and not ln.startswith("#")
    ]
    if not overview:
        report.warn(
            "no free-text overview block between the summary line and the first "
            "section — this is the highest-value part of the file"
        )

    # A heading inside the overview block would terminate it per the spec.
    for offset, line in enumerate(body):
        if line.startswith("#"):
            report.error(
                f"line {h1_index + 2 + offset} is a heading inside the overview "
                "block — the spec allows any section type except headings there"
            )

    sections = [ln[3:].strip() for ln in lines if ln.startswith("## ")]
    if not sections:
        report.warn("no '##' sections — the file contains no link lists")
    if "Optional" in sections and sections[-1] != "Optional":
        report.warn("'## Optional' is not the last section")

    entries = 0
    for i, line in enumerate(lines, 1):
        if not line.startswith("- "):
            continue
        entries += 1
        match = ENTRY_RE.match(line)
        if not match:
            report.error(f"line {i} does not parse as an entry: {line[:70]}")
            continue

        url = match.group("url")
        desc = match.group("desc")

        if not url.startswith("http"):
            report.error(f"line {i} URL is not absolute: {url}")
        if url.endswith(".md"):
            report.error(
                f"line {i} URL ends in .md — Webflow does not serve markdown variants"
            )
        if not desc:
            report.warn(f"line {i} has no description: {url}")
        elif len(desc) > 300:
            report.warn(f"line {i} description is {len(desc)} characters, very long")

    report.note(f"{entries} entries across {len(sections)} sections")

    seen: dict[str, int] = {}
    for i, line in enumerate(lines, 1):
        match = ENTRY_RE.match(line) if line.startswith("- ") else None
        if not match:
            continue
        url = match.group("url")
        if url in seen:
            report.warn(f"line {i} duplicates the URL on line {seen[url]}: {url}")
        else:
            seen[url] = i


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("path", help="path to the llms.txt file")
    parser.add_argument(
        "--allow-punctuation",
        action="store_true",
        help="downgrade apostrophes and ampersands from errors to warnings",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="suppress informational notes"
    )
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print(f"FAIL   file not found: {path}")
        return 2

    report = Report(quiet=args.quiet)
    text = check_encoding_and_size(path, report)
    if text is not None:
        check_characters(text, report, args.allow_punctuation)
        check_structure(text, report)

    return report.render()


if __name__ == "__main__":
    sys.exit(main())

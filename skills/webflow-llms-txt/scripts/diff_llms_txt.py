#!/usr/bin/env python3
"""
Diff two llms.txt files and report what changed.

Entries are matched on URL. A changed slug surfaces as one addition plus one
removal, so entries whose titles match across those two lists are re-paired and
reported as a single URL change instead.

Usage:
    python diff_llms_txt.py previous-llms.txt llms.txt
    python diff_llms_txt.py previous-llms.txt llms.txt --format text

Exit codes:
    0  parsed successfully (whether or not anything changed)
    2  a file could not be read
"""

import argparse
import json
import re
import sys
from pathlib import Path

ENTRY_RE = re.compile(r"^- \[(?P<title>.*?)\]\((?P<url>[^)]*)\)(?::\s*(?P<desc>.*))?$")


def parse(path: Path) -> dict[str, dict]:
    """Map URL -> {section, title, desc}."""
    entries: dict[str, dict] = {}
    section = None
    subsection = None

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            subsection = None
            continue
        if line.startswith("### "):
            subsection = line[4:].strip()
            continue
        if not line.startswith("- "):
            continue

        match = ENTRY_RE.match(line)
        if not match or section is None:
            continue

        label = f"{section} > {subsection}" if subsection else section
        entries[match.group("url")] = {
            "section": label,
            "title": match.group("title"),
            "desc": (match.group("desc") or "").strip(),
        }

    return entries


def truncate(text: str, words: int = 15) -> str:
    parts = text.split()
    if len(parts) <= words:
        return text
    return " ".join(parts[:words]) + "..."


def build_diff(old: dict[str, dict], new: dict[str, dict]) -> dict:
    added = [{"url": u, **new[u]} for u in new if u not in old]
    removed = [{"url": u, **old[u]} for u in old if u not in new]

    # Re-pair slug changes: same title, different URL.
    repaired = []
    removed_by_title = {entry["title"]: entry for entry in removed}
    for entry in list(added):
        match = removed_by_title.get(entry["title"])
        if not match:
            continue
        repaired.append(
            {
                "title": entry["title"],
                "section": entry["section"],
                "old_url": match["url"],
                "new_url": entry["url"],
                "desc_changed": match["desc"] != entry["desc"],
            }
        )
        added.remove(entry)
        removed.remove(match)
        del removed_by_title[entry["title"]]

    changed = []
    for url in new:
        if url not in old:
            continue
        before, after = old[url], new[url]
        if before["title"] == after["title"] and before["desc"] == after["desc"]:
            continue
        record = {"url": url, "section": after["section"]}
        if before["title"] != after["title"]:
            record["title"] = [before["title"], after["title"]]
        if before["desc"] != after["desc"]:
            record["desc"] = [truncate(before["desc"]), truncate(after["desc"])]
        changed.append(record)

    moved = [
        {
            "url": url,
            "title": new[url]["title"],
            "section": [old[url]["section"], new[url]["section"]],
        }
        for url in new
        if url in old and old[url]["section"] != new[url]["section"]
    ]

    return {
        "counts": {
            "previous": len(old),
            "current": len(new),
            "added": len(added),
            "removed": len(removed),
            "url_changed": len(repaired),
            "updated": len(changed),
            "moved": len(moved),
        },
        "added": added,
        "removed": removed,
        "repaired": repaired,
        "changed": changed,
        "moved": moved,
    }


def render_text(diff: dict) -> str:
    out: list[str] = []
    counts = diff["counts"]
    out.append(
        f"{counts['previous']} entries previously, {counts['current']} now.\n"
    )

    if diff["added"]:
        out.append("Added")
        for entry in diff["added"]:
            out.append(f"  - [{entry['title']}]({entry['url']}) - {entry['section']}")
        out.append("")

    if diff["removed"]:
        out.append("Removed")
        for entry in diff["removed"]:
            out.append(
                f"  - [{entry['title']}]({entry['url']}) - was in {entry['section']}"
            )
        out.append("")

    if diff["repaired"]:
        out.append("URL changed")
        for entry in diff["repaired"]:
            out.append(
                f"  - {entry['title']} - {entry['old_url']} -> {entry['new_url']}"
            )
        out.append("")

    if diff["changed"]:
        out.append("Updated")
        for entry in diff["changed"]:
            if "title" in entry:
                out.append(
                    f"  - title: {entry['title'][0]} -> {entry['title'][1]}"
                )
            if "desc" in entry:
                out.append(f"  - {entry['url']}")
                out.append(f"      was: {entry['desc'][0]}")
                out.append(f"      now: {entry['desc'][1]}")
        out.append("")

    if diff["moved"]:
        out.append("Moved between sections")
        for entry in diff["moved"]:
            out.append(
                f"  - {entry['title']}: {entry['section'][0]} -> {entry['section'][1]}"
            )
        out.append("")

    if len(out) == 1:
        out.append("No changes.")

    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("previous", help="the previous llms.txt")
    parser.add_argument("current", help="the newly generated llms.txt")
    parser.add_argument(
        "--format", choices=["json", "text"], default="json", help="output format"
    )
    args = parser.parse_args()

    previous, current = Path(args.previous), Path(args.current)
    for path in (previous, current):
        if not path.is_file():
            print(f"file not found: {path}", file=sys.stderr)
            return 2

    diff = build_diff(parse(previous), parse(current))

    if args.format == "json":
        print(json.dumps(diff, indent=2))
    else:
        print(render_text(diff))

    return 0


if __name__ == "__main__":
    sys.exit(main())

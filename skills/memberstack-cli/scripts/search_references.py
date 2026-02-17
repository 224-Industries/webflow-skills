#!/usr/bin/env python3
"""
Search Memberstack CLI reference files.
Usage:
    python3 search_references.py --list
    python3 search_references.py --tag <tag>
    python3 search_references.py --search <query>
"""

import sys
import re
from pathlib import Path


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown text. Returns (metadata, body)."""
    if not text.startswith("---"):
        return {}, text

    end = text.find("---", 3)
    if end == -1:
        return {}, text

    raw = text[3:end].strip()
    body = text[end + 3:].strip()
    metadata = {}

    for line in raw.splitlines():
        match = re.match(r'^(\w+):\s*(.+)$', line)
        if not match:
            continue
        key = match.group(1)
        value = match.group(2).strip()

        # Strip surrounding quotes
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]

        # Parse inline YAML list: [a, b, c]
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip('"').strip("'")
                     for item in value[1:-1].split(",")]
            value = [item for item in items if item]

        metadata[key] = value

    return metadata, body


def load_references() -> list[dict]:
    """Load all reference files from the references directory."""
    script_dir = Path(__file__).resolve().parent
    refs_dir = script_dir / ".." / "references"
    refs_dir = refs_dir.resolve()

    if not refs_dir.is_dir():
        print(f"References directory not found: {refs_dir}")
        sys.exit(1)

    results = []
    reference_files = sorted(list(refs_dir.glob("*.md")))

    for md_file in reference_files:
        text = md_file.read_text()
        metadata, body = parse_frontmatter(text)
        results.append({
            "file": str(md_file),
            "name": metadata.get("name", md_file.stem),
            "description": metadata.get("description", ""),
            "tags": metadata.get("tags", []),
            "body": body,
        })

    return results


def print_ref(ref: dict) -> None:
    """Print a single reference entry."""
    tags = ref["tags"]
    tag_str = ", ".join(tags) if isinstance(tags, list) else str(tags)
    print(f"  Name:        {ref['name']}")
    print(f"  Description: {ref['description']}")
    print(f"  Tags:        {tag_str}")
    print(f"  File:        {ref['file']}")
    print()


def cmd_list(refs: list[dict]) -> None:
    """List all references."""
    print(f"Found {len(refs)} reference files:\n")
    for ref in refs:
        print_ref(ref)


def cmd_tag(refs: list[dict], tag: str) -> None:
    """Search references by tag (exact match)."""
    tag_lower = tag.lower()
    matches = [r for r in refs if tag_lower in
               [t.lower() for t in r["tags"]] if isinstance(r["tags"], list)]

    if not matches:
        print(f"No references found with tag: {tag}")
        return

    print(f"Found {len(matches)} reference(s) matching tag '{tag}':\n")
    for ref in matches:
        print_ref(ref)


def cmd_search(refs: list[dict], query: str) -> None:
    """Search references by keyword across name, description, tags, and body."""
    query_lower = query.lower()
    matches = []

    for ref in refs:
        tag_str = " ".join(ref["tags"]) if isinstance(ref["tags"], list) else str(ref["tags"])
        searchable = " ".join([
            ref["name"],
            ref["description"],
            tag_str,
            ref["body"],
        ]).lower()

        if query_lower in searchable:
            matches.append(ref)

    if not matches:
        print(f"No references found matching: {query}")
        return

    print(f"Found {len(matches)} reference(s) matching '{query}':\n")
    for ref in matches:
        print_ref(ref)


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    refs = load_references()
    arg = sys.argv[1]

    if arg == "--list":
        cmd_list(refs)
    elif arg == "--tag":
        if len(sys.argv) < 3:
            print("Usage: search_references.py --tag <tag>")
            sys.exit(1)
        cmd_tag(refs, sys.argv[2])
    elif arg == "--search":
        if len(sys.argv) < 3:
            print("Usage: search_references.py --search <query>")
            sys.exit(1)
        cmd_search(refs, sys.argv[2])
    else:
        print(f"Unknown argument: {arg}")
        print(__doc__.strip())
        sys.exit(1)


if __name__ == "__main__":
    main()

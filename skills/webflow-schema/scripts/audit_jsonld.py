#!/usr/bin/env python3
"""
Audit the JSON-LD a live page actually ships.

Fetches each URL, parses every application/ld+json block, and reports:
parse failures, unresolved Webflow binding tokens, HTML entities, empty values,
relative URLs, non-ISO dates and durations, self-serving reviews, and schema
types that appear more than once on the page.

Usage:
    python audit_jsonld.py URL [URL ...]
    python audit_jsonld.py --file page.html

Exit code is 1 if any page has a problem, otherwise 0.
"""

import json
import re
import sys
import urllib.request

SCRIPT_RE = re.compile(
    r"<script[^>]*type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>",
    re.IGNORECASE | re.DOTALL,
)
ENTITY_RE = re.compile(r"&#?\w+;")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$")
ISO_DURATION_RE = re.compile(r"^P(?=\d|T\d)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(\d+H)?(\d+M)?(\d+(\.\d+)?S)?)?$")
URL_KEYS = {"url", "item", "@id", "image", "logo", "sameAs"}
DATE_KEYS = {"datePublished", "dateModified", "dateCreated", "uploadDate", "startDate", "endDate"}
DURATION_KEYS = {"timeRequired", "duration", "totalTime", "cookTime", "prepTime"}
REVIEW_KEYS = {"review", "aggregateRating"}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (schema audit)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def walk(node, path, found):
    """Collect problems from a parsed JSON-LD node."""
    if isinstance(node, dict):
        types = node.get("@type")
        if types:
            for t in types if isinstance(types, list) else [types]:
                found["types"].append(t)
        for key, value in node.items():
            here = f"{path}.{key}" if path else key
            if key in REVIEW_KEYS:
                found["problems"].append(f"review markup at {here} (self-serving reviews earn no rich results)")
            if isinstance(value, str):
                check_string(key, value, here, found)
            else:
                walk(value, here, found)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            here = f"{path}[{i}]"
            if isinstance(item, str):
                check_string(path.rsplit(".", 1)[-1], item, here, found)
            else:
                walk(item, here, found)


def check_string(key, value, here, found):
    v = value.strip()
    if v == "":
        found["problems"].append(f"empty value at {here}")
        return
    if "{{wf" in v:
        found["problems"].append(f"unresolved binding token at {here}")
    entities = ENTITY_RE.findall(v)
    if entities:
        found["problems"].append(f"HTML entities {sorted(set(entities))} at {here}: {v[:80]!r}")
    if key in URL_KEYS and not v.startswith(("https://", "http://")):
        found["problems"].append(f"relative or invalid URL at {here}: {v[:80]!r}")
    if key in DATE_KEYS and not ISO_DATE_RE.match(v):
        found["problems"].append(f"non-ISO date at {here}: {v!r}")
    if key in DURATION_KEYS and not ISO_DURATION_RE.match(v):
        found["problems"].append(f"non-ISO duration at {here}: {v!r} (use a form like PT10M)")


def audit(label, html):
    blocks = SCRIPT_RE.findall(html)
    print(f"\n== {label}")
    print(f"   JSON-LD blocks found: {len(blocks)}")
    found = {"types": [], "problems": []}
    for n, raw in enumerate(blocks, 1):
        raw = raw.strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            found["problems"].append(f"block {n} does not parse: {exc}")
            if "{{wf" in raw:
                found["problems"].append(f"block {n} contains unresolved binding tokens")
            continue
        walk(data, f"block{n}", found)

    counts = {}
    for t in found["types"]:
        counts[t] = counts.get(t, 0) + 1
    if counts:
        print("   types: " + ", ".join(f"{t} x{c}" if c > 1 else t for t, c in sorted(counts.items())))
    for t, c in sorted(counts.items()):
        if c > 1 and t in {"FAQPage", "Article", "BlogPosting", "BreadcrumbList", "ItemList", "Organization", "WebPage"}:
            found["problems"].append(f"{t} appears {c} times (check for a template binding plus a hand-embedded block)")

    if found["problems"]:
        for p in found["problems"]:
            print(f"   PROBLEM: {p}")
    else:
        print("   OK: no problems found")
    return bool(found["problems"])


def main(argv):
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__)
        return 0
    bad = False
    if argv[0] == "--file":
        for path in argv[1:]:
            with open(path, encoding="utf-8", errors="replace") as fh:
                bad |= audit(path, fh.read())
    else:
        for url in argv:
            try:
                bad |= audit(url, fetch(url))
            except Exception as exc:  # network errors are reported, not raised
                print(f"\n== {url}\n   ERROR: could not fetch ({exc})")
                bad = True
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

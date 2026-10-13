#!/usr/bin/env python3
"""
Check text before it is bound into Webflow's JSON-LD field.

Webflow HTML-escapes bound CMS values, so a straight apostrophe, straight
double quote or ampersand renders as &#39;, &quot; or &amp; in the schema.
This script flags those characters and suggests the safe form.

Usage:
    python check_bindable_text.py --csv export.csv [--columns col1,col2]
    python check_bindable_text.py --file values.txt
    echo "It's here" | python check_bindable_text.py

With --csv, every cell is checked unless --columns names the fields to check
(use the column headers from a Webflow CMS CSV export).

Exit code is 1 if anything needs fixing, otherwise 0.
"""

import csv
import sys

UNSAFE = {
    "'": "straight apostrophe, use ’ (smart apostrophe)",
    '"': "straight double quote, use “ ” (smart quotes)",
    "&": "ampersand, spell it 'and'",
}


def check(label, text):
    issues = [(ch, why) for ch, why in UNSAFE.items() if ch in text]
    if "&#" in text or "&amp;" in text or "&quot;" in text:
        issues.append(("&...;", "already contains an HTML entity, replace it with the plain character"))
    for ch, why in issues:
        print(f"{label}: {why}\n    {text[:120]!r}")
    return bool(issues)


def main(argv):
    if argv and argv[0] in {"-h", "--help"}:
        print(__doc__)
        return 0
    bad = False
    if argv and argv[0] == "--csv":
        path = argv[1]
        columns = None
        if "--columns" in argv:
            columns = [c.strip() for c in argv[argv.index("--columns") + 1].split(",")]
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            for row_no, row in enumerate(reader, 2):
                for col, value in row.items():
                    if columns and col not in columns:
                        continue
                    if value and check(f"row {row_no}, {col}", value):
                        bad = True
    else:
        source = open(argv[1], encoding="utf-8") if argv and argv[0] == "--file" else sys.stdin
        for line_no, line in enumerate(source, 1):
            line = line.rstrip("\n")
            if line and check(f"line {line_no}", line):
                bad = True
    if not bad:
        print("OK: nothing will be escaped")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

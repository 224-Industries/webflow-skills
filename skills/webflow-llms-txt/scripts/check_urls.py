#!/usr/bin/env python3
"""
HEAD-check every URL in an llms.txt file and report anything that is not a 200.

A 301 usually means a slug changed or the wrong host variant was used — follow it
and emit the destination URL instead. A 404 means the page is gone — drop it from
the file. Never ship a URL you know is broken.

Usage:
    python check_urls.py llms.txt
    python check_urls.py llms.txt --workers 4 --timeout 20
    python check_urls.py llms.txt --failures-only
    python check_urls.py llms.txt --json

Exit codes:
    0  every URL returned 200
    1  one or more URLs did not
    2  file could not be read
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ENTRY_RE = re.compile(r"^- \[(?P<title>.*?)\]\((?P<url>[^)]*)\)")
USER_AGENT = "webflow-llms-txt-checker/1.0 (+https://github.com/224-industries/webflow-skills)"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Report redirects rather than following them silently."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def extract_urls(text: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    seen: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        match = ENTRY_RE.match(line)
        if not match:
            continue
        url = match.group("url")
        if url.startswith("http") and url not in seen:
            seen.add(url)
            found.append((match.group("title"), url))
    return found


def probe(url: str, timeout: int, method: str = "HEAD") -> dict:
    request = urllib.request.Request(
        url, method=method, headers={"User-Agent": USER_AGENT}
    )
    try:
        with OPENER.open(request, timeout=timeout) as response:
            return {"status": response.status, "location": None}
    except urllib.error.HTTPError as exc:
        # Some servers reject HEAD outright. Retry once with GET before believing it.
        if exc.code in (403, 405, 501) and method == "HEAD":
            return probe(url, timeout, method="GET")
        return {"status": exc.code, "location": exc.headers.get("Location")}
    except urllib.error.URLError as exc:
        return {"status": None, "location": None, "error": str(exc.reason)}
    except Exception as exc:  # noqa: BLE001 - a bad URL should not kill the run
        return {"status": None, "location": None, "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("path", help="path to the llms.txt file")
    parser.add_argument("--workers", type=int, default=4, help="concurrent requests")
    parser.add_argument("--timeout", type=int, default=15, help="seconds per request")
    parser.add_argument(
        "--failures-only", action="store_true", help="print only non-200 results"
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print(f"file not found: {path}", file=sys.stderr)
        return 2

    urls = extract_urls(path.read_text(encoding="utf-8"))
    if not urls:
        print("no URLs found in the file", file=sys.stderr)
        return 2

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        probes = list(
            pool.map(lambda pair: probe(pair[1], args.timeout), urls)
        )

    results = [
        {"title": title, "url": url, **result}
        for (title, url), result in zip(urls, probes)
    ]
    failures = [r for r in results if r["status"] != 200]

    if args.json:
        print(json.dumps({"checked": len(results), "results": results}, indent=2))
    else:
        for result in results:
            if args.failures_only and result["status"] == 200:
                continue
            status = result["status"] or "ERR"
            line = f"{status:>4}  {result['url']}"
            if result.get("location"):
                line += f"\n      -> {result['location']}"
            if result.get("error"):
                line += f"\n      {result['error']}"
            print(line)

        print(
            f"\n{len(results)} checked, {len(results) - len(failures)} ok, "
            f"{len(failures)} to fix"
        )

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

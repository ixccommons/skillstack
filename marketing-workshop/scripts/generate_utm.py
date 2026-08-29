#!/usr/bin/env python3
"""Deterministic UTM link generator.

    python3 marketing-workshop/scripts/generate_utm.py "https://example.com/pricing" \
        --source newsletter --medium email --campaign launch-2026-08 \
        --content top-cta --term "b2b saas"

Rules:

  - non-UTM query parameters already on the URL are preserved, in their
    original order
  - an existing utm_* parameter is replaced, never duplicated
  - values are percent-encoded
  - UTM parameters are always emitted in the same order (source, medium,
    campaign, content, term), so the same inputs always produce the same
    string — useful for diffing campaign-plan.csv over time
  - a URL with no scheme or no host is rejected with ValueError

Standard library only.
"""

import argparse
import sys
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

UTM_ORDER = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"]
UTM_KEY_FOR = {
    "source": "utm_source",
    "medium": "utm_medium",
    "campaign": "utm_campaign",
    "content": "utm_content",
    "term": "utm_term",
}


def validate_url(url):
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https"):
        raise ValueError(f"invalid URL (missing or unsupported scheme): {url!r}")
    if not parts.netloc:
        raise ValueError(f"invalid URL (missing host): {url!r}")
    return parts


def build_utm_url(url, source=None, medium=None, campaign=None, content=None, term=None):
    parts = validate_url(url)

    existing = parse_qsl(parts.query, keep_blank_values=True)
    kept = [(k, v) for k, v in existing if k not in UTM_ORDER]

    values = {
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": campaign,
        "utm_content": content,
        "utm_term": term,
    }
    utm_pairs = [(key, values[key]) for key in UTM_ORDER if values[key] is not None]

    query = urlencode(kept + utm_pairs)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, query, parts.fragment))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Deterministic UTM link generator")
    parser.add_argument("url")
    parser.add_argument("--source")
    parser.add_argument("--medium")
    parser.add_argument("--campaign")
    parser.add_argument("--content")
    parser.add_argument("--term")
    args = parser.parse_args(argv)

    try:
        result = build_utm_url(
            args.url,
            source=args.source,
            medium=args.medium,
            campaign=args.campaign,
            content=args.content,
            term=args.term,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())

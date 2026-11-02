#!/usr/bin/env python3
"""Read RSS 2.0 or Atom feeds and list their posts."""
import argparse
import os
import urllib.request
import xml.etree.ElementTree as ET

ATOM = "{http://www.w3.org/2005/Atom}"

def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "rss-feed-reader/1.0"})
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read()

def parse_feed(data: bytes):
    """Return a list of dicts with title, link, published for RSS or Atom."""
    root = ET.fromstring(data)
    posts = []
    if root.tag.lower().endswith("rss") or root.find("channel") is not None:
        channel = root.find("channel") if root.find("channel") is not None else root
        for item in channel.findall("item"):
            posts.append({
                "title": (item.findtext("title") or "(no title)").strip(),
                "link": (item.findtext("link") or "").strip(),
                "published": (item.findtext("pubDate") or "").strip(),
            })
    elif root.tag == f"{ATOM}feed":
        for entry in root.findall(f"{ATOM}entry"):
            link = ""
            for candidate in entry.findall(f"{ATOM}link"):
                if candidate.get("rel", "alternate") == "alternate":
                    link = candidate.get("href", "")
                    break
            posts.append({
                "title": (entry.findtext(f"{ATOM}title") or "(no title)").strip(),
                "link": link,
                "published": (entry.findtext(f"{ATOM}updated") or "").strip(),
            })
    else:
        raise ValueError("not an RSS or Atom feed")
    return posts

RSS_SAMPLE = b"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>Demo Feed</title>
<item><title>First post</title><link>https://example.com/1</link><pubDate>Mon, 02 Nov 2026 09:00:00 GMT</pubDate></item>
<item><title>Second post</title><link>https://example.com/2</link><pubDate>Sun, 01 Nov 2026 12:00:00 GMT</pubDate></item>
</channel></rss>"""

ATOM_SAMPLE = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>Demo Atom</title>
<entry><title>Atom entry</title><link href="https://example.com/a"/><updated>2026-11-02T10:00:00Z</updated></entry>
</feed>"""

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url")
    parser.add_argument("--file")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for label, data in (("RSS", RSS_SAMPLE), ("Atom", ATOM_SAMPLE)):
            posts = parse_feed(data)
            print(f"{label}: {len(posts)} post(s)")
            for post in posts:
                print(f"  {post['published']:<31} {post['title']}  {post['link']}")
        return

    if args.url:
        data = fetch(args.url)
    elif args.file:
        with open(args.file, "rb") as fh:
            data = fh.read()
    else:
        raise SystemExit("provide --url, --file, or --demo")
    try:
        posts = parse_feed(data)
    except (ET.ParseError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}")
    for post in posts[:args.limit]:
        print(f"{post['published']:<31} {post['title']}  {post['link']}")

if __name__ == "__main__":
    main()

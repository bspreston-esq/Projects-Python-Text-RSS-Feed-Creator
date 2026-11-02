# RSS Feed Creator

**Category:** Text

## Problem

Given a link to RSS/Atom Feed, get all posts and display them.

## Solution

Fetches the feed with `urllib`, parses it with `xml.etree.ElementTree`, and normalizes RSS 2.0 `<item>` and Atom `<entry>` elements into a common title/link/date record. Supports local files as well as URLs, and honours `rel="alternate"` for Atom links.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --url https://example.com/feed.xml
python3 main.py --file feed.atom --limit 5
python3 main.py --demo
```

## Example

```text
RSS: 2 post(s)
  Mon, 02 Nov 2026 09:00:00 GMT   First post  https://example.com/1
  Sun, 01 Nov 2026 12:00:00 GMT   Second post  https://example.com/2
Atom: 1 post(s)
  2026-11-02T10:00:00Z            Atom entry  https://example.com/a
```

## Attribution

The problem statement is from [karan/Projects](https://github.com/karan/Projects), a list of practical projects that anyone can solve in any programming language (MIT License, Copyright (c) 2013 Karan Goel). The Python solution in this repository was implemented by [bspreston-esq](https://github.com/bspreston-esq).

This repository is part of the [Projects-Python-All](https://github.com/bspreston-esq/Projects-Python-All) collection.

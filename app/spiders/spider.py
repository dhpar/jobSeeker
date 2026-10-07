python
"""jobwatch.py: pull public job feeds, filter, show only new matches."""
import html
import re
import sqlite3
import time
from itertools import chain

import requests  # pip install requests

HEADERS = {"User-Agent": "jobwatch/0.1 (personal job search script)"}
TIMEOUT = 15
DELAY = 1.0  # seconds between requests, be polite

# Slugs come from the careers page URL. Placeholders below.
GREENHOUSE = ["company-a", "company-b"]
LEVER = ["company-c"]
ASHBY = ["company-d"]

TITLE_RE = re.compile(
    r"\b(full[- ]?stack|front[- ]?end|ai|product engineer|founding engineer)\b", re.I
)
STACK_RE = re.compile(r"\b(python|react|next\.?js|typescript)\b", re.I)
LOCATION_RE = re.compile(r"remote|minnesota|minneapolis|st\.? paul|edina", re.I)

def get_json(url, params=None):
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError) as e:
        print(f"skip {url}: {e}")
        return None
    finally:
        time.sleep(DELAY)
        
def clean(text):
    text = html.unescape(text or "")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()

def greenhouse(slug):
    data = get_json(
        f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs", {"content": "true"}
    )
    for j in (data or {}).get("jobs", []):
        yield dict(
            source="greenhouse", company=slug, title=j["title"],
            location=(j.get("location") or {}).get("name", ""),
            url=j["absolute_url"], text=clean(j.get("content")),
        )


def lever(slug):
    data = get_json(f"https://api.lever.co/v0/postings/{slug}", {"mode": "json"})
    if not isinstance(data, list):
        return
    for j in data:
        cats = j.get("categories") or {}
        yield dict(
            source="lever", company=slug, title=j["text"],
            location=cats.get("location") or "",
            url=j["hostedUrl"], text=j.get("descriptionPlain", ""),
        )


def ashby(slug):
    data = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
    for j in (data or {}).get("jobs", []):
        loc = j.get("location") or ""
        if j.get("isRemote"):
            loc += " remote"
        yield dict(
            source="ashby", company=slug, title=j["title"], location=loc,
            url=j["jobUrl"], text=j.get("descriptionPlain", ""),
        )


def hn_hiring():
    q = get_json(
        "https://hn.algolia.com/api/v1/search_by_date",
        {"tags": "story,author_whoishiring", "query": "Who is hiring", "hitsPerPage": 5},
    )
    hits = [h for h in (q or {}).get("hits", []) if "who is hiring" in h["title"].lower()]
    if not hits:
        return
    thread = get_json(f"https://hn.algolia.com/api/v1/items/{hits[0]['objectID']}")
    for c in (thread or {}).get("children", []):
        text = clean(c.get("text"))
        if text:
            # HN comments start with "Company | Role | Location"
            yield dict(
                source="hn", company=text[:40], title=text[:120], location=text[:200],
                url=f"https://news.ycombinator.com/item?id={c['id']}", text=text,
            )


def matches(job):
    return bool(
        TITLE_RE.search(job["title"])
        and LOCATION_RE.search(job["location"])
        and STACK_RE.search(job["text"])
    )

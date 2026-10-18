"""jobwatch.py: pull public job feeds, filter, show only new matches."""
import asyncio
from datetime import datetime
import html
import re
import time
from itertools import chain
import httpx
import requests
from scrapy import Spider
from sys import path
from app.db.db import insert_jobs
import json

def SPIDER_CONFIG():
    GREENHOUSE = []
    LEVER = []
    ASHBY = []
    with open("config.json", "r") as file:
        json_data = json.load(file)
        for agregator in json_data:
            if agregator["source"] == 'greenhouse':
                GREENHOUSE = [agregator['slugs']] 
            elif agregator["source"] == 'lever':
                LEVER = [agregator['slugs']]
            elif agregator["source"] == 'hackernews':
                ASHBY = [agregator['slugs']]
    return {
        'headers': { 
            "User-Agent": "jobwatch/0.1 (personal job search script)" 
        },
        'timeout': 15,
        'delay': 1.0,
        'slugs': {
            'greenhouse': GREENHOUSE,
            'lever': LEVER,
            'ashby': ASHBY
        } 
    }


            
# Slugs come from the careers page URL. Placeholders below.

TITLE_RE = re.compile(
    r'(?=[^.]*\b(?:engineer|dev(?:eloper)?|react|typescript|next)\b)'
    r'(?=[^.]*\bremote\b|(?=[^.]*\b(?:minnesota|mn)\b)(?=[^.]*\bhibrid\b))'
    r'[^.]+',
    re.IGNORECASE,
)

STACK_RE = re.compile(r"\b(python|react|next\.?js|typescript)\b", re.I)
MINNESOTA_RE = re.compile(r"minnesota|minneapolis|st\.? paul|edina", re.IGNORECASE)
HIBRID_RE = re.compile(r'\bhibrid\b', re.IGNORECASE)
REMOTE_RE = re.compile(r'\bremote\b', re.IGNORECASE)

def agregate_urls():
    URLS:list[str] = []
    with open("config.json", "r") as file:
        json_data = json.load(file)
        for agregator in json_data:
            if agregator["source"] == 'greenhouse':
                for slug in agregator['slugs']:
                    URLS.append(
                        f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
                    ) 
            elif agregator["source"] == 'lever':
                for slug in agregator['slugs']:
                    URLS.append(
                        f"https://api.lever.co/v0/postings/{slug}"
                    )
            elif agregator["source"] == 'hackernews':
                for slug in agregator['slugs']:
                    URLS.append(
                        f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
                    )
    return URLS
    
def get_json(url, params=None):
    try:
        r = requests.get(url, params=params, headers=SPIDER_CONFIG()['headers'], timeout=SPIDER_CONFIG()['timeout'])
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError) as e:
        print(f"skip {url}: {e}")
        return None
    finally:
        time.sleep(SPIDER_CONFIG()['delay'])

async def agregated_requests():
    # Limits simultaneous connections to avoid overwhelming the server/your OS
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=20)
    URLS = agregate_urls()
    # Use AsyncClient to keep connections alive across requests
    async with httpx.AsyncClient(limits=limits) as client:
        tasks = [fetch_url(client, url) for url in URLS]
        
        # Gather runs all tasks concurrently
        results = await asyncio.gather(*tasks)
        
        for result in results:
            yield dict(
                source="greenhouse", 
                company=result.slug or 'No company found', 
                title=result["title"],
                location=(result.get("location") or {}).get("name", ""),
                url=j["absolute_url"], text=clean(result.get("content")),
            )
            
def clean(text):
    text = html.unescape(text or "")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()

async def fetch_url(client: httpx.AsyncClient, url: str, slug = ''):
    response = await client.get(url)
    return dict(
        source="greenhouse", 
        company=response.slug or 'No company found', 
        title=response["title"],
        location=response["location"],
        url=response["absolute_url"], 
        text=response["content"],
    )

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
        {
            "tags": "story,author_whoishiring", 
            "query": "Who is hiring", 
            "hitsPerPage": 5
        },
    )
    hits = [hit for hit in (q or {}).get("hits", []) if "who is hiring" or "Who wants to be hired?" in hit["title"].lower()]
    if not hits:
        return
    thread = get_json(f"https://hn.algolia.com/api/v1/items/{hits[0]['objectID']}")
    for c in (thread or {}).get("children", []):
        text_bloob = clean(c.get("text"))
        if text_bloob:
            # HN comments start with "Company | Role | Location"
            title, position, text = text_bloob.split(' — ')
            yield dict(
                source="hn", 
                company=text[:40], 
                title=title, 
                location=text[:200], 
                first_seen=datetime.now(),
                url=f"https://news.ycombinator.com/item?id={c['id']}", text=text,
            )

def matches(job):
    return bool(
        TITLE_RE.search(job["title"])
        and ((MINNESOTA_RE.search(job["location"]) and HIBRID_RE.search(job["location"])) or REMOTE_RE.search(job["location"]))
        and STACK_RE.search(job["text"])
    )

def collect_matched_jobs():
    """Gather all matching jobs from every configured source."""
    jobs = chain(
        *(greenhouse(s) for s in GREENHOUSE),
        *(lever(s) for s in LEVER),
        *(ashby(s) for s in ASHBY),
        hn_hiring(),
    )
    for job in jobs:
        if matches(job):
            yield job

class MySpider(Spider):
    """Scrapy spider: collects matched jobs and writes them to output.json via FEEDS."""
    name = "jobs"
    print("scraping...")
    agregated_requests()
    jobs = collect_matched_jobs()
    insert_jobs(jobs)

    async def start(self):
        print("adding to db...")
        for job in collect_matched_jobs():
            yield job

    def parse(self, response):
        return

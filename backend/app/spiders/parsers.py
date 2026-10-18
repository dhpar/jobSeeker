# This file is not yet used or imported
import re
from bs4 import BeautifulSoup

def clean_url(href: str) -> str | None:
    # Some posts have markdown-style links inside the href, like:
    # https://[www.example.com](https://www.example.com)
    md = re.search(r"\]\((https?://[^)]+)\)", href)
    if md:
        return md.group(1)
    m = re.search(r"https?://\S+", href)
    return m.group(0) if m else None

def find_apply_link(soup: BeautifulSoup) -> str | None:
    candidates = []
    for a in soup.find_all("a", href=True):
        url = clean_url(a["href"])
        if url:
            candidates.append((a.get_text(strip=True).lower(), url))

    # Prefer links that look like job pages.
    for text, url in candidates:
        if "apply" in text or "job" in url or "career" in url:
            return url

    # Fall back to the first link, which is often the company site.
    return candidates[0][1] if candidates else None

def parse_post(raw: str) -> dict:
    head, _, rest = raw.partition("<p>")

    title = BeautifulSoup(head, "html.parser").get_text(" ", strip=True)
    apply_url = find_apply_link(BeautifulSoup(raw, "html.parser"))
    description = BeautifulSoup(rest, "html.parser").get_text("\n", strip=True)

    fields = extract_fields(title, description)
    return {
        "company": fields.get("company"),
        "role": fields.get("role"),
        "location": fields.get("location"),
        "apply_url": apply_url,
        "description": description,
    }

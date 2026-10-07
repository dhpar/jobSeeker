import sqlite3
import uvicorn
from itertools import chain
from app.spiders.spider import ASHBY, GREENHOUSE, LEVER, ashby, greenhouse, hn_hiring, lever, matches

def main():
    db = sqlite3.connect("jobs.db")
    db.execute(
        "CREATE TABLE IF NOT EXISTS seen (url TEXT PRIMARY KEY, company TEXT, "
        "title TEXT, first_seen TEXT DEFAULT CURRENT_TIMESTAMP)"
    )
    jobs = chain(
        *(greenhouse(s) for s in GREENHOUSE),
        *(lever(s) for s in LEVER),
        *(ashby(s) for s in ASHBY),
        hn_hiring(),
    )
    new = []
    for job in jobs:
        if not matches(job):
            continue
        cur = db.execute(
            "INSERT OR IGNORE INTO seen (url, company, title) VALUES (?, ?, ?)",
            (job["url"], job["company"], job["title"]),
        )
        if cur.rowcount:
            new.append(job)
    db.commit()

    for j in new:
        print(f"[{j['source']}] {j['company']} | {j['title'][:80]} | {j['location'][:40]}")
        print(f"  {j['url']}")
    print(f"{len(new)} new matches")


if __name__ == "__main__":
    main()
    uvicorn.run("app.app:app", host="0.0.0.0", port=8888, reload=True)
    
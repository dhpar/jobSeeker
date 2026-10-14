import sqlite3
from fastapi import logger
import uvicorn
from itertools import chain
from app.db.db import db_location
from app.spiders.spider import ASHBY, GREENHOUSE, LEVER, ashby, greenhouse, hn_hiring, lever, matches
from app.db.db import init_db, insert_job

def main():
    init_db()

    jobs = chain(
        *(greenhouse(s) for s in GREENHOUSE),
        *(lever(s) for s in LEVER),
        *(ashby(s) for s in ASHBY),
        hn_hiring(),
    )
    new = []
    for job in jobs:
        insert_job(job)

    for j in new:
        print(f"[{j['source']}] {j['company']} | {j['title'][:80]} | {j['location'][:40]}")
        print(f"  {j['url']}")
    print(f"{len(new)} new matches")

if __name__ == "__main__":
    main()
    uvicorn.run("app.app:app", host="0.0.0.0", port=8888, reload=True)
    
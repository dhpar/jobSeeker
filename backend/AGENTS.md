# AGENTS.md

## Architecture
- FastAPI app factory in app/app.py (create_app()), registers router from app/modules/main/route.py.
- Main controller in app/modules/main/controller.py returns a simple message.
- Scraper logic in app/spiders/spider.py (fetchers for Greenhouse, Lever, Ashby, HN) plus MySpider (Scrapy) writing output.json.
- Endpoints: GET /, GET /docs, GET /scrape (background), GET /jobs (reads output.json), GET /api/v1/main/.
- CORS via CORSMiddleware; origins from CORS_ORIGINS env var (comma-separated, default localhost:5173).
- run.py scrapes (filters + dedup to SQLite jobs.db) then starts Uvicorn on 0.0.0.0:8888.

## Commands
- Install: pip install -r requirements.txt (use .venv/Scripts/activate on Windows)
- Dev: python run.py (serves :8888)
- API only: uvicorn app.app:app --reload --port 8888
- HTTP scrape: GET /scrape; results: GET /jobs
- Tests: pytest; single test: pytest path/to/test.py::test_name

## Notes
- output.json written by Scrapy FEEDS (MySpider). GET /jobs reads it.
- Filters: TITLE_RE, STACK_RE, LOCATION_RE in app/spiders/spider.py.
- Sources: GREENHOUSE, LEVER, ASHBY (placeholders), plus HN Who is Hiring.
- run.py uses INSERT OR IGNORE into seen(url PRIMARY KEY) for dedup.
- MySpider must exist (imported by app/app.py). Server binds to 0.0.0.0:8888 in run.py and Docker.
- On Windows PowerShell avoid &&; use separate commands.

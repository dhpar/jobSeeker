# JobSeeker

Scrapes job postings (Greenhouse, Lever, Ashby, HN Who's Hiring), matches them against a candidate profile, and presents them in a web UI with job-description filtering.

## Structure

| Directory   | Contents                                                              |
| ----------- | --------------------------------------------------------------------- |
| `backend/`  | FastAPI + Scrapy API: scraping, matching, JSON persistence             |
| `frontend/` | Svelte + TypeScript + TanStack Query UI with JD filtering              |

## Quick start

Backend (terminal 1):

```bash
cd backend
pip install -r requirements.txt
python run.py        # serves API on http://localhost:8888
```

Frontend (terminal 2):

```bash
cd frontend
npm install
npm run dev          # serves UI on http://localhost:5173 (proxies /jobs, /scrape to :8888)
```

Open http://localhost:5173.

See `backend/README.md` and `frontend/README.md` for details.

## Future roadmap

- Resume upload and cross-referencing against scraped jobs (frontend stub already present)
- AI-powered semantic search within job descriptions (frontend stub already present)

## License

MIT

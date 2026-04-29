# Jobseeker

FastAPI + Scrapy application that scrapes job listings, aggregates postings, and matches them against a candidate profile via API. The project is designed to locate job postings that match a specific candidate profile and can be extended to cross-reference resumes and track jobs.

## Project Overview

- Purpose: Scrape job postings from major boards and aggregated sources.
- Primary targets: LinkedIn, Indeed, and job board URLs listed on https://www.jobsearchhack.com/p/400-job-boards.
- Output: The project uses `output.json` as the persistent data file for scraped results and URL storage.

## Features

- FastAPI-based HTTP API
- Background scraping endpoint
- Simple data retrieval endpoint
- Scrapy spider for job listing extraction
- Docker Compose support for containerized execution

## Architecture

- `app/app.py` - FastAPI application factory and route definitions
- `app/modules/main/route.py` - API router for the main application endpoint
- `app/modules/main/controller.py` - controller logic for main routes
- `app/spiders/spider.py` - Scrapy spider implementation
- `output.json` - file used for storing URL data / scraped output

## Requirements

- Python 3.10+ (recommended)
- FastAPI
- Uvicorn
- Scrapy
- python-dotenv
- pytest
- httpx
- twisted

## Running Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
python run.py
```

3. Open the API:

- `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

## Running with Docker

Use Docker Compose to build and run the service:

```bash
docker compose up --build
```

The app will be available at `http://localhost:8888`.

## API Endpoints

- `GET /` - Health check
- `GET /docs` - Swagger UI documentation
- `GET /scrape` - Starts the scraping process in the background
- `GET /get-data` - Returns scraped data from `output.json`
- `GET /api/v1/main/` - Returns the main controller payload

## Data Output

- `output.json` is used by the scraping pipeline.
- It is intended to store the URLs to scrape and can also hold the extracted job listing data.

## Future Roadmap

- Allow users to upload a resume and cross-reference it with scraped job data
- Show related job postings based on resume content
- Suggest resume edits to maximize response rates
- Integrate a job tracker to keep track of posted jobs

## Author

David H. Parramon

## License

MIT

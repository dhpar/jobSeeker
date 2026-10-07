import asyncio

from scrapy.crawler import CrawlerProcess
from app.spiders.spider import MySpider
from app.modules.main.route import main_router
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from scrapy.utils.project import get_project_settings
import os
import json

def run_spider():
    """Function to run the Scrapy spider."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(MySpider)
    process.start() # The script will block here until crawl is finished


def create_app() -> FastAPI:
    app = FastAPI(
        title="Job Seeker API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.include_router(main_router)

    origins = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/scrape")
    async def scrape_data(background_tasks: BackgroundTasks):
        """
        Endpoint to activate the scraping process.
        Runs the spider in a background task.
        """
        background_tasks.add_task(run_spider)
        return { "status": "Scraping activated in the background..." }
    
    @app.get("/jobs")
    def get_scraped_data():
        """
        Endpoint to retrieve the last scraped data.
        """
        if os.path.exists("output.json"):
            with open("output.json", "r") as file:
                data = json.load(file)
            return {"data": data}
        return {"status": "No data found, run /scrape first"}
    
    @app.get("/")
    def root():
        return {"message": "API is running", "docs": "/docs"}

    return app

app = create_app()

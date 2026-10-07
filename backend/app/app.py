import asyncio
import json
import os
import subprocess
import sys
import threading
from pathlib import Path

from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.modules.main.route import main_router
from app.ws import manager

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = BASE_DIR / "output.json"

# Held while a scrape runs; released by the background task when it finishes.
_scrape_lock = threading.Lock()

def run_spider() -> None:
    """Run the Scrapy spider in a subprocess.

    The Twisted reactor cannot restart in-process and its signal handlers must
    be installed in the main thread, so every scrape gets a fresh process.
    """
    subprocess.run(
        [sys.executable, "-m", "app.spiders.run_once"],
        cwd=BASE_DIR,
        check=True,
        timeout=300,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )

def scrape_and_notify(loop: asyncio.AbstractEventLoop) -> None:
    """Background task: run the spider, then broadcast the result to WS clients."""
    try:
        run_spider()
        payload = {"event": "scrape_completed", "ok": True}
    except Exception as exc:
        payload = {"event": "scrape_completed", "ok": False, "error": str(exc)}
    finally:
        _scrape_lock.release()
    asyncio.run_coroutine_threadsafe(manager.broadcast(payload), loop)

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
        Runs the spider in a background task and broadcasts progress on /ws.
        """
        if not _scrape_lock.acquire(blocking=False):
            return {"status": "Scrape already in progress..."}
        loop = asyncio.get_running_loop()
        background_tasks.add_task(scrape_and_notify, loop)
        await manager.broadcast({"event": "scrape_started"})
        return {"status": "Scraping activated in the background..."}

    @app.get("/jobs")
    def get_scraped_data():
        """
        Endpoint to retrieve the last scraped data.
        """
        if OUTPUT_FILE.exists():
            with open(OUTPUT_FILE, "r", encoding="utf8") as file:
                data = json.load(file)
            return {"data": data}
        return {"status": "No data found, run /scrape first"}

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """Live scrape progress: receives scrape_started / scrape_completed events."""
        await manager.connect(websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(websocket)

    @app.get("/")
    def root():
        return {"message": "API is running", "docs": "/docs"}

    return app

app = create_app()

import os
from pathlib import Path
import sqlite3


def db_location():
    BASE_DIR = Path(__file__).resolve().parents[0]
    OUTPUT_FILE = BASE_DIR / "jobs.db"
    return OUTPUT_FILE

def get_db():
    conn = sqlite3.connect(db_location(), detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with sqlite3.connect(db_location()) as conn:
        c = conn.cursor()

        c.execute(
            "CREATE TABLE IF NOT EXISTS seen (url TEXT PRIMARY KEY, company TEXT, title TEXT, location TEXT, text TEXT, source TEXT, first_seen TEXT DEFAULT CURRENT_TIMESTAMP)"
        )
        
        return c

def insert_jobs(jobs):
    with sqlite3.connect(db_location()) as conn:
        c = conn.cursor()
        c.executemany(
            "INSERT OR IGNORE INTO seen VALUES (:url, :company, :title, :location, :text, :source, :first_seen)",
            jobs
        )
        conn.commit()

def select_jobs():
    with sqlite3.connect(db_location()) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        jobs = c.execute('''SELECT * FROM seen''')
        jobs_list = jobs.fetchall()
        
        return jobs_list
    
import sqlite3
from contextlib import closing
from pathlib import Path

from app.db import db


def test_db_location_uses_app_db_directory_and_opens_from_another_working_directory(
    tmp_path, monkeypatch
):
    backend_dir = tmp_path / "backend"
    db_module = backend_dir / "app" / "db" / "db.py"
    working_dir = tmp_path / "working directory"
    working_dir.mkdir()
    monkeypatch.setattr(db, "__file__", str(db_module))
    monkeypatch.chdir(working_dir)

    location = db.db_location()

    assert location == db_module.parent / "jobs.db"
    assert location.is_absolute()
    with closing(sqlite3.connect(location)) as connection:
        connection.execute("CREATE TABLE jobs (id INTEGER PRIMARY KEY)")

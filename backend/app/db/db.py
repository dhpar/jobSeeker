from pathlib import Path


def db_location() -> Path:
    path = Path(__file__).resolve().parent / "jobs.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


class _NoopDB:
    def init_app(self, _app):
        return None

    def create_all(self):
        return None


db = _NoopDB()

class _NoopDB:
    def init_app(self, _app):
        return None

    def create_all(self):
        return None


db = _NoopDB()

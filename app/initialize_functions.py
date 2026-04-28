from fastapi import FastAPI
from app.modules.main.route import main_router


def initialize_route(app: FastAPI):
    app.include_router(main_router)


def initialize_db(app: FastAPI):
    # No database initialization is required for the starter FastAPI app.
    return app


def initialize_swagger(app: FastAPI):
    # FastAPI ships OpenAPI/Swagger UI at /docs by default.
    return app.openapi()

import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routes import router
from app.services.comic_service import ComicService


def create_app() -> FastAPI:
    settings = get_settings()

    settings.ensure_directories()

    logging.basicConfig(level=logging.INFO)

    app = FastAPI(
        title=settings.app_name,
        description="Generate personalized five-panel AI comics.",
        version="1.0.0",
    )

    app.state.settings = settings
    app.state.comic_service = ComicService(settings)

    app.mount(
        "/static",
        StaticFiles(directory=str(settings.static_dir)),
        name="static",
    )

    app.include_router(router)

    return app


app = create_app()
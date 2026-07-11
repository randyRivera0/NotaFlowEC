from __future__ import annotations

import os

from fastapi import FastAPI
from nicegui import ui

from app.api.router import router as api_router
from app.frontend.pages import register_pages


def create_app() -> FastAPI:
    """Build the shared FastAPI and NiceGUI ASGI application."""
    application = FastAPI(title="NotaFlow EC API", version="0.1.0")
    application.include_router(api_router, prefix="/api")
    register_pages()
    ui.run_with(application, title="NotaFlow EC", favicon="💳")
    return application


app = create_app()


if __name__ in {"__main__", "__mp_main__"}:
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "8000")),
        reload=False,
    )

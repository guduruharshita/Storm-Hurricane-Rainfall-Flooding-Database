from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from storm_db.api.routers import analytics, events
from storm_db.config import settings
from storm_db.database import init_db


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        init_db()
        yield

    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=(
            "REST API for querying and analysing natural disaster events: "
            "hurricanes, earthquakes, droughts, tsunamis, and floods."
        ),
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    def health() -> dict:
        return {"status": "ok"}

    app.include_router(events.router)
    app.include_router(analytics.router)

    return app


app = create_app()

from fastapi import FastAPI

from .routes.gpx import router as gpx_router

app = FastAPI()
app.include_router(gpx_router)

__all__ = ["app"]

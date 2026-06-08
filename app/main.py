from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.model import Attendance, Task, User, WorkLog


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    App startup par tables create karta hai.
    Production me Alembic migration preferred hai,
    lekin abhi learning aur quick setup ke liye helpful hai.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Root"])
def root():
    """Basic health route."""
    return {
        "success": True,
        "message": "Bidoo ERP Backend Running",
        "docs": "/docs",
    }


@app.get("/config-test", tags=["Root"])
def config_test():
    """Configuration load verify karne ke liye small debug route."""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }

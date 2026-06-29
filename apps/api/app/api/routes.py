from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.routers import router as auth_router
from app.habits.routers import router as habits_router
from app.notes.routers import router as notes_router
from app.tasks.routers.tasks import router as tasks_router
from app.core.config import Settings, get_settings
from app.schemas.health import HealthResponse, RootResponse
from app.services.health import get_health_status, get_root_status

router = APIRouter()

# Feature Routers
router.include_router(auth_router)
router.include_router(tasks_router)
router.include_router(notes_router)
router.include_router(habits_router)


@router.get("/", response_model=RootResponse, tags=["System"])
def read_root(
    settings: Annotated[Settings, Depends(get_settings)],
) -> RootResponse:
    return get_root_status(settings)


@router.get("/health", response_model=HealthResponse, tags=["System"])
def read_health() -> HealthResponse:
    return get_health_status()
from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.health import HealthResponse, RootResponse
from app.services.health import get_health_status, get_root_status

router = APIRouter()


@router.get("/", response_model=RootResponse, tags=["system"])
def read_root(settings: Annotated[Settings, Depends(get_settings)]) -> RootResponse:
    return get_root_status(settings)


@router.get("/health", response_model=HealthResponse, tags=["system"])
def read_health() -> HealthResponse:
    return get_health_status()

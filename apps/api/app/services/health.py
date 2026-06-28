from app.core.config import Settings
from app.schemas.health import HealthResponse, RootResponse


def get_root_status(settings: Settings) -> RootResponse:
    return RootResponse(name=settings.api_name, status="ok")


def get_health_status() -> HealthResponse:
    return HealthResponse(status="ok")

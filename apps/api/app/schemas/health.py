from typing import Literal

from pydantic import BaseModel, ConfigDict


class RootResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    status: Literal["ok"]


class HealthResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: Literal["ok"]

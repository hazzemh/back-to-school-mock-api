from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class Command(BaseModel):
    model_config = ConfigDict(extra="allow")
    order: int
    title: str
    subtitle: str
    command_id: str


class SpecialDay(BaseModel):
    model_config = ConfigDict(extra="allow")
    events: list[Any] = Field(default_factory=list)
    is_special_day: bool


class DashboardMeta(BaseModel):
    model_config = ConfigDict(extra="allow")
    commands: list[Command]
    timezone: str
    data_as_of: str
    special_day: SpecialDay
    generated_at: str
    configuration: dict[str, Any]
    applied_filters: dict[str, Any]
    payload_version: str


class ReturnedData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    meta: DashboardMeta
    sections: list[dict[str, Any]]


class DataContainer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    returned_data: ReturnedData


class DashboardEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    StatusCode: int
    Messages: Any | None
    Data: DataContainer
    DataCount: int


class FTTHMaturityIndexEnvelope(BaseModel):
    """Passthrough envelope for the FTTH Maturity Index dashboard's flat, non-standard payload shape."""

    model_config = ConfigDict(extra="allow")


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str


class ErrorResponse(BaseModel):
    error: ErrorDetail

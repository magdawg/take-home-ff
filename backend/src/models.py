"""Pydantic models for asset management and insights"""

from enum import Enum

from pydantic import BaseModel, ConfigDict


class AssetStatus(str, Enum):
    """Asset status enumeration"""

    ACTIVE = "active"
    DEFAULTED = "defaulted"


class AssetInput(BaseModel):
    """Asset input model for POST requests"""

    id: str
    nominal_value: float
    due_date: str  # Format: YYYY-MM-DD
    interest_rate: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "id-1",
                "nominal_value": 100.0,
                "due_date": "2025-12-04",
                "interest_rate": 0.03,
            }
        }
    )


class AssetOutput(BaseModel):
    """Asset output model for GET requests"""

    id: str
    nominal_value: float
    status: AssetStatus
    due_date: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "id-1",
                "nominal_value": 100.0,
                "status": "active",
                "due_date": "2025-12-04",
            }
        }
    )


class AssetData(BaseModel):
    """Asset data model for internal storage"""

    id: str
    nominal_value: float
    due_date: str
    interest_rate: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "id-1",
                "nominal_value": 100.0,
                "due_date": "2025-12-04",
                "interest_rate": 0.03,
            }
        }
    )


class Insight(BaseModel):
    """Insight model for GET /insights"""

    id: str
    name: str
    value: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "id-1",
                "name": "average_interest_rate",
                "value": 0.04,
            }
        }
    )

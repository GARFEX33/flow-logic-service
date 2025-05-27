"""Database models."""

from typing import Any, Dict
from pydantic import BaseModel, ConfigDict

class FlujoEjecutado(BaseModel):
    """FlujoEjecutado data model."""

    id: str
    data: Dict[str, Any]
    status: str

    model_config = ConfigDict(from_attributes=True)
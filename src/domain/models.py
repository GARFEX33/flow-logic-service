from uuid import UUID
from datetime import datetime
from typing import Literal, Optional, Dict
from pydantic import BaseModel, Field

class Evento(BaseModel):
    id: UUID
    tipo_evento: str
    payload: Dict
    timestamp: datetime

class FlujoEjecutado(BaseModel):
    id: UUID
    tipo_evento: str
    payload: Dict
    estado: Literal['recibido', 'en_proceso', 'procesado', 'fallido']
    timestamp: datetime
    error: Optional[str] = None
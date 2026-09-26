from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from .models import TipoReporte, EstadoReporte


class ReporteCreate(BaseModel):
    tipo: TipoReporte
    especie: str
    descripcion: Optional[str] = None
    foto_url: Optional[str] = None
    embedding: Optional[List[float]] = None
    latitud: float
    longitud: float


class ReporteOut(BaseModel):
    id: int
    tipo: TipoReporte
    especie: str
    descripcion: Optional[str]
    foto_url: Optional[str]
    latitud: float
    longitud: float
    estado: EstadoReporte
    fecha_creacion: datetime

    class Config:
        from_attributes = True
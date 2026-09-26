import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from geoalchemy2 import Geography

from .database import Base


class TipoReporte(str, enum.Enum):
    perdida = "perdida"
    encontrada = "encontrada"


class EstadoReporte(str, enum.Enum):
    abierto = "abierto"
    resuelto = "resuelto"


class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoReporte), nullable=False)
    especie = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    foto_url = Column(String, nullable=True)

    # Guardamos los embeddings como texto (listas de números en formato JSON),
    # ya que no estamos usando pgvector.
    embedding = Column(Text, nullable=True)
    embedding_texto = Column(Text, nullable=True)

    ubicacion = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)

    estado = Column(Enum(EstadoReporte), default=EstadoReporte.abierto)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
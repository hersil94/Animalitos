import json
import os
import uuid
from typing import List, Optional

import numpy as np
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..ai import calcular_embedding, calcular_embedding_texto

router = APIRouter(prefix="/reportes", tags=["reportes"])

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _a_out(reporte: models.Reporte) -> schemas.ReporteOut:
    punto = to_shape(reporte.ubicacion)
    return schemas.ReporteOut(
        id=reporte.id,
        tipo=reporte.tipo,
        especie=reporte.especie,
        descripcion=reporte.descripcion,
        foto_url=reporte.foto_url,
        latitud=punto.y,
        longitud=punto.x,
        estado=reporte.estado,
        fecha_creacion=reporte.fecha_creacion,
    )


@router.post("/subir-foto")
def subir_foto(archivo: UploadFile = File(...)):
    extension = os.path.splitext(archivo.filename)[1]
    nombre_unico = f"{uuid.uuid4()}{extension}"
    ruta_completa = os.path.join(UPLOAD_DIR, nombre_unico)

    contenido = archivo.file.read()
    with open(ruta_completa, "wb") as destino:
        destino.write(contenido)

    embedding = calcular_embedding(contenido)

    return {
        "foto_url": f"/static/uploads/{nombre_unico}",
        "embedding": embedding,
    }


@router.post("/", response_model=schemas.ReporteOut)
def crear_reporte(reporte: schemas.ReporteCreate, db: Session = Depends(get_db)):
    punto = WKTElement(f"POINT({reporte.longitud} {reporte.latitud})", srid=4326)

    embedding_json = json.dumps(reporte.embedding) if reporte.embedding else None

    embedding_texto_json = None
    if reporte.descripcion:
        embedding_texto = calcular_embedding_texto(reporte.descripcion)
        embedding_texto_json = json.dumps(embedding_texto)

    nuevo = models.Reporte(
        tipo=reporte.tipo,
        especie=reporte.especie,
        descripcion=reporte.descripcion,
        foto_url=reporte.foto_url,
        embedding=embedding_json,
        embedding_texto=embedding_texto_json,
        ubicacion=punto,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return _a_out(nuevo)


@router.get("/", response_model=List[schemas.ReporteOut])
def listar_reportes(
    tipo: Optional[models.TipoReporte] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radio_km: Optional[float] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Reporte).filter(
        models.Reporte.estado == models.EstadoReporte.abierto
    )

    if tipo is not None:
        query = query.filter(models.Reporte.tipo == tipo)

    if lat is not None and lon is not None and radio_km is not None:
        punto_busqueda = WKTElement(f"POINT({lon} {lat})", srid=4326)
        query = query.filter(
            func.ST_DWithin(
                models.Reporte.ubicacion, punto_busqueda, radio_km * 1000
            )
        )

    return [_a_out(r) for r in query.all()]


@router.get("/{reporte_id}", response_model=schemas.ReporteOut)
def obtener_reporte(reporte_id: int, db: Session = Depends(get_db)):
    reporte = db.query(models.Reporte).filter(models.Reporte.id == reporte_id).first()
    if reporte is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return _a_out(reporte)


@router.patch("/{reporte_id}/resolver", response_model=schemas.ReporteOut)
def resolver_reporte(reporte_id: int, db: Session = Depends(get_db)):
    reporte = db.query(models.Reporte).filter(models.Reporte.id == reporte_id).first()
    if reporte is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    reporte.estado = models.EstadoReporte.resuelto
    db.commit()
    db.refresh(reporte)
    return _a_out(reporte)


def _similitud_coseno(vector_a, vector_b):
    a = np.array(vector_a)
    b = np.array(vector_b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


@router.get("/{reporte_id}/sugerencias")
def sugerencias(reporte_id: int, db: Session = Depends(get_db)):
    reporte = db.query(models.Reporte).filter(models.Reporte.id == reporte_id).first()
    if reporte is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    if not reporte.embedding:
        raise HTTPException(status_code=400, detail="Este reporte no tiene foto, no se puede comparar")

    embedding_base = json.loads(reporte.embedding)
    embedding_texto_base = json.loads(reporte.embedding_texto) if reporte.embedding_texto else None

    tipo_opuesto = (
        models.TipoReporte.encontrada
        if reporte.tipo == models.TipoReporte.perdida
        else models.TipoReporte.perdida
    )

    candidatos = db.query(models.Reporte).filter(
        models.Reporte.tipo == tipo_opuesto,
        models.Reporte.estado == models.EstadoReporte.abierto,
        models.Reporte.embedding.isnot(None),
        models.Reporte.especie == reporte.especie,
    ).all()

    resultados = []
    for candidato in candidatos:
        embedding_candidato = json.loads(candidato.embedding)
        sim_imagen = _similitud_coseno(embedding_base, embedding_candidato)

        sim_texto = None
        if embedding_texto_base and candidato.embedding_texto:
            embedding_texto_candidato = json.loads(candidato.embedding_texto)
            sim_texto = _similitud_coseno(embedding_texto_base, embedding_texto_candidato)

        if sim_texto is not None:
            puntaje_final = 0.7 * sim_imagen + 0.3 * sim_texto
        else:
            puntaje_final = sim_imagen

        resultados.append((puntaje_final, sim_imagen, sim_texto, candidato))

    resultados.sort(key=lambda x: x[0], reverse=True)

    UMBRAL = 0.75
    top = [r for r in resultados if r[0] >= UMBRAL][:5]

    return [
        {
            "similitud": round(puntaje, 3),
            "similitud_imagen": round(sim_img, 3),
            "similitud_texto": round(sim_txt, 3) if sim_txt is not None else None,
            "reporte": _a_out(candidato),
        }
        for puntaje, sim_img, sim_txt, candidato in top
    ]
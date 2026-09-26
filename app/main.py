from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import reportes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mascotas Perdidas API")
templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(reportes.router)


@app.get("/")
def root():
    return {"mensaje": "API de Mascotas Perdidas funcionando 🐾"}


@app.get("/mapa")
def mapa(request: Request):
    return templates.TemplateResponse("mapa.html", {"request": request})
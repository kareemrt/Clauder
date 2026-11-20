from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from .database import engine
from . import models
from .routers import medications, doses, symptoms, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="MediTrack",
    description="Medication adherence and health tracking platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(medications.router)
app.include_router(doses.router)
app.include_router(symptoms.router)
app.include_router(reports.router)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/medications", response_class=HTMLResponse)
def medications_page(request: Request):
    return templates.TemplateResponse("medications.html", {"request": request})


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "MediTrack"}

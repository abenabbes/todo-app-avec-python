from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database import init_db
from api.routers import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()   # crée les tables au démarrage
    yield

app = FastAPI(title="API Gestionnaire de Tâches", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # à restreindre en production !
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)

@app.get("/health")
async def health():
    return {"status": "ok"}

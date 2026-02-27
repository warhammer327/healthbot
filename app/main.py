from fastapi import FastAPI
from app.routes.v1.ingest import ingest_router
from app.routes.v1.generate import generate_router
from app.routes.v1.retrieve import retrieve_router

app = FastAPI(title="Healthbot")

app.include_router(ingest_router, prefix="/v1", tags=["Ingest"])
app.include_router(generate_router, prefix="/v1", tags=["Generate"])
app.include_router(retrieve_router, prefix="/v1", tags=["Retrieve"])

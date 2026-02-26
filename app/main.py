from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from app.routes.v1.ingest import ingest_router
from app.routes.v1.generate import generate_router
from app.routes.v1.retrieve import retrieve_router

app = FastAPI(title="Healthbot")

model = SentenceTransformer(
    "paraphrase-multilingual-mpnet-base-v2",
)

app.include_router(ingest_router, tags=["Ingest"])
app.include_router(generate_router, tags=["Generate"])
app.include_router(retrieve_router, tags=["Retrieve"])

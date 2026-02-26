from fastapi import APIRouter, UploadFile, File, HTTPException

ingest_router = APIRouter()


@ingest_router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    return {"message": "Document ingested", "language_detected": "something"}

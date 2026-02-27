import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.ingest import IngestResponse, IngestRequest
from app.services.ingestion_service import IngestionService

logger = logging.getLogger(__name__)
ingest_router = APIRouter()


@ingest_router.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")

    try:
        validated = IngestRequest(filename=file.filename, content=content)
    except ValueError as e:
        logger.warning("Validation failed for file '%s': %s", file.filename, e)
        raise HTTPException(status_code=400, detail=str(e))

    try:
        IngestionService.ingest_text(content=content)
        logger.info("Successfully ingested file '%s'", validated.filename)
    except Exception as e:
        logger.error("Ingestion failed for file '%s': %s", validated.filename, e)
        raise HTTPException(status_code=500, detail="Ingestion failed")

    return IngestResponse(success=True, error=None, filename=validated.filename)

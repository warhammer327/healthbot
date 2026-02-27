from fastapi import APIRouter, HTTPException
from app.services.retrieval_service import RetrievalService
from app.schemas.retrieve import RetrieveResponse
from app.utils.translate import translate_text

retrieve_router = APIRouter()

SUPPORTED_LANGUAGES = {"en", "ja"}


@retrieve_router.get("/retrieve", response_model=RetrieveResponse)
async def retrieve(query: str, output_language: str = "en"):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")
    if output_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400, detail=f"Unsupported output_language '{output_language}'"
        )

    results = RetrievalService.retrieve(query)

    if output_language == "ja":
        for result in results:
            result["chunk"] = await translate_text(result["chunk"], dest="ja")

    return RetrieveResponse(success=True, error=None, results=results)

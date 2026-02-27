from fastapi import APIRouter, HTTPException
from app.services.retrieval_service import RetrievalService
from app.schemas.generate import GenerateResponse
from app.utils.translate import translate_text, detect_language

generate_router = APIRouter()

SUPPORTED_LANGUAGES = {"en", "ja"}


@generate_router.get("/generate", response_model=GenerateResponse)
async def generate(query: str, kb_language: str = "en"):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")
    if kb_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400, detail=f"Unsupported kb_language '{kb_language}'"
        )

    detected_lang = await detect_language(query)

    # Translate query to kb_language for retrieval if needed
    retrieval_query = query
    if detected_lang != kb_language:
        retrieval_query = await translate_text(query, dest=kb_language)

    results = RetrievalService.retrieve(retrieval_query)

    context = "\n".join(r["chunk"] for r in results)

    mock_response = f"Based on the available medical guidelines:\n\n{context}\n\nIn summary, the retrieved information addresses your query about: {retrieval_query}"

    # Translate response back to query language if needed
    if detected_lang != kb_language:
        mock_response = await translate_text(mock_response, dest=detected_lang)

    return GenerateResponse(success=True, error=None, response=mock_response)

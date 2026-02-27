from fastapi import APIRouter, HTTPException
from app.services.retrieval_service import RetrievalService
from app.schemas.generate import GenerateResponse
from app.utils.translate import translate_text, detect_language

generate_router = APIRouter()


@generate_router.get("/generate", response_model=GenerateResponse)
async def generate(query: str):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")

    detected_lang = await detect_language(query)

    # Translate query to English for retrieval if needed
    english_query = query
    if detected_lang != "en":
        english_query = await translate_text(query, dest="en")

    results = RetrievalService.retrieve(english_query)

    context = "\n".join(r["chunk"] for r in results)

    mock_response = f"Based on the available medical guidelines:\n\n{context}\n\nIn summary, the retrieved information addresses your query about: {english_query}"

    # Translate response back to query language if needed
    if detected_lang != "en":
        mock_response = await translate_text(mock_response, dest=detected_lang)

    return GenerateResponse(success=True, error=None, response=mock_response)

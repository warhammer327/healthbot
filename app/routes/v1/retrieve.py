from fastapi import APIRouter, HTTPException
from app.services.retrieval_service import RetrievalService
from app.schemas.retrieve import RetrieveResponse

retrieve_router = APIRouter()


@retrieve_router.get("/retrieve", response_model=RetrieveResponse)
async def retrieve(query: str):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")
    results = RetrievalService.retrieve(query)
    return RetrieveResponse(success=True, error=None, results=results)

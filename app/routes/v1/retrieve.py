from fastapi import APIRouter, HTTPException

retrieve_router = APIRouter()


@retrieve_router.post("/generate")
async def retrieve():
    return {"message": "retrieved something"}

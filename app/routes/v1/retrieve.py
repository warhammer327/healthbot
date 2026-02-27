from fastapi import APIRouter, HTTPException

retrieve_router = APIRouter()


@retrieve_router.get("/retrieve")
async def retrieve():
    return {"message": "retrieved something"}

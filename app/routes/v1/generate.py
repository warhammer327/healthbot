from fastapi import APIRouter, HTTPException

generate_router = APIRouter()


@generate_router.get("/generate")
async def generate():
    return {"message": "something something"}

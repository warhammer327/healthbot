from fastapi import APIRouter, HTTPException

generate_router = APIRouter()


@generate_router.post("/generate")
async def generate():
    return {"message": "something something"}

from pydantic import BaseModel


class GenerateResponse(BaseModel):
    success: bool
    error: str | None
    response: str

from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    error: str | None = None

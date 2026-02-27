from pydantic import BaseModel, field_validator
from app.schemas.base_response import BaseResponse


class RetrieveRequest(BaseModel):
    query: str

    @field_validator("query")
    def must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Query must not be empty")
        return v


class RetrieveResult(BaseModel):
    rank: int
    score: float
    chunk: str


class RetrieveResponse(BaseResponse):
    results: list[RetrieveResult]

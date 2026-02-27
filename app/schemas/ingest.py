from pydantic import BaseModel, field_validator
from app.schemas.base_response import BaseResponse


class IngestRequest(BaseModel):
    filename: str
    content: str

    @field_validator("filename")
    def must_be_txt(cls, v):
        if not v.endswith(".txt"):
            raise ValueError("Only .txt files are allowed")
        return v

    @field_validator("content")
    def must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Content must not be empty")
        return v


class IngestResponse(BaseResponse):
    filename: str

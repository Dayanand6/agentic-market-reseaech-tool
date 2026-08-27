from pydantic import BaseModel, Field, field_validator


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=300)

    @field_validator("query")
    @classmethod
    def sanitize_query(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Query cannot be empty or only whitespace")

        return cleaned


class ResearchResponse(BaseModel):
    query: str
    status: str
    message: str
    summary: str
    results: list[dict]
    report: dict

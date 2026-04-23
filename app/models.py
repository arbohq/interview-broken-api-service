from pydantic import BaseModel, Field


class CategorizeRequest(BaseModel):
    description: str = Field(..., min_length=3, max_length=500)
    categories: list[str] = Field(..., min_length=1)
    llm_output: str = Field(..., min_length=2)


class CategorizationResult(BaseModel):
    suggested_category: str
    confidence_score: float
    reasoning: str
    status: str


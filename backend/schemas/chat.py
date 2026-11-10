from pydantic import BaseModel, Field  # pyright: ignore[reportMissingImports]

class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    ticket_id: str | None = None

class ChatResponse(BaseModel):
    ticket_id: str
    answer: str
    sources: list[dict]
    subqueries: list[str]

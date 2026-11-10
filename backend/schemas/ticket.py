from pydantic import BaseModel

class TicketOut(BaseModel):
    ticket_key: str
    title: str
    model_config = {"from_attributes": True}

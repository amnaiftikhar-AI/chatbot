from pydantic import BaseModel

class DocumentOut(BaseModel):
    id: int
    document_key: str
    filename: str
    title: str
    document_type: str
    device_model: str
    software_version: str
    category: str
    status: str
    model_config = {"from_attributes": True}

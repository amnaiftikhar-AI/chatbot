from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.services.chat_service import answer_question

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        return await answer_question(db, request.question, request.ticket_id)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

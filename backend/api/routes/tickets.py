from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models import Ticket, Message

router = APIRouter()


@router.get("/")
def list_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
    output = []

    for ticket in tickets:
        last_message = (
            db.query(Message)
            .filter(Message.ticket_id == ticket.id)
            .order_by(Message.id.desc())
            .first()
        )
        output.append({
            "ticket_id": ticket.ticket_key,
            "title": ticket.title,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
            "last_message": last_message.content[:160] if last_message else ""
        })

    return output


@router.get("/{ticket_key}/messages")
def ticket_messages(ticket_key: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_key == ticket_key).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    messages = (
        db.query(Message)
        .filter(Message.ticket_id == ticket.id)
        .order_by(Message.id.asc())
        .all()
    )

    return {
        "ticket_id": ticket_key,
        "title": ticket.title,
        "messages": [
            {
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at.isoformat() if message.created_at else None
            }
            for message in messages
        ]
    }


@router.delete("/{ticket_key}")
def delete_ticket(ticket_key: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_key == ticket_key).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()

    return {"message": "Conversation history deleted", "ticket_id": ticket_key}

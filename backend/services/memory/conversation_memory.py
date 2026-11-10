from uuid import uuid4

from backend.models import Ticket, Message


def get_or_create_ticket(db, ticket_key, title):
    if ticket_key:
        ticket = db.query(Ticket).filter(Ticket.ticket_key == ticket_key).first()
        if ticket is None:
            raise LookupError("Ticket ID not found. Start a new conversation or provide a valid ticket ID.")
        return ticket

    ticket = Ticket(ticket_key=str(uuid4()), title=title[:250])
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def load_history(db, ticket_id):
    messages = (
        db.query(Message)
        .filter(Message.ticket_id == ticket_id)
        .order_by(Message.id.asc())
        .all()
    )
    return [{"role": item.role, "content": item.content} for item in messages]


def save_message(db, ticket_id, role, content):
    message = Message(ticket_id=ticket_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

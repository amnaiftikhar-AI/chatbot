import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.db.base import Base
from backend.models import Ticket, Message
from backend.services.memory.conversation_memory import (
    get_or_create_ticket,
    load_history,
    save_message,
)


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_ticket_creation_and_message_persistence(db):
    ticket = get_or_create_ticket(db, None, "VPN issue")
    assert ticket.ticket_key

    save_message(db, ticket.id, "user", "VPN is not connecting")
    save_message(db, ticket.id, "assistant", "Please check DNS.")

    history = load_history(db, ticket.id)

    assert [item["role"] for item in history] == ["user", "assistant"]
    assert history[0]["content"] == "VPN is not connecting"


def test_existing_ticket_is_reused(db):
    first = get_or_create_ticket(db, None, "VPN issue")
    second = get_or_create_ticket(db, first.ticket_key, "Follow-up")

    assert first.id == second.id
    assert first.ticket_key == second.ticket_key


def test_unknown_ticket_id_is_rejected(db):
    with pytest.raises(LookupError):
        get_or_create_ticket(db, "not-a-real-ticket", "Follow-up")

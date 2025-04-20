from app.models import Ticket, Message
from app.database import SessionLocal
from sqlalchemy.orm import Session
from uuid import UUID

def create_ticket(db: Session, title: str, description: str, user_id: UUID):
    """
    Function to create a ticket and store it in the database.
    """
    ticket = Ticket(title=title, description=description, user_id=user_id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def get_tickets(db: Session, user_id: UUID):
    """
    Function to get all the tickets
    """
    return db.query(Ticket).filter(Ticket.user_id == user_id).all()

def get_ticket_by_id(db: Session, ticket_id: UUID):
    """
    Function to get ticket by id.
    """
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def add_message(db: Session, ticket_id: UUID, content: str, is_ai: bool):
    """
    Function to add a message to the database.
    """
    message = Message(content=content, is_ai=is_ai, ticket_id=ticket_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_ticket_messages(db: Session, ticket_id: UUID):
    return db.query(Message).filter(Message.ticket_id == ticket_id).all()
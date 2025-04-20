from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import SessionLocal
from app.services.auth import login_user, create_user
from app.services.ticket import create_ticket, get_tickets, get_ticket_by_id, add_message, get_ticket_messages
from app.services.ai_service import get_ai_response
from app.utils.jwt_util import verify_token
from app.schemas import UserCreate, TicketCreate, Ticket, MessageCreate, Message
from app.database import Base, engine

#init app
app = FastAPI()

#create database tables
Base.metadata.create_all(bind=engine)

#function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#function to get the current user id based on the token
def get_current_user(token: str):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload["id"]

@app.post("/auth/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user.email, user.password)
    return {"id": db_user.id, "email": db_user.email}

@app.post("/auth/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    token = login_user(db, user.email, user.password)
    if token:
        return token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.post("/tickets")
def create_ticket_endpoint(ticket: TicketCreate, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    new_ticket = create_ticket(db, ticket.title, ticket.description, token)
    return new_ticket

@app.get("/tickets")
def get_user_tickets(db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    tickets = get_tickets(db, token)
    return tickets

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: UUID, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket

@app.post("/tickets/{ticket_id}/messages")
def add_message_to_ticket(ticket_id: UUID, message: MessageCreate, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    new_message = add_message(db, ticket_id, message.content, is_ai=False)
    return new_message

@app.get("/tickets/{ticket_id}/ai-response")
async def stream_ai_response(ticket_id: UUID, db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    ticket = get_ticket_by_id(db, ticket_id)
    messages = get_ticket_messages(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return StreamingResponse(get_ai_response(ticket, messages, db), media_type="text/plain")


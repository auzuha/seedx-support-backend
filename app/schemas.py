from pydantic import BaseModel
from typing import Optional
import uuid

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: uuid.UUID
    role: str

    class Config:
        orm_mode = True

class TicketBase(BaseModel):
    title: str
    description: str

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: uuid.UUID
    status: str
    created_at: str
    user_id: uuid.UUID

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: uuid.UUID
    is_ai: bool
    created_at: str

    class Config:
        orm_mode = True

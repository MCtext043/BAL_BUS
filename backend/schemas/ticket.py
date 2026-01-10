"""
Схемы для билетов
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class TicketCreate(BaseModel):
    """Схема создания билета"""
    trip_id: int
    full_name: str = Field(..., min_length=2, max_length=200)
    email: EmailStr
    consent_to_processing: bool = Field(..., description="Согласие на обработку персональных данных")


class TicketResponse(BaseModel):
    """Схема ответа с билетом"""
    id: int
    trip_id: int
    full_name: str
    email: str
    price: float
    ticket_number: str
    is_paid: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


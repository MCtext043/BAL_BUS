"""
Модель билета
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.core.database import Base


class Ticket(Base):
    """Билет на рейс"""
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    ticket_number = Column(String, unique=True, nullable=False, index=True)
    is_paid = Column(Boolean, default=False)  # Пока муляж, потом через Элплат
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связь с рейсом (опционально, если нужен доступ к trip)
    # trip = relationship("Trip", back_populates="tickets")


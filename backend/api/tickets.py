"""
API для покупки билетов
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
import uuid
from datetime import datetime

from backend.core.database import get_db
from backend.models.ticket import Ticket
from backend.models.trip import Trip
from backend.schemas.ticket import TicketCreate, TicketResponse
from backend.core.email import send_ticket_email

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def purchase_ticket(
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db),
):
    """Покупка билета на рейс"""
    try:
        # Проверка согласия на обработку данных
        if not ticket_data.consent_to_processing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Необходимо согласие на обработку персональных данных"
            )
        
        # Проверка существования рейса
        result = await db.execute(
            select(Trip).where(Trip.id == ticket_data.trip_id, Trip.is_active == True)  # noqa: E712
        )
        trip = result.scalar_one_or_none()
        
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рейс не найден или неактивен"
            )
        
        # Генерация номера билета
        ticket_number = f"BAL-{uuid.uuid4().hex[:8].upper()}-{datetime.now().strftime('%Y%m%d')}"
        
        # Создание билета
        db_ticket = Ticket(
            trip_id=ticket_data.trip_id,
            full_name=ticket_data.full_name,
            email=ticket_data.email,
            price=trip.price,
            ticket_number=ticket_number,
            is_paid=False,  # Пока муляж, потом через Элплат
        )
        
        db.add(db_ticket)
        await db.commit()
        await db.refresh(db_ticket)
        
        # Отправка email с билетом (муляж)
        email_data = {
            "ticket_number": ticket_number,
            "full_name": ticket_data.full_name,
            "email": ticket_data.email,
            "trip_origin": trip.origin,
            "trip_destination": trip.destination,
            "departure_time": trip.departure_time.strftime("%d.%m.%Y %H:%M"),
            "arrival_time": trip.arrival_time.strftime("%d.%m.%Y %H:%M"),
            "price": trip.price,
        }
        
        await send_ticket_email(ticket_data.email, email_data)
        
        logger.info(f"Билет создан: {ticket_number} для {ticket_data.full_name} ({ticket_data.email})")
        
        return db_ticket
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка покупки билета: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка сервера: {str(e)}"
        )


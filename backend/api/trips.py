"""
API для расписания рейсов
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import date

from backend.core.database import get_db
from backend.models.trip import Trip
from backend.schemas.trip import TripCreate, TripUpdate, TripResponse
from backend.api.deps import get_current_dispatcher

router = APIRouter()


@router.get("/", response_model=List[TripResponse])
async def list_trips(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    departure_date: Optional[date] = None,
    _t: Optional[str] = None,  # Параметр для обхода кэша
    db: AsyncSession = Depends(get_db),
):
    """Публичный список рейсов"""
    query = select(Trip).where(Trip.is_active == True)  # noqa: E712
    if origin:
        query = query.where(Trip.origin.ilike(f"%{origin}%"))
    if destination:
        query = query.where(Trip.destination.ilike(f"%{destination}%"))
    if departure_date:
        query = query.where(func.date(Trip.departure_time) == departure_date)
    query = query.order_by(Trip.departure_time)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=TripResponse)
async def create_trip(
    trip: TripCreate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_dispatcher),
):
    """Создать рейс (только диспетчер)"""
    db_trip = Trip(**trip.dict())
    db.add(db_trip)
    await db.commit()
    await db.refresh(db_trip)
    return db_trip


@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(
    trip_id: int,
    trip_update: TripUpdate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_dispatcher),
):
    """Обновить рейс (только диспетчер)"""
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    db_trip = result.scalar_one_or_none()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    for key, value in trip_update.dict(exclude_unset=True).items():
        setattr(db_trip, key, value)
    await db.commit()
    await db.refresh(db_trip)
    return db_trip


@router.delete("/{trip_id}", status_code=204)
async def delete_trip(
    trip_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_dispatcher),
):
    """Удалить рейс (только диспетчер)"""
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    db_trip = result.scalar_one_or_none()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db_trip.is_active = False
    await db.commit()
    return None


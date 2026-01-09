"""
Схемы для рейсов
"""
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class TripBase(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    is_active: bool = True
    
    @field_validator("origin", "destination")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError("Должно быть не менее 2 символов")
        if len(v) > 100:
            raise ValueError("Слишком длинное значение (максимум 100 символов)")
        return v


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None


class TripResponse(TripBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


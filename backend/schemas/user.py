"""
Схемы для пользователя
"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_dispatcher: bool = False


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Валидация пароля"""
        if len(v) < 6:
            raise ValueError('Пароль должен быть не менее 6 символов')
        if len(v) > 200:
            raise ValueError('Пароль слишком длинный')
        return v
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Валидация имени пользователя"""
        if len(v) < 3:
            raise ValueError('Имя пользователя должно быть не менее 3 символов')
        if len(v) > 50:
            raise ValueError('Имя пользователя слишком длинное (максимум 50 символов)')
        return v


class UserResponse(UserBase):
    """Схема ответа с данными пользователя"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


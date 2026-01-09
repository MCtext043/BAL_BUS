"""
Скрипт для заполнения тестовыми данными
"""
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import AsyncSessionLocal
from backend.models.trip import Trip


async def seed_trips():
    """Заполнение тестовыми рейсами"""
    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже рейсы
        from sqlalchemy import select
        result = await session.execute(select(Trip))
        existing = result.scalars().all()
        if existing:
            print("Тестовые данные уже существуют")
            return
        
        # Создаем рейсы на сегодня и завтра
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        test_trips = [
            # Сегодня
            Trip(
                origin="Москва",
                destination="Санкт-Петербург",
                departure_time=today.replace(hour=8, minute=0),
                arrival_time=today.replace(hour=14, minute=30),
                price=2500.00,
                is_active=True
            ),
            Trip(
                origin="Москва",
                destination="Казань",
                departure_time=today.replace(hour=10, minute=30),
                arrival_time=today.replace(hour=18, minute=0),
                price=1800.00,
                is_active=True
            ),
            Trip(
                origin="Санкт-Петербург",
                destination="Москва",
                departure_time=today.replace(hour=9, minute=15),
                arrival_time=today.replace(hour=15, minute=45),
                price=2500.00,
                is_active=True
            ),
            Trip(
                origin="Москва",
                destination="Нижний Новгород",
                departure_time=today.replace(hour=14, minute=0),
                arrival_time=today.replace(hour=20, minute=30),
                price=1200.00,
                is_active=True
            ),
            # Завтра
            Trip(
                origin="Москва",
                destination="Санкт-Петербург",
                departure_time=tomorrow.replace(hour=8, minute=0),
                arrival_time=tomorrow.replace(hour=14, minute=30),
                price=2500.00,
                is_active=True
            ),
            Trip(
                origin="Казань",
                destination="Москва",
                departure_time=tomorrow.replace(hour=7, minute=30),
                arrival_time=tomorrow.replace(hour=15, minute=0),
                price=1800.00,
                is_active=True
            ),
            Trip(
                origin="Москва",
                destination="Воронеж",
                departure_time=tomorrow.replace(hour=12, minute=0),
                arrival_time=tomorrow.replace(hour=17, minute=30),
                price=1500.00,
                is_active=True
            ),
        ]
        
        for trip in test_trips:
            session.add(trip)
        
        await session.commit()
        print(f"Создано {len(test_trips)} тестовых рейсов")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_trips())


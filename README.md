# BAL_BUS - Регистрация пользователей

Простое приложение для регистрации пользователей на FastAPI с Bootstrap интерфейсом.

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных

По умолчанию используется SQLite (файл `balbus.db` создастся автоматически).

Для использования PostgreSQL создайте файл `.env`:

```env
DATABASE_URL=postgresql+asyncpg://balbus_user:balbus_password@localhost:5432/balbus
SECRET_KEY=your-secret-key-min-32-chars
DEBUG=True
```

### 3. Запуск

```bash
python run.py
```

Приложение будет доступно по адресу: http://localhost:8005

## Структура проекта

```
BAL_BUS/
├── backend/
│   ├── main.py              # Точка входа FastAPI
│   ├── core/
│   │   ├── config.py        # Настройки
│   │   ├── database.py      # БД конфигурация
│   │   └── security.py      # Хеширование паролей
│   ├── models/
│   │   └── user.py          # Модель пользователя
│   ├── schemas/
│   │   └── user.py          # Pydantic схемы
│   └── api/
│       └── auth.py           # API endpoints
├── templates/
│   ├── base.html            # Базовый шаблон
│   ├── index.html           # Главная страница
│   └── register.html        # Страница регистрации
├── static/                   # Статические файлы (если нужны)
├── requirements.txt
└── run.py
```

## API Endpoints

- `GET /` - Главная страница
- `GET /register` - Страница регистрации
- `POST /api/auth/register` - Регистрация пользователя
- `GET /health` - Проверка здоровья сервиса
- `GET /docs` - Swagger документация

## Использование

1. Откройте http://localhost:8006
2. Выберите роль: пассажир или диспетчер (кнопки на главной)
3. Пассажир: видит расписание (сегодня/завтра + выбор даты)
4. Диспетчер: авторизуйтесь /login, затем редактируйте рейсы (CRUD)

## Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL** / **SQLite** - база данных
- **Bootstrap 5** - CSS фреймворк
- **Jinja2** - шаблонизатор


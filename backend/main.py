"""
FastAPI приложение с регистрацией
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, FileSystemLoader
import os
import logging

from backend.core.database import engine, Base
from backend.api.auth import router as auth_router
from backend.api.trips import router as trips_router
from backend.api.tickets import router as tickets_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="BAL_BUS Registration")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статических файлов (если директория существует)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение шаблонов
template_env = Environment(loader=FileSystemLoader("templates"))

# Подключение роутеров
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(trips_router, prefix="/api/trips", tags=["trips"])
app.include_router(tickets_router, prefix="/api/tickets", tags=["tickets"])


@app.on_event("startup")
async def startup():
    """Создание таблиц при запуске"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Заполнение тестовыми данными
    try:
        from backend.api.seed import seed_trips
        await seed_trips()
    except Exception as e:
        logger.warning(f"Не удалось заполнить тестовые данные: {e}")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Главная страница"""
    template = template_env.get_template("index.html")
    return HTMLResponse(content=template.render())


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Страница регистрации"""
    template = template_env.get_template("register.html")
    return HTMLResponse(content=template.render())


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Страница входа"""
    template = template_env.get_template("login.html")
    return HTMLResponse(content=template.render())


@app.get("/health")
async def health():
    """Проверка здоровья сервиса"""
    return {"status": "ok"}

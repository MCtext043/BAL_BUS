"""
Скрипт для запуска FastAPI приложения
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
    )


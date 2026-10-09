from fastapi import FastAPI

from app.routers import auth

app = FastAPI(
    title="Canary Tokens API",
    description="Сервис для обнаружения несанкционированного доступа к документам",
    version="0.1.0",
)

app.include_router(auth.router)


@app.get("/health", tags=["system"])
def health_check() -> dict:
    return {"status": "ok"}
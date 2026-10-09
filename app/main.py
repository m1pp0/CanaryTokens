from fastapi import FastAPI

app = FastAPI(
    title="Canary Tokens API",
    description="Сервис для обнаружения несанкционированного доступа к документам",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health_check() -> dict:
    return {"status": "ok"}
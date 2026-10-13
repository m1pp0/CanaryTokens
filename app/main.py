from fastapi import FastAPI
from app.routers import auth, events, public, tokens
from app.routers import auth, tokens, public

app = FastAPI(
    title="Canary Tokens API",
    description="Сервис для обнаружения доступа к документам",
    version="0",
)


app.include_router(auth.router)
app.include_router(tokens.router)
app.include_router(events.router)
app.include_router(public.router)

@app.get("/health", tags=["system"])
def health_check() -> dict:
    return {"status": "ok"}


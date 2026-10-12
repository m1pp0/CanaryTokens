from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event, Token

router = APIRouter(tags=["public"])


@router.get("/t/{token_uuid}", response_class=HTMLResponse)
def trigger_token(
    token_uuid: str,
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    token = db.query(Token).filter(Token.uuid == token_uuid).first()
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден",
        )

    event = Event(
        token_id=token.id,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        referer=request.headers.get("referer"),
    )
    db.add(event)
    db.commit()

    return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Документ недоступен</title>
        </head>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>Документ недоступен</h1>
            <p>Возможно, ссылка устарела или была отозвана.</p>
        </body>
        </html>
        """,
        status_code=200,
    )
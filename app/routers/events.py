from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Event, Token, User
from app.schemas import EventListOut, EventOut

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=EventListOut)
def list_events(
    token_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EventListOut:
    user_token_ids = [
        t.id for t in db.query(Token.id).filter(Token.user_id == current_user.id).all()
    ]
    base_query = db.query(Event).filter(Event.token_id.in_(user_token_ids))
    if token_id is not None:
        if token_id not in user_token_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Токен не найден",
            )
        base_query = base_query.filter(Event.token_id == token_id)

    total = base_query.count()
    items = (
        base_query.order_by(Event.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return EventListOut(
        total=total,
        limit=limit,
        offset=offset,
        items=items,
    )


@router.get("/{event_id}", response_model=EventOut)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие не найдено",
        )

    token = db.query(Token).filter(Token.id == event.token_id).first()
    if token is None or token.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому событию",
        )

    return event
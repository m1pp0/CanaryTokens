import uuid as uuid_lib

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import BASE_URL
from app.database import get_db
from app.models import Token, User
from app.schemas import TokenCreate, TokenListOut, TokenOut

router = APIRouter(prefix="/tokens", tags=["tokens"])


def _to_out(token: Token) -> TokenOut:
    return TokenOut(
        id=token.id,
        uuid=token.uuid,
        label=token.label,
        memo=token.memo,
        url=f"{BASE_URL}/t/{token.uuid}",
        created_at=token.created_at,
        user_id=token.user_id,
    )


def _get_own_token(token_id: int, user: User, db: Session) -> Token:
    token = db.query(Token).filter(Token.id == token_id).first()
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Токен не найден",
        )
    if token.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому токену",
        )
    return token


@router.post("", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def create_token(
    payload: TokenCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TokenOut:
    token = Token(
        uuid=str(uuid_lib.uuid4()),
        label=payload.label,
        memo=payload.memo,
        user_id=current_user.id,
    )
    db.add(token)
    db.commit()
    db.refresh(token)
    return _to_out(token)


@router.get("", response_model=TokenListOut)
def list_tokens(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TokenListOut:
    base_query = db.query(Token).filter(Token.user_id == current_user.id)
    total = base_query.count()
    items = (
        base_query.order_by(Token.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return TokenListOut(
        total=total,
        limit=limit,
        offset=offset,
        items=[_to_out(t) for t in items],
    )


@router.get("/{token_id}", response_model=TokenOut)
def get_token(
    token_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TokenOut:
    token = _get_own_token(token_id, current_user, db)
    return _to_out(token)


@router.delete("/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_token(
    token_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    token = _get_own_token(token_id, current_user, db)
    db.delete(token)
    db.commit()
    return None
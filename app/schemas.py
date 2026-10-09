from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr = Field(..., description='Email пользователя')

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128, description='Пароль')

class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

class TokenBase(BaseModel):
    label: str = Field(..., min_length=1, max_length=255, description='Название приманки')
    memo: Optional[str] = Field(None, max_length=2000, description='Заметки')

class TokenCreate(TokenBase): 
    pass

class TokenOut(TokenBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: str
    url: str
    created_at: datetime
    user_id: int

class TokenListOut(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[TokenOut]

class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    referer: Optional[str] = None
    created_at: datetime
    token_id: int

class EventListOut(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[EventOut]

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class TokenData(BaseModel):
    user_id: Optional[int] = None

    
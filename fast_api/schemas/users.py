from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class MessageSchema(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    empresa_id: Optional[int] = None
    # cargo: str
    # empresa: str


class UserSchemaPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    empresa_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes = True  # Pydantic v2
    #     # ou orm_mode = True  # Pydantic v1


class UserList(BaseModel):
    users: list[UserSchemaPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

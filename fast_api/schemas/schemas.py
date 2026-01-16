from pydantic import BaseModel, EmailStr


class MessageSchema(BaseModel):
    message: str


class UserSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    # cargo: str
    # empresa: str


class UserSchemaPublic(BaseModel):
    nome: str
    email: EmailStr
    id: int


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserSchemaPublic]

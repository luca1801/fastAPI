from pydantic import BaseModel, ConfigDict, EmailStr


class MessageSchema(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    # cargo: str
    # empresa: str


class UserSchemaPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes = True  # Pydantic v2
    #     # ou orm_mode = True  # Pydantic v1


class UserList(BaseModel):
    users: list[UserSchemaPublic]

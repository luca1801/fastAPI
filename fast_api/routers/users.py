from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_api.database.database import get_session
from fast_api.models.users import UserBase
from fast_api.schemas.schemas import (
    FilterPage,
    MessageSchema,
    UserList,
    UserSchema,
    UserSchemaPublic,
)
from fast_api.security.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])

T_Session = Annotated[Session, Depends(get_session)]
T_Current_User = Annotated[UserBase, Depends(get_current_user)]

# Definindo um endpoint com o endereço / acessível pelo método HTTP GET
# @router.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
# def read_root():
#     return {'message': 'Hello World!'}


# Problema que estava causando falha nos testes, ficava
# usando banco de produção:
# O problema é que você chama next(get_session()) direto no router,
# ignorando o override do pytest; isso sempre usa o engine de produção.
# Injete a sessão via Depends e finalize o conftest.py.
@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=UserSchemaPublic
)
def create_user(user: UserSchema, session: T_Session):
    # session = next(get_session())
    db_user = session.scalar(
        select(UserBase).where(
            (UserBase.username == user.username)
            | (UserBase.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )
    new_user = UserBase(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    new_user = UserSchemaPublic.model_validate(new_user)
    # session.close()
    return new_user
    # return UserSchemaPublic(
    #     id=new_user.id, username=new_user.username, email=new_user.email
    # )

    # user_with_id = UserDB(
    #     **user.model_dump(),
    #     id=len(database) + 1,
    # )
    # database.append(user_with_id)
    # return user_with_id


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users(
    session: T_Session,
    current_user: T_Current_User,
    filter_users: Annotated[FilterPage, Query()],
):
    users = session.scalars(
        select(UserBase).limit(filter_users.limit).offset(filter_users.offset)
    ).all()
    # users = UserList.model_validate(users)
    return {'users': users}


@router.put(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaPublic,
)
def update_user(
    user: UserSchema,
    user_id: int,
    session: T_Session,
    current_user: T_Current_User,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to update this user',
        )
    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)
        session.commit()
        session.refresh(current_user)
        return UserSchemaPublic.model_validate(current_user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists',
        )


# @app.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_Current_User,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to delete this user',
        )
    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted successfully'}


# Oauth2 é um protocolo aberto para autorização, para esquema
# de credenciais, o fastiapi conta com o OAuth2PasswordRequestForm
# @router.post('/token', response_model=Token)
# def login_for_acess_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     session: Session = Depends(get_session),
# ):
#     user = session.scalar(
#         select(UserBase).where(UserBase.email == form_data.username)
#     )

#     if not user:
#         raise HTTPException(
#             status_code=HTTPStatus.UNAUTHORIZED,
#             detail='Incorrect username or password',
#             headers={'WWW-Authenticate': 'Bearer'},
#         )
#     if not verify_password(form_data.password, user.password):
#         raise HTTPException(
#             status_code=HTTPStatus.UNAUTHORIZED,
#             detail='Incorrect username or password',
#             headers={'WWW-Authenticate': 'Bearer'},
#         )
#     access_token = create_access_token(data={'sub': user.email})
#     return {'access_token': access_token, 'token_type': 'bearer'}

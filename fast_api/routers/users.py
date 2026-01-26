from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_api.database.database import get_session
from fast_api.models.users import UserBase
from fast_api.schemas.schemas import (
    MessageSchema,
    UserList,
    UserSchema,
    UserSchemaPublic,
)

router = APIRouter(prefix='/users', tags=['users'])


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
def create_user(
    user: UserSchema,
    session: Session = Depends(get_session),
):
    # session = next(get_session())
    db_user = session.scalar(
        select(UserBase).where(
            (UserBase.username == user.username)
            | (UserBase.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            print(db_user.username)
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
        username=user.username, email=user.email, password=user.password
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
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(UserBase).limit(limit).offset(offset)).all()
    # users = UserList.model_validate(users)
    return {'users': users}


@router.put(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaPublic,
)
def update_user(
    user: UserSchema, user_id: int, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(UserBase).where(UserBase.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password
        session.commit()
        session.refresh(user_db)
        return UserSchemaPublic.model_validate(user_db)
    except IntegrityError:
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
    session: Session = Depends(get_session),
):
    user_db = session.scalar(select(UserBase).where(UserBase.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    session.delete(user_db)
    session.commit()
    return {'message': 'User deleted successfully'}

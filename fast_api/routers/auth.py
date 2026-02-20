# Este arquivo é responsável por lidar com a autenticação dos usuários,
# utilizando o protocolo OAuth2 para gerar tokens de acesso.
# Ele define uma rota para login, onde os usuários podem enviar suas
# credenciais (email e senha) e receber um token de acesso válido para
# autenticação em outras rotas protegidas da aplicação.
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy.orm import Session
from fast_api.database.database import get_session
from fast_api.models.users import UserBase
from fast_api.schemas.schemas import (
    Token,
)
from fast_api.security.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_Auth_Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Current_User = Annotated[UserBase, Depends(get_current_user)]


@router.post('/token', response_model=Token)
async def login_for_acess_token(
    form_data: T_Auth_Form,
    session: T_Session,
):
    user = await session.scalar(
        select(UserBase).where(UserBase.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    current_user: T_Current_User,
):
    access_token = create_access_token(data={'sub': current_user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}

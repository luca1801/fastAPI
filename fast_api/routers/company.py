from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy.orm import Session
from fast_api.database.database import get_session
from fast_api.models.company import Company as CompanyModel
from fast_api.models.users import UserBase
from fast_api.schemas.company import (
    Company,
    CompanySchema,
)
from fast_api.security.security import (
    get_current_user,
)

router = APIRouter(prefix='/company', tags=['company'])

T_Session = Annotated[AsyncSession, Depends(get_session)]
T_Current_User = Annotated[UserBase, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=CompanySchema)
async def create_company(
    company: Company, session: T_Session, current_user: T_Current_User
):
    db_company = await session.scalar(
        select(CompanyModel).where(CompanyModel.name == company.name)
    )
    if db_company:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Company name already exists',
        )
    new_company = CompanyModel(
        name=company.name,
        service=company.service,
        location=company.location,
        ramal=company.ramal,
    )
    print(f'Created company: {new_company}')
    session.add(new_company)
    try:
        await session.commit()
        await session.refresh(new_company)
        new_company = CompanySchema.model_validate(new_company)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Failed to create company',
        )
    return new_company

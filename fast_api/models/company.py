from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fast_api.models.users import UserBase

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from fast_api.models.registry import table_registry
from fast_api.schemas.enums import CompanyStatus

# table_registry = registry()


@mapped_as_dataclass(table_registry)
class Company:
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(unique=True)
    service: Mapped[str]
    location: Mapped[str]
    ramal: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    status: Mapped[CompanyStatus] = mapped_column(
        default=CompanyStatus.active, nullable=False
    )

    users_company: Mapped[list['UserBase']] = relationship(
        'UserBase',
        init=False,
        back_populates='empresa',
        cascade='all, delete-orphan',
    )  # type: ignore

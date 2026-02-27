from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fast_api.models.company import Company


from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from fast_api.models.registry import table_registry

# table_registry = registry()


@mapped_as_dataclass(table_registry)
class UserBase:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    empresa_id: Mapped[int] = mapped_column(
        ForeignKey('companies.id'), nullable=True
    )
    # empresa_name: Mapped[str] = mapped_column(
    #     ForeignKey('companies.name'), nullable=False
    # )
    # updated_at: Mapped[datetime] = mapped_column(
    #     init=False, server_default=func.now(), onupdate=func.now()
    # )
    # updated_at: Mapped[datetime] = mapped_column(
    #     init=False, default=datetime.now, onupdate=lambda: datetime.now()
    # )

    empresa: Mapped['Company'] = relationship(
        'Company', init=False, back_populates='users_company'
    )  # type: ignore

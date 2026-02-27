from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fast_api.schemas.users import UserSchemaPublic

from pydantic import BaseModel, ConfigDict, Field

from fast_api.schemas.enums import CompanyStatus


class Company(BaseModel):
    name: str
    service: str
    location: str
    ramal: str


class CreateCompany(Company):
    status: CompanyStatus = CompanyStatus.active


class CompanySchema(Company):
    id: int
    status: CompanyStatus
    # created_at: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class CompanyWithEmployees(Company):
    users_company: list['UserSchemaPublic'] = Field(default_factory=list)

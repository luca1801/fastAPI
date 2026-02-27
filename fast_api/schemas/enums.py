from enum import Enum


class CompanyStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'

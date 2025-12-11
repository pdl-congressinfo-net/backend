from pydantic import BaseModel


# =========================
# COMPANY SCHEMAS
# =========================
class CompanyBase(BaseModel):
    name: str
    sponsoring: bool = False
    location_id: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    sponsoring: bool | None = None
    location_id: str | None = None


class CompanyRead(CompanyBase):
    id: str

    class Config:
        from_attributes = True


# =========================
# COMPANY EMPLOYEE SCHEMAS
# =========================
class CompanyEmployeeBase(BaseModel):
    departement: str | None = None
    function: str | None = None
    user_id: str | None = None
    company_id: str | None = None


class CompanyEmployeeCreate(CompanyEmployeeBase):
    pass


class CompanyEmployeeUpdate(BaseModel):
    departement: str | None = None
    function: str | None = None
    user_id: str | None = None
    company_id: str | None = None


class CompanyEmployeeRead(CompanyEmployeeBase):
    id: str

    class Config:
        from_attributes = True

from pydantic import BaseModel

from app.common.exceptions import NotFoundError
from app.features.companies import repo
from app.features.companies.model import Company, CompanyEmployee, Sponsoring


# =========================
# COMPANY SERVICE
# =========================
def list_companies(db, pagination):
    return repo.list_companies(db, pagination)


def get_company(db, company_id: str):
    company = repo.get_company_by_id(db, company_id)
    if not company:
        raise NotFoundError("Company not found")
    return company


def create_company(db, payload: BaseModel):
    company = Company.model_validate(payload)
    return repo.create_company(db, company)


def update_company(db, company_id: str, payload: BaseModel):
    company = repo.get_company_by_id(db, company_id)
    if not company:
        raise NotFoundError("Company not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_company(db, company, updates)


def delete_company(db, company_id: str):
    company = repo.get_company_by_id(db, company_id)
    if not company:
        raise NotFoundError("Company not found")
    repo.delete_company(db, company)


# =========================
# COMPANY EMPLOYEE SERVICE
# =========================
def list_company_employees(db, pagination):
    return repo.list_company_employees(db, pagination)


def get_company_employee(db, employee_id: str):
    employee = repo.get_company_employee_by_id(db, employee_id)
    if not employee:
        raise NotFoundError("Company employee not found")
    return employee


def create_company_employee(db, payload: BaseModel):
    employee = CompanyEmployee.model_validate(payload)
    return repo.create_company_employee(db, employee)


def update_company_employee(db, employee_id: str, payload: BaseModel):
    employee = repo.get_company_employee_by_id(db, employee_id)
    if not employee:
        raise NotFoundError("Company employee not found")

    updates = payload.model_dump(exclude_unset=True)
    return repo.update_company_employee(db, employee, updates)


def delete_company_employee(db, employee_id: str):
    employee = repo.get_company_employee_by_id(db, employee_id)
    if not employee:
        raise NotFoundError("Company employee not found")
    repo.delete_company_employee(db, employee)


# =========================
# SPONSORING SERVICE
# =========================
def list_sponsorings(db, pagination):
    return repo.list_sponsorings(db, pagination)


def get_sponsoring(db, sponsoring_id: str):
    sponsoring = repo.get_sponsoring_by_id(db, sponsoring_id)
    if not sponsoring:
        raise NotFoundError("Sponsoring not found")
    return sponsoring


def create_sponsoring(db, payload: BaseModel):
    sponsoring = Sponsoring.model_validate(payload)
    return repo.create_sponsoring(db, sponsoring)


def update_sponsoring(db, sponsoring_id: str, payload: BaseModel):
    sponsoring = repo.get_sponsoring_by_id(db, sponsoring_id)
    if not sponsoring:
        raise NotFoundError("Sponsoring not found")
    updates = payload.model_dump(exclude_unset=True)
    return repo.update_sponsoring(db, sponsoring, updates)


def delete_sponsoring(db, sponsoring_id: str):
    sponsoring = repo.get_sponsoring_by_id(db, sponsoring_id)
    if not sponsoring:
        raise NotFoundError("Sponsoring not found")
    repo.delete_sponsoring(db, sponsoring)

from sqlalchemy.orm import Session

from app.features.companies.model import Company, CompanyEmployee, Sponsoring
from app.utils.pagination import PaginationParams
from app.utils.refine_query import refine_query


# =========================
# COMPANY REPO
# =========================
def list_companies(db: Session, pagination: PaginationParams):
    query = db.query(Company)
    return refine_query(query, Company, pagination)


def get_company_by_id(db: Session, company_id: str):
    return db.query(Company).filter(Company.id == company_id).first()


def get_company_by_name(db: Session, name: str):
    return db.query(Company).filter(Company.name == name).first()


def create_company(db: Session, company: Company):
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def update_company(db: Session, company: Company, updates: dict):
    for key, value in updates.items():
        setattr(company, key, value)
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company: Company):
    db.delete(company)
    db.commit()


# =========================
# COMPANY EMPLOYEE REPO
# =========================
def list_company_employees(db: Session, pagination: PaginationParams):
    query = db.query(CompanyEmployee)
    return refine_query(query, CompanyEmployee, pagination)


def get_company_employee_by_id(db: Session, employee_id: str):
    return db.query(CompanyEmployee).filter(CompanyEmployee.id == employee_id).first()


def get_company_employee_by_contact_id(db: Session, contact_id: str):
    return (
        db.query(CompanyEmployee)
        .filter(CompanyEmployee.contact_id == contact_id)
        .first()
    )


def create_company_employee(db: Session, employee: CompanyEmployee):
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_company_employee(db: Session, employee: CompanyEmployee, updates: dict):
    for key, value in updates.items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete_company_employee(db: Session, employee: CompanyEmployee):
    db.delete(employee)
    db.commit()


# =========================
# SPONSORING REPO
# =========================
def list_sponsorings(db: Session, pagination: PaginationParams):
    query = db.query(Sponsoring)
    return refine_query(query, Sponsoring, pagination)


def get_sponsoring_by_id(db: Session, sponsoring_id: str):
    return db.query(Sponsoring).filter(Sponsoring.id == sponsoring_id).first()


def create_sponsoring(db: Session, sponsoring: Sponsoring):
    db.add(sponsoring)
    db.commit()
    db.refresh(sponsoring)
    return sponsoring


def update_sponsoring(db: Session, sponsoring: Sponsoring, updates: dict):
    for key, value in updates.items():
        setattr(sponsoring, key, value)
    db.commit()
    db.refresh(sponsoring)
    return sponsoring


def delete_sponsoring(db: Session, sponsoring: Sponsoring):
    db.delete(sponsoring)
    db.commit()

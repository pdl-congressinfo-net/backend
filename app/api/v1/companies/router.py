from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.v1.companies import schema
from app.common.deps import get_db, require_permission
from app.common.permissions import Companies, CompanyEmployees
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.companies import service
from app.features.users.model import User
from app.utils.pagination import PaginationParams

companies_router = APIRouter()


@companies_router.get("/employees", response_model=list[schema.CompanyEmployeeRead])
async def list_company_employees(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(CompanyEmployees.List)),
):
    """List all company employees."""
    results, total = service.list_company_employees(db, pagination)
    return refine_list_response(response, results, total)


@companies_router.get(
    "/employees/{employee_id}", response_model=ApiResponse[schema.CompanyEmployeeRead]
)
async def get_company_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(CompanyEmployees.Show)),
):
    """Get a specific company employee by ID."""
    employee = service.get_company_employee(db, employee_id)
    return ApiResponse(data=employee)


@companies_router.post(
    "/employees", response_model=ApiResponse[schema.CompanyEmployeeRead]
)
async def create_company_employee(
    employee: schema.CompanyEmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(CompanyEmployees.Create)),
):
    """Create a new company employee."""
    db_employee = service.create_company_employee(db, employee)
    return ApiResponse(data=db_employee)


@companies_router.patch(
    "/employees/{employee_id}", response_model=ApiResponse[schema.CompanyEmployeeRead]
)
async def update_company_employee(
    employee_id: str,
    employee: schema.CompanyEmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(CompanyEmployees.Update)),
):
    """Update an existing company employee."""
    db_employee = service.update_company_employee(db, employee_id, employee)
    return ApiResponse(data=db_employee)


@companies_router.delete("/employees/{employee_id}", response_model=MessageResponse)
async def delete_company_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(CompanyEmployees.Delete)),
):
    """Delete a company employee."""
    service.delete_company_employee(db, employee_id)
    return MessageResponse(message="Company employee deleted successfully")


@companies_router.get("", response_model=list[schema.CompanyRead])
async def list_companies(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Companies.List)),
):
    """List all companies."""
    results, total = service.list_companies(db, pagination)
    return refine_list_response(response, results, total)


@companies_router.get("/{company_id}", response_model=ApiResponse[schema.CompanyRead])
async def get_company(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Companies.Show)),
):
    """Get a specific company by ID."""
    company = service.get_company(db, company_id)
    return ApiResponse(data=company)


@companies_router.post("", response_model=ApiResponse[schema.CompanyRead])
async def create_company(
    company: schema.CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Companies.Create)),
):
    """Create a new company."""
    db_company = service.create_company(db, company)
    return ApiResponse(data=db_company)


@companies_router.patch("/{company_id}", response_model=ApiResponse[schema.CompanyRead])
async def update_company(
    company_id: str,
    company: schema.CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Companies.Update)),
):
    """Update an existing company."""
    db_company = service.update_company(db, company_id, company)
    return ApiResponse(data=db_company)


@companies_router.delete("/{company_id}", response_model=MessageResponse)
async def delete_company(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Companies.Delete)),
):
    """Delete a company."""
    service.delete_company(db, company_id)
    return MessageResponse(message="Company deleted successfully")


# =========================
# SPONSORINGS ENDPOINTS
# =========================
@companies_router.get("/sponsorings", response_model=list[schema.SponsoringRead])
async def list_sponsorings(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Companies.List)),
):
    results, total = service.list_sponsorings(db, pagination)
    return refine_list_response(response, results, total)


@companies_router.get(
    "/sponsorings/{sponsoring_id}", response_model=ApiResponse[schema.SponsoringRead]
)
async def get_sponsoring(
    sponsoring_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Companies.Show)),
):
    sponsoring = service.get_sponsoring(db, sponsoring_id)
    return ApiResponse(data=sponsoring)


@companies_router.post(
    "/sponsorings", response_model=ApiResponse[schema.SponsoringRead]
)
async def create_sponsoring(
    sponsoring: schema.SponsoringCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Companies.Create)),
):
    sponsoring = service.create_sponsoring(db, sponsoring)
    return ApiResponse(data=sponsoring)


@companies_router.patch(
    "/sponsorings/{sponsoring_id}", response_model=ApiResponse[schema.SponsoringRead]
)
async def update_sponsoring(
    sponsoring_id: str,
    sponsoring: schema.SponsoringUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Companies.Update)),
):
    sponsoring = service.update_sponsoring(db, sponsoring_id, sponsoring)
    return ApiResponse(data=sponsoring)


@companies_router.delete("/sponsorings/{sponsoring_id}", response_model=MessageResponse)
async def delete_sponsoring(
    sponsoring_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Companies.Delete)),
):
    service.delete_sponsoring(db, sponsoring_id)
    return MessageResponse(message="Sponsoring deleted successfully")

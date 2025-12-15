from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.v1.contacts import schema
from app.common.deps import get_db, require_permission
from app.common.permissions import Contacts
from app.common.refine import refine_list_response
from app.common.responses import ApiResponse, MessageResponse
from app.features.users.model import Contact, User
from app.utils.pagination import PaginationParams

contacts_router = APIRouter()


@contacts_router.get("", response_model=list[schema.ContactRead])
async def list_contacts(
    response: Response,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Contacts.List)),
):
    query = db.query(Contact)
    results, total = refine_list_response(response, *ContactList(query, pagination))
    return results


def ContactList(query, pagination):
    # Minimal inline refine to avoid extra repo boilerplate
    start = pagination._start or 0
    end = pagination._end or 50
    sort = pagination._sort
    order = pagination._order

    if sort:
        col = getattr(Contact, sort, None)
        if col is not None:
            query = query.order_by(col.desc() if order == "DESC" else col.asc())

    total = query.count()
    items = query.offset(start).limit(end - start).all()
    return items, total


@contacts_router.get("/{contact_id}", response_model=ApiResponse[schema.ContactRead])
async def get_contact(
    contact_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Contacts.Show)),
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    return ApiResponse(data=contact)


@contacts_router.post("", response_model=ApiResponse[schema.ContactRead])
async def create_contact(
    payload: schema.ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Contacts.Create)),
):
    contact = Contact.model_validate(payload)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return ApiResponse(data=contact)


@contacts_router.patch("/{contact_id}", response_model=ApiResponse[schema.ContactRead])
async def update_contact(
    contact_id: str,
    payload: schema.ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Contacts.Update)),
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        return ApiResponse(data=None)

    updates = payload.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(contact, k, v)
    db.commit()
    db.refresh(contact)
    return ApiResponse(data=contact)


@contacts_router.delete("/{contact_id}", response_model=MessageResponse)
async def delete_contact(
    contact_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Contacts.Delete)),
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return MessageResponse(message="Contact deleted successfully")

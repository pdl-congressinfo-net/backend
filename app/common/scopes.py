from sqlalchemy.orm import Query, Session

from app.features.permissions.model import ObjectPermission
from app.features.users.model import User

ACTION_FIELD_MAP = {
    "show": ObjectPermission.can_show,
    "update": ObjectPermission.can_update,
    "delete": ObjectPermission.can_delete,
}


def has_object_permission(
    *,
    db: Session,
    user: User,
    resource: str,
    object_id: str,
    action: str,
) -> bool:
    column = ACTION_FIELD_MAP[action]

    return (
        db.query(ObjectPermission)
        .filter(
            ObjectPermission.user_id == user.id,
            ObjectPermission.resource == resource,
            ObjectPermission.object_id == object_id,
            column.is_(True),
        )
        .first()
        is not None
    )


def apply_object_scope(
    *,
    query: Query,
    user: User,
    resource: str,
    action: str,
    model,
):
    column = ACTION_FIELD_MAP[action]

    return query.join(
        ObjectPermission,
        ObjectPermission.object_id == model.id,
    ).filter(
        ObjectPermission.user_id == user.id,
        ObjectPermission.resource == resource,
        column.is_(True),
    )

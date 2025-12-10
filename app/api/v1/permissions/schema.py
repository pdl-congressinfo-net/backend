from pydantic import BaseModel


# =========================
# PERMISSION SCHEMAS
# =========================
class PermissionBase(BaseModel):
    name: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: str | None = None


class PermissionRead(PermissionBase):
    id: str

    class Config:
        from_attributes = True

from pydantic import BaseModel


# =========================
# ROLE SCHEMAS
# =========================
class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = None


class RoleRead(RoleBase):
    id: str

    class Config:
        from_attributes = True


# =========================
# ROLE PERMISSION SCHEMAS
# =========================
class RolePermissionCreate(BaseModel):
    role_id: str
    permission_id: str


class RolePermissionRead(BaseModel):
    role_id: str
    permission_id: str

    class Config:
        from_attributes = True

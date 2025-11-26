from pydantic import BaseModel


class RolePermissionBase(BaseModel):
    role_id: str
    permission_id: str


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionUpdate(BaseModel):
    role_id: str | None = None
    permission_id: str | None = None


class RolePermissionRead(RolePermissionBase):
    pass


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = None


class RoleRead(RoleBase):
    id: str
    name: str

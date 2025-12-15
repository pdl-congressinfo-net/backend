from pydantic import BaseModel, model_validator


# =========================
# PERMISSION SCHEMAS
# =========================
class PermissionBase(BaseModel):
    name: str


class PermissionCreate(BaseModel):
    name: str | None = None
    resource_name: str | None = None

    @model_validator(mode="after")
    def check_exactly_one_field(self):
        """Validate that exactly one of name or resource_name is provided."""
        if self.name and self.resource_name:
            raise ValueError("Provide either 'name' or 'resource_name', not both")
        if not self.name and not self.resource_name:
            raise ValueError("Either 'name' or 'resource_name' must be provided")
        return self


class PermissionUpdate(BaseModel):
    name: str | None = None


class PermissionRead(PermissionBase):
    id: str

    class Config:
        from_attributes = True

from datetime import datetime

from pydantic import BaseModel


class UserRoleBase(BaseModel):
    user_id: str
    role_id: str


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(BaseModel):
    user_id: str | None = None
    role_id: str | None = None


class UserRoleRead(UserRoleBase):
    class Config:
        from_attributes = True


class UserPermissionBase(BaseModel):
    user_id: str
    permission_id: str


class UserPermissionCreate(UserPermissionBase):
    pass


class UserPermissionUpdate(BaseModel):
    user_id: str | None = None
    permission_id: str | None = None


class UserPermissionRead(UserPermissionBase):
    class Config:
        from_attributes = True


class ContactBase(BaseModel):
    titles: str | None = None
    first_name: str
    last_name: str | None = None
    phone_number: str | None = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    titles: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None


class ContactRead(ContactBase):
    id: str | None = None
    email: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    contact: ContactCreate | None = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None
    contact: ContactUpdate | None = None


class UserRead(UserBase):
    id: str
    created_at: datetime
    last_login: datetime | None = None
    oeak_id: int | None = None
    contact: ContactRead | None = None

    class Config:
        from_attributes = True


class LoginOTPBase(BaseModel):
    user_id: str | None = None
    email: str
    otp_code: str
    created_at: datetime
    expires_at: datetime
    resend_available_at: datetime
    used: bool = False


class LoginOTPCreate(LoginOTPBase):
    pass


class LoginOTPUpdate(BaseModel):
    user_id: str | None = None
    email: str | None = None
    otp_code: str | None = None
    created_at: datetime | None = None
    expires_at: datetime | None = None
    resend_available_at: datetime | None = None
    used: bool | None = None


class LoginOTPRead(LoginOTPBase):
    id: str

    class Config:
        from_attributes = True

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
    id: str

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
    id: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    email: str | None = None
    full_name: str | None = None
    password: str | None = None


class UserRead(UserBase):
    id: str
    created_at: str
    last_login: str | None = None

    class Config:
        from_attributes = True


class LoginOTPBase(BaseModel):
    user_id: str | None = None
    email: str
    otp_code: str
    created_at: str
    expires_at: str
    resend_available_at: str
    used: bool = False


class LoginOTPCreate(LoginOTPBase):
    pass


class LoginOTPUpdate(BaseModel):
    user_id: str | None = None
    email: str | None = None
    otp_code: str | None = None
    created_at: str | None = None
    expires_at: str | None = None
    resend_available_at: str | None = None
    used: bool | None = None


class LoginOTPRead(LoginOTPBase):
    id: str

    class Config:
        from_attributes = True

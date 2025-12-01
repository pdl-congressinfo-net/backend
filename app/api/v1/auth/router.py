from datetime import datetime, timedelta

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from sqlmodel import select

from app.api.v1.auth.schema import MagicLoginRequest
from app.api.v1.permissions.schema import PermissionBase
from app.api.v1.users.schema import (
    UserCreate,
    UserLogin,
)
from app.common.deps import (
    check_permissions_role,
    check_permissions_user,
    get_current_user,
    get_db,
)
from app.core.config import settings
from app.core.mail import send_email
from app.core.security import (
    create_access_token,
    create_magic_link,
    decode_magic_token,
    generate_otp,
    get_password_hash,
    set_refresh_cookie,
    set_split_jwt_cookies,
    verify_password,
)
from app.features.users.model import LoginOTP, User

auth_router = APIRouter()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    """User registration endpoint"""
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    new_user = User(
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=get_password_hash(user_create.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"detail": "User registered successfully"}


@auth_router.post("/login")
async def login_user(
    response: Response, user_login: UserLogin, db: Session = Depends(get_db)
):
    """User login endpoint"""
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(days=7)

    access_token = create_access_token({"sub": user_login.email}, access_expires)
    refresh_token = create_access_token({"sub": user_login.email}, refresh_expires)

    set_split_jwt_cookies(response, access_token)
    set_refresh_cookie(response, refresh_token)

    user.last_login = datetime.utcnow()
    db.commit()

    return {"detail": "Login successful"}


@auth_router.post("/logout")
def logout(request: Request, response: Response):
    """
    Logout the user by clearing JWT cookies
    (hp + signature) and optional refresh token.
    """

    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        raise HTTPException(status_code=403, detail="CSRF protection")

    # Clear header.payload cookie
    response.delete_cookie(
        key="jwt_hp",
        httponly=False,
        secure=True,
        samesite="none",
    )

    # Clear signature cookie
    response.delete_cookie(
        key="jwt_sig",
        httponly=True,
        secure=True,
        samesite="none",
    )

    # If you also use a refresh token cookie:
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="none",
    )

    return {"detail": "Logged out"}


@auth_router.post("/request-otp")
async def request_otp(email: str, db: Session = Depends(get_db)):
    # Check recent OTP for resend limit
    statement = (
        select(LoginOTP)
        .where(LoginOTP.email == email)
        .order_by(LoginOTP.created_at.desc())
    )
    last_otp = db.exec(statement).first()

    if last_otp and last_otp.resend_available_at > datetime.utcnow():
        raise HTTPException(
            status_code=429, detail="Resend allowed only after 30 seconds"
        )

    otp = generate_otp()

    otp_entry = LoginOTP(
        email=email,
        otp_code=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=30),
        resend_available_at=datetime.utcnow() + timedelta(seconds=30),
    )
    db.add(otp_entry)
    db.commit()

    magic_token = create_magic_link(email, otp_entry.id)

    magic_link = f"https://192.168.1.42:5173/magic-login?token={magic_token}"

    await send_email(
        email_to=email,
        subject="Your Login OTP",
        html_content=f"""
        Your OTP is: {otp}

        Or click here to login without typing the code:
        {magic_link}

        This link and OTP expire in 2 minutes.
        """,
    )

    return {"detail": "OTP sent"}


@auth_router.post("/verify-otp")
async def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    statement = (
        select(LoginOTP)
        .where(
            LoginOTP.email == email, LoginOTP.otp_code == otp, LoginOTP.used == False
        )
        .order_by(LoginOTP.created_at.desc())
    )

    otp_entry = db.exec(statement).first()

    if not otp_entry:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    # otp_entry.used = True
    db.add(otp_entry)
    db.commit()


@auth_router.post("/magic-login")
async def magic_login(request: MagicLoginRequest, db: Session = Depends(get_db)):
    data = decode_magic_token(request.token)
    if not data:
        raise HTTPException(status_code=400, detail="Invalid or expired link")

    otp_entry = db.get(LoginOTP, data["otp_id"])
    if not otp_entry or otp_entry.used:
        raise HTTPException(status_code=400, detail="Invalid or used link")
    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Link expired")

    otp_entry.used = True
    db.commit()

    access_expires = timedelta(minutes=15)
    refresh_expires = timedelta(days=7)

    access_token = create_access_token({"sub": data["email"]}, access_expires)
    refresh_token = create_access_token({"sub": data["email"]}, refresh_expires)

    response = Response()
    set_refresh_cookie(response, refresh_token)
    set_split_jwt_cookies(response, access_token)
    return response


@auth_router.post("/refresh")
async def refresh_token(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = decode_magic_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload["sub"]

    access_expires = timedelta(minutes=15)
    refresh_expires = timedelta(days=7)

    access_token = create_access_token({"sub": email}, access_expires)
    refresh_token = create_access_token({"sub": email}, refresh_expires)

    response = Response()
    set_refresh_cookie(response, refresh_token)
    set_split_jwt_cookies(response, access_token)
    return response


@auth_router.post("/permissions")
async def get_current_user_permissions(
    permission: PermissionBase,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user:
        return check_permissions_user(user, [permission.permission])
    else:
        return check_permissions_role("guest", [permission.permission], db)

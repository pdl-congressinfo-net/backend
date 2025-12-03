import json
import os
import random
from datetime import datetime, timedelta

from cryptography.fernet import Fernet
from fastapi import Response
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def test_password_hashing():
    plain_password = "superduper"
    hashed_password = get_password_hash(plain_password)
    assert verify_password(plain_password, hashed_password) == True
    assert verify_password("wrongpassword", hashed_password) == False


test_password_hashing()

FERNET_KEY = os.environ.get("FERNET_KEY") or Fernet.generate_key()
fernet = Fernet(FERNET_KEY)


def generate_otp():
    return f"{random.randint(100000, 999999)}"


def create_magic_link(email: str, otp_id: str):
    payload = {
        "email": email,
        "otp_id": otp_id,
        "expires_at": (datetime.utcnow() + timedelta(minutes=2)).isoformat(),
    }
    token = fernet.encrypt(json.dumps(payload).encode()).decode()
    return token


def decode_magic_token(token: str):
    try:
        decrypted = fernet.decrypt(token.encode(), ttl=120)
        data = json.loads(decrypted)
        print("Decoded token data:", data)
        return data
    except Exception as e:
        print("Failed to decode token:", e)
        return None


def set_refresh_cookie(response: Response, refresh_token: str):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )


def set_split_jwt_cookies(response: Response, token: str):
    header, payload, signature = token.split(".")
    hp = f"{header}.{payload}"

    # JavaScript-readable part of the token
    response.set_cookie(
        key="jwt_hp",
        value=hp,
        httponly=False,
        secure=True,
        samesite="none",
        max_age=60 * 15,
    )

    # Signature stored separately (HTTPOnly)
    response.set_cookie(
        key="jwt_sig",
        value=signature,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 15,
    )

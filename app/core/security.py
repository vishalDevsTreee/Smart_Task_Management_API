from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
import hashlib
import bcrypt


_BCRYPT_SHA256_PREFIX = "bcrypt-sha256$"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash(password: str) -> str:
    password_bytes = hashlib.sha256(password.encode("utf-8")).digest()
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return f"{_BCRYPT_SHA256_PREFIX}{hashed.decode('ascii')}"


def verify(plain_password: str, hashed_password: str) -> bool:
    if hashed_password.startswith(_BCRYPT_SHA256_PREFIX):
        password_bytes = hashlib.sha256(plain_password.encode("utf-8")).digest()
        stored_hash = hashed_password.removeprefix(_BCRYPT_SHA256_PREFIX)
    else:
        password_bytes = plain_password.encode("utf-8")
        stored_hash = hashed_password

    return bcrypt.checkpw(password_bytes, stored_hash.encode("ascii"))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    return user_id
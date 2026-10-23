import hashlib

import bcrypt


_BCRYPT_SHA256_PREFIX = "bcrypt-sha256$"


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

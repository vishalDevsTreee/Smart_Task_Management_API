from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.auth import models
from app.core import security
from app.database import get_db

def create_user(data, db):
    hashed_password = security.hash(data.password)
    data.password = hashed_password
    new_user =models.User(
        name =data.name,
        email =data.email,
        password =hashed_password
    )
    if new_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User Already Exists")
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login(user_credentials, db):
    user =db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    if not security.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    access_token = security.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}
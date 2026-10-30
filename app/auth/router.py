from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.auth import schemas, service


router = APIRouter(tags=["Authentication"])


@router.post("/", status_code=status.HTTP_201_CREATED,
                  response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, 
                db: Session=Depends(get_db)):
    
    return service.create_user(user, db)

@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return service.login(user_credentials, db)
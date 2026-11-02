from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.Dashboard import schemas, service
from app.core import dependencies
from app.project_management import models


router = APIRouter(tags=["Dashboard"])

#@router.get("/api/projects/all")
#def get_projects(db: Session=Depends(get_db),
#                 current_user =Depends(dependencies.get_current_user)):
#    return service.get_projects(db, current_user)



@router.get("/api/tasks/dashboard", response_model= schemas.DashboardResponse)
def get_dashboard(db: Session=Depends(get_db),
                  current_user =Depends(dependencies.get_current_user)):
    return service.get_dashboard(db, current_user)


from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.project_management import schemas, service
from app.core import dependencies

router =APIRouter(tags=["Project Management"])



@router.post("/projects", status_code=status.HTTP_201_CREATED, response_model=schemas.ProjectOut)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(dependencies.get_current_user)):

    return service.create_project(project, db, current_user)



@router.get("/retrieve/projects", status_code=status.HTTP_201_CREATED,
            response_model=list[schemas.ProjectOut])
def get_projects(db: Session=Depends(get_db),
                current_user =Depends(dependencies.get_current_user)):

    return service.get_projects(db, current_user)



@router.get("/projects/id", status_code=status.HTTP_201_CREATED,
            response_model=list[schemas.ProjectOut])
def get_project_byID(project_id: int,
                     db: Session=Depends(get_db)):
    
    return service.get_project_byID(project_id, db)



@router.post("/project/id", response_model=schemas.ProjectOut)
def update_project(project_id: int,
                   update: schemas.ProjectUpdate,
                   db: Session=Depends(get_db),
                   current_user =Depends(dependencies.get_current_user)):
    
    return service.update_project(project_id, update, db, current_user)



@router.delete("/project/id")
def delete_project(project_id: int,
                   db: Session=Depends(get_db),
                   current_user =Depends(dependencies.get_current_user)):
    
    return service.delete_project(project_id, db, current_user)




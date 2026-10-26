from .. import schemas, models, oauth2
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(tags=["Project Management"])


@router.post("/projects", status_code=status.HTTP_201_CREATED, response_model=schemas.ProjectOut)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    existing_project = db.query(models.Project).filter(models.Project.owner_id == current_user.id,
                                                       models.Project.name == project.name).first()
    if existing_project:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Project Already Exists")
    new_project = models.Project(name=project.name,
                                 description=project.description,
                                 owner_id=current_user.id,
                                 due_date=project.due_date)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/retrieve/projects", status_code=status.HTTP_201_CREATED,
            response_model=list[schemas.ProjectOut])
def get_projects(db: Session=Depends(get_db),
                      current_user =Depends(oauth2.get_current_user)):
    user =db.query(models.Project).filter(models.Project.owner_id == current_user.id).all()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"User is not logged in")
    return user 

@router.get("/projects/id", status_code=status.HTTP_201_CREATED,
            response_model=list[schemas.ProjectOut])
def get_project_byID(project_id: int,
                     db: Session=Depends(get_db),
                     current_user =Depends(oauth2.get_current_user)):
    user =db.query(models.Project).filter(models.Project.id == project_id).all()
    return user

@router.post("/project/id", response_model=schemas.ProjectOut)
def update_project(project_id: int,
                   update: schemas.ProjectUpdate,
                   db: Session=Depends(get_db),
                   current_user =Depends(oauth2.get_current_user)):

    query = db.query(models.Project).filter(models.Project.id == project_id,
                                            models.Project.owner_id == current_user.id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"User is not logged in!")
    query.name = update.name
    query.description = update.description
    query.status = update.status
    query.due_date = update.due_date

    db.commit()
    db.refresh(query)

    return query

@router.delete("/project/id")
def delete_project(project_id: int,
                   db: Session=Depends(get_db),
                   current_user =Depends(oauth2.get_current_user)):

    project =db.query(models.Project).filter(models.Project.id == project_id,
                                             models.Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with id {project_id} not found")

    db.delete(project)
    db.commit()
    return {"Message": f"Project with id {project_id} deleted successfully"}



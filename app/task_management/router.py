from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.task_management import schemas, service
from app.core import dependencies

router =APIRouter(tags=["Task Management"])



@router.post("/api/projects/{project_id}/tasks", status_code=status.HTTP_201_CREATED,
             response_model=schemas.TaskResponse)
def create_task(project_id: int,
                task: schemas.TaskCreate,
                db: Session=Depends(get_db),
                current_user = Depends(dependencies.get_current_user)):

    return service.create_task(project_id, task, db, current_user)



@router.get("/api/projects/tasks", response_model=list[schemas.TaskResponse])
def get_task(skip: int = Query(default=0, ge=0),
             limit: int = Query(default=10, ge=1, le=100),
             db: Session = Depends(get_db),
             current_user = Depends(dependencies.get_current_user)):

    return service.get_task(skip, limit, db, current_user)



@router.post("/api/projects/update/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int,
                task: schemas.TaskUpdate,
                db: Session = Depends(get_db), 
                current_user = Depends(dependencies.get_current_user)):

    return service.update_task(task_id, task, db, current_user)



@router.delete("/api/delete/task/{task_id}")
def delete_task(task_id: int,
                db: Session =Depends(get_db),
                current_user =Depends(dependencies.get_current_user)):

    return service.delete_task(task_id, db, current_user)



@router.get("/api/tasks", response_model=list[schemas.TaskResponse])
def get_task_by_status(task_status: schemas.TaskStatus| None = Query(default=None),
                       skip: int = Query(default=0, ge=0),
                       limit: int = Query(default=10, ge=1, le=100),
                       db: Session=Depends(get_db),
                       current_user = Depends(dependencies.get_current_user)):

    return service.get_task_by_status(task_status, skip, limit, db, current_user)



@router.get("/api/tasks/priority", response_model=list[schemas.TaskResponse])
def get_task_by_priority(priority: schemas.TaskPriority| None = Query(default=None),
                         skip: int = Query(default=0, ge=0),
                         limit: int = Query(default=10, ge=1, le=100),
                         db: Session=Depends(get_db),
                         current_user =Depends(dependencies.get_current_user)):

    return service.get_task_by_priority(priority, skip, limit, db, current_user)



@router.get("/api/task/{project_id}", response_model=list[schemas.TaskResponse])
def get_task_by_project(project_id: int,
                        skip: int = Query(default=0, ge=0),
                        limit: int = Query(default=10, ge=1, le=100),
                        db: Session=Depends(get_db),
                        current_user =Depends(dependencies.get_current_user)):

    return service.get_task_by_project(project_id, skip, limit, db, current_user)



@router.get("/api/task", response_model=schemas.TaskResponse)
def get_task_by_title(title: str = Query(min_length=1, max_length=100), 
                      db: Session=Depends(get_db),
                      current_user =Depends(dependencies.get_current_user)):

    return service.get_task_by_title(title, db, current_user)


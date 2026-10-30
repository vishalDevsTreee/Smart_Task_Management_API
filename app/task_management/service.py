from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.task_management import models
from app.core import security
from app.database import get_db

def create_task(project_id, task, db, current_user):
    project =db.query(models.Project).filter(models.Project.owner_id == current_user.id,
                                             models.Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project not found")

    new_task =models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        project_id=project_id,
        owner_id=current_user.id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task



def get_task(skip, limit, db, current_user):
    task =db.query(models.Task).filter(models.Task.owner_id == current_user.id).order_by(
        models.Task.id
    ).offset(skip).limit(limit).all()
        
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Task Found")

    return task[skip:skip + limit]



def update_task(task_id, task, db, current_user):
    updated_task =db.query(models.Task).filter(models.Task.id == task_id,
                                               models.Task.owner_id == current_user.id).first()
        
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Task Found")
    
    updated_task.status=task.status
    updated_task.priority=task.priority
    
    db.commit()
    db.refresh(updated_task)

    return updated_task



def delete_task(task_id, db, current_user):
    delete_task =db.query(models.Task).filter(models.Task.id == task_id,
                                              models.Task.owner_id == current_user.id).first()
    
    if not delete_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task Not Found")
    
    db.delete(delete_task)
    db.commit()
    
    return {"Message": f"Task with id {task_id} deleted successfully"}



def get_task_by_status(task_status, skip, limit, db, current_user):
    task =db.query(models.Task).filter(models.Task.owner_id == current_user.id,
                                       models.Task.status == task_status).order_by(
                                           models.Task.id
                                       ).offset(skip).limit(limit).all()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task Not Found")

    return task



def get_task_by_priority(priority, skip, limit, db, current_user):
    task =db.query(models.Task).filter(models.Task.owner_id == current_user.id,
                                       models.Task.priority == priority).order_by(
                                           models.Task.id
                                       ).offset(skip).limit(limit).all()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task Not Found")

    return task



def get_task_by_project(project_id, skip, limit, db, current_user):
    task =db.query(models.Task).filter(models.Task.project_id == project_id,
                                       models.Task.owner_id == current_user.id).order_by(
                                           models.Task.id
                                       ).offset(skip).limit(limit).all()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Task Not Found")

    return task



def get_task_by_title(title, db, current_user):
    task =db.query(models.Task).filter(models.Task.title == title,
                                       models.Task.owner_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task Not Found")

    return task
    




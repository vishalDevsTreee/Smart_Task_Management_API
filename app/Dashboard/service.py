from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.project_management import models as project_models
from app.task_management import models as task_models
from app.core import security
from app.database import get_db

from datetime import datetime, timezone



def get_dashboard(db, current_user):
    return{
        "total_projects": count_projects(db, current_user),
        "total_tasks": count_tasks(db, current_user),
        "completed_tasks": count_completed_tasks(db, current_user),
        "pending_tasks": count_pending_tasks(db, current_user),
        "inprogress_tasks": count_inprogress_tasks(db, current_user),
        "overdue_tasks": count_overdue_tasks(db, current_user)
    }



def count_projects(db, current_user):
    projects =db.query(project_models.Project).filter(project_models.Project.owner_id == current_user.id).count()
                           
    return projects



def count_tasks(db, current_user):
    task =db.query(task_models.Task).filter(task_models.Task.owner_id == current_user.id).count()

    return task



def count_completed_tasks(db, current_user):
    task =db.query(task_models.Task).filter(task_models.Task.owner_id == current_user.id,
                                            task_models.Task.status == task_models.ProjectStatus.COMPLETED).count()

    return task 



def count_pending_tasks(db, current_user):
    task =db.query(task_models.Task).filter(task_models.Task.owner_id == current_user.id,
                                            task_models.Task.status == task_models.ProjectStatus.PENDING).count()

    return task



def count_inprogress_tasks(db, current_user):
    task =db.query(task_models.Task).filter(task_models.Task.owner_id == current_user.id,
                                            task_models.Task.status == task_models.ProjectStatus.INPROGRESS).count()

    return task



def count_overdue_tasks(db, current_user):
    now = datetime.now(timezone.utc)
    task =db.query(task_models.Task).filter(task_models.Task.owner_id == current_user.id,
                                            task_models.Task.due_date < now,
                                            task_models.Task.status != task_models.ProjectStatus.COMPLETED).count()
    
    return task





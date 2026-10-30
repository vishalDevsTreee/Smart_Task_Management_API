from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from .models import ProjectPriority, ProjectStatus
import enum




class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PENDING
    priority: ProjectPriority = ProjectPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: ProjectStatus
    priority: ProjectPriority
    project_id: int
    owner_id: int
    created_at: datetime
    due_date: datetime | None

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    status: ProjectStatus = ProjectStatus.PENDING
    priority: ProjectPriority = ProjectPriority.MEDIUM

class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    INPROGRESS = "INPROGRESS"
    COMPLETED = "COMPLETED"

class TaskPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"



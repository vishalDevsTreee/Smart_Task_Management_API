from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func, Enum
import enum
from datetime import datetime

class ProjectStatus(str, enum.Enum):
    PENDING ="PENDING"
    INPROGRESS ="INPROGRESS"
    COMPLETED ="COMPLETED"

class ProjectPriority(str, enum.Enum):
    LOW ="LOW"
    MEDIUM ="MEDIUM"
    HIGH ="HIGH"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(ProjectStatus, name="task_status"),
        nullable=False,
        default=ProjectStatus.PENDING,
        server_default=ProjectStatus.PENDING.value,
    )
    priority = Column(
        Enum(ProjectPriority, name="task_priority"),
        nullable=False,
        default=ProjectPriority.MEDIUM,
        server_default=ProjectPriority.MEDIUM.value,
    )
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    due_date = Column(DateTime(timezone=True), nullable=True)

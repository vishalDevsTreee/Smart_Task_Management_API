from .database import Base
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, func

class User(Base):
    __tablename__ ="users"

    id = Column(Integer, primary_key=True, nullable=False)
    name =Column(String, nullable=False)
    email =Column(String, nullable=False)
    password =Column(String, nullable=False)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(120), nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), nullable=False, server_default="active")
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
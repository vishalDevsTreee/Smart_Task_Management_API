from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional




class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = None
    due_date: Optional[date] = None



class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    status: str
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



class ProjectUpdate(BaseModel):
    name: str
    description: str
    status: str
    due_date: Optional[date]
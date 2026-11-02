from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total_projects: int
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    inprogress_tasks: int 
    overdue_tasks: int

    class Config:
        from_attributes = True
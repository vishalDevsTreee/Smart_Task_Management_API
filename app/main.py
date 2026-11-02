from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.project_management.router import router as project_management_router
from app.task_management.router import router as task_management_router
from app.Dashboard.router import router as dashboard_router

app = FastAPI(title="Smart Task Management API")



app.include_router(auth_router)
app.include_router(project_management_router)
app.include_router(task_management_router)
app.include_router(dashboard_router)


@app.get("/")
def read_root():
    return {"message": "Smart Task Management API"}


from fastapi import FastAPI
from .database import engine
import time 
from time import sleep
import psycopg2
from psycopg2.extras import RealDictCursor
from app.auth.router import router as auth_router
from app.project_management.router import router as project_management_router
from app.task_management.router import router as task_management_router


while True:
        try:
            conn =psycopg2.connect(host='localhost', database='Smart_Task_Management',
                                    user='postgres', password='123', 
                                    cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("Database connected successfully")
            break
        except Exception as error:
            print("connection to database failed")
            print("Error:", error)
            time.sleep(2)

app = FastAPI(title="Smart Task Management API")

app.include_router(auth_router)
app.include_router(project_management_router)
app.include_router(task_management_router)


@app.get("/")
def read_root():
    return {"message": "Smart Task Management API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

from fastapi import FastAPI
from .database import engine
from time import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .routers import user


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
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "Smart Task Management API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

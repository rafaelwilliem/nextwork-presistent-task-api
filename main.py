from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from database import (
    create_task_record,
    get_task_record,
    initialize_database,
    list_task_records,
    update_task_record,
)

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)

class TaskUpdate(BaseModel):
    completed: bool

class Task(BaseModel):
    id: int
    title: str
    completed: bool

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(title="Task API", version="0.0.1", lifespan=lifespan)

# app = FastAPI(title="Task API", version="0.0.1")

# tasks = [
#     {
#         "id": 1,
#         "title": "Try the task API",
#         "completed": False
#     }
# ]

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/tasks", response_model=list[Task])
def list_tasks() -> Any:
    return list_task_records()

@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED
)

def create_task(task : TaskCreate) -> Any:
    return create_task_record(task.title)
# def create_task(task: TaskCreate) -> dict[str,Any]:
#     new_task = {
#         "id": len(tasks) + 1,
#         "title": task.title,
#         "completed": False,
#     }
#     tasks.append(new_task)
#     return new_task

# @app.post(
#     "/tasks",
#     response_model=Task,
#     status_code=status.HTTP_201_CREATED
# )
# def create_task(task : TaskCreate) -> dict[str, Any]:
#     new_task = {
#         "id" : len(task) + 1,
#     }

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Any:
    task = get_task_record(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task
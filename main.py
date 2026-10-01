from typing import Any

from fastapi import FastAPI, status
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)

class Task(BaseModel):
    id: int
    title: str
    completed: bool

app = FastAPI(title="Task API", version="0.0.1")

tasks = [
    {
        "id": 1,
        "title": "Try the task API",
        "completed": False
    }
]

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[dict[str, Any]]:
    return tasks

@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate) -> dict[str,Any]:
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "completed": False,
    }
    tasks.append(new_task)
    return new_task

@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED
)
def create_task(task : TaskCreate) -> dict[str, Any]:
    new_task = {
        "id" : len(tasks) + 1,
    }
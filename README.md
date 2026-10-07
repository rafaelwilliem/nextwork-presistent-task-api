# Persistent Task API

A small FastAPI backend that validates task data, persists it in SQLite, and exposes an interactive API contract.

## Features

- Health check
- Create and list tasks
- Retrieve a task by ID
- Mark a task complete or incomplete
- Pydantic request and response validation
- SQLite persistence across server restarts
- Structured 404 responses

## Tech stack

- Python 3.10+
- FastAPI 0.141.1
- Pydantic 2.13.5
- SQLite through Python's `sqlite3` module

## API routes

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/health` | Check that the API is running |
| GET | `/tasks` | List every task |
| POST | `/tasks` | Create a task |
| GET | `/tasks/{task_id}` | Retrieve one task |
| PATCH | `/tasks/{task_id}` | Change a task's completion state |

Example create request:

```json
{
  "title": "Write API documentation"
}
```

Example update request:

```json
{
  "completed": true
}
```

## Backend concepts demonstrated

This project demonstrates routing, request validation, response schemas, HTTP status codes, application lifespan, SQL parameter binding, transactions, persistence, and API documentation.
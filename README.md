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
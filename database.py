import sqlite3
from typing import Any

DATABASE_PATH = "task.db"

def get_connection () -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def row_to_task(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "is_completed": bool(row["is_completed"])
    }

def initialize_database() -> None:
    connection = get_connection()
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            completed INTEGER NOT NULL DEFAULT 0
                CHECK (completed IN (0,1))
            )
            """
        )
        connection.commit()
    finally:
        connection.close()

def create_task_record(title:str) -> dict[str, Any]:
    connection = get_connection()
    try:
        cursor = connection.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,),
        )
        connection.commit()
        row = connection.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()
        if row is None:
            raise RuntimeError("Task was created but could not be loaded")
        return row_to_task(row)
    finally:
        connection.close
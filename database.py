from typing import final
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
        "completed": bool(row["completed"])
    }

def initialize_database() -> None:
    connection = get_connection()
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
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
        connection.close()

def list_task_records (completed: bool | None = None) -> list[dict[str, Any]]:
    connection = get_connection()
    try:
        if completed is None:
            rows = connection.execute(
                "SELECT id, title, completed FROM tasks ORDER BY id"
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT id,title,completed
                FROM tasks
                WHERE completed = ?
                ORDER BY id
                """, (int(completed),),
            ).fetchall()
        return [row_to_task(row) for row in rows]
    finally:
        connection.close()

def get_task_record(task_id: int) -> dict[str, Any] | None:
    connection = get_connection()
    try:
        row = connection.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
        return row_to_task(row) if row is not None else None
    finally:
        connection.close()

def update_task_record (task_id:int, completed:bool) -> dict[str, Any] | None :
    connection = get_connection()
    try :
        cursor = connection.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (int(completed), task_id),
        )
        connection.commit()
        if cursor.rowcount == 0:
            return None
        row = connection.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
        return row_to_task(row) if row is not None else None
    finally :
        connection.close()
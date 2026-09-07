import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "app.db"
INIT_SQL_PATH = BASE_DIR / "data" / "init.sql"


def init_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    sql = INIT_SQL_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.executescript(sql)
        connection.commit()


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

# database.py
import sqlite3
from contextlib import contextmanager

DB_PATH = "app.db"


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def column_exists(conn, table: str, column: str) -> bool:
    cursor = conn.execute(f"PRAGMA table_info({table})")
    return any(row["name"] == column for row in cursor.fetchall())


def is_not_null(conn, table: str, column: str) -> bool:
    cursor = conn.execute(f"PRAGMA table_info({table})")
    for row in cursor.fetchall():
        if row["name"] == column:
            return row["notnull"] == 1
    return False


def rebuild_queries_table(conn):

    conn.execute("ALTER TABLE queriesnew RENAME TO queriesnew_old")

    conn.execute("""
    CREATE TABLE queriesnew (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        query_text TEXT NOT NULL,
        response_text TEXT NOT NULL,
        video_url TEXT,
        language TEXT,
        class_name TEXT,
        subject_name TEXT,
        chapter_name TEXT,
        video_id TEXT,
        feedback TEXT
    )
    """)

    conn.execute("""
    INSERT INTO queriesnew (
        id, query_text, response_text, video_url,
        language, class_name, subject_name,
        chapter_name, video_id, feedback
    )
    SELECT
        id, query_text, response_text, video_url,
        language, class_name, subject_name,
        chapter_name, video_id, feedback
    FROM queriesnew_old
    """)

    conn.execute("DROP TABLE queriesnew_old")
    conn.commit()


def init_db():

    with get_db() as conn:

        # 1 Queries table

        conn.execute("""
        CREATE TABLE IF NOT EXISTS queriesnew (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            query_text TEXT NOT NULL,
            response_text TEXT NOT NULL,
            video_url TEXT,
            language TEXT,
            class_name TEXT,
            subject_name TEXT,
            chapter_name TEXT,
            video_id TEXT,
            feedback TEXT
        )
        """)

        # 2 Users table

        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            credits INTEGER DEFAULT 10,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 3 Credits wallet table

        conn.execute("""
        CREATE TABLE IF NOT EXISTS credits (
            user_id TEXT PRIMARY KEY,
            totalcredits INTEGER DEFAULT 0,
            usedcredits INTEGER DEFAULT 0,
            balance INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 4 Payments history table

        conn.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            credits INTEGER,
            usedcredits INTEGER,
            balance INTEGER,
            payment_id TEXT,
            amount INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()

        # Auto add columns if missing

        if not column_exists(conn, "queriesnew", "user_id"):
            conn.execute("ALTER TABLE queriesnew ADD COLUMN user_id TEXT")

        if not column_exists(conn, "queriesnew", "video_id"):
            conn.execute("ALTER TABLE queriesnew ADD COLUMN video_id TEXT")

        if not column_exists(conn, "queriesnew", "feedback"):
            conn.execute("ALTER TABLE queriesnew ADD COLUMN feedback TEXT")

        conn.commit()

        # Fix old DB constraint

        if is_not_null(conn, "queriesnew", "video_url"):
            print("Fixing NOT NULL constraint on video_url")
            rebuild_queries_table(conn)

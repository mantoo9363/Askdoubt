
# database.py
#import sqlite3
#from contextlib import contextmanager

#DB_PATH = "app.db"


#@contextmanager
#def get_db():
 #   conn = sqlite3.connect(DB_PATH)
  #  conn.row_factory = sqlite3.Row
   # try:
    #    yield conn
    #finally:
     #   conn.close()


#def column_exists(conn, table: str, column: str) -> bool:
 #   cursor = conn.execute(f"PRAGMA table_info({table})")
  #  return any(row["name"] == column for row in cursor.fetchall())


#def is_not_null(conn, table: str, column: str) -> bool:
 #   cursor = conn.execute(f"PRAGMA table_info({table})")
  #  for row in cursor.fetchall():
   #     if row["name"] == column:
    #        return row["notnull"] == 1
    #return False


#def rebuild_queries_table(conn):

 #   conn.execute("ALTER TABLE queriesnew RENAME TO queriesnew_old")

  #  conn.execute("""
   # CREATE TABLE queriesnew (
    #    id INTEGER PRIMARY KEY AUTOINCREMENT,
     #   user_id TEXT,
      #  query_text TEXT NOT NULL,
       # response_text TEXT NOT NULL,
       # video_url TEXT,
       # language TEXT,
       # class_name TEXT,
       # subject_name TEXT,
       # chapter_name TEXT,
       # video_id TEXT,
       # feedback TEXT
    #)
    #""")

    #conn.execute("""
    #INSERT INTO queriesnew (
     #   id, query_text, response_text, video_url,
      #  language, class_name, subject_name,
      #  chapter_name, video_id, feedback
    #)
    #SELECT
     #   id, query_text, response_text, video_url,
      #  language, class_name, subject_name,
      #  chapter_name, video_id, feedback
    #FROM queriesnew_old
    #""")

    #conn.execute("DROP TABLE queriesnew_old")
    #conn.commit()


#def init_db():

 #   with get_db() as conn:

        # 1 Queries table

  #      conn.execute("""
   #     CREATE TABLE IF NOT EXISTS queriesnew (
    #        id INTEGER PRIMARY KEY AUTOINCREMENT,
     #       user_id TEXT,
      #      query_text TEXT NOT NULL,
       #     response_text TEXT NOT NULL,
        #    video_url TEXT,
         #   language TEXT,
        #    class_name TEXT,
         #   subject_name TEXT,
         #   chapter_name TEXT,
         #   video_id TEXT,
         #   feedback TEXT
        #)
       # """)

        # 2 Users table

       # conn.execute("""
       # CREATE TABLE IF NOT EXISTS users (
        #    user_id TEXT PRIMARY KEY,
         #   credits INTEGER DEFAULT 10,
          #  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        #)
       # """)

        # 3 Credits wallet table

       # conn.execute("""
       # CREATE TABLE IF NOT EXISTS credits (
        #    user_id TEXT PRIMARY KEY,
         #   totalcredits INTEGER DEFAULT 0,
          #  usedcredits INTEGER DEFAULT 0,
           # balance INTEGER DEFAULT 0,
           # updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        #)
       # """)

        # 4 Payments history table

       # conn.execute("""
        #CREATE TABLE IF NOT EXISTS payments (
      #      id INTEGER PRIMARY KEY AUTOINCREMENT,
       #     user_id TEXT,
        #    credits INTEGER,
         #   usedcredits INTEGER,
          #  balance INTEGER,
           # payment_id TEXT,
          #  amount INTEGER,
          #  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       # )
      #  """)

       # conn.commit()

        # Auto add columns if missing

      #  if not column_exists(conn, "queriesnew", "user_id"):
       #     conn.execute("ALTER TABLE queriesnew ADD COLUMN user_id TEXT")

      #  if not column_exists(conn, "queriesnew", "video_id"):
       #     conn.execute("ALTER TABLE queriesnew ADD COLUMN video_id TEXT")

      #  if not column_exists(conn, "queriesnew", "feedback"):
       #     conn.execute("ALTER TABLE queriesnew ADD COLUMN feedback TEXT")

      #  conn.commit()

        # Fix old DB constraint

       # if is_not_null(conn, "queriesnew", "video_url"):
        #    print("Fixing NOT NULL constraint on video_url")
         #   rebuild_queries_table(conn)
#=======================================new code ===27 mar 2026===========================================

# database.py
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


# =========================
# REBUILD TABLE (FIXED)
# =========================
def rebuild_queries_table(conn):

    conn.execute("ALTER TABLE queriesnew RENAME TO queriesnew_old")

    conn.execute("""
    CREATE TABLE queriesnew (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,

        name TEXT,
        email TEXT,
        mobile_number TEXT,

        query_text TEXT NOT NULL,
        response_text TEXT NOT NULL,

        video_url TEXT,
        language TEXT,
        llm_type TEXT,
        is_retrieved INTEGER DEFAULT 0,

        class_name TEXT,
        subject_name TEXT,
        chapter_name TEXT,

        video_id TEXT,
        feedback TEXT
    )
    """)

    # 🔥 FIXED INSERT (NO DATA LOSS)
    conn.execute("""
    INSERT INTO queriesnew (
        id, user_id, name, email, mobile_number,
        query_text, response_text, video_url,
        language, llm_type, is_retrieved,
        class_name, subject_name, chapter_name,
        video_id, feedback
    )
    SELECT
        id, user_id, name, email, mobile_number,
        query_text, response_text, video_url,
        language, llm_type, is_retrieved,
        class_name, subject_name, chapter_name,
        video_id, feedback
    FROM queriesnew_old
    """)

    conn.execute("DROP TABLE queriesnew_old")
    conn.commit()


# =========================
# INIT DB
# =========================
def init_db():

    with get_db() as conn:

        # =========================
        # QUERIES TABLE
        # =========================
        conn.execute("""
        CREATE TABLE IF NOT EXISTS queriesnew (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,

            name TEXT,
            email TEXT,
            mobile_number TEXT,

            query_text TEXT NOT NULL,
            response_text TEXT NOT NULL,

            video_url TEXT,
            language TEXT,
            llm_type TEXT,
            is_retrieved INTEGER DEFAULT 0,

            class_name TEXT,
            subject_name TEXT,
            chapter_name TEXT,

            video_id TEXT,
            feedback TEXT
        )
        """)

        # =========================
        # USERS TABLE
        # =========================
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            credits INTEGER DEFAULT 10,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # =========================
        # CREDITS TABLE (ALIGNED)
        # =========================
        conn.execute("""
        CREATE TABLE IF NOT EXISTS credits (
            user_id TEXT PRIMARY KEY,
            totalcredits INTEGER DEFAULT 0,
            usedcredits INTEGER DEFAULT 0,
            balance INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # =========================
        # PAYMENTS TABLE
        # =========================
        conn.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT,

            name TEXT,
            email TEXT,
            mobile_number TEXT,

            amount INTEGER,
            cgst REAL,
            sgst REAL,
            total_amount INTEGER,

            credits INTEGER,

            razorpay_order_id TEXT,
            razorpay_payment_id TEXT,
            razorpay_signature TEXT,

            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()

        # =========================
        # AUTO ADD COLUMNS
        # =========================

        for col in ["name", "email", "mobile_number", "llm_type", "video_id", "feedback"]:
            if not column_exists(conn, "queriesnew", col):
                conn.execute(f"ALTER TABLE queriesnew ADD COLUMN {col} TEXT")

        if not column_exists(conn, "queriesnew", "is_retrieved"):
            conn.execute("ALTER TABLE queriesnew ADD COLUMN is_retrieved INTEGER DEFAULT 0")

        conn.commit()

        # =========================
        # FIX OLD DB
        # =========================
        if is_not_null(conn, "queriesnew", "video_url"):
            print("Fixing NOT NULL constraint on video_url")
            rebuild_queries_table(conn)

        # =========================
        # PERFORMANCE INDEX
        # =========================
        conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_queries
        ON queriesnew(query_text, language, llm_type)
        """)

        conn.commit()






#==========================================================end code=============================================
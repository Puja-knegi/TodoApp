import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.exc import OperationalError
from app.db.session import Base, engine
from app.models import user
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "todoapp")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def create_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"✅ Database '{DB_NAME}' created.")
        else:
            print(f"ℹ️ Database '{DB_NAME}' already exists.")
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Error creating database:", e)

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully.")
    except OperationalError as e:
        print("❌ SQLAlchemy connection error:", e)

if __name__ == "__main__":
    try:
        create_database()
        create_tables()
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
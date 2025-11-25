import os
from pathlib import Path
from contextlib import contextmanager
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)


def get_database_url() -> str:
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME")

    if not all([user, password, db]):
        raise RuntimeError("Variáveis de ambiente do banco não configuradas.")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


DATABASE_URL = get_database_url()

engine: Engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=5,
    future=True,
    pool_pre_ping=True,
)


@contextmanager
def get_connection() -> Generator[Connection, None, None]:
    conn: Connection = engine.connect()
    trans = conn.begin()
    
    try:
        yield conn
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    finally:
        conn.close()
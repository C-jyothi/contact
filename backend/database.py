
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Local database by default.
# Render can provide another database location.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./contacts.db"
)

# SQLite needs this setting when used with FastAPI.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Creates database sessions.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database tables.
Base = declarative_base()


# Provides a database session to an API request.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

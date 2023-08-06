import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DOKER_DATABASE_URL = os.getenv('DATABASE_URL')
LOCAL_DATABASE_URL = 'postgresql://postgres:posrgres@0.0.0.0:5432/postgres'

engine = create_engine(
    DOKER_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

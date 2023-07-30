from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DOKER_DATABASE_URL = os.getenv("DATABASE_URL")
LOCAL_DATABASE_URL = "postgresql://postgres:posrgres@0.0.0.0:5432/postgres"

engine = create_engine(
    DOKER_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


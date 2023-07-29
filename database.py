from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DOKER_DATABASE_URL = 'postgresql://postgres:postgres@postgres/postgres'
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:posrgres@0.0.0.0:5432/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


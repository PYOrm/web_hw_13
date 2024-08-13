from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.Settings import settings

DB_URL = settings.sqlalchemy_database_url

engine = create_engine(DB_URL)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

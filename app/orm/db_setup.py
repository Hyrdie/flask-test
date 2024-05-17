import os
from typing import Generator

from databases import Database
from settings import settings
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)
metadata = MetaData()
database = Database(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)
def get_engine():
    return engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_session():
    return SessionLocal()

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Mynameismike99@localhost/db"
SQLALCHEMY_DATABASE_URL = 'postgresql://ml:ml_password@db:5432/frames_db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
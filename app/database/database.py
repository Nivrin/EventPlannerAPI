import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

current_dir = os.path.dirname(os.path.abspath(__file__))

database_dir = os.path.join(current_dir, '..', '..', 'data_and_logs', 'database')

os.makedirs(database_dir, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(database_dir, 'database.db')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database():
    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

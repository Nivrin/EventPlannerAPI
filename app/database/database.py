from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "sqlite:///database/database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

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

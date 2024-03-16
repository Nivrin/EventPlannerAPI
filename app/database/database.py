from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Specify the URL of your pre-existing SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///C:/Users/USER/Desktop/niv/EventPlannerAPI/app/database/database.db"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker using the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

# Database configuration
DATABASE_URL = "sqlite:///./templates.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database and create tables"""
    Base.metadata.create_all(bind=engine)
    
    # Create templates directory if it doesn't exist
    os.makedirs("app/templates", exist_ok=True)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
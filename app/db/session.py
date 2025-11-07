from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Logger Configuration
from app.utils.logging_config import configure_logger
logger = configure_logger(__file__)

load_dotenv()

# Create Engine by passing Database URL
engine = create_engine(os.getenv("QA_DB_URL"))

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
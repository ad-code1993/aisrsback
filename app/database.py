from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv
import logging

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Default to SQLite if not set
engine = create_engine(DATABASE_URL, echo=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Log the loaded DATABASE_URL
logger.info(f"Loaded DATABASE_URL: {DATABASE_URL}")

# Raise an error if DATABASE_URL is not set
if not DATABASE_URL:
    logger.error("DATABASE_URL is not set. Please check your environment variables or .env file.")
    raise RuntimeError("DATABASE_URL is required but not set.")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
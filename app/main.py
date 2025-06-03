from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, create_db_and_tables
from .routers import srs
from dotenv import load_dotenv
import os
import logging

# Explicitly specify the path to the .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Log database URL for debugging
logger.info(f"Using DATABASE_URL: {DATABASE_URL}")

# Ensure DATABASE_URL is not None
if not DATABASE_URL:
    logger.error("DATABASE_URL is not set. Please check your environment variables or .env file.")
    raise ValueError("DATABASE_URL is required but not set.")



app = FastAPI(title="SRS Generation API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(srs.router)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    try:
        create_db_and_tables()
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

@app.get("/")
def health_check():
    logger.info("Health check endpoint accessed.")
    return {"status": "active", "message": "SRS Generation API is running"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, create_db_and_tables
from .routers import srs

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
    create_db_and_tables()

@app.get("/")
def health_check():
    return {"status": "active", "message": "SRS Generation API is running"}

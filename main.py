from fastapi import FastAPI
from app.utils.logs import create_logger
from app.routes.api import router as api_router
from app.routes.example import router as example_router
from dotenv import load_dotenv
import uvicorn
import os
import logging


# Load environment variables from .env file
load_dotenv()

# Reduce watchfiles logging spam
logging.getLogger("watchfiles.main").setLevel(logging.WARNING)

# Setup logger
logger = create_logger("fastapi_server")

# Create FastAPI app
app = FastAPI(
    title="FastAPI Template",
    description="A simple FastAPI server template with Docker support and logging",
    version="1.0.0",
    debug=os.getenv("DEBUG", 'false') == 'true' ,
)

# Include API router
app.include_router(api_router)
app.include_router(example_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Hello World", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    logger.info("Starting FastAPI server on http://0.0.0.0:5001")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5001,
        reload=os.getenv("RELOAD", 'false') == 'true'
    )

"""Main FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

# Load environment variables
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(env_path, override=True)

from app.api import forecasting, inventory, analytics, assistant
from app.utils import init_db, seed_sample_data

# Initialize database
init_db()
seed_sample_data()

# Create FastAPI app
app = FastAPI(
    title="AI Retail Intelligence Platform",
    description="Demand Forecasting & Inventory Optimization",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(forecasting.router)
app.include_router(inventory.router)
app.include_router(analytics.router)
app.include_router(assistant.router)


# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "AI Retail Intelligence Platform",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": str(__import__('datetime').datetime.utcnow())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# FastAPI app for MongoDB operations

"""
Production FastAPI Application
Run: python main.py
"""

from database import get_database, close_connection
from get_endpoints import router as get_router
from post_endpoints import router as post_router
import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="Heart Attack Prediction API",
    description="MongoDB-based API for heart attack prediction data",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(get_router, prefix="/api", tags=["GET Operations - MongoDB"])
app.include_router(post_router, prefix="/api", tags=["POST Operations - MongoDB"])  # NEW

# Startup
@app.on_event("startup")
async def startup():
    print("HEART ATTACK PREDICTION API - STARTING")
    get_database()  # Initialize connection
    print(f"API Documentation: http://localhost:{config.API_PORT}/docs")

# Shutdown
@app.on_event("shutdown")
async def shutdown():
    print("Shutting down...")
    close_connection()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Heart Attack Prediction API",
        "status": "running",
        "documentation": "/docs",
        "team_member": "2 - MongoDB GET & POST Endpoints"
    }

# Health check
@app.get("/health")
async def health():
    try:
        db = get_database()
        db.list_collection_names()
        return {"status": "healthy", "database": "connected"}
    except:
        return {"status": "unhealthy", "database": "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
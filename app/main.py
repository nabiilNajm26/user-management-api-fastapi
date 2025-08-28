from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .core.database import create_tables
from .core.config import get_settings
from .api.users import router as users_router

settings = get_settings()

app = FastAPI(
    title="User Management API",
    description="Simple REST API for user management with full CRUD operations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router)

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup (with error handling)"""
    try:
        create_tables()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️ Database connection failed: {e}")
        print("App will start but database operations will fail until DB is available")

@app.get("/")
def read_root():
    return {
        "message": "User Management API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "users": "/users",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    from .core.database import engine
    
    # Check database connectivity
    db_status = "disconnected"
    try:
        with engine.connect() as connection:
            db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "service": "user-management-api",
        "version": "1.0.0",
        "database": db_status
    }

if __name__ == "__main__":
    import uvicorn
    # Railway provides PORT env var, fallback to 8000 for local
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
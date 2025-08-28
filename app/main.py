from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.database import create_tables
from .core.config import get_settings
from .api.users import router as users_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Simple REST API for user management with full CRUD operations",
    version=settings.app_version
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
    """Create database tables on startup"""
    create_tables()

@app.get("/")
def read_root():
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs",
        "endpoints": {
            "users": "/users",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "user-management-api",
        "version": settings.app_version
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
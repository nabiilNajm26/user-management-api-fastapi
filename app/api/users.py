from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
import math

from ..core.database import get_db
from ..services.user_service import UserService
from ..schemas.user import (
    UserCreate, 
    UserUpdate, 
    UserResponse, 
    UserListResponse
)
from ..core.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user
    
    - **email**: User's email address (must be unique)
    - **name**: User's full name
    """
    return UserService.create_user(db, user_data)


@router.get("/", response_model=UserListResponse)
def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(settings.default_page_size, ge=1, le=settings.max_page_size, description="Number of users per page"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in name or email"),
    db: Session = Depends(get_db)
):
    """
    Get users with pagination and optional filtering
    
    - **page**: Page number (starts from 1)
    - **page_size**: Number of users per page
    - **is_active**: Filter by active status (optional)
    - **search**: Search term for name or email (optional)
    """
    skip = (page - 1) * page_size
    users, total = UserService.get_users(
        db=db, 
        skip=skip, 
        limit=page_size,
        is_active=is_active,
        search=search
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return UserListResponse(
        users=users,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID
    
    - **user_id**: UUID of the user
    """
    return UserService.get_user_by_id(db, user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user information
    
    - **user_id**: UUID of the user to update
    - **email**: New email address (optional)
    - **name**: New name (optional)
    - **is_active**: New active status (optional)
    """
    return UserService.update_user(db, user_id, user_data)


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: UUID,
    hard_delete: bool = Query(False, description="If true, permanently delete user"),
    db: Session = Depends(get_db)
):
    """
    Delete user (soft delete by default)
    
    - **user_id**: UUID of the user to delete
    - **hard_delete**: If true, permanently delete user; if false, just deactivate
    """
    return UserService.delete_user(db, user_id, soft_delete=not hard_delete)


@router.get("/stats/summary")
def get_user_stats(
    db: Session = Depends(get_db)
):
    """
    Get user statistics
    
    Returns summary of user counts (total, active, inactive)
    """
    return UserService.get_user_stats(db)
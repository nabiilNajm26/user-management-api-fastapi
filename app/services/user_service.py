from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from typing import Optional
from fastapi import HTTPException, status

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.config import get_settings

settings = get_settings()


class UserService:
    """Service class for user-related operations"""

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user
        
        Args:
            db: Database session
            user_data: User creation data
            
        Returns:
            Created user instance
            
        Raises:
            HTTPException: If user with email already exists
        """
        # Check if user with email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Create new user
        db_user = User(
            email=user_data.email,
            name=user_data.name
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User UUID
            
        Returns:
            User instance
            
        Raises:
            HTTPException: If user not found
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            db: Database session
            email: User email address
            
        Returns:
            User instance or None if not found
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_users(
        db: Session, 
        skip: int = 0, 
        limit: int = 20,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ) -> tuple[list[User], int]:
        """
        Get users with pagination and optional filtering
        
        Args:
            db: Database session
            skip: Number of users to skip (for pagination)
            limit: Maximum number of users to return
            is_active: Filter by active status (optional)
            search: Search term for name or email (optional)
            
        Returns:
            Tuple of (users list, total count)
        """
        query = db.query(User)
        
        # Apply filters
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (User.name.ilike(search_term)) | 
                (User.email.ilike(search_term))
            )
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
        
        return users, total

    @staticmethod
    def update_user(db: Session, user_id: UUID, user_data: UserUpdate) -> User:
        """
        Update user information
        
        Args:
            db: Database session
            user_id: User UUID
            user_data: User update data
            
        Returns:
            Updated user instance
            
        Raises:
            HTTPException: If user not found or email already taken
        """
        # Get existing user
        user = UserService.get_user_by_id(db, user_id)
        
        # Check if email is being updated and already exists
        if user_data.email and user_data.email != user.email:
            existing_user = UserService.get_user_by_email(db, user_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
        
        # Update user fields
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return user

    @staticmethod
    def delete_user(db: Session, user_id: UUID, soft_delete: bool = True) -> User:
        """
        Delete user (soft delete by default)
        
        Args:
            db: Database session
            user_id: User UUID
            soft_delete: If True, set is_active=False; if False, actually delete
            
        Returns:
            Deleted user instance (for soft delete) or None (for hard delete)
            
        Raises:
            HTTPException: If user not found
        """
        user = UserService.get_user_by_id(db, user_id)
        
        if soft_delete:
            # Soft delete - just deactivate
            user.is_active = False
            db.commit()
            db.refresh(user)
            return user
        else:
            # Hard delete - actually remove from database
            db.delete(user)
            db.commit()
            return user

    @staticmethod
    def get_user_stats(db: Session) -> dict:
        """
        Get user statistics
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with user statistics
        """
        total_users = db.query(func.count(User.id)).scalar()
        active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
        inactive_users = total_users - active_users
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": inactive_users
        }
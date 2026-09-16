from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.db.database import get_db
from app.models import User, UserRole, Role
from app.core.config import settings
from app.core.jwt import decode_token

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(
        User.id == user_id,
        User.deleted_at == None
    ).first()
    
    if user is None:
        raise credentials_exception
    
    if user.status != 'active':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active"
        )
    
    return user


def get_user_roles(user: User, db: Session) -> List[str]:
    """Get list of role names for a user."""
    roles = db.query(Role.name).join(UserRole).filter(
        UserRole.user_id == user.id
    ).all()
    return [role[0] for role in roles]


def require_role(required_role: str):
    """Dependency to check if user has required role."""
    async def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        user_roles = get_user_roles(current_user, db)
        
        # Check if user has required role or is admin
        if required_role not in user_roles and 'admin' not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required role: {required_role}"
            )
        
        return current_user
    
    return role_checker


def require_any_role(required_roles: List[str]):
    """Dependency to check if user has any of the required roles."""
    async def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        user_roles = get_user_roles(current_user, db)
        
        # Check if user has any of the required roles or is admin
        has_role = any(role in user_roles for role in required_roles)
        if not has_role and 'admin' not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have any of the required roles: {required_roles}"
            )
        
        return current_user
    
    return role_checker


def get_current_student(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student record for current user."""
    from app.models import Student
    
    student = db.query(Student).filter(
        Student.user_id == current_user.id,
        Student.deleted_at == None
    ).first()
    
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student record not found"
        )
    
    return student


def get_current_staff(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get staff record for current user."""
    from app.models import Staff
    
    staff = db.query(Staff).filter(
        Staff.user_id == current_user.id,
        Staff.deleted_at == None
    ).first()
    
    if staff is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff record not found"
        )
    
    return staff

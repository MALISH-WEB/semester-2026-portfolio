from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models import User, Student, Payment, StudentFinancialAccount
from app.schemas import UserLogin, Token, UserResponse, FinancialStatus, RegistrationEligibilityResponse
from app.core.security import verify_password, get_password_hash
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.services.financial_engine import get_financial_status, check_registration_eligibility, get_semester_policy

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT tokens."""
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email, User.deleted_at == None).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if user.status != 'active':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not active"
        )
    
    # Get user roles
    role_names = [role.role.name for role in user.roles]
    
    # Create tokens
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "roles": role_names
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(lambda: None)  # Will implement proper dependency
):
    """Get current user profile."""
    # This will be implemented with proper authentication dependency
    pass


@router.post("/register")
def register_student(
    # Will implement student registration
    db: Session = Depends(get_db)
):
    """Register a new student user."""
    pass

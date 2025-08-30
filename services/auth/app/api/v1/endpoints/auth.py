from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from typing import Any

from ....core.config import settings
from ....core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash
)
from ....database import get_db
from ....database.models import User, AuthCredentials, RefreshToken
from ....schemas.user import UserCreate, User as UserSchema, Token, TokenRefresh

router = APIRouter()

@router.post("/register", response_model=UserSchema)
def register(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    """"Register a new user"""
    # Check if user exists
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    user = User(email=user_in.email)
    db.add(user)
    db.flush() # Get user.id without committing

    # Create auth credentials
    auth_credentials = AuthCredentials(
        user_id=user.id,
        hashed_password=get_password_hash(user_in.password),
        password_changed_at=datetime.now(timezone.utc)
    )
    db.add(auth_credentials)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Oauth2 compatible token login"""
    # Find user and credentials
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.auth_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(form_data.password, user.auth_credentials.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create tokens
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    # Store refresh token
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(db_refresh_token)
    db.commit()

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/refresh", response_model=Token)
def refresh_token(
        refresh_token_in: TokenRefresh,
        db: Session = Depends(get_db)
) -> Any:
    """Refresh access token"""
    #Find refresh token
    token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token_in.refresh_token
    ).first()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Check if token is expired
    if token.expires_at < datetime.now(timezone.utc):
        db.delete(token)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    # Create new tokens
    access_token = create_access_token(str(token.user_id))
    new_refresh_token = create_refresh_token(str(token.user_id))

    # Update refresh token
    token.token = new_refresh_token
    token.expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db.commit()

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token
    )
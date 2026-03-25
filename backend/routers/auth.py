"""
Authentication API Routes
Handles user login, logout, and token management
"""

from fastapi import APIRouter, HTTPException, status, Header, Depends
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta

from utils.session_store import session_store

router = APIRouter()

# Authentication configuration
VALID_USERNAME = "kuanlong.li"
VALID_PASSWORD = "kuanlong.li"  # Default password for demo
SECRET_KEY = "internet-a1-shopping-cart-secret-key-2024"
ALGORITHM = "HS256"


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    User login
    
    - **username**: Username (default: kuanlong.li)
    - **password**: Password (default: kuanlong.li)
    
    Returns JWT token on successful authentication
    """
    # Validate credentials
    if request.username != VALID_USERNAME or request.password != VALID_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Generate JWT token
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {
        "sub": request.username,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Store session in memory
    session_store.create_session(request.username, token)
    
    return TokenResponse(
        access_token=token,
        user={"username": request.username}
    )


@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """
    User logout
    
    Requires Authorization header with Bearer token
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No token provided"
        )
    
    # Extract token from "Bearer <token>" format
    token = authorization.replace("Bearer ", "")
    session_store.delete_session(token)
    
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Get current authenticated user
    
    Requires Authorization header with Bearer token
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Extract token
    token = authorization.replace("Bearer ", "")
    session = session_store.get_session(token)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return {"username": session["username"]}


# Dependency injection for protected routes
async def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Get current user if authenticated, returns None otherwise
    
    Used for optional authentication (e.g., showing stock info only when logged in)
    """
    if not authorization:
        return None
    
    try:
        token = authorization.replace("Bearer ", "")
        session = session_store.get_session(token)
        return session["username"] if session else None
    except Exception:
        return None


async def get_current_user_required(authorization: Optional[str] = Header(None)) -> str:
    """
    Get current user, requires authentication
    
    Used for protected routes that require login
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        token = authorization.replace("Bearer ", "")
        session = session_store.get_session(token)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return session["username"]
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

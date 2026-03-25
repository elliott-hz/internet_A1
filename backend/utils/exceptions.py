"""
Custom Exception Handlers
Provides centralized error handling for the API
"""

from fastapi import HTTPException, status


class DatabaseError(HTTPException):
    """Custom exception for database errors"""
    
    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class NotFoundError(HTTPException):
    """Custom exception for resource not found"""
    
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found"
        )


class ValidationError(HTTPException):
    """Custom exception for validation errors"""
    
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class StockError(HTTPException):
    """Custom exception for stock-related errors"""
    
    def __init__(self, detail: str = "Stock error"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class UnauthorizedError(HTTPException):
    """Custom exception for unauthorized access"""
    
    def __init__(self, detail: str = "Unauthorized access"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
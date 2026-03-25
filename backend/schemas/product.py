"""
Product Pydantic Schemas
For request/response validation and serialization
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    """Base product schema with common fields"""
    
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    image_url: Optional[str] = Field(None, max_length=500, description="Product image URL")
    stock_quantity: int = Field(default=0, ge=0, description="Stock quantity")
    is_available: bool = Field(default=True, description="Product availability status")


class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    
    pass


class ProductUpdate(BaseModel):
    """Schema for updating an existing product"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: Optional[float] = Field(None, gt=0, description="Product price (must be positive)")
    image_url: Optional[str] = Field(None, max_length=500, description="Product image URL")
    stock_quantity: Optional[int] = Field(None, ge=0, description="Stock quantity")
    is_available: Optional[bool] = Field(None, description="Product availability status")


class ProductResponse(ProductBase):
    """Schema for product response"""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

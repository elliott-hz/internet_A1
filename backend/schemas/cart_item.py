"""
Cart Item Schemas
"""

from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional


class CartItemCreate(BaseModel):
    """Schema for creating a cart item"""
    
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    """Schema for updating a cart item"""
    
    quantity: int


class CartItemResponse(BaseModel):
    """Schema for cart item response"""
    
    id: int
    product_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime
    
    # Product information - populated from the 'product' relationship
    product_name: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    stock_quantity: Optional[int] = None
    
    @field_validator('product_name', 'price', 'image_url', 'stock_quantity', mode='before')
    @classmethod
    def populate_from_product(cls, v, info):
        """Populate fields from the nested product relationship"""
        # Access the data dictionary to get the product object
        if hasattr(info.data, 'product') and info.data.product:
            product = info.data.product
            if info.field_name == 'product_name':
                return product.name
            elif info.field_name == 'price':
                return float(product.price) if product.price else None
            elif info.field_name == 'image_url':
                return product.image_url
            elif info.field_name == 'stock_quantity':
                return product.stock_quantity
        return v
    
    model_config = ConfigDict(from_attributes=True)
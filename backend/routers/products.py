"""
Product Router
Handles product-related endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from models.database import get_db
from services.product_service import ProductService
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from routers.auth import get_current_user_optional, get_current_user_required


router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
async def get_all_products(
    skip: int = 0,
    limit: int = 100,
    available_only: bool = False,
    db: Session = Depends(get_db),
    current_user: Optional[str] = Depends(get_current_user_optional)
):
    """Get all products with optional pagination and filtering.
    
    When authenticated, includes stock quantity information.
    """
    products = ProductService.get_all(db, skip, limit, available_only)
    
    # If authenticated, include stock info (already included in ProductResponse)
    # If not authenticated, we could hide stock_quantity if needed
    # For now, we return the same data but you could modify based on auth status
    
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[str] = Depends(get_current_user_optional)
):
    """Get a specific product by ID.
    
    When authenticated, includes detailed stock information.
    """
    return ProductService.get_by_id(db, product_id)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_required)
):
    """Create a new product. Requires authentication."""
    return ProductService.create(db, product_data)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_required)
):
    """Update an existing product. Requires authentication."""
    return ProductService.update(db, product_id, product_data)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_required)
):
    """Delete a product. Requires authentication."""
    ProductService.delete(db, product_id)
    return None

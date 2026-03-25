"""
Product Service
Business logic for product operations
"""

from sqlalchemy.orm import Session
from typing import List, Optional

from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from utils.exceptions import NotFoundError, ValidationError


class ProductService:
    """Service class for product-related business logic"""
    
    @staticmethod
    def get_all(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        available_only: bool = False
    ) -> List[Product]:
        """
        Get all products with optional pagination and filtering
        
        Args:
            db: Database session
            skip: Number of items to skip
            limit: Maximum number of items to return
            available_only: Filter only available products
            
        Returns:
            List of Product objects
        """
        query = db.query(Product)
        
        if available_only:
            query = query.filter(Product.is_available == True)
        
        return query.order_by(Product.name).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Product:
        """
        Get product by ID
        
        Args:
            db: Database session
            product_id: Product ID
            
        Returns:
            Product object
            
        Raises:
            NotFoundError: If product is not found
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise NotFoundError("Product")
        return product
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Product:
        """
        Get product by name
        
        Args:
            db: Database session
            name: Product name
            
        Returns:
            Product object
            
        Raises:
            NotFoundError: If product is not found
        """
        product = db.query(Product).filter(Product.name == name).first()
        if not product:
            raise NotFoundError("Product")
        return product
    
    @staticmethod
    def create(db: Session, product_data: ProductCreate) -> Product:
        """
        Create a new product
        
        Args:
            db: Database session
            product_data: Product creation data
            
        Returns:
            Created Product object
        """
        # Validate price
        if product_data.price <= 0:
            raise ValidationError("Price must be greater than zero", "price")
        
        # Validate stock quantity
        if product_data.stock_quantity < 0:
            raise ValidationError("Stock quantity cannot be negative", "stock_quantity")
        
        product = Product(**product_data.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def update(
        db: Session, 
        product_id: int, 
        product_data: ProductUpdate
    ) -> Product:
        """
        Update an existing product
        
        Args:
            db: Database session
            product_id: Product ID to update
            product_data: Product update data
            
        Returns:
            Updated Product object
            
        Raises:
            NotFoundError: If product is not found
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise NotFoundError("Product")
        
        # Update only provided fields
        update_data = product_data.model_dump(exclude_unset=True)
        
        # Validate fields if provided
        if 'price' in update_data and update_data['price'] <= 0:
            raise ValidationError("Price must be greater than zero", "price")
        
        if 'quantity' in update_data and update_data['quantity'] < 0:
            raise ValidationError("Quantity cannot be negative", "quantity")
        
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def delete(db: Session, product_id: int) -> bool:
        """
        Delete a product
        
        Args:
            db: Database session
            product_id: Product ID to delete
            
        Returns:
            True if deleted
            
        Raises:
            NotFoundError: If product is not found
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise NotFoundError("Product")
        
        db.delete(product)
        db.commit()
        return True

"""
Tests for Product API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestProductsAPI:
    """Test suite for Product API endpoints"""
    
    def test_get_all_products_empty(self, client: TestClient, db_session: Session):
        """Test getting all products when database is empty"""
        response = client.get("/api/products/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_all_products_with_data(
        self, 
        client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test getting all products with test data"""
        response = client.get("/api/products/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Check product structure
        first_product = data[0]
        assert "id" in first_product
        assert "name" in first_product
        assert "price" in first_product
        assert "is_available" in first_product
    
    def test_get_all_products_pagination(
        self, 
        client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test pagination for products list"""
        response = client.get("/api/products/?skip=0&limit=2")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_get_all_products_available_only(
        self, 
        client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test filtering only available products"""
        response = client.get("/api/products/?available_only=true")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # Only 2 products are available
        
        # All returned products should be available
        for product in data:
            assert product["is_available"] is True
    
    def test_get_product_by_id(
        self, 
        client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test getting a specific product by ID"""
        product_id = setup_test_data["product1_id"]
        response = client.get(f"/api/products/{product_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == "Test Product 1"
        assert data["price"] == 29.99
    
    def test_get_product_not_found(
        self, 
        client: TestClient, 
        db_session: Session
    ):
        """Test getting a non-existent product"""
        response = client.get("/api/products/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_create_product(
        self, 
        authenticated_client: TestClient, 
        db_session: Session
    ):
        """Test creating a new product"""
        product_data = {
            "name": "New Test Product",
            "description": "Test Description",
            "price": 39.99,
            "stock_quantity": 50,
            "is_available": True,
            "image_url": "https://example.com/image.jpg"
        }
        
        response = authenticated_client.post("/api/products/", json=product_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == product_data["name"]
        assert data["price"] == product_data["price"]
        assert "id" in data
    
    def test_create_product_invalid_price(
        self, 
        authenticated_client: TestClient, 
        db_session: Session
    ):
        """Test creating a product with invalid price"""
        product_data = {
            "name": "Invalid Product",
            "description": "Test",
            "price": -10,  # Invalid negative price
            "stock_quantity": 10,
            "is_available": True
        }
        
        response = authenticated_client.post("/api/products/", json=product_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_create_product_invalid_quantity(
        self, 
        authenticated_client: TestClient, 
        db_session: Session
    ):
        """Test creating a product with invalid stock quantity"""
        product_data = {
            "name": "Invalid Product",
            "description": "Test",
            "price": 10.0,
            "stock_quantity": -5,  # Invalid negative quantity
            "is_available": True
        }
        
        response = authenticated_client.post("/api/products/", json=product_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_update_product(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test updating an existing product"""
        product_id = setup_test_data["product1_id"]
        update_data = {
            "name": "Updated Product Name",
            "price": 59.99
        }
        
        response = authenticated_client.put(f"/api/products/{product_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Product Name"
        assert data["price"] == 59.99
    
    def test_update_product_not_found(
        self, 
        authenticated_client: TestClient, 
        db_session: Session
    ):
        """Test updating a non-existent product"""
        update_data = {
            "name": "Updated Name"
        }
        
        response = authenticated_client.put("/api/products/99999", json=update_data)
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_delete_product(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test deleting a product"""
        product_id = setup_test_data["product1_id"]
        
        response = authenticated_client.delete(f"/api/products/{product_id}")
        
        assert response.status_code == 204
        
        # Verify product is deleted
        get_response = authenticated_client.get(f"/api/products/{product_id}")
        assert get_response.status_code == 404
    
    def test_delete_product_not_found(
        self, 
        authenticated_client: TestClient, 
        db_session: Session
    ):
        """Test deleting a non-existent product"""
        response = authenticated_client.delete("/api/products/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_create_product_requires_auth(self, client: TestClient, db_session: Session):
        """Test that creating a product requires authentication"""
        product_data = {
            "name": "Test Product",
            "description": "Test",
            "price": 10.0,
            "stock_quantity": 10,
            "is_available": True
        }
        
        response = client.post("/api/products/", json=product_data)
        assert response.status_code == 401
    
    def test_update_product_requires_auth(
        self, 
        client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test that updating a product requires authentication"""
        product_id = setup_test_data["product1_id"]
        update_data = {
            "name": "Updated Name"
        }
        
        response = client.put(f"/api/products/{product_id}", json=update_data)
        assert response.status_code == 401
    
    def test_delete_product_requires_auth(
        self, 
        client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test that deleting a product requires authentication"""
        product_id = setup_test_data["product1_id"]
        
        response = client.delete(f"/api/products/{product_id}")
        assert response.status_code == 401

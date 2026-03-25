"""
Tests for Shopping Cart API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestCartAPI:
    """Test suite for Shopping Cart API endpoints"""
    
    def test_get_cart_items_empty(self, authenticated_client: TestClient, db_session: Session):
        """Test getting cart items when cart is empty"""
        response = authenticated_client.get("/api/cart")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_cart_items_with_data(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test getting cart items with test data"""
        # Add item to cart first
        cart_item_data = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 2
        }
        authenticated_client.post("/api/cart/items", json=cart_item_data)
        
        # Get cart items
        response = authenticated_client.get("/api/cart")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        
        cart_item = data[0]
        assert cart_item["product_id"] == setup_test_data["product1_id"]
        assert cart_item["quantity"] == 2
        assert "product_name" in cart_item
        assert "price" in cart_item
    
    def test_add_to_cart(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test adding a new item to cart"""
        cart_item_data = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 3
        }
        
        response = authenticated_client.post("/api/cart/items", json=cart_item_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["product_id"] == setup_test_data["product1_id"]
        assert data["quantity"] == 3
        assert "id" in data
    
    def test_add_to_cart_product_not_found(
        self, 
        authenticated_client: TestClient, 
        db_session: Session
    ):
        """Test adding non-existent product to cart"""
        cart_item_data = {
            "product_id": 99999,
            "quantity": 1
        }
        
        response = authenticated_client.post("/api/cart/items", json=cart_item_data)
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_add_to_cart_unavailable_product(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test adding unavailable product to cart"""
        cart_item_data = {
            "product_id": setup_test_data["product3_id"],
            "quantity": 1
        }
        
        response = authenticated_client.post("/api/cart/items", json=cart_item_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not available" in data["detail"].lower()
    
    def test_add_to_cart_insufficient_stock(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test adding more items than available in stock"""
        cart_item_data = {
            "product_id": setup_test_data["product2_id"],
            "quantity": 60  # More than stock (50) but less than 99
        }
        
        response = authenticated_client.post("/api/cart/items", json=cart_item_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "stock" in data["detail"].lower()
    
    def test_add_to_cart_invalid_quantity_zero(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test adding item with zero quantity"""
        cart_item_data = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 0
        }
        
        response = authenticated_client.post("/api/cart/items", json=cart_item_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_add_to_cart_invalid_quantity_negative(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test adding item with negative quantity"""
        cart_item_data = {
            "product_id": setup_test_data["product1_id"],
            "quantity": -5
        }
        
        response = authenticated_client.post("/api/cart/items", json=cart_item_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_add_to_cart_quantity_exceeds_limit(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test adding item with quantity exceeding 99 limit"""
        cart_item_data = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 100
        }
        
        response = authenticated_client.post("/api/cart/items", json=cart_item_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "99" in data["detail"]
    
    def test_update_existing_cart_item(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test updating quantity when adding same product again"""
        # Add item to cart first
        cart_item_data = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 2
        }
        authenticated_client.post("/api/cart/items", json=cart_item_data)
        
        # Add same product again
        cart_item_data_again = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 3
        }
        
        response = authenticated_client.post("/api/cart/items", json=cart_item_data_again)
        
        assert response.status_code == 201
        data = response.json()
        assert data["quantity"] == 5  # 2 + 3
    
    def test_update_existing_cart_item_exceeds_99(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test that updating doesn't exceed 99 quantity limit"""
        # Add item to cart with high quantity
        cart_item_data = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 95
        }
        authenticated_client.post("/api/cart/items", json=cart_item_data)
        
        # Try to add more
        cart_item_data_again = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 10
        }
        
        response = authenticated_client.post("/api/cart/items", json=cart_item_data_again)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "99" in data["detail"]
    
    def test_update_cart_item(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test updating a cart item's quantity"""
        # Add item to cart first
        cart_item_data = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 2
        }
        create_response = authenticated_client.post("/api/cart/items", json=cart_item_data)
        item_id = create_response.json()["id"]
        
        # Update the item
        update_data = {
            "quantity": 5
        }
        
        response = authenticated_client.put(f"/api/cart/items/{item_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["quantity"] == 5
    
    def test_update_cart_item_not_found(
        self, 
        authenticated_client: TestClient, 
        db_session: Session
    ):
        """Test updating non-existent cart item"""
        update_data = {
            "quantity": 5
        }
        
        response = authenticated_client.put("/api/cart/items/99999", json=update_data)
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_update_cart_item_invalid_quantity(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test updating with invalid quantity"""
        # Add item to cart first
        cart_item_data = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 2
        }
        create_response = authenticated_client.post("/api/cart/items", json=cart_item_data)
        item_id = create_response.json()["id"]
        
        # Update with invalid quantity
        update_data = {
            "quantity": 0
        }
        
        response = authenticated_client.put(f"/api/cart/items/{item_id}", json=update_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_remove_from_cart(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test removing an item from cart"""
        # Add item to cart first
        cart_item_data = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 2
        }
        create_response = authenticated_client.post("/api/cart/items", json=cart_item_data)
        item_id = create_response.json()["id"]
        
        # Remove the item
        response = authenticated_client.delete(f"/api/cart/items/{item_id}")
        
        assert response.status_code == 204
        
        # Verify it's removed
        get_response = authenticated_client.get("/api/cart")
        assert len(get_response.json()) == 0
    
    def test_remove_from_cart_not_found(
        self, 
        authenticated_client: TestClient, 
        db_session: Session
    ):
        """Test removing non-existent cart item"""
        response = authenticated_client.delete("/api/cart/items/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_clear_cart(
        self, 
        authenticated_client: TestClient, 
        db_session: Session,
        setup_test_data: dict
    ):
        """Test clearing all items from cart"""
        # Add multiple items to cart
        cart_item_data1 = {
            "product_id": setup_test_data["product1_id"],
            "quantity": 2
        }
        cart_item_data2 = {
            "product_id": setup_test_data["product2_id"],
            "quantity": 1
        }
        
        authenticated_client.post("/api/cart/items", json=cart_item_data1)
        authenticated_client.post("/api/cart/items", json=cart_item_data2)
        
        # Clear cart
        response = authenticated_client.delete("/api/cart")
        
        assert response.status_code == 204
        
        # Verify cart is empty
        get_response = authenticated_client.get("/api/cart")
        assert len(get_response.json()) == 0
    
    def test_clear_cart_already_empty(
        self, 
        authenticated_client: TestClient, 
        db_session: Session
    ):
        """Test clearing an already empty cart"""
        response = authenticated_client.delete("/api/cart")
        
        assert response.status_code == 204
    
    def test_cart_requires_authentication(self, client: TestClient, db_session: Session):
        """Test that cart endpoints require authentication"""
        # All cart endpoints should return 401 without authentication
        
        # Test GET /api/cart
        response = client.get("/api/cart")
        assert response.status_code == 401
        
        # Test POST /api/cart/items
        response = client.post("/api/cart/items", json={"product_id": 1, "quantity": 1})
        assert response.status_code == 401
        
        # Test PUT /api/cart/items/1
        response = client.put("/api/cart/items/1", json={"quantity": 1})
        assert response.status_code == 401
        
        # Test DELETE /api/cart/items/1
        response = client.delete("/api/cart/items/1")
        assert response.status_code == 401
        
        # Test DELETE /api/cart
        response = client.delete("/api/cart")
        assert response.status_code == 401

"""
Test script for authentication functionality
Tests login, logout, and token validation
"""

import sys
from fastapi.testclient import TestClient
sys.path.append('..')

from main import app

client = TestClient(app)


def test_login_success():
    """Test successful login with valid credentials"""
    response = client.post(
        "/api/auth/login",
        json={"username": "kuanlong.li", "password": "kuanlong.li"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["username"] == "kuanlong.li"
    print("✓ Login test passed")


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/api/auth/login",
        json={"username": "wrong_user", "password": "wrong_password"}
    )
    
    assert response.status_code == 401
    print("✓ Invalid credentials test passed")


def test_get_current_user():
    """Test getting current user with valid token"""
    # First login to get token
    login_response = client.post(
        "/api/auth/login",
        json={"username": "kuanlong.li", "password": "kuanlong.li"}
    )
    token = login_response.json()["access_token"]
    
    # Then get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "kuanlong.li"
    print("✓ Get current user test passed")


def test_logout():
    """Test logout functionality"""
    # First login to get token
    login_response = client.post(
        "/api/auth/login",
        json={"username": "kuanlong.li", "password": "kuanlong.li"}
    )
    token = login_response.json()["access_token"]
    
    # Then logout
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/auth/logout", headers=headers)
    
    assert response.status_code == 200
    
    # Try to use the token after logout (should fail)
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 401
    print("✓ Logout test passed")


if __name__ == "__main__":
    print("Running authentication tests...\n")
    
    test_login_success()
    test_login_invalid_credentials()
    test_get_current_user()
    test_logout()
    
    print("\n✅ All authentication tests passed!")

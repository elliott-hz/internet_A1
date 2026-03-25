"""
Test Configuration
Sets up test database and fixtures for testing
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from models.database import Base, get_db
import os

# Test database configuration
# Store test.db in the database directory alongside production database
DATABASE_DIR = os.path.join(os.path.dirname(__file__), "../..", "database")
os.makedirs(DATABASE_DIR, exist_ok=True)  # Ensure directory exists
TEST_DATABASE_URL = f"sqlite:///{os.path.join(DATABASE_DIR, 'test.db')}"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database for each test function
    
    This fixture ensures complete test isolation by:
    1. Dropping all tables before each test (removes all data and schema)
    2. Recreating all tables with fresh schema
    3. Providing a clean database session
    4. Cleaning up after test completes
    
    Each test function gets a completely clean database state.
    """
    # Drop all tables first to ensure clean state (removes all data)
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables with fresh schema
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Optional: Clean up tables after test (if you want to keep test.db file clean)
        # Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client with test database session
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    with TestClient(app=app, base_url="http://test") as test_client:
        yield test_client
    
    # Clean up overrides
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def setup_test_data(db_session):
    """
    Setup test data for tests
    """
    from models.product import Product
    from models.cart_item import CartItem
    
    # Create test products
    product1 = Product(
        name="Test Product 1",
        description="Test Description 1",
        price=29.99,
        stock_quantity=100,
        is_available=True,
        image_url="https://example.com/image1.jpg"
    )
    
    product2 = Product(
        name="Test Product 2",
        description="Test Description 2",
        price=49.99,
        stock_quantity=50,
        is_available=True,
        image_url="https://example.com/image2.jpg"
    )
    
    product3 = Product(
        name="Unavailable Product",
        description="This product is not available",
        price=19.99,
        stock_quantity=0,
        is_available=False,
        image_url="https://example.com/image3.jpg"
    )
    
    db_session.add(product1)
    db_session.add(product2)
    db_session.add(product3)
    db_session.commit()
    
    return {
        "product1_id": product1.id,
        "product2_id": product2.id,
        "product3_id": product3.id
    }


@pytest.fixture(scope="function")
def auth_token(client: TestClient):
    """
    Get authentication token for testing
    
    This fixture logs in with default credentials and returns the token.
    Available for all test files that import conftest.
    """
    login_response = client.post(
        "/api/auth/login",
        json={"username": "kuanlong.li", "password": "kuanlong.li"}
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


@pytest.fixture(scope="function")
def authenticated_client(client: TestClient, auth_token: str):
    """
    Create an authenticated test client
    
    This fixture adds the authorization header to all requests.
    Available for all test files that import conftest.
    """
    client.headers["Authorization"] = f"Bearer {auth_token}"
    yield client
    # Clean up: remove header after tests
    if "Authorization" in client.headers:
        del client.headers["Authorization"]

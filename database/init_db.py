"""
Database Initialization Script for SQLite
Supports two initialization methods:
1. ORM method (default) - Uses SQLAlchemy ORM to create tables and seed data
2. SQL method - Uses SQL files (init.sql and seed_data.sql) to initialize database

Usage:
    python init_db.py              # Default: ORM method
    python init_db.py --method=orm # Explicitly use ORM method
    python init_db.py --method=sql # Use SQL files method
"""

import sys
import os
import argparse

# Add backend directory to path to import models
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_dir)

from sqlalchemy import text
from models.database import engine, Base, SessionLocal
from models.product import Product
from models.cart_item import CartItem


def create_tables():
    """Create tables using SQLAlchemy ORM"""
    print("Creating database tables using ORM...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")


def seed_data():
    """Insert sample product data using ORM"""
    print("Seeding sample data using ORM...")
    
    # Sample products data
    sample_products = [
        {
            "name": "Wireless Bluetooth Headphones",
            "description": "Premium noise-cancelling over-ear headphones with 30-hour battery life and superior sound quality",
            "price": 79.99,
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
            "stock_quantity": 50,
            "is_available": True
        },
        {
            "name": "Smart Watch Pro",
            "description": "Feature-rich smartwatch with heart rate monitor, GPS, fitness tracking, and 7-day battery life",
            "price": 199.99,
            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500",
            "stock_quantity": 30,
            "is_available": True
        },
        {
            "name": "Portable Power Bank",
            "description": "20000mAh high-capacity portable charger with fast charging and dual USB ports",
            "price": 39.99,
            "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500",
            "stock_quantity": 100,
            "is_available": True
        },
        {
            "name": "Mechanical Keyboard",
            "description": "RGB backlit mechanical gaming keyboard with blue switches and aluminum frame",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500",
            "stock_quantity": 45,
            "is_available": True
        },
        {
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse with adjustable DPI, silent clicks, and long battery life",
            "price": 29.99,
            "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500",
            "stock_quantity": 75,
            "is_available": True
        },
        {
            "name": "USB-C Hub Adapter",
            "description": "7-in-1 USB-C hub with HDMI, USB 3.0, SD card reader, and power delivery",
            "price": 49.99,
            "image_url": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=500",
            "stock_quantity": 60,
            "is_available": True
        },
        {
            "name": "Laptop Stand",
            "description": "Adjustable aluminum laptop stand with ergonomic design and heat dissipation",
            "price": 44.99,
            "image_url": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=500",
            "stock_quantity": 40,
            "is_available": True
        },
        {
            "name": "Webcam HD 1080p",
            "description": "Full HD webcam with autofocus, built-in microphone, and wide-angle lens",
            "price": 59.99,
            "image_url": "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=500",
            "stock_quantity": 35,
            "is_available": True
        },
        {
            "name": "External SSD 1TB",
            "description": "Portable solid-state drive with ultra-fast transfer speeds and durable design",
            "price": 129.99,
            "image_url": "https://picsum.photos/seed/ssd-drive/500/500.jpg",
            "stock_quantity": 25,
            "is_available": True
        },
        {
            "name": "Phone Stand Holder",
            "description": "Adjustable cell phone stand compatible with all smartphones, perfect for desk",
            "price": 14.99,
            "image_url": "https://images.unsplash.com/photo-1585338107529-13afc5f02586?w=500",
            "stock_quantity": 120,
            "is_available": True
        },
        {
            "name": "LED Desk Lamp",
            "description": "Dimmable LED desk lamp with touch control, USB charging port, and eye-care technology",
            "price": 34.99,
            "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500",
            "stock_quantity": 55,
            "is_available": True
        },
        {
            "name": "Bluetooth Speaker",
            "description": "Portable waterproof Bluetooth speaker with 360° sound and 12-hour playtime",
            "price": 54.99,
            "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500",
            "stock_quantity": 65,
            "is_available": True
        }
    ]
    
    from sqlalchemy.orm import Session
    
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_count = db.query(Product).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} products. Skipping seed.")
            return
        
        # Insert sample products
        for product_data in sample_products:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        
        # Verify insertion
        total_products = db.query(Product).count()
        print(f"✅ Successfully inserted {total_products} products!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()


def create_tables_with_sql():
    """Create tables using SQL file"""
    print("Creating database tables using SQL file...")
    
    sql_file = os.path.join(os.path.dirname(__file__), 'init.sql')
    
    if not os.path.exists(sql_file):
        raise FileNotFoundError(f"SQL file not found: {sql_file}")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    db = SessionLocal()
    try:
        # Split SQL script into individual statements and execute each one
        # SQLite requires executing statements one by one when using SQLAlchemy
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:  # Skip empty statements
                db.execute(text(statement))
        
        db.commit()
        print("✅ Tables created successfully from init.sql!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error executing SQL: {e}")
        raise
    finally:
        db.close()


def seed_data_with_sql():
    """Insert sample data using SQL file"""
    print("Seeding sample data using SQL file...")
    
    sql_file = os.path.join(os.path.dirname(__file__), 'seed_data.sql')
    
    if not os.path.exists(sql_file):
        raise FileNotFoundError(f"SQL file not found: {sql_file}")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    db = SessionLocal()
    try:
        # Split SQL script into individual statements and execute each one
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:  # Skip empty statements
                db.execute(text(statement))
        
        db.commit()
        
        # Verify insertion
        total_products = db.query(Product).count()
        print(f"✅ Successfully inserted {total_products} products from seed_data.sql!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error executing SQL: {e}")
        raise
    finally:
        db.close()


def init_with_orm():
    """Initialize database using ORM method"""
    print("=" * 60)
    print("Internet A1 Shopping Cart - Database Initialization (ORM)")
    print("=" * 60)
    print()
    
    try:
        # Create tables
        create_tables()
        
        # Seed data
        seed_data()
        
        print()
        print("=" * 60)
        print("✅ Database initialization completed successfully!")
        print("=" * 60)
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Database initialization failed: {e}")
        print("=" * 60)
        sys.exit(1)


def init_with_sql():
    """Initialize database using SQL files method"""
    print("=" * 60)
    print("Internet A1 Shopping Cart - Database Initialization (SQL)")
    print("=" * 60)
    print()
    
    try:
        # Create tables from SQL file
        create_tables_with_sql()
        
        # Seed data from SQL file
        seed_data_with_sql()
        
        print()
        print("=" * 60)
        print("✅ Database initialization completed successfully!")
        print("=" * 60)
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Database initialization failed: {e}")
        print("=" * 60)
        sys.exit(1)


def main():
    """Main function to initialize database"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Initialize the database')
    parser.add_argument('--method', type=str, choices=['orm', 'sql'], default='orm',
                       help='Initialization method: orm (default) or sql')
    
    args = parser.parse_args()
    
    # Initialize based on method
    if args.method == 'sql':
        init_with_sql()
    else:
        init_with_orm()


if __name__ == "__main__":
    main()

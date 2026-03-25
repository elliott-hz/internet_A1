-- SQLite Database Initialization Script
-- Internet A1 E-commerce Shopping Cart
-- Compatible with SQLite (removed MySQL-specific syntax)

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS cart_items;
DROP TABLE IF EXISTS products;

-- Create Products table
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(500),
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    is_available BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index for products table
CREATE INDEX IF NOT EXISTS idx_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_availability ON products(is_available);

-- Create Cart Items table
CREATE TABLE IF NOT EXISTS cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Create index for cart_items table
CREATE INDEX IF NOT EXISTS idx_product_id ON cart_items(product_id);

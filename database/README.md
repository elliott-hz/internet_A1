# Database Initialization Guide

## Quick Start

### Method 1: ORM (Default - Recommended)
```bash
python3 init_db.py
# or explicitly
python3 init_db.py --method=orm
```

**Pros:** Type-safe, Pythonic, better validation  
**Cons:** Slightly slower

### Method 2: SQL Files
```bash
python3 init_db.py --method=sql
```

**Pros:** Direct SQL execution, easier to inspect schema  
**Cons:** No type validation, MySQL syntax in SQL files

## Files

- `init_db.py` - Main initialization script (supports both methods)
- `init.sql` - Database schema (SQLite compatible)
- `seed_data.sql` - Sample product data

## Initialization Database

```bash
# Initialize with ORM (default)
python3 init_db.py
or
python3 init_db.py --method=orm

# Initialize with SQL files
python3 init_db.py --method=sql
```

## SQLite Command Line Usage Guide

### Opening the Database in Command Line

To interact with the SQLite database directly using SQL commands:

```bash
sqlite3 database/internet_a1.db
```

Or from the database directory:

```bash
cd database
sqlite3 internet_a1.db
```

Once inside, you'll see the `sqlite>` prompt where you can execute SQL commands.

### Useful SQLite Commands

#### Display Settings
```sql
.headers on          -- Show column headers
.mode column         -- Display results in column format
.width 5 20 10       -- Set column widths
.tables              -- List all tables
.schema products     -- View products table structure
.schema cart_items   -- View cart_items table structure
.quit                -- Exit sqlite3
.exit                -- Exit sqlite3
```

### CRUD Operations

#### CREATE (Insert Data)
```sql
-- Insert a new product
INSERT INTO products (name, description, price, image_url, stock, category_id, created_at, updated_at)
VALUES ('New Product', 'Product description here', 99.99, 'https://example.com/image.jpg', 100, 1, datetime('now'), datetime('now'));
```

#### READ (Query Data)
```sql
-- Query all products
SELECT * FROM products;

-- Query specific columns
SELECT id, name FROM products;

-- Filter by price (products under $50)
SELECT * FROM products WHERE price < 50;

-- Sort by price (high to low)
SELECT * FROM products ORDER BY price DESC;

-- Search by name (contains "Wireless")
SELECT * FROM products WHERE name LIKE '%Wireless%';

-- Count total products
SELECT COUNT(*) as total FROM products;

-- Calculate average price
SELECT AVG(price) as average_price FROM products;

-- Group by category
SELECT is_available, COUNT(*) as count, AVG(price) as avg_price FROM products GROUP BY is_available;
```

#### UPDATE (Modify Data)
```sql
-- Update product price
UPDATE products SET price = 69.99 WHERE id = 1;

-- Bulk update (10% off all products)
UPDATE products SET price = price * 0.9;
```

#### DELETE (Remove Data)
```sql
-- Delete a specific product
DELETE FROM products WHERE id = 1;

-- Delete out-of-stock products
DELETE FROM products WHERE stock_quantity = 0;

-- Delete all products (careful!)
DELETE FROM products;
```

### Quick One-Liner Commands

You can also execute single SQL commands without entering interactive mode:

```bash
# Query products with low stock
sqlite3 internet_a1.db "SELECT id, name, stock_quantity FROM products WHERE stock_quantity < 50;"

# Update product price
sqlite3 internet_a1.db "UPDATE products SET price = 75.99 WHERE id = 1;"

# Delete a product
sqlite3 internet_a1.db "DELETE FROM products WHERE id = 1;"

# Count total products
sqlite3 internet_a1.db "SELECT COUNT(*) FROM products;"

# Export query results to CSV
sqlite3 -header -csv internet_a1.db "SELECT id, name, price FROM products;" > products.csv
```

### Backup and Restore

#### Create Database Backup
```bash
# Create a backup copy
cp internet_a1.db internet_a1_backup.db

# Or use SQLite's backup command
sqlite3 internet_a1.db ".backup 'internet_a1_backup.db'"
```

#### Export to SQL File
```bash
sqlite3 internet_a1.db ".dump" > backup.sql
```

#### Import from SQL File
```bash
sqlite3 internet_a1.db < backup.sql
```
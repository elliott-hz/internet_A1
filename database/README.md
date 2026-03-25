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

## Usage Examples

```bash
# Initialize with ORM (default)
python3 init_db.py

# Initialize with SQL files
python3 init_db.py --method=sql

# Show help
python3 init_db.py --help
```

## Files

- `init_db.py` - Main initialization script (supports both methods)
- `init.sql` - Database schema (SQLite compatible)
- `seed_data.sql` - Sample product data

## Notes

- Both methods create the same database structure and data
- Default method is **ORM** (no arguments needed)
- If database already has data, seeding will be skipped automatically
- SQL files are now SQLite-compatible (converted from MySQL syntax)

## Troubleshooting

**Error: "ModuleNotFoundError: No module named 'sqlalchemy'"**
```bash
cd ../backend
source venv/bin/activate
pip install -r requirements.txt
```

**Error: "no such table: products"**
Delete the database file and reinitialize:
```bash
rm internet_a1.db
python3 init_db.py --method=sql
```

# Internet A1 - E-commerce Shopping Cart

## Project Summary
This is a single-page e-commerce shopping cart application that allows users to browse products, add items to cart, modify quantities, and remove items. The application demonstrates full CRUD operations with a MySQL database, built with React frontend and FastAPI backend.

## 1. Tech Stack

### 1.1 Frontend
- **Framework**: React 18.x
- **Language**: JavaScript (ES6+)
- **Styling**: Styled Components
- **State Management**: React Hooks (useState, useEffect, Context API)
- **HTTP Client**: Axios
- **Build Tool**: Vite (with hot reload)

### 1.2 Backend
- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Database ORM**: SQLAlchemy
- **Database**: SQLite (default, python built-in light database, no further libriaries installation required)
- **CORS**: FastAPI CORS middleware

**Note**: The application uses SQLite by default for easy setup. MySQL support is available but optional - see [Database README](database/README.md) for details.

### 1.3 Development Tools
- **Code Quality**: ESLint + Prettier (frontend)
- **Code Quality**: Black + Flake8 (backend)
- **Hot Reload**: Vite HMR (frontend) + Uvicorn auto-reload (backend)

## 2. Features

- ✅ **Product Catalog**: Display all available products with dynamic data loading
- ✅ **Shopping Cart Management**: Add/remove items, adjust quantities
- ✅ **CRUD Operations**: 
  - **Create**: Add new products to cart
  - **Read**: View products and cart items
  - **Update**: Modify item quantities
  - **Delete**: Remove items from cart
- ✅ **Single Page Application**: Dynamic component rendering without page reloads
- ✅ **Responsive Design**: Mobile-friendly interface
- ✅ **Real-time Updates**: Instant UI feedback on all operations
- ✅ **Error Handling**: User-friendly error messages and fallback UI

**Note:** Configuration files are organized within their respective directories:
- Frontend configs (`.eslintrc.json`, `.prettierrc`, `vite.config.js`) are in `frontend/`
- Backend configs (`requirements.txt`, `pyproject.toml`) are in `backend/`

## 3. Folder Structure

```
internet_A1/
├── README.md                    # Project documentation (this file)
├── Assignment.md                # Assignment requirements
├── cleanup.sh                   # Cleanup script
├── restart.sh                   # Restart script
├── install.sh                   # Install script
└── .gitignore                   # Git ignore rules
│
├── frontend/                    # React Frontend Application
│   ├── index.html              # Single HTML entry point
│   ├── package.json            # Node.js dependencies & scripts
│   ├── vite.config.js          # Vite build configuration
│   ├── .eslintrc.json          # ESLint configuration
│   ├── .prettierrc             # Prettier settings
│   │
│   ├── src/                    # Source code
│   │   ├── main.jsx            # React entry point
│   │   ├── App.jsx             # Main application component
│   │   │
│   │   ├── components/         # Reusable UI components
│   │   │   ├── ProductList/    # Product listing component
│   │   │   │   ├── ProductList.jsx
│   │   │   │   └── ProductList.styles.js
│   │   │   ├── ProductCard/    # Individual product card
│   │   │   │   ├── ProductCard.jsx
│   │   │   │   └── ProductCard.styles.js
│   │   │   ├── ShoppingCart/   # Shopping cart container
│   │   │   │   ├── ShoppingCart.jsx
│   │   │   │   └── ShoppingCart.styles.js
│   │   │   ├── CartItem/       # Individual cart item with +/- controls
│   │   │   │   ├── CartItem.jsx
│   │   │   │   └── CartItem.styles.js
│   │   │   ├── Header/         # Navigation header
│   │   │   │   ├── Header.jsx
│   │   │   │   └── Header.styles.js
│   │   │   ├── Login/          # Login form component
│   │   │   │   ├── Login.jsx
│   │   │   │   └── Login.styles.js
│   │   │   └── Modal/          # Confirmation modal and Toast
│   │   │       ├── Modal.jsx       # Confirmation dialog
│   │   │       ├── Modal.styles.js
│   │   │       ├── Toast.jsx       # Toast notification component
│   │   │       └── Toast.styles.js
│   │   │
│   │   ├── hooks/              # Custom React hooks
│   │   │   ├── useCart.js      # Cart operations hook (uses CartContext)
│   │   │   ├── useProducts.js  # Products fetching hook (deprecated - use ProductsContext)
│   │   │   └── useApi.js       # Generic API calls hook
│   │   │
│   │   ├── services/           # API integration layer
│   │   │   ├── api.js          # Axios instance configuration
│   │   │   ├── productService.js # Product-related API calls
│   │   │   └── cartService.js  # Cart-related API calls
│   │   │
│   │   ├── context/            # React Context providers
│   │   │   ├── CartContext.jsx # Global cart state management with optimistic updates
│   │   │   ├── ProductsContext.jsx # Global products state sharing (avoid repeated API calls)
│   │   │   └── AuthContext.jsx # Authentication state management
│   │   │
│   │   ├── utils/              # Helper functions
│   │   │   ├── formatters.js   # Price/date formatting
│   │   │   └── validators.js   # Input validation
│   │   │
│   │   ├── assets/             # Static resources
│   │   │   ├── images/         # Product images, icons
│   │   │   └── styles/         # Global styles
│   │   │       ├── global.js   # Global styled components
│   │   │       └── variables.js # CSS variables (colors, spacing)
│   │   │
│   │   └── constants/          # Application constants
│   │       └── index.js        # API endpoints, config values
│   │
│   └── public/                 # Public assets
│       └── favicon.ico
│
├── backend/                     # FastAPI Backend Application
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── pyproject.toml          # Black & Flake8 configuration
│   └── .gitignore              # Python git ignore rules
│   │
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   ├── database.py         # Database connection
│   │   ├── product.py          # Product model
│   │   └── cart_item.py        # Cart item model
│   │
│   ├── schemas/                # Pydantic schemas (data validation)
│   │   ├── __init__.py
│   │   ├── product.py          # Product schemas
│   │   └── cart_item.py        # Cart item schemas
│   │
│   ├── routers/                # API route handlers
│   │   ├── __init__.py
│   │   ├── products.py         # Product endpoints
│   │   └── cart.py             # Cart endpoints
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── product_service.py  # Product operations
│   │   └── cart_service.py     # Cart operations
│   │
│   └── utils/                  # Backend utilities
│       ├── __init__.py
│       └── exceptions.py       # Custom exception handlers
│
└── database/                    # Database Setup Scripts
    ├── init.sql                # SQLite schema initialization (SQL method)
    ├── seed_data.sql           # Sample product data (SQL method)
    ├── init_db.py              # Database initialization script
    └── README.md               # Database setup instructions
```

## 3. Troubleshooting Guide

This guide provides solutions for common issues you may encounter while setting up or running the Internet A1 project.

### 3.1 Installation Issues

#### 1. Prerequisites Check Failed

**Error**: Git/Node.js/Python is not installed

**Solution**:
```bash
# Install Git
# macOS: Install Xcode Command Line Tools
xcode-select --install

# Or download from: https://git-scm.com/downloads

# Install Node.js 18.x or higher
# Download from: https://nodejs.org/en/download/

# Install Python 3.9 or higher
# Download from: https://www.python.org/downloads/
```

**Verify installations**:
```bash
git --version
node -v
npm -v
python3 --version
```

#### 2. Backend Dependencies Installation Failed

**Error**: `pip install` fails or import errors occur

**Solution**:
```bash
cd backend

# Remove virtual environment and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 3. Frontend Dependencies Installation Failed

**Error**: `npm install` fails

**Solution**:
```bash
cd frontend

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```


### 3.2 Backend Issues

#### 1. Backend Won't Start

**Error**: Cannot start Uvicorn server

**Solution 1 - Check port 8000**:
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process using port 8000
kill -9 <PID>

# Or use the restart script
./restart.sh
```

**Solution 2 - Verify virtual environment**:
```bash
cd backend
source venv/bin/activate

# Test if you can run the app
python main.py
```

**Solution 3 - Check for syntax errors**:
```bash
cd backend
python -m py_compile main.py
```

#### 2. Backend Import Errors

**Error**: `ModuleNotFoundError` or `ImportError`

**Solution**:
```bash
cd backend
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify installation
python -c "import fastapi; import sqlalchemy; print('All imports OK')"
```

#### 3. Database Connection Failed

**Error**: Cannot connect to database

**Solution**:
```bash
# Check if database file exists
ls -lh database/internet_a1.db

# If not, reinitialize database
cd database
python init_db.py

# Verify products were created
cd ../backend
source venv/bin/activate
python -c "from models.database import SessionLocal; from models.product import Product; db = SessionLocal(); print(f'Products: {db.query(Product).count()}'); db.close()"
```

### 3.3 Frontend Issues

#### 1. Frontend Won't Start

**Error**: Vite dev server fails to start

**Solution 1 - Check port 5173**:
```bash
# Check if port 5173 is in use
lsof -i :5173

# Kill the process
kill -9 <PID>

# Restart frontend
cd frontend
npm run dev
```

**Solution 2 - Reinstall dependencies**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Solution 3 - Clear Vite cache**:
```bash
cd frontend
rm -rf node_modules/.vite
npm run dev
```

#### 2. Frontend Build Errors

**Error**: Compilation or build errors

**Solution**:
```bash
cd frontend

# Clear everything and reinstall
rm -rf node_modules package-lock.json dist
npm cache clean --force
npm install

# Try running again
npm run dev
```

### 3.4 Database Issues

#### 1. Database File Missing

**Error**: `database/internet_a1.db` not found

**Solution**:
```bash
# Navigate to database directory
cd database

# Re-run initialization
python init_db.py

# Verify file was created
ls -lh internet_a1.db
```

#### 2. Database Schema Issues

**Error**: Table doesn't exist or schema mismatch

**Solution**:
```bash
# Delete and recreate database
cd database
rm internet_a1.db
python init_db.py

# Verify tables were created
cd ../backend
source venv/bin/activate
python -c "from models.database import SessionLocal; db = SessionLocal(); result = db.execute('SELECT name FROM sqlite_master WHERE type=\"table\"'); print([row[0] for row in result]); db.close()"
```

#### 3. Data Not Persisting

**Error**: Cart items or products disappear

**Solution**:
1. Check if you're using the correct database file location
2. Verify database write permissions:
```bash
cd database
chmod 644 internet_a1.db
```

3. Re-seed data if needed:
```bash
cd database
python init_db.py
```

### 3.5 API Issues

#### 1. API Endpoints Not Working

**Error**: API returns 404 or 500 errors

**Solution 1 - Test health endpoint**:
```bash
curl http://localhost:8000/api/health
```

**Solution 2 - Check backend logs**:
```bash
# Stop backend (Ctrl+C)
# Restart with verbose logging
cd backend
source venv/bin/activate
uvicorn main:app --reload --log-level debug
```

**Solution 3 - Verify API routes**:
```bash
# List all available routes
curl http://localhost:8000/docs
```

#### 2. CORS Errors

**Error**: CORS policy blocking requests

**Solution**:
Check that backend CORS settings in `backend/main.py` include the frontend URL (http://localhost:5173).


### 3.6 Port Conflicts

#### 1. Port 8000 Already in Use

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in backend/main.py
# Look for: uvicorn.run(..., port=8000)
# Change to: uvicorn.run(..., port=8001)
```

#### 2. Port 5173 Already in Use

**Solution**:
```bash
# Find process using port 5173
lsof -i :5173

# Kill the process
kill -9 <PID>

# Or change port in frontend/vite.config.js
# Add: server: { port: 5174 }
```

### 5.6 General Debugging Tips

#### 1. Check All Services Status

```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Check if frontend is running
curl http://localhost:5173

# List all related processes
ps aux | grep -E 'uvicorn|node|vite'

# Check ports
lsof -i :8000
lsof -i :5173
```

#### 2. Clean Restart

```bash
# Stop all services
kill $(lsof -ti :8000) $(lsof -ti :5173) 2>/dev/null || true

# Clean and restart everything
./install.sh
```

#### 3. View Logs

**Backend logs**:
```bash
cd backend
tail -f logs/app.log  # If logging to file
```

**Frontend logs**:
Check browser console (F12) for frontend errors.

---
### 3.8 Quick Reference Commands

```bash
# Check versions
git --version
node -v
npm -v
python3 --version

# Check ports
lsof -i :8000
lsof -i :5173

# Test API
curl http://localhost:8000/api/health
curl http://localhost:8000/api/products

# Restart services
./restart.sh

# Reinstall everything
./install.sh
```
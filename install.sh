#!/bin/bash

# =============================================================================
# Install Script for Internet A1 Project
# =============================================================================
# This script will:
# 1. Check prerequisites (Git, Node.js 18+, Python 3.9+)
# 2. Clean up existing environment
# 3. Install backend dependencies
# 4. Initialize database
# 5. Install frontend dependencies
# =============================================================================

set -e  # Exit on error

echo "========================================="
echo "  Internet A1 Project Installation"
echo "========================================="
echo ""

# Define project root
PROJECT_ROOT=$(git rev-parse --show-toplevel)
echo "Project Root: $PROJECT_ROOT"
echo ""

# =============================================================================
# Step 1: Prerequisites Check
# =============================================================================
echo "========================================="
echo "  Step 1: Checking Prerequisites"
echo "========================================="

# Check Git installation
echo "Checking Git..."
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed!"
    echo "Please install Git first: https://git-scm.com/downloads"
    exit 1
else
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo "Git is installed (version: $GIT_VERSION)"
fi

# Check Node.js installation (must be 18.x or higher)
echo "Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed!"
    echo "   Please install Node.js 18.x or higher: https://nodejs.org/en/download/"
    exit 1
else
    NODE_VERSION=$(node -v | sed 's/v//' | cut -d. -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        echo "Error: Node.js version is too low (current: v$NODE_VERSION)!"
        echo "   Please upgrade to Node.js 18.x or higher: https://nodejs.org/en/download/"
        exit 1
    else
        echo "Node.js is installed (version: $(node -v))"
    fi
fi

# Check npm installation
echo "Checking npm..."
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed!"
    echo "   Please reinstall Node.js."
    exit 1
else
    echo "npm is installed (version: $(npm -v))"
fi

# Check Python installation (must be 3.9 or higher)
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed!"
    echo "   Please install Python 3.9 or higher: https://www.python.org/downloads/"
    exit 1
else
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PYTHON_VERSION_NUM=$(python3 -c 'import sys; print(sys.version_info[0]*100 + sys.version_info[1])')
    if [ "$PYTHON_VERSION_NUM" -lt 309 ]; then
        echo "Error: Python version is too low (current: $PYTHON_VERSION)!"
        echo "   Please upgrade to Python 3.9 or higher."
        exit 1
    else
        echo "Python is installed (version: $PYTHON_VERSION)"
    fi
fi

echo ""
echo "All prerequisites are met!"
echo ""

# =============================================================================
# Step 2: Cleanup Existing Environment
# =============================================================================
echo "========================================="
echo "  Step 2: Cleaning Up Environment"
echo "========================================="

cd "$PROJECT_ROOT"

if [ -f "cleanup.sh" ]; then
    chmod +x cleanup.sh
    echo "Running cleanup script..."
    ./cleanup.sh
    echo "Cleanup completed"
else
    echo "cleanup.sh not found, skipping cleanup"
fi

echo ""

# =============================================================================
# Step 3: Backend Setup
# =============================================================================
echo "========================================="
echo "  Step 3: Setting Up Backend"
echo "========================================="

cd "$PROJECT_ROOT/backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Backend dependencies installed"
elif [ -f "pyproject.toml" ]; then
    pip install .
    echo "Backend dependencies installed from pyproject.toml"
else
    echo "No requirements file found, skipping dependency installation"
fi

echo ""

# =============================================================================
# Step 4: Database Setup
# =============================================================================
echo "========================================="
echo "  Step 4: Setting Up Database"
echo "========================================="

cd "$PROJECT_ROOT/database"

echo "Initializing database..."
# python3 init_db.py --method=orm   # Use ORM method for better compatibility with SQLAlchemy
python3 init_db.py --method=sql  # Use raw SQL method for direct execution (may require splitting statements for SQLite)

# Verify database was created
if [ -f "$PROJECT_ROOT/database/internet_a1.db" ]; then
    echo "Database created successfully at: $PROJECT_ROOT/database/internet_a1.db"
    
    # Verify products were inserted
    cd "$PROJECT_ROOT/backend"
    source venv/bin/activate
    PRODUCT_COUNT=$(python -c "from models.database import SessionLocal; from models.product import Product; db = SessionLocal(); count = db.query(Product).count(); db.close(); print(count)")
    echo "Database initialized with $PRODUCT_COUNT products"
else
    echo "Error: Database file was not created!"
    exit 1
fi

echo ""

# =============================================================================
# Step 5: Frontend Setup
# =============================================================================
echo "========================================="
echo "  Step 5: Setting Up Frontend"
echo "========================================="

cd "$PROJECT_ROOT/frontend"

echo "Installing frontend dependencies..."
npm install

if [ -d "node_modules" ]; then
    echo "Frontend dependencies installed"
else
    echo "Error: Frontend dependencies installation failed!"
    exit 1
fi

echo ""

# =============================================================================
# Installation Complete
# =============================================================================
echo "========================================="
echo " Installation Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Start the backend: ./restart.sh"
echo "2. Start the frontend: cd frontend && npm run dev"
echo ""
echo "Or use the restart script to start both services."
echo ""

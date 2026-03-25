#!/bin/bash

# =============================================================================
# Restart Script for Internet A1 Project
# =============================================================================
# This script will:
# 1. Stop any existing backend and frontend processes
# 2. Run all tests (must pass 100%)
# 3. Start the backend server (FastAPI/Uvicorn)
# 4. Start the frontend development server (Vite)
# =============================================================================

set -e  # Exit on error

# Parse command line arguments
SKIP_TESTS=false
for arg in "$@"; do
    case $arg in
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
    esac
done

echo "========================================="
echo "  Restarting Internet A1 Services"
echo "========================================="
echo ""

# Define project root
PROJECT_ROOT=$(git rev-parse --show-toplevel)
echo "Project Root: $PROJECT_ROOT"
if [ "$SKIP_TESTS" = true ]; then
    echo "⚠️  Tests will be SKIPPED (--skip-tests flag detected)"
fi
echo ""

# =============================================================================
# Step 1: Stop Existing Processes
# =============================================================================
echo "========================================="
echo "  Step 1: Stopping Existing Services"
echo "========================================="

# Kill backend process (port 8000)
echo "Checking for backend process on port 8000..."
if lsof -ti:8000; then
    echo "Killing backend process..."
    kill -9 $(lsof -ti:8000) || true
    echo "✅ Backend process stopped"
else
    echo "ℹ️  No backend process found on port 8000"
fi

# Kill frontend process (port 5173)
echo "Checking for frontend process on port 5173..."
if lsof -ti:5173; then
    echo "Killing frontend process..."
    kill -9 $(lsof -ti:5173) || true
    echo "✅ Frontend process stopped"
else
    echo "ℹ️  No frontend process found on port 5173"
fi

echo ""

# =============================================================================
# Step 2: Run Tests (MUST PASS 100%)
# =============================================================================
if [ "$SKIP_TESTS" = true ]; then
    echo "========================================="
    echo "  Step 2: Skipping Tests (--skip-tests)"
    echo "========================================="
    echo ""
    echo "⚠️  WARNING: Skipping test suite..."
    echo "   This is NOT recommended for production deployments."
    echo ""
    sleep 2
else
    echo "========================================="
    echo "  Step 2: Running All Tests"
    echo "========================================="
    echo ""
    echo "⚠️  All tests MUST pass before starting services..."
    echo ""

    cd "$PROJECT_ROOT/backend"

    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "❌ Error: Virtual environment not found!"
        echo "   Please run ./install.sh first."
        exit 1
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Check if pytest is installed
    if ! command -v pytest &> /dev/null; then
        echo "❌ Error: pytest is not installed!"
        echo "   Installing test dependencies..."
        pip install -r requirements.txt -q
    fi

    # Run all tests
    echo "Running pytest..."
    echo ""
    if pytest tests/ -v --tb=short; then
        echo ""
        echo "✅ All tests passed successfully!"
        echo ""
    else
        echo ""
        echo "❌ Tests failed! Aborting service startup."
        echo ""
        echo "========================================="
        echo "  🚫 Service Startup Aborted"
        echo "========================================="
        echo ""
        echo "Reason: Test suite did not pass 100%"
        echo ""
        echo "Please fix the failing tests and try again."
        echo "To skip tests (not recommended), use: ./restart.sh --skip-tests"
        echo "========================================="
        exit 1
    fi

    echo ""
fi

# =============================================================================
# Step 3: Start Backend Server
# =============================================================================
echo "========================================="
echo "  Step 3: Starting Backend Server"
echo "========================================="

# Check if database exists
if [ ! -f "$PROJECT_ROOT/database/internet_a1.db" ]; then
    echo "⚠️  Database not found, initializing..."
    cd "$PROJECT_ROOT/database"
    python3 init_db.py
    cd "$PROJECT_ROOT/backend"
fi

echo "Starting Uvicorn server on http://0.0.0.0:8000"
echo "Backend API will be available at: http://localhost:8000/api"
echo ""

# Start backend in background
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "✅ Backend started with PID: $BACKEND_PID"

# Wait a moment for backend to start
sleep 3

echo ""

# =============================================================================
# Step 4: Start Frontend Server
# =============================================================================
echo "========================================="
echo "  Step 4: Starting Frontend Server"
echo "========================================="

cd "$PROJECT_ROOT/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ Error: Frontend dependencies not installed!"
    echo "   Please run ./install.sh first."
    exit 1
fi

echo "Starting Vite development server..."
echo "Frontend will be available at: http://localhost:5173"
echo ""

# Start frontend in background
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started with PID: $FRONTEND_PID"

echo ""

# =============================================================================
# Services Started
# =============================================================================
echo "========================================="
echo "  ✅ All Services Started!"
echo "========================================="
echo ""
echo "Backend API:  http://localhost:8000/api"
echo "Frontend App: http://localhost:5173"
echo ""
echo "Service PIDs:"
echo "  Backend:  $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo ""
echo "To stop services:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Or run this script again to restart."
echo "========================================="

# Keep script running to show logs
wait
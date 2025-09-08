# ProjectMeats Development Makefile
# Provides essential development commands for Django + React application

.PHONY: help setup dev test clean docs format lint

# Default target
help:
	@echo "ProjectMeats Development Commands"
	@echo ""
	@echo "Quick Start:"
	@echo "  python setup.py - Complete setup (recommended)"
	@echo "  make dev        - Start development servers"
	@echo ""
	@echo "Development:"
	@echo "  make backend    - Start Django server only"
	@echo "  make frontend   - Start React server only"
	@echo "  make migrate    - Apply database migrations"
	@echo "  make migrations - Create new migrations"
	@echo "  make shell      - Open Django shell"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test       - Run all tests"
	@echo "  make format     - Format code"
	@echo "  make lint       - Lint code"
	@echo "  make docs       - Generate API docs"
	@echo "  make clean      - Clean artifacts"
	@echo ""
	@echo "See README.md for complete documentation."

# Setup commands
setup: setup-backend setup-frontend
	@echo "✅ Complete setup finished! Run 'make dev' to start development."

setup-backend:
	@echo "🔧 Setting up Django backend..."
	cd backend && cp -n .env.example .env 2>/dev/null || true
	cd backend && pip install -r requirements.txt
	cd backend && python manage.py migrate
	@echo "✅ Backend setup complete!"

setup-frontend:
	@echo "🔧 Setting up React frontend..."
	cd frontend && npm install
	@echo "✅ Frontend setup complete!"

# Development commands
dev:
	@echo "🚀 Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo ""
	@make -j2 backend frontend

backend:
	@echo "🐍 Starting Django development server..."
	cd backend && python manage.py runserver

frontend:
	@echo "⚛️  Starting React development server..."
	cd frontend && npm start

# Database commands
migrate:
	cd backend && python manage.py migrate

migrations:
	cd backend && python manage.py makemigrations

shell:
	cd backend && python manage.py shell

# Testing commands
test: test-backend test-frontend

test-backend:
	@echo "🧪 Running Django tests..."
	cd backend && python manage.py test

test-frontend:
	@echo "🧪 Running React tests..."
	cd frontend && npm test -- --watchAll=false

# Code quality
format:
	@echo "🎨 Formatting code..."
	cd backend && black . --exclude=migrations
	cd backend && isort . --skip=migrations

lint:
	@echo "🔍 Linting code..."
	cd backend && flake8 . --exclude=migrations

# Documentation and cleanup
docs:
	@echo "📚 Generating API documentation..."
	cd backend && python manage.py spectacular --file ../docs/api_schema.yml
	@echo "✅ API schema generated at docs/api_schema.yml"

clean:
	@echo "🧹 Cleaning build artifacts..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	cd frontend && rm -rf build node_modules/.cache 2>/dev/null || true
	@echo "✅ Cleanup complete!"
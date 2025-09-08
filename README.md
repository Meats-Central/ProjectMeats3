# ProjectMeats3

A comprehensive business management application for meat sales brokers, migrated from PowerApps/Dataverse to a modern Django REST Framework (backend) and React TypeScript (frontend) stack. This system manages suppliers, customers, purchase orders, accounts receivables, and related business entities.

**Enhanced with AI Assistant**: Features intelligent chat interface with Copilot-style UI, document processing, and business intelligence capabilities.

## ⚠️ Quick Fix: "Authentication credentials were not provided"

**Having authentication issues?** Run this one command:

```bash
python setup_ai_assistant.py
```

This interactive wizard will configure everything needed including authentication, database, and AI features. See [QUICK_SETUP.md](QUICK_SETUP.md) for more details.

## 🏗️ Technology Stack

- **Backend**: Django 4.2.7 + Django REST Framework + PostgreSQL
- **Frontend**: React 18.2.0 + TypeScript + Styled Components  
- **AI Assistant**: OpenAI GPT-4 integration with modern Copilot-style interface
- **Authentication**: Django User system with profile management
- **API**: RESTful endpoints with OpenAPI documentation
- **Testing**: 95+ comprehensive backend tests

## 📁 Project Structure

```
ProjectMeats3/
├── backend/                    # Django REST Framework API
│   ├── apps/                  # Business entities (9 complete)
│   │   ├── accounts_receivables/  # Customer payments
│   │   ├── suppliers/            # Supplier management
│   │   ├── customers/            # Customer relationships
│   │   ├── purchase_orders/      # Order processing
│   │   ├── plants/              # Processing facilities
│   │   ├── contacts/            # Contact management
│   │   └── core/                # Shared utilities
│   └── requirements.txt
├── frontend/                   # React TypeScript application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── screens/           # Main application screens
│   │   └── services/         # API communication
│   └── package.json
├── docs/                      # Documentation
└── powerapps_export/          # Original PowerApps solution
```

## 🚀 Quick Setup

**Prerequisites**: Python 3.9+, Node.js 16+, Git

### Option 1: Interactive AI Assistant Setup (Recommended)
```bash
# Clone repository
git clone https://github.com/Meats-Central/ProjectMeats3.git
cd ProjectMeats3

# Run comprehensive AI assistant setup wizard
python setup_ai_assistant.py
```

This guided setup will configure:
- ✅ Backend authentication and database
- ✅ AI provider credentials (OpenAI, Anthropic, Azure OpenAI)
- ✅ Environment variables and secrets
- ✅ Frontend integration
- ✅ Database initialization

### Option 2: Standard Setup
```bash
# Clone repository
git clone https://github.com/Meats-Central/ProjectMeats3.git
cd ProjectMeats3

# Full setup (backend + frontend)
python setup.py

# Configure AI assistant separately
python setup_ai_assistant.py
```

### Option 3: Platform-Specific Setup

**Windows Users:**
```cmd
setup_windows.bat
```

**Linux/macOS:**
```bash
make setup
# or
./setup.sh
```

### Manual Setup (Advanced Users)
```bash
# Backend only
python setup.py --backend

# Frontend only  
python setup.py --frontend

# AI assistant only
python setup.py --ai-only
```

## 🔧 Development

### Start Development Servers
```bash
# Start both servers (Linux/macOS)
make dev

# Windows users - use separate terminals:
# Terminal 1: cd backend && python manage.py runserver
# Terminal 2: cd frontend && npm start
```

### Access URLs
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000  
- **API Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

### AI Assistant Features
After running `python setup_ai_assistant.py`:
- **Chat Interface**: Intelligent conversational AI for business operations with modern Copilot-style UI
- **Document Processing**: Upload and analyze purchase orders, invoices, contracts via drag & drop
- **Entity Extraction**: Automatic data extraction and database integration
- **Business Intelligence**: Natural language queries about your data

### Default Credentials
- **Username**: admin
- **Password**: WATERMELON1219

### Development Commands
```bash
make test          # Run all tests
make migrate       # Run Django migrations
make docs          # Generate API documentation
make clean         # Clean build artifacts
```

## 🤖 AI Assistant Enhancements

This version includes the latest AI Assistant improvements from PR #63:

### Fixed Issues ✅
- **HTTP 404 Errors**: Fixed API endpoint URLs (/ai-assistant/ai-chat/chat/)
- **Intelligent Responses**: Enhanced with meat industry-specific AI responses
- **Modern UI**: Complete Copilot-style interface with integrated file upload
- **Drag & Drop**: Seamless document upload experience

### New Features ✅
- **Integrated File Upload**: Attachment button in message input
- **Drag & Drop Support**: Drop files anywhere in chat area
- **Visual Feedback**: Animations, loading states, error handling
- **File Validation**: Support for PDF, images, documents with size limits
- **Enhanced UX**: Professional error messages and user guidance

## 📋 Migration Status

**Completed Entities**:
- ✅ **Accounts Receivables** - Customer payment tracking
- ✅ **Suppliers** - Supplier management system  
- ✅ **Customers** - Customer relationship management
- ✅ **Purchase Orders** - Order processing workflow
- ✅ **Plants** - Processing facility management
- ✅ **Contacts** - Contact information system
- ✅ **User Profiles** - Authentication and user management
- ✅ **AI Assistant** - Intelligent chat with document processing

*See [docs/migration_mapping.md](docs/migration_mapping.md) for detailed PowerApps → Django field mappings.*

## 🧪 Testing

```bash
# Backend tests
cd backend && python manage.py test

# Frontend tests  
cd frontend && npm test

# Full test suite
make test
```

**Test Status**: ✅ 95+ backend tests covering all business entities

## 📚 Documentation

### Quick Start Guides
- **[QUICK_SETUP.md](QUICK_SETUP.md)** - Solve authentication issues in 5 minutes
- **[AI Assistant Setup](docs/ai_assistant_setup.md)** - Complete AI configuration guide
- **[Setup & Development Guide](docs/setup-and-development.md)** - Complete setup and development instructions

### Technical Documentation  
- **[API Reference](docs/api_reference.md)** - Complete API documentation  
- **[Production Deployment](docs/production_deployment.md)** - Production deployment guide
- **[Migration Mapping](docs/migration_mapping.md)** - PowerApps to Django mappings
- **[Architecture Guide](docs/architecture.md)** - System architecture and design decisions

## 🚀 Performance & Production

### Recent Optimizations ✅
- **Database indexes**: Strategic indexes for improved query performance
- **Query optimization**: Reduced N+1 queries with `select_related()`
- **Code quality**: Automated formatting and linting
- **Security review**: Comprehensive security assessment
- **AI Assistant**: Fixed API endpoints and enhanced UI performance

### Production Deployment

ProjectMeats3 includes an **interactive production deployment system** with guided setup optimized for Digital Ocean App Platform:

```bash
# Interactive production setup with server recommendations
python deploy_production.py

# Or quick server provider comparison
python server_guide.py
```

**Features**:
- 🎯 **Digital Ocean App Platform Ready**: Optimized configuration files
- 🌟 **Interactive console prompts** for all configuration values
- 🔧 **Automated configuration file generation**
- 🚀 **One-command deployment**
- 🔒 **Security best practices** (SSL, firewall, environment variables)
- 📊 **Deployment verification** and health checks

**Quick Setup**:
1. Choose Digital Ocean App Platform (recommended) or other providers
2. Run `python deploy_production.py` for guided configuration
3. Upload configuration to Digital Ocean
4. Access your production application with SSL/HTTPS

See [docs/production_setup_guide.md](docs/production_setup_guide.md) for the complete deployment guide.

## 👥 Contributing

1. Follow the [Setup & Development Guide](docs/setup-and-development.md)
2. Use existing patterns from implemented entities
3. Add tests for new functionality
4. Update documentation for changes

**Code Standards**:
- **Backend**: Django/DRF best practices, type hints, comprehensive tests
- **Frontend**: React functional components with TypeScript
- **AI Assistant**: Modern UI patterns following Microsoft Copilot design
- **Documentation**: Clear inline comments for PowerApps migrations

---

**Need Help?** Check the [docs/](docs/) folder or create an issue for questions.

## 🔄 Version History

- **v3.0** - Enhanced AI Assistant with Copilot-style UI, fixed API endpoints, production-ready deployment
- **v2.0** - Complete Django + React migration from PowerApps
- **v1.0** - Original PowerApps solution

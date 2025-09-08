# ProjectMeats Environment Configuration Guide

## Overview

ProjectMeats uses a centralized environment configuration system that provides:
- **Centralized management** of all environment variables
- **Environment-specific configurations** (development, staging, production)
- **Validation and error checking** for required variables
- **Security best practices** for each deployment environment
- **Easy deployment** with standardized configurations

## Quick Start

### 1. Set Up Development Environment
```bash
# Option 1: Using the configuration manager (recommended)
python config/manage_env.py setup development

# Option 2: Using Make
make env-dev

# Option 3: Manual setup
cp config/environments/development.env backend/.env
cp config/shared/frontend.env.template frontend/.env.local
```

### 2. Validate Configuration
```bash
python config/manage_env.py validate
# or
make env-validate
```

### 3. Start Development Servers
```bash
# Start both backend and frontend
make dev

# Or start individually
make backend    # Django server on :8000
make frontend   # React server on :3000
```

## Environment Configuration Files

### Directory Structure
```
config/
├── README.md                    # Environment configuration documentation
├── environments/               # Environment-specific configurations
│   ├── development.env        # Development environment
│   ├── staging.env           # Staging environment
│   └── production.env        # Production environment
├── shared/                    # Shared configuration templates
│   ├── backend.env.template  # Backend environment template
│   └── frontend.env.template # Frontend environment template
└── deployment/               # Deployment configurations
    └── manage_env.py         # Environment management script
```

### Environment Files

#### Development (config/environments/development.env)
- **Database**: SQLite for local development
- **Debug**: Enabled for development
- **CORS**: Allows localhost origins
- **Security**: Disabled for development ease
- **AI Services**: Optional API keys

#### Staging (config/environments/staging.env)  
- **Database**: PostgreSQL with environment variables
- **Debug**: Disabled  
- **CORS**: Restricted to staging domains
- **Security**: Enabled with HTTPS
- **AI Services**: Staging API keys
- **Monitoring**: Basic monitoring setup

#### Production (config/environments/production.env)
- **Database**: PostgreSQL with connection pooling
- **Debug**: Disabled
- **CORS**: Restricted to production domains only
- **Security**: Full security features enabled
- **AI Services**: Production API keys
- **Monitoring**: Full monitoring and alerting
- **Performance**: Optimized settings

## Environment Variables

### Backend Variables

#### Django Core
| Variable | Description | Development | Staging | Production |
|----------|-------------|-------------|---------|-----------|
| `SECRET_KEY` | Django secret key | Generated | ${STAGING_SECRET_KEY} | ${PRODUCTION_SECRET_KEY} |
| `DEBUG` | Debug mode | `True` | `False` | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` | Staging domains | Production domains |

#### Database
| Variable | Description | Development | Staging | Production |
|----------|-------------|-------------|---------|-----------|
| `DATABASE_URL` | Database connection | `sqlite:///db.sqlite3` | PostgreSQL URL | PostgreSQL URL with pooling |

#### Security & CORS
| Variable | Description | Development | Staging | Production |
|----------|-------------|-------------|---------|-----------|
| `CORS_ALLOWED_ORIGINS` | CORS origins | `localhost:3000` | Staging frontend | Production frontend only |
| `SECURE_SSL_REDIRECT` | Force HTTPS | `False` | `True` | `True` |
| `SECURE_HSTS_SECONDS` | HSTS max age | `0` | `31536000` | `31536000` |

#### AI Services
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Optional |
| `ANTHROPIC_API_KEY` | Anthropic API key | Optional |

### Frontend Variables

#### API Configuration
| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_BASE_URL` | Backend API URL | `http://localhost:8000/api/v1` |
| `REACT_APP_ENVIRONMENT` | Environment name | `development` |

#### Feature Flags
| Variable | Description | Default |
|----------|-------------|---------|
| `REACT_APP_AI_ASSISTANT_ENABLED` | Enable AI chat | `true` |
| `REACT_APP_ENABLE_DOCUMENT_UPLOAD` | Enable file uploads | `true` |
| `REACT_APP_ENABLE_CHAT_EXPORT` | Enable chat export | `true` |

## Deployment Guide

### Development Deployment
1. **Setup**: `python config/manage_env.py setup development`
2. **Install**: `pip install -r backend/requirements.txt && cd frontend && npm install`
3. **Migrate**: `cd backend && python manage.py migrate`
4. **Run**: `make dev`

### Staging Deployment
1. **Environment Variables**: Set staging environment variables in your deployment system
2. **Setup**: `python config/manage_env.py setup staging`
3. **Validate**: `python config/manage_env.py validate`
4. **Deploy**: Follow your staging deployment process

### Production Deployment
1. **Environment Variables**: Set production environment variables securely
2. **Setup**: `python config/manage_env.py setup production`
3. **Validate**: `python config/manage_env.py validate`
4. **Security Check**: Verify all security settings are enabled
5. **Deploy**: Follow your production deployment process

## Security Best Practices

### Secret Management
- **Generate unique secrets** for each environment
- **Store secrets securely** using your deployment platform's secret management
- **Never commit secrets** to version control
- **Rotate secrets regularly** especially for production

### Environment Separation  
- **Use different databases** for each environment
- **Separate API keys** for AI services per environment
- **Restrict CORS origins** to specific domains
- **Enable security features** in staging and production

### Access Control
- **Limit staging access** to development team only
- **Secure production access** with proper authentication
- **Monitor access logs** for suspicious activity
- **Regular security audits** of environment configurations

## Troubleshooting

### Common Issues

#### CORS Errors
**Symptom**: Frontend can't connect to backend
**Solution**: 
1. Check `CORS_ALLOWED_ORIGINS` in backend `.env`
2. Ensure frontend domain is included
3. Restart backend server after changes

#### Database Connection Errors
**Symptom**: Django can't connect to database
**Solution**:
1. Verify `DATABASE_URL` format
2. Check database credentials
3. Ensure database server is running
4. Test connection manually

#### Environment Variable Not Found
**Symptom**: `KeyError` for environment variable
**Solution**:
1. Run validation: `python config/manage_env.py validate`
2. Check variable exists in `.env` file
3. Ensure no typos in variable names
4. Restart application after changes

### Validation Commands
```bash
# Validate current environment
python config/manage_env.py validate

# Generate new secrets
python config/manage_env.py generate-secrets

# Check Django configuration
cd backend && python manage.py check

# Test frontend build
cd frontend && npm run build
```

## Migration from Legacy Configuration

### Automatic Migration
The new configuration system is backward compatible. Existing `.env` and `.env.local` files will continue to work.

### Manual Migration Steps
1. **Backup existing files**: `cp backend/.env backend/.env.backup`
2. **Set up new configuration**: `python config/manage_env.py setup development`
3. **Copy custom values**: Transfer any custom configurations from backup files
4. **Validate setup**: `python config/manage_env.py validate`
5. **Test application**: `make dev`

### Legacy File Support
- `backend/.env.example` - Now points to centralized system
- `frontend/.env.example` - Now points to centralized system
- Existing `.env` files will be backed up automatically

## Environment Management Commands

### Configuration Manager
```bash
# Set up environments
python config/manage_env.py setup development
python config/manage_env.py setup staging
python config/manage_env.py setup production

# Validation and utilities
python config/manage_env.py validate
python config/manage_env.py generate-secrets
```

### Make Commands
```bash
# Environment setup
make env-dev        # Set up development
make env-staging    # Set up staging  
make env-prod       # Set up production
make env-validate   # Validate configuration
make env-secrets    # Generate secrets

# Development
make dev           # Start development servers
make backend       # Start backend only
make frontend      # Start frontend only
```

### Project Setup
```bash
# Complete project setup (recommended)
python setup.py

# Component setup
python setup.py --backend
python setup.py --frontend
```

This centralized system ensures consistent, secure, and easily manageable environment configurations across all deployment environments.
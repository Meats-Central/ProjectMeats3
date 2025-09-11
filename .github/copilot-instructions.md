# GitHub Copilot Instructions for ProjectMeats3

## Project Overview
ProjectMeats3 is a web application for meat sales brokers, migrated from PowerApps to a modern stack. It manages business entities like suppliers, customers, purchase orders, accounts receivables, plants, contacts, and user profiles. Key features include:
- RESTful API for CRUD operations on entities.
- AI Assistant (powered by OpenAI GPT-4) with a Copilot-style UI for chat, document processing, entity extraction, and business intelligence (e.g., supplier performance metrics).
- User authentication and profile management using Django's built-in system.
- Document upload and analysis for invoices/orders.

The app is designed for scalability, with a focus on data accuracy, security, and ease of deployment on platforms like DigitalOcean.

## Technology Stack
- **Backend**: Django 4.2.7, Django REST Framework (DRF) for APIs, PostgreSQL as the primary database (SQLite for local dev).
- **Frontend**: React 18.2.0 with TypeScript, Styled Components for UI, Axios for API calls.
- **AI Integrations**: OpenAI API (e.g., GPT-4) for natural language processing and entity extraction.
- **Database & Tools**: PostgreSQL for production; tools like Poetry/Pipenv for dependencies, Jest/React Testing Library for frontend tests, Black/Flake8 for Python linting, ESLint/Prettier for TypeScript.
- **Deployment**: Docker and docker-compose for containerization; DigitalOcean Droplets and Managed Databases; GitHub Actions for CI/CD.
- **Other**: OpenAPI for API docs, CORS/CSRF protections, rate limiting in DRF.

## Coding Standards
- **Python/Django**:
  - Follow PEP8 style guide; use Black for auto-formatting.
  - Models: Define in apps/<entity>/models.py with ForeignKeys for relationships (e.g., PurchaseOrder linked to Supplier).
  - Views: Use DRF ViewSets or GenericAPIView; include authentication (e.g., IsAuthenticated) and permissions.
  - Serializers: Use ModelSerializer; add custom validation for business logic (e.g., invoice totals).
  - Settings: Use environment variables for secrets (e.g., OPENAI_API_KEY); separate dev/prod configs.
- **TypeScript/React**:
  - Use ESLint with Airbnb config and Prettier for formatting.
  - Components: Functional with hooks; organize in src/components/ (reusable) and src/screens/ (pages).
  - State Management: Use React Context or Zustand for complex states (e.g., AI chat sessions); avoid prop drilling.
  - API Calls: Centralize in src/services/; handle errors with try-catch and user-friendly messages.
- **General**:
  - Commit Messages: Use conventional commits (e.g., "feat: add AI entity extraction").
  - Branching: GitFlow (feature/*, bugfix/*, release/*).
  - File Naming: Kebab-case for files, CamelCase for classes/components.

## Best Practices
- **Testing**:
  - Backend: Aim for 95%+ coverage; use Django's TestCase; test APIs with APITestCase.
  - Frontend: Use Jest and React Testing Library; test components and integrations.
  - Run tests with `make test`; include in CI.
- **Security**:
  - Never hardcode secrets; use .env files (ignored in .gitignore).
  - Enable HTTPS in prod; use Django's security middleware.
  - Sanitize user inputs, especially in AI prompts to prevent injection.
- **Performance**:
  - Use caching (e.g., Redis) for frequent API calls.
  - Optimize queries with select_related/prefetch_related in Django.
- **AI-Specific**:
  - Prompts: Be descriptive and context-aware (e.g., "Extract supplier name and total from this invoice text: [text]").
  - Error Handling: Graceful fallbacks for OpenAI rate limits or errors.
- **Documentation**:
  - Update README.md and docs/ for new features.
  - Use docstrings in code; generate API docs with DRF's built-in.
- **Contributions**:
  - Add pre-commit hooks for linting.
  - Ensure new features include tests and docs.
  - For new entities, mirror existing apps (e.g., models, serializers, views, tests).

## Task-Specific Guidance
- When fixing bugs: Check logs first; reproduce in dev env.
- When adding features: Start with backend models/serializers, then API views, finally frontend integration.
- When optimizing: Profile with tools like Django Debug Toolbar.
- Ignore deprecated features; prefer modern alternatives (e.g., async views if needed).

These instructions help Copilot generate code that fits seamlessly into ProjectMeats3. Review and update as the project evolves.
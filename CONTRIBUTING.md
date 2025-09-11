# Contributing to ProjectMeats3

Welcome to ProjectMeats3! We appreciate your interest in contributing to our Django + React business management application.

## 🚀 Quick Start

1. **Fork the repository** and clone your fork
2. **Set up development environment**:
   ```bash
   # Recommended setup
   python config/manage_env.py setup development
   pip install -r backend/requirements.txt
   cd frontend && npm install && cd ..
   
   # Alternative setup
   python setup_env.py
   ```
3. **Start development servers**:
   ```bash
   make dev  # Starts both backend and frontend
   ```

## 🔄 Development Workflow (GitFlow)

We follow GitFlow branching model:

### Branch Structure
- **`main`** - Production-ready code
- **`develop`** - Integration branch for features
- **`feature/*`** - New features (e.g., `feature/user-authentication`)
- **`release/*`** - Release preparation (e.g., `release/v1.1.0`)
- **`hotfix/*`** - Critical production fixes

### Workflow Steps

1. **Create feature branch from develop**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit**:
   ```bash
   # Make your changes
   git add .
   git commit -m "Add: brief description of changes"
   ```

3. **Keep branch updated**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/your-feature-name
   git rebase develop
   ```

4. **Push and create PR**:
   ```bash
   git push origin feature/your-feature-name
   # Create PR from feature branch to develop
   ```

## 📝 Code Standards

### Python (Backend)
- **Django 4.2+** best practices
- **Black** formatting (line length: 88)
- **isort** for imports
- **flake8** for linting
- **Type hints** where beneficial
- **Docstrings** for complex functions/classes

### JavaScript/TypeScript (Frontend)
- **React 18+** with TypeScript
- **ESLint** with TypeScript rules
- **Prettier** formatting
- **Functional components** with hooks
- **Clear component naming**

### General
- **Clear, descriptive commit messages**
- **One feature per branch**
- **Tests for new functionality**
- **Update documentation** when needed

## 🧪 Testing

### Backend Testing
```bash
make test-backend          # Run Django tests
cd backend && python manage.py test
```

### Frontend Testing
```bash
make test-frontend         # Run React tests
cd frontend && npm test
```

### Full Test Suite
```bash
make test                  # Run all tests
```

## 🛠️ Code Quality

### Pre-commit Hooks
Set up automated code quality checks:
```bash
pip install pre-commit
pre-commit install
```

### Manual Quality Checks
```bash
make format               # Format code (black, prettier)
make lint                 # Lint code (flake8, eslint)
make clean                # Clean artifacts
```

## 🗂️ Project Structure

```
ProjectMeats3/
├── backend/              # Django REST API
│   ├── apps/            # Business entities (9 apps)
│   ├── projectmeats/    # Django settings
│   └── requirements.txt
├── frontend/            # React TypeScript app
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── screens/     # Main app screens
│   │   └── services/    # API communication
│   └── package.json
├── config/              # Environment management
├── docs/                # Documentation
└── Makefile            # Development commands
```

## 🎯 Contribution Guidelines

### New Features
1. **Check existing issues** first
2. **Create issue** if none exists
3. **Discuss approach** before major changes
4. **Follow existing patterns** in codebase
5. **Add tests** for new functionality
6. **Update documentation** if needed

### Bug Fixes
1. **Reproduce the bug** locally
2. **Write test** that fails (proves bug exists)
3. **Fix the bug** with minimal changes
4. **Verify test passes** and no regressions
5. **Include clear description** in PR

### Documentation
- Update README.md for user-facing changes
- Add/update docstrings for new functions
- Update API documentation if endpoints change
- Include examples for complex features

## 📋 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Pre-commit hooks pass
- [ ] Documentation updated
- [ ] No merge conflicts with target branch

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass
- [ ] New tests added (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### Review Process
1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Address feedback** and update PR
4. **Approval** from at least one maintainer
5. **Merge** to target branch

## 🚦 Release Process

### Version Numbers
We use [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0) - Breaking changes
- **Minor** (1.X.0) - New features, backward compatible
- **Patch** (1.1.X) - Bug fixes, backward compatible

### Release Steps
1. Create `release/vX.X.X` branch from develop
2. Update version numbers and CHANGELOG.md
3. Final testing and bug fixes
4. Merge to main and tag release
5. Deploy to production
6. Merge back to develop

## 💬 Communication

- **GitHub Issues** - Bug reports, feature requests
- **GitHub Discussions** - General questions, ideas
- **Pull Requests** - Code review and collaboration

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://reactjs.org/docs/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Digital Ocean App Platform](https://docs.digitalocean.com/products/app-platform/)

## 🆘 Need Help?

- Check existing [issues](https://github.com/Meats-Central/ProjectMeats3/issues)
- Review [documentation](./docs/)
- Create new issue with detailed description
- Join discussions for questions and ideas

Thank you for contributing to ProjectMeats3! 🚀
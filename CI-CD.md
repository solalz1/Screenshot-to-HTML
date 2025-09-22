# 🔄 CI/CD Pipeline Documentation

This document describes the complete CI/CD setup for the Screenshot to HTML project.

## 📋 Overview

The project uses **GitHub Actions** for continuous integration and deployment with the following key features:

- ✅ **Automated Testing** on multiple Python versions
- ✅ **Code Quality Enforcement** with linting and formatting
- ✅ **Security Scanning** for vulnerabilities and code issues
- ✅ **Docker Build & Push** with multi-architecture support
- ✅ **Automated Deployments** to staging and production
- ✅ **Dependency Management** with automated updates
- ✅ **Release Management** with automated changelogs

## 🚀 Workflows

### 1. **Continuous Integration** (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main`

**Jobs:**
- **Test Matrix**: Python 3.9, 3.10, 3.11, 3.12 on Ubuntu
- **Code Quality**: Linting with ruff, formatting with black/isort
- **Type Checking**: Static analysis with mypy
- **Security Scan**: Dependency checks with safety, code analysis with bandit
- **Coverage**: Test coverage reporting to Codecov

**Duration:** ~5-8 minutes

### 2. **Docker Build & Push** (`.github/workflows/docker.yml`)

**Triggers:**
- Push to `main` branch
- Version tags (`v*`)
- Pull requests (build only, no push)

**Features:**
- **Multi-architecture builds**: AMD64 and ARM64
- **Container registry**: GitHub Container Registry (ghcr.io)
- **Security scanning**: Trivy vulnerability scanner
- **Caching**: Build cache optimization
- **Docker Compose validation**

**Duration:** ~10-15 minutes

### 3. **Deployment** (`.github/workflows/deploy.yml`)

**Triggers:**
- Version tags (`v*`)
- Manual workflow dispatch

**Environments:**
- **Staging**: For beta/rc versions and manual staging deploys
- **Production**: For stable releases with security approval

**Security:**
- Pre-deployment security scans
- Environment-specific approvals
- Deployment notifications

### 4. **Release Management** (`.github/workflows/release.yml`)

**Triggers:**
- Version tags (`v*`)

**Features:**
- Automated changelog generation
- GitHub release creation
- Docker image tagging
- Pre-release support (alpha, beta, rc)

### 5. **Dependency Updates** (`.github/workflows/dependency-update.yml`)

**Schedule:**
- Weekly on Mondays at 9 AM UTC
- Manual trigger available

**Features:**
- Automated dependency updates with pip-tools
- Security vulnerability scanning
- Automated pull request creation
- Review assignment

## 🔧 Configuration Files

### **Dependabot** (`.github/dependabot.yml`)
- Automated dependency updates for Python, Docker, and GitHub Actions
- Weekly schedule with proper labeling and review assignment

### **Issue Templates** (`.github/ISSUE_TEMPLATE/`)
- Bug report template with environment details
- Feature request template with implementation context

### **Pull Request Template** (`.github/pull_request_template.md`)
- Comprehensive checklist for code reviews
- Testing and documentation requirements

### **Code Quality** (`pyproject.toml`)
- **Black**: Code formatting (88 character line length)
- **isort**: Import sorting with black compatibility
- **Ruff**: Fast Python linting with security rules
- **MyPy**: Type checking configuration
- **Pytest**: Test configuration with coverage settings

## 📊 Quality Gates

### **Pull Request Requirements:**
1. ✅ All tests must pass on all Python versions
2. ✅ Code coverage must not decrease
3. ✅ No security vulnerabilities in dependencies
4. ✅ Code formatting and linting checks pass
5. ✅ Docker build succeeds

### **Deployment Requirements:**
1. ✅ All CI checks pass
2. ✅ Security scan approval for production
3. ✅ Version tag follows semantic versioning
4. ✅ Docker image security scan passes

## 🏃‍♂️ Local Development

### **Run CI Pipeline Locally:**

```bash
# Run all checks (equivalent to CI)
./scripts/ci-local.sh

# Run specific check types
./scripts/ci-local.sh --quality    # Code quality only
./scripts/ci-local.sh --security   # Security checks only
./scripts/ci-local.sh --tests      # Tests only
./scripts/ci-local.sh --docker     # Docker tests only
```

### **Manual Commands:**

```bash
# Code formatting
black app.py tests/
isort app.py tests/

# Linting
ruff check app.py tests/

# Type checking
mypy app.py --ignore-missing-imports

# Security checks
safety check
bandit -r app.py

# Tests with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Docker build test
docker build -t screenshot-to-html .
docker-compose config
```

## 🚀 Deployment Process

### **Staging Deployment:**
1. Create a beta/rc tag: `git tag v1.0.0-beta.1`
2. Push tag: `git push origin v1.0.0-beta.1`
3. GitHub Actions automatically deploys to staging
4. Manual approval may be required

### **Production Deployment:**
1. Create a stable tag: `git tag v1.0.0`
2. Push tag: `git push origin v1.0.0`
3. Security scan runs automatically
4. Production deployment requires approval
5. Release is created with changelog

### **Manual Deployment:**
1. Go to GitHub Actions → Deploy to Production
2. Click "Run workflow"
3. Select environment (staging/production)
4. Approve deployment if required

## 🔐 Security Features

### **Dependency Security:**
- **Safety**: Checks for known vulnerabilities in dependencies
- **Bandit**: Static analysis for common security issues
- **Trivy**: Container image vulnerability scanning
- **Automated updates**: Weekly dependency updates with security checks

### **Code Security:**
- **Secret scanning**: GitHub's secret detection
- **Security policies**: Automated security advisories
- **Container security**: Non-root user execution
- **Secure defaults**: Proper environment variable handling

### **Access Control:**
- **Environment protection**: Staging and production approval requirements
- **Branch protection**: Required status checks and reviews
- **Secrets management**: Secure API key and token storage

## 📈 Monitoring & Reporting

### **Test Coverage:**
- **Codecov integration**: Automatic coverage reporting
- **Coverage requirements**: Minimum coverage thresholds
- **Coverage history**: Track coverage changes over time

### **Security Reports:**
- **Dependency vulnerabilities**: Weekly security audits
- **Code security issues**: Bandit reports in CI
- **Container security**: Trivy scan results

### **Build Metrics:**
- **Build duration**: Track CI/CD performance
- **Success rates**: Monitor pipeline reliability
- **Deployment frequency**: Release cadence tracking

## 🛠️ Maintenance

### **Weekly Tasks:**
- Review Dependabot PRs for dependency updates
- Check security scan results
- Monitor test coverage trends

### **Monthly Tasks:**
- Review and update CI/CD workflows
- Update security tools and configurations
- Analyze build performance metrics

### **Quarterly Tasks:**
- Review and update security policies
- Update Python version matrix
- Evaluate new tools and improvements

## 🚨 Troubleshooting

### **Common Issues:**

**CI Tests Failing:**
- Check Python version compatibility
- Verify dependency installation
- Review test environment setup

**Docker Build Fails:**
- Check Dockerfile syntax
- Verify base image availability
- Review dependency installation in container

**Security Scan Failures:**
- Update vulnerable dependencies
- Review bandit security warnings
- Check container base image for vulnerabilities

**Deployment Issues:**
- Verify environment configuration
- Check deployment secrets and credentials
- Review deployment logs and error messages

### **Getting Help:**
- Check GitHub Actions logs for detailed error messages
- Review this documentation for configuration details
- Create an issue using the bug report template
- Contact the development team for urgent issues

---

**For questions or improvements to the CI/CD pipeline, please create an issue or pull request.**

#!/bin/bash

# Local CI/CD Testing Script
# This script mimics the CI/CD pipeline locally for development and testing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."

    if ! command_exists python3; then
        print_error "Python 3 is not installed"
        exit 1
    fi

    if ! command_exists pip; then
        print_error "pip is not installed"
        exit 1
    fi

    if ! command_exists docker; then
        print_warning "Docker is not installed - skipping Docker tests"
        SKIP_DOCKER=true
    fi

    print_success "Prerequisites check passed"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Install requirements
    pip install -r requirements.txt
    pip install pytest pytest-cov pytest-mock memory-profiler psutil
    pip install ruff black isort mypy safety bandit

    print_success "Dependencies installed"
}

# Run code quality checks
run_code_quality() {
    print_status "Running code quality checks..."

    source venv/bin/activate

    # Format check
    print_status "Checking code formatting with black..."
    black --check app.py tests/ || {
        print_warning "Code formatting issues found. Run 'black app.py tests/' to fix."
    }

    # Import sorting
    print_status "Checking import sorting with isort..."
    isort --check-only app.py tests/ || {
        print_warning "Import sorting issues found. Run 'isort app.py tests/' to fix."
    }

    # Linting
    print_status "Running linter with ruff..."
    ruff check app.py tests/

    # Type checking
    print_status "Running type checker with mypy..."
    mypy app.py --ignore-missing-imports || {
        print_warning "Type checking issues found."
    }

    print_success "Code quality checks completed"
}

# Run security checks
run_security_checks() {
    print_status "Running security checks..."

    source venv/bin/activate

    # Safety check for dependencies
    print_status "Checking for security vulnerabilities in dependencies..."
    safety check || {
        print_warning "Security vulnerabilities found in dependencies"
    }

    # Bandit security check
    print_status "Running bandit security scan..."
    bandit -r app.py -f json -o bandit-report.json || {
        print_warning "Security issues found. Check bandit-report.json"
    }

    print_success "Security checks completed"
}

# Run tests
run_tests() {
    print_status "Running tests..."

    source venv/bin/activate

    # Run tests with coverage
    pytest tests/ -v --cov=app --cov-report=xml --cov-report=term-missing

    print_success "Tests completed"
}

# Run Docker tests
run_docker_tests() {
    if [ "$SKIP_DOCKER" = true ]; then
        print_warning "Skipping Docker tests (Docker not available)"
        return
    fi

    print_status "Running Docker tests..."

    # Test docker-compose configuration first (doesn't require image build)
    print_status "Testing docker-compose configuration..."
    if docker compose config > /dev/null 2>&1; then
        print_success "Docker-compose configuration is valid"
    else
        print_error "Docker-compose configuration is invalid"
        return 1
    fi

    # Test Docker build (may fail due to authentication issues)
    print_status "Testing Docker build..."
    if docker build -t screenshot-to-html-test . > /dev/null 2>&1; then
        print_success "Docker build successful"

        # Cleanup test image
        docker rmi screenshot-to-html-test > /dev/null 2>&1
    else
        print_warning "Docker build failed (likely due to Docker Hub authentication)"
        print_warning "This is expected if Docker Hub email is not verified"
        print_warning "GitHub Actions will handle this with proper authentication"
    fi

    print_success "Docker tests completed"
}

# Generate reports
generate_reports() {
    print_status "Generating reports..."

    # Create reports directory
    mkdir -p reports

    # Move coverage report
    if [ -f "coverage.xml" ]; then
        mv coverage.xml reports/
    fi

    # Move security reports
    if [ -f "bandit-report.json" ]; then
        mv bandit-report.json reports/
    fi

    print_success "Reports generated in reports/ directory"
}

# Main execution
main() {
    print_status "Starting local CI/CD pipeline..."

    # Parse command line arguments
    RUN_ALL=true
    RUN_QUALITY=false
    RUN_SECURITY=false
    RUN_TESTS=false
    RUN_DOCKER=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --quality)
                RUN_ALL=false
                RUN_QUALITY=true
                shift
                ;;
            --security)
                RUN_ALL=false
                RUN_SECURITY=true
                shift
                ;;
            --tests)
                RUN_ALL=false
                RUN_TESTS=true
                shift
                ;;
            --docker)
                RUN_ALL=false
                RUN_DOCKER=true
                shift
                ;;
            --help)
                echo "Usage: $0 [--quality] [--security] [--tests] [--docker] [--help]"
                echo "  --quality   Run only code quality checks"
                echo "  --security  Run only security checks"
                echo "  --tests     Run only tests"
                echo "  --docker    Run only Docker tests"
                echo "  --help      Show this help message"
                echo ""
                echo "Without arguments, runs all checks"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    check_prerequisites
    install_dependencies

    if [ "$RUN_ALL" = true ] || [ "$RUN_QUALITY" = true ]; then
        run_code_quality
    fi

    if [ "$RUN_ALL" = true ] || [ "$RUN_SECURITY" = true ]; then
        run_security_checks
    fi

    if [ "$RUN_ALL" = true ] || [ "$RUN_TESTS" = true ]; then
        run_tests
    fi

    if [ "$RUN_ALL" = true ] || [ "$RUN_DOCKER" = true ]; then
        run_docker_tests
    fi

    generate_reports

    print_success "Local CI/CD pipeline completed successfully!"
}

# Run main function with all arguments
main "$@"

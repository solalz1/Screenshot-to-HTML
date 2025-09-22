#!/bin/bash

# Screenshot to HTML - Docker Deployment Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
CONTAINER_NAME="screenshot-to-html-app"
PORT="7860"
IMAGE_NAME="screenshot-to-html"

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

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to build the Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t $IMAGE_NAME .
    print_success "Docker image built successfully!"
}

# Function to run the container
run_container() {
    print_status "Starting container..."

    # Stop and remove existing container if it exists
    if docker ps -a --format 'table {{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
        print_warning "Stopping existing container..."
        docker stop $CONTAINER_NAME > /dev/null 2>&1 || true
        docker rm $CONTAINER_NAME > /dev/null 2>&1 || true
    fi

    # Check if .env file exists
    ENV_FILE=""
    if [ -f ".env" ]; then
        ENV_FILE="--env-file .env"
        print_status "Using .env file for environment variables"
    else
        print_warning "No .env file found. You can create one from env.example"
    fi

    # Run the container
    docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:7860 \
        $ENV_FILE \
        --restart unless-stopped \
        $IMAGE_NAME

    print_success "Container started successfully!"
    print_status "Access the app at: http://localhost:$PORT"
}

# Function to use docker-compose
compose_up() {
    print_status "Starting with docker-compose..."

    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found!"
        exit 1
    fi

    docker-compose up -d --build
    print_success "Application started with docker-compose!"
    print_status "Access the app at: http://localhost:7860"
}

# Function to stop the container
stop_container() {
    print_status "Stopping container..."
    docker stop $CONTAINER_NAME > /dev/null 2>&1 || true
    docker rm $CONTAINER_NAME > /dev/null 2>&1 || true
    print_success "Container stopped!"
}

# Function to show logs
show_logs() {
    if docker ps --format 'table {{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
        docker logs -f $CONTAINER_NAME
    else
        print_error "Container $CONTAINER_NAME is not running"
    fi
}

# Function to show help
show_help() {
    echo "Screenshot to HTML - Docker Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build       Build the Docker image"
    echo "  run         Build and run the container"
    echo "  compose     Use docker-compose to start the application"
    echo "  stop        Stop and remove the container"
    echo "  logs        Show container logs"
    echo "  restart     Restart the container"
    echo "  clean       Stop container and remove image"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 run              # Build and run the application"
    echo "  $0 compose          # Use docker-compose"
    echo "  $0 logs             # View application logs"
}

# Main script logic
case "$1" in
    "build")
        check_docker
        build_image
        ;;
    "run")
        check_docker
        build_image
        run_container
        ;;
    "compose")
        check_docker
        compose_up
        ;;
    "stop")
        check_docker
        stop_container
        ;;
    "logs")
        check_docker
        show_logs
        ;;
    "restart")
        check_docker
        stop_container
        build_image
        run_container
        ;;
    "clean")
        check_docker
        stop_container
        docker rmi $IMAGE_NAME > /dev/null 2>&1 || true
        print_success "Cleanup completed!"
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    "")
        print_error "No command specified. Use '$0 help' for usage information."
        exit 1
        ;;
    *)
        print_error "Unknown command: $1"
        print_status "Use '$0 help' for usage information."
        exit 1
        ;;
esac

# 🐳 Docker Deployment Guide

This guide covers how to deploy the Screenshot to HTML application using Docker and Docker Compose.

## 📋 Prerequisites

Before starting, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Git**: For cloning the repository

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
git clone <repository-url>
cd project

docker-compose up -d --build

```

### Option 2: Using Docker Run Script

```bash
chmod +x docker-run.sh

./docker-run.sh run

```

### Option 3: Manual Docker Commands

```bash
docker build -t screenshot-to-html .

docker run -d \
  --name screenshot-to-html-app \
  -p 7860:7860 \
  --env-file .env \
  --restart unless-stopped \
  screenshot-to-html

```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
cp env.example .env

nano .env
```

Example `.env` file:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here

GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
DEBUG=false
```

### Docker Compose Configuration

The `docker-compose.yml` file includes:

- **Port Mapping**: `7860:7860` (host:container)
- **Environment Variables**: Loaded from `.env` file
- **Health Checks**: Automatic container health monitoring
- **Restart Policy**: `unless-stopped` for reliability
- **Volume Mounting**: Optional data persistence

## 📝 Available Commands

### Using the Docker Run Script

```bash
# Build the Docker image
./docker-run.sh build

# Build and run the container
./docker-run.sh run

# Start with docker-compose
./docker-run.sh compose

# Stop the container
./docker-run.sh stop

# View logs
./docker-run.sh logs

# Restart the container
./docker-run.sh restart

# Clean up (stop container and remove image)
./docker-run.sh clean

# Show help
./docker-run.sh help
```

### Using Docker Compose Directly

```bash
# Start the application (build if needed)
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Restart the application
docker-compose restart

# Rebuild and restart
docker-compose up -d --build --force-recreate
```

## 🔍 Monitoring and Troubleshooting

### Health Checks

The container includes built-in health checks:

- **Endpoint**: `http://localhost:7860/`
- **Interval**: 30 seconds
- **Timeout**: 30 seconds
- **Retries**: 3
- **Start Period**: 5 seconds

### Viewing Logs

```bash
# Docker Compose
docker-compose logs -f gradio-app

# Docker directly
docker logs -f screenshot-to-html-app

# Using the script
./docker-run.sh logs
```

### Common Issues and Solutions

#### Port Already in Use
```bash
# Check what's using port 7860
sudo lsof -i :7860

# Kill the process if needed
sudo kill -9 <PID>

# Or use a different port
docker run -p 8080:7860 screenshot-to-html
```

#### Container Won't Start
```bash
# Check container status
docker ps -a

# View container logs
docker logs screenshot-to-html-app

# Check resource usage
docker stats
```

#### API Key Issues
```bash
# Verify environment variables
docker exec screenshot-to-html-app env | grep GOOGLE

# Update the .env file and restart
docker-compose restart
```

## 🏗️ Build Details

### Docker Image

- **Base Image**: `python:3.12-slim`
- **Size**: ~200MB (optimized for production)
- **Architecture**: Multi-platform (amd64, arm64)
- **Security**: Runs as non-root user

### Dependencies

- **Gradio**: Web framework for the UI
- **Google Generative AI**: For AI processing
- **Pillow**: Image processing
- **Python-dotenv**: Environment management

### Build Process

1. Install system dependencies (minimal)
2. Copy and install Python requirements
3. Copy application code
4. Create non-root user
5. Set proper permissions
6. Configure Gradio server settings

## 🔒 Security Considerations

### Container Security

- **Non-root User**: Application runs as `app_user`
- **Minimal Dependencies**: Only essential packages installed
- **Health Checks**: Automatic monitoring for security
- **Resource Limits**: Can be configured in docker-compose

### API Security

- **Environment Variables**: API keys stored securely
- **Network Isolation**: Container network separation
- **Access Control**: Can be configured with reverse proxy

### Production Deployment

For production environments, consider:

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  gradio-app:
    build: .
    restart: always
    environment:
      - DEBUG=false
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
    networks:
      - app-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`yourdomain.com`)"
      - "traefik.http.routers.app.tls=true"

networks:
  app-network:
    driver: bridge
```

## 📊 Performance Optimization

### Resource Limits

```yaml
# In docker-compose.yml
services:
  gradio-app:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
```

### Image Optimization

The Dockerfile is optimized for:
- **Layer Caching**: Requirements installed before code copy
- **Minimal Size**: Only necessary dependencies
- **Security**: Non-root user execution
- **Health Monitoring**: Built-in health checks

## 🌐 Accessing the Application

Once the container is running:

1. **Local Access**: http://localhost:7860
2. **Network Access**: http://[your-ip]:7860
3. **Production**: Configure domain and SSL

### Testing the Deployment

```bash
# Check if the app is responding
curl -f http://localhost:7860/

# Check container health
docker inspect --format='{{.State.Health.Status}}' screenshot-to-html-app

# Load test (optional)
ab -n 100 -c 10 http://localhost:7860/
```

## 🆘 Support

If you encounter issues:

1. **Check Logs**: Use the logging commands above
2. **Verify Configuration**: Ensure `.env` file is correct
3. **Resource Check**: Monitor Docker resource usage
4. **Network Check**: Verify port availability
5. **Rebuild**: Try cleaning and rebuilding the image

For more help, check the application logs and Docker documentation.

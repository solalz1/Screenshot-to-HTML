# 🌐 Screenshot to HTML with Gemini AI

A powerful Gradio application that uses Google's Gemini AI to analyze screenshots of websites and generate complete HTML code to recreate them. The app provides both the generated code and a live interactive preview.

## ✨ Features

- **Screenshot Upload**: Upload images (PNG, JPG, JPEG, GIF, BMP, WEBP) of websites
- **AI-Powered Analysis**: Uses Google Gemini AI models for intelligent website analysis
- **Complete HTML Generation**: Generates standalone HTML files with embedded CSS and JavaScript
- **Live Preview**: View the generated website in an interactive iframe preview
- **Modern Design**: Responsive, mobile-friendly layouts with modern CSS techniques
- **User-Friendly Interface**: Clean, intuitive Gradio interface with helpful instructions
- **Comprehensive Testing**: Full test suite with 73% code coverage

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key (get it from [Google AI Studio](https://aistudio.google.com/app/apikey))

### Installation

1. Clone or download this project
2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Run the Gradio app:

```bash
python app.py
```

6. Open your browser and go to the link displayed (maybe `http://127.0.0.1:7860`)

### Usage

1. **Enter API Key**: Input your Gemini API key in the input field
2. **Upload Screenshot**: Choose a screenshot of the website you want to recreate
3. **Generate Code**: Click the "Send" button to generate HTML code
4. **View Results**: 
   - **HTML Tab**: See the live interactive website preview
   - **Code Tab**: View and copy the generated HTML code

## 📋 Requirements

The app requires the following Python packages:

- `gradio>=4.0.0` - Web app framework
- `google-generativeai>=0.8.0` - Google Gemini AI integration
- `pillow>=10.0.0` - Image processing
- `python-dotenv>=1.0.0` - Environment variable management

## 🔧 Configuration

### Getting Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and paste it into the app's input field

### Supported File Types

**Images:**
- PNG, JPG, JPEG, GIF, BMP, WEBP

Upload screenshots of websites you want to recreate as HTML code.

## 🎯 How It Works

1. **Image Processing**: The app processes uploaded screenshot images directly
2. **AI Analysis**: Google Gemini analyzes the visual content and understands the website structure
3. **Code Generation**: The AI generates complete HTML code with:
   - Semantic HTML structure
   - Embedded CSS styling
   - Responsive design
   - Interactive elements
   - Modern web practices
4. **Preview Rendering**: The generated code is rendered in an interactive iframe preview

## 🔒 Privacy & Security

- API keys are handled securely and not stored
- Uploaded files are processed locally and temporarily
- No data is permanently stored on the server
- All processing happens in your local environment

## 🔄 CI/CD Workflows

The project includes several automated workflows:

### **1. Continuous Integration (`ci.yml`)**
Triggered on push to `main`/`develop` and pull requests:
- Multi-version Python testing (3.9-3.12)
- Code quality checks (ruff, black, isort, mypy)
- Security scanning (safety, bandit)
- Test coverage reporting

### **2. Docker Build (`docker.yml`)**
Triggered on push to `main` and tags:
- Multi-architecture Docker builds (AMD64, ARM64)
- Container security scanning with Trivy
- Automatic pushes to GitHub Container Registry
- Docker Compose validation

### **3. Deployment (`deploy.yml`)**
Triggered on version tags and manual dispatch:
- Staging and production deployment environments
- Security scan requirements for production
- Deployment notifications

### **4. Release Management (`release.yml`)**
Triggered on version tags:
- Automatic release creation with changelogs
- Docker image publishing
- Documentation updates

### **5. Dependency Updates (`dependency-update.yml`)**
Scheduled weekly:
- Automated dependency updates via Dependabot
- Security vulnerability scanning
- Automated pull request creation

## 🛠️ Troubleshooting

### Common Issues

**"Error configuring Gemini API"**
- Verify your API key is correct
- Check your internet connection
- Ensure your API key has proper permissions

**"Error rendering HTML"**
- The generated HTML might contain complex elements
- Try refreshing the page and generating again
- Check that your Gemini API key is valid

### Tips for Best Results

- Use high-quality screenshots with clear text and layouts
- Ensure good contrast and lighting in images
- Simple layouts tend to generate more accurate results
- Take screenshots of complete website sections

### Virtual Environment Management

**To deactivate the virtual environment:**
```bash
deactivate
```

**To reactivate later:**
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

## 🧪 Testing

This project includes a comprehensive test suite with **73% code coverage** to ensure reliability and catch regressions.

### Test Suite Overview

The test suite covers:
- ✅ **Data Processing**: HTML extraction, validation, error handling
- ✅ **File Operations**: Reading, error handling, Unicode support  
- ✅ **HTML Processing**: Content preparation, iframe generation, escaping
- ✅ **API Integration**: Key validation, error handling (with mocking)
- ✅ **UI Functions**: Basic Gradio component handling
- ✅ **Edge Cases**: Large content, special characters, malformed input
- ✅ **Integration**: End-to-end pipelines

### Running Tests

**Install test dependencies:**
```bash
pip install pytest pytest-cov pytest-mock memory-profiler psutil
```

**Run all tests:**
```bash
pytest tests/ -v
```

**Run tests with coverage report:**
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

**Run specific test categories:**
```bash
# API validation tests
pytest tests/test_app.py::TestAPIValidation -v

# Data processing tests
pytest tests/test_app.py::TestDataProcessing -v

# HTML processing tests
pytest tests/test_app.py::TestHTMLProcessing -v
```

### Test Results

```
25 tests collected
✅ 25 passed, 0 failed
📊 73% code coverage
⚡ All tests complete in ~3 seconds
```

### Test Structure

```
tests/
├── test_app.py              # Main test suite (25 tests)
│   ├── TestDataProcessing   # HTML extraction & validation
│   ├── TestFileOperations   # File reading & error handling
│   ├── TestHTMLProcessing   # Content preparation & escaping
│   ├── TestExampleHandling  # Cached examples functionality
│   ├── TestUIFunctions      # Gradio component handling
│   ├── TestAPIValidation    # Gemini API integration
│   ├── TestDataValidation   # Input validation & security
│   ├── TestEdgeCases        # Boundary conditions & error cases
│   └── TestIntegration      # End-to-end functionality
```

### Continuous Integration & Deployment

The project includes comprehensive CI/CD pipelines with GitHub Actions:

#### **Automated Testing**
- **Multi-Python Support** - Tests on Python 3.9, 3.10, 3.11, 3.12
- **Code Quality Checks** - Linting with ruff, formatting with black
- **Security Scanning** - Dependency vulnerability checks with safety and bandit
- **Coverage Reporting** - Automatic coverage reporting to Codecov
- **Cross-platform** - Tests run on Linux, with Docker builds for multiple architectures

#### **Docker & Deployment**
- **Automated Docker Builds** - Multi-architecture images (AMD64, ARM64)
- **Container Registry** - Automatic pushes to GitHub Container Registry
- **Security Scanning** - Trivy vulnerability scanning for container images
- **Deployment Automation** - Staging and production deployment workflows

#### **Dependency Management**
- **Dependabot Integration** - Automated dependency updates
- **Security Monitoring** - Weekly security audits
- **Automated PRs** - Dependency updates via pull requests

#### **Release Management**
- **Automated Releases** - Tag-based release creation with changelogs
- **Semantic Versioning** - Support for pre-release versions (alpha, beta, rc)
- **Container Tagging** - Docker images tagged with version numbers

## 🐳 Docker Deployment

The application is fully containerized and ready for deployment with Docker:

### Quick Start with Docker

#### **Method 1: Docker Compose (Recommended)**
```bash
# 1. Copy and edit environment file
cp env.example .env
# Edit .env and add your Gemini API key

# 2. Start the application
docker-compose up -d --build

# 3. Access your app at http://localhost:7860
```

#### **Method 2: Using the Helper Script**
```bash
# 1. Make the script executable
chmod +x docker-run.sh

# 2. Build and run the application
./docker-run.sh run

# 3. Other useful commands:
./docker-run.sh logs    # View app logs
./docker-run.sh stop    # Stop the app
./docker-run.sh restart # Restart the app
./docker-run.sh help    # Show all commands
```

#### **Method 3: Manual Docker Commands**
```bash
# 1. Build the Docker image
docker build -t screenshot-to-html .

# 2. Run the container
docker run -d \
  --name screenshot-to-html-app \
  -p 7860:7860 \
  --env-file .env \
  --restart unless-stopped \
  screenshot-to-html

# 3. Access your app at http://localhost:7860
```

### Docker Management Commands

```bash
# View running containers
docker ps

# View application logs
docker logs screenshot-to-html-app
# or with docker-compose:
docker-compose logs -f

# Stop the application
docker stop screenshot-to-html-app
# or with docker-compose:
docker-compose down

# Restart the application
docker restart screenshot-to-html-app
# or with docker-compose:
docker-compose restart

# Update after code changes
docker-compose up -d --build --force-recreate

# Clean up (remove containers and images)
docker-compose down --rmi all --volumes
```

### Configuration

1. **Copy environment file**: `cp env.example .env`
2. **Add your API key**: Edit `.env` and add your Gemini API key
3. **Start the container**: Choose one of the 3 methods above
4. **Access the app**: http://localhost:7860

### Docker Features

- ✅ **Optimized Build**: Multi-stage build with minimal dependencies
- ✅ **Security**: Non-root user execution
- ✅ **Health Checks**: Automatic container monitoring
- ✅ **Environment Config**: Easy configuration via `.env` file
- ✅ **Volume Mounting**: Optional data persistence
- ✅ **Auto-restart**: Container restarts on failure

For detailed Docker documentation, see **[DOCKER.md](DOCKER.md)**

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving the code
- Adding documentation

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Gradio](https://gradio.app/)
- Powered by [Google Gemini AI](https://ai.google.dev/)
- Image handling with [Pillow](https://pillow.readthedocs.io/)
- Testing with [pytest](https://pytest.org/)

---

**Happy coding! 🚀** 
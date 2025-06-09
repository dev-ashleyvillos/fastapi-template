# FastAPI Template

A production-ready FastAPI server template with Docker support, comprehensive logging, and deployment configurations. Perfect for starting new FastAPI projects quickly.

## ✨ Features

- **FastAPI** with automatic API documentation
- **Docker** support with docker-compose
- **Rotating logs** to prevent disk space issues
- **Environment-based configuration**
- **cPanel/Passenger deployment** ready
- **Example routes** for reference
- **Production and development configurations**

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (for containerized development)
- Git

### Using This Template

1. **Clone or download this template**
   ```bash
   # Method 1: Clone directly
   git clone <this-template-url> your-project-name
   cd your-project-name
   
   # Method 2: Use GitHub's "Use this template" button
   # Method 3: Download ZIP and extract
   ```

2. **Customize for your project**
   ```bash
   # Update project name in main.py
   # Update docker-compose service name if needed
   # Modify README.md for your project
   ```

### Local Development (Without Docker)

1. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run the server**
   ```bash
   python main.py
   ```

The server will start at `http://localhost:5001`

### Docker Development (Recommended)

1. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Docker settings
   ```

2. **Build and run**
   ```bash
   # Build and start the container
   docker-compose up --build
   
   # Or run in background
   docker-compose up -d --build
   ```

3. **View logs**
   ```bash
   # Follow logs
   docker-compose logs -f fastapi-app
   
   # View recent logs
   docker-compose logs --tail=50 fastapi-app
   ```

4. **Stop the server**
   ```bash
   docker-compose down
   ```

## 📋 API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: `http://localhost:5001/docs` (Swagger UI)
- **Alternative API Docs**: `http://localhost:5001/redoc` (ReDoc)
- **Health Check**: `http://localhost:5001/` or `http://localhost:5001/health`

### Available Endpoints

#### Main API (`/api`)
- `GET /api/test` - Simple test endpoint

#### Examples (`/example`) 
*Note: These are documentation examples showing FastAPI features*
- `GET /example/simple` - Basic endpoint example
- `GET /example/query-params` - Query parameter examples
- `GET /example/users/{user_id}` - Path parameter examples
- `POST /example/chat` - Request body + query params example
- `POST /example/users` - Pydantic model validation example
- `GET /example/conversations/{id}/messages` - Pagination example
- `GET /example/error-examples/{code}` - HTTP error examples

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Python interpreter path (required for passenger_wsgi.py deployment)
PYTHON_DIR="/path/to/your/venv/bin/python"

# Debug mode - shows detailed error messages and tracebacks
DEBUG=false

# Auto-reload on code changes (development only)
RELOAD=false

# Logging verbosity (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

### Development vs Production Settings

#### Development Settings
```env
DEBUG=true
RELOAD=true
LOG_LEVEL=DEBUG
```

#### Production Settings
```env
DEBUG=false
RELOAD=false
LOG_LEVEL=INFO
```

## 🐳 Docker Commands

### Basic Operations
```bash
# Build and start
docker-compose up --build

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Restart the service
docker-compose restart fastapi-app

# View logs
docker-compose logs -f fastapi-app

# Execute commands in running container
docker-compose exec fastapi-app bash
```

### Troubleshooting Docker

#### Problem: Watchfiles logging spam
**Solution**: Set `RELOAD=false` in your `.env` file

#### Problem: Changes not reflecting
**Solutions**:
1. If `RELOAD=false`: Restart the container manually
   ```bash
   docker-compose restart fastapi-app
   ```
2. If you want hot reload: Set `RELOAD=true` (accept verbose logs)

#### Problem: Container won't start
**Solutions**:
1. Check logs: `docker-compose logs fastapi-app`
2. Rebuild: `docker-compose up --build`
3. Remove and rebuild: `docker-compose down && docker-compose up --build`

## 📁 Project Structure

```
fastapi-template/
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py          # Main API routes
│   │   └── example.py      # Documentation examples
│   └── utils/
│       ├── __init__.py
│       └── logs.py         # Logging configuration
├── logs/                   # Log files (auto-generated)
├── .env                    # Environment variables (create from .env.example)
├── .env.example           # Environment template
├── .gitignore
├── docker-compose.yml     # Docker services
├── Dockerfile            # Container definition
├── main.py              # FastAPI application entry point
├── passenger_wsgi.py    # WSGI adapter for cPanel/Passenger deployment
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 📝 Logging

The application uses rotating log files to prevent disk space issues:

- **Location**: `logs/` directory
- **File naming**: `app_YYYYMMDD.log`
- **Rotation**: When a log file reaches 10MB, it rotates
- **Retention**: Keeps 5 log files (maximum 50MB total)
- **Control**: Use `LOG_LEVEL` environment variable

### Log Levels
- `DEBUG`: Very detailed logs (function calls, variables)
- `INFO`: General information (requests, server events)
- `WARNING`: Potential issues
- `ERROR`: Serious problems only

## 🚢 Deployment

### cPanel/Passenger Deployment

1. **Upload files** to your cPanel hosting
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Update environment variables** in `.env`:
   ```env
   PYTHON_DIR="/home/username/virtualenv/projectname/bin/python"
   DEBUG=false
   RELOAD=false
   LOG_LEVEL=INFO
   ```
4. **Configure passenger_wsgi.py** (already included and configured)
5. **Set document root** to your project directory

### Production Docker

For production deployment:

```bash
# Build production image
docker build -t your-app-name .

# Run production container
docker run -d \\
  --name your-app-name \\
  -p 5001:5001 \\
  -e DEBUG=false \\
  -e RELOAD=false \\
  -e LOG_LEVEL=INFO \\
  your-app-name
```

## 🛠️ Customizing This Template

### 1. Update Project Information

**In `main.py`:**
```python
app = FastAPI(
    title="Your Project Name",
    description="Your project description",
    version="1.0.0",
    # ... other settings
)
```

**In `docker-compose.yml`:**
```yaml
services:
  your-app-name:  # Change service name
    # ... rest of configuration
```

### 2. Add Your Routes

**Create new route files:**
```python
# app/routes/your_routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/your-prefix", tags=["your-tag"])

@router.get("/your-endpoint")
async def your_endpoint():
    return {"message": "Your custom endpoint"}
```

**Include in main.py:**
```python
from app.routes.your_routes import router as your_router
app.include_router(your_router)
```

### 3. Remove Example Routes (Optional)

If you don't need the example routes:
1. Delete `app/routes/example.py`
2. Remove the import and include statement from `main.py`

## 🔧 Common Issues

### Port Already in Use
```bash
# Find and kill process using port 5001
lsof -ti:5001 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "5002:5001"  # Use different external port
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🎯 What's Included

- ✅ **FastAPI setup** with automatic docs
- ✅ **Docker configuration** for development and production
- ✅ **Environment-based configuration**
- ✅ **Rotating log files** with size limits
- ✅ **Health check endpoints**
- ✅ **Example routes** showing FastAPI features
- ✅ **cPanel/Passenger deployment** configuration
- ✅ **Production-ready** error handling
- ✅ **Type hints** and **Pydantic models**
- ✅ **CORS configuration** ready (just uncomment in main.py)

## 🤝 Contributing to This Template

If you find improvements that would benefit the template:
1. Fork this repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## 📄 License

This template is provided as-is for educational and commercial use. Modify as needed for your projects.

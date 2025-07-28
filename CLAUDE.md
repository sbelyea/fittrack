# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FitTrack is a web application for tracking fitness goals, with a primary focus on weightlifting. It's built using a JavaScript/Python/MySQL tech stack with Flask as the backend framework.

## Tech Stack

- **Backend**: Python Flask with SQLAlchemy ORM
- **Frontend**: HTML/CSS/JavaScript (Vanilla JS)
- **Database**: MySQL with PyMySQL driver
- **Authentication**: Flask-Login with password hashing

## Development Commands

### Docker (Recommended)
```bash
# Start everything (first time)
docker-compose up

# Start in background
docker-compose up -d

# Stop everything
docker-compose down

# View logs
docker-compose logs

# Rebuild after code changes
docker-compose up --build

# Fresh start (removes all data)
docker-compose down -v && docker-compose up

# Quick scripts
./start-docker.sh    # Linux/Mac
start-docker.bat     # Windows
```

### Manual Setup (Alternative)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Setup database and environment
python database_setup.py

# Quick setup (Windows)
setup.bat

# Quick setup (Linux/Mac)
./setup.sh

# Start development server
python run.py
# or
python app.py

# Access at http://localhost:5000
```

## Project Structure

```
fittrack/
├── app.py                  # Main Flask application
├── run.py                  # Application runner
├── database_setup.py       # Database initialization script
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Multi-container setup
├── .dockerignore          # Docker ignore file
├── .env.docker            # Docker environment config
├── start-docker.sh/bat    # Easy Docker startup scripts
├── stop-docker.sh/bat     # Easy Docker stop scripts
├── DOCKER_SETUP.md        # Complete Docker guide
├── templates/             # Jinja2 HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   └── dashboard.html    # User dashboard
├── static/               # Static assets
│   ├── css/style.css     # Main stylesheet
│   └── js/main.js        # Frontend JavaScript
├── docker/               # Docker configuration
│   └── mysql-init/       # Database initialization scripts
└── logs/                 # Application logs (Docker)
```

## Database Schema

### User Model (app.py:25)
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `created_at`: Registration timestamp

## Key Features

- User registration and authentication
- Secure password hashing with Werkzeug
- Session management with Flask-Login
- Responsive web design
- MySQL database integration
- Form validation (frontend and backend)

## Environment Configuration

### Docker (Recommended)
No manual configuration needed! Docker Compose handles everything automatically.

### Manual Setup
Copy `.env.example` to `.env` and configure:
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: MySQL connection string
- `MYSQL_*`: Individual MySQL connection parameters

## Docker Architecture

- **Web Container**: Python Flask application
- **MySQL Container**: Database with automatic initialization
- **Network**: Internal Docker network for secure communication
- **Volumes**: Persistent data storage for MySQL
- **Health Checks**: Automatic service monitoring

## Security Notes

- Passwords are hashed using Werkzeug's security functions
- Session management via Flask-Login
- CSRF protection ready (Flask-WTF included)
- Environment variables for sensitive configuration
- Docker containers run with non-root users
- Network isolation between containers
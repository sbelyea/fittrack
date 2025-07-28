# FitTrack

A personal fitness tracking application focused on weightlifting goals and progress monitoring.

## About

FitTrack is a personal project designed to help track fitness goals, with a primary focus on weightlifting. The application allows users to monitor their progress, set goals, and maintain a record of their fitness journey.

## Getting Started

You have two options to run FitTrack:

### Option 1: Docker (Recommended - Super Easy!) 🐳

**Prerequisites**: Just install Docker Desktop
- [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

**Quick Start**:
1. Download this project
2. Double-click `start-docker.bat` (Windows) or run `./start-docker.sh` (Mac/Linux)
3. Wait for everything to download and start
4. Open http://localhost:5000 in your browser
5. Create an account and start using FitTrack!

That's it! Docker handles everything automatically - no manual setup needed.

📖 **Need help with Docker?** See the complete [Docker Setup Guide](DOCKER_SETUP.md)

### Option 2: Manual Installation

**Prerequisites**:
- Python 3.7 or higher
- MySQL 5.7 or higher
- pip (Python package installer)

**Installation**:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fittrack
   ```

2. Run the setup script:
   - **Windows**: Double-click `setup.bat` or run `setup.bat` in command prompt
   - **Linux/Mac**: Run `chmod +x setup.sh && ./setup.sh`

3. Configure your database:
   - Edit the `.env` file with your MySQL credentials
   - Make sure MySQL server is running

4. Start the application:
   ```bash
   python run.py
   ```

5. Open your browser and go to `http://localhost:5000`

### Manual Setup (Alternative)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. Set up the database:
   ```bash
   python database_setup.py
   ```

4. Run the application:
   ```bash
   python run.py
   ```

## Docker Commands (Quick Reference)

```bash
# Start everything
docker-compose up

# Start in background
docker-compose up -d

# Stop everything
docker-compose down

# View logs
docker-compose logs

# Fresh start (WARNING: removes all data!)
docker-compose down -v && docker-compose up
```

## Features

- **User Authentication**: Secure user registration and login system
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dashboard**: Personal dashboard to track fitness progress
- **MySQL Database**: Robust data storage with MySQL integration
- **Security**: Password hashing and secure session management

### Planned Features

- Workout logging and tracking
- Goal setting and progress monitoring
- Exercise library and workout templates
- Progress charts and analytics
- Social features and workout sharing

## Contributing

This is a personal project, but suggestions and feedback are welcome.

## License

*To be determined*
# 🐳 FitTrack Docker Setup Guide

This guide will help you run FitTrack using Docker containers. Don't worry if you're new to Docker - we'll walk through everything step by step!

## What is Docker?

Docker is a tool that packages your application and all its dependencies into "containers" - think of them as lightweight virtual machines that work the same way on any computer.

## Prerequisites

You need to install Docker on your computer first:

### Windows
1. Download **Docker Desktop for Windows** from: https://www.docker.com/products/docker-desktop/
2. Run the installer and follow the setup wizard
3. Restart your computer when prompted
4. Open Docker Desktop and wait for it to start

### Mac
1. Download **Docker Desktop for Mac** from: https://www.docker.com/products/docker-desktop/
2. Drag Docker to your Applications folder
3. Open Docker from Applications and wait for it to start

### Linux (Ubuntu/Debian)
```bash
# Update your system
sudo apt update

# Install Docker
sudo apt install docker.io docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (so you don't need sudo)
sudo usermod -aG docker $USER

# Log out and log back in for changes to take effect
```

## Quick Start (The Easy Way!)

1. **Download the project** (if you haven't already):
   ```bash
   git clone <your-repository-url>
   cd fittrack
   ```

2. **Start everything with one command**:
   ```bash
   docker-compose up
   ```
   
   This will:
   - Download the MySQL database
   - Build your FitTrack application
   - Start both containers
   - Set up the database automatically

3. **Open your browser** and go to: http://localhost:5000

4. **Create an account** and start using FitTrack!

## What Just Happened?

When you ran `docker-compose up`, Docker:
1. Downloaded a MySQL 8.0 database image
2. Built your FitTrack application into a container
3. Created a network so they can talk to each other
4. Started both containers
5. Set up the database with the correct tables

## Useful Commands

### Start the application
```bash
# Start in the foreground (you'll see all the logs)
docker-compose up

# Start in the background (runs silently)
docker-compose up -d
```

### Stop the application
```bash
# Stop all containers
docker-compose down

# Stop and remove all data (fresh start)
docker-compose down -v
```

### View logs
```bash
# See logs from all containers
docker-compose logs

# See logs from just the web app
docker-compose logs web

# See logs from just the database
docker-compose logs mysql

# Follow logs in real-time
docker-compose logs -f
```

### Restart just one service
```bash
# Restart just the web application
docker-compose restart web

# Restart just the database
docker-compose restart mysql
```

## Troubleshooting

### Problem: "Port 5000 is already in use"
**Solution**: Either stop whatever is using port 5000, or change the port in `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Change 5000 to 8080 (or any available port)
```

### Problem: "Port 3306 is already in use"
**Solution**: You probably have MySQL already running. Either:
- Stop your local MySQL: `sudo service mysql stop` (Linux) or stop it from System Preferences (Mac)
- Or change the port in `docker-compose.yml`:
```yaml
ports:
  - "3307:3306"  # Change first 3306 to 3307
```

### Problem: "Permission denied" errors
**Solution**: 
- **Windows**: Make sure Docker Desktop is running as administrator
- **Linux**: Make sure you're in the docker group: `sudo usermod -aG docker $USER` then log out and back in

### Problem: Application won't start
**Solution**: Check the logs to see what's wrong:
```bash
docker-compose logs web
```

### Problem: Database connection errors
**Solution**: 
1. Make sure the database is healthy: `docker-compose ps`
2. Wait a bit longer - the database takes time to start
3. Check database logs: `docker-compose logs mysql`

## Advanced Usage

### Access the database directly
```bash
# Connect to MySQL command line
docker-compose exec mysql mysql -u fittrack_user -p fittrack

# Password is: fittrack_password
```

### Update the application
```bash
# Rebuild and restart after code changes
docker-compose up --build

# Or rebuild just the web service
docker-compose build web
docker-compose restart web
```

### Run commands inside the container
```bash
# Open a shell in the web container
docker-compose exec web bash

# Run a one-off command
docker-compose exec web python database_setup.py
```

## File Structure

Here's what the Docker files do:

```
fittrack/
├── Dockerfile              # Instructions to build the web app container
├── docker-compose.yml      # Defines both web and database containers
├── .dockerignore           # Files to exclude from the Docker image
├── .env.docker             # Environment variables for Docker
└── docker/
    └── mysql-init/
        └── 01-init.sql     # Database initialization script
```

## Production Notes

**⚠️ Important**: Before using this in production:

1. **Change the secret key** in `docker-compose.yml`
2. **Change database passwords** in `docker-compose.yml`
3. **Use proper SSL certificates**
4. **Set up proper backups** for the database
5. **Use a reverse proxy** like nginx

## Getting Help

If you're stuck:
1. Check the logs: `docker-compose logs`
2. Try a fresh start: `docker-compose down -v && docker-compose up`
3. Make sure Docker is running: `docker --version`
4. Check if ports are available: `netstat -an | grep 5000`

## Next Steps

Once everything is running, you can:
- Create a user account at http://localhost:5000/register
- Log in and explore the dashboard
- Start building additional features!

Happy coding! 🚀
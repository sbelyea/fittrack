@echo off
echo =================================
echo    Starting FitTrack with Docker
echo =================================
echo.

echo Checking if Docker is running...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not running!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

echo Docker is available!
echo.

echo Starting FitTrack application...
echo This may take a few minutes the first time as Docker downloads required images.
echo.

docker-compose up

echo.
echo Application stopped. Press any key to exit...
pause >nul
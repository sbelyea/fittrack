#!/bin/bash

echo "================================="
echo "   Starting FitTrack with Docker"
echo "================================="
echo ""

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed!"
    echo "Please install Docker first:"
    echo "- Ubuntu/Debian: sudo apt install docker.io docker-compose"
    echo "- Mac: Download Docker Desktop from https://www.docker.com/products/docker-desktop/"
    echo ""
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "ERROR: Docker is not running!"
    echo "Please start Docker:"
    echo "- Linux: sudo systemctl start docker"
    echo "- Mac: Open Docker Desktop application"
    echo ""
    exit 1
fi

echo "Docker is available!"
echo ""

echo "Starting FitTrack application..."
echo "This may take a few minutes the first time as Docker downloads required images."
echo ""

# Start the application
docker-compose up

echo ""
echo "Application stopped."
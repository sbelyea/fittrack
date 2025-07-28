#!/bin/bash

echo "================================="
echo "   Stopping FitTrack Docker"
echo "================================="
echo ""

echo "Stopping all FitTrack containers..."
docker-compose down

echo ""
echo "All containers stopped successfully!"
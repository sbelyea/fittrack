#!/bin/bash

echo "Setting up FitTrack application..."

echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template. Please edit it with your database credentials."
else
    echo ".env file already exists."
fi

echo ""
echo "Setting up database..."
python database_setup.py

echo ""
echo "Setup complete! To start the application, run: python run.py"
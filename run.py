#!/usr/bin/env python3
"""
FitTrack Application Runner
This script starts the Flask development server
"""

from app import app

if __name__ == '__main__':
    print("Starting FitTrack application...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
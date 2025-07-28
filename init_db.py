#!/usr/bin/env python3
"""
Database initialization script for FitTrack
This script ensures the database tables are created before the Flask app starts
"""

import os
import sys
import time
from app import app, db

def wait_for_db():
    """Wait for database to be ready"""
    max_retries = 30
    retry_count = 0
    
    print("Waiting for database to be ready...")
    
    while retry_count < max_retries:
        try:
            with app.app_context():
                with db.engine.connect() as conn:
                    conn.execute(db.text('SELECT 1'))
                print("Database is ready!")
                return True
        except Exception as e:
            retry_count += 1
            print(f"Database not ready yet (attempt {retry_count}/{max_retries}): {e}")
            time.sleep(2)
    
    print("Database failed to become ready after maximum retries")
    return False

def create_tables():
    """Create all database tables"""
    try:
        with app.app_context():
            # Check if tables exist and drop them if they do (for development)
            # This ensures we always have the latest schema
            print("Checking existing tables...")
            
            # Drop all tables first to ensure clean schema
            db.drop_all()
            print("Dropped existing tables")
            
            # Create all tables with current schema
            db.create_all()
            print("Database tables created successfully with updated schema!")
            return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("Initializing FitTrack database...")
    
    if wait_for_db():
        if create_tables():
            print("Database initialization completed successfully!")
            sys.exit(0)
        else:
            print("Failed to create database tables")
            sys.exit(1)
    else:
        print("Failed to connect to database")
        sys.exit(1)
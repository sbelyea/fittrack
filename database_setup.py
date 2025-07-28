#!/usr/bin/env python3
"""
Database setup script for FitTrack
This script creates the MySQL database and tables required for the application.
"""

import os
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """Create the MySQL database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', '')
        )
        
        cursor = connection.cursor()
        
        # Create database
        database_name = os.getenv('MYSQL_DATABASE', 'fittrack')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' created successfully (or already exists)")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    
    return True

def setup_tables():
    """Set up database tables using Flask-SQLAlchemy"""
    from app import app, db
    
    try:
        with app.app_context():
            # Check if tables already exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print(f"Found existing tables: {existing_tables}")
            
            if existing_tables:
                response = input("Tables already exist. Do you want to recreate them? This will DELETE ALL DATA! (y/N): ")
                if response.lower() != 'y':
                    print("Skipping table creation. Using existing tables.")
                    return True
                
                print("Dropping existing tables...")
                db.drop_all()
            
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            print("Database tables created successfully")
            return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("Setting up FitTrack database...")
    
    if create_database():
        if setup_tables():
            print("Database setup completed successfully!")
        else:
            print("Failed to create tables")
    else:
        print("Failed to create database")
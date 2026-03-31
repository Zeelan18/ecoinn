"""
Database initialization and management module
"""

import sqlite3
import os
from datetime import datetime
import datetime as dt

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'db.sqlite3')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with tables"""
    
    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create energy_usage table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS energy_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source TEXT NOT NULL,
            amount REAL NOT NULL,
            mode TEXT DEFAULT 'Urban',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Create alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            alert_type TEXT NOT NULL,
            message TEXT NOT NULL,
            severity TEXT DEFAULT 'info',
            read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Create daily_reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            total_energy REAL NOT NULL,
            total_cost REAL NOT NULL,
            total_savings REAL NOT NULL,
            solar_usage REAL DEFAULT 0,
            battery_usage REAL DEFAULT 0,
            grid_usage REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, date)
        )
    ''')
    
    # Create system_config table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            solar_max REAL DEFAULT 8000,
            battery_capacity REAL DEFAULT 10000,
            battery_min_threshold REAL DEFAULT 0.2,
            grid_cost_per_kwh REAL DEFAULT 0.12,
            outage_simulated BOOLEAN DEFAULT FALSE,
            mode TEXT DEFAULT 'Urban',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Create predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            hour INTEGER NOT NULL,
            predicted_demand REAL NOT NULL,
            confidence REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_energy_usage_user_id 
        ON energy_usage(user_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_energy_usage_timestamp 
        ON energy_usage(timestamp)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_alerts_user_id 
        ON alerts(user_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_predictions_user_id 
        ON predictions(user_id)
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"✓ Database initialized at {DATABASE_PATH}")
    
    # Add demo user automatically
    add_demo_user()

def add_demo_user():
    """Add a demo user for testing"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    from werkzeug.security import generate_password_hash
    
    try:
        # Check if demo user exists
        cursor.execute('SELECT id FROM users WHERE username = ?', ('demo',))
        if cursor.fetchone():
            return
        
        password_hash = generate_password_hash('demo123')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', ('demo', 'demo@ecovolt.ai', password_hash))
        
        conn.commit()
        print("✓ Demo user added (username: demo, password: demo123)")
    except Exception as e:
        print(f"✗ Error adding demo user: {e}")
    finally:
        conn.close()

def reset_database():
    """Reset database (delete and recreate)"""
    if os.path.exists(DATABASE_PATH):
        try:
            os.remove(DATABASE_PATH)
            print(f"✓ Deleted {DATABASE_PATH}")
        except Exception as e:
            print(f"✗ Error deleting database: {e}")
    
    init_database()
    add_demo_user()

if __name__ == '__main__':
    init_database()
    add_demo_user()
    print("Database setup complete!")

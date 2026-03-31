#!/usr/bin/env python3
"""
EcoVolt AI - Smart Microgrid System
Production-ready web application for energy optimization
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import json
from datetime import datetime, timedelta
import hashlib
import secrets
from functools import wraps
from ai_optimizer import EnergyOptimizer
from db_init import init_database, get_db_connection
import math

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Initialize database
init_database()

# Initialize AI Optimizer
optimizer = EnergyOptimizer()

# ==================== HELPER FUNCTIONS ====================

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current logged-in user"""
    if 'user_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email FROM users WHERE id = ?', (session['user_id'],))
        user = cursor.fetchone()
        conn.close()
        return user
    return None

def record_energy_usage(user_id, source, amount, mode='Urban'):
    """Record energy usage in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO energy_usage (user_id, source, amount, mode, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, source, amount, mode, datetime.now()))
    conn.commit()
    conn.close()

def get_user_history(user_id, hours=24):
    """Get user's energy usage history"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cutoff_time = datetime.now() - timedelta(hours=hours)
    cursor.execute('''
        SELECT timestamp, source, amount, mode FROM energy_usage 
        WHERE user_id = ? AND timestamp > ?
        ORDER BY timestamp DESC
    ''', (user_id, cutoff_time.isoformat()))
    history = cursor.fetchall()
    conn.close()
    return history

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Redirect to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return render_template('login.html', error='Username and password required'), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials'), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not all([username, email, password, confirm_password]):
            return render_template('login.html', show_register=True, error='All fields required'), 400
        
        if password != confirm_password:
            return render_template('login.html', show_register=True, error='Passwords do not match'), 400
        
        if len(password) < 6:
            return render_template('login.html', show_register=True, error='Password must be at least 6 characters'), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return render_template('login.html', show_register=True, error='User already exists'), 400
        
        # Create new user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        conn.commit()
        
        # Get user ID and log them in
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]
        conn.close()
        
        session['user_id'] = user_id
        session['username'] = username
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', show_register=True)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

# ==================== MAIN DASHBOARD ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    user = get_current_user()
    return render_template('dashboard.html', username=user[1] if user else 'User')

# ==================== API ENDPOINTS ====================

@app.route('/api/energy-data', methods=['GET'])
@login_required
def get_energy_data():
    """Get simulated real-time energy data"""
    user = get_current_user()
    user_id = user[0]
    mode = request.args.get('mode', 'Urban')
    
    # Get current hour for realistic solar generation
    hour = datetime.now().hour
    
    # Solar generation (peak at noon, 0 at night)
    solar_factor = max(0, math.sin((hour - 6) * math.pi / 12)) if 6 <= hour <= 18 else 0
    solar_power = int(solar_factor * 5000) + (10 if mode == 'Rural' else 50)
    
    # Battery status simulation
    import random
    battery_capacity = 10000
    battery_current = random.randint(2000, 9000)
    battery_percent = (battery_current / battery_capacity) * 100
    
    # Energy demand based on mode and time
    if mode == 'Urban':
        base_demand = random.randint(1000, 3000)
    else:  # Rural
        base_demand = random.randint(300, 1000)
    
    # Add peak hour multiplier
    if 18 <= hour <= 21:  # Evening peak
        base_demand = int(base_demand * 1.5)
    elif 6 <= hour < 9:  # Morning peak
        base_demand = int(base_demand * 1.3)
    
    # Grid availability (simulated)
    grid_available = True
    grid_power = 5000 if grid_available else 0
    
    data = {
        'timestamp': datetime.now().isoformat(),
        'mode': mode,
        'solar': {
            'current': solar_power,
            'max': 8000,
            'efficiency': 85
        },
        'battery': {
            'current': battery_current,
            'capacity': battery_capacity,
            'percent': round(battery_percent, 2),
            'charging': random.choice([True, False])
        },
        'grid': {
            'available': grid_available,
            'power': grid_power,
            'status': 'Connected' if grid_available else 'Disconnected'
        },
        'demand': {
            'current': base_demand,
            'estimated': base_demand
        },
        'cost_per_kwh': 0.12 if mode == 'Urban' else 0.15
    }
    
    return jsonify(data)

@app.route('/api/optimize', methods=['POST'])
@login_required
def optimize_energy():
    """Get AI optimization decision"""
    user = get_current_user()
    user_id = user[0]
    data = request.get_json()
    
    solar = float(data.get('solar', 0))
    battery_current = float(data.get('battery_current', 0))
    battery_capacity = float(data.get('battery_capacity', 10000))
    grid_available = data.get('grid_available', True)
    demand = float(data.get('demand', 0))
    mode = data.get('mode', 'Urban')
    outage_simulated = data.get('outage_simulated', False)
    
    # Get historical data for prediction
    history = get_user_history(user_id, hours=168)  # 1 week
    
    # Call AI optimizer
    decision = optimizer.optimize(
        solar=solar,
        battery_current=battery_current,
        battery_capacity=battery_capacity,
        grid_available=grid_available and not outage_simulated,
        demand=demand,
        mode=mode,
        history=history
    )
    
    # Record the usage
    record_energy_usage(user_id, decision['source'], demand, mode)
    
    return jsonify({
        'source': decision['source'],
        'efficiency': decision['efficiency'],
        'cost': decision['cost'],
        'savings': decision['savings'],
        'recommendation': decision['recommendation'],
        'alert': decision.get('alert', None)
    })

@app.route('/api/daily-report', methods=['GET'])
@login_required
def daily_report():
    """Get daily energy report"""
    user = get_current_user()
    user_id = user[0]
    
    history = get_user_history(user_id, hours=24)
    
    # Calculate statistics
    total_energy = sum(float(h[2]) for h in history)
    
    source_stats = {}
    for h in history:
        source = h[1]
        amount = float(h[2])
        if source not in source_stats:
            source_stats[source] = 0
        source_stats[source] += amount
    
    # Calculate savings
    total_cost = sum(float(h[2]) * 0.12 for h in history if h[1] == 'Grid')
    solar_saved = sum(float(h[2]) * 0.12 for h in history if h[1] == 'Solar')
    battery_saved = sum(float(h[2]) * 0.08 for h in history if h[1] == 'Battery')
    
    total_savings = solar_saved + battery_saved
    
    return jsonify({
        'total_energy': round(total_energy, 2),
        'total_cost': round(total_cost, 2),
        'total_savings': round(total_savings, 2),
        'source_distribution': source_stats,
        'records_count': len(history),
        'average_demand': round(total_energy / len(history) if history else 0, 2)
    })

@app.route('/api/tips', methods=['GET'])
def get_tips():
    """Get energy saving tips"""
    tips = [
        "Use solar energy during peak hours (10 AM - 4 PM)",
        "Charge battery when solar generation is high",
        "Shift heavy loads to off-peak hours",
        "Maintain battery health by avoiding full discharge",
        "Monitor real-time usage to identify peaks",
        "Set devices to sleep mode when not in use",
        "Use natural ventilation during cool hours",
        "Optimize HVAC scheduling based on weather",
        "Regular maintenance improves energy efficiency",
        "Consider time-of-use pricing for better savings"
    ]
    return jsonify({'tips': tips})

@app.route('/api/predictions', methods=['GET'])
@login_required
def get_predictions():
    """Get AI predictions for next 24 hours"""
    user = get_current_user()
    user_id = user[0]
    
    history = get_user_history(user_id, hours=168)
    predictions = optimizer.predict_usage(history, hours=24)
    
    return jsonify({
        'next_24h': predictions,
        'confidence': 0.85
    })

@app.route('/api/health-check', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return jsonify({'error': 'Forbidden'}), 403

# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 60)
    print("EcoVolt AI - Smart Microgrid System")
    print("=" * 60)
    print("Starting Flask application...")
    print("Access the application at: http://localhost:5000")
    print("=" * 60)
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

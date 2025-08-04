"""
BOTZZZ Admin Panel - Flask Web Application
A comprehensive admin interface for managing bot simulations and analytics
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import sqlite3
from datetime import datetime, timedelta
import secrets
import subprocess
import threading
from functools import wraps
import hashlib

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Enhanced user class with registration fields
class User(UserMixin):
    def __init__(self, user_id, username, password_hash, role='user', email=None, service_type=None, created_at=None):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.email = email
        self.service_type = service_type
        self.created_at = created_at or datetime.now().isoformat()

    @property
    def is_active(self):
        return True

# Simulated user database (in production, use proper database)
ADMIN_USERS = {
    'admin': User('1', 'admin', generate_password_hash('BOTZZZ2025!'), 'super_admin', 'admin@botzzz.com'),
    'operator': User('2', 'operator', generate_password_hash('operator123'), 'operator', 'operator@botzzz.com'),
    'viewer': User('3', 'viewer', generate_password_hash('viewer123'), 'viewer', 'viewer@botzzz.com')
}

# Regular user database
USERS = {}

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID from both admin and regular user databases."""
    # Check admin users first
    for user in ADMIN_USERS.values():
        if user.id == user_id:
            return user
    # Check regular users
    for user in USERS.values():
        if user.id == user_id:
            return user
    return None

def role_required(required_role):
    """Decorator to require specific user roles"""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            role_hierarchy = {'viewer': 1, 'operator': 2, 'super_admin': 3}
            user_level = role_hierarchy.get(current_user.role, 0)
            required_level = role_hierarchy.get(required_role, 999)
            
            if user_level < required_level:
                flash('Access denied. Insufficient privileges.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Database initialization
def init_database():
    """Initialize SQLite database for admin panel"""
    conn = sqlite3.connect('botzzz_admin.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulation_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            parameters TEXT,
            results TEXT,
            log_file TEXT,
            created_by TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            component TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_detection_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            bot_id TEXT,
            video_id TEXT,
            risk_score REAL,
            detection_method TEXT,
            confidence_score REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            simulation_run_id INTEGER,
            FOREIGN KEY (simulation_run_id) REFERENCES simulation_runs (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cache_key TEXT UNIQUE NOT NULL,
            data TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def log_system_event(level, message, component='system', user_id=None):
    """Log system events to database"""
    conn = sqlite3.connect('botzzz_admin.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO system_logs (level, message, component, user_id)
        VALUES (?, ?, ?, ?)
    ''', (level, message, component, user_id))
    conn.commit()
    conn.close()

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = ADMIN_USERS.get(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            log_system_event('INFO', f'User {username} logged in successfully', 'auth', user.id)
            flash(f'Welcome to BOTZZZ Admin Panel, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            log_system_event('WARNING', f'Failed login attempt for username: {username}', 'auth')
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    log_system_event('INFO', f'User {current_user.username} logged out', 'auth', current_user.id)
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        service_type = request.form['service_type']
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Check if username already exists
        if username in USERS or username in ADMIN_USERS:
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        user_id = str(len(USERS) + len(ADMIN_USERS) + 10)  # Simple ID generation
        new_user = User(user_id, username, generate_password_hash(password), 'user', email, service_type)
        USERS[username] = new_user
        
        log_system_event('INFO', f'New user registered: {username}', 'auth')
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('user_login'))
    
    return render_template('register.html')

@app.route('/user-login', methods=['GET', 'POST'])
def user_login():
    """User login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember_me' in request.form
        
        user = USERS.get(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            log_system_event('INFO', f'User {username} logged in', 'auth', user.id)
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            log_system_event('WARNING', f'Failed user login attempt for username: {username}', 'auth')
            flash('Invalid username or password', 'error')
    
    return render_template('user_login.html')

@app.route('/user-dashboard')
@login_required
def user_dashboard():
    """User dashboard - only for regular users."""
    if current_user.role in ['super_admin', 'admin', 'operator', 'viewer']:
        # Redirect admin users to admin dashboard
        return redirect(url_for('dashboard'))
    return render_template('user_dashboard.html')

# Routes
@app.route('/')
def home():
    """Public index page showcasing BOTZZZ services."""
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard with real-time analytics."""
    # Get recent simulation runs
    conn = sqlite3.connect('botzzz_admin.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) as total,
               SUM(CASE WHEN status = 'running' THEN 1 ELSE 0 END) as running,
               SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
               SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed
        FROM simulation_runs
    ''')
    simulation_stats = cursor.fetchone()
    
    cursor.execute('''
        SELECT name, type, status, created_at, completed_at
        FROM simulation_runs
        ORDER BY created_at DESC
        LIMIT 5
    ''')
    recent_simulations = cursor.fetchall()
    
    cursor.execute('''
        SELECT level, COUNT(*) as count
        FROM system_logs
        WHERE timestamp > datetime('now', '-24 hours')
        GROUP BY level
    ''')
    log_stats = cursor.fetchall()
    
    conn.close()
    
    # System metrics
    system_metrics = {
        'cpu_usage': '45%',  # In production, get actual metrics
        'memory_usage': '62%',
        'disk_usage': '38%',
        'active_connections': 23,
        'uptime': '5 days, 12 hours'
    }
    
    return render_template('dashboard.html',
                         simulation_stats=simulation_stats,
                         recent_simulations=recent_simulations,
                         log_stats=log_stats,
                         system_metrics=system_metrics)

@app.route('/simulations')
@login_required
def simulations():
    """Simulation management page"""
    conn = sqlite3.connect('botzzz_admin.db')
    cursor = conn.cursor()
    
    # Get all simulations with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    cursor.execute('''
        SELECT id, name, type, status, created_at, started_at, completed_at, created_by
        FROM simulation_runs
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    simulations = cursor.fetchall()
    
    cursor.execute('SELECT COUNT(*) FROM simulation_runs')
    total_count = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('simulations.html',
                         simulations=simulations,
                         page=page,
                         per_page=per_page,
                         total_count=total_count)

@app.route('/simulations/create', methods=['GET', 'POST'])
@role_required('operator')
def create_simulation():
    """Create new simulation"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Validate simulation parameters
        simulation_name = data.get('name', '')
        simulation_type = data.get('type', 'youtube')
        parameters = data.get('parameters', {})
        
        if not simulation_name:
            return jsonify({'error': 'Simulation name is required'}), 400
        
        # Save to database
        conn = sqlite3.connect('botzzz_admin.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO simulation_runs (name, type, status, parameters, created_by)
            VALUES (?, ?, 'pending', ?, ?)
        ''', (simulation_name, simulation_type, json.dumps(parameters), current_user.username))
        
        simulation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_system_event('INFO', f'New simulation created: {simulation_name}', 'simulation', current_user.id)
        
        return jsonify({'success': True, 'simulation_id': simulation_id})
    
    return render_template('create_simulation.html')

@app.route('/simulations/<int:simulation_id>/start', methods=['POST'])
@role_required('operator')
def start_simulation(simulation_id):
    """Start a simulation"""
    conn = sqlite3.connect('botzzz_admin.db')
    cursor = conn.cursor()
    
    # Get simulation details
    cursor.execute('SELECT name, type, parameters FROM simulation_runs WHERE id = ?', (simulation_id,))
    simulation = cursor.fetchone()
    
    if not simulation:
        return jsonify({'error': 'Simulation not found'}), 404
    
    # Update status to running
    cursor.execute('''
        UPDATE simulation_runs 
        SET status = 'running', started_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (simulation_id,))
    
    conn.commit()
    conn.close()
    
    # Start simulation in background thread
    def run_simulation():
        try:
            simulation_name, sim_type, parameters = simulation
            log_file = f"simulation_{simulation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            
            # Execute simulation script
            if sim_type == 'youtube':
                script_path = '../simulation/simulate_engagement_youtube_realistic.py'
            elif sim_type == 'instagram':
                script_path = '../simulation/simulate_engagement_instagram.py'
            elif sim_type == 'tiktok':
                script_path = '../simulation/simulate_engagement_tiktok_influencer.py'
            else:
                script_path = '../simulation/simulate_engagement.py'
            
            # Run simulation script
            with open(log_file, 'w') as f:
                process = subprocess.run(
                    ['python', script_path],
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    cwd=os.path.dirname(os.path.abspath(__file__))
                )
            
            # Update simulation status
            conn = sqlite3.connect('botzzz_admin.db')
            cursor = conn.cursor()
            
            status = 'completed' if process.returncode == 0 else 'failed'
            cursor.execute('''
                UPDATE simulation_runs 
                SET status = ?, completed_at = CURRENT_TIMESTAMP, log_file = ?
                WHERE id = ?
            ''', (status, log_file, simulation_id))
            
            conn.commit()
            conn.close()
            
            log_system_event('INFO', f'Simulation {simulation_name} {status}', 'simulation', current_user.id)
            
        except Exception as e:
            # Mark as failed
            conn = sqlite3.connect('botzzz_admin.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE simulation_runs 
                SET status = 'failed', completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (simulation_id,))
            conn.commit()
            conn.close()
            
            log_system_event('ERROR', f'Simulation {simulation_name} failed: {str(e)}', 'simulation', current_user.id)
    
    # Start simulation in background
    thread = threading.Thread(target=run_simulation)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': 'Simulation started'})

@app.route('/analytics')
@login_required
def analytics():
    """Analytics dashboard"""
    # Load recent simulation data for analytics
    try:
        # Try to load the most recent simulation data
        data_files = [
            '../data/youtube_realistic_simulation.json',
            '../data/youtube_engagement_log_realistic.json'
        ]
        
        analytics_data = {}
        for file_path in data_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    analytics_data[os.path.basename(file_path)] = data
        
        # Process analytics
        engagement_metrics = {}
        if 'youtube_engagement_log_realistic.json' in analytics_data:
            log_data = analytics_data['youtube_engagement_log_realistic.json']
            
            # Calculate metrics
            total_events = len(log_data)
            real_user_events = len([e for e in log_data if e.get('user_type') == 'real'])
            bot_events = len([e for e in log_data if e.get('user_type') == 'bot'])
            
            engagement_metrics = {
                'total_events': total_events,
                'real_user_events': real_user_events,
                'bot_events': bot_events,
                'bot_percentage': (bot_events / total_events * 100) if total_events > 0 else 0,
                'high_risk_events': len([e for e in log_data if e.get('detection_risk_score', 0) > 0.7])
            }
    
    except Exception as e:
        analytics_data = {}
        engagement_metrics = {}
        log_system_event('WARNING', f'Analytics data loading failed: {str(e)}', 'analytics', current_user.id)
    
    return render_template('analytics.html',
                         analytics_data=analytics_data,
                         engagement_metrics=engagement_metrics)

@app.route('/detection')
@login_required
def detection():
    """Bot detection dashboard"""
    conn = sqlite3.connect('botzzz_admin.db')
    cursor = conn.cursor()
    
    # Get detection events
    cursor.execute('''
        SELECT event_type, bot_id, video_id, risk_score, detection_method, 
               confidence_score, timestamp
        FROM bot_detection_events
        ORDER BY timestamp DESC
        LIMIT 100
    ''')
    detection_events = cursor.fetchall()
    
    # Get detection statistics
    cursor.execute('''
        SELECT detection_method, COUNT(*) as count, AVG(confidence_score) as avg_confidence
        FROM bot_detection_events
        WHERE timestamp > datetime('now', '-24 hours')
        GROUP BY detection_method
    ''')
    detection_stats = cursor.fetchall()
    
    conn.close()
    
    return render_template('detection.html',
                         detection_events=detection_events,
                         detection_stats=detection_stats)

@app.route('/logs')
@login_required
def logs():
    """System logs viewer"""
    conn = sqlite3.connect('botzzz_admin.db')
    cursor = conn.cursor()
    
    # Get logs with filtering
    level_filter = request.args.get('level', '')
    component_filter = request.args.get('component', '')
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page
    
    query = 'SELECT level, message, component, timestamp, user_id FROM system_logs WHERE 1=1'
    params = []
    
    if level_filter:
        query += ' AND level = ?'
        params.append(level_filter)
    
    if component_filter:
        query += ' AND component = ?'
        params.append(component_filter)
    
    query += ' ORDER BY timestamp DESC LIMIT ? OFFSET ?'
    params.extend([per_page, offset])
    
    cursor.execute(query, params)
    logs = cursor.fetchall()
    
    # Get total count for pagination
    count_query = 'SELECT COUNT(*) FROM system_logs WHERE 1=1'
    count_params = []
    
    if level_filter:
        count_query += ' AND level = ?'
        count_params.append(level_filter)
    
    if component_filter:
        count_query += ' AND component = ?'
        count_params.append(component_filter)
    
    cursor.execute(count_query, count_params)
    total_count = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('logs.html',
                         logs=logs,
                         page=page,
                         per_page=per_page,
                         total_count=total_count,
                         level_filter=level_filter,
                         component_filter=component_filter)

@app.route('/settings')
@role_required('super_admin')
def settings():
    """Admin settings page"""
    return render_template('settings.html')

@app.route('/api/system-status')
@login_required
def api_system_status():
    """API endpoint for system status"""
    status = {
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy',
        'version': '1.0.0',
        'uptime': '5 days, 12 hours',
        'active_simulations': 2,
        'cpu_usage': 45.2,
        'memory_usage': 62.1,
        'disk_usage': 38.5
    }
    return jsonify(status)

@app.route('/api/simulations/<int:simulation_id>/logs')
@login_required
def api_simulation_logs(simulation_id):
    """API endpoint to get simulation logs"""
    conn = sqlite3.connect('botzzz_admin.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT log_file FROM simulation_runs WHERE id = ?', (simulation_id,))
    result = cursor.fetchone()
    
    if not result or not result[0]:
        return jsonify({'error': 'Log file not found'}), 404
    
    log_file = result[0]
    
    try:
        with open(log_file, 'r') as f:
            logs = f.read()
        return jsonify({'logs': logs})
    except FileNotFoundError:
        return jsonify({'error': 'Log file not accessible'}), 404

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, error_message='Page not found'), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html', error_code=403, error_message='Access forbidden'), 403

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message='Internal server error'), 500

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Log system startup
    log_system_event('INFO', 'BOTZZZ Admin Panel started', 'system')
    
    print("BOTZZZ Admin Panel Starting...")
    print("Default credentials:")
    print("  Admin: admin / BOTZZZ2025!")
    print("  Operator: operator / operator123")
    print("  Viewer: viewer / viewer123")
    print("\nAccess the panel at: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

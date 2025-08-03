#!/bin/bash

# BOTZZZ Admin Panel Installation Script
# This script sets up the BOTZZZ admin panel with all dependencies

echo "🚀 BOTZZZ Admin Panel Installation"
echo "=================================="

# Check Python version
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ Python detected: $python_version"
else
    echo "❌ Python 3 is required but not installed"
    echo "Please install Python 3.8 or higher and try again"
    exit 1
fi

# Check if pip is available
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 is available"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo "✅ pip is available"
    PIP_CMD="pip"
else
    echo "❌ pip is not available"
    echo "Please install pip and try again"
    exit 1
fi

# Create virtual environment (optional but recommended)
read -p "Do you want to create a virtual environment? (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
$PIP_CMD install -r requirements.txt

if [[ $? -eq 0 ]]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images
mkdir -p logs
mkdir -p data
echo "✅ Directories created"

# Set permissions
echo "🔐 Setting permissions..."
chmod +x app.py
chmod 755 static
chmod 755 templates
echo "✅ Permissions set"

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "
import sqlite3
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
print('Database initialized successfully')
"

if [[ $? -eq 0 ]]; then
    echo "✅ Database initialized"
else
    echo "❌ Database initialization failed"
    exit 1
fi

# Create environment file
echo "📝 Creating environment configuration..."
cat > .env << EOF
# BOTZZZ Admin Panel Environment Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
DATABASE_URL=sqlite:///botzzz_admin.db
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=5
EOF
echo "✅ Environment file created"

# Create startup script
echo "📝 Creating startup script..."
cat > start.sh << 'EOF'
#!/bin/bash
echo "Starting BOTZZZ Admin Panel..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Start the Flask application
python3 app.py
EOF

chmod +x start.sh
echo "✅ Startup script created"

# Create systemd service file (for production)
echo "📝 Creating systemd service file..."
cat > botzzz-admin.service << EOF
[Unit]
Description=BOTZZZ Admin Panel
After=network.target

[Service]
Type=exec
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
echo "✅ Systemd service file created (botzzz-admin.service)"

# Create Docker configuration
echo "📝 Creating Docker configuration..."
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p static/css static/js static/images logs data

# Set permissions
RUN chmod +x app.py

# Initialize database
RUN python -c "exec(open('init_db.py').read())" 2>/dev/null || true

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False

# Start application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
EOF

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  botzzz-admin:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./botzzz_admin.db:/app/botzzz_admin.db
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - botzzz-admin
    restart: unless-stopped
EOF

cat > .dockerignore << 'EOF'
venv/
__pycache__/
*.pyc
.env
.git/
*.log
node_modules/
EOF

echo "✅ Docker configuration created"

# Installation complete
echo ""
echo "🎉 BOTZZZ Admin Panel Installation Complete!"
echo "============================================="
echo ""
echo "📋 What's been installed:"
echo "  ✅ Python dependencies"
echo "  ✅ Database schema"
echo "  ✅ Directory structure"
echo "  ✅ Environment configuration"
echo "  ✅ Startup scripts"
echo "  ✅ Docker configuration"
echo "  ✅ Systemd service file"
echo ""
echo "🚀 Quick Start:"
echo "  1. Start the application: ./start.sh"
echo "  2. Open browser: http://localhost:5000"
echo "  3. Login with: admin / BOTZZZ2025!"
echo ""
echo "🐳 Docker Start:"
echo "  docker-compose up -d"
echo ""
echo "🔧 Production Setup:"
echo "  sudo cp botzzz-admin.service /etc/systemd/system/"
echo "  sudo systemctl enable botzzz-admin"
echo "  sudo systemctl start botzzz-admin"
echo ""
echo "📖 Documentation: https://github.com/omer3kale/BOTZZZ"
echo ""
echo "Default Admin Credentials:"
echo "  Username: admin"
echo "  Password: BOTZZZ2025!"
echo ""
echo "Happy bot simulating! 🤖"

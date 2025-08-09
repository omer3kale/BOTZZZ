#!/usr/bin/env python3
"""
BOTZZZ Production WSGI Configuration
Enterprise-grade production server configuration with bulletproof systems
"""

import os
import sys
from werkzeug.middleware.proxy_fix import ProxyFix

# Add the admin_panel directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

# Configure for production with proxy support
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Production configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', app.secret_key),
    DEBUG=False,
    TESTING=False,
    ENV='production'
)

if __name__ == "__main__":
    # For production, use a proper WSGI server like Gunicorn
    # gunicorn --bind 0.0.0.0:5001 --workers 4 --worker-class sync wsgi:app
    app.run(host='0.0.0.0', port=5001)

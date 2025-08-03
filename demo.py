#!/usr/bin/env python3
"""
BOTZZZ Admin Panel Demo Script
Demonstrates the key features and capabilities of the admin panel
"""

import os
import sys
import time
import json
import requests
from datetime import datetime

# Add the admin panel directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'admin_panel'))

def print_banner():
    """Print the BOTZZZ demo banner"""
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║              🤖 BOTZZZ ADMIN PANEL DEMO 🤖           ║
    ║                                                      ║
    ║     Professional Bot Simulation Management           ║
    ║     Multi-Platform Analytics & Detection             ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)

def check_admin_panel_status():
    """Check if the admin panel is running"""
    try:
        response = requests.get('http://localhost:5000/api/system-status', timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except requests.exceptions.RequestException:
        return False, None

def demo_simulation_creation():
    """Demonstrate simulation creation via API"""
    print("\n🚀 SIMULATION CREATION DEMO")
    print("=" * 50)
    
    simulation_configs = [
        {
            "name": "YouTube View Farm Analysis",
            "type": "youtube",
            "parameters": {
                "num_creators": 10,
                "num_real_users": 500,
                "num_bots": 50,
                "simulation_steps": 100,
                "bot_types": ["view_farm", "subscriber_farm"],
                "advanced_options": ["network_forensics", "behavioral_analysis"]
            }
        },
        {
            "name": "Instagram Engagement Pod Study",
            "type": "instagram", 
            "parameters": {
                "num_creators": 8,
                "num_real_users": 300,
                "num_bots": 40,
                "simulation_steps": 75,
                "bot_types": ["engagement_pod", "sophisticated_bot"],
                "advanced_options": ["economic_modeling", "real_time_detection"]
            }
        },
        {
            "name": "TikTok Viral Manipulation Analysis",
            "type": "tiktok",
            "parameters": {
                "num_creators": 15,
                "num_real_users": 1000,
                "num_bots": 100,
                "simulation_steps": 200,
                "bot_types": ["view_farm", "engagement_pod", "sophisticated_bot"],
                "advanced_options": ["network_forensics", "behavioral_analysis", "economic_modeling"]
            }
        }
    ]
    
    for i, config in enumerate(simulation_configs, 1):
        print(f"\n📋 Demo Simulation {i}: {config['name']}")
        print(f"   Platform: {config['type'].title()}")
        print(f"   Users: {config['parameters']['num_real_users']:,}")
        print(f"   Bots: {config['parameters']['num_bots']:,}")
        print(f"   Duration: {config['parameters']['simulation_steps']} steps (~{config['parameters']['simulation_steps'] * 10} minutes)")
        print(f"   Bot Types: {', '.join(config['parameters']['bot_types'])}")
        print(f"   Advanced Features: {', '.join(config['parameters']['advanced_options'])}")

def demo_analytics_capabilities():
    """Demonstrate analytics and detection capabilities"""
    print("\n📊 ANALYTICS & DETECTION DEMO")
    print("=" * 50)
    
    analytics_features = {
        "Real-time Metrics": [
            "Live system performance monitoring",
            "Active simulation tracking",
            "Resource usage analytics",
            "User activity monitoring"
        ],
        "Bot Detection": [
            "Network forensics analysis",
            "Behavioral pattern recognition", 
            "Device fingerprint analysis",
            "Coordination detection",
            "Risk scoring algorithms"
        ],
        "Economic Impact": [
            "Revenue pollution calculations",
            "Ad fraud impact assessment",
            "Creator income analysis",
            "Platform cost evaluation"
        ],
        "Advanced Analytics": [
            "Cross-platform correlation",
            "Temporal pattern analysis",
            "Geographical distribution",
            "Engagement authenticity scoring"
        ]
    }
    
    for category, features in analytics_features.items():
        print(f"\n🎯 {category}:")
        for feature in features:
            print(f"   ✅ {feature}")

def demo_security_features():
    """Demonstrate security and access control features"""
    print("\n🛡️ SECURITY & ACCESS CONTROL DEMO")
    print("=" * 50)
    
    security_features = {
        "Authentication": [
            "Multi-user support with secure login",
            "Password hashing with Werkzeug",
            "Session management with Flask-Login",
            "Failed login attempt tracking"
        ],
        "Authorization": [
            "Role-based access control (Super Admin, Operator, Viewer)",
            "Granular permission system",
            "Route-level access restrictions",
            "Activity-based access validation"
        ],
        "Audit & Logging": [
            "Comprehensive activity logging",
            "User action tracking",
            "System event monitoring",
            "Security incident detection"
        ],
        "Data Protection": [
            "Input validation and sanitization",
            "SQL injection prevention",
            "XSS protection",
            "Secure file handling"
        ]
    }
    
    print("\n👥 USER ROLES & PERMISSIONS:")
    roles = {
        "Super Admin": ["Full system access", "User management", "System configuration", "Delete operations"],
        "Operator": ["Create simulations", "Start/stop processes", "View analytics", "Monitor logs"],
        "Viewer": ["Read-only access", "Dashboard viewing", "Report generation", "Status monitoring"]
    }
    
    for role, permissions in roles.items():
        print(f"\n🔐 {role}:")
        for permission in permissions:
            print(f"   ✅ {permission}")
    
    print(f"\n🔒 SECURITY FEATURES:")
    for category, features in security_features.items():
        print(f"\n   {category}:")
        for feature in features:
            print(f"     • {feature}")

def demo_deployment_options():
    """Demonstrate deployment and production features"""
    print("\n🚀 DEPLOYMENT & PRODUCTION DEMO")
    print("=" * 50)
    
    deployment_options = {
        "Development": {
            "method": "Direct Python execution",
            "command": "python3 admin_panel/app.py",
            "features": ["Debug mode", "Auto-reload", "Detailed error messages"]
        },
        "Production": {
            "method": "Gunicorn WSGI server",
            "command": "gunicorn -w 4 -b 0.0.0.0:5000 app:app",
            "features": ["Multi-worker", "Load balancing", "Production optimized"]
        },
        "Docker": {
            "method": "Containerized deployment",
            "command": "docker-compose up -d",
            "features": ["Isolated environment", "Easy scaling", "Consistent deployment"]
        },
        "Systemd": {
            "method": "System service",
            "command": "systemctl start botzzz-admin",
            "features": ["Auto-start on boot", "Service management", "Log integration"]
        }
    }
    
    for method, details in deployment_options.items():
        print(f"\n🎯 {method} Deployment:")
        print(f"   Method: {details['method']}")
        print(f"   Command: {details['command']}")
        print(f"   Features:")
        for feature in details['features']:
            print(f"     ✅ {feature}")

def demo_api_endpoints():
    """Demonstrate API capabilities"""
    print("\n🔌 API ENDPOINTS DEMO")
    print("=" * 50)
    
    api_categories = {
        "Authentication": [
            "POST /login - User authentication",
            "GET /logout - User logout"
        ],
        "Dashboard": [
            "GET /dashboard - Main dashboard view",
            "GET /api/system-status - Real-time metrics"
        ],
        "Simulations": [
            "GET /simulations - List all simulations",
            "POST /simulations/create - Create new simulation",
            "POST /simulations/{id}/start - Start simulation",
            "GET /api/simulations/{id}/logs - Get logs"
        ],
        "Analytics": [
            "GET /analytics - Analytics dashboard",
            "GET /detection - Bot detection metrics",
            "GET /logs - System logs viewer"
        ]
    }
    
    for category, endpoints in api_categories.items():
        print(f"\n📡 {category} APIs:")
        for endpoint in endpoints:
            print(f"   {endpoint}")

def show_installation_guide():
    """Show installation and setup guide"""
    print("\n📦 INSTALLATION GUIDE")
    print("=" * 50)
    
    steps = [
        ("1. Clone Repository", "git clone https://github.com/omer3kale/BOTZZZ.git"),
        ("2. Navigate to Directory", "cd BOTZZZ/admin_panel"),
        ("3. Run Installation Script", "./install.sh"),
        ("4. Start Application", "./start.sh"),
        ("5. Open Browser", "http://localhost:5000")
    ]
    
    print("\n🚀 Quick Installation:")
    for step, command in steps:
        print(f"   {step}")
        print(f"   $ {command}\n")
    
    print("🔑 Default Login Credentials:")
    credentials = [
        ("Super Admin", "admin", "BOTZZZ2025!"),
        ("Operator", "operator", "operator123"),
        ("Viewer", "viewer", "viewer123")
    ]
    
    for role, username, password in credentials:
        print(f"   {role}: {username} / {password}")

def main():
    """Main demo function"""
    print_banner()
    
    # Check if admin panel is running
    is_running, status = check_admin_panel_status()
    
    if is_running:
        print("✅ BOTZZZ Admin Panel is running!")
        print(f"   Status: {status.get('status', 'Unknown')}")
        print(f"   Version: {status.get('version', 'Unknown')}")
        print(f"   Uptime: {status.get('uptime', 'Unknown')}")
        print("   Access: http://localhost:5000")
    else:
        print("⚠️  BOTZZZ Admin Panel is not running")
        print("   Start it with: cd admin_panel && python3 app.py")
    
    print("\n" + "=" * 60)
    print("                    DEMONSTRATION MENU")
    print("=" * 60)
    
    demos = [
        ("1", "🚀 Simulation Creation", demo_simulation_creation),
        ("2", "📊 Analytics & Detection", demo_analytics_capabilities),
        ("3", "🛡️ Security Features", demo_security_features),
        ("4", "🚀 Deployment Options", demo_deployment_options),
        ("5", "🔌 API Endpoints", demo_api_endpoints),
        ("6", "📦 Installation Guide", show_installation_guide),
        ("7", "🌐 Open Admin Panel", lambda: os.system("open http://localhost:5000") if sys.platform == "darwin" else None),
        ("0", "❌ Exit Demo", lambda: sys.exit(0))
    ]
    
    while True:
        print("\nSelect a demo option:")
        for num, title, _ in demos:
            print(f"   {num}. {title}")
        
        try:
            choice = input("\nEnter your choice (0-7): ").strip()
            
            if choice == "7":
                print("\n🌐 Opening BOTZZZ Admin Panel in browser...")
                if sys.platform == "darwin":  # macOS
                    os.system("open http://localhost:5000")
                elif sys.platform == "linux":  # Linux
                    os.system("xdg-open http://localhost:5000")
                elif sys.platform == "win32":  # Windows
                    os.system("start http://localhost:5000")
                else:
                    print("   Manual access: http://localhost:5000")
                continue
            
            demo = next((func for num, _, func in demos if num == choice), None)
            if demo:
                demo()
                input("\nPress Enter to continue...")
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

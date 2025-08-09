#!/usr/bin/env python3
"""
BOTZZZ Test Configuration and Requirements
========================================

Test configuration file for comprehensive testing setup.
"""

# Testing Requirements
testing_requirements = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0", 
    "coverage>=7.2.0",
    "unittest-mock>=1.0.0",
    "factory-boy>=3.3.0",
    "freezegun>=1.2.0",
    "responses>=0.23.0"
]

# Test Configuration
TEST_CONFIG = {
    "coverage_target": 100,
    "test_timeout": 300,  # 5 minutes
    "parallel_tests": True,
    "verbose_output": True,
    "fail_fast": False,
    "generate_html_report": True,
    "test_directories": [
        "admin_panel/",
        "simulation/",
        "analysis/",
        "research/"
    ],
    "exclude_patterns": [
        "*/migrations/*",
        "*/venv/*",
        "*/__pycache__/*",
        "*/htmlcov/*"
    ]
}

# Mock configurations for testing
MOCK_CONFIGS = {
    "supabase": {
        "url": "https://test-project.supabase.co",
        "key": "test-anon-key-12345",
        "service_role_key": "test-service-role-key-12345"
    },
    "database": {
        "test_db_name": "botzzz_test.db",
        "use_memory_db": True,
        "backup_existing": True
    },
    "external_services": {
        "mock_apis": True,
        "mock_payments": True,
        "mock_social_platforms": True
    }
}

def get_test_database_url():
    """Get test database URL"""
    return "sqlite:///:memory:"

def get_mock_supabase_config():
    """Get mock Supabase configuration for testing"""
    return MOCK_CONFIGS["supabase"]

def setup_test_environment():
    """Set up test environment variables"""
    import os
    
    # Set test environment variables
    os.environ['TESTING'] = 'True'
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['DATABASE_URL'] = get_test_database_url()
    
    # Mock external service URLs
    os.environ['SUPABASE_URL'] = MOCK_CONFIGS["supabase"]["url"]
    os.environ['SUPABASE_KEY'] = MOCK_CONFIGS["supabase"]["key"]
    
    return True

if __name__ == "__main__":
    print("🧪 BOTZZZ Test Configuration")
    print("=" * 40)
    print(f"📊 Coverage Target: {TEST_CONFIG['coverage_target']}%")
    print(f"⏱️  Test Timeout: {TEST_CONFIG['test_timeout']}s")
    print(f"🔧 Test Directories: {len(TEST_CONFIG['test_directories'])}")
    print(f"🚫 Exclude Patterns: {len(TEST_CONFIG['exclude_patterns'])}")
    print()
    print("📦 Required Testing Packages:")
    for req in testing_requirements:
        print(f"   • {req}")
    print()
    print("💡 To install testing requirements:")
    print("   pip install pytest pytest-cov coverage")
    print()
    print("🚀 To run comprehensive tests:")
    print("   python test_comprehensive.py")

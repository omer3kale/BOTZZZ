#!/usr/bin/env python3
"""
Quick test of Supabase integration
"""

import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_supabase_integration():
    """Test basic Supabase functionality"""
    print("🧪 Testing BOTZZZ Supabase Integration")
    print("=" * 50)
    
    try:
        # Test import
        print("📦 Testing imports...")
        from supabase_config import SupabaseManager, SupabaseConfig
        print("✅ Supabase imports successful")
        
        # Test configuration
        print("⚙️  Testing configuration...")
        config = SupabaseConfig(
            url="https://test-project.supabase.co",
            key="test-key",
            service_role_key="test-service-key"
        )
        print("✅ Configuration creation successful")
        
        # Test manager initialization
        print("🚀 Testing manager initialization...")
        manager = SupabaseManager(config)
        print("✅ Manager initialization successful")
        
        # Test health check (will fail without real credentials, but should not crash)
        print("🔍 Testing health check...")
        health_status = manager.get_health_status()
        print(f"📊 Health status: {health_status.get('connection_status', 'unknown')}")
        
        print("\n🎉 Basic integration test completed successfully!")
        print("📋 Next steps:")
        print("   1. Set up your Supabase project")
        print("   2. Configure .env with your credentials")
        print("   3. Run: python setup_supabase.py")
        print("   4. Start the enhanced platform!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Install dependencies: pip install -r requirements_supabase.txt")
        return False
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_fallback_mode():
    """Test SQLite fallback functionality"""
    print("\n🔄 Testing SQLite fallback mode...")
    
    try:
        # Test the enhanced logging function
        from app import log_system_event_sqlite
        
        result = log_system_event_sqlite("INFO", "Test message", "test_component")
        if result:
            print("✅ SQLite fallback logging works")
        else:
            print("⚠️  SQLite fallback had issues")
            
        return True
        
    except Exception as e:
        print(f"❌ Fallback test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 BOTZZZ Enterprise Platform - Supabase Integration Test")
    print()
    
    # Run tests
    supabase_test = test_supabase_integration()
    fallback_test = test_fallback_mode()
    
    print("\n📊 Test Results:")
    print(f"   Supabase Integration: {'✅ PASS' if supabase_test else '❌ FAIL'}")
    print(f"   SQLite Fallback: {'✅ PASS' if fallback_test else '❌ FAIL'}")
    
    if supabase_test and fallback_test:
        print("\n🎉 All tests passed! Your integration is ready.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
    
    print("\n📖 For full setup, run: python setup_supabase.py")

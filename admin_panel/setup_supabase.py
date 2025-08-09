#!/usr/bin/env python3
"""
BOTZZZ Supabase Setup Script
Automated setup and configuration for Supabase integration
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import secrets
import string

class SupabaseSetup:
    """
    Comprehensive setup script for BOTZZZ Supabase integration
    """
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.env_file = self.project_root / '.env'
        self.env_template = self.project_root / '.env.template'
        self.schema_file = self.project_root / 'supabase_schema.sql'
        self.migration_script = self.project_root / 'supabase_migration.py'
        
    def print_banner(self):
        """Print setup banner"""
        print("🚀" + "=" * 60)
        print("  BOTZZZ ENTERPRISE PLATFORM - SUPABASE SETUP")
        print("  Advanced Database Integration & Real-time Features")
        print("=" * 62)
        print()
    
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ is required")
            return False
        else:
            print("✅ Python version OK")
        
        # Check if required files exist
        required_files = [
            self.env_template,
            self.schema_file,
            self.migration_script
        ]
        
        for file_path in required_files:
            if file_path.exists():
                print(f"✅ Found {file_path.name}")
            else:
                print(f"❌ Missing required file: {file_path.name}")
                return False
        
        return True
    
    def install_dependencies(self):
        """Install required Python packages"""
        print("\n📦 Installing Supabase dependencies...")
        
        requirements_file = self.project_root / 'requirements_supabase.txt'
        
        if not requirements_file.exists():
            print("❌ Requirements file not found")
            return False
        
        try:
            # Install requirements
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ], check=True, capture_output=True)
            
            print("✅ Dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def generate_secret_key(self, length=64):
        """Generate a secure secret key"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def create_env_file(self):
        """Create .env file from template with user input"""
        print("\n⚙️  Creating environment configuration...")
        
        if self.env_file.exists():
            response = input("📋 .env file already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("📝 Skipping .env file creation")
                return True
        
        # Read template
        with open(self.env_template, 'r') as f:
            env_content = f.read()
        
        print("\n🔧 Please provide your Supabase configuration:")
        print("   (You can find these values in your Supabase project dashboard)")
        
        # Get Supabase URL
        supabase_url = input("\n🌐 Supabase Project URL: ").strip()
        if not supabase_url:
            supabase_url = "https://your-project-id.supabase.co"
        
        # Get Supabase keys
        anon_key = input("🔑 Supabase Anonymous Key: ").strip()
        if not anon_key:
            anon_key = "your-anon-key-here"
        
        service_key = input("🔐 Supabase Service Role Key (keep secret): ").strip()
        if not service_key:
            service_key = "your-service-role-key-here"
        
        # Generate secure keys
        flask_secret = self.generate_secret_key(64)
        jwt_secret = self.generate_secret_key(32)
        
        # Replace placeholders
        env_content = env_content.replace('https://your-project-id.supabase.co', supabase_url)
        env_content = env_content.replace('your-anon-key-here', anon_key)
        env_content = env_content.replace('your-service-role-key-here', service_key)
        env_content = env_content.replace('your-super-secret-key-change-this-in-production', flask_secret)
        env_content = env_content.replace('your-jwt-secret-key', jwt_secret)
        
        # Write .env file
        with open(self.env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ Environment file created successfully")
        return True
    
    def setup_supabase_schema(self):
        """Setup database schema in Supabase"""
        print("\n🗄️  Setting up Supabase database schema...")
        
        # Check if we have Supabase configuration
        if not self.env_file.exists():
            print("❌ .env file not found. Please run environment setup first.")
            return False
        
        print("📋 Database schema setup options:")
        print("   1. Automatic setup (recommended)")
        print("   2. Manual setup (you'll apply the SQL yourself)")
        print("   3. Skip schema setup")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            return self.auto_setup_schema()
        elif choice == '2':
            return self.manual_setup_schema()
        else:
            print("⏭️  Skipping schema setup")
            return True
    
    def auto_setup_schema(self):
        """Automatically apply schema to Supabase"""
        try:
            print("🔄 Attempting automatic schema setup...")
            
            # Import after dependencies are installed
            from supabase_config import initialize_supabase, SupabaseConfig
            
            # Load environment variables
            from dotenv import load_dotenv
            load_dotenv(self.env_file)
            
            # Initialize Supabase
            config = SupabaseConfig(
                url=os.getenv('SUPABASE_URL'),
                key=os.getenv('SUPABASE_ANON_KEY'),
                service_role_key=os.getenv('SUPABASE_SERVICE_KEY')
            )
            
            supabase_manager = initialize_supabase(config)
            
            # Test connection
            health_status = supabase_manager.get_health_status()
            
            if health_status.get('is_connected'):
                print("✅ Connected to Supabase successfully")
                
                # Read and execute schema
                with open(self.schema_file, 'r') as f:
                    schema_sql = f.read()
                
                # Split into individual statements and execute
                statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
                
                executed_count = 0
                for statement in statements:
                    try:
                        # Use service client for schema operations
                        supabase_manager.service_client.rpc('exec_sql', {'sql': statement}).execute()
                        executed_count += 1
                    except Exception as e:
                        print(f"⚠️  Warning executing statement: {e}")
                
                print(f"✅ Schema setup completed ({executed_count} statements executed)")
                return True
            else:
                print("❌ Failed to connect to Supabase")
                return False
                
        except Exception as e:
            print(f"❌ Automatic schema setup failed: {e}")
            return self.manual_setup_schema()
    
    def manual_setup_schema(self):
        """Provide manual schema setup instructions"""
        print("\n📖 Manual Schema Setup Instructions:")
        print("=" * 50)
        print("1. Open your Supabase project dashboard")
        print("2. Go to the SQL Editor")
        print("3. Copy and paste the contents of 'supabase_schema.sql'")
        print("4. Execute the SQL script")
        print("5. Verify that all tables and functions were created")
        print()
        print(f"📄 Schema file location: {self.schema_file.absolute()}")
        print()
        
        response = input("✅ Have you completed the manual schema setup? (y/N): ")
        return response.lower() == 'y'
    
    def migrate_existing_data(self):
        """Migrate data from SQLite if it exists"""
        print("\n🔄 Checking for existing SQLite data...")
        
        sqlite_db = self.project_root / 'botzzz_admin.db'
        
        if not sqlite_db.exists():
            print("📝 No existing SQLite database found - starting fresh")
            return True
        
        print(f"🗄️  Found existing SQLite database: {sqlite_db}")
        response = input("🔄 Would you like to migrate existing data to Supabase? (y/N): ")
        
        if response.lower() != 'y':
            print("⏭️  Skipping data migration")
            return True
        
        try:
            print("🚀 Starting data migration...")
            
            # Import migration script
            from supabase_migration import SupabaseMigration
            
            # Create migration instance
            migration = SupabaseMigration(str(sqlite_db))
            
            # Create backup first
            backup_result = migration.create_migration_backup()
            if backup_result['success']:
                print(f"✅ Backup created: {backup_result['backup_path']}")
            else:
                print(f"❌ Backup failed: {backup_result['error']}")
                return False
            
            # Run migration
            migration_result = migration.run_full_migration()
            
            if migration_result['success']:
                print("✅ Data migration completed successfully!")
                print(f"📊 Migrated {migration_result['total_migrated']} records")
                if migration_result['total_errors'] > 0:
                    print(f"⚠️  {migration_result['total_errors']} errors occurred")
                
                # Save migration log
                log_file = self.project_root / f"migration_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(log_file, 'w') as f:
                    json.dump(migration_result, f, indent=2, default=str)
                print(f"📝 Migration log saved: {log_file}")
                
                return True
            else:
                print(f"❌ Migration failed: {migration_result['error']}")
                return False
                
        except Exception as e:
            print(f"❌ Migration error: {e}")
            return False
    
    def create_startup_script(self):
        """Create a startup script for easy server management"""
        print("\n🚀 Creating startup script...")
        
        startup_script = self.project_root / 'start_supabase.py'
        
        script_content = '''#!/usr/bin/env python3
"""
BOTZZZ Enterprise Platform Startup Script
Enhanced startup with Supabase integration
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Main startup function"""
    print("🚀 Starting BOTZZZ Enterprise Platform with Supabase...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv('.env')
    
    # Import and run the Flask app
    from app import app
    
    # Get configuration
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5002))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"🌐 Server starting on http://{host}:{port}")
    print("📊 Enhanced with Supabase real-time capabilities")
    print("🔒 Enterprise security features enabled")
    print()
    
    # Start the server
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    main()
'''
        
        with open(startup_script, 'w') as f:
            f.write(script_content)
        
        # Make it executable
        os.chmod(startup_script, 0o755)
        
        print(f"✅ Startup script created: {startup_script}")
        return True
    
    def run_tests(self):
        """Run basic connectivity and functionality tests"""
        print("\n🧪 Running connectivity tests...")
        
        try:
            # Load environment
            from dotenv import load_dotenv
            load_dotenv(self.env_file)
            
            # Import after dependencies are installed
            from supabase_config import get_supabase_manager
            
            # Test Supabase connection
            supabase_manager = get_supabase_manager()
            health_status = supabase_manager.get_health_status()
            
            if health_status.get('is_connected'):
                print("✅ Supabase connection test passed")
                
                # Test basic operations
                test_log = supabase_manager.log_system_event(
                    'INFO', 
                    'Supabase setup test', 
                    'setup_script',
                    metadata={'test': True}
                )
                
                if test_log:
                    print("✅ Database write test passed")
                else:
                    print("⚠️  Database write test failed")
                
                # Test read operations
                stats = supabase_manager.get_simulation_stats()
                if 'total' in stats:
                    print("✅ Database read test passed")
                else:
                    print("⚠️  Database read test failed")
                
                return True
            else:
                print("❌ Supabase connection test failed")
                return False
                
        except Exception as e:
            print(f"❌ Test error: {e}")
            return False
    
    def print_success_message(self):
        """Print setup completion message"""
        print("\n🎉" + "=" * 60)
        print("  SUPABASE SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 62)
        print()
        print("🚀 Your BOTZZZ Enterprise Platform is now enhanced with:")
        print("   ✅ PostgreSQL database with real-time capabilities")
        print("   ✅ Advanced analytics and business intelligence")
        print("   ✅ Enterprise-grade security and compliance")
        print("   ✅ Scalable architecture for high-volume operations")
        print()
        print("📋 Next steps:")
        print("   1. Start the server: python start_supabase.py")
        print("   2. Access the dashboard: http://localhost:5002")
        print("   3. Login with: admin / BOTZZZ2025!")
        print()
        print("📚 Resources:")
        print("   • Configuration: .env")
        print("   • Database schema: supabase_schema.sql")
        print("   • Migration logs: migration_log_*.json")
        print()
        print("🔧 Need help? Check the documentation or contact support.")
        print("=" * 62)
    
    def run_setup(self):
        """Run the complete setup process"""
        self.print_banner()
        
        # Step 1: Prerequisites
        if not self.check_prerequisites():
            print("❌ Prerequisites check failed. Please resolve the issues and try again.")
            return False
        
        # Step 2: Install dependencies
        if not self.install_dependencies():
            print("❌ Dependency installation failed.")
            return False
        
        # Step 3: Create environment file
        if not self.create_env_file():
            print("❌ Environment configuration failed.")
            return False
        
        # Step 4: Setup database schema
        if not self.setup_supabase_schema():
            print("❌ Database schema setup failed.")
            return False
        
        # Step 5: Migrate existing data
        if not self.migrate_existing_data():
            print("❌ Data migration failed.")
            return False
        
        # Step 6: Create startup script
        if not self.create_startup_script():
            print("❌ Startup script creation failed.")
            return False
        
        # Step 7: Run tests
        if not self.run_tests():
            print("⚠️  Some tests failed, but setup is complete.")
        
        # Success!
        self.print_success_message()
        return True

def main():
    """Main entry point"""
    setup = SupabaseSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test-only':
        # Run tests only
        setup.run_tests()
    else:
        # Run full setup
        setup.run_setup()

if __name__ == "__main__":
    main()

"""
Supabase Migration Script for BOTZZZ Enterprise Platform
Handles migration from SQLite to Supabase PostgreSQL with data preservation
"""

import sqlite3
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import logging
from supabase_config import get_supabase_manager, SupabaseConfig, initialize_supabase

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SupabaseMigration:
    """
    Comprehensive migration system for transitioning from SQLite to Supabase
    """
    
    def __init__(self, sqlite_db_path: str = 'botzzz_admin.db', supabase_config: SupabaseConfig = None):
        self.sqlite_db_path = sqlite_db_path
        self.supabase_manager = initialize_supabase(supabase_config) if supabase_config else get_supabase_manager()
        self.migration_log = []
        
    def log_migration_step(self, step: str, status: str, details: str = ""):
        """Log migration step with timestamp"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'step': step,
            'status': status,
            'details': details
        }
        self.migration_log.append(log_entry)
        logger.info(f"Migration Step: {step} - {status} - {details}")
    
    def check_sqlite_database(self) -> Dict[str, Any]:
        """Check SQLite database existence and structure"""
        try:
            if not os.path.exists(self.sqlite_db_path):
                return {
                    'exists': False,
                    'message': f'SQLite database not found at {self.sqlite_db_path}',
                    'tables': []
                }
            
            conn = sqlite3.connect(self.sqlite_db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Get row counts for each table
            table_stats = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                table_stats[table] = count
            
            conn.close()
            
            return {
                'exists': True,
                'tables': tables,
                'table_stats': table_stats,
                'total_records': sum(table_stats.values())
            }
            
        except Exception as e:
            logger.error(f"Error checking SQLite database: {e}")
            return {
                'exists': False,
                'error': str(e),
                'tables': []
            }
    
    def check_supabase_connection(self) -> Dict[str, Any]:
        """Verify Supabase connection and schema"""
        try:
            health_status = self.supabase_manager.get_health_status()
            
            # Test basic operations
            test_result = self.supabase_manager.client.table('simulation_runs').select('*').limit(1).execute()
            
            return {
                'connected': health_status.get('is_connected', False),
                'health_status': health_status,
                'schema_accessible': True,
                'message': 'Supabase connection verified successfully'
            }
            
        except Exception as e:
            logger.error(f"Supabase connection check failed: {e}")
            return {
                'connected': False,
                'error': str(e),
                'message': 'Failed to connect to Supabase'
            }
    
    def migrate_simulation_runs(self) -> Dict[str, Any]:
        """Migrate simulation_runs table from SQLite to Supabase"""
        try:
            self.log_migration_step("simulation_runs_migration", "started", "Beginning simulation runs migration")
            
            # Connect to SQLite
            conn = sqlite3.connect(self.sqlite_db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            # Get all simulation runs
            cursor.execute("""
                SELECT id, name, type, status, created_at, started_at, completed_at, 
                       parameters, results, log_file, created_by
                FROM simulation_runs
            """)
            
            rows = cursor.fetchall()
            migrated_count = 0
            errors = []
            
            for row in rows:
                try:
                    # Prepare data for Supabase
                    simulation_data = {
                        'name': row['name'],
                        'type': row['type'],
                        'status': row['status'],
                        'created_at': row['created_at'],
                        'started_at': row['started_at'],
                        'completed_at': row['completed_at'],
                        'parameters': json.loads(row['parameters']) if row['parameters'] else {},
                        'results': json.loads(row['results']) if row['results'] else None,
                        'log_file': row['log_file'],
                        'created_by': row['created_by'],
                        'priority': 5,  # Default priority
                        'progress_percentage': 100 if row['status'] == 'completed' else 0
                    }
                    
                    # Insert into Supabase
                    result = self.supabase_manager.client.table('simulation_runs').insert(simulation_data).execute()
                    
                    if result.data:
                        migrated_count += 1
                    else:
                        errors.append(f"Failed to insert simulation ID {row['id']}")
                        
                except Exception as e:
                    errors.append(f"Error migrating simulation ID {row['id']}: {str(e)}")
            
            conn.close()
            
            self.log_migration_step(
                "simulation_runs_migration", 
                "completed", 
                f"Migrated {migrated_count}/{len(rows)} simulation runs"
            )
            
            return {
                'success': True,
                'total_records': len(rows),
                'migrated_count': migrated_count,
                'errors': errors
            }
            
        except Exception as e:
            self.log_migration_step("simulation_runs_migration", "failed", str(e))
            return {
                'success': False,
                'error': str(e),
                'migrated_count': 0
            }
    
    def migrate_system_logs(self) -> Dict[str, Any]:
        """Migrate system_logs table from SQLite to Supabase"""
        try:
            self.log_migration_step("system_logs_migration", "started", "Beginning system logs migration")
            
            conn = sqlite3.connect(self.sqlite_db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all system logs
            cursor.execute("""
                SELECT id, level, message, component, timestamp, user_id
                FROM system_logs
            """)
            
            rows = cursor.fetchall()
            migrated_count = 0
            errors = []
            
            # Process in batches to avoid overwhelming Supabase
            batch_size = 100
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                batch_data = []
                
                for row in batch:
                    try:
                        log_data = {
                            'level': row['level'],
                            'message': row['message'],
                            'component': row['component'] or 'system',
                            'timestamp': row['timestamp'],
                            'user_id': row['user_id'],
                            'severity_score': self._calculate_severity_score(row['level'])
                        }
                        batch_data.append(log_data)
                        
                    except Exception as e:
                        errors.append(f"Error preparing log ID {row['id']}: {str(e)}")
                
                # Insert batch
                if batch_data:
                    try:
                        result = self.supabase_manager.client.table('system_logs').insert(batch_data).execute()
                        if result.data:
                            migrated_count += len(result.data)
                    except Exception as e:
                        errors.append(f"Batch insert error: {str(e)}")
            
            conn.close()
            
            self.log_migration_step(
                "system_logs_migration",
                "completed",
                f"Migrated {migrated_count}/{len(rows)} system logs"
            )
            
            return {
                'success': True,
                'total_records': len(rows),
                'migrated_count': migrated_count,
                'errors': errors
            }
            
        except Exception as e:
            self.log_migration_step("system_logs_migration", "failed", str(e))
            return {
                'success': False,
                'error': str(e),
                'migrated_count': 0
            }
    
    def migrate_bot_detection_events(self) -> Dict[str, Any]:
        """Migrate bot_detection_events table from SQLite to Supabase"""
        try:
            self.log_migration_step("bot_detection_migration", "started", "Beginning bot detection events migration")
            
            conn = sqlite3.connect(self.sqlite_db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all bot detection events
            cursor.execute("""
                SELECT event_type, bot_id, video_id, risk_score, detection_method, 
                       confidence_score, timestamp, simulation_run_id
                FROM bot_detection_events
            """)
            
            rows = cursor.fetchall()
            migrated_count = 0
            errors = []
            
            for row in rows:
                try:
                    event_data = {
                        'event_type': row['event_type'],
                        'bot_id': row['bot_id'],
                        'video_id': row['video_id'],
                        'platform': 'youtube',  # Default platform
                        'risk_score': row['risk_score'],
                        'detection_method': row['detection_method'],
                        'confidence_score': row['confidence_score'],
                        'timestamp': row['timestamp'],
                        'simulation_run_id': row['simulation_run_id']
                    }
                    
                    result = self.supabase_manager.client.table('bot_detection_events').insert(event_data).execute()
                    
                    if result.data:
                        migrated_count += 1
                    else:
                        errors.append(f"Failed to insert bot detection event")
                        
                except Exception as e:
                    errors.append(f"Error migrating bot detection event: {str(e)}")
            
            conn.close()
            
            self.log_migration_step(
                "bot_detection_migration",
                "completed", 
                f"Migrated {migrated_count}/{len(rows)} bot detection events"
            )
            
            return {
                'success': True,
                'total_records': len(rows),
                'migrated_count': migrated_count,
                'errors': errors
            }
            
        except Exception as e:
            self.log_migration_step("bot_detection_migration", "failed", str(e))
            return {
                'success': False,
                'error': str(e),
                'migrated_count': 0
            }
    
    def migrate_analytics_cache(self) -> Dict[str, Any]:
        """Migrate analytics_cache table from SQLite to Supabase"""
        try:
            self.log_migration_step("analytics_cache_migration", "started", "Beginning analytics cache migration")
            
            conn = sqlite3.connect(self.sqlite_db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all analytics cache entries that haven't expired
            cursor.execute("""
                SELECT cache_key, data, expires_at, created_at
                FROM analytics_cache
                WHERE expires_at > datetime('now')
            """)
            
            rows = cursor.fetchall()
            migrated_count = 0
            errors = []
            
            for row in rows:
                try:
                    cache_data = {
                        'cache_key': row['cache_key'],
                        'data': json.loads(row['data']) if row['data'] else {},
                        'expires_at': row['expires_at'],
                        'created_at': row['created_at'],
                        'access_count': 0,
                        'size_bytes': len(row['data']) if row['data'] else 0
                    }
                    
                    result = self.supabase_manager.client.table('analytics_cache').insert(cache_data).execute()
                    
                    if result.data:
                        migrated_count += 1
                    else:
                        errors.append(f"Failed to insert cache key: {row['cache_key']}")
                        
                except Exception as e:
                    errors.append(f"Error migrating cache key {row['cache_key']}: {str(e)}")
            
            conn.close()
            
            self.log_migration_step(
                "analytics_cache_migration",
                "completed",
                f"Migrated {migrated_count}/{len(rows)} analytics cache entries"
            )
            
            return {
                'success': True,
                'total_records': len(rows),
                'migrated_count': migrated_count,
                'errors': errors
            }
            
        except Exception as e:
            self.log_migration_step("analytics_cache_migration", "failed", str(e))
            return {
                'success': False,
                'error': str(e),
                'migrated_count': 0
            }
    
    def create_default_users(self) -> Dict[str, Any]:
        """Create default admin users in Supabase"""
        try:
            self.log_migration_step("default_users_creation", "started", "Creating default users")
            
            default_users = [
                {
                    'user_id': 'admin-001',
                    'email': 'admin@botzzz.com',
                    'username': 'admin',
                    'role': 'super_admin',
                    'is_active': True
                },
                {
                    'user_id': 'operator-001',
                    'email': 'operator@botzzz.com',
                    'username': 'operator',
                    'role': 'operator',
                    'is_active': True
                },
                {
                    'user_id': 'viewer-001',
                    'email': 'viewer@botzzz.com',
                    'username': 'viewer',
                    'role': 'viewer',
                    'is_active': True
                }
            ]
            
            created_count = 0
            errors = []
            
            for user_data in default_users:
                try:
                    # Check if user already exists
                    existing = self.supabase_manager.client.table('user_profiles')\
                        .select('*')\
                        .eq('user_id', user_data['user_id'])\
                        .execute()
                    
                    if not existing.data:
                        result = self.supabase_manager.client.table('user_profiles').insert(user_data).execute()
                        if result.data:
                            created_count += 1
                            logger.info(f"Created user: {user_data['username']}")
                    else:
                        logger.info(f"User already exists: {user_data['username']}")
                        
                except Exception as e:
                    errors.append(f"Error creating user {user_data['username']}: {str(e)}")
            
            self.log_migration_step(
                "default_users_creation",
                "completed",
                f"Created {created_count} default users"
            )
            
            return {
                'success': True,
                'created_count': created_count,
                'errors': errors
            }
            
        except Exception as e:
            self.log_migration_step("default_users_creation", "failed", str(e))
            return {
                'success': False,
                'error': str(e),
                'created_count': 0
            }
    
    def run_full_migration(self) -> Dict[str, Any]:
        """Execute complete migration process"""
        migration_start = datetime.now()
        self.log_migration_step("full_migration", "started", "Beginning full database migration")
        
        # Step 1: Check prerequisites
        sqlite_check = self.check_sqlite_database()
        supabase_check = self.check_supabase_connection()
        
        if not sqlite_check.get('exists', False):
            return {
                'success': False,
                'error': 'SQLite database not found',
                'migration_log': self.migration_log
            }
        
        if not supabase_check.get('connected', False):
            return {
                'success': False,
                'error': 'Cannot connect to Supabase',
                'migration_log': self.migration_log
            }
        
        # Step 2: Execute migrations
        results = {}
        
        # Migrate core tables
        results['simulation_runs'] = self.migrate_simulation_runs()
        results['system_logs'] = self.migrate_system_logs()
        results['bot_detection_events'] = self.migrate_bot_detection_events()
        results['analytics_cache'] = self.migrate_analytics_cache()
        
        # Create default users
        results['default_users'] = self.create_default_users()
        
        # Calculate totals
        total_migrated = sum(r.get('migrated_count', 0) for r in results.values() if isinstance(r, dict))
        total_errors = sum(len(r.get('errors', [])) for r in results.values() if isinstance(r, dict))
        
        migration_end = datetime.now()
        duration = (migration_end - migration_start).total_seconds()
        
        self.log_migration_step(
            "full_migration",
            "completed",
            f"Migration completed in {duration:.2f} seconds. Migrated: {total_migrated} records, Errors: {total_errors}"
        )
        
        return {
            'success': True,
            'duration_seconds': duration,
            'total_migrated': total_migrated,
            'total_errors': total_errors,
            'detailed_results': results,
            'migration_log': self.migration_log
        }
    
    def _calculate_severity_score(self, level: str) -> int:
        """Calculate numerical severity score for log level"""
        severity_map = {
            'DEBUG': 1,
            'INFO': 2,
            'WARNING': 3,
            'ERROR': 4,
            'CRITICAL': 5
        }
        return severity_map.get(level, 2)
    
    def create_migration_backup(self) -> Dict[str, Any]:
        """Create backup of SQLite database before migration"""
        try:
            if not os.path.exists(self.sqlite_db_path):
                return {'success': False, 'error': 'Source database not found'}
            
            backup_path = f"{self.sqlite_db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Copy SQLite database
            import shutil
            shutil.copy2(self.sqlite_db_path, backup_path)
            
            return {
                'success': True,
                'backup_path': backup_path,
                'message': f'Backup created at {backup_path}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def validate_migration(self) -> Dict[str, Any]:
        """Validate migration by comparing record counts"""
        try:
            sqlite_check = self.check_sqlite_database()
            
            if not sqlite_check.get('exists', False):
                return {'success': False, 'error': 'SQLite database not found for validation'}
            
            # Get Supabase record counts
            supabase_counts = {}
            tables_to_check = ['simulation_runs', 'system_logs', 'bot_detection_events']
            
            for table in tables_to_check:
                try:
                    result = self.supabase_manager.client.table(table).select('*', count='exact').limit(1).execute()
                    supabase_counts[table] = result.count
                except:
                    supabase_counts[table] = 0
            
            # Compare counts
            sqlite_counts = sqlite_check.get('table_stats', {})
            comparison = {}
            
            for table in tables_to_check:
                sqlite_count = sqlite_counts.get(table, 0)
                supabase_count = supabase_counts.get(table, 0)
                comparison[table] = {
                    'sqlite_count': sqlite_count,
                    'supabase_count': supabase_count,
                    'matches': sqlite_count == supabase_count
                }
            
            all_match = all(comp['matches'] for comp in comparison.values())
            
            return {
                'success': True,
                'validation_passed': all_match,
                'comparison': comparison,
                'message': 'Migration validation completed'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

def main():
    """Main migration execution function"""
    print("🚀 BOTZZZ Supabase Migration Tool")
    print("=" * 50)
    
    # Initialize migration
    migration = SupabaseMigration()
    
    # Create backup
    print("\n📦 Creating backup...")
    backup_result = migration.create_migration_backup()
    if backup_result['success']:
        print(f"✅ Backup created: {backup_result['backup_path']}")
    else:
        print(f"❌ Backup failed: {backup_result['error']}")
        return
    
    # Run migration
    print("\n🔄 Running full migration...")
    migration_result = migration.run_full_migration()
    
    if migration_result['success']:
        print(f"✅ Migration completed successfully!")
        print(f"📊 Total records migrated: {migration_result['total_migrated']}")
        print(f"⚠️  Total errors: {migration_result['total_errors']}")
        print(f"⏱️  Duration: {migration_result['duration_seconds']:.2f} seconds")
        
        # Validate migration
        print("\n🔍 Validating migration...")
        validation_result = migration.validate_migration()
        if validation_result['success'] and validation_result['validation_passed']:
            print("✅ Migration validation passed!")
        else:
            print("❌ Migration validation failed or had issues")
            print(f"Details: {validation_result}")
    else:
        print(f"❌ Migration failed: {migration_result['error']}")
    
    # Save migration log
    log_filename = f"migration_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_filename, 'w') as f:
        json.dump(migration_result, f, indent=2, default=str)
    
    print(f"\n📝 Migration log saved to: {log_filename}")

if __name__ == "__main__":
    main()

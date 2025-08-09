"""
Supabase Configuration and Database Client
Provides PostgreSQL database connection and real-time capabilities for BOTZZZ Enterprise Platform
"""

import os
from supabase import create_client, Client
from typing import Dict, Any, List, Optional
import json
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SupabaseConfig:
    """Supabase configuration settings"""
    url: str
    key: str
    service_role_key: str
    schema: str = 'public'
    auto_refresh_token: bool = True
    persist_session: bool = True
    
class SupabaseManager:
    """
    Advanced Supabase database manager for enterprise-grade operations
    Provides real-time subscriptions, advanced querying, and data synchronization
    """
    
    def __init__(self, config: SupabaseConfig = None):
        # Use environment variables or default values
        self.url = config.url if config else os.getenv('SUPABASE_URL', 'https://your-project.supabase.co')
        self.key = config.key if config else os.getenv('SUPABASE_ANON_KEY', 'your-anon-key')
        self.service_key = config.service_role_key if config else os.getenv('SUPABASE_SERVICE_KEY', 'your-service-key')
        
        # Initialize clients
        self.client: Client = create_client(self.url, self.key)
        self.service_client: Client = create_client(self.url, self.service_key)
        
        # Real-time subscriptions storage
        self.subscriptions = {}
        self.is_connected = False
        
        logger.info("🚀 Supabase Manager initialized successfully")
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test database connection and return status"""
        try:
            # Test basic connection
            result = self.client.table('simulation_runs').select('*').limit(1).execute()
            
            # Test service role connection
            service_result = self.service_client.table('system_logs').select('*').limit(1).execute()
            
            self.is_connected = True
            return {
                'status': 'connected',
                'timestamp': datetime.now().isoformat(),
                'client_connection': True,
                'service_connection': True,
                'message': 'Supabase connection established successfully'
            }
        except Exception as e:
            logger.error(f"Supabase connection failed: {e}")
            self.is_connected = False
            return {
                'status': 'failed',
                'timestamp': datetime.now().isoformat(),
                'client_connection': False,
                'service_connection': False,
                'error': str(e),
                'message': 'Failed to connect to Supabase'
            }
    
    # =====================================
    # SIMULATION RUNS MANAGEMENT
    # =====================================
    
    def create_simulation(self, name: str, sim_type: str, parameters: Dict, created_by: str) -> Dict[str, Any]:
        """Create a new simulation run with enhanced tracking"""
        try:
            simulation_data = {
                'name': name,
                'type': sim_type,
                'status': 'pending',
                'created_at': datetime.now().isoformat(),
                'parameters': json.dumps(parameters),
                'created_by': created_by,
                'priority': parameters.get('priority', 5),
                'estimated_duration': parameters.get('estimated_duration', 300),  # seconds
                'resource_requirements': json.dumps(parameters.get('resources', {}))
            }
            
            result = self.client.table('simulation_runs').insert(simulation_data).execute()
            
            if result.data:
                simulation_id = result.data[0]['id']
                logger.info(f"✅ Simulation created: {name} (ID: {simulation_id})")
                return {
                    'success': True,
                    'simulation_id': simulation_id,
                    'data': result.data[0]
                }
            else:
                raise Exception("Failed to create simulation")
                
        except Exception as e:
            logger.error(f"❌ Failed to create simulation: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_simulation_stats(self) -> Dict[str, Any]:
        """Get comprehensive simulation statistics"""
        try:
            # Get total counts by status
            total_result = self.client.table('simulation_runs').select('status').execute()
            
            stats = {
                'total': len(total_result.data),
                'running': 0,
                'completed': 0,
                'failed': 0,
                'pending': 0
            }
            
            # Count by status
            for sim in total_result.data:
                status = sim['status']
                if status in stats:
                    stats[status] += 1
            
            # Get recent simulations
            recent_result = self.client.table('simulation_runs')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(10)\
                .execute()
            
            stats['recent_simulations'] = recent_result.data
            stats['success_rate'] = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get simulation stats: {e}")
            return {
                'total': 0,
                'running': 0,
                'completed': 0,
                'failed': 0,
                'recent_simulations': [],
                'success_rate': 0,
                'error': str(e)
            }
    
    def update_simulation_status(self, simulation_id: int, status: str, results: Dict = None) -> bool:
        """Update simulation status with detailed tracking"""
        try:
            update_data = {
                'status': status,
                'updated_at': datetime.now().isoformat()
            }
            
            if status == 'running':
                update_data['started_at'] = datetime.now().isoformat()
            elif status in ['completed', 'failed']:
                update_data['completed_at'] = datetime.now().isoformat()
                if results:
                    update_data['results'] = json.dumps(results)
            
            result = self.client.table('simulation_runs')\
                .update(update_data)\
                .eq('id', simulation_id)\
                .execute()
            
            logger.info(f"✅ Simulation {simulation_id} status updated to: {status}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update simulation status: {e}")
            return False
    
    # =====================================
    # SYSTEM LOGS MANAGEMENT
    # =====================================
    
    def log_system_event(self, level: str, message: str, component: str = 'system', 
                        user_id: str = None, metadata: Dict = None) -> bool:
        """Enhanced system logging with metadata support"""
        try:
            log_data = {
                'level': level,
                'message': message,
                'component': component,
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'metadata': json.dumps(metadata) if metadata else None,
                'severity_score': self._calculate_severity_score(level),
                'source_ip': metadata.get('ip_address') if metadata else None
            }
            
            result = self.client.table('system_logs').insert(log_data).execute()
            
            # For critical errors, also trigger real-time alert
            if level in ['ERROR', 'CRITICAL']:
                self._trigger_realtime_alert(log_data)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to log system event: {e}")
            return False
    
    def get_system_logs(self, filters: Dict = None, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """Get system logs with advanced filtering and pagination"""
        try:
            query = self.client.table('system_logs').select('*')
            
            # Apply filters
            if filters:
                if filters.get('level'):
                    query = query.eq('level', filters['level'])
                if filters.get('component'):
                    query = query.eq('component', filters['component'])
                if filters.get('user_id'):
                    query = query.eq('user_id', filters['user_id'])
                if filters.get('start_date'):
                    query = query.gte('timestamp', filters['start_date'])
                if filters.get('end_date'):
                    query = query.lte('timestamp', filters['end_date'])
            
            # Get total count for pagination
            count_result = query.execute()
            total_count = len(count_result.data)
            
            # Apply pagination
            offset = (page - 1) * per_page
            logs_result = query.order('timestamp', desc=True)\
                .range(offset, offset + per_page - 1)\
                .execute()
            
            return {
                'logs': logs_result.data,
                'total_count': total_count,
                'page': page,
                'per_page': per_page,
                'total_pages': (total_count + per_page - 1) // per_page
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get system logs: {e}")
            return {
                'logs': [],
                'total_count': 0,
                'error': str(e)
            }
    
    # =====================================
    # ANALYTICS & BUSINESS INTELLIGENCE
    # =====================================
    
    def store_analytics_data(self, metric_name: str, value: float, 
                           dimensions: Dict = None, timestamp: datetime = None) -> bool:
        """Store analytics data for business intelligence"""
        try:
            analytics_data = {
                'metric_name': metric_name,
                'value': value,
                'dimensions': json.dumps(dimensions) if dimensions else None,
                'timestamp': (timestamp or datetime.now()).isoformat(),
                'created_at': datetime.now().isoformat()
            }
            
            result = self.client.table('analytics_metrics').insert(analytics_data).execute()
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store analytics data: {e}")
            return False
    
    def get_analytics_summary(self, time_range: int = 24) -> Dict[str, Any]:
        """Get comprehensive analytics summary for specified time range (hours)"""
        try:
            start_time = datetime.now() - timedelta(hours=time_range)
            
            # Get metrics aggregated by type
            result = self.client.table('analytics_metrics')\
                .select('metric_name, value, timestamp')\
                .gte('timestamp', start_time.isoformat())\
                .execute()
            
            # Process metrics
            metrics_summary = {}
            for metric in result.data:
                name = metric['metric_name']
                if name not in metrics_summary:
                    metrics_summary[name] = {
                        'count': 0,
                        'total': 0,
                        'average': 0,
                        'latest': 0
                    }
                
                metrics_summary[name]['count'] += 1
                metrics_summary[name]['total'] += metric['value']
                metrics_summary[name]['latest'] = metric['value']
            
            # Calculate averages
            for name, data in metrics_summary.items():
                data['average'] = data['total'] / data['count'] if data['count'] > 0 else 0
            
            return {
                'time_range_hours': time_range,
                'metrics': metrics_summary,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get analytics summary: {e}")
            return {'metrics': {}, 'error': str(e)}
    
    # =====================================
    # REAL-TIME SUBSCRIPTIONS
    # =====================================
    
    def subscribe_to_simulation_updates(self, callback_function) -> str:
        """Subscribe to real-time simulation updates"""
        try:
            subscription_id = f"sim_updates_{datetime.now().timestamp()}"
            
            # Create real-time subscription
            subscription = self.client.channel('simulation_updates')\
                .on('postgres_changes', 
                    event='*', 
                    schema='public', 
                    table='simulation_runs',
                    callback=callback_function)\
                .subscribe()
            
            self.subscriptions[subscription_id] = subscription
            
            logger.info(f"✅ Subscribed to simulation updates: {subscription_id}")
            return subscription_id
            
        except Exception as e:
            logger.error(f"❌ Failed to subscribe to simulation updates: {e}")
            return None
    
    def subscribe_to_system_alerts(self, callback_function) -> str:
        """Subscribe to real-time system alerts and critical logs"""
        try:
            subscription_id = f"alerts_{datetime.now().timestamp()}"
            
            # Subscribe to critical and error logs
            subscription = self.client.channel('system_alerts')\
                .on('postgres_changes',
                    event='INSERT',
                    schema='public',
                    table='system_logs',
                    filter='level=in.(ERROR,CRITICAL)',
                    callback=callback_function)\
                .subscribe()
            
            self.subscriptions[subscription_id] = subscription
            
            logger.info(f"✅ Subscribed to system alerts: {subscription_id}")
            return subscription_id
            
        except Exception as e:
            logger.error(f"❌ Failed to subscribe to system alerts: {e}")
            return None
    
    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from real-time updates"""
        try:
            if subscription_id in self.subscriptions:
                self.subscriptions[subscription_id].unsubscribe()
                del self.subscriptions[subscription_id]
                logger.info(f"✅ Unsubscribed from: {subscription_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to unsubscribe: {e}")
            return False
    
    # =====================================
    # USER MANAGEMENT & AUTHENTICATION
    # =====================================
    
    def create_user_profile(self, user_id: str, email: str, username: str, 
                          role: str = 'user', metadata: Dict = None) -> bool:
        """Create user profile with enhanced tracking"""
        try:
            profile_data = {
                'user_id': user_id,
                'email': email,
                'username': username,
                'role': role,
                'metadata': json.dumps(metadata) if metadata else None,
                'created_at': datetime.now().isoformat(),
                'is_active': True,
                'last_login': None,
                'login_count': 0
            }
            
            result = self.client.table('user_profiles').insert(profile_data).execute()
            
            logger.info(f"✅ User profile created: {username}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create user profile: {e}")
            return False
    
    def update_user_login(self, user_id: str) -> bool:
        """Update user login statistics"""
        try:
            # Increment login count and update last login
            result = self.client.rpc('increment_user_login', {'user_id': user_id}).execute()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update user login: {e}")
            return False
    
    # =====================================
    # ADVANCED QUERYING & REPORTING
    # =====================================
    
    def execute_custom_query(self, table: str, query_config: Dict) -> Dict[str, Any]:
        """Execute custom queries for advanced reporting"""
        try:
            query = self.client.table(table)
            
            # Apply select
            if query_config.get('select'):
                query = query.select(query_config['select'])
            else:
                query = query.select('*')
            
            # Apply filters
            if query_config.get('filters'):
                for filter_config in query_config['filters']:
                    op = filter_config.get('op', 'eq')
                    column = filter_config['column']
                    value = filter_config['value']
                    
                    if op == 'eq':
                        query = query.eq(column, value)
                    elif op == 'neq':
                        query = query.neq(column, value)
                    elif op == 'gt':
                        query = query.gt(column, value)
                    elif op == 'gte':
                        query = query.gte(column, value)
                    elif op == 'lt':
                        query = query.lt(column, value)
                    elif op == 'lte':
                        query = query.lte(column, value)
                    elif op == 'like':
                        query = query.like(column, value)
                    elif op == 'in':
                        query = query.is_('in', value)
            
            # Apply ordering
            if query_config.get('order'):
                for order in query_config['order']:
                    column = order['column']
                    desc = order.get('desc', False)
                    query = query.order(column, desc=desc)
            
            # Apply limit
            if query_config.get('limit'):
                query = query.limit(query_config['limit'])
            
            # Execute query
            result = query.execute()
            
            return {
                'success': True,
                'data': result.data,
                'count': len(result.data)
            }
            
        except Exception as e:
            logger.error(f"❌ Custom query failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'data': []
            }
    
    # =====================================
    # UTILITY METHODS
    # =====================================
    
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
    
    def _trigger_realtime_alert(self, log_data: Dict):
        """Trigger real-time alert for critical events"""
        try:
            alert_data = {
                'alert_type': 'system_error',
                'severity': log_data['level'],
                'message': log_data['message'],
                'component': log_data['component'],
                'timestamp': log_data['timestamp'],
                'acknowledged': False
            }
            
            # Insert into alerts table for tracking
            self.client.table('system_alerts').insert(alert_data).execute()
            
        except Exception as e:
            logger.error(f"❌ Failed to trigger real-time alert: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive database health status"""
        try:
            # Test connection
            connection_test = asyncio.run(self.test_connection()) if not self.is_connected else {'status': 'connected'}
            
            # Get table sizes
            tables = ['simulation_runs', 'system_logs', 'analytics_metrics', 'user_profiles']
            table_stats = {}
            
            for table in tables:
                try:
                    result = self.client.table(table).select('*', count='exact').limit(1).execute()
                    table_stats[table] = {'count': result.count, 'status': 'healthy'}
                except:
                    table_stats[table] = {'count': 0, 'status': 'error'}
            
            # Calculate uptime and performance metrics
            health_data = {
                'connection_status': connection_test['status'],
                'is_connected': self.is_connected,
                'active_subscriptions': len(self.subscriptions),
                'table_statistics': table_stats,
                'timestamp': datetime.now().isoformat(),
                'response_time_ms': 0  # Would implement actual response time testing
            }
            
            return health_data
            
        except Exception as e:
            logger.error(f"❌ Failed to get health status: {e}")
            return {
                'connection_status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Global instance
supabase_manager = None

def get_supabase_manager() -> SupabaseManager:
    """Get global Supabase manager instance"""
    global supabase_manager
    if supabase_manager is None:
        supabase_manager = SupabaseManager()
    return supabase_manager

def initialize_supabase(config: SupabaseConfig = None) -> SupabaseManager:
    """Initialize Supabase with custom configuration"""
    global supabase_manager
    supabase_manager = SupabaseManager(config)
    return supabase_manager

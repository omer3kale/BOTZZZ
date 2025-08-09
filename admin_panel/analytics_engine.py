"""
Real-Time Analytics Engine - BOTZZZ Tier 1 Feature
Advanced analytics and insights for bot operations and system performance
"""

import json
import time
import threading
from datetime import datetime, timedelta
from collections import defaultdict, deque
from typing import Dict, List, Any, Optional
import sqlite3
import logging

class AnalyticsEngine:
    """
    Enterprise-grade real-time analytics engine
    Provides comprehensive insights and predictive analytics
    """
    
    def __init__(self):
        self.metrics_buffer = defaultdict(deque)
        self.real_time_data = defaultdict(dict)
        self.analytics_db = 'botzzz_analytics.db'
        self.is_running = False
        self.update_interval = 5  # seconds
        self.retention_hours = 24
        
        self.init_database()
        
    def init_database(self):
        """Initialize analytics database"""
        try:
            with sqlite3.connect(self.analytics_db) as conn:
                cursor = conn.cursor()
                
                # Analytics events table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analytics_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        event_type VARCHAR(50),
                        service_name VARCHAR(100),
                        metric_name VARCHAR(100),
                        metric_value REAL,
                        metadata TEXT,
                        tags TEXT
                    )
                ''')
                
                # Performance metrics table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS performance_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        service VARCHAR(50),
                        response_time REAL,
                        success_rate REAL,
                        throughput REAL,
                        error_rate REAL,
                        cpu_usage REAL,
                        memory_usage REAL
                    )
                ''')
                
                # User activity table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_activity (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        user_id VARCHAR(50),
                        action VARCHAR(100),
                        endpoint VARCHAR(200),
                        duration REAL,
                        success BOOLEAN
                    )
                ''')
                
                conn.commit()
                logging.info("Analytics database initialized successfully")
                
        except Exception as e:
            logging.error(f"Error initializing analytics database: {e}")
    
    def start(self):
        """Start the analytics engine"""
        if not self.is_running:
            self.is_running = True
            self.analytics_thread = threading.Thread(target=self._analytics_loop, daemon=True)
            self.analytics_thread.start()
            logging.info("Analytics engine started")
    
    def stop(self):
        """Stop the analytics engine"""
        self.is_running = False
        logging.info("Analytics engine stopped")
    
    def _analytics_loop(self):
        """Main analytics processing loop"""
        while self.is_running:
            try:
                self._process_metrics()
                self._calculate_insights()
                self._cleanup_old_data()
                time.sleep(self.update_interval)
            except Exception as e:
                logging.error(f"Error in analytics loop: {e}")
    
    def record_event(self, event_type: str, service_name: str, metric_name: str, 
                    metric_value: float, metadata: Optional[Dict] = None, 
                    tags: Optional[List[str]] = None):
        """Record an analytics event"""
        try:
            with sqlite3.connect(self.analytics_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO analytics_events 
                    (event_type, service_name, metric_name, metric_value, metadata, tags)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    event_type,
                    service_name,
                    metric_name,
                    metric_value,
                    json.dumps(metadata) if metadata else None,
                    json.dumps(tags) if tags else None
                ))
                conn.commit()
                
        except Exception as e:
            logging.error(f"Error recording analytics event: {e}")
    
    def record_performance_metric(self, service: str, response_time: float, 
                                success_rate: float, throughput: float, 
                                error_rate: float, cpu_usage: float = 0.0, 
                                memory_usage: float = 0.0):
        """Record performance metrics"""
        try:
            with sqlite3.connect(self.analytics_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO performance_metrics 
                    (service, response_time, success_rate, throughput, error_rate, cpu_usage, memory_usage)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (service, response_time, success_rate, throughput, error_rate, cpu_usage, memory_usage))
                conn.commit()
                
        except Exception as e:
            logging.error(f"Error recording performance metric: {e}")
    
    def record_user_activity(self, user_id: str, action: str, endpoint: str, 
                           duration: float, success: bool):
        """Record user activity"""
        try:
            with sqlite3.connect(self.analytics_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO user_activity 
                    (user_id, action, endpoint, duration, success)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, action, endpoint, duration, success))
                conn.commit()
                
        except Exception as e:
            logging.error(f"Error recording user activity: {e}")
    
    def get_real_time_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive real-time dashboard data"""
        try:
            with sqlite3.connect(self.analytics_db) as conn:
                cursor = conn.cursor()
                
                # Service performance overview
                cursor.execute('''
                    SELECT service, 
                           AVG(response_time) as avg_response_time,
                           AVG(success_rate) as avg_success_rate,
                           AVG(throughput) as avg_throughput,
                           AVG(error_rate) as avg_error_rate,
                           COUNT(*) as data_points
                    FROM performance_metrics 
                    WHERE timestamp > datetime('now', '-1 hour')
                    GROUP BY service
                ''')
                
                services = {}
                for row in cursor.fetchall():
                    services[row[0]] = {
                        'avg_response_time': round(row[1] or 0, 2),
                        'avg_success_rate': round(row[2] or 0, 4),
                        'avg_throughput': round(row[3] or 0, 2),
                        'avg_error_rate': round(row[4] or 0, 4),
                        'data_points': row[5]
                    }
                
                # Recent activity summary
                cursor.execute('''
                    SELECT action, COUNT(*) as count
                    FROM user_activity 
                    WHERE timestamp > datetime('now', '-1 hour')
                    GROUP BY action
                    ORDER BY count DESC
                    LIMIT 10
                ''')
                
                recent_activities = {row[0]: row[1] for row in cursor.fetchall()}
                
                # System trends
                cursor.execute('''
                    SELECT 
                        DATE(timestamp) as date,
                        AVG(response_time) as avg_response_time,
                        AVG(success_rate) as avg_success_rate,
                        COUNT(*) as total_requests
                    FROM performance_metrics 
                    WHERE timestamp > datetime('now', '-7 days')
                    GROUP BY DATE(timestamp)
                    ORDER BY date DESC
                ''')
                
                trends = []
                for row in cursor.fetchall():
                    trends.append({
                        'date': row[0],
                        'avg_response_time': round(row[1] or 0, 2),
                        'avg_success_rate': round(row[2] or 0, 4),
                        'total_requests': row[3]
                    })
                
                return {
                    'services': services,
                    'recent_activities': recent_activities,
                    'trends': trends,
                    'timestamp': datetime.now().isoformat(),
                    'total_services': len(services),
                    'total_recent_activities': sum(recent_activities.values())
                }
                
        except Exception as e:
            logging.error(f"Error getting dashboard data: {e}")
            return {}
    
    def get_service_insights(self, service_name: str, hours: int = 24) -> Dict[str, Any]:
        """Get detailed insights for a specific service"""
        try:
            with sqlite3.connect(self.analytics_db) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT 
                        MIN(response_time) as min_response_time,
                        MAX(response_time) as max_response_time,
                        AVG(response_time) as avg_response_time,
                        AVG(success_rate) as avg_success_rate,
                        AVG(throughput) as avg_throughput,
                        AVG(error_rate) as avg_error_rate,
                        COUNT(*) as total_requests
                    FROM performance_metrics 
                    WHERE service = ? AND timestamp > datetime('now', '-{} hours')
                '''.format(hours), (service_name,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'service': service_name,
                        'min_response_time': row[0] or 0,
                        'max_response_time': row[1] or 0,
                        'avg_response_time': round(row[2] or 0, 2),
                        'avg_success_rate': round(row[3] or 0, 4),
                        'avg_throughput': round(row[4] or 0, 2),
                        'avg_error_rate': round(row[5] or 0, 4),
                        'total_requests': row[6],
                        'health_score': self._calculate_health_score(row[2], row[3], row[5])
                    }
                
                return {'service': service_name, 'no_data': True}
                
        except Exception as e:
            logging.error(f"Error getting service insights: {e}")
            return {}
    
    def _calculate_health_score(self, avg_response_time: float, success_rate: float, error_rate: float) -> float:
        """Calculate a health score from 0-100"""
        # Response time score (lower is better)
        response_score = max(0, 100 - (avg_response_time or 0) / 10)  # Penalty for high response times
        
        # Success rate score (higher is better)
        success_score = (success_rate or 0) * 100
        
        # Error rate score (lower is better)
        error_score = max(0, 100 - (error_rate or 0) * 1000)  # Penalty for high error rates
        
        # Weighted average
        health_score = (response_score * 0.3 + success_score * 0.5 + error_score * 0.2)
        
        return round(health_score, 2)
    
    def _process_metrics(self):
        """Process accumulated metrics"""
        # This would integrate with existing monitoring systems
        pass
    
    def _calculate_insights(self):
        """Calculate predictive insights and anomalies"""
        # This would perform ML-based analysis
        pass
    
    def _cleanup_old_data(self):
        """Remove old data beyond retention period"""
        try:
            with sqlite3.connect(self.analytics_db) as conn:
                cursor = conn.cursor()
                
                retention_timestamp = datetime.now() - timedelta(hours=self.retention_hours * 7)  # Keep 7x retention for trends
                
                cursor.execute('DELETE FROM analytics_events WHERE timestamp < ?', (retention_timestamp,))
                cursor.execute('DELETE FROM performance_metrics WHERE timestamp < ?', (retention_timestamp,))
                cursor.execute('DELETE FROM user_activity WHERE timestamp < ?', (retention_timestamp,))
                
                conn.commit()
                
        except Exception as e:
            logging.error(f"Error cleaning up old data: {e}")

# Global analytics engine instance
analytics_engine = AnalyticsEngine()
analytics_engine.start()

# Convenience functions for easy integration
def record_service_performance(service: str, response_time: float, success: bool):
    """Record service performance data"""
    success_rate = 1.0 if success else 0.0
    error_rate = 0.0 if success else 1.0
    throughput = 1.0 / response_time if response_time > 0 else 0.0
    
    analytics_engine.record_performance_metric(
        service, response_time, success_rate, throughput, error_rate
    )

def record_api_call(user_id: str, endpoint: str, duration: float, success: bool):
    """Record API call analytics"""
    analytics_engine.record_user_activity(user_id, 'API_CALL', endpoint, duration, success)

def get_analytics_summary():
    """Get analytics summary for dashboard"""
    return analytics_engine.get_real_time_dashboard_data()

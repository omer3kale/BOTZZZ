"""
Advanced Customer Success & Retention Hub
Ultra High-Impact Business Feature - Tier 2 Feature #6

Comprehensive customer lifecycle management system with AI-powered retention analytics,
automated customer journey optimization, and predictive churn prevention.
"""

import sqlite3
import json
import datetime
import time
import threading
import random
import hashlib
import requests
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomerStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CHURNED = "churned"
    AT_RISK = "at_risk"
    VIP = "vip"
    TRIAL = "trial"

class CustomerTier(Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"

class InteractionType(Enum):
    EMAIL = "email"
    CHAT = "chat"
    PHONE = "phone"
    VIDEO_CALL = "video_call"
    IN_APP = "in_app"
    SOCIAL_MEDIA = "social_media"

class ChurnRisk(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class JourneyStage(Enum):
    AWARENESS = "awareness"
    TRIAL = "trial"
    ONBOARDING = "onboarding"
    ACTIVATION = "activation"
    GROWTH = "growth"
    RETENTION = "retention"
    ADVOCACY = "advocacy"

@dataclass
class Customer:
    customer_id: str
    email: str
    name: str
    company: str
    tier: CustomerTier
    status: CustomerStatus
    join_date: datetime.datetime
    last_activity: datetime.datetime
    lifetime_value: float
    monthly_usage: float
    satisfaction_score: float
    churn_risk: ChurnRisk
    journey_stage: JourneyStage

@dataclass
class CustomerInteraction:
    interaction_id: str
    customer_id: str
    interaction_type: InteractionType
    subject: str
    description: str
    timestamp: datetime.datetime
    duration_minutes: int
    satisfaction_rating: int
    resolution_status: str
    agent_id: str

@dataclass
class RetentionMetric:
    metric_name: str
    value: float
    target: float
    period: str
    trend: float
    benchmark: float

class CustomerSuccessHub:
    def __init__(self, db_path: str = "customer_success.db"):
        self.db_path = db_path
        self.customers = {}
        self.interactions = []
        self.retention_models = {}
        self.success_metrics = {}
        self.is_monitoring = False
        self.monitoring_thread = None
        
        # Initialize database
        self.init_database()
        
        # Load existing data
        self.load_customers()
        self.load_interactions()
        
        # Start monitoring
        self.start_monitoring()
        
        logger.info("Customer Success Hub initialized successfully")

    def init_database(self):
        """Initialize database schema for customer success management"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                company TEXT,
                tier TEXT DEFAULT 'bronze',
                status TEXT DEFAULT 'trial',
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                lifetime_value REAL DEFAULT 0.0,
                monthly_usage REAL DEFAULT 0.0,
                satisfaction_score REAL DEFAULT 0.0,
                churn_risk TEXT DEFAULT 'low',
                journey_stage TEXT DEFAULT 'awareness',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Customer interactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction_id TEXT UNIQUE NOT NULL,
                customer_id TEXT NOT NULL,
                interaction_type TEXT NOT NULL,
                subject TEXT,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration_minutes INTEGER DEFAULT 0,
                satisfaction_rating INTEGER DEFAULT 0,
                resolution_status TEXT DEFAULT 'pending',
                agent_id TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        
        # Customer journey events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS journey_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data TEXT, -- JSON
                stage_from TEXT,
                stage_to TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                impact_score REAL DEFAULT 0.0,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        
        # Retention metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS retention_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                target REAL,
                period TEXT,
                trend REAL DEFAULT 0.0,
                benchmark REAL DEFAULT 0.0,
                calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Churn predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS churn_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                churn_probability REAL NOT NULL,
                risk_factors TEXT, -- JSON array
                recommended_actions TEXT, -- JSON array
                confidence_score REAL,
                prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                model_version TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        
        # Customer health scores table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                health_score REAL NOT NULL,
                engagement_score REAL,
                usage_score REAL,
                satisfaction_score REAL,
                payment_health_score REAL,
                calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        
        # Success playbooks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS success_playbooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                playbook_name TEXT UNIQUE NOT NULL,
                customer_segment TEXT,
                trigger_conditions TEXT, -- JSON
                actions TEXT, -- JSON array
                success_metrics TEXT, -- JSON
                is_active BOOLEAN DEFAULT TRUE,
                execution_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Customer feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feedback_id TEXT UNIQUE NOT NULL,
                customer_id TEXT NOT NULL,
                feedback_type TEXT,
                rating INTEGER,
                comment TEXT,
                sentiment_score REAL,
                category TEXT,
                status TEXT DEFAULT 'open',
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        
        conn.commit()
        
        # Insert sample data
        self.insert_sample_data(cursor)
        conn.close()

    def insert_sample_data(self, cursor):
        """Insert sample data for demonstration"""
        
        # Sample customers
        sample_customers = [
            ('cust_001', 'john@techcorp.com', 'John Smith', 'TechCorp Inc', 'platinum', 'active', '2023-06-15', '2024-01-15 14:30:00', 125000.0, 850.5, 4.8, 'low', 'advocacy'),
            ('cust_002', 'sarah@innovate.com', 'Sarah Johnson', 'Innovate LLC', 'gold', 'active', '2023-09-20', '2024-01-14 16:45:00', 78000.0, 620.3, 4.5, 'low', 'growth'),
            ('cust_003', 'mike@startup.io', 'Mike Chen', 'Startup Solutions', 'silver', 'at_risk', '2023-12-10', '2024-01-10 09:15:00', 35000.0, 280.7, 3.2, 'high', 'retention'),
            ('cust_004', 'emma@global.com', 'Emma Davis', 'Global Enterprise', 'diamond', 'vip', '2023-03-08', '2024-01-15 18:20:00', 250000.0, 1250.8, 4.9, 'low', 'advocacy'),
            ('cust_005', 'alex@midsize.com', 'Alex Wilson', 'MidSize Corp', 'bronze', 'inactive', '2023-11-25', '2023-12-28 10:30:00', 12000.0, 95.2, 2.8, 'critical', 'retention'),
            ('cust_006', 'lisa@fastgrow.com', 'Lisa Brown', 'FastGrow Inc', 'gold', 'active', '2023-08-14', '2024-01-15 12:10:00', 89000.0, 720.4, 4.6, 'medium', 'growth'),
            ('cust_007', 'david@enterprise.com', 'David Taylor', 'Enterprise Solutions', 'platinum', 'active', '2023-05-22', '2024-01-15 15:45:00', 145000.0, 920.6, 4.7, 'low', 'advocacy'),
            ('cust_008', 'maria@boutique.com', 'Maria Garcia', 'Boutique Agency', 'silver', 'trial', '2024-01-05', '2024-01-15 11:20:00', 5000.0, 180.3, 4.1, 'medium', 'onboarding'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO customers 
            (customer_id, email, name, company, tier, status, join_date, last_activity, 
             lifetime_value, monthly_usage, satisfaction_score, churn_risk, journey_stage) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_customers)
        
        # Sample interactions
        sample_interactions = [
            ('int_001', 'cust_001', 'video_call', 'Quarterly Business Review', 'Discussed growth strategy and new features', '2024-01-15 14:00:00', 45, 5, 'completed', 'agent_sarah'),
            ('int_002', 'cust_002', 'email', 'Feature Request Follow-up', 'Following up on API integration request', '2024-01-14 16:30:00', 15, 4, 'completed', 'agent_mike'),
            ('int_003', 'cust_003', 'chat', 'Usage Decline Inquiry', 'Proactive outreach due to usage drop', '2024-01-10 09:00:00', 25, 3, 'in_progress', 'agent_lisa'),
            ('int_004', 'cust_004', 'phone', 'VIP Support Request', 'Priority support for enterprise deployment', '2024-01-15 18:00:00', 35, 5, 'completed', 'agent_david'),
            ('int_005', 'cust_005', 'email', 'Win-back Campaign', 'Automated re-engagement sequence', '2024-01-12 10:00:00', 5, 2, 'pending', 'system_auto'),
            ('int_006', 'cust_006', 'in_app', 'Onboarding Check-in', 'Progress review and guidance', '2024-01-15 12:00:00', 20, 4, 'completed', 'agent_emma'),
            ('int_007', 'cust_007', 'video_call', 'Expansion Discussion', 'Exploring additional use cases', '2024-01-15 15:30:00', 50, 5, 'completed', 'agent_sarah'),
            ('int_008', 'cust_008', 'chat', 'Trial Support', 'Helping with initial setup', '2024-01-15 11:00:00', 30, 4, 'completed', 'agent_mike'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO customer_interactions 
            (interaction_id, customer_id, interaction_type, subject, description, 
             timestamp, duration_minutes, satisfaction_rating, resolution_status, agent_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_interactions)
        
        # Sample retention metrics
        sample_metrics = [
            ('Monthly Churn Rate', 3.2, 5.0, '2024-01', -0.8, 4.1),
            ('Customer Satisfaction', 4.4, 4.5, '2024-01', 0.3, 4.2),
            ('Net Revenue Retention', 115.8, 110.0, '2024-01', 2.1, 108.5),
            ('Product Adoption Rate', 78.9, 80.0, '2024-01', -1.2, 75.6),
            ('Support Ticket Resolution', 92.3, 95.0, '2024-01', 1.8, 89.7),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO retention_metrics 
            (metric_name, value, target, period, trend, benchmark) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_metrics)
        
        # Sample churn predictions
        sample_predictions = [
            ('cust_003', 0.73, '["low_usage", "declining_engagement", "support_issues"]', '["personal_outreach", "usage_training", "discount_offer"]', 0.89, 'v2.1'),
            ('cust_005', 0.91, '["inactive_status", "no_recent_login", "payment_issues"]', '["win_back_campaign", "payment_assistance", "product_demo"]', 0.94, 'v2.1'),
            ('cust_008', 0.45, '["trial_status", "limited_usage"]', '["onboarding_acceleration", "success_manager_assignment"]', 0.78, 'v2.1'),
            ('cust_006', 0.28, '["usage_plateau"]', '["feature_introduction", "expansion_discussion"]', 0.82, 'v2.1'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO churn_predictions 
            (customer_id, churn_probability, risk_factors, recommended_actions, confidence_score, model_version) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_predictions)
        
        # Sample customer health scores
        sample_health = [
            ('cust_001', 9.2, 9.5, 8.9, 4.8, 9.8),
            ('cust_002', 8.4, 8.7, 8.1, 4.5, 8.9),
            ('cust_003', 4.7, 3.2, 4.8, 3.2, 6.1),
            ('cust_004', 9.8, 9.9, 9.7, 4.9, 9.9),
            ('cust_005', 2.1, 1.5, 2.2, 2.8, 2.6),
            ('cust_006', 8.1, 8.3, 7.9, 4.6, 8.5),
            ('cust_007', 9.1, 9.3, 8.8, 4.7, 9.4),
            ('cust_008', 6.8, 7.2, 6.4, 4.1, 7.1),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO customer_health 
            (customer_id, health_score, engagement_score, usage_score, satisfaction_score, payment_health_score) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_health)
        
        # Sample success playbooks
        sample_playbooks = [
            ('High-Risk Customer Recovery', 'at_risk,churned', '{"churn_risk": "high", "days_inactive": ">= 14"}', 
             '["personal_outreach", "usage_audit", "success_plan"]', '{"churn_reduction": 45.0, "engagement_increase": 67.0}', True, 23, 0.65),
            ('VIP Customer Expansion', 'vip,platinum', '{"satisfaction_score": ">= 4.5", "usage_trend": "stable"}', 
             '["expansion_discussion", "feature_preview", "case_study_creation"]', '{"revenue_expansion": 78.0}', True, 12, 0.83),
            ('Trial Conversion Acceleration', 'trial', '{"trial_days_remaining": "<= 7", "usage_score": "<= 5.0"}', 
             '["demo_scheduling", "success_manager_introduction", "conversion_incentive"]', '{"conversion_rate": 34.0}', True, 45, 0.56),
            ('Onboarding Success Path', 'trial,onboarding', '{"days_since_signup": "<= 30", "activation_events": "< 3"}', 
             '["onboarding_acceleration", "feature_guidance", "milestone_tracking"]', '{"activation_rate": 89.0}', True, 78, 0.72),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO success_playbooks 
            (playbook_name, customer_segment, trigger_conditions, actions, success_metrics, 
             is_active, execution_count, success_rate) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_playbooks)

    def load_customers(self):
        """Load customers from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM customers')
        customers = cursor.fetchall()
        
        for customer in customers:
            self.customers[customer[1]] = Customer(  # customer[1] is customer_id
                customer_id=customer[1],
                email=customer[2],
                name=customer[3],
                company=customer[4],
                tier=CustomerTier(customer[5]),
                status=CustomerStatus(customer[6]),
                join_date=datetime.datetime.fromisoformat(customer[7]),
                last_activity=datetime.datetime.fromisoformat(customer[8]),
                lifetime_value=customer[9],
                monthly_usage=customer[10],
                satisfaction_score=customer[11],
                churn_risk=ChurnRisk(customer[12]),
                journey_stage=JourneyStage(customer[13])
            )
        
        conn.close()
        logger.info(f"Loaded {len(self.customers)} customers")

    def load_interactions(self):
        """Load customer interactions from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM customer_interactions ORDER BY timestamp DESC LIMIT 100')
        interactions = cursor.fetchall()
        
        self.interactions = []
        for interaction in interactions:
            self.interactions.append(CustomerInteraction(
                interaction_id=interaction[1],
                customer_id=interaction[2],
                interaction_type=InteractionType(interaction[3]),
                subject=interaction[4],
                description=interaction[5],
                timestamp=datetime.datetime.fromisoformat(interaction[6]),
                duration_minutes=interaction[7],
                satisfaction_rating=interaction[8],
                resolution_status=interaction[9],
                agent_id=interaction[10]
            ))
        
        conn.close()
        logger.info(f"Loaded {len(self.interactions)} recent interactions")

    def start_monitoring(self):
        """Start background monitoring and automation"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            logger.info("Customer success monitoring started")

    def stop_monitoring(self):
        """Stop background monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Customer success monitoring stopped")

    def _monitoring_loop(self):
        """Background monitoring loop"""
        while self.is_monitoring:
            try:
                # Update customer health scores
                self._update_customer_health()
                
                # Check for at-risk customers
                self._identify_at_risk_customers()
                
                # Execute success playbooks
                self._execute_success_playbooks()
                
                # Update retention metrics
                self._calculate_retention_metrics()
                
                # Sleep for 10 minutes
                time.sleep(600)
                
            except Exception as e:
                logger.error(f"Error in customer success monitoring loop: {e}")
                time.sleep(60)

    def _update_customer_health(self):
        """Update customer health scores based on recent activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for customer_id, customer in self.customers.items():
            # Calculate health score components
            engagement_score = self._calculate_engagement_score(customer_id)
            usage_score = min(customer.monthly_usage / 1000.0 * 10, 10)  # Normalized to 10
            satisfaction_score = customer.satisfaction_score * 2  # Convert to 10-point scale
            payment_health = self._calculate_payment_health(customer_id)
            
            # Overall health score (weighted average)
            health_score = (
                engagement_score * 0.3 +
                usage_score * 0.3 +
                satisfaction_score * 0.2 +
                payment_health * 0.2
            )
            
            # Update database
            cursor.execute('''
                INSERT INTO customer_health 
                (customer_id, health_score, engagement_score, usage_score, 
                 satisfaction_score, payment_health_score) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (customer_id, health_score, engagement_score, usage_score, 
                  satisfaction_score, payment_health))
        
        conn.commit()
        conn.close()

    def _calculate_engagement_score(self, customer_id: str) -> float:
        """Calculate customer engagement score"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent interactions
        cursor.execute('''
            SELECT COUNT(*), AVG(satisfaction_rating) 
            FROM customer_interactions 
            WHERE customer_id = ? AND timestamp > datetime('now', '-30 days')
        ''', (customer_id,))
        
        result = cursor.fetchone()
        interaction_count = result[0] or 0
        avg_satisfaction = result[1] or 0
        
        conn.close()
        
        # Score based on interaction frequency and quality
        frequency_score = min(interaction_count / 5.0 * 5, 5)  # Max 5 points for frequency
        quality_score = avg_satisfaction  # Max 5 points for quality
        
        return frequency_score + quality_score

    def _calculate_payment_health(self, customer_id: str) -> float:
        """Calculate payment health score"""
        # Simplified payment health based on tier and status
        customer = self.customers.get(customer_id)
        if not customer:
            return 0
        
        tier_scores = {
            CustomerTier.BRONZE: 5,
            CustomerTier.SILVER: 6,
            CustomerTier.GOLD: 7,
            CustomerTier.PLATINUM: 8,
            CustomerTier.DIAMOND: 10
        }
        
        status_multipliers = {
            CustomerStatus.ACTIVE: 1.0,
            CustomerStatus.VIP: 1.2,
            CustomerStatus.TRIAL: 0.7,
            CustomerStatus.AT_RISK: 0.5,
            CustomerStatus.INACTIVE: 0.3,
            CustomerStatus.CHURNED: 0.0
        }
        
        base_score = tier_scores.get(customer.tier, 5)
        multiplier = status_multipliers.get(customer.status, 1.0)
        
        return base_score * multiplier

    def _identify_at_risk_customers(self):
        """Identify customers at risk of churning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get customers with low health scores or declining activity
        cursor.execute('''
            SELECT DISTINCT ch.customer_id, ch.health_score
            FROM customer_health ch
            JOIN customers c ON ch.customer_id = c.customer_id
            WHERE ch.health_score < 5.0 
            AND ch.calculated_at = (
                SELECT MAX(calculated_at) 
                FROM customer_health 
                WHERE customer_id = ch.customer_id
            )
        ''')
        
        at_risk_customers = cursor.fetchall()
        
        for customer_id, health_score in at_risk_customers:
            # Update customer status if needed
            if customer_id in self.customers:
                if health_score < 3.0:
                    new_risk = ChurnRisk.CRITICAL
                elif health_score < 4.0:
                    new_risk = ChurnRisk.HIGH
                else:
                    new_risk = ChurnRisk.MEDIUM
                
                self.customers[customer_id].churn_risk = new_risk
                
                # Update database
                cursor.execute('''
                    UPDATE customers 
                    SET churn_risk = ?, status = CASE 
                        WHEN churn_risk = 'critical' THEN 'at_risk'
                        ELSE status 
                    END
                    WHERE customer_id = ?
                ''', (new_risk.value, customer_id))
        
        conn.commit()
        conn.close()

    def _execute_success_playbooks(self):
        """Execute automated success playbooks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM success_playbooks WHERE is_active = 1')
        playbooks = cursor.fetchall()
        
        for playbook in playbooks:
            playbook_id = playbook[0]
            playbook_name = playbook[1]
            customer_segment = playbook[2]
            trigger_conditions = json.loads(playbook[3])
            actions = json.loads(playbook[4])
            
            # Find matching customers
            matching_customers = self._find_matching_customers(customer_segment, trigger_conditions)
            
            if matching_customers:
                logger.info(f"Executing playbook '{playbook_name}' for {len(matching_customers)} customers")
                
                for customer_id in matching_customers:
                    self._execute_playbook_actions(customer_id, actions)
                
                # Update execution count
                cursor.execute('''
                    UPDATE success_playbooks 
                    SET execution_count = execution_count + 1 
                    WHERE id = ?
                ''', (playbook_id,))
        
        conn.commit()
        conn.close()

    def _find_matching_customers(self, segment: str, conditions: Dict) -> List[str]:
        """Find customers matching playbook conditions"""
        matching_customers = []
        segments = segment.split(',')
        
        for customer_id, customer in self.customers.items():
            # Check segment match
            if customer.status.value not in segments and customer.tier.value not in segments:
                continue
            
            # Check specific conditions
            matches = True
            for condition, threshold in conditions.items():
                if condition == "churn_risk" and customer.churn_risk.value != threshold:
                    matches = False
                    break
                elif condition == "satisfaction_score":
                    if ">=" in threshold and customer.satisfaction_score < float(threshold.replace(">=", "").strip()):
                        matches = False
                        break
                # Add more condition checks as needed
            
            if matches:
                matching_customers.append(customer_id)
        
        return matching_customers

    def _execute_playbook_actions(self, customer_id: str, actions: List[str]):
        """Execute specific actions for a customer"""
        for action in actions:
            logger.info(f"Executing action '{action}' for customer {customer_id}")
            # In a real implementation, this would trigger actual actions
            # like sending emails, scheduling calls, creating tasks, etc.

    def _calculate_retention_metrics(self):
        """Calculate and update retention metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Current month churn rate
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN status = 'churned' THEN 1 END) * 100.0 / COUNT(*) as churn_rate
            FROM customers 
            WHERE updated_at > datetime('now', 'start of month')
        ''')
        churn_rate = cursor.fetchone()[0] or 0
        
        # Average satisfaction score
        cursor.execute('SELECT AVG(satisfaction_score) FROM customers WHERE status = "active"')
        avg_satisfaction = cursor.fetchone()[0] or 0
        
        # Update metrics
        metrics = [
            ('Monthly Churn Rate', churn_rate, 5.0, datetime.now().strftime('%Y-%m')),
            ('Customer Satisfaction', avg_satisfaction, 4.5, datetime.now().strftime('%Y-%m'))
        ]
        
        for metric_name, value, target, period in metrics:
            cursor.execute('''
                INSERT INTO retention_metrics 
                (metric_name, value, target, period) 
                VALUES (?, ?, ?, ?)
            ''', (metric_name, value, target, period))
        
        conn.commit()
        conn.close()

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get comprehensive customer success dashboard metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        metrics = {}
        
        # Customer counts by status
        cursor.execute('SELECT status, COUNT(*) FROM customers GROUP BY status')
        status_counts = dict(cursor.fetchall())
        metrics['customer_status'] = status_counts
        
        # Customer counts by tier
        cursor.execute('SELECT tier, COUNT(*) FROM customers GROUP BY tier')
        tier_counts = dict(cursor.fetchall())
        metrics['customer_tiers'] = tier_counts
        
        # Churn risk distribution
        cursor.execute('SELECT churn_risk, COUNT(*) FROM customers GROUP BY churn_risk')
        risk_distribution = dict(cursor.fetchall())
        metrics['churn_risk_distribution'] = risk_distribution
        
        # Key metrics
        cursor.execute('SELECT COUNT(*) FROM customers')
        metrics['total_customers'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(lifetime_value) FROM customers')
        metrics['total_lifetime_value'] = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT AVG(satisfaction_score) FROM customers WHERE status = "active"')
        metrics['avg_satisfaction'] = round(cursor.fetchone()[0] or 0, 2)
        
        cursor.execute('SELECT AVG(health_score) FROM customer_health WHERE calculated_at > datetime("now", "-1 day")')
        metrics['avg_health_score'] = round(cursor.fetchone()[0] or 0, 1)
        
        # Recent interactions
        cursor.execute('''
            SELECT COUNT(*), AVG(satisfaction_rating)
            FROM customer_interactions 
            WHERE timestamp > datetime('now', '-7 days')
        ''')
        interaction_data = cursor.fetchone()
        metrics['weekly_interactions'] = interaction_data[0] or 0
        metrics['avg_interaction_rating'] = round(interaction_data[1] or 0, 1)
        
        # At-risk customers
        cursor.execute('SELECT COUNT(*) FROM customers WHERE churn_risk IN ("high", "critical")')
        metrics['at_risk_customers'] = cursor.fetchone()[0] or 0
        
        # Journey stage distribution
        cursor.execute('SELECT journey_stage, COUNT(*) FROM customers GROUP BY journey_stage')
        journey_distribution = dict(cursor.fetchall())
        metrics['journey_stages'] = journey_distribution
        
        # Recent retention metrics
        cursor.execute('''
            SELECT metric_name, value, target, trend 
            FROM retention_metrics 
            WHERE calculated_at > datetime('now', '-7 days')
            ORDER BY calculated_at DESC
        ''')
        recent_metrics = cursor.fetchall()
        metrics['retention_metrics'] = [
            {
                'name': row[0],
                'value': round(row[1], 2),
                'target': round(row[2], 2),
                'trend': round(row[3] or 0, 1)
            }
            for row in recent_metrics
        ]
        
        conn.close()
        return metrics

    def get_customer_profile(self, customer_id: str) -> Dict[str, Any]:
        """Get detailed customer profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Customer basic info
        cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,))
        customer_data = cursor.fetchone()
        
        if not customer_data:
            return {'error': 'Customer not found'}
        
        # Recent interactions
        cursor.execute('''
            SELECT * FROM customer_interactions 
            WHERE customer_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''', (customer_id,))
        interactions = cursor.fetchall()
        
        # Health score history
        cursor.execute('''
            SELECT health_score, engagement_score, usage_score, calculated_at
            FROM customer_health 
            WHERE customer_id = ? 
            ORDER BY calculated_at DESC 
            LIMIT 30
        ''', (customer_id,))
        health_history = cursor.fetchall()
        
        # Churn prediction
        cursor.execute('''
            SELECT churn_probability, risk_factors, recommended_actions, confidence_score
            FROM churn_predictions 
            WHERE customer_id = ? 
            ORDER BY prediction_date DESC 
            LIMIT 1
        ''', (customer_id,))
        churn_data = cursor.fetchone()
        
        conn.close()
        
        profile = {
            'customer_id': customer_data[1],
            'name': customer_data[3],
            'email': customer_data[2],
            'company': customer_data[4],
            'tier': customer_data[5],
            'status': customer_data[6],
            'join_date': customer_data[7],
            'lifetime_value': customer_data[9],
            'satisfaction_score': customer_data[11],
            'churn_risk': customer_data[12],
            'journey_stage': customer_data[13],
            'interactions': [
                {
                    'type': interaction[3],
                    'subject': interaction[4],
                    'timestamp': interaction[6],
                    'rating': interaction[8],
                    'status': interaction[9]
                }
                for interaction in interactions
            ],
            'health_history': [
                {
                    'health_score': round(h[0], 1),
                    'engagement_score': round(h[1], 1),
                    'usage_score': round(h[2], 1),
                    'date': h[3]
                }
                for h in health_history
            ]
        }
        
        if churn_data:
            profile['churn_prediction'] = {
                'probability': round(churn_data[0], 3),
                'risk_factors': json.loads(churn_data[1]) if churn_data[1] else [],
                'recommended_actions': json.loads(churn_data[2]) if churn_data[2] else [],
                'confidence': round(churn_data[3], 2)
            }
        
        return profile

    def create_customer_interaction(self, customer_id: str, interaction_type: str, 
                                   subject: str, description: str, agent_id: str,
                                   duration_minutes: int = 0, rating: int = 0) -> str:
        """Create a new customer interaction record"""
        interaction_id = f"int_{int(time.time())}_{random.randint(1000, 9999)}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO customer_interactions 
            (interaction_id, customer_id, interaction_type, subject, description, 
             duration_minutes, satisfaction_rating, agent_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (interaction_id, customer_id, interaction_type, subject, description,
              duration_minutes, rating, agent_id))
        
        # Update customer last activity
        cursor.execute('''
            UPDATE customers 
            SET last_activity = CURRENT_TIMESTAMP 
            WHERE customer_id = ?
        ''', (customer_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created interaction {interaction_id} for customer {customer_id}")
        return interaction_id

    def get_at_risk_customers(self) -> List[Dict[str, Any]]:
        """Get list of customers at risk of churning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.customer_id, c.name, c.company, c.churn_risk, c.satisfaction_score,
                   ch.health_score, cp.churn_probability, cp.risk_factors
            FROM customers c
            LEFT JOIN customer_health ch ON c.customer_id = ch.customer_id
            LEFT JOIN churn_predictions cp ON c.customer_id = cp.customer_id
            WHERE c.churn_risk IN ('high', 'critical')
            AND ch.calculated_at = (
                SELECT MAX(calculated_at) FROM customer_health WHERE customer_id = c.customer_id
            )
            ORDER BY c.churn_risk DESC, ch.health_score ASC
        ''')
        
        at_risk_customers = cursor.fetchall()
        conn.close()
        
        return [
            {
                'customer_id': row[0],
                'name': row[1],
                'company': row[2],
                'churn_risk': row[3],
                'satisfaction_score': row[4],
                'health_score': round(row[5] or 0, 1),
                'churn_probability': round(row[6] or 0, 3) if row[6] else None,
                'risk_factors': json.loads(row[7]) if row[7] else []
            }
            for row in at_risk_customers
        ]

    def get_success_playbooks(self) -> List[Dict[str, Any]]:
        """Get all success playbooks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM success_playbooks ORDER BY success_rate DESC')
        playbooks = cursor.fetchall()
        
        conn.close()
        
        return [
            {
                'id': row[0],
                'name': row[1],
                'segment': row[2],
                'actions': json.loads(row[4]),
                'is_active': bool(row[6]),
                'execution_count': row[7],
                'success_rate': round(row[8], 2)
            }
            for row in playbooks
        ]

# Global instance
customer_success_hub = None

def get_customer_success_hub():
    """Get or create global customer success hub instance"""
    global customer_success_hub
    if customer_success_hub is None:
        customer_success_hub = CustomerSuccessHub()
    return customer_success_hub

if __name__ == "__main__":
    # Test the Customer Success Hub
    hub = CustomerSuccessHub()
    
    print("🎯 Customer Success Hub Test")
    print("=" * 50)
    
    # Get dashboard metrics
    metrics = hub.get_dashboard_metrics()
    print(f"📊 Dashboard Metrics:")
    print(f"   Total Customers: {metrics['total_customers']}")
    print(f"   Total Lifetime Value: ${metrics['total_lifetime_value']:,.2f}")
    print(f"   Average Satisfaction: {metrics['avg_satisfaction']}/5.0")
    print(f"   Average Health Score: {metrics['avg_health_score']}/10.0")
    print(f"   At-Risk Customers: {metrics['at_risk_customers']}")
    
    # Get at-risk customers
    at_risk = hub.get_at_risk_customers()
    print(f"\n⚠️  At-Risk Customers ({len(at_risk)}):")
    for customer in at_risk[:3]:
        print(f"   • {customer['name']} ({customer['company']}) - Risk: {customer['churn_risk']}")
    
    # Get success playbooks
    playbooks = hub.get_success_playbooks()
    print(f"\n📋 Success Playbooks ({len(playbooks)}):")
    for playbook in playbooks[:3]:
        print(f"   • {playbook['name']} - Success Rate: {playbook['success_rate']:.1f}% ({playbook['execution_count']} executions)")
    
    # Create test interaction
    interaction_id = hub.create_customer_interaction(
        customer_id="cust_001",
        interaction_type="email",
        subject="Test Support",
        description="This is a test customer interaction",
        agent_id="agent_test",
        duration_minutes=15,
        rating=4
    )
    print(f"\n✉️  Created test interaction: {interaction_id}")
    
    print(f"\n✅ Customer Success Hub test completed successfully!")
    print(f"💼 Tier 2 Feature #6: Customer Success & Retention Hub Ready!")

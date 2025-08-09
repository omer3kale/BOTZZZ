"""
🏪 Enterprise Marketplace & Client Portal
Ultra High-Impact Revenue Generation System

This module provides:
- Multi-tenant SaaS platform with white-label capabilities
- Subscription management with tiered pricing
- Client self-service portal
- Revenue analytics and MRR tracking
- API marketplace for bot services
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib
import secrets
import stripe
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Stripe configuration (demo keys - replace with real keys in production)
stripe.api_key = "sk_test_demo_key_replace_with_real"

class SubscriptionTier(Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional" 
    ENTERPRISE = "enterprise"
    WHITE_LABEL = "white_label"

class ClientStatus(Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"

@dataclass
class PricingPlan:
    tier: SubscriptionTier
    name: str
    monthly_price: float
    yearly_price: float
    bot_limit: int
    campaign_limit: int
    api_calls_limit: int
    features: List[str]
    is_white_label: bool = False

class EnterpriseMarketplace:
    def __init__(self, db_path: str = "../botzzz_marketplace.db"):
        self.db_path = db_path
        self.init_database()
        self.setup_pricing_plans()
        
        logger.info("Enterprise Marketplace initialized")
    
    def init_database(self):
        """Initialize the marketplace database with all required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Clients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id TEXT UNIQUE NOT NULL,
                    company_name TEXT NOT NULL,
                    contact_email TEXT NOT NULL,
                    contact_name TEXT,
                    subscription_tier TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    trial_end_date TEXT,
                    billing_cycle TEXT NOT NULL,
                    monthly_revenue REAL DEFAULT 0,
                    total_revenue REAL DEFAULT 0,
                    api_key TEXT UNIQUE,
                    webhook_url TEXT,
                    white_label_domain TEXT,
                    custom_branding TEXT,
                    metadata TEXT DEFAULT '{}'
                )
            ''')
            
            # Subscriptions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id TEXT NOT NULL,
                    stripe_subscription_id TEXT,
                    plan_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    current_period_start TEXT,
                    current_period_end TEXT,
                    monthly_amount REAL,
                    yearly_amount REAL,
                    created_date TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            ''')
            
            # Revenue tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS revenue_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    stripe_invoice_id TEXT,
                    event_date TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            ''')
            
            # API usage tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id TEXT NOT NULL,
                    endpoint TEXT NOT NULL,
                    calls_count INTEGER DEFAULT 0,
                    usage_date TEXT NOT NULL,
                    response_time_avg REAL,
                    success_rate REAL,
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            ''')
            
            # Marketplace services table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS marketplace_services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    price_model TEXT NOT NULL,
                    base_price REAL NOT NULL,
                    per_call_price REAL DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    features TEXT DEFAULT '[]',
                    created_date TEXT NOT NULL
                )
            ''')
            
            # White-label configurations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS white_label_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id TEXT NOT NULL,
                    domain TEXT,
                    logo_url TEXT,
                    primary_color TEXT,
                    secondary_color TEXT,
                    company_name TEXT,
                    support_email TEXT,
                    custom_css TEXT,
                    features_enabled TEXT DEFAULT '[]',
                    FOREIGN KEY (client_id) REFERENCES clients (client_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Marketplace database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing marketplace database: {e}")
            raise
    
    def setup_pricing_plans(self):
        """Setup the pricing plans for different subscription tiers"""
        self.pricing_plans = {
            SubscriptionTier.STARTER: PricingPlan(
                tier=SubscriptionTier.STARTER,
                name="Starter",
                monthly_price=99.0,
                yearly_price=990.0,
                bot_limit=10,
                campaign_limit=25,
                api_calls_limit=10000,
                features=[
                    "Basic bot management",
                    "Campaign creation",
                    "Analytics dashboard",
                    "Email support"
                ]
            ),
            SubscriptionTier.PROFESSIONAL: PricingPlan(
                tier=SubscriptionTier.PROFESSIONAL,
                name="Professional",
                monthly_price=299.0,
                yearly_price=2990.0,
                bot_limit=50,
                campaign_limit=100,
                api_calls_limit=50000,
                features=[
                    "Advanced bot management",
                    "AI-powered campaigns",
                    "Real-time analytics",
                    "API access",
                    "Priority support",
                    "Custom reporting"
                ]
            ),
            SubscriptionTier.ENTERPRISE: PricingPlan(
                tier=SubscriptionTier.ENTERPRISE,
                name="Enterprise",
                monthly_price=999.0,
                yearly_price=9990.0,
                bot_limit=200,
                campaign_limit=500,
                api_calls_limit=250000,
                features=[
                    "Unlimited bot management",
                    "Advanced AI features",
                    "Custom integrations",
                    "Dedicated account manager",
                    "24/7 support",
                    "SOC 2 compliance",
                    "Custom reporting",
                    "Multi-user access"
                ]
            ),
            SubscriptionTier.WHITE_LABEL: PricingPlan(
                tier=SubscriptionTier.WHITE_LABEL,
                name="White Label",
                monthly_price=2499.0,
                yearly_price=24990.0,
                bot_limit=1000,
                campaign_limit=2000,
                api_calls_limit=1000000,
                features=[
                    "Complete white-label solution",
                    "Custom domain and branding",
                    "Reseller capabilities", 
                    "Revenue sharing",
                    "Custom development",
                    "Dedicated infrastructure",
                    "24/7 premium support"
                ],
                is_white_label=True
            )
        }
    
    def create_client(self, company_name: str, contact_email: str, 
                     contact_name: str, subscription_tier: SubscriptionTier,
                     billing_cycle: str = "monthly") -> str:
        """Create a new client in the marketplace"""
        try:
            client_id = f"client_{secrets.token_hex(8)}"
            api_key = f"sk_live_{secrets.token_hex(24)}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate trial end date (14 days)
            trial_end = datetime.now() + timedelta(days=14)
            
            cursor.execute('''
                INSERT INTO clients (
                    client_id, company_name, contact_email, contact_name,
                    subscription_tier, status, created_date, trial_end_date,
                    billing_cycle, api_key
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                client_id, company_name, contact_email, contact_name,
                subscription_tier.value, ClientStatus.TRIAL.value,
                datetime.now().isoformat(), trial_end.isoformat(),
                billing_cycle, api_key
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Client created: {client_id} - {company_name}")
            return client_id
            
        except Exception as e:
            logger.error(f"Error creating client: {e}")
            raise
    
    def setup_white_label(self, client_id: str, config: Dict[str, Any]) -> bool:
        """Setup white-label configuration for a client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO white_label_configs (
                    client_id, domain, logo_url, primary_color,
                    secondary_color, company_name, support_email,
                    custom_css, features_enabled
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                client_id,
                config.get('domain'),
                config.get('logo_url'),
                config.get('primary_color', '#667eea'),
                config.get('secondary_color', '#764ba2'),
                config.get('company_name'),
                config.get('support_email'),
                config.get('custom_css', ''),
                json.dumps(config.get('features_enabled', []))
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"White-label setup completed for client: {client_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up white-label: {e}")
            return False
    
    def track_revenue_event(self, client_id: str, event_type: str, 
                           amount: float, stripe_invoice_id: str = None) -> bool:
        """Track a revenue event for analytics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO revenue_events (
                    client_id, event_type, amount, stripe_invoice_id, event_date
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                client_id, event_type, amount, stripe_invoice_id,
                datetime.now().isoformat()
            ))
            
            # Update client total revenue
            cursor.execute('''
                UPDATE clients 
                SET total_revenue = total_revenue + ?
                WHERE client_id = ?
            ''', (amount, client_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Revenue event tracked: {client_id} - {event_type} - ${amount}")
            return True
            
        except Exception as e:
            logger.error(f"Error tracking revenue event: {e}")
            return False
    
    def get_mrr_analytics(self) -> Dict[str, Any]:
        """Get Monthly Recurring Revenue analytics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Current MRR
            cursor.execute('''
                SELECT SUM(monthly_revenue) as current_mrr
                FROM clients
                WHERE status = 'active' AND billing_cycle = 'monthly'
            ''')
            monthly_mrr = cursor.fetchone()[0] or 0
            
            # Annual contracts (convert to monthly)
            cursor.execute('''
                SELECT SUM(total_revenue / 12) as annual_mrr
                FROM clients
                WHERE status = 'active' AND billing_cycle = 'yearly'
            ''')
            yearly_mrr = cursor.fetchone()[0] or 0
            
            total_mrr = monthly_mrr + yearly_mrr
            
            # Revenue by tier
            cursor.execute('''
                SELECT subscription_tier, SUM(monthly_revenue), COUNT(*) as clients
                FROM clients
                WHERE status = 'active'
                GROUP BY subscription_tier
            ''')
            revenue_by_tier = {}
            for tier, revenue, count in cursor.fetchall():
                revenue_by_tier[tier] = {
                    'revenue': revenue or 0,
                    'clients': count,
                    'avg_revenue_per_client': (revenue or 0) / count if count > 0 else 0
                }
            
            # Growth metrics
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_clients,
                    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_clients,
                    SUM(CASE WHEN status = 'trial' THEN 1 ELSE 0 END) as trial_clients,
                    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as churned_clients
                FROM clients
            ''')
            metrics = cursor.fetchone()
            
            conn.close()
            
            return {
                'current_mrr': total_mrr,
                'monthly_mrr': monthly_mrr,
                'yearly_mrr': yearly_mrr,
                'revenue_by_tier': revenue_by_tier,
                'total_clients': metrics[0],
                'active_clients': metrics[1],
                'trial_clients': metrics[2],
                'churned_clients': metrics[3],
                'churn_rate': (metrics[3] / metrics[0] * 100) if metrics[0] > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting MRR analytics: {e}")
            return {}
    
    def get_client_dashboard_data(self, client_id: str) -> Dict[str, Any]:
        """Get dashboard data for a specific client"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Client info
            cursor.execute('''
                SELECT * FROM clients WHERE client_id = ?
            ''', (client_id,))
            client_data = cursor.fetchone()
            
            if not client_data:
                return {}
            
            # API usage stats
            cursor.execute('''
                SELECT endpoint, SUM(calls_count) as total_calls
                FROM api_usage
                WHERE client_id = ? AND usage_date >= date('now', '-30 days')
                GROUP BY endpoint
                ORDER BY total_calls DESC
                LIMIT 10
            ''', (client_id,))
            api_usage = cursor.fetchall()
            
            # Revenue history
            cursor.execute('''
                SELECT event_type, amount, event_date
                FROM revenue_events
                WHERE client_id = ?
                ORDER BY event_date DESC
                LIMIT 12
            ''', (client_id,))
            revenue_history = cursor.fetchall()
            
            # Get pricing plan details
            tier = SubscriptionTier(client_data[5])  # subscription_tier column
            pricing_plan = self.pricing_plans.get(tier)
            
            conn.close()
            
            return {
                'client_info': {
                    'client_id': client_data[1],
                    'company_name': client_data[2],
                    'contact_email': client_data[3],
                    'status': client_data[6],
                    'subscription_tier': client_data[5],
                    'created_date': client_data[7],
                    'trial_end_date': client_data[8],
                    'monthly_revenue': client_data[10],
                    'total_revenue': client_data[11]
                },
                'pricing_plan': {
                    'name': pricing_plan.name if pricing_plan else 'Unknown',
                    'bot_limit': pricing_plan.bot_limit if pricing_plan else 0,
                    'campaign_limit': pricing_plan.campaign_limit if pricing_plan else 0,
                    'api_calls_limit': pricing_plan.api_calls_limit if pricing_plan else 0,
                    'features': pricing_plan.features if pricing_plan else []
                },
                'api_usage': [{'endpoint': row[0], 'calls': row[1]} for row in api_usage],
                'revenue_history': [
                    {'type': row[0], 'amount': row[1], 'date': row[2]}
                    for row in revenue_history
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting client dashboard data: {e}")
            return {}
    
    def get_marketplace_services(self) -> List[Dict[str, Any]]:
        """Get all available marketplace services"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM marketplace_services
                WHERE is_active = 1
                ORDER BY category, name
            ''')
            
            services = []
            for row in cursor.fetchall():
                services.append({
                    'service_id': row[1],
                    'name': row[2],
                    'description': row[3],
                    'category': row[4],
                    'price_model': row[5],
                    'base_price': row[6],
                    'per_call_price': row[7],
                    'features': json.loads(row[9]),
                    'created_date': row[10]
                })
            
            conn.close()
            return services
            
        except Exception as e:
            logger.error(f"Error getting marketplace services: {e}")
            return []
    
    def add_marketplace_service(self, name: str, description: str, 
                              category: str, price_model: str, 
                              base_price: float, per_call_price: float = 0,
                              features: List[str] = None) -> str:
        """Add a new service to the marketplace"""
        try:
            service_id = f"svc_{secrets.token_hex(8)}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO marketplace_services (
                    service_id, name, description, category,
                    price_model, base_price, per_call_price,
                    features, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                service_id, name, description, category,
                price_model, base_price, per_call_price,
                json.dumps(features or []), datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Marketplace service added: {service_id} - {name}")
            return service_id
            
        except Exception as e:
            logger.error(f"Error adding marketplace service: {e}")
            raise

# Sample data initialization
def init_sample_data():
    """Initialize the marketplace with sample data"""
    marketplace = EnterpriseMarketplace()
    
    # Add sample services
    services = [
        {
            'name': 'Instagram Growth Bot',
            'description': 'AI-powered Instagram engagement and follower growth',
            'category': 'Social Media Growth',
            'price_model': 'subscription',
            'base_price': 49.99,
            'features': ['Auto-follow', 'Smart engagement', 'Hashtag research', 'Analytics']
        },
        {
            'name': 'Content Generation API',
            'description': 'AI-generated captions, hashtags, and content ideas',
            'category': 'Content Creation',
            'price_model': 'per_call',
            'base_price': 0,
            'per_call_price': 0.05,
            'features': ['GPT-4 powered', 'Brand voice matching', 'Trend analysis']
        },
        {
            'name': 'Advanced Analytics Suite',
            'description': 'Comprehensive social media analytics and reporting',
            'category': 'Analytics',
            'price_model': 'subscription',
            'base_price': 99.99,
            'features': ['Cross-platform tracking', 'Custom reports', 'Competitor analysis']
        }
    ]
    
    for service in services:
        try:
            marketplace.add_marketplace_service(**service)
        except:
            pass  # Service might already exist
    
    # Add sample clients
    sample_clients = [
        {
            'company_name': 'Digital Marketing Pro',
            'contact_email': 'admin@digitalmarketingpro.com',
            'contact_name': 'Sarah Johnson',
            'subscription_tier': SubscriptionTier.PROFESSIONAL
        },
        {
            'company_name': 'Enterprise Solutions Inc',
            'contact_email': 'tech@enterprisesolutions.com',
            'contact_name': 'Michael Chen',
            'subscription_tier': SubscriptionTier.ENTERPRISE
        },
        {
            'company_name': 'Social Growth Agency',
            'contact_email': 'owner@socialgrowth.agency',
            'contact_name': 'Emma Rodriguez',
            'subscription_tier': SubscriptionTier.WHITE_LABEL
        }
    ]
    
    for client_info in sample_clients:
        try:
            client_id = marketplace.create_client(**client_info)
            
            # Add some sample revenue events
            marketplace.track_revenue_event(
                client_id, 
                'subscription_payment',
                marketplace.pricing_plans[client_info['subscription_tier']].monthly_price
            )
        except:
            pass  # Client might already exist
    
    logger.info("Sample marketplace data initialized")

if __name__ == "__main__":
    # Initialize sample data when module is run directly
    init_sample_data()
    
    # Test the marketplace
    marketplace = EnterpriseMarketplace()
    mrr_data = marketplace.get_mrr_analytics()
    print("MRR Analytics:", json.dumps(mrr_data, indent=2))
    
    services = marketplace.get_marketplace_services()
    print(f"Available Services: {len(services)}")
    for service in services:
        print(f"- {service['name']}: ${service['base_price']}")

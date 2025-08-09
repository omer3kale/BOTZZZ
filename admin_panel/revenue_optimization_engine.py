"""
Revenue Optimization Engine
Ultra High-Impact Business Feature - Tier 2 Feature #7

Advanced revenue maximization platform with AI-powered pricing optimization,
intelligent upselling recommendations, conversion rate optimization, and dynamic pricing strategies.
"""

import sqlite3
import json
import datetime
import time
import threading
import random
import math
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PricingStrategy(Enum):
    DYNAMIC = "dynamic"
    COMPETITIVE = "competitive"
    VALUE_BASED = "value_based"
    PENETRATION = "penetration"
    PREMIUM = "premium"
    PSYCHOLOGICAL = "psychological"

class OptimizationType(Enum):
    PRICING = "pricing"
    UPSELLING = "upselling"
    CROSS_SELLING = "cross_selling"
    CONVERSION = "conversion"
    RETENTION = "retention"
    CHURN_PREVENTION = "churn_prevention"

class RevenueMetricType(Enum):
    MRR = "mrr"
    ARR = "arr"
    ARPU = "arpu"
    LTV = "ltv"
    CAC = "cac"
    CHURN_RATE = "churn_rate"
    CONVERSION_RATE = "conversion_rate"
    UPSELL_RATE = "upsell_rate"

class PriceTestStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ANALYZING = "analyzing"

@dataclass
class PricingRecommendation:
    recommendation_id: str
    product_id: str
    current_price: float
    recommended_price: float
    strategy: PricingStrategy
    expected_revenue_lift: float
    confidence_score: float
    reasoning: str
    market_analysis: Dict[str, Any]
    created_at: datetime.datetime

@dataclass
class UpsellOpportunity:
    opportunity_id: str
    customer_id: str
    current_plan: str
    recommended_plan: str
    revenue_potential: float
    success_probability: float
    trigger_events: List[str]
    messaging_strategy: str
    optimal_timing: str
    created_at: datetime.datetime

@dataclass
class RevenueMetric:
    metric_id: str
    metric_type: RevenueMetricType
    value: float
    target: float
    period: str
    growth_rate: float
    benchmark: float
    trend_analysis: Dict[str, Any]
    calculated_at: datetime.datetime

class RevenueOptimizationEngine:
    def __init__(self, db_path: str = "revenue_optimization.db"):
        self.db_path = db_path
        self.pricing_models = {}
        self.optimization_strategies = {}
        self.revenue_metrics = {}
        self.active_tests = {}
        self.is_optimizing = False
        self.optimization_thread = None
        
        # Initialize database
        self.init_database()
        
        # Load existing data
        self.load_pricing_strategies()
        self.load_revenue_metrics()
        
        # Start optimization engine
        self.start_optimization_engine()
        
        logger.info("Revenue Optimization Engine initialized successfully")

    def init_database(self):
        """Initialize the revenue optimization database with proper locking"""
        import time
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                # Use a longer timeout and enable WAL mode for better concurrency
                conn = sqlite3.connect(self.db_path, timeout=30.0)
                conn.execute('PRAGMA journal_mode=WAL')
                conn.execute('PRAGMA busy_timeout=30000')
                cursor = conn.cursor()
                
                # Create tables
                self._create_tables(cursor)
                
                # Check if data exists before inserting samples
                cursor.execute('SELECT COUNT(*) FROM products')
                product_count = cursor.fetchone()[0]
                
                if product_count == 0:
                    self.insert_sample_data(cursor)
                
                conn.commit()
                conn.close()
                print("💰 Revenue Optimization Engine database initialized successfully")
                return
                
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    print(f"Database locked, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    print(f"Failed to initialize revenue optimization database after {max_retries} attempts: {e}")
                    # Create empty database without sample data
                    try:
                        conn = sqlite3.connect(self.db_path, timeout=30.0)
                        conn.execute('PRAGMA journal_mode=WAL')
                        cursor = conn.cursor()
                        self._create_tables(cursor)
                        conn.commit()
                        conn.close()
                        print("💰 Revenue Optimization Engine database initialized (minimal)")
                        return
                    except Exception as final_e:
                        print(f"Critical error: Could not initialize revenue database: {final_e}")
                        return
            except Exception as e:
                print(f"Unexpected error initializing revenue database: {e}")
                return

    def insert_sample_data(self, cursor):
        """Insert sample data for demonstration with better transaction handling"""
        
        # Sample products
        sample_products = [
            ('prod_starter', 'Starter Plan', 'subscription', 29.99, 8.00, 73.3, -1.2, '{"competitor_a": 24.99, "competitor_b": 34.99}', 'dynamic'),
            ('prod_pro', 'Professional Plan', 'subscription', 79.99, 18.00, 77.5, -0.9, '{"competitor_a": 69.99, "competitor_b": 89.99}', 'value_based'),
            ('prod_enterprise', 'Enterprise Plan', 'subscription', 199.99, 45.00, 77.5, -0.6, '{"competitor_a": 179.99, "competitor_b": 249.99}', 'premium'),
            ('prod_addon_analytics', 'Advanced Analytics Add-on', 'addon', 39.99, 5.00, 87.5, -1.5, '{"competitor_a": 29.99, "competitor_b": 49.99}', 'competitive'),
            ('prod_addon_api', 'API Access Add-on', 'addon', 19.99, 2.00, 90.0, -0.8, '{"competitor_a": 15.99, "competitor_b": 24.99}', 'psychological'),
        ]
        
        # Insert products one by one to avoid locking issues
        for product in sample_products:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO products 
                    (product_id, name, category, current_price, cost, margin_percentage, 
                     demand_elasticity, competitor_prices, pricing_strategy) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', product)
            except sqlite3.Error as e:
                print(f"Warning: Could not insert product {product[0]}: {e}")
                continue
        
        # Sample revenue metrics
        current_date = datetime.datetime.now()
        sample_metrics = [
            ('mrr_202408', 'mrr', 125840.50, 150000.00, '2024-08', 12.8, 110000.00, '{"trend": "upward", "seasonal_factor": 1.05}'),
            ('arr_2024', 'arr', 1510086.00, 1800000.00, '2024', 15.2, 1350000.00, '{"trend": "strong_growth", "yoy_growth": 0.152}'),
            ('arpu_202408', 'arpu', 94.50, 110.00, '2024-08', 8.3, 87.20, '{"trend": "improving", "segment_variation": 0.3}'),
            ('ltv_overall', 'ltv', 1285.75, 1500.00, 'overall', 11.4, 1156.00, '{"trend": "positive", "churn_impact": -0.2}'),
            ('cac_202408', 'cac', 78.25, 65.00, '2024-08', -5.8, 83.10, '{"trend": "optimizing", "channel_efficiency": 0.85}'),
            ('churn_rate_202408', 'churn_rate', 3.2, 2.5, '2024-08', -0.8, 4.1, '{"trend": "improving", "cohort_analysis": "stable"}'),
            ('conversion_rate_202408', 'conversion_rate', 18.7, 22.0, '2024-08', 2.3, 16.8, '{"trend": "upward", "funnel_optimization": 0.15}'),
            ('upsell_rate_202408', 'upsell_rate', 24.6, 30.0, '2024-08', 4.1, 21.3, '{"trend": "strong", "success_factors": ["timing", "personalization"]}'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO revenue_metrics 
            (metric_id, metric_type, value, target, period, growth_rate, benchmark, trend_data) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_metrics)
        
        # Sample pricing recommendations
        sample_recommendations = [
            ('rec_001', 'prod_starter', 29.99, 34.99, 'psychological', 18.2, 0.87, 'Price anchoring analysis suggests $34.99 ($35) creates better value perception', '{"market_position": "competitive", "demand_forecast": "elastic"}'),
            ('rec_002', 'prod_pro', 79.99, 89.99, 'value_based', 23.5, 0.91, 'Feature utilization data indicates customers perceive higher value than current price', '{"usage_analysis": "high", "customer_feedback": "positive"}'),
            ('rec_003', 'prod_addon_analytics', 39.99, 44.99, 'competitive', 15.7, 0.82, 'Competitor analysis shows room for premium positioning', '{"competitive_gap": 12.5, "differentiation": "strong"}'),
            ('rec_004', 'prod_enterprise', 199.99, 189.99, 'penetration', -8.1, 0.76, 'Lower price could increase enterprise adoption rate significantly', '{"adoption_barrier": "price_sensitivity", "volume_potential": "high"}'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO pricing_recommendations 
            (recommendation_id, product_id, current_price, recommended_price, strategy, 
             expected_revenue_lift, confidence_score, reasoning, market_analysis) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_recommendations)
        
        # Sample upsell opportunities
        sample_upsells = [
            ('ups_001', 'cust_001', 'Starter Plan', 'Professional Plan', 600.00, 0.78, '["usage_threshold_reached", "feature_request", "team_growth"]', 'Highlight advanced features usage patterns', 'after_3_months'),
            ('ups_002', 'cust_003', 'Professional Plan', 'Enterprise Plan', 1440.00, 0.65, '["api_calls_increasing", "compliance_requirements"]', 'Focus on scalability and enterprise features', 'quarterly_review'),
            ('ups_003', 'cust_005', 'Starter Plan', 'Professional Plan', 600.00, 0.82, '["multiple_projects", "collaboration_needs"]', 'Emphasize team collaboration benefits', 'immediate'),
            ('ups_004', 'cust_007', 'Professional Plan', 'Enterprise Plan + Analytics', 1800.00, 0.73, '["data_export_usage", "reporting_requests"]', 'Advanced analytics value demonstration', 'next_billing_cycle'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO upsell_opportunities 
            (opportunity_id, customer_id, current_plan, recommended_plan, revenue_potential, 
             success_probability, trigger_events, messaging_strategy, optimal_timing) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_upsells)
        
        # Sample A/B price tests
        sample_tests = [
            ('test_001', 'prod_starter', 'Starter Plan Price Test A', 29.99, 34.99, 'active', 0.5, '2024-08-01', '2024-08-31', 156, 142, 4678.44, 4968.58, 0.12, None),
            ('test_002', 'prod_addon_api', 'API Addon Pricing Test', 19.99, 24.99, 'analyzing', 0.5, '2024-07-15', '2024-08-15', 89, 76, 1779.11, 1899.24, 0.95, 'variant'),
            ('test_003', 'prod_pro', 'Professional Plan Bundle Test', 79.99, 89.99, 'completed', 0.4, '2024-07-01', '2024-07-31', 67, 73, 5359.33, 6569.27, 0.89, 'variant'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO price_tests 
            (test_id, product_id, test_name, control_price, variant_price, test_status, 
             traffic_split, start_date, end_date, control_conversions, variant_conversions, 
             control_revenue, variant_revenue, statistical_significance, winner) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_tests)
        
        # Sample customer segments
        sample_segments = [
            ('seg_high_value', 'High Value Customers', '{"ltv": "> 2000", "mrr": "> 150", "tenure": "> 12"}', 234, 2847.50, 189.25, 1.2, 42.8, 0.3),
            ('seg_growth', 'Growth Potential', '{"usage_trend": "increasing", "feature_adoption": "> 70%"}', 567, 945.30, 78.90, 8.5, 28.7, 0.6),
            ('seg_at_risk', 'At Risk Customers', '{"engagement": "declining", "support_tickets": "> 3"}', 123, 567.20, 45.60, 24.8, 12.3, 0.9),
            ('seg_new_users', 'New Users (First 90 Days)', '{"tenure": "< 90", "trial_status": "converted"}', 189, 234.75, 19.50, 12.3, 8.9, 1.2),
            ('seg_enterprise', 'Enterprise Segment', '{"plan": "Enterprise", "seats": "> 50"}', 45, 4567.80, 380.65, 2.1, 67.8, 0.2),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO customer_segments 
            (segment_id, segment_name, criteria, customer_count, average_ltv, average_mrr, 
             churn_rate, upsell_rate, pricing_sensitivity) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_segments)
        
        # Sample optimization campaigns
        sample_campaigns = [
            ('camp_001', 'Q3 Pricing Optimization', 'pricing', 'mrr', 120000.00, 150000.00, 125840.50, 'active', '2024-07-01', '2024-09-30', '["dynamic_pricing", "psychological_pricing"]', '{"tests_running": 3, "recommendations_implemented": 2}', 15.2),
            ('camp_002', 'Upsell Acceleration Campaign', 'upselling', 'upsell_rate', 18.5, 28.0, 24.6, 'active', '2024-08-01', '2024-10-31', '["personalized_messaging", "optimal_timing"]', '{"opportunities_identified": 67, "conversion_rate": 0.36}', 23.8),
            ('camp_003', 'Enterprise Conversion Drive', 'conversion', 'enterprise_conversions', 12, 25, 18, 'active', '2024-07-15', '2024-09-15', '["value_demonstration", "roi_calculator"]', '{"demos_scheduled": 34, "proposals_sent": 19}', 18.7),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO optimization_campaigns 
            (campaign_id, campaign_name, optimization_type, target_metric, baseline_value, 
             target_value, current_value, campaign_status, start_date, end_date, strategies, results, roi) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_campaigns)

    def load_pricing_strategies(self):
        """Load pricing strategies and models"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM pricing_recommendations WHERE status = "pending"')
        recommendations = cursor.fetchall()
        
        self.pricing_models = {}
        for rec in recommendations:
            self.pricing_models[rec[2]] = {  # rec[2] is product_id
                'current_price': rec[3],
                'recommended_price': rec[4],
                'strategy': rec[5],
                'expected_lift': rec[6],
                'confidence': rec[7]
            }
        
        conn.close()
        logger.info(f"Loaded {len(self.pricing_models)} pricing strategies")

    def load_revenue_metrics(self):
        """Load current revenue metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT metric_type, value, target, growth_rate, benchmark 
            FROM revenue_metrics 
            WHERE calculated_at > datetime('now', '-30 days')
        ''')
        metrics = cursor.fetchall()
        
        for metric in metrics:
            self.revenue_metrics[metric[0]] = {
                'value': metric[1],
                'target': metric[2],
                'growth_rate': metric[3],
                'benchmark': metric[4]
            }
        
        conn.close()
        logger.info(f"Loaded {len(self.revenue_metrics)} revenue metrics")

    def start_optimization_engine(self):
        """Start background revenue optimization"""
        if not self.is_optimizing:
            self.is_optimizing = True
            self.optimization_thread = threading.Thread(target=self._optimization_loop)
            self.optimization_thread.daemon = True
            self.optimization_thread.start()
            logger.info("Revenue optimization engine started")

    def stop_optimization_engine(self):
        """Stop background optimization"""
        self.is_optimizing = False
        if self.optimization_thread:
            self.optimization_thread.join(timeout=5)
        logger.info("Revenue optimization engine stopped")

    def _optimization_loop(self):
        """Background optimization loop"""
        while self.is_optimizing:
            try:
                # Update revenue metrics
                self._update_revenue_metrics()
                
                # Analyze pricing opportunities
                self._analyze_pricing_opportunities()
                
                # Identify upsell opportunities
                self._identify_upsell_opportunities()
                
                # Monitor A/B tests
                self._monitor_price_tests()
                
                # Update customer segments
                self._update_customer_segments()
                
                # Sleep for 15 minutes
                time.sleep(900)
                
            except Exception as e:
                logger.error(f"Error in revenue optimization loop: {e}")
                time.sleep(300)

    def _update_revenue_metrics(self):
        """Update revenue metrics with latest calculations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simulate metric updates (in production, this would pull real data)
        current_date = datetime.datetime.now()
        period = current_date.strftime('%Y-%m')
        
        # Calculate simulated MRR growth
        if 'mrr' in self.revenue_metrics:
            current_mrr = self.revenue_metrics['mrr']['value']
            # Simulate 1-3% monthly growth
            growth_rate = random.uniform(0.01, 0.03)
            new_mrr = current_mrr * (1 + growth_rate)
            
            cursor.execute('''
                INSERT INTO revenue_metrics 
                (metric_id, metric_type, value, target, period, growth_rate, benchmark) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (f'mrr_{period}', 'mrr', new_mrr, 150000.00, period, growth_rate * 100, current_mrr))
            
            self.revenue_metrics['mrr']['value'] = new_mrr
            self.revenue_metrics['mrr']['growth_rate'] = growth_rate * 100
        
        # Update other key metrics
        metrics_updates = [
            ('conversion_rate', random.uniform(0.15, 0.25), random.uniform(0.01, 0.05)),
            ('upsell_rate', random.uniform(0.20, 0.35), random.uniform(0.02, 0.08)),
            ('churn_rate', random.uniform(0.02, 0.05), random.uniform(-0.02, 0.01))
        ]
        
        for metric_type, base_value, variance in metrics_updates:
            if metric_type in self.revenue_metrics:
                current_value = self.revenue_metrics[metric_type]['value']
                change = random.uniform(-variance, variance)
                new_value = max(0, current_value + change)
                
                cursor.execute('''
                    INSERT INTO revenue_metrics 
                    (metric_id, metric_type, value, target, period, growth_rate) 
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (f'{metric_type}_{period}', metric_type, new_value, 
                      self.revenue_metrics[metric_type]['target'], period, change))
        
        conn.commit()
        conn.close()

    def _analyze_pricing_opportunities(self):
        """Analyze and generate pricing optimization opportunities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        
        for product in products:
            product_id = product[1]
            current_price = product[3]
            competitor_prices = json.loads(product[8]) if product[8] else {}
            
            # Analyze market position
            if competitor_prices:
                avg_competitor_price = sum(competitor_prices.values()) / len(competitor_prices)
                price_gap = (avg_competitor_price - current_price) / current_price
                
                # Generate recommendation if significant gap exists
                if abs(price_gap) > 0.1:  # More than 10% difference
                    strategy = PricingStrategy.COMPETITIVE if price_gap > 0 else PricingStrategy.PREMIUM
                    recommended_price = current_price * (1 + price_gap * 0.5)  # Move halfway
                    
                    confidence = min(0.9, 0.6 + abs(price_gap))
                    expected_lift = self._calculate_expected_revenue_lift(
                        current_price, recommended_price, product[6]  # demand_elasticity
                    )
                    
                    rec_id = f"rec_{product_id}_{int(time.time())}"
                    
                    cursor.execute('''
                        INSERT INTO pricing_recommendations 
                        (recommendation_id, product_id, current_price, recommended_price, 
                         strategy, expected_revenue_lift, confidence_score, reasoning, market_analysis) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (rec_id, product_id, current_price, recommended_price, 
                          strategy.value, expected_lift, confidence,
                          f"Market analysis suggests {strategy.value} positioning opportunity",
                          json.dumps({"competitor_gap": price_gap, "market_position": "adjustment_needed"})))
        
        conn.commit()
        conn.close()

    def _calculate_expected_revenue_lift(self, current_price: float, new_price: float, elasticity: float) -> float:
        """Calculate expected revenue lift from price change"""
        price_change = (new_price - current_price) / current_price
        demand_change = elasticity * price_change
        revenue_change = (1 + price_change) * (1 + demand_change) - 1
        return revenue_change * 100

    def _identify_upsell_opportunities(self):
        """Identify new upselling opportunities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simulate finding customers ready for upsells
        potential_customers = [
            ('cust_009', 'Starter Plan', 'Professional Plan', 0.79, '["usage_spike", "team_addition"]'),
            ('cust_010', 'Professional Plan', 'Enterprise Plan', 0.67, '["api_usage_increase", "compliance_needs"]'),
            ('cust_011', 'Starter Plan', 'Professional Plan + Analytics', 0.74, '["reporting_requests", "dashboard_usage"]')
        ]
        
        for customer_id, current_plan, recommended_plan, probability, triggers in potential_customers:
            # Calculate revenue potential
            revenue_potential = self._calculate_upsell_revenue_potential(current_plan, recommended_plan)
            
            opportunity_id = f"ups_{customer_id}_{int(time.time())}"
            
            cursor.execute('''
                INSERT INTO upsell_opportunities 
                (opportunity_id, customer_id, current_plan, recommended_plan, 
                 revenue_potential, success_probability, trigger_events, 
                 messaging_strategy, optimal_timing) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (opportunity_id, customer_id, current_plan, recommended_plan,
                  revenue_potential, probability, triggers,
                  self._generate_upsell_messaging(recommended_plan),
                  self._determine_optimal_timing(triggers)))
        
        conn.commit()
        conn.close()

    def _calculate_upsell_revenue_potential(self, current_plan: str, recommended_plan: str) -> float:
        """Calculate revenue potential from upsell"""
        plan_prices = {
            'Starter Plan': 29.99,
            'Professional Plan': 79.99,
            'Enterprise Plan': 199.99,
            'Professional Plan + Analytics': 119.98,
            'Enterprise Plan + Analytics': 239.98
        }
        
        current_price = plan_prices.get(current_plan, 0)
        recommended_price = plan_prices.get(recommended_plan, 0)
        
        return (recommended_price - current_price) * 12  # Annual revenue difference

    def _generate_upsell_messaging(self, recommended_plan: str) -> str:
        """Generate personalized upsell messaging strategy"""
        messaging_strategies = {
            'Professional Plan': 'Highlight team collaboration and advanced features',
            'Enterprise Plan': 'Focus on scalability, security, and enterprise features',
            'Professional Plan + Analytics': 'Emphasize data insights and reporting capabilities',
            'Enterprise Plan + Analytics': 'Comprehensive solution for data-driven enterprises'
        }
        return messaging_strategies.get(recommended_plan, 'Value-based messaging')

    def _determine_optimal_timing(self, triggers: str) -> str:
        """Determine optimal timing for upsell approach"""
        trigger_list = json.loads(triggers)
        
        if 'usage_spike' in trigger_list:
            return 'immediate'
        elif 'team_addition' in trigger_list:
            return 'after_onboarding'
        elif 'compliance_needs' in trigger_list:
            return 'next_billing_cycle'
        else:
            return 'quarterly_review'

    def _monitor_price_tests(self):
        """Monitor and analyze A/B price tests"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM price_tests WHERE test_status = "active"')
        active_tests = cursor.fetchall()
        
        for test in active_tests:
            test_id = test[1]
            control_conversions = test[11]
            variant_conversions = test[12]
            
            # Simulate test progress
            if control_conversions + variant_conversions > 100:  # Minimum sample size
                # Calculate statistical significance
                significance = self._calculate_statistical_significance(
                    control_conversions, variant_conversions, test[9]  # traffic_split
                )
                
                cursor.execute('''
                    UPDATE price_tests 
                    SET statistical_significance = ? 
                    WHERE test_id = ?
                ''', (significance, test_id))
                
                # Determine winner if significant
                if significance > 0.95:
                    control_rate = control_conversions / (control_conversions + variant_conversions)
                    variant_rate = variant_conversions / (control_conversions + variant_conversions)
                    
                    winner = 'variant' if variant_rate > control_rate else 'control'
                    
                    cursor.execute('''
                        UPDATE price_tests 
                        SET test_status = 'analyzing', winner = ? 
                        WHERE test_id = ?
                    ''', (winner, test_id))
        
        conn.commit()
        conn.close()

    def _calculate_statistical_significance(self, control_conv: int, variant_conv: int, split: float) -> float:
        """Calculate statistical significance of A/B test"""
        # Simplified statistical significance calculation
        total_conversions = control_conv + variant_conv
        if total_conversions < 50:
            return 0.0
        
        # Mock calculation - in production, use proper statistical tests
        base_significance = min(0.99, total_conversions / 200.0)
        return base_significance

    def _update_customer_segments(self):
        """Update customer segment analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simulate segment updates
        cursor.execute('SELECT segment_id, customer_count, average_ltv FROM customer_segments')
        segments = cursor.fetchall()
        
        for segment_id, customer_count, avg_ltv in segments:
            # Simulate slight changes in segment metrics
            new_count = max(0, customer_count + random.randint(-5, 10))
            new_ltv = avg_ltv * (1 + random.uniform(-0.05, 0.1))
            
            cursor.execute('''
                UPDATE customer_segments 
                SET customer_count = ?, average_ltv = ? 
                WHERE segment_id = ?
            ''', (new_count, new_ltv, segment_id))
        
        conn.commit()
        conn.close()

    def get_revenue_dashboard_metrics(self) -> Dict[str, Any]:
        """Get comprehensive revenue optimization dashboard metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        metrics = {}
        
        # Current revenue metrics
        cursor.execute('''
            SELECT metric_type, value, target, growth_rate 
            FROM revenue_metrics 
            WHERE calculated_at > datetime('now', '-7 days')
            GROUP BY metric_type 
            HAVING calculated_at = MAX(calculated_at)
        ''')
        current_metrics = cursor.fetchall()
        metrics['current_metrics'] = {
            row[0]: {
                'value': round(row[1], 2),
                'target': round(row[2], 2),
                'growth_rate': round(row[3], 2)
            }
            for row in current_metrics
        }
        
        # Active pricing recommendations
        cursor.execute('''
            SELECT COUNT(*), AVG(expected_revenue_lift), AVG(confidence_score)
            FROM pricing_recommendations 
            WHERE status = 'pending'
        ''')
        rec_data = cursor.fetchone()
        metrics['pricing_recommendations'] = {
            'count': rec_data[0] or 0,
            'avg_expected_lift': round(rec_data[1] or 0, 1),
            'avg_confidence': round(rec_data[2] or 0, 2)
        }
        
        # Active upsell opportunities
        cursor.execute('''
            SELECT COUNT(*), SUM(revenue_potential), AVG(success_probability)
            FROM upsell_opportunities 
            WHERE status = 'active'
        ''')
        upsell_data = cursor.fetchone()
        metrics['upsell_opportunities'] = {
            'count': upsell_data[0] or 0,
            'total_potential': round(upsell_data[1] or 0, 2),
            'avg_probability': round(upsell_data[2] or 0, 2)
        }
        
        # A/B test summary
        cursor.execute('''
            SELECT test_status, COUNT(*), AVG(statistical_significance)
            FROM price_tests 
            GROUP BY test_status
        ''')
        test_summary = cursor.fetchall()
        metrics['ab_tests'] = {
            row[0]: {
                'count': row[1],
                'avg_significance': round(row[2] or 0, 2)
            }
            for row in test_summary
        }
        
        # Customer segments overview
        cursor.execute('''
            SELECT segment_name, customer_count, average_ltv, upsell_rate
            FROM customer_segments 
            ORDER BY average_ltv DESC
        ''')
        segment_data = cursor.fetchall()
        metrics['customer_segments'] = [
            {
                'name': row[0],
                'count': row[1],
                'avg_ltv': round(row[2], 2),
                'upsell_rate': round(row[3], 1)
            }
            for row in segment_data
        ]
        
        # Active optimization campaigns
        cursor.execute('''
            SELECT campaign_name, optimization_type, current_value, target_value, roi
            FROM optimization_campaigns 
            WHERE campaign_status = 'active'
        ''')
        campaign_data = cursor.fetchall()
        metrics['active_campaigns'] = [
            {
                'name': row[0],
                'type': row[1],
                'current': round(row[2], 2),
                'target': round(row[3], 2),
                'roi': round(row[4], 1)
            }
            for row in campaign_data
        ]
        
        # Revenue trends (last 12 months)
        cursor.execute('''
            SELECT period, value
            FROM revenue_metrics 
            WHERE metric_type = 'mrr' 
            ORDER BY calculated_at DESC 
            LIMIT 12
        ''')
        trend_data = cursor.fetchall()
        metrics['revenue_trends'] = [
            {'period': row[0], 'value': round(row[1], 2)}
            for row in trend_data
        ]
        
        conn.close()
        return metrics

    def create_pricing_recommendation(self, product_id: str, strategy: str, 
                                    target_lift: float = None) -> str:
        """Create a new pricing recommendation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current product data
        cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
        product = cursor.fetchone()
        
        if not product:
            conn.close()
            raise ValueError(f"Product {product_id} not found")
        
        current_price = float(product[4])  # current_price column
        elasticity = float(product[7])     # demand_elasticity column
        
        # Calculate recommended price based on strategy
        recommended_price = self._calculate_strategic_price(
            current_price, PricingStrategy(strategy), target_lift or 20.0
        )
        
        expected_lift = self._calculate_expected_revenue_lift(
            current_price, recommended_price, elasticity
        )
        
        recommendation_id = f"rec_{product_id}_{int(time.time())}"
        
        cursor.execute('''
            INSERT INTO pricing_recommendations 
            (recommendation_id, product_id, current_price, recommended_price, 
             strategy, expected_revenue_lift, confidence_score, reasoning, market_analysis) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (recommendation_id, product_id, current_price, recommended_price,
              strategy, expected_lift, 0.85,
              f"Strategic {strategy} pricing recommendation",
              json.dumps({"analysis_type": "strategic", "target_lift": target_lift})))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created pricing recommendation {recommendation_id} for {product_id}")
        return recommendation_id

    def _calculate_strategic_price(self, current_price: float, strategy: PricingStrategy, 
                                 target_lift: float) -> float:
        """Calculate price based on pricing strategy"""
        if strategy == PricingStrategy.PREMIUM:
            return current_price * 1.25
        elif strategy == PricingStrategy.COMPETITIVE:
            return current_price * 0.95
        elif strategy == PricingStrategy.PSYCHOLOGICAL:
            # Price ending in .99 or .95
            base = int(current_price * 1.1)
            return base + 0.99 if base % 10 != 9 else base + 0.95
        elif strategy == PricingStrategy.PENETRATION:
            return current_price * 0.85
        elif strategy == PricingStrategy.VALUE_BASED:
            return current_price * (1 + target_lift / 100)
        else:  # DYNAMIC
            return current_price * random.uniform(1.05, 1.2)

    def create_ab_price_test(self, product_id: str, test_name: str, 
                           variant_price: float, duration_days: int = 30) -> str:
        """Create a new A/B price test"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current product price
        cursor.execute('SELECT current_price FROM products WHERE product_id = ?', (product_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            raise ValueError(f"Product {product_id} not found")
        
        control_price = float(result[0])
        test_id = f"test_{product_id}_{int(time.time())}"
        end_date = datetime.datetime.now() + datetime.timedelta(days=duration_days)
        
        cursor.execute('''
            INSERT INTO price_tests 
            (test_id, product_id, test_name, control_price, variant_price, 
             traffic_split, end_date) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (test_id, product_id, test_name, control_price, variant_price, 0.5, end_date))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created A/B price test {test_id} for {product_id}")
        return test_id

    def get_pricing_recommendations(self, product_id: str = None) -> List[Dict[str, Any]]:
        """Get pricing recommendations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if product_id:
            cursor.execute('''
                SELECT * FROM pricing_recommendations 
                WHERE product_id = ? AND status = 'pending' 
                ORDER BY confidence_score DESC
            ''', (product_id,))
        else:
            cursor.execute('''
                SELECT * FROM pricing_recommendations 
                WHERE status = 'pending' 
                ORDER BY expected_revenue_lift DESC
            ''')
        
        recommendations = cursor.fetchall()
        conn.close()
        
        return [
            {
                'recommendation_id': rec[1],
                'product_id': rec[2],
                'current_price': rec[3],
                'recommended_price': rec[4],
                'strategy': rec[5],
                'expected_lift': round(rec[6], 1),
                'confidence': round(rec[7], 2),
                'reasoning': rec[8],
                'created_at': rec[11]
            }
            for rec in recommendations
        ]

    def get_upsell_opportunities(self, customer_id: str = None) -> List[Dict[str, Any]]:
        """Get upsell opportunities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if customer_id:
            cursor.execute('''
                SELECT * FROM upsell_opportunities 
                WHERE customer_id = ? AND status = 'active'
                ORDER BY success_probability DESC
            ''', (customer_id,))
        else:
            cursor.execute('''
                SELECT * FROM upsell_opportunities 
                WHERE status = 'active' 
                ORDER BY revenue_potential DESC
            ''')
        
        opportunities = cursor.fetchall()
        conn.close()
        
        return [
            {
                'opportunity_id': opp[1],
                'customer_id': opp[2],
                'current_plan': opp[3],
                'recommended_plan': opp[4],
                'revenue_potential': round(opp[5], 2),
                'success_probability': round(opp[6], 2),
                'trigger_events': json.loads(opp[7]) if opp[7] else [],
                'messaging_strategy': opp[8],
                'optimal_timing': opp[9],
                'created_at': opp[12]
            }
            for opp in opportunities
        ]

    def get_ab_test_results(self, test_id: str = None) -> List[Dict[str, Any]]:
        """Get A/B test results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if test_id:
            cursor.execute('SELECT * FROM price_tests WHERE test_id = ?', (test_id,))
        else:
            cursor.execute('SELECT * FROM price_tests ORDER BY created_at DESC LIMIT 10')
        
        tests = cursor.fetchall()
        conn.close()
        
        return [
            {
                'test_id': test[1],
                'product_id': test[2],
                'test_name': test[3],
                'control_price': test[4],
                'variant_price': test[5],
                'status': test[6],
                'control_conversions': test[11],
                'variant_conversions': test[12],
                'control_revenue': round(test[13], 2),
                'variant_revenue': round(test[14], 2),
                'statistical_significance': round(test[15], 2),
                'winner': test[16],
                'created_at': test[18]
            }
            for test in tests
        ]

# Global instance
revenue_optimization_engine = None

def get_revenue_optimization_engine():
    """Get or create global revenue optimization engine instance"""
    global revenue_optimization_engine
    if revenue_optimization_engine is None:
        try:
            revenue_optimization_engine = RevenueOptimizationEngine()
        except Exception as e:
            print(f"Warning: Could not initialize Revenue Optimization Engine: {e}")
            # Return a mock object to prevent crashes
            class MockRevenueEngine:
                def __init__(self):
                    self.active_optimizations = []
                    self.pricing_strategies = {}
                    
                def get_dashboard_data(self):
                    return {
                        'status': 'unavailable',
                        'mrr': 0,
                        'growth_rate': 0,
                        'active_recommendations': 0,
                        'upsell_opportunities': 0
                    }
                    
                def optimize_pricing(self, product_id):
                    return {'status': 'unavailable'}
                    
                def generate_recommendations(self):
                    return []
                    
                def get_upsell_opportunities(self):
                    return []
                    
            revenue_optimization_engine = MockRevenueEngine()
    return revenue_optimization_engine

if __name__ == "__main__":
    # Test the Revenue Optimization Engine
    engine = RevenueOptimizationEngine()
    
    print("💰 Revenue Optimization Engine Test")
    print("=" * 50)
    
    # Get dashboard metrics
    metrics = engine.get_revenue_dashboard_metrics()
    print(f"📊 Dashboard Metrics:")
    
    if 'current_metrics' in metrics and 'mrr' in metrics['current_metrics']:
        mrr_data = metrics['current_metrics']['mrr']
        print(f"   MRR: ${mrr_data['value']:,.2f} (Target: ${mrr_data['target']:,.2f})")
        print(f"   Growth Rate: {mrr_data['growth_rate']:.1f}%")
    
    if 'pricing_recommendations' in metrics:
        rec_data = metrics['pricing_recommendations']
        print(f"   Pricing Recommendations: {rec_data['count']} active")
        print(f"   Avg Expected Lift: {rec_data['avg_expected_lift']:.1f}%")
    
    if 'upsell_opportunities' in metrics:
        upsell_data = metrics['upsell_opportunities']
        print(f"   Upsell Opportunities: {upsell_data['count']} active")
        print(f"   Total Revenue Potential: ${upsell_data['total_potential']:,.2f}")
    
    # Get pricing recommendations
    recommendations = engine.get_pricing_recommendations()
    print(f"\n💡 Top Pricing Recommendations ({len(recommendations)}):")
    for rec in recommendations[:3]:
        print(f"   • {rec['product_id']}: ${rec['current_price']} → ${rec['recommended_price']} ({rec['expected_lift']:.1f}% lift)")
    
    # Get upsell opportunities
    upsells = engine.get_upsell_opportunities()
    print(f"\n🎯 Top Upsell Opportunities ({len(upsells)}):")
    for opp in upsells[:3]:
        print(f"   • {opp['customer_id']}: {opp['current_plan']} → {opp['recommended_plan']} (${opp['revenue_potential']:,.2f} potential)")
    
    # Create test recommendation
    rec_id = engine.create_pricing_recommendation('prod_starter', 'psychological', 15.0)
    print(f"\n💎 Created test pricing recommendation: {rec_id}")
    
    # Create test A/B price test
    test_id = engine.create_ab_price_test('prod_pro', 'Professional Plan Price Optimization', 84.99, 21)
    print(f"\n🧪 Created test A/B price test: {test_id}")
    
    print(f"\n✅ Revenue Optimization Engine test completed successfully!")
    print(f"💼 Tier 2 Feature #7: Revenue Optimization Engine Ready!")

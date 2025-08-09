"""
AI-Powered Bot Management System - BOTZZZ Tier 1 Feature
Intelligent bot orchestration, optimization, and automated decision-making
"""

import json
import time
import random
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import sqlite3
import logging
from enum import Enum
from dataclasses import dataclass, asdict

class BotStatus(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    WARMING = "warming"
    COOLING = "cooling"
    MAINTENANCE = "maintenance"
    SUSPENDED = "suspended"

class Platform(Enum):
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    FACEBOOK = "facebook"

@dataclass
class BotProfile:
    bot_id: str
    platform: Platform
    status: BotStatus
    engagement_rate: float
    success_rate: float
    actions_performed: int
    last_active: datetime
    performance_score: float
    risk_level: str
    assigned_tasks: List[str]
    metadata: Dict[str, Any]

@dataclass
class EngagementTask:
    task_id: str
    platform: Platform
    task_type: str  # like, comment, follow, share
    target_url: str
    priority: int  # 1-10
    estimated_duration: float
    created_at: datetime
    assigned_bot: Optional[str]
    status: str
    metadata: Dict[str, Any]

class AIBotManager:
    """
    Intelligent bot management system with AI-powered optimization
    """
    
    def __init__(self):
        self.bots: Dict[str, BotProfile] = {}
        self.tasks_queue: List[EngagementTask] = []
        self.completed_tasks: List[EngagementTask] = []
        self.ai_db = 'botzzz_ai_management.db'
        self.is_running = False
        self.optimization_interval = 30  # seconds
        
        # AI decision parameters
        self.performance_weights = {
            'engagement_rate': 0.3,
            'success_rate': 0.4,
            'response_time': 0.2,
            'risk_level': 0.1
        }
        
        self.init_database()
        self.generate_sample_bots()
        
    def init_database(self):
        """Initialize AI management database"""
        try:
            with sqlite3.connect(self.ai_db) as conn:
                cursor = conn.cursor()
                
                # Bot profiles table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bot_profiles (
                        bot_id VARCHAR(50) PRIMARY KEY,
                        platform VARCHAR(20),
                        status VARCHAR(20),
                        engagement_rate REAL,
                        success_rate REAL,
                        actions_performed INTEGER,
                        last_active DATETIME,
                        performance_score REAL,
                        risk_level VARCHAR(10),
                        assigned_tasks TEXT,
                        metadata TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tasks table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS engagement_tasks (
                        task_id VARCHAR(50) PRIMARY KEY,
                        platform VARCHAR(20),
                        task_type VARCHAR(30),
                        target_url TEXT,
                        priority INTEGER,
                        estimated_duration REAL,
                        created_at DATETIME,
                        assigned_bot VARCHAR(50),
                        status VARCHAR(20),
                        completed_at DATETIME,
                        metadata TEXT
                    )
                ''')
                
                # Performance history
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bot_performance_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        bot_id VARCHAR(50),
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        engagement_rate REAL,
                        success_rate REAL,
                        actions_count INTEGER,
                        performance_score REAL,
                        notes TEXT
                    )
                ''')
                
                conn.commit()
                logging.info("AI management database initialized")
                
        except Exception as e:
            logging.error(f"Error initializing AI management database: {e}")
    
    def start(self):
        """Start the AI bot management system"""
        if not self.is_running:
            self.is_running = True
            self.management_thread = threading.Thread(target=self._management_loop, daemon=True)
            self.management_thread.start()
            logging.info("AI Bot Management System started")
    
    def stop(self):
        """Stop the AI bot management system"""
        self.is_running = False
        logging.info("AI Bot Management System stopped")
    
    def generate_sample_bots(self):
        """Generate sample bots for demonstration"""
        platforms = list(Platform)
        statuses = [BotStatus.IDLE, BotStatus.ACTIVE, BotStatus.WARMING]
        
        for i in range(20):  # Create 20 sample bots
            bot_id = f"bot_{i+1:03d}"
            platform = random.choice(platforms)
            status = random.choice(statuses)
            
            bot = BotProfile(
                bot_id=bot_id,
                platform=platform,
                status=status,
                engagement_rate=random.uniform(0.02, 0.15),  # 2-15% engagement
                success_rate=random.uniform(0.85, 0.98),  # 85-98% success
                actions_performed=random.randint(50, 5000),
                last_active=datetime.now() - timedelta(minutes=random.randint(1, 1440)),
                performance_score=random.uniform(75, 98),
                risk_level=random.choice(['LOW', 'MEDIUM', 'HIGH']),
                assigned_tasks=[],
                metadata={
                    'created_date': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                    'account_age_days': random.randint(30, 365),
                    'followers_count': random.randint(100, 10000),
                    'last_maintenance': (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat()
                }
            )
            
            self.bots[bot_id] = bot
            self._save_bot_to_db(bot)
    
    def _management_loop(self):
        """Main AI management loop"""
        while self.is_running:
            try:
                self._optimize_bot_assignments()
                self._monitor_bot_performance()
                self._auto_scale_operations()
                self._risk_assessment()
                time.sleep(self.optimization_interval)
            except Exception as e:
                logging.error(f"Error in AI management loop: {e}")
    
    def create_engagement_task(self, platform: Platform, task_type: str, 
                             target_url: str, priority: int = 5) -> str:
        """Create a new engagement task"""
        task_id = f"task_{int(time.time())}_{random.randint(1000, 9999)}"
        
        task = EngagementTask(
            task_id=task_id,
            platform=platform,
            task_type=task_type,
            target_url=target_url,
            priority=priority,
            estimated_duration=self._estimate_task_duration(task_type),
            created_at=datetime.now(),
            assigned_bot=None,
            status="PENDING",
            metadata={}
        )
        
        self.tasks_queue.append(task)
        self._save_task_to_db(task)
        
        # Immediately try to assign the task
        self._assign_task_to_optimal_bot(task)
        
        return task_id
    
    def _estimate_task_duration(self, task_type: str) -> float:
        """Estimate task duration based on type"""
        duration_map = {
            'like': 2.0,      # 2 seconds
            'comment': 15.0,   # 15 seconds
            'follow': 3.0,     # 3 seconds
            'share': 8.0,      # 8 seconds
            'view': 30.0,      # 30 seconds
            'story_view': 5.0  # 5 seconds
        }
        return duration_map.get(task_type, 10.0)
    
    def _assign_task_to_optimal_bot(self, task: EngagementTask) -> Optional[str]:
        """AI-powered task assignment to optimal bot"""
        # Filter bots by platform and availability
        available_bots = [
            bot for bot in self.bots.values()
            if bot.platform == task.platform and 
            bot.status in [BotStatus.IDLE, BotStatus.ACTIVE] and
            len(bot.assigned_tasks) < 5  # Max 5 concurrent tasks
        ]
        
        if not available_bots:
            return None
        
        # AI scoring algorithm for bot selection
        best_bot = None
        best_score = -1
        
        for bot in available_bots:
            score = self._calculate_bot_suitability_score(bot, task)
            if score > best_score:
                best_score = score
                best_bot = bot
        
        if best_bot:
            # Assign task to bot
            best_bot.assigned_tasks.append(task.task_id)
            task.assigned_bot = best_bot.bot_id
            task.status = "ASSIGNED"
            
            # Update database
            self._update_bot_in_db(best_bot)
            self._update_task_in_db(task)
            
            logging.info(f"Task {task.task_id} assigned to bot {best_bot.bot_id} (score: {best_score})")
            return best_bot.bot_id
        
        return None
    
    def _calculate_bot_suitability_score(self, bot: BotProfile, task: EngagementTask) -> float:
        """Calculate AI suitability score for bot-task pairing"""
        # Performance component
        performance_score = (
            bot.engagement_rate * self.performance_weights['engagement_rate'] +
            bot.success_rate * self.performance_weights['success_rate'] +
            (bot.performance_score / 100) * self.performance_weights['response_time']
        )
        
        # Risk penalty
        risk_penalty = {
            'LOW': 0.0,
            'MEDIUM': -0.05,
            'HIGH': -0.15
        }.get(bot.risk_level, 0.0)
        
        # Load balancing (fewer assigned tasks = higher score)
        load_bonus = max(0, (5 - len(bot.assigned_tasks)) / 5 * 0.1)
        
        # Recency bonus (recently active bots get preference)
        time_since_active = (datetime.now() - bot.last_active).total_seconds() / 3600
        recency_bonus = max(0, (24 - time_since_active) / 24 * 0.05)
        
        # Priority multiplier
        priority_multiplier = 1 + (task.priority - 5) * 0.02
        
        final_score = (performance_score + load_bonus + recency_bonus + risk_penalty) * priority_multiplier
        
        return final_score
    
    def _optimize_bot_assignments(self):
        """Continuously optimize bot task assignments"""
        # Reassign tasks from overloaded bots to underutilized ones
        for bot in self.bots.values():
            if len(bot.assigned_tasks) > 3:  # Overloaded
                # Try to redistribute some tasks
                self._redistribute_bot_tasks(bot)
    
    def _redistribute_bot_tasks(self, overloaded_bot: BotProfile):
        """Redistribute tasks from overloaded bot"""
        if len(overloaded_bot.assigned_tasks) > 0:
            task_id = overloaded_bot.assigned_tasks[-1]  # Take last task
            
            # Find the task
            task = next((t for t in self.tasks_queue if t.task_id == task_id), None)
            if task and task.status == "ASSIGNED":
                # Remove from current bot
                overloaded_bot.assigned_tasks.remove(task_id)
                task.assigned_bot = None
                task.status = "PENDING"
                
                # Try to reassign to a better bot
                self._assign_task_to_optimal_bot(task)
    
    def _monitor_bot_performance(self):
        """Monitor and update bot performance metrics"""
        for bot in self.bots.values():
            # Simulate performance updates
            if bot.status == BotStatus.ACTIVE:
                # Slightly adjust performance metrics
                bot.engagement_rate += random.uniform(-0.002, 0.002)
                bot.engagement_rate = max(0.01, min(0.20, bot.engagement_rate))
                
                bot.success_rate += random.uniform(-0.01, 0.01)
                bot.success_rate = max(0.70, min(1.0, bot.success_rate))
                
                # Update performance score
                bot.performance_score = (
                    bot.engagement_rate * 100 * 0.3 +
                    bot.success_rate * 100 * 0.7
                )
                
                # Record performance history
                self._record_performance_history(bot)
    
    def _auto_scale_operations(self):
        """Automatically scale bot operations based on demand"""
        pending_tasks = [t for t in self.tasks_queue if t.status == "PENDING"]
        
        if len(pending_tasks) > 10:  # High demand
            # Activate idle bots
            idle_bots = [b for b in self.bots.values() if b.status == BotStatus.IDLE]
            for bot in idle_bots[:3]:  # Activate up to 3 bots
                bot.status = BotStatus.ACTIVE
                self._update_bot_in_db(bot)
                logging.info(f"Auto-scaled: Activated bot {bot.bot_id}")
        
        elif len(pending_tasks) < 2:  # Low demand
            # Put some active bots to idle
            active_bots = [b for b in self.bots.values() 
                          if b.status == BotStatus.ACTIVE and len(b.assigned_tasks) == 0]
            for bot in active_bots[:2]:  # Idle up to 2 bots
                bot.status = BotStatus.IDLE
                self._update_bot_in_db(bot)
                logging.info(f"Auto-scaled: Idled bot {bot.bot_id}")
    
    def _risk_assessment(self):
        """Continuous risk assessment and mitigation"""
        for bot in self.bots.values():
            risk_score = self._calculate_risk_score(bot)
            
            if risk_score > 0.8:
                bot.risk_level = "HIGH"
                if bot.status == BotStatus.ACTIVE:
                    bot.status = BotStatus.COOLING
                    # Clear assigned tasks
                    bot.assigned_tasks = []
                    self._update_bot_in_db(bot)
                    logging.warning(f"High risk detected: Bot {bot.bot_id} moved to cooling")
            
            elif risk_score > 0.5:
                bot.risk_level = "MEDIUM"
            else:
                bot.risk_level = "LOW"
    
    def _calculate_risk_score(self, bot: BotProfile) -> float:
        """Calculate risk score for a bot"""
        # Factors contributing to risk
        activity_factor = min(1.0, bot.actions_performed / 1000)  # High activity = higher risk
        success_factor = 1.0 - bot.success_rate  # Low success = higher risk
        age_factor = max(0, (30 - bot.metadata.get('account_age_days', 30)) / 30)  # New account = higher risk
        
        risk_score = (activity_factor * 0.4 + success_factor * 0.4 + age_factor * 0.2)
        return min(1.0, risk_score)
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        bot_stats = self._calculate_bot_statistics()
        task_stats = self._calculate_task_statistics()
        performance_trends = self._get_performance_trends()
        
        return {
            'bot_statistics': bot_stats,
            'task_statistics': task_stats,
            'performance_trends': performance_trends,
            'system_health': self._get_system_health(),
            'ai_recommendations': self._generate_ai_recommendations(),
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_bot_statistics(self) -> Dict[str, Any]:
        """Calculate bot statistics"""
        total_bots = len(self.bots)
        active_bots = len([b for b in self.bots.values() if b.status == BotStatus.ACTIVE])
        idle_bots = len([b for b in self.bots.values() if b.status == BotStatus.IDLE])
        
        avg_engagement = sum(b.engagement_rate for b in self.bots.values()) / total_bots
        avg_success = sum(b.success_rate for b in self.bots.values()) / total_bots
        
        platform_distribution = {}
        for platform in Platform:
            platform_distribution[platform.value] = len([
                b for b in self.bots.values() if b.platform == platform
            ])
        
        return {
            'total_bots': total_bots,
            'active_bots': active_bots,
            'idle_bots': idle_bots,
            'avg_engagement_rate': round(avg_engagement, 4),
            'avg_success_rate': round(avg_success, 4),
            'platform_distribution': platform_distribution,
            'risk_distribution': {
                'LOW': len([b for b in self.bots.values() if b.risk_level == 'LOW']),
                'MEDIUM': len([b for b in self.bots.values() if b.risk_level == 'MEDIUM']),
                'HIGH': len([b for b in self.bots.values() if b.risk_level == 'HIGH'])
            }
        }
    
    def _calculate_task_statistics(self) -> Dict[str, Any]:
        """Calculate task statistics"""
        total_tasks = len(self.tasks_queue) + len(self.completed_tasks)
        pending_tasks = len([t for t in self.tasks_queue if t.status == "PENDING"])
        assigned_tasks = len([t for t in self.tasks_queue if t.status == "ASSIGNED"])
        completed_tasks = len(self.completed_tasks)
        
        return {
            'total_tasks': total_tasks,
            'pending_tasks': pending_tasks,
            'assigned_tasks': assigned_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': round(completed_tasks / total_tasks if total_tasks > 0 else 0, 4)
        }
    
    def _get_performance_trends(self) -> List[Dict[str, Any]]:
        """Get performance trends"""
        # This would analyze historical data
        return []
    
    def _get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics"""
        healthy_bots = len([b for b in self.bots.values() if b.risk_level == 'LOW'])
        total_bots = len(self.bots)
        
        health_percentage = (healthy_bots / total_bots * 100) if total_bots > 0 else 0
        
        return {
            'overall_health_percentage': round(health_percentage, 1),
            'healthy_bots': healthy_bots,
            'total_bots': total_bots,
            'system_load': round(len([t for t in self.tasks_queue if t.status != "COMPLETED"]) / 50 * 100, 1)
        }
    
    def _generate_ai_recommendations(self) -> List[Dict[str, str]]:
        """Generate AI-powered recommendations"""
        recommendations = []
        
        # High-risk bot recommendations
        high_risk_bots = [b for b in self.bots.values() if b.risk_level == 'HIGH']
        if len(high_risk_bots) > 3:
            recommendations.append({
                'type': 'WARNING',
                'title': 'High Risk Bot Alert',
                'message': f'{len(high_risk_bots)} bots are at high risk. Consider putting them in maintenance mode.',
                'action': 'Review high-risk bots'
            })
        
        # Performance recommendations
        low_performers = [b for b in self.bots.values() if b.performance_score < 70]
        if len(low_performers) > 5:
            recommendations.append({
                'type': 'OPTIMIZATION',
                'title': 'Performance Optimization',
                'message': f'{len(low_performers)} bots have low performance scores. Consider optimization.',
                'action': 'Optimize bot performance'
            })
        
        # Scaling recommendations
        pending_tasks = len([t for t in self.tasks_queue if t.status == "PENDING"])
        if pending_tasks > 20:
            recommendations.append({
                'type': 'SCALING',
                'title': 'Scale Up Recommendation',
                'message': f'{pending_tasks} tasks are pending. Consider activating more bots.',
                'action': 'Activate idle bots'
            })
        
        return recommendations
    
    # Database operations
    def _save_bot_to_db(self, bot: BotProfile):
        """Save bot profile to database"""
        try:
            with sqlite3.connect(self.ai_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO bot_profiles 
                    (bot_id, platform, status, engagement_rate, success_rate, actions_performed,
                     last_active, performance_score, risk_level, assigned_tasks, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    bot.bot_id, bot.platform.value, bot.status.value,
                    bot.engagement_rate, bot.success_rate, bot.actions_performed,
                    bot.last_active, bot.performance_score, bot.risk_level,
                    json.dumps(bot.assigned_tasks), json.dumps(bot.metadata)
                ))
                conn.commit()
        except Exception as e:
            logging.error(f"Error saving bot to database: {e}")
    
    def _update_bot_in_db(self, bot: BotProfile):
        """Update bot in database"""
        self._save_bot_to_db(bot)
    
    def _save_task_to_db(self, task: EngagementTask):
        """Save task to database"""
        try:
            with sqlite3.connect(self.ai_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO engagement_tasks 
                    (task_id, platform, task_type, target_url, priority, estimated_duration,
                     created_at, assigned_bot, status, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    task.task_id, task.platform.value, task.task_type,
                    task.target_url, task.priority, task.estimated_duration,
                    task.created_at, task.assigned_bot, task.status,
                    json.dumps(task.metadata)
                ))
                conn.commit()
        except Exception as e:
            logging.error(f"Error saving task to database: {e}")
    
    def _update_task_in_db(self, task: EngagementTask):
        """Update task in database"""
        self._save_task_to_db(task)
    
    def _record_performance_history(self, bot: BotProfile):
        """Record bot performance history"""
        try:
            with sqlite3.connect(self.ai_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO bot_performance_history 
                    (bot_id, engagement_rate, success_rate, actions_count, performance_score)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    bot.bot_id, bot.engagement_rate, bot.success_rate,
                    bot.actions_performed, bot.performance_score
                ))
                conn.commit()
        except Exception as e:
            logging.error(f"Error recording performance history: {e}")

# Global AI bot manager instance
ai_bot_manager = AIBotManager()
ai_bot_manager.start()

# Convenience functions
def create_engagement_campaign(platform: str, task_type: str, targets: List[str], priority: int = 5) -> List[str]:
    """Create multiple engagement tasks for a campaign"""
    task_ids = []
    platform_enum = Platform(platform.lower())
    
    for target in targets:
        task_id = ai_bot_manager.create_engagement_task(platform_enum, task_type, target, priority)
        task_ids.append(task_id)
    
    return task_ids

def get_ai_dashboard_data():
    """Get AI management dashboard data"""
    return ai_bot_manager.get_dashboard_data()

def get_bot_performance_report(bot_id: str):
    """Get detailed performance report for a specific bot"""
    if bot_id in ai_bot_manager.bots:
        return asdict(ai_bot_manager.bots[bot_id])
    return None

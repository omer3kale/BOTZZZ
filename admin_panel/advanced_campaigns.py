"""
Advanced Campaign Management System - BOTZZZ Tier 1 Feature
Sophisticated campaign orchestration with targeting, scheduling, and optimization
"""

import json
import time
import uuid
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict, field
import sqlite3
import logging

class CampaignStatus(Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TargetingType(Enum):
    HASHTAG = "hashtag"
    USER_PROFILE = "user_profile"
    COMPETITOR = "competitor"
    LOCATION = "location"
    CUSTOM = "custom"

class EngagementType(Enum):
    LIKES = "likes"
    COMMENTS = "comments"
    FOLLOWS = "follows"
    SHARES = "shares"
    VIEWS = "views"
    STORY_VIEWS = "story_views"

@dataclass
class CampaignTarget:
    target_id: str
    targeting_type: TargetingType
    value: str  # hashtag, username, location, etc.
    weight: float = 1.0  # Importance weight
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EngagementGoal:
    engagement_type: EngagementType
    target_count: int
    daily_limit: int
    priority: int = 5  # 1-10

@dataclass
class Campaign:
    campaign_id: str
    name: str
    description: str
    platform: str
    status: CampaignStatus
    targets: List[CampaignTarget]
    goals: List[EngagementGoal]
    start_date: datetime
    end_date: datetime
    budget_limit: Optional[float]
    created_by: str
    created_at: datetime
    progress: Dict[str, Any] = field(default_factory=dict)
    analytics: Dict[str, Any] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CampaignExecution:
    execution_id: str
    campaign_id: str
    bot_id: str
    target_id: str
    engagement_type: EngagementType
    executed_at: datetime
    success: bool
    result_data: Dict[str, Any]

class AdvancedCampaignManager:
    """
    Enterprise-grade campaign management with AI-powered optimization
    """
    
    def __init__(self):
        self.campaigns: Dict[str, Campaign] = {}
        self.executions: List[CampaignExecution] = []
        self.campaign_db = 'botzzz_campaigns.db'
        self.is_running = False
        self.execution_interval = 10  # seconds
        
        # Performance tracking
        self.performance_metrics = {}
        
        self.init_database()
        self.generate_sample_campaigns()
        
    def init_database(self):
        """Initialize campaign database"""
        try:
            with sqlite3.connect(self.campaign_db) as conn:
                cursor = conn.cursor()
                
                # Campaigns table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS campaigns (
                        campaign_id VARCHAR(50) PRIMARY KEY,
                        name VARCHAR(200),
                        description TEXT,
                        platform VARCHAR(30),
                        status VARCHAR(20),
                        targets TEXT,
                        goals TEXT,
                        start_date DATETIME,
                        end_date DATETIME,
                        budget_limit REAL,
                        created_by VARCHAR(100),
                        created_at DATETIME,
                        progress TEXT,
                        analytics TEXT,
                        settings TEXT
                    )
                ''')
                
                # Campaign executions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS campaign_executions (
                        execution_id VARCHAR(50) PRIMARY KEY,
                        campaign_id VARCHAR(50),
                        bot_id VARCHAR(50),
                        target_id VARCHAR(50),
                        engagement_type VARCHAR(30),
                        executed_at DATETIME,
                        success BOOLEAN,
                        result_data TEXT,
                        FOREIGN KEY (campaign_id) REFERENCES campaigns (campaign_id)
                    )
                ''')
                
                # Campaign analytics table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS campaign_analytics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        campaign_id VARCHAR(50),
                        date DATE,
                        engagement_type VARCHAR(30),
                        target_count INTEGER,
                        achieved_count INTEGER,
                        success_rate REAL,
                        cost REAL,
                        roi REAL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                logging.info("Campaign database initialized")
                
        except Exception as e:
            logging.error(f"Error initializing campaign database: {e}")
    
    def start(self):
        """Start the campaign management system"""
        if not self.is_running:
            self.is_running = True
            self.execution_thread = threading.Thread(target=self._execution_loop, daemon=True)
            self.execution_thread.start()
            logging.info("Advanced Campaign Manager started")
    
    def stop(self):
        """Stop the campaign management system"""
        self.is_running = False
        logging.info("Advanced Campaign Manager stopped")
    
    def create_campaign(self, name: str, description: str, platform: str,
                       targets: List[Dict[str, Any]], goals: List[Dict[str, Any]],
                       start_date: datetime, end_date: datetime,
                       created_by: str, budget_limit: Optional[float] = None,
                       settings: Optional[Dict[str, Any]] = None) -> str:
        """Create a new campaign"""
        
        campaign_id = f"camp_{uuid.uuid4().hex[:12]}"
        
        # Convert targets
        campaign_targets = []
        for target_data in targets:
            target = CampaignTarget(
                target_id=f"tgt_{uuid.uuid4().hex[:8]}",
                targeting_type=TargetingType(target_data['type']),
                value=target_data['value'],
                weight=target_data.get('weight', 1.0),
                metadata=target_data.get('metadata', {})
            )
            campaign_targets.append(target)
        
        # Convert goals
        engagement_goals = []
        for goal_data in goals:
            goal = EngagementGoal(
                engagement_type=EngagementType(goal_data['type']),
                target_count=goal_data['target_count'],
                daily_limit=goal_data['daily_limit'],
                priority=goal_data.get('priority', 5)
            )
            engagement_goals.append(goal)
        
        # Create campaign
        campaign = Campaign(
            campaign_id=campaign_id,
            name=name,
            description=description,
            platform=platform,
            status=CampaignStatus.DRAFT,
            targets=campaign_targets,
            goals=engagement_goals,
            start_date=start_date,
            end_date=end_date,
            budget_limit=budget_limit,
            created_by=created_by,
            created_at=datetime.now(),
            settings=settings or {}
        )
        
        # Initialize progress and analytics
        campaign.progress = {
            goal.engagement_type.value: {
                'target': goal.target_count,
                'achieved': 0,
                'daily_achieved': 0,
                'daily_limit': goal.daily_limit
            }
            for goal in engagement_goals
        }
        
        campaign.analytics = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'success_rate': 0.0,
            'average_engagement_rate': 0.0,
            'cost_spent': 0.0,
            'roi': 0.0
        }
        
        self.campaigns[campaign_id] = campaign
        self._save_campaign_to_db(campaign)
        
        logging.info(f"Campaign created: {campaign_id} - {name}")
        return campaign_id
    
    def launch_campaign(self, campaign_id: str) -> bool:
        """Launch a campaign"""
        if campaign_id not in self.campaigns:
            return False
        
        campaign = self.campaigns[campaign_id]
        if campaign.status != CampaignStatus.DRAFT:
            return False
        
        # Validate campaign
        if not self._validate_campaign(campaign):
            return False
        
        campaign.status = CampaignStatus.SCHEDULED
        self._update_campaign_in_db(campaign)
        
        logging.info(f"Campaign launched: {campaign_id}")
        return True
    
    def pause_campaign(self, campaign_id: str) -> bool:
        """Pause a running campaign"""
        if campaign_id not in self.campaigns:
            return False
        
        campaign = self.campaigns[campaign_id]
        if campaign.status == CampaignStatus.RUNNING:
            campaign.status = CampaignStatus.PAUSED
            self._update_campaign_in_db(campaign)
            logging.info(f"Campaign paused: {campaign_id}")
            return True
        
        return False
    
    def resume_campaign(self, campaign_id: str) -> bool:
        """Resume a paused campaign"""
        if campaign_id not in self.campaigns:
            return False
        
        campaign = self.campaigns[campaign_id]
        if campaign.status == CampaignStatus.PAUSED:
            campaign.status = CampaignStatus.RUNNING
            self._update_campaign_in_db(campaign)
            logging.info(f"Campaign resumed: {campaign_id}")
            return True
        
        return False
    
    def _execution_loop(self):
        """Main campaign execution loop"""
        while self.is_running:
            try:
                self._process_scheduled_campaigns()
                self._execute_running_campaigns()
                self._update_campaign_analytics()
                self._check_campaign_completion()
                time.sleep(self.execution_interval)
            except Exception as e:
                logging.error(f"Error in campaign execution loop: {e}")
    
    def _process_scheduled_campaigns(self):
        """Process campaigns that should start running"""
        current_time = datetime.now()
        
        for campaign in self.campaigns.values():
            if (campaign.status == CampaignStatus.SCHEDULED and 
                campaign.start_date <= current_time):
                campaign.status = CampaignStatus.RUNNING
                self._update_campaign_in_db(campaign)
                logging.info(f"Campaign started: {campaign.campaign_id}")
    
    def _execute_running_campaigns(self):
        """Execute tasks for running campaigns"""
        from ai_bot_manager import ai_bot_manager
        
        current_time = datetime.now()
        
        for campaign in self.campaigns.values():
            if campaign.status != CampaignStatus.RUNNING:
                continue
            
            # Check if campaign should still be running
            if current_time > campaign.end_date:
                campaign.status = CampaignStatus.COMPLETED
                self._update_campaign_in_db(campaign)
                continue
            
            # Execute campaign goals
            self._execute_campaign_goals(campaign)
    
    def _execute_campaign_goals(self, campaign: Campaign):
        """Execute specific campaign goals"""
        from ai_bot_manager import ai_bot_manager, Platform
        
        for goal in campaign.goals:
            progress = campaign.progress[goal.engagement_type.value]
            
            # Check if goal is already achieved
            if progress['achieved'] >= goal.target_count:
                continue
            
            # Check daily limit
            if progress['daily_achieved'] >= goal.daily_limit:
                continue
            
            # Calculate how many executions needed
            remaining = min(
                goal.target_count - progress['achieved'],
                goal.daily_limit - progress['daily_achieved'],
                5  # Max 5 executions per cycle
            )
            
            if remaining <= 0:
                continue
            
            # Select targets for execution
            selected_targets = self._select_targets_for_execution(campaign, goal, remaining)
            
            # Create engagement tasks
            for target in selected_targets:
                try:
                    platform_enum = Platform(campaign.platform.lower())
                    task_id = ai_bot_manager.create_engagement_task(
                        platform_enum,
                        goal.engagement_type.value,
                        target.value,
                        goal.priority
                    )
                    
                    # Record execution
                    execution = CampaignExecution(
                        execution_id=f"exec_{uuid.uuid4().hex[:12]}",
                        campaign_id=campaign.campaign_id,
                        bot_id="pending_assignment",
                        target_id=target.target_id,
                        engagement_type=goal.engagement_type,
                        executed_at=datetime.now(),
                        success=True,  # Assume success for task creation
                        result_data={'task_id': task_id}
                    )
                    
                    self.executions.append(execution)
                    self._save_execution_to_db(execution)
                    
                    # Update progress
                    progress['achieved'] += 1
                    progress['daily_achieved'] += 1
                    
                except Exception as e:
                    logging.error(f"Error executing campaign goal: {e}")
    
    def _select_targets_for_execution(self, campaign: Campaign, goal: EngagementGoal, count: int) -> List[CampaignTarget]:
        """Intelligently select targets for execution"""
        # Weight-based selection
        available_targets = [t for t in campaign.targets if t.weight > 0]
        
        if not available_targets:
            return []
        
        # Sort by weight (descending)
        sorted_targets = sorted(available_targets, key=lambda t: t.weight, reverse=True)
        
        # Select top targets up to count
        return sorted_targets[:count]
    
    def _update_campaign_analytics(self):
        """Update campaign analytics"""
        for campaign in self.campaigns.values():
            if campaign.status in [CampaignStatus.RUNNING, CampaignStatus.COMPLETED]:
                self._calculate_campaign_analytics(campaign)
    
    def _calculate_campaign_analytics(self, campaign: Campaign):
        """Calculate analytics for a campaign"""
        # Get executions for this campaign
        campaign_executions = [e for e in self.executions if e.campaign_id == campaign.campaign_id]
        
        if not campaign_executions:
            return
        
        total_executions = len(campaign_executions)
        successful_executions = len([e for e in campaign_executions if e.success])
        failed_executions = total_executions - successful_executions
        
        success_rate = successful_executions / total_executions if total_executions > 0 else 0.0
        
        # Update campaign analytics
        campaign.analytics.update({
            'total_executions': total_executions,
            'successful_executions': successful_executions,
            'failed_executions': failed_executions,
            'success_rate': round(success_rate, 4),
            'last_updated': datetime.now().isoformat()
        })
        
        self._update_campaign_in_db(campaign)
    
    def _check_campaign_completion(self):
        """Check if campaigns should be completed"""
        current_time = datetime.now()
        
        for campaign in self.campaigns.values():
            if campaign.status == CampaignStatus.RUNNING:
                # Check if end date reached
                if current_time > campaign.end_date:
                    campaign.status = CampaignStatus.COMPLETED
                    self._update_campaign_in_db(campaign)
                    logging.info(f"Campaign completed: {campaign.campaign_id}")
                    continue
                
                # Check if all goals achieved
                all_goals_achieved = True
                for goal in campaign.goals:
                    progress = campaign.progress[goal.engagement_type.value]
                    if progress['achieved'] < goal.target_count:
                        all_goals_achieved = False
                        break
                
                if all_goals_achieved:
                    campaign.status = CampaignStatus.COMPLETED
                    self._update_campaign_in_db(campaign)
                    logging.info(f"Campaign completed (goals achieved): {campaign.campaign_id}")
    
    def _validate_campaign(self, campaign: Campaign) -> bool:
        """Validate campaign configuration"""
        # Check dates
        if campaign.start_date >= campaign.end_date:
            logging.error(f"Invalid dates for campaign {campaign.campaign_id}")
            return False
        
        # Check targets
        if not campaign.targets:
            logging.error(f"No targets for campaign {campaign.campaign_id}")
            return False
        
        # Check goals
        if not campaign.goals:
            logging.error(f"No goals for campaign {campaign.campaign_id}")
            return False
        
        return True
    
    def get_campaign_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive campaign dashboard data"""
        total_campaigns = len(self.campaigns)
        
        status_counts = {}
        for status in CampaignStatus:
            status_counts[status.value] = len([
                c for c in self.campaigns.values() if c.status == status
            ])
        
        # Platform distribution
        platform_distribution = {}
        for campaign in self.campaigns.values():
            platform = campaign.platform
            platform_distribution[platform] = platform_distribution.get(platform, 0) + 1
        
        # Performance metrics
        total_executions = len(self.executions)
        successful_executions = len([e for e in self.executions if e.success])
        success_rate = successful_executions / total_executions if total_executions > 0 else 0.0
        
        # Recent campaigns
        recent_campaigns = sorted(
            self.campaigns.values(),
            key=lambda c: c.created_at,
            reverse=True
        )[:5]
        
        return {
            'summary': {
                'total_campaigns': total_campaigns,
                'status_distribution': status_counts,
                'platform_distribution': platform_distribution,
                'total_executions': total_executions,
                'success_rate': round(success_rate, 4)
            },
            'recent_campaigns': [
                {
                    'campaign_id': c.campaign_id,
                    'name': c.name,
                    'platform': c.platform,
                    'status': c.status.value,
                    'progress': self._calculate_campaign_progress(c),
                    'created_at': c.created_at.isoformat()
                }
                for c in recent_campaigns
            ],
            'performance_trends': self._get_performance_trends(),
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_campaign_progress(self, campaign: Campaign) -> float:
        """Calculate overall campaign progress percentage"""
        if not campaign.goals:
            return 0.0
        
        total_progress = 0.0
        for goal in campaign.goals:
            goal_progress = campaign.progress.get(goal.engagement_type.value, {})
            achieved = goal_progress.get('achieved', 0)
            target = goal_progress.get('target', 1)
            goal_completion = min(100.0, (achieved / target) * 100) if target > 0 else 0.0
            total_progress += goal_completion
        
        return round(total_progress / len(campaign.goals), 1)
    
    def _get_performance_trends(self) -> List[Dict[str, Any]]:
        """Get performance trends over time"""
        # This would analyze historical data
        # For now, return sample trend data
        return [
            {'date': '2025-08-01', 'success_rate': 0.92, 'total_executions': 145},
            {'date': '2025-08-02', 'success_rate': 0.89, 'total_executions': 167},
            {'date': '2025-08-03', 'success_rate': 0.94, 'total_executions': 189},
            {'date': '2025-08-04', 'success_rate': 0.91, 'total_executions': 201},
            {'date': '2025-08-05', 'success_rate': 0.88, 'total_executions': 178},
            {'date': '2025-08-06', 'success_rate': 0.93, 'total_executions': 156}
        ]
    
    def generate_sample_campaigns(self):
        """Generate sample campaigns for demonstration"""
        sample_campaigns = [
            {
                'name': 'Instagram Growth Campaign',
                'description': 'Increase followers and engagement on Instagram',
                'platform': 'instagram',
                'targets': [
                    {'type': 'hashtag', 'value': '#fitness', 'weight': 1.5},
                    {'type': 'hashtag', 'value': '#workout', 'weight': 1.2},
                    {'type': 'user_profile', 'value': '@fitness_influencer', 'weight': 2.0}
                ],
                'goals': [
                    {'type': 'likes', 'target_count': 500, 'daily_limit': 50, 'priority': 7},
                    {'type': 'follows', 'target_count': 100, 'daily_limit': 20, 'priority': 9}
                ],
                'start_date': datetime.now(),
                'end_date': datetime.now() + timedelta(days=7),
                'created_by': 'admin'
            },
            {
                'name': 'YouTube Engagement Boost',
                'description': 'Boost video engagement and subscriber count',
                'platform': 'youtube',
                'targets': [
                    {'type': 'hashtag', 'value': '#tech', 'weight': 1.8},
                    {'type': 'competitor', 'value': '@tech_channel', 'weight': 1.5}
                ],
                'goals': [
                    {'type': 'likes', 'target_count': 300, 'daily_limit': 30, 'priority': 6},
                    {'type': 'comments', 'target_count': 50, 'daily_limit': 10, 'priority': 8}
                ],
                'start_date': datetime.now() + timedelta(hours=2),
                'end_date': datetime.now() + timedelta(days=5),
                'created_by': 'operator'
            },
            {
                'name': 'TikTok Viral Push',
                'description': 'Maximize TikTok video reach and engagement',
                'platform': 'tiktok',
                'targets': [
                    {'type': 'hashtag', 'value': '#viral', 'weight': 2.0},
                    {'type': 'hashtag', 'value': '#trending', 'weight': 1.7}
                ],
                'goals': [
                    {'type': 'likes', 'target_count': 1000, 'daily_limit': 100, 'priority': 10},
                    {'type': 'shares', 'target_count': 200, 'daily_limit': 25, 'priority': 8}
                ],
                'start_date': datetime.now() - timedelta(hours=1),
                'end_date': datetime.now() + timedelta(days=3),
                'created_by': 'admin'
            }
        ]
        
        for campaign_data in sample_campaigns:
            try:
                self.create_campaign(**campaign_data)
            except Exception as e:
                logging.error(f"Error creating sample campaign: {e}")
    
    def _serialize_campaign_data(self, obj):
        """Custom serializer that handles enums"""
        if hasattr(obj, '__dict__'):
            result = {}
            for key, value in obj.__dict__.items():
                if isinstance(value, Enum):
                    result[key] = value.value
                elif isinstance(value, list):
                    result[key] = [self._serialize_campaign_data(item) for item in value]
                elif isinstance(value, dict):
                    result[key] = {k: self._serialize_campaign_data(v) for k, v in value.items()}
                else:
                    result[key] = value
            return result
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, list):
            return [self._serialize_campaign_data(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self._serialize_campaign_data(v) for k, v in obj.items()}
        else:
            return obj

    # Database operations
    def _save_campaign_to_db(self, campaign: Campaign):
        """Save campaign to database"""
        try:
            with sqlite3.connect(self.campaign_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO campaigns 
                    (campaign_id, name, description, platform, status, targets, goals,
                     start_date, end_date, budget_limit, created_by, created_at,
                     progress, analytics, settings)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    campaign.campaign_id, campaign.name, campaign.description,
                    campaign.platform, campaign.status.value,
                    json.dumps([self._serialize_campaign_data(t) for t in campaign.targets]),
                    json.dumps([self._serialize_campaign_data(g) for g in campaign.goals]),
                    campaign.start_date, campaign.end_date, campaign.budget_limit,
                    campaign.created_by, campaign.created_at,
                    json.dumps(campaign.progress),
                    json.dumps(campaign.analytics),
                    json.dumps(campaign.settings)
                ))
                conn.commit()
        except Exception as e:
            logging.error(f"Error saving campaign to database: {e}")
    
    def _update_campaign_in_db(self, campaign: Campaign):
        """Update campaign in database"""
        self._save_campaign_to_db(campaign)
    
    def _save_execution_to_db(self, execution: CampaignExecution):
        """Save execution to database"""
        try:
            with sqlite3.connect(self.campaign_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO campaign_executions 
                    (execution_id, campaign_id, bot_id, target_id, engagement_type,
                     executed_at, success, result_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    execution.execution_id, execution.campaign_id, execution.bot_id,
                    execution.target_id, execution.engagement_type.value,
                    execution.executed_at, execution.success,
                    json.dumps(execution.result_data)
                ))
                conn.commit()
        except Exception as e:
            logging.error(f"Error saving execution to database: {e}")

# Global campaign manager instance
campaign_manager = AdvancedCampaignManager()
campaign_manager.start()

# Convenience functions
def create_quick_campaign(name: str, platform: str, hashtags: List[str], 
                         likes_target: int, follows_target: int = 0) -> str:
    """Create a quick campaign with simple parameters"""
    targets = [{'type': 'hashtag', 'value': f"#{tag}", 'weight': 1.0} for tag in hashtags]
    
    goals = [{'type': 'likes', 'target_count': likes_target, 'daily_limit': likes_target // 7, 'priority': 7}]
    if follows_target > 0:
        goals.append({'type': 'follows', 'target_count': follows_target, 'daily_limit': follows_target // 7, 'priority': 8})
    
    return campaign_manager.create_campaign(
        name=name,
        description=f"Quick campaign for {platform}",
        platform=platform,
        targets=targets,
        goals=goals,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=7),
        created_by="system"
    )

def get_campaign_dashboard_data():
    """Get campaign dashboard data"""
    return campaign_manager.get_campaign_dashboard_data()

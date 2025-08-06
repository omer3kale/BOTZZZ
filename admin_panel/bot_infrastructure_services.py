"""
BOTZZZ Bot Infrastructure Services
=================================

Comprehensive bot limitation solution services including:
- Captcha Solver Services
- Rate Limit Tracker & Bypass
- Proxy Management Systems
- Account Warming Services
- Detection Evasion Tools
- Bot Farm Management
"""

import random
import time
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib
import base64

class CaptchaSolverService:
    """
    Advanced CAPTCHA solving service integration
    Supports multiple providers and challenge types
    """
    
    def __init__(self):
        self.providers = {
            "2captcha": {
                "api_key": "demo_key",
                "base_url": "https://2captcha.com",
                "success_rate": 0.92,
                "avg_solve_time": 35,  # seconds
                "cost_per_captcha": 0.003,  # USD
                "supported_types": ["recaptcha_v2", "recaptcha_v3", "hcaptcha", "funcaptcha", "image_captcha"]
            },
            "anticaptcha": {
                "api_key": "demo_key", 
                "base_url": "https://anti-captcha.com",
                "success_rate": 0.89,
                "avg_solve_time": 42,
                "cost_per_captcha": 0.0025,
                "supported_types": ["recaptcha_v2", "recaptcha_v3", "hcaptcha", "image_captcha"]
            },
            "deathbycaptcha": {
                "api_key": "demo_key",
                "base_url": "https://deathbycaptcha.com",
                "success_rate": 0.85,
                "avg_solve_time": 28,
                "cost_per_captcha": 0.0039,
                "supported_types": ["recaptcha_v2", "image_captcha", "audio_captcha"]
            },
            "captcha_guru": {
                "api_key": "demo_key",
                "base_url": "https://captchaguru.com", 
                "success_rate": 0.94,
                "avg_solve_time": 31,
                "cost_per_captcha": 0.0028,
                "supported_types": ["recaptcha_v2", "recaptcha_v3", "hcaptcha", "funcaptcha"]
            }
        }
        
        self.solve_history = []
        
    def solve_captcha(self, captcha_type: str, site_key: str, page_url: str, provider: str = "auto") -> Dict[str, Any]:
        """
        Solve a CAPTCHA challenge using specified or optimal provider
        """
        if provider == "auto":
            provider = self._select_optimal_provider(captcha_type)
        
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        
        provider_info = self.providers[provider]
        
        # Simulate solving process
        start_time = time.time()
        solve_time = random.normalvariate(provider_info["avg_solve_time"], 8)
        solve_time = max(15, min(120, solve_time))  # Clamp between 15-120 seconds
        
        # Determine success
        success = random.random() < provider_info["success_rate"]
        
        result = {
            "provider": provider,
            "captcha_type": captcha_type,
            "site_key": site_key,
            "page_url": page_url,
            "success": success,
            "solve_time": solve_time,
            "cost": provider_info["cost_per_captcha"] if success else 0,
            "solution": self._generate_solution_token() if success else None,
            "timestamp": datetime.now().isoformat(),
            "error": None if success else "Failed to solve captcha"
        }
        
        self.solve_history.append(result)
        return result
    
    def _select_optimal_provider(self, captcha_type: str) -> str:
        """Select the best provider based on success rate and cost for captcha type"""
        suitable_providers = []
        
        for name, info in self.providers.items():
            if captcha_type in info["supported_types"]:
                # Score based on success rate / cost ratio
                score = info["success_rate"] / info["cost_per_captcha"]
                suitable_providers.append((name, score))
        
        if not suitable_providers:
            return "2captcha"  # Default fallback
        
        # Return highest scoring provider
        return max(suitable_providers, key=lambda x: x[1])[0]
    
    def _generate_solution_token(self) -> str:
        """Generate realistic captcha solution token"""
        token_data = {
            "timestamp": int(time.time()),
            "random": random.randint(100000, 999999)
        }
        token_str = json.dumps(token_data)
        return base64.b64encode(token_str.encode()).decode()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get captcha solving statistics"""
        if not self.solve_history:
            return {"total_attempts": 0}
        
        total = len(self.solve_history)
        successful = sum(1 for r in self.solve_history if r["success"])
        total_cost = sum(r["cost"] for r in self.solve_history)
        avg_solve_time = sum(r["solve_time"] for r in self.solve_history) / total
        
        provider_stats = {}
        for result in self.solve_history:
            provider = result["provider"]
            if provider not in provider_stats:
                provider_stats[provider] = {"attempts": 0, "successes": 0, "cost": 0}
            provider_stats[provider]["attempts"] += 1
            if result["success"]:
                provider_stats[provider]["successes"] += 1
            provider_stats[provider]["cost"] += result["cost"]
        
        return {
            "total_attempts": total,
            "successful_solves": successful,
            "success_rate": successful / total if total > 0 else 0,
            "total_cost": total_cost,
            "average_solve_time": avg_solve_time,
            "cost_per_success": total_cost / successful if successful > 0 else 0,
            "provider_breakdown": provider_stats
        }


class RateLimitTracker:
    """
    Advanced rate limit tracking and bypass system
    Monitors platform limits and manages request timing
    """
    
    def __init__(self):
        # Platform-specific rate limits (realistic values)
        self.platform_limits = {
            "youtube": {
                "views_per_hour": 100,
                "likes_per_hour": 50,
                "comments_per_hour": 25,
                "subscribes_per_hour": 20,
                "daily_watch_time_minutes": 480,
                "detection_threshold": 0.8
            },
            "instagram": {
                "likes_per_hour": 60,
                "follows_per_hour": 30,
                "comments_per_hour": 15,
                "stories_per_hour": 100,
                "posts_per_day": 3,
                "detection_threshold": 0.75
            },
            "tiktok": {
                "likes_per_hour": 200,
                "follows_per_hour": 50,
                "comments_per_hour": 30,
                "shares_per_hour": 40,
                "videos_per_day": 5,
                "detection_threshold": 0.85
            },
            "twitter": {
                "tweets_per_hour": 25,
                "likes_per_hour": 300,
                "retweets_per_hour": 100,
                "follows_per_hour": 40,
                "dm_per_hour": 15,
                "detection_threshold": 0.7
            }
        }
        
        self.account_activity = {}  # Track activity per account
        self.global_limits = {}     # Track global IP/proxy limits
        
    def check_rate_limit(self, platform: str, account_id: str, action: str) -> Dict[str, Any]:
        """
        Check if action is within rate limits
        """
        if platform not in self.platform_limits:
            return {"allowed": False, "error": f"Unknown platform: {platform}"}
        
        current_time = datetime.now()
        limits = self.platform_limits[platform]
        
        # Initialize tracking for account
        if account_id not in self.account_activity:
            self.account_activity[account_id] = {}
        
        if platform not in self.account_activity[account_id]:
            self.account_activity[account_id][platform] = {
                "actions": [],
                "last_reset": current_time,
                "warning_level": 0.0
            }
        
        account_data = self.account_activity[account_id][platform]
        
        # Clean old actions (older than 1 hour)
        cutoff_time = current_time - timedelta(hours=1)
        account_data["actions"] = [
            a for a in account_data["actions"] 
            if datetime.fromisoformat(a["timestamp"]) > cutoff_time
        ]
        
        # Check specific action limit
        limit_key = f"{action}_per_hour"
        if limit_key not in limits:
            return {"allowed": False, "error": f"Unknown action: {action}"}
        
        action_limit = limits[limit_key]
        recent_actions = [
            a for a in account_data["actions"] 
            if a["action"] == action
        ]
        
        current_count = len(recent_actions)
        utilization = current_count / action_limit
        
        # Calculate risk factors
        risk_factors = self._calculate_risk_factors(account_data, limits, current_time)
        
        # Determine if action should be allowed
        allowed = current_count < action_limit and risk_factors["total_risk"] < limits["detection_threshold"]
        
        # Calculate recommended delay
        recommended_delay = self._calculate_optimal_delay(recent_actions, action_limit, risk_factors)
        
        result = {
            "allowed": allowed,
            "current_count": current_count,
            "limit": action_limit,
            "utilization": utilization,
            "risk_factors": risk_factors,
            "recommended_delay": recommended_delay,
            "reset_time": (current_time + timedelta(hours=1)).isoformat(),
            "warning_level": account_data["warning_level"]
        }
        
        # If allowed, record the action
        if allowed:
            account_data["actions"].append({
                "action": action,
                "timestamp": current_time.isoformat(),
                "risk_score": risk_factors["total_risk"]
            })
        
        return result
    
    def _calculate_risk_factors(self, account_data: Dict, limits: Dict, current_time: datetime) -> Dict[str, float]:
        """Calculate various risk factors for detection"""
        
        actions = account_data["actions"]
        if not actions:
            return {"total_risk": 0.0, "timing_risk": 0.0, "volume_risk": 0.0, "pattern_risk": 0.0}
        
        # Timing risk - too consistent intervals
        timing_risk = 0.0
        if len(actions) >= 3:
            intervals = []
            for i in range(1, len(actions)):
                prev_time = datetime.fromisoformat(actions[i-1]["timestamp"])
                curr_time = datetime.fromisoformat(actions[i]["timestamp"])
                intervals.append((curr_time - prev_time).total_seconds())
            
            if intervals:
                # High consistency in timing is risky
                avg_interval = sum(intervals) / len(intervals)
                variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)
                consistency = 1.0 / (1.0 + variance / (avg_interval ** 2)) if avg_interval > 0 else 0
                timing_risk = consistency * 0.4  # Max 40% risk from timing
        
        # Volume risk - too many actions too quickly
        recent_actions = len([a for a in actions if datetime.fromisoformat(a["timestamp"]) > current_time - timedelta(minutes=10)])
        volume_risk = min(recent_actions / 10, 1.0) * 0.3  # Max 30% risk from volume
        
        # Pattern risk - predictable behavior
        action_types = [a["action"] for a in actions[-10:]]  # Last 10 actions
        unique_actions = len(set(action_types))
        pattern_risk = (1.0 - unique_actions / max(len(action_types), 1)) * 0.3  # Max 30% risk from patterns
        
        total_risk = min(timing_risk + volume_risk + pattern_risk, 1.0)
        
        # Update warning level
        account_data["warning_level"] = total_risk
        
        return {
            "total_risk": total_risk,
            "timing_risk": timing_risk,
            "volume_risk": volume_risk,
            "pattern_risk": pattern_risk
        }
    
    def _calculate_optimal_delay(self, recent_actions: List, action_limit: int, risk_factors: Dict) -> int:
        """Calculate optimal delay between actions to avoid detection"""
        
        if not recent_actions:
            return random.randint(30, 120)  # Initial delay
        
        # Base delay calculation
        base_delay = 3600 / action_limit  # Spread evenly across hour
        
        # Adjust based on risk
        risk_multiplier = 1.0 + (risk_factors["total_risk"] * 3)  # 1x to 4x multiplier
        
        # Add randomness to avoid pattern detection  
        randomization = random.uniform(0.7, 1.3)
        
        optimal_delay = int(base_delay * risk_multiplier * randomization)
        
        return max(30, min(1800, optimal_delay))  # Clamp between 30 seconds and 30 minutes
    
    def get_account_status(self, account_id: str) -> Dict[str, Any]:
        """Get comprehensive status for an account across all platforms"""
        if account_id not in self.account_activity:
            return {"account_id": account_id, "status": "inactive", "platforms": {}}
        
        account_data = self.account_activity[account_id]
        platform_status = {}
        
        for platform, data in account_data.items():
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(hours=1)
            
            recent_actions = [
                a for a in data["actions"] 
                if datetime.fromisoformat(a["timestamp"]) > cutoff_time
            ]
            
            action_breakdown = {}
            for action in recent_actions:
                action_type = action["action"]
                if action_type not in action_breakdown:
                    action_breakdown[action_type] = 0
                action_breakdown[action_type] += 1
            
            platform_status[platform] = {
                "recent_actions": len(recent_actions),
                "warning_level": data["warning_level"],
                "action_breakdown": action_breakdown,
                "last_activity": max([a["timestamp"] for a in recent_actions]) if recent_actions else "never"
            }
        
        overall_risk = max([data["warning_level"] for data in account_data.values()]) if account_data else 0
        
        return {
            "account_id": account_id,
            "overall_risk": overall_risk,
            "status": "high_risk" if overall_risk > 0.8 else "medium_risk" if overall_risk > 0.5 else "safe",
            "platforms": platform_status
        }


class ProxyManager:
    """
    Comprehensive proxy management system
    Handles rotation, health checking, and geographic distribution
    """
    
    def __init__(self):
        self.proxy_pools = {
            "residential": {
                "providers": ["luminati", "smartproxy", "oxylabs", "geosurf"],
                "cost_per_gb": 15.0,
                "success_rate": 0.94,
                "avg_speed": 45,  # Mbps
                "detection_rate": 0.05
            },
            "datacenter": {
                "providers": ["blazingseollc", "myprivateproxy", "instantproxies"],
                "cost_per_proxy": 2.50,
                "success_rate": 0.87,
                "avg_speed": 180,  # Mbps  
                "detection_rate": 0.25
            },
            "mobile": {
                "providers": ["airproxy", "mobileproxy_space", "proxy_seller"],
                "cost_per_gb": 25.0,
                "success_rate": 0.91,
                "avg_speed": 28,  # Mbps
                "detection_rate": 0.08
            }
        }
        
        self.active_proxies = []
        self.proxy_health = {}
        self.rotation_history = []
        
        # Initialize some demo proxies
        self._initialize_demo_proxies()
    
    def _initialize_demo_proxies(self):
        """Initialize demo proxy pool"""
        regions = ["US-East", "US-West", "EU-West", "EU-East", "Asia-Pacific", "South-America"]
        
        for i in range(50):
            proxy_type = random.choice(["residential", "datacenter", "mobile"])
            region = random.choice(regions)
            
            proxy = {
                "id": f"proxy_{i+1:03d}",
                "type": proxy_type,
                "ip": f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
                "port": random.randint(8000, 9999),
                "region": region,
                "provider": random.choice(self.proxy_pools[proxy_type]["providers"]),
                "health_score": random.uniform(0.7, 1.0),
                "last_used": None,
                "usage_count": 0,
                "detected": False,
                "created_at": datetime.now() - timedelta(days=random.randint(1, 90))
            }
            
            self.active_proxies.append(proxy)
            self.proxy_health[proxy["id"]] = proxy["health_score"]
    
    def get_optimal_proxy(self, platform: str, region_preference: str = None, avoid_detected: bool = True) -> Dict[str, Any]:
        """
        Get optimal proxy based on platform requirements and preferences
        """
        available_proxies = [p for p in self.active_proxies if not (avoid_detected and p["detected"])]
        
        if region_preference:
            available_proxies = [p for p in available_proxies if p["region"] == region_preference]
        
        if not available_proxies:
            return {"error": "No suitable proxies available"}
        
        # Score proxies based on multiple factors
        scored_proxies = []
        for proxy in available_proxies:
            score = self._calculate_proxy_score(proxy, platform)
            scored_proxies.append((proxy, score))
        
        # Select best proxy
        best_proxy = max(scored_proxies, key=lambda x: x[1])[0]
        
        # Update usage
        best_proxy["last_used"] = datetime.now().isoformat()
        best_proxy["usage_count"] += 1
        
        # Record rotation
        self.rotation_history.append({
            "proxy_id": best_proxy["id"],
            "platform": platform,
            "timestamp": datetime.now().isoformat(),
            "reason": "optimal_selection"
        })
        
        return {
            "proxy": best_proxy,
            "connection_string": f"{best_proxy['ip']}:{best_proxy['port']}",
            "recommended_usage_duration": random.randint(300, 1800),  # 5-30 minutes
            "estimated_success_rate": self.proxy_pools[best_proxy["type"]]["success_rate"]
        }
    
    def _calculate_proxy_score(self, proxy: Dict, platform: str) -> float:
        """Calculate suitability score for proxy"""
        base_score = proxy["health_score"]
        
        # Prefer less used proxies
        usage_penalty = min(proxy["usage_count"] / 100, 0.3)
        
        # Prefer recently created proxies (fresher)
        age_days = (datetime.now() - datetime.fromisoformat(proxy["created_at"].isoformat())).days
        age_penalty = min(age_days / 365, 0.2)  # Max 20% penalty for old proxies
        
        # Type suitability for platform
        type_bonus = 0.0
        if platform in ["youtube", "instagram"] and proxy["type"] == "residential":
            type_bonus = 0.2
        elif platform in ["tiktok", "twitter"] and proxy["type"] == "mobile":
            type_bonus = 0.15
        
        final_score = base_score - usage_penalty - age_penalty + type_bonus
        return max(0.1, min(1.0, final_score))
    
    def rotate_proxy(self, current_proxy_id: str, reason: str = "scheduled_rotation") -> Dict[str, Any]:
        """
        Rotate to a new proxy, avoiding the current one
        """
        current_proxy = next((p for p in self.active_proxies if p["id"] == current_proxy_id), None)
        if not current_proxy:
            return {"error": "Current proxy not found"}
        
        # Get new proxy from different provider/region if possible
        avoid_criteria = {
            "provider": current_proxy["provider"],
            "region": current_proxy["region"]
        }
        
        available_proxies = [
            p for p in self.active_proxies 
            if p["id"] != current_proxy_id and 
               not p["detected"] and
               (p["provider"] != avoid_criteria["provider"] or p["region"] != avoid_criteria["region"])
        ]
        
        if not available_proxies:
            # Fallback to any available proxy
            available_proxies = [p for p in self.active_proxies if p["id"] != current_proxy_id and not p["detected"]]
        
        if not available_proxies:
            return {"error": "No alternative proxies available"}
        
        # Select new proxy with highest health score
        new_proxy = max(available_proxies, key=lambda p: p["health_score"])
        
        # Update usage
        new_proxy["last_used"] = datetime.now().isoformat()
        new_proxy["usage_count"] += 1
        
        # Record rotation
        self.rotation_history.append({
            "from_proxy": current_proxy_id,
            "to_proxy": new_proxy["id"],
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "new_proxy": new_proxy,
            "connection_string": f"{new_proxy['ip']}:{new_proxy['port']}",
            "rotation_reason": reason
        }
    
    def mark_proxy_detected(self, proxy_id: str, platform: str, detection_type: str):
        """Mark a proxy as detected by platform"""
        proxy = next((p for p in self.active_proxies if p["id"] == proxy_id), None)
        if proxy:
            proxy["detected"] = True
            proxy["detection_info"] = {
                "platform": platform,
                "type": detection_type,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_proxy_statistics(self) -> Dict[str, Any]:
        """Get comprehensive proxy pool statistics"""
        total_proxies = len(self.active_proxies)
        active_proxies = len([p for p in self.active_proxies if not p["detected"]])
        detected_proxies = total_proxies - active_proxies
        
        # Type distribution
        type_distribution = {}
        for proxy in self.active_proxies:
            proxy_type = proxy["type"]
            if proxy_type not in type_distribution:
                type_distribution[proxy_type] = {"total": 0, "active": 0}
            type_distribution[proxy_type]["total"] += 1
            if not proxy["detected"]:
                type_distribution[proxy_type]["active"] += 1
        
        # Region distribution
        region_distribution = {}
        for proxy in self.active_proxies:
            region = proxy["region"]
            if region not in region_distribution:
                region_distribution[region] = {"total": 0, "active": 0}
            region_distribution[region]["total"] += 1
            if not proxy["detected"]:
                region_distribution[region]["active"] += 1
        
        # Health statistics
        health_scores = [p["health_score"] for p in self.active_proxies if not p["detected"]]
        avg_health = sum(health_scores) / len(health_scores) if health_scores else 0
        
        return {
            "total_proxies": total_proxies,
            "active_proxies": active_proxies,
            "detected_proxies": detected_proxies,
            "detection_rate": detected_proxies / total_proxies if total_proxies > 0 else 0,
            "average_health": avg_health,
            "type_distribution": type_distribution,
            "region_distribution": region_distribution,
            "recent_rotations": len([r for r in self.rotation_history if datetime.fromisoformat(r["timestamp"]) > datetime.now() - timedelta(hours=24)])
        }


class AccountWarmingService:
    """
    Automated account warming and reputation building service
    Gradually builds account credibility to avoid detection
    """
    
    def __init__(self):
        self.warming_stages = {
            "stage_1_registration": {
                "duration_days": (1, 3),
                "activities": ["profile_setup", "basic_browsing"],
                "daily_actions": (5, 15),
                "human_behavior_score": 0.95,
                "description": "Initial account setup and basic activity"
            },
            "stage_2_exploration": {
                "duration_days": (3, 7),
                "activities": ["content_consumption", "light_engagement"],
                "daily_actions": (15, 35),
                "human_behavior_score": 0.90,
                "description": "Exploring platform, consuming content, occasional likes"
            },
            "stage_3_engagement": {
                "duration_days": (7, 14),
                "activities": ["commenting", "following", "sharing"],
                "daily_actions": (25, 60),
                "human_behavior_score": 0.85,
                "description": "Increased engagement, building social connections"
            },
            "stage_4_active_user": {
                "duration_days": (14, 30),
                "activities": ["content_creation", "community_participation"],
                "daily_actions": (40, 100),
                "human_behavior_score": 0.80,
                "description": "Active participation, content creation"
            },
            "stage_5_established": {
                "duration_days": None,  # Ongoing
                "activities": ["full_engagement", "bot_activities"],
                "daily_actions": (50, 200),
                "human_behavior_score": 0.75,
                "description": "Fully warmed account ready for bot operations"
            }
        }
        
        self.warming_accounts = {}
    
    def start_account_warming(self, account_id: str, platform: str, target_stage: str = "stage_5_established") -> Dict[str, Any]:
        """
        Start automated account warming process
        """
        if account_id in self.warming_accounts:
            return {"error": "Account already in warming process"}
        
        warming_plan = self._create_warming_plan(platform, target_stage)
        
        account_warming = {
            "account_id": account_id,
            "platform": platform,
            "target_stage": target_stage,
            "current_stage": "stage_1_registration",
            "start_date": datetime.now(),
            "plan": warming_plan,
            "completed_activities": [],
            "daily_activity_log": [],
            "reputation_score": 0.1,  # Starting reputation
            "detection_risk": 0.95,   # High risk initially
            "estimated_completion": self._calculate_completion_date(warming_plan)
        }
        
        self.warming_accounts[account_id] = account_warming
        
        return {
            "account_id": account_id,
            "warming_started": True,
            "estimated_duration": len(warming_plan),
            "target_stage": target_stage,
            "estimated_completion": account_warming["estimated_completion"]
        }
    
    def _create_warming_plan(self, platform: str, target_stage: str) -> List[Dict]:
        """Create detailed day-by-day warming plan"""
        plan = []
        current_date = datetime.now()
        
        stages_to_complete = []
        for stage_name in self.warming_stages.keys():
            stages_to_complete.append(stage_name)
            if stage_name == target_stage:
                break
        
        for stage_name in stages_to_complete:
            stage = self.warming_stages[stage_name]
            
            if stage["duration_days"]:
                duration = random.randint(*stage["duration_days"])
                
                for day in range(duration):
                    daily_actions = random.randint(*stage["daily_actions"])
                    
                    day_plan = {
                        "date": (current_date + timedelta(days=len(plan))).isoformat(),
                        "stage": stage_name,
                        "target_actions": daily_actions,
                        "activity_types": stage["activities"].copy(),
                        "human_behavior_score": stage["human_behavior_score"],
                        "completed": False
                    }
                    
                    plan.append(day_plan)
        
        return plan
    
    def _calculate_completion_date(self, plan: List[Dict]) -> str:
        """Calculate estimated completion date"""
        if not plan:
            return datetime.now().isoformat()
        
        return plan[-1]["date"]
    
    def execute_daily_warming(self, account_id: str) -> Dict[str, Any]:
        """
        Execute daily warming activities for an account
        """
        if account_id not in self.warming_accounts:
            return {"error": "Account not in warming process"}
        
        account = self.warming_accounts[account_id]
        current_date = datetime.now().date()
        
        # Find today's plan
        today_plan = None
        for day in account["plan"]:
            plan_date = datetime.fromisoformat(day["date"]).date()
            if plan_date == current_date and not day["completed"]:
                today_plan = day
                break
        
        if not today_plan:
            return {"error": "No warming activities scheduled for today"}
        
        # Simulate executing activities
        activities_completed = []
        total_actions = 0
        
        for activity_type in today_plan["activity_types"]:
            actions_for_activity = random.randint(1, today_plan["target_actions"] // len(today_plan["activity_types"]) + 1)
            
            for _ in range(actions_for_activity):
                activity = self._simulate_warming_activity(activity_type, account["platform"])
                activities_completed.append(activity)
                total_actions += 1
                
                if total_actions >= today_plan["target_actions"]:
                    break
            
            if total_actions >= today_plan["target_actions"]:
                break
        
        # Update account progress
        today_plan["completed"] = True
        account["completed_activities"].extend(activities_completed)
        
        # Update reputation and risk scores
        account["reputation_score"] = min(1.0, account["reputation_score"] + 0.02)
        account["detection_risk"] = max(0.1, account["detection_risk"] - 0.015)
        
        # Log daily activity
        daily_log = {
            "date": current_date.isoformat(),
            "stage": today_plan["stage"],
            "actions_completed": total_actions,
            "reputation_gain": 0.02,
            "risk_reduction": 0.015,
            "activities": activities_completed
        }
        
        account["daily_activity_log"].append(daily_log)
        
        # Check if stage completed
        stage_completed = self._check_stage_completion(account)
        
        return {
            "account_id": account_id,
            "date": current_date.isoformat(),
            "actions_completed": total_actions,
            "target_actions": today_plan["target_actions"],
            "current_reputation": account["reputation_score"],
            "current_risk": account["detection_risk"],
            "stage_completed": stage_completed,
            "activities": activities_completed
        }
    
    def _simulate_warming_activity(self, activity_type: str, platform: str) -> Dict[str, Any]:
        """Simulate a warming activity"""
        
        activity_templates = {
            "profile_setup": [
                {"action": "update_bio", "description": "Updated profile bio"},
                {"action": "upload_avatar", "description": "Uploaded profile picture"},
                {"action": "add_contact_info", "description": "Added contact information"}
            ],
            "basic_browsing": [
                {"action": "view_homepage", "description": "Browsed homepage feed"},
                {"action": "search_content", "description": "Searched for content"},
                {"action": "view_trending", "description": "Checked trending topics"}
            ],
            "content_consumption": [
                {"action": "watch_video", "description": "Watched video", "duration": random.randint(30, 300)},
                {"action": "read_post", "description": "Read social media post"},
                {"action": "view_story", "description": "Viewed story content"}
            ],
            "light_engagement": [
                {"action": "like_content", "description": "Liked content"},
                {"action": "save_content", "description": "Saved content for later"},
                {"action": "share_content", "description": "Shared content"}
            ],
            "commenting": [
                {"action": "comment", "description": "Posted comment", "text": "Nice video!"},
                {"action": "reply", "description": "Replied to comment"}
            ],
            "following": [
                {"action": "follow_user", "description": "Followed user"},
                {"action": "subscribe_channel", "description": "Subscribed to channel"}
            ],
            "sharing": [
                {"action": "share_post", "description": "Shared post"},
                {"action": "retweet", "description": "Retweeted content"}
            ],
            "content_creation": [
                {"action": "create_post", "description": "Created original post"},
                {"action": "upload_video", "description": "Uploaded video content"}
            ],
            "community_participation": [
                {"action": "join_group", "description": "Joined community group"},
                {"action": "participate_discussion", "description": "Participated in discussion"}
            ]
        }
        
        if activity_type not in activity_templates:
            activity_type = "basic_browsing"  # Fallback
        
        template = random.choice(activity_templates[activity_type])
        
        return {
            "activity_type": activity_type,
            "action": template["action"],
            "description": template["description"],
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "success": random.random() > 0.05,  # 95% success rate
            "human_behavior_score": random.uniform(0.8, 0.95)
        }
    
    def _check_stage_completion(self, account: Dict) -> bool:
        """Check if current stage is completed"""
        current_stage = account["current_stage"]
        
        # Count completed days in current stage
        completed_days = len([
            day for day in account["plan"] 
            if day["stage"] == current_stage and day["completed"]
        ])
        
        total_days = len([
            day for day in account["plan"] 
            if day["stage"] == current_stage
        ])
        
        if completed_days == total_days and completed_days > 0:
            # Move to next stage
            stage_names = list(self.warming_stages.keys())
            current_index = stage_names.index(current_stage)
            
            if current_index < len(stage_names) - 1:
                account["current_stage"] = stage_names[current_index + 1]
            
            return True
        
        return False
    
    def get_account_warming_status(self, account_id: str) -> Dict[str, Any]:
        """Get comprehensive warming status for account"""
        if account_id not in self.warming_accounts:
            return {"error": "Account not found in warming process"}
        
        account = self.warming_accounts[account_id]
        
        # Calculate progress
        total_days = len(account["plan"])
        completed_days = len([day for day in account["plan"] if day["completed"]])
        progress_percentage = (completed_days / total_days) * 100 if total_days > 0 else 0
        
        # Days remaining
        remaining_days = total_days - completed_days
        
        # Recent activity
        recent_activity = account["daily_activity_log"][-7:] if account["daily_activity_log"] else []
        
        return {
            "account_id": account_id,
            "platform": account["platform"],
            "current_stage": account["current_stage"],
            "progress_percentage": progress_percentage,
            "days_completed": completed_days,
            "days_remaining": remaining_days,
            "reputation_score": account["reputation_score"],
            "detection_risk": account["detection_risk"],
            "estimated_completion": account["estimated_completion"],
            "recent_activity": recent_activity,
            "ready_for_bot_operations": account["reputation_score"] >= 0.7 and account["detection_risk"] <= 0.3
        }


# Initialize services
captcha_solver = CaptchaSolverService()
rate_limiter = RateLimitTracker()
proxy_manager = ProxyManager()
account_warmer = AccountWarmingService()

def get_bot_infrastructure_stats() -> Dict[str, Any]:
    """Get comprehensive statistics for all bot infrastructure services"""
    return {
        "captcha_service": captcha_solver.get_stats(),
        "rate_limits": {
            "tracked_accounts": len(rate_limiter.account_activity),
            "active_monitors": len([a for a in rate_limiter.account_activity.values() if any(platform for platform in a.values())])
        },
        "proxy_manager": proxy_manager.get_proxy_statistics(),
        "account_warming": {
            "accounts_in_warming": len(account_warmer.warming_accounts),
            "ready_accounts": len([a for a in account_warmer.warming_accounts.values() if a["reputation_score"] >= 0.7])
        }
    }

if __name__ == "__main__":
    # Demo usage
    print("BOTZZZ Bot Infrastructure Services Demo")
    print("=" * 50)
    
    # Test CAPTCHA solver
    print("\n1. CAPTCHA Solver Test:")
    captcha_result = captcha_solver.solve_captcha("recaptcha_v2", "demo_site_key", "https://example.com")
    print(f"   Success: {captcha_result['success']}")
    print(f"   Provider: {captcha_result['provider']}")
    print(f"   Solve Time: {captcha_result['solve_time']:.1f}s")
    
    # Test Rate Limiter
    print("\n2. Rate Limiter Test:")
    rate_check = rate_limiter.check_rate_limit("youtube", "test_account_001", "likes")
    print(f"   Action Allowed: {rate_check['allowed']}")
    print(f"   Utilization: {rate_check['utilization']:.1%}")
    print(f"   Risk Level: {rate_check['risk_factors']['total_risk']:.2f}")
    
    # Test Proxy Manager
    print("\n3. Proxy Manager Test:")
    proxy_result = proxy_manager.get_optimal_proxy("youtube", "US-East")
    if "proxy" in proxy_result:
        print(f"   Proxy Selected: {proxy_result['proxy']['id']}")
        print(f"   Type: {proxy_result['proxy']['type']}")
        print(f"   Region: {proxy_result['proxy']['region']}")
    
    # Test Account Warming
    print("\n4. Account Warming Test:")
    warming_result = account_warmer.start_account_warming("test_account_002", "youtube")
    print(f"   Warming Started: {warming_result['warming_started']}")
    print(f"   Estimated Duration: {warming_result['estimated_duration']} days")
    
    # Overall stats
    print("\n5. Infrastructure Overview:")
    stats = get_bot_infrastructure_stats()
    print(f"   Active Proxies: {stats['proxy_manager']['active_proxies']}")
    print(f"   Tracked Accounts: {stats['rate_limits']['tracked_accounts']}")
    print(f"   Warming Accounts: {stats['account_warming']['accounts_in_warming']}")


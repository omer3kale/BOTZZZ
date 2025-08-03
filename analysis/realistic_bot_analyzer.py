import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class RealisticBotAnalyzer:
    """Advanced analyzer for realistic bot behavior simulation data"""
    
    def __init__(self):
        self.data_dir = "../data"
        self.output_dir = "../analysis_results"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_realistic_data(self):
        """Load all realistic simulation datasets"""
        datasets = {}
        
        # Load Spotify realistic data
        try:
            with open(f"{self.data_dir}/spotify_realistic_simulation.json", "r") as f:
                datasets["spotify"] = json.load(f)
            print("✓ Loaded Spotify realistic simulation data")
        except FileNotFoundError:
            print("⚠ Spotify realistic data not found")
            
        # Load YouTube realistic data
        try:
            with open(f"{self.data_dir}/youtube_realistic_simulation.json", "r") as f:
                datasets["youtube"] = json.load(f)
            print("✓ Loaded YouTube realistic simulation data")
        except FileNotFoundError:
            print("⚠ YouTube realistic data not found")
            
        # Load detection data
        try:
            with open(f"{self.data_dir}/spotify_detection_events.json", "r") as f:
                datasets["spotify_detection"] = json.load(f)
            print("✓ Loaded Spotify detection events")
        except FileNotFoundError:
            print("⚠ Spotify detection data not found")
            
        return datasets
    
    def analyze_bot_sophistication(self, datasets):
        """Analyze sophistication levels of different bot types"""
        analysis = {}
        
        for platform, data in datasets.items():
            if platform.endswith("_detection"):
                continue
                
            platform_analysis = {
                "bot_types": {},
                "detection_evasion": {},
                "economic_impact": {}
            }
            
            if "bots" in data:
                # Analyze bot type distribution and characteristics
                for bot in data["bots"]:
                    bot_type = bot["bot_type"]
                    if bot_type not in platform_analysis["bot_types"]:
                        platform_analysis["bot_types"][bot_type] = {
                            "count": 0,
                            "description": bot.get("bot_description", ""),
                            "evasion_techniques": [],
                            "detection_signatures": [],
                            "avg_daily_quota": 0,
                            "geographic_distribution": {}
                        }
                    
                    stats = platform_analysis["bot_types"][bot_type]
                    stats["count"] += 1
                    stats["avg_daily_quota"] += bot.get("daily_stream_quota", 0)
                    stats["evasion_techniques"].extend(bot.get("evasion_techniques", []))
                    stats["detection_signatures"].extend(list(bot.get("detection_signatures", {}).keys()))
                    
                    location = bot.get("farm_location", {})
                    country = location.get("country", "Unknown")
                    if country not in stats["geographic_distribution"]:
                        stats["geographic_distribution"][country] = 0
                    stats["geographic_distribution"][country] += 1
                
                # Calculate averages
                for bot_type, stats in platform_analysis["bot_types"].items():
                    if stats["count"] > 0:
                        stats["avg_daily_quota"] = stats["avg_daily_quota"] / stats["count"]
                        stats["unique_evasion_techniques"] = len(set(stats["evasion_techniques"]))
                        stats["unique_detection_signatures"] = len(set(stats["detection_signatures"]))
            
            # Analyze engagement patterns
            if "engagement_log" in data:
                engagement_df = pd.DataFrame(data["engagement_log"])
                
                if not engagement_df.empty:
                    # Bot vs Real user behavior analysis
                    bot_data = engagement_df[engagement_df["user_type"] == "bot"]
                    real_data = engagement_df[engagement_df["user_type"] == "real"]
                    
                    if not bot_data.empty:
                        platform_analysis["behavior_patterns"] = {
                            "bot_completion_rates": bot_data.get("completion_rate", []).describe().to_dict() if "completion_rate" in bot_data.columns else {},
                            "real_completion_rates": real_data.get("completion_rate", []).describe().to_dict() if "completion_rate" in real_data.columns else {},
                            "bot_session_patterns": self.analyze_session_patterns(bot_data),
                            "real_session_patterns": self.analyze_session_patterns(real_data)
                        }
            
            # Economic impact analysis
            if "economic_summary" in data:
                platform_analysis["economic_impact"] = data["economic_summary"]
            
            analysis[platform] = platform_analysis
        
        return analysis
    
    def analyze_session_patterns(self, engagement_data):
        """Analyze user session patterns for behavioral fingerprinting"""
        if engagement_data.empty:
            return {}
        
        # Group by user and timestamp to identify sessions
        engagement_data['timestamp'] = pd.to_datetime(engagement_data['timestamp'])
        engagement_data = engagement_data.sort_values(['user', 'timestamp'])
        
        session_analysis = {
            "avg_session_length": 0,
            "temporal_patterns": {},
            "repetition_patterns": {}
        }
        
        # Analyze sessions per user
        for user in engagement_data['user'].unique():
            user_data = engagement_data[engagement_data['user'] == user]
            
            # Calculate time gaps between actions
            user_data['time_diff'] = user_data['timestamp'].diff()
            
            # Session breaks (>30 minutes gap)
            session_breaks = user_data['time_diff'] > pd.Timedelta(minutes=30)
            sessions = user_data[session_breaks]
            
            if len(sessions) > 0:
                avg_session_length = len(user_data) / len(sessions)
                session_analysis["avg_session_length"] += avg_session_length
        
        if len(engagement_data['user'].unique()) > 0:
            session_analysis["avg_session_length"] /= len(engagement_data['user'].unique())
        
        # Analyze temporal patterns
        engagement_data['hour'] = engagement_data['timestamp'].dt.hour
        hourly_activity = engagement_data['hour'].value_counts().to_dict()
        session_analysis["temporal_patterns"] = hourly_activity
        
        # Analyze content repetition patterns
        if 'track_id' in engagement_data.columns:
            track_repetition = engagement_data['track_id'].value_counts()
            session_analysis["repetition_patterns"] = {
                "avg_track_repetition": track_repetition.mean(),
                "max_track_repetition": track_repetition.max(),
                "unique_tracks_ratio": len(track_repetition) / len(engagement_data)
            }
        
        return session_analysis
    
    def detect_bot_signatures(self, datasets):
        """Advanced bot detection using behavioral signatures"""
        detection_results = {}
        
        for platform, data in datasets.items():
            if platform.endswith("_detection"):
                continue
            
            platform_detection = {
                "behavioral_anomalies": [],
                "temporal_anomalies": [],
                "technical_anomalies": [],
                "risk_scores": {}
            }
            
            if "engagement_log" in data:
                engagement_df = pd.DataFrame(data["engagement_log"])
                
                if not engagement_df.empty:
                    # Behavioral anomaly detection
                    platform_detection["behavioral_anomalies"] = self.detect_behavioral_anomalies(engagement_df)
                    
                    # Temporal pattern detection
                    platform_detection["temporal_anomalies"] = self.detect_temporal_anomalies(engagement_df)
                    
                    # Technical fingerprint detection
                    platform_detection["technical_anomalies"] = self.detect_technical_anomalies(engagement_df)
                    
                    # Calculate risk scores per user
                    platform_detection["risk_scores"] = self.calculate_risk_scores(engagement_df)
            
            detection_results[platform] = platform_detection
        
        return detection_results
    
    def detect_behavioral_anomalies(self, engagement_df):
        """Detect behavioral patterns indicative of bot activity"""
        anomalies = []
        
        # Analyze completion rates
        if "completion_rate" in engagement_df.columns:
            user_completion_rates = engagement_df.groupby("user")["completion_rate"].agg(['mean', 'std', 'count'])
            
            # Flag users with suspiciously consistent completion rates
            suspicious_consistency = user_completion_rates[
                (user_completion_rates['std'] < 0.05) & 
                (user_completion_rates['count'] > 10)
            ]
            
            for user in suspicious_consistency.index:
                anomalies.append({
                    "type": "consistent_completion_rate",
                    "user": user,
                    "avg_completion_rate": suspicious_consistency.loc[user, 'mean'],
                    "std_completion_rate": suspicious_consistency.loc[user, 'std'],
                    "risk_level": "high"
                })
        
        # Analyze listening patterns
        if "listen_duration_ms" in engagement_df.columns and "duration_ms" in engagement_df.columns:
            # Users who consistently listen for minimal time
            minimal_listeners = engagement_df.groupby("user").apply(
                lambda x: (x["listen_duration_ms"] <= 35000).mean() > 0.8
            )
            
            for user in minimal_listeners[minimal_listeners].index:
                user_data = engagement_df[engagement_df["user"] == user]
                avg_listen_time = user_data["listen_duration_ms"].mean()
                
                anomalies.append({
                    "type": "minimal_listen_time",
                    "user": user,
                    "avg_listen_duration": avg_listen_time,
                    "minimal_listen_ratio": (user_data["listen_duration_ms"] <= 35000).mean(),
                    "risk_level": "high"
                })
        
        return anomalies
    
    def detect_temporal_anomalies(self, engagement_df):
        """Detect temporal patterns indicative of automated behavior"""
        anomalies = []
        
        engagement_df['timestamp'] = pd.to_datetime(engagement_df['timestamp'])
        
        # Analyze activity patterns per user
        for user in engagement_df['user'].unique():
            user_data = engagement_df[engagement_df['user'] == user]
            
            if len(user_data) < 10:  # Need sufficient data
                continue
            
            # Check for robotic timing patterns
            user_data = user_data.sort_values('timestamp')
            time_diffs = user_data['timestamp'].diff().dt.total_seconds()
            
            # Remove NaN values
            time_diffs = time_diffs.dropna()
            
            if len(time_diffs) > 5:
                # Suspiciously regular intervals
                time_diff_std = time_diffs.std()
                time_diff_mean = time_diffs.mean()
                
                if time_diff_std < 10 and time_diff_mean > 30:  # Very consistent timing
                    anomalies.append({
                        "type": "robotic_timing",
                        "user": user,
                        "avg_interval_seconds": time_diff_mean,
                        "interval_consistency": time_diff_std,
                        "risk_level": "medium"
                    })
                
                # 24/7 activity patterns
                user_hours = user_data['timestamp'].dt.hour.unique()
                if len(user_hours) > 20:  # Active in most hours
                    anomalies.append({
                        "type": "24_7_activity",
                        "user": user,
                        "active_hours_count": len(user_hours),
                        "risk_level": "medium"
                    })
        
        return anomalies
    
    def detect_technical_anomalies(self, engagement_df):
        """Detect technical fingerprints of bot activity"""
        anomalies = []
        
        # Analyze user agents and device patterns
        if "user_agent" in engagement_df.columns:
            # Identify suspicious user agent patterns
            user_agent_counts = engagement_df.groupby("user")["user_agent"].nunique()
            
            # Users with no user agent diversity (always same device)
            no_diversity_users = user_agent_counts[user_agent_counts == 1]
            
            for user in no_diversity_users.index:
                user_data = engagement_df[engagement_df["user"] == user]
                if len(user_data) > 50:  # Significant activity with no device change
                    anomalies.append({
                        "type": "no_device_diversity",
                        "user": user,
                        "total_sessions": len(user_data),
                        "unique_user_agents": user_agent_counts[user],
                        "risk_level": "medium"
                    })
        
        # Analyze geolocation consistency for bots
        if "bot_country" in engagement_df.columns:
            bot_data = engagement_df[engagement_df["user_type"] == "bot"]
            
            # Bots should show consistent geographic patterns
            geo_consistency = bot_data.groupby("user")["bot_country"].nunique()
            inconsistent_bots = geo_consistency[geo_consistency > 1]
            
            for user in inconsistent_bots.index:
                anomalies.append({
                    "type": "geographic_inconsistency",
                    "user": user,
                    "countries_count": inconsistent_bots[user],
                    "risk_level": "low"  # Might be sophisticated evasion
                })
        
        return anomalies
    
    def calculate_risk_scores(self, engagement_df):
        """Calculate comprehensive risk scores for users"""
        risk_scores = {}
        
        for user in engagement_df['user'].unique():
            user_data = engagement_df[engagement_df['user'] == user]
            risk_score = 0
            risk_factors = []
            
            # Behavioral risk factors
            if "completion_rate" in user_data.columns:
                completion_rates = user_data["completion_rate"]
                if completion_rates.std() < 0.05 and len(completion_rates) > 10:
                    risk_score += 0.3
                    risk_factors.append("consistent_completion_rate")
                
                if completion_rates.mean() < 0.2:
                    risk_score += 0.4
                    risk_factors.append("minimal_listening")
            
            # Volume risk factors
            activity_count = len(user_data)
            if activity_count > 1000:  # Very high activity
                risk_score += 0.2
                risk_factors.append("high_volume_activity")
            
            # Temporal risk factors
            if len(user_data) > 5:
                user_data_sorted = user_data.sort_values('timestamp')
                user_data_sorted['timestamp'] = pd.to_datetime(user_data_sorted['timestamp'])
                time_diffs = user_data_sorted['timestamp'].diff().dt.total_seconds().dropna()
                
                if len(time_diffs) > 0 and time_diffs.std() < 30:
                    risk_score += 0.3
                    risk_factors.append("robotic_timing")
            
            # Technical risk factors
            if "user_agent" in user_data.columns:
                if user_data["user_agent"].nunique() == 1 and len(user_data) > 50:
                    risk_score += 0.2
                    risk_factors.append("no_device_diversity")
            
            # Bot type confirmation
            if "user_type" in user_data.columns and user_data["user_type"].iloc[0] == "bot":
                risk_score = 1.0  # Confirmed bot
                risk_factors.append("confirmed_bot")
            
            risk_scores[user] = {
                "risk_score": min(risk_score, 1.0),
                "risk_factors": risk_factors,
                "risk_level": "high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low"
            }
        
        return risk_scores
    
    def generate_comprehensive_report(self, datasets):
        """Generate comprehensive analysis report"""
        print("Generating comprehensive realistic bot behavior analysis...")
        
        # Load and analyze data
        sophistication_analysis = self.analyze_bot_sophistication(datasets)
        detection_analysis = self.detect_bot_signatures(datasets)
        
        # Create comprehensive report
        report = {
            "analysis_metadata": {
                "generated_at": datetime.now().isoformat(),
                "analysis_type": "realistic_bot_behavior_analysis",
                "platforms_analyzed": list(datasets.keys())
            },
            "sophistication_analysis": sophistication_analysis,
            "detection_analysis": detection_analysis,
            "cross_platform_insights": self.generate_cross_platform_insights(sophistication_analysis),
            "recommendations": self.generate_recommendations(sophistication_analysis, detection_analysis)
        }
        
        # Save detailed report
        with open(f"{self.output_dir}/realistic_bot_analysis_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # Generate visual analysis
        self.create_visualizations(datasets, sophistication_analysis, detection_analysis)
        
        # Create summary markdown report
        self.create_markdown_report(report)
        
        return report
    
    def generate_cross_platform_insights(self, sophistication_analysis):
        """Generate insights comparing bot sophistication across platforms"""
        insights = {
            "bot_type_comparison": {},
            "sophistication_levels": {},
            "economic_impact_comparison": {}
        }
        
        # Compare bot types across platforms
        all_bot_types = set()
        for platform, data in sophistication_analysis.items():
            if "bot_types" in data:
                all_bot_types.update(data["bot_types"].keys())
        
        for bot_type in all_bot_types:
            insights["bot_type_comparison"][bot_type] = {}
            for platform, data in sophistication_analysis.items():
                if "bot_types" in data and bot_type in data["bot_types"]:
                    bot_data = data["bot_types"][bot_type]
                    insights["bot_type_comparison"][bot_type][platform] = {
                        "count": bot_data["count"],
                        "avg_daily_quota": bot_data["avg_daily_quota"],
                        "evasion_techniques": bot_data["unique_evasion_techniques"],
                        "detection_signatures": bot_data["unique_detection_signatures"]
                    }
        
        # Compare economic impact
        for platform, data in sophistication_analysis.items():
            if "economic_impact" in data:
                economic_data = data["economic_impact"]
                insights["economic_impact_comparison"][platform] = {
                    "bot_revenue_percentage": economic_data.get("revenue_analysis", {}).get("bot_revenue_percentage", 0),
                    "bot_roi": economic_data.get("revenue_analysis", {}).get("bot_roi", 0),
                    "detection_rate": economic_data.get("detection_analysis", {}).get("detection_rate", 0)
                }
        
        return insights
    
    def generate_recommendations(self, sophistication_analysis, detection_analysis):
        """Generate actionable recommendations based on analysis"""
        recommendations = {
            "detection_improvements": [],
            "platform_specific": {},
            "general_strategies": []
        }
        
        # Analyze detection effectiveness
        for platform, detection_data in detection_analysis.items():
            platform_recs = []
            
            # Check detection coverage
            behavioral_coverage = len(detection_data.get("behavioral_anomalies", []))
            temporal_coverage = len(detection_data.get("temporal_anomalies", []))
            technical_coverage = len(detection_data.get("technical_anomalies", []))
            
            if behavioral_coverage < 5:
                platform_recs.append("Implement advanced behavioral pattern analysis")
            
            if temporal_coverage < 3:
                platform_recs.append("Enhance temporal activity monitoring")
            
            if technical_coverage < 2:
                platform_recs.append("Strengthen device fingerprinting detection")
            
            # Analyze bot sophistication levels
            if platform in sophistication_analysis:
                bot_types = sophistication_analysis[platform].get("bot_types", {})
                
                sophisticated_bots = [bt for bt, data in bot_types.items() 
                                    if data.get("unique_evasion_techniques", 0) > 3]
                
                if sophisticated_bots:
                    platform_recs.append(f"Focus on detecting sophisticated bot types: {', '.join(sophisticated_bots)}")
                
                # Economic impact recommendations
                economic_impact = sophistication_analysis[platform].get("economic_impact", {})
                bot_revenue_pct = economic_impact.get("revenue_analysis", {}).get("bot_revenue_percentage", 0)
                
                if bot_revenue_pct > 25:
                    platform_recs.append("Implement urgent bot mitigation measures - high revenue impact detected")
                elif bot_revenue_pct > 15:
                    platform_recs.append("Moderate bot activity detected - consider enhanced monitoring")
            
            recommendations["platform_specific"][platform] = platform_recs
        
        # General recommendations
        recommendations["general_strategies"] = [
            "Implement machine learning-based behavioral analysis",
            "Deploy real-time detection systems with adaptive thresholds",
            "Establish cross-platform bot intelligence sharing",
            "Develop economic impact assessment frameworks",
            "Create industry-wide bot detection standards"
        ]
        
        return recommendations
    
    def create_visualizations(self, datasets, sophistication_analysis, detection_analysis):
        """Create comprehensive visualizations"""
        plt.style.use('default')
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Bot Type Distribution Across Platforms
        plt.subplot(3, 3, 1)
        platform_bot_counts = {}
        for platform, data in sophistication_analysis.items():
            if "bot_types" in data:
                platform_bot_counts[platform] = sum(bt["count"] for bt in data["bot_types"].values())
        
        if platform_bot_counts:
            plt.bar(platform_bot_counts.keys(), platform_bot_counts.values(), color=['#FF6B6B', '#4ECDC4'])
            plt.title('Bot Count by Platform', fontweight='bold')
            plt.ylabel('Number of Bots')
            plt.xticks(rotation=45)
        
        # 2. Economic Impact Comparison
        plt.subplot(3, 3, 2)
        revenue_impact = {}
        for platform, data in sophistication_analysis.items():
            economic = data.get("economic_impact", {}).get("revenue_analysis", {})
            revenue_impact[platform] = economic.get("bot_revenue_percentage", 0)
        
        if revenue_impact:
            colors = ['#FF9999' if v > 25 else '#FFE66D' if v > 15 else '#95E1D3' for v in revenue_impact.values()]
            plt.bar(revenue_impact.keys(), revenue_impact.values(), color=colors)
            plt.title('Bot Revenue Impact by Platform', fontweight='bold')
            plt.ylabel('Bot Revenue Percentage (%)')
            plt.axhline(y=25, color='red', linestyle='--', alpha=0.7, label='High Risk (25%)')
            plt.axhline(y=15, color='orange', linestyle='--', alpha=0.7, label='Medium Risk (15%)')
            plt.legend()
            plt.xticks(rotation=45)
        
        # 3. Detection Effectiveness
        plt.subplot(3, 3, 3)
        detection_counts = {}
        for platform, data in detection_analysis.items():
            total_anomalies = (len(data.get("behavioral_anomalies", [])) + 
                             len(data.get("temporal_anomalies", [])) + 
                             len(data.get("technical_anomalies", [])))
            detection_counts[platform] = total_anomalies
        
        if detection_counts:
            plt.bar(detection_counts.keys(), detection_counts.values(), color=['#A8E6CF', '#88D8C0'])
            plt.title('Detection Events by Platform', fontweight='bold')
            plt.ylabel('Number of Detection Events')
            plt.xticks(rotation=45)
        
        # 4. Bot Sophistication Levels
        plt.subplot(3, 3, 4)
        sophistication_data = []
        platforms = []
        bot_types = []
        
        for platform, data in sophistication_analysis.items():
            if "bot_types" in data:
                for bot_type, bt_data in data["bot_types"].items():
                    sophistication_data.append(bt_data.get("unique_evasion_techniques", 0))
                    platforms.append(platform)
                    bot_types.append(bot_type)
        
        if sophistication_data:
            colors = plt.cm.Set3(np.linspace(0, 1, len(set(bot_types))))
            color_map = {bt: colors[i] for i, bt in enumerate(set(bot_types))}
            bar_colors = [color_map[bt] for bt in bot_types]
            
            x_pos = range(len(sophistication_data))
            plt.bar(x_pos, sophistication_data, color=bar_colors)
            plt.title('Bot Sophistication (Evasion Techniques)', fontweight='bold')
            plt.ylabel('Number of Evasion Techniques')
            plt.xlabel('Bot Instance')
            
            # Create legend
            legend_elements = [plt.Rectangle((0,0),1,1, fc=color_map[bt]) for bt in set(bot_types)]
            plt.legend(legend_elements, set(bot_types), loc='upper right', bbox_to_anchor=(1.15, 1))
        
        # 5. Geographic Distribution
        plt.subplot(3, 3, 5)
        all_countries = {}
        for platform, data in sophistication_analysis.items():
            if "bot_types" in data:
                for bot_type, bt_data in data["bot_types"].items():
                    for country, count in bt_data.get("geographic_distribution", {}).items():
                        if country not in all_countries:
                            all_countries[country] = 0
                        all_countries[country] += count
        
        if all_countries:
            top_countries = dict(sorted(all_countries.items(), key=lambda x: x[1], reverse=True)[:10])
            plt.barh(list(top_countries.keys()), list(top_countries.values()), color='#FFB6C1')
            plt.title('Bot Farm Geographic Distribution', fontweight='bold')
            plt.xlabel('Number of Bots')
        
        # 6. Risk Score Distribution
        plt.subplot(3, 3, 6)
        all_risk_scores = []
        for platform, data in detection_analysis.items():
            risk_scores = data.get("risk_scores", {})
            for user, score_data in risk_scores.items():
                all_risk_scores.append(score_data["risk_score"])
        
        if all_risk_scores:
            plt.hist(all_risk_scores, bins=20, color='#DDA0DD', alpha=0.7, edgecolor='black')
            plt.title('Risk Score Distribution', fontweight='bold')
            plt.xlabel('Risk Score')
            plt.ylabel('Number of Users')
            plt.axvline(x=0.7, color='red', linestyle='--', label='High Risk Threshold')
            plt.axvline(x=0.4, color='orange', linestyle='--', label='Medium Risk Threshold')
            plt.legend()
        
        # 7. Temporal Activity Patterns
        plt.subplot(3, 3, 7)
        hourly_activity = {}
        for platform, data in sophistication_analysis.items():
            if "bot_types" in data:
                for bot_type, bt_data in data["bot_types"].items():
                    patterns = bt_data.get("behavior_patterns", {}).get("temporal_patterns", {})
                    for hour, count in patterns.items():
                        if hour not in hourly_activity:
                            hourly_activity[hour] = 0
                        hourly_activity[hour] += count
        
        if hourly_activity:
            hours = sorted(hourly_activity.keys())
            activity = [hourly_activity[h] for h in hours]
            plt.plot(hours, activity, marker='o', color='#20B2AA', linewidth=2)
            plt.title('Bot Activity by Hour', fontweight='bold')
            plt.xlabel('Hour of Day')
            plt.ylabel('Activity Count')
            plt.grid(True, alpha=0.3)
        
        # 8. Detection Method Effectiveness
        plt.subplot(3, 3, 8)
        detection_methods = {"Behavioral": 0, "Temporal": 0, "Technical": 0}
        for platform, data in detection_analysis.items():
            detection_methods["Behavioral"] += len(data.get("behavioral_anomalies", []))
            detection_methods["Temporal"] += len(data.get("temporal_anomalies", []))
            detection_methods["Technical"] += len(data.get("technical_anomalies", []))
        
        if sum(detection_methods.values()) > 0:
            plt.pie(detection_methods.values(), labels=detection_methods.keys(), autopct='%1.1f%%',
                   colors=['#FFB347', '#87CEEB', '#98FB98'])
            plt.title('Detection Method Distribution', fontweight='bold')
        
        # 9. Bot ROI Analysis
        plt.subplot(3, 3, 9)
        roi_data = {}
        for platform, data in sophistication_analysis.items():
            economic = data.get("economic_impact", {}).get("revenue_analysis", {})
            roi = economic.get("bot_roi", 0)
            if roi > 0:
                roi_data[platform] = roi
        
        if roi_data:
            colors = ['#FF6B6B' if v > 500 else '#FFE66D' if v > 200 else '#95E1D3' for v in roi_data.values()]
            plt.bar(roi_data.keys(), roi_data.values(), color=colors)
            plt.title('Bot Operation ROI by Platform', fontweight='bold')
            plt.ylabel('ROI (%)')
            plt.xticks(rotation=45)
            plt.axhline(y=200, color='orange', linestyle='--', alpha=0.7, label='High Profitability (200%)')
            plt.legend()
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/realistic_bot_analysis.png", dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✓ Visualizations saved to {self.output_dir}/realistic_bot_analysis.png")
    
    def create_markdown_report(self, report):
        """Create a comprehensive markdown report"""
        markdown_content = f"""# Realistic Bot Behavior Analysis Report

## Executive Summary
Generated: {report['analysis_metadata']['generated_at']}
Platforms Analyzed: {', '.join(report['analysis_metadata']['platforms_analyzed'])}

## Key Findings

### Bot Sophistication Analysis
"""
        
        for platform, data in report['sophistication_analysis'].items():
            if "bot_types" in data:
                markdown_content += f"\n#### {platform.upper()} Platform\n"
                markdown_content += f"- **Bot Types Identified**: {len(data['bot_types'])}\n"
                
                for bot_type, bt_data in data['bot_types'].items():
                    markdown_content += f"  - **{bot_type}**: {bt_data['count']} instances\n"
                    markdown_content += f"    - Description: {bt_data['description']}\n"
                    markdown_content += f"    - Avg Daily Quota: {bt_data['avg_daily_quota']:.0f}\n"
                    markdown_content += f"    - Evasion Techniques: {bt_data['unique_evasion_techniques']}\n"
                    markdown_content += f"    - Detection Signatures: {bt_data['unique_detection_signatures']}\n"
                
                if "economic_impact" in data:
                    economic = data["economic_impact"]
                    markdown_content += f"\n**Economic Impact:**\n"
                    markdown_content += f"- Bot Revenue Share: {economic.get('revenue_analysis', {}).get('bot_revenue_percentage', 0):.1f}%\n"
                    markdown_content += f"- Bot ROI: {economic.get('revenue_analysis', {}).get('bot_roi', 0):.1f}%\n"
                    markdown_content += f"- Detection Rate: {economic.get('detection_analysis', {}).get('detection_rate', 0):.1f}%\n"
        
        markdown_content += f"\n### Detection Analysis\n"
        
        for platform, detection_data in report['detection_analysis'].items():
            markdown_content += f"\n#### {platform.upper()} Detection Results\n"
            markdown_content += f"- Behavioral Anomalies: {len(detection_data.get('behavioral_anomalies', []))}\n"
            markdown_content += f"- Temporal Anomalies: {len(detection_data.get('temporal_anomalies', []))}\n"
            markdown_content += f"- Technical Anomalies: {len(detection_data.get('technical_anomalies', []))}\n"
            markdown_content += f"- Users Analyzed: {len(detection_data.get('risk_scores', {}))}\n"
        
        markdown_content += f"\n### Cross-Platform Insights\n"
        
        cross_platform = report.get('cross_platform_insights', {})
        if 'economic_impact_comparison' in cross_platform:
            markdown_content += f"\n#### Economic Impact Comparison\n"
            for platform, economic in cross_platform['economic_impact_comparison'].items():
                markdown_content += f"- **{platform}**: {economic['bot_revenue_percentage']:.1f}% bot revenue, {economic['bot_roi']:.1f}% ROI\n"
        
        markdown_content += f"\n### Recommendations\n"
        
        recommendations = report.get('recommendations', {})
        
        markdown_content += f"\n#### Platform-Specific Recommendations\n"
        for platform, recs in recommendations.get('platform_specific', {}).items():
            markdown_content += f"\n**{platform.upper()}:**\n"
            for rec in recs:
                markdown_content += f"- {rec}\n"
        
        markdown_content += f"\n#### General Strategies\n"
        for strategy in recommendations.get('general_strategies', []):
            markdown_content += f"- {strategy}\n"
        
        markdown_content += f"\n---\n*Report generated by Realistic Bot Analyzer*"
        
        # Save markdown report
        with open(f"{self.output_dir}/realistic_bot_analysis_report.md", "w") as f:
            f.write(markdown_content)
        
        print(f"✓ Markdown report saved to {self.output_dir}/realistic_bot_analysis_report.md")

def main():
    analyzer = RealisticBotAnalyzer()
    
    # Load datasets
    datasets = analyzer.load_realistic_data()
    
    if datasets:
        # Generate comprehensive analysis
        report = analyzer.generate_comprehensive_report(datasets)
        
        print("\n" + "="*50)
        print("REALISTIC BOT ANALYSIS COMPLETE")
        print("="*50)
        
        # Print summary
        for platform in datasets.keys():
            if platform.endswith("_detection"):
                continue
            print(f"\n{platform.upper()} Summary:")
            if platform in report['sophistication_analysis']:
                analysis = report['sophistication_analysis'][platform]
                if 'bot_types' in analysis:
                    print(f"  Bot Types: {len(analysis['bot_types'])}")
                    total_bots = sum(bt['count'] for bt in analysis['bot_types'].values())
                    print(f"  Total Bots: {total_bots}")
                if 'economic_impact' in analysis:
                    economic = analysis['economic_impact']
                    bot_rev_pct = economic.get('revenue_analysis', {}).get('bot_revenue_percentage', 0)
                    bot_roi = economic.get('revenue_analysis', {}).get('bot_roi', 0)
                    print(f"  Bot Revenue Impact: {bot_rev_pct:.1f}%")
                    print(f"  Bot ROI: {bot_roi:.1f}%")
        
        print(f"\nDetailed analysis saved to: analysis_results/")
        print(f"- JSON Report: realistic_bot_analysis_report.json")
        print(f"- Markdown Report: realistic_bot_analysis_report.md") 
        print(f"- Visualizations: realistic_bot_analysis.png")
    
    else:
        print("No realistic bot data found. Please run the realistic simulations first.")

if __name__ == "__main__":
    main()

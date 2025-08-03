"""
Economic Analysis Module for Bot Research
Analyzes the financial impact of bot activities across different platforms
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

class EconomicAnalyzer:
    def __init__(self):
        self.platform_metrics = {
            "youtube": {
                "revenue_per_1000_views": 1.0,  # $1-5 per 1000 views (CPM)
                "revenue_per_subscriber": 0.05,  # Estimated value per subscriber
                "ad_revenue_share": 0.55,  # YouTube takes 45%, creator gets 55%
                "premium_revenue_multiplier": 1.8  # Premium views pay more
            },
            "spotify": {
                "revenue_per_stream": 0.003,  # $0.003-0.005 per stream
                "premium_multiplier": 1.5,  # Premium streams pay more
                "min_play_duration": 30000,  # 30 seconds minimum for payout
                "artist_revenue_share": 0.70  # Artist gets ~70% after platform fees
            },
            "instagram": {
                "revenue_per_1000_impressions": 0.5,  # Lower than YouTube
                "sponsored_post_value": 100,  # Value per 10k followers
                "engagement_value_multiplier": 2.0,  # Higher engagement = higher value
                "story_revenue_multiplier": 0.8  # Stories pay less than posts
            }
        }
    
    def load_engagement_data(self, platform, file_path):
        """Load engagement data for a specific platform"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
    
    def analyze_youtube_economics(self, engagement_data):
        """Analyze economic impact of bots on YouTube"""
        metrics = self.platform_metrics["youtube"]
        
        # Separate real and bot activities
        real_views = [e for e in engagement_data if e.get("type") == "real" and e.get("action") == "view"]
        bot_views = [e for e in engagement_data if e.get("type") == "bot" and e.get("action") == "view"]
        
        real_likes = [e for e in engagement_data if e.get("type") == "real" and e.get("action") == "like"]
        bot_likes = [e for e in engagement_data if e.get("type") == "bot" and e.get("action") == "like"]
        
        # Calculate revenue impact
        real_revenue = (len(real_views) / 1000) * metrics["revenue_per_1000_views"]
        bot_revenue = (len(bot_views) / 1000) * metrics["revenue_per_1000_views"]
        
        # Bot detection risk (higher engagement ratio = higher risk)
        total_views = len(real_views) + len(bot_views)
        total_likes = len(real_likes) + len(bot_likes)
        
        engagement_ratio = (total_likes / total_views) if total_views > 0 else 0
        normal_engagement_ratio = 0.05  # Typical 5% engagement rate
        
        detection_risk = min(1.0, max(0, (engagement_ratio - normal_engagement_ratio) / normal_engagement_ratio))
        
        return {
            "platform": "youtube",
            "real_views": len(real_views),
            "bot_views": len(bot_views),
            "real_revenue": round(real_revenue, 4),
            "bot_revenue": round(bot_revenue, 4),
            "total_revenue": round(real_revenue + bot_revenue, 4),
            "bot_revenue_percentage": round((bot_revenue / (real_revenue + bot_revenue)) * 100, 2) if (real_revenue + bot_revenue) > 0 else 0,
            "engagement_ratio": round(engagement_ratio, 4),
            "detection_risk_score": round(detection_risk, 4),
            "estimated_monthly_revenue": round((real_revenue + bot_revenue) * 30, 2)
        }
    
    def analyze_spotify_economics(self, engagement_data, economic_data=None):
        """Analyze economic impact of bots on Spotify"""
        metrics = self.platform_metrics["spotify"]
        
        if economic_data:
            # Use detailed economic data if available
            real_revenue = sum(e["revenue_generated"] for e in economic_data if e["user_type"] == "real")
            bot_revenue = sum(e["revenue_generated"] for e in economic_data if e["user_type"] == "bot")
            
            real_streams = len([e for e in engagement_data if e.get("user_type") == "real" and e.get("action") == "stream"])
            bot_streams = len([e for e in engagement_data if e.get("user_type") == "bot" and e.get("action") == "stream"])
        else:
            # Calculate from engagement data
            real_streams = [e for e in engagement_data if e.get("user_type") == "real" and e.get("action") == "stream"]
            bot_streams = [e for e in engagement_data if e.get("user_type") == "bot" and e.get("action") == "stream"]
            
            real_revenue = len(real_streams) * metrics["revenue_per_stream"]
            bot_revenue = len(bot_streams) * metrics["revenue_per_stream"]
            
            real_streams = len(real_streams)
            bot_streams = len(bot_streams)
        
        # Analyze streaming patterns for bot detection
        bot_stream_events = [e for e in engagement_data if e.get("user_type") == "bot" and e.get("action") == "stream"]
        
        # Calculate average completion rates
        real_completion_rates = [e.get("completion_rate", 0) for e in engagement_data 
                               if e.get("user_type") == "real" and e.get("action") == "stream" and "completion_rate" in e]
        bot_completion_rates = [e.get("completion_rate", 0) for e in engagement_data 
                              if e.get("user_type") == "bot" and e.get("action") == "stream" and "completion_rate" in e]
        
        avg_real_completion = np.mean(real_completion_rates) if real_completion_rates else 0
        avg_bot_completion = np.mean(bot_completion_rates) if bot_completion_rates else 0
        
        # Detection risk based on unusual patterns
        completion_diff = abs(avg_bot_completion - avg_real_completion)
        detection_risk = min(1.0, completion_diff * 2)  # Higher difference = higher risk
        
        return {
            "platform": "spotify",
            "real_streams": real_streams,
            "bot_streams": bot_streams,
            "real_revenue": round(real_revenue, 4),
            "bot_revenue": round(bot_revenue, 4),
            "total_revenue": round(real_revenue + bot_revenue, 4),
            "bot_revenue_percentage": round((bot_revenue / (real_revenue + bot_revenue)) * 100, 2) if (real_revenue + bot_revenue) > 0 else 0,
            "avg_real_completion_rate": round(avg_real_completion, 4),
            "avg_bot_completion_rate": round(avg_bot_completion, 4),
            "detection_risk_score": round(detection_risk, 4),
            "estimated_monthly_revenue": round((real_revenue + bot_revenue) * 30, 2)
        }
    
    def analyze_instagram_economics(self, engagement_data):
        """Analyze economic impact of bots on Instagram"""
        metrics = self.platform_metrics["instagram"]
        
        # Separate real and bot activities
        real_likes = [e for e in engagement_data if e.get("type") == "real" and e.get("action") == "like"]
        bot_likes = [e for e in engagement_data if e.get("type") == "bot" and e.get("action") == "like"]
        
        real_comments = [e for e in engagement_data if e.get("type") == "real" and e.get("action") == "comment"]
        bot_comments = [e for e in engagement_data if e.get("type") == "bot" and e.get("action") == "comment"]
        
        # Instagram revenue is primarily through sponsored content and brand partnerships
        # Calculate based on engagement rates
        total_engagements = len(real_likes) + len(bot_likes) + len(real_comments) + len(bot_comments)
        real_engagements = len(real_likes) + len(real_comments)
        bot_engagements = len(bot_likes) + len(bot_comments)
        
        # Estimate value based on engagement (very rough approximation)
        engagement_value = (total_engagements / 1000) * metrics["revenue_per_1000_impressions"]
        
        # Calculate what portion is "artificial"
        bot_engagement_percentage = (bot_engagements / total_engagements) * 100 if total_engagements > 0 else 0
        
        return {
            "platform": "instagram",
            "real_engagements": real_engagements,
            "bot_engagements": bot_engagements,
            "total_engagement_value": round(engagement_value, 4),
            "bot_engagement_percentage": round(bot_engagement_percentage, 2),
            "estimated_monthly_value": round(engagement_value * 30, 2)
        }
    
    def generate_comparison_report(self, analyses):
        """Generate a comprehensive comparison report across platforms"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "platforms_analyzed": len(analyses),
                "total_bot_revenue": sum(a.get("bot_revenue", 0) for a in analyses),
                "total_real_revenue": sum(a.get("real_revenue", 0) for a in analyses),
                "average_bot_percentage": np.mean([a.get("bot_revenue_percentage", 0) for a in analyses])
            },
            "platform_details": analyses,
            "insights": []
        }
        
        # Generate insights
        if report["summary"]["average_bot_percentage"] > 30:
            report["insights"].append("HIGH ALERT: Bot activity represents over 30% of revenue across platforms")
        
        if report["summary"]["average_bot_percentage"] > 15:
            report["insights"].append("MODERATE RISK: Significant bot activity detected")
        
        # Find platform with highest bot activity
        highest_bot_platform = max(analyses, key=lambda x: x.get("bot_revenue_percentage", 0))
        report["insights"].append(f"Platform with highest bot activity: {highest_bot_platform.get('platform', 'unknown')} ({highest_bot_platform.get('bot_revenue_percentage', 0)}%)")
        
        return report
    
    def create_visualizations(self, analyses, output_dir="../data/"):
        """Create visualization charts for the economic analysis"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8')
        
        # 1. Revenue comparison chart
        platforms = [a.get("platform", "unknown") for a in analyses]
        real_revenues = [a.get("real_revenue", 0) for a in analyses]
        bot_revenues = [a.get("bot_revenue", 0) for a in analyses]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Revenue comparison
        x = np.arange(len(platforms))
        width = 0.35
        
        ax1.bar(x - width/2, real_revenues, width, label='Real Users', color='#2ecc71')
        ax1.bar(x + width/2, bot_revenues, width, label='Bot Users', color='#e74c3c')
        
        ax1.set_xlabel('Platform')
        ax1.set_ylabel('Revenue ($)')
        ax1.set_title('Revenue Comparison: Real vs Bot Users')
        ax1.set_xticks(x)
        ax1.set_xticklabels(platforms)
        ax1.legend()
        
        # Bot percentage pie chart
        bot_percentages = [a.get("bot_revenue_percentage", 0) for a in analyses]
        colors = ['#e74c3c', '#f39c12', '#3498db']
        
        ax2.pie(bot_percentages, labels=platforms, autopct='%1.1f%%', colors=colors[:len(platforms)])
        ax2.set_title('Bot Revenue Percentage by Platform')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}economic_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Detection risk heatmap
        risk_data = []
        for analysis in analyses:
            risk_data.append([
                analysis.get("platform", "unknown"),
                analysis.get("detection_risk_score", 0),
                analysis.get("bot_revenue_percentage", 0)
            ])
        
        if risk_data:
            df = pd.DataFrame(risk_data, columns=['Platform', 'Detection Risk', 'Bot Revenue %'])
            
            plt.figure(figsize=(10, 6))
            
            # Create correlation matrix
            numeric_df = df[['Detection Risk', 'Bot Revenue %']]
            correlation_matrix = numeric_df.corr()
            
            sns.heatmap(correlation_matrix, annot=True, cmap='RdYlBu_r', center=0)
            plt.title('Risk Correlation Analysis')
            plt.tight_layout()
            plt.savefig(f"{output_dir}risk_analysis.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        print(f"Visualizations saved to {output_dir}")

def main():
    """Example usage of the Economic Analyzer"""
    analyzer = EconomicAnalyzer()
    
    # You can load data and run analysis
    print("Economic Analysis Module Ready")
    print("Example usage:")
    print("analyzer = EconomicAnalyzer()")
    print("youtube_data = analyzer.load_engagement_data('youtube', '../data/engagement_log.json')")
    print("youtube_analysis = analyzer.analyze_youtube_economics(youtube_data)")
    print("print(youtube_analysis)")

if __name__ == "__main__":
    main()

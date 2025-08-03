"""
Spotify Bot Economics Analysis Tool
Analyzes the economic impact specifically for Spotify streaming data
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

class SpotifyEconomicsAnalyzer:
    def __init__(self, data_dir="../data"):
        self.data_dir = data_dir
        self.spotify_metrics = {
            "base_payout_per_stream": 0.003,  # $0.003 average
            "premium_multiplier": 1.5,
            "min_play_duration_ms": 30000,  # 30 seconds
            "platform_cut": 0.30,  # Spotify takes ~30%
            "label_cut": 0.15,  # Labels take ~15%
            "artist_share": 0.55,  # Artist gets ~55%
        }
    
    def load_spotify_data(self):
        """Load Spotify simulation data"""
        try:
            with open(f"{self.data_dir}/spotify_engagement_log.json", "r") as f:
                engagement_data = json.load(f)
            
            with open(f"{self.data_dir}/spotify_economic_log.json", "r") as f:
                economic_data = json.load(f)
            
            with open(f"{self.data_dir}/spotify_economic_summary.json", "r") as f:
                summary_data = json.load(f)
            
            return engagement_data, economic_data, summary_data
        except FileNotFoundError as e:
            print(f"Data file not found: {e}")
            return None, None, None
    
    def analyze_streaming_patterns(self, engagement_data):
        """Analyze streaming patterns between real users and bots"""
        print("Analyzing streaming patterns...")
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(engagement_data)
        
        # Filter for stream actions only
        streams_df = df[df['action'] == 'stream'].copy()
        
        if streams_df.empty:
            return {}
        
        # Analyze by user type
        real_streams = streams_df[streams_df['user_type'] == 'real']
        bot_streams = streams_df[streams_df['user_type'] == 'bot']
        
        analysis = {
            "total_streams": len(streams_df),
            "real_streams": len(real_streams),
            "bot_streams": len(bot_streams),
            "bot_percentage": (len(bot_streams) / len(streams_df)) * 100,
            
            # Completion rate analysis
            "avg_real_completion": real_streams['completion_rate'].mean() if not real_streams.empty else 0,
            "avg_bot_completion": bot_streams['completion_rate'].mean() if not bot_streams.empty else 0,
            
            # Listen duration analysis
            "avg_real_duration_sec": real_streams['listen_duration_ms'].mean() / 1000 if not real_streams.empty else 0,
            "avg_bot_duration_sec": bot_streams['listen_duration_ms'].mean() / 1000 if not bot_streams.empty else 0,
            
            # Platform analysis
            "platform_distribution": streams_df['platform'].value_counts().to_dict() if 'platform' in streams_df.columns else {},
            
            # Genre analysis
            "genre_distribution": streams_df['genre'].value_counts().to_dict() if 'genre' in streams_df.columns else {},
        }
        
        # Calculate suspicious pattern indicators
        analysis["suspicious_indicators"] = {
            "completion_rate_difference": abs(analysis["avg_real_completion"] - analysis["avg_bot_completion"]),
            "duration_variance_real": real_streams['listen_duration_ms'].std() if not real_streams.empty else 0,
            "duration_variance_bot": bot_streams['listen_duration_ms'].std() if not bot_streams.empty else 0,
        }
        
        return analysis
    
    def analyze_economic_impact(self, economic_data, engagement_data):
        """Detailed economic impact analysis"""
        print("Analyzing economic impact...")
        
        # Convert to DataFrames
        economic_df = pd.DataFrame(economic_data)
        engagement_df = pd.DataFrame(engagement_data)
        
        # Calculate revenue by user type
        real_revenue = economic_df[economic_df['user_type'] == 'real']['revenue_generated'].sum()
        bot_revenue = economic_df[economic_df['user_type'] == 'bot']['revenue_generated'].sum()
        total_revenue = real_revenue + bot_revenue
        
        # Calculate artist-level analysis
        artist_analysis = {}
        if not economic_df.empty:
            for artist in economic_df['artist'].unique():
                artist_data = economic_df[economic_df['artist'] == artist]
                artist_real = artist_data[artist_data['user_type'] == 'real']['revenue_generated'].sum()
                artist_bot = artist_data[artist_data['user_type'] == 'bot']['revenue_generated'].sum()
                
                artist_analysis[artist] = {
                    "real_revenue": artist_real,
                    "bot_revenue": artist_bot,
                    "total_revenue": artist_real + artist_bot,
                    "bot_percentage": (artist_bot / (artist_real + artist_bot)) * 100 if (artist_real + artist_bot) > 0 else 0
                }
        
        # Calculate subscription type impact
        subscription_analysis = {}
        if 'subscription_type' in economic_df.columns:
            for sub_type in economic_df['subscription_type'].unique():
                sub_data = economic_df[economic_df['subscription_type'] == sub_type]
                subscription_analysis[sub_type] = {
                    "total_revenue": sub_data['revenue_generated'].sum(),
                    "stream_count": len(sub_data),
                    "avg_revenue_per_stream": sub_data['revenue_generated'].mean()
                }
        
        # Estimate real-world scaling
        daily_scaling_factor = 365 * 1000  # Scale to represent real platform size
        
        economic_impact = {
            "simulation_totals": {
                "real_revenue": real_revenue,
                "bot_revenue": bot_revenue,
                "total_revenue": total_revenue,
                "bot_revenue_percentage": (bot_revenue / total_revenue) * 100 if total_revenue > 0 else 0
            },
            "scaled_estimates": {
                "daily_real_revenue": real_revenue * daily_scaling_factor,
                "daily_bot_revenue": bot_revenue * daily_scaling_factor,
                "annual_bot_revenue": bot_revenue * daily_scaling_factor * 365,
                "annual_revenue_loss": bot_revenue * daily_scaling_factor * 365 * 0.3  # Assuming 30% is pure loss
            },
            "artist_breakdown": artist_analysis,
            "subscription_breakdown": subscription_analysis
        }
        
        return economic_impact
    
    def detect_bot_patterns(self, engagement_data):
        """Advanced bot pattern detection"""
        print("Detecting bot patterns...")
        
        df = pd.DataFrame(engagement_data)
        
        if df.empty:
            return {}
        
        # Analyze temporal patterns
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['minute'] = df['timestamp'].dt.minute
        
        bot_data = df[df['user_type'] == 'bot']
        real_data = df[df['user_type'] == 'real']
        
        patterns = {
            "temporal_analysis": {},
            "behavioral_analysis": {},
            "technical_analysis": {}
        }
        
        # Temporal patterns
        if 'hour' in df.columns:
            patterns["temporal_analysis"] = {
                "bot_hourly_distribution": bot_data['hour'].value_counts().to_dict(),
                "real_hourly_distribution": real_data['hour'].value_counts().to_dict(),
                "bot_activity_concentration": bot_data['hour'].std() if not bot_data.empty else 0,
                "real_activity_concentration": real_data['hour'].std() if not real_data.empty else 0
            }
        
        # Behavioral patterns
        if not bot_data.empty and not real_data.empty:
            patterns["behavioral_analysis"] = {
                "avg_bot_actions_per_user": len(bot_data) / bot_data['user'].nunique(),
                "avg_real_actions_per_user": len(real_data) / real_data['user'].nunique(),
                "bot_action_variety": bot_data['action'].nunique(),
                "real_action_variety": real_data['action'].nunique()
            }
        
        # Technical patterns
        if 'platform' in df.columns:
            patterns["technical_analysis"] = {
                "bot_platform_preferences": bot_data['platform'].value_counts().to_dict(),
                "real_platform_preferences": real_data['platform'].value_counts().to_dict()
            }
        
        return patterns
    
    def create_spotify_visualizations(self, streaming_analysis, economic_impact, bot_patterns):
        """Create Spotify-specific visualizations"""
        print("Creating Spotify visualizations...")
        
        # Set style
        plt.style.use('seaborn-v0_8')
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Streaming patterns comparison
        ax1 = plt.subplot(3, 3, 1)
        user_types = ['Real Users', 'Bots']
        stream_counts = [streaming_analysis['real_streams'], streaming_analysis['bot_streams']]
        colors = ['#1DB954', '#FF6B6B']  # Spotify green and red
        
        ax1.bar(user_types, stream_counts, color=colors)
        ax1.set_title('Stream Count: Real vs Bot', fontweight='bold')
        ax1.set_ylabel('Number of Streams')
        
        # 2. Completion rate comparison
        ax2 = plt.subplot(3, 3, 2)
        completion_rates = [streaming_analysis['avg_real_completion'] * 100, 
                           streaming_analysis['avg_bot_completion'] * 100]
        
        ax2.bar(user_types, completion_rates, color=colors)
        ax2.set_title('Average Completion Rate', fontweight='bold')
        ax2.set_ylabel('Completion Rate (%)')
        ax2.axhline(y=80, color='black', linestyle='--', alpha=0.5, label='80% threshold')
        ax2.legend()
        
        # 3. Revenue distribution pie chart
        ax3 = plt.subplot(3, 3, 3)
        revenue_values = [economic_impact['simulation_totals']['real_revenue'],
                         economic_impact['simulation_totals']['bot_revenue']]
        
        ax3.pie(revenue_values, labels=user_types, autopct='%1.1f%%', colors=colors, startangle=90)
        ax3.set_title('Revenue Distribution', fontweight='bold')
        
        # 4. Artist revenue breakdown
        ax4 = plt.subplot(3, 3, 4)
        artist_data = economic_impact['artist_breakdown']
        if artist_data:
            artists = list(artist_data.keys())[:10]  # Top 10 artists
            bot_percentages = [artist_data[artist]['bot_percentage'] for artist in artists]
            
            ax4.barh(artists, bot_percentages, color='#FF6B6B')
            ax4.set_title('Bot Revenue % by Artist (Top 10)', fontweight='bold')
            ax4.set_xlabel('Bot Revenue Percentage')
        
        # 5. Platform distribution
        ax5 = plt.subplot(3, 3, 5)
        platform_dist = streaming_analysis.get('platform_distribution', {})
        if platform_dist:
            platforms = list(platform_dist.keys())
            counts = list(platform_dist.values())
            
            ax5.pie(counts, labels=platforms, autopct='%1.1f%%', startangle=90)
            ax5.set_title('Platform Distribution', fontweight='bold')
        
        # 6. Genre analysis
        ax6 = plt.subplot(3, 3, 6)
        genre_dist = streaming_analysis.get('genre_distribution', {})
        if genre_dist:
            genres = list(genre_dist.keys())[:8]  # Top 8 genres
            counts = [genre_dist[genre] for genre in genres]
            
            ax6.bar(genres, counts, color=plt.cm.Set3(np.linspace(0, 1, len(genres))))
            ax6.set_title('Top Genres by Stream Count', fontweight='bold')
            ax6.tick_params(axis='x', rotation=45)
            ax6.set_ylabel('Stream Count')
        
        # 7. Economic scaling projection
        ax7 = plt.subplot(3, 3, 7)
        time_periods = ['Daily', 'Weekly', 'Monthly', 'Annual']
        real_scaled = [
            economic_impact['scaled_estimates']['daily_real_revenue'],
            economic_impact['scaled_estimates']['daily_real_revenue'] * 7,
            economic_impact['scaled_estimates']['daily_real_revenue'] * 30,
            economic_impact['scaled_estimates']['daily_real_revenue'] * 365
        ]
        bot_scaled = [
            economic_impact['scaled_estimates']['daily_bot_revenue'],
            economic_impact['scaled_estimates']['daily_bot_revenue'] * 7,
            economic_impact['scaled_estimates']['daily_bot_revenue'] * 30,
            economic_impact['scaled_estimates']['annual_bot_revenue']
        ]
        
        x = np.arange(len(time_periods))
        width = 0.35
        
        ax7.bar(x - width/2, real_scaled, width, label='Real Revenue', color='#1DB954')
        ax7.bar(x + width/2, bot_scaled, width, label='Bot Revenue', color='#FF6B6B')
        
        ax7.set_title('Scaled Revenue Projections', fontweight='bold')
        ax7.set_ylabel('Revenue (USD)')
        ax7.set_xticks(x)
        ax7.set_xticklabels(time_periods)
        ax7.legend()
        ax7.set_yscale('log')  # Log scale for better visualization
        
        # 8. Subscription type analysis
        ax8 = plt.subplot(3, 3, 8)
        sub_data = economic_impact['subscription_breakdown']
        if sub_data:
            sub_types = list(sub_data.keys())
            revenues = [sub_data[sub]['total_revenue'] for sub in sub_types]
            
            ax8.bar(sub_types, revenues, color=['#1DB954', '#FFD700'])  # Green for premium, gold for free
            ax8.set_title('Revenue by Subscription Type', fontweight='bold')
            ax8.set_ylabel('Revenue (USD)')
        
        # 9. Detection risk indicators
        ax9 = plt.subplot(3, 3, 9)
        risk_metrics = ['Completion Rate\nDifference', 'Duration Variance\nDifference', 'Bot Activity\nConcentration']
        risk_values = [
            streaming_analysis['suspicious_indicators']['completion_rate_difference'],
            abs(streaming_analysis['suspicious_indicators']['duration_variance_bot'] - 
                streaming_analysis['suspicious_indicators']['duration_variance_real']) / 1000000,  # Scale down
            bot_patterns.get('temporal_analysis', {}).get('bot_activity_concentration', 0)
        ]
        
        colors_risk = ['#FF6B6B', '#FFA500', '#FFD700']
        ax9.bar(risk_metrics, risk_values, color=colors_risk)
        ax9.set_title('Bot Detection Risk Indicators', fontweight='bold')
        ax9.set_ylabel('Risk Score')
        
        plt.tight_layout()
        os.makedirs("../results", exist_ok=True)
        plt.savefig('../results/spotify_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Spotify visualization saved to ../results/spotify_analysis.png")
    
    def generate_spotify_report(self):
        """Generate comprehensive Spotify analysis report"""
        print("Generating Spotify analysis report...")
        
        # Load data
        engagement_data, economic_data, summary_data = self.load_spotify_data()
        
        if not engagement_data:
            print("No Spotify data found. Please run the Spotify simulation first.")
            return
        
        # Run analyses
        streaming_analysis = self.analyze_streaming_patterns(engagement_data)
        economic_impact = self.analyze_economic_impact(economic_data, engagement_data)
        bot_patterns = self.detect_bot_patterns(engagement_data)
        
        # Create visualizations
        self.create_spotify_visualizations(streaming_analysis, economic_impact, bot_patterns)
        
        # Generate report
        report = f"""
# Spotify Bot Economics Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This analysis examines {len(engagement_data):,} engagement events from Spotify simulation data,
revealing significant bot activity and its economic implications.

### Key Findings
- **Bot Activity**: {streaming_analysis.get('bot_percentage', 0):.1f}% of all streams are from bots
- **Revenue Impact**: ${economic_impact['simulation_totals']['bot_revenue']:.4f} generated by bots ({economic_impact['simulation_totals']['bot_revenue_percentage']:.1f}% of total)
- **Completion Rates**: Bots show {streaming_analysis.get('avg_bot_completion', 0)*100:.1f}% vs Real users {streaming_analysis.get('avg_real_completion', 0)*100:.1f}%

## Streaming Pattern Analysis

### Overall Activity
- Total Streams: {streaming_analysis.get('total_streams', 0):,}
- Real User Streams: {streaming_analysis.get('real_streams', 0):,}
- Bot Streams: {streaming_analysis.get('bot_streams', 0):,}

### Listen Duration Patterns
- Average Real User Duration: {streaming_analysis.get('avg_real_duration_sec', 0):.1f} seconds
- Average Bot Duration: {streaming_analysis.get('avg_bot_duration_sec', 0):.1f} seconds
- Duration Difference: {abs(streaming_analysis.get('avg_real_duration_sec', 0) - streaming_analysis.get('avg_bot_duration_sec', 0)):.1f} seconds

## Economic Impact Analysis

### Revenue Distribution
- Real User Revenue: ${economic_impact['simulation_totals']['real_revenue']:.4f}
- Bot Revenue: ${economic_impact['simulation_totals']['bot_revenue']:.4f}
- Total Revenue: ${economic_impact['simulation_totals']['total_revenue']:.4f}

### Scaled Projections (Real-world estimates)
- Annual Bot Revenue: ${economic_impact['scaled_estimates']['annual_bot_revenue']:,.2f}
- Estimated Annual Loss: ${economic_impact['scaled_estimates']['annual_revenue_loss']:,.2f}

### Top Affected Artists
"""
        
        # Add artist analysis
        artist_data = economic_impact['artist_breakdown']
        if artist_data:
            sorted_artists = sorted(artist_data.items(), 
                                  key=lambda x: x[1]['bot_percentage'], reverse=True)[:5]
            
            for artist, data in sorted_artists:
                report += f"- {artist}: {data['bot_percentage']:.1f}% bot revenue (${data['bot_revenue']:.4f})\n"
        
        report += f"""

## Bot Detection Indicators

### Suspicious Patterns Detected
- Completion Rate Anomaly: {streaming_analysis['suspicious_indicators']['completion_rate_difference']:.3f}
- Duration Variance (Real): {streaming_analysis['suspicious_indicators']['duration_variance_real']/1000:.1f}s
- Duration Variance (Bot): {streaming_analysis['suspicious_indicators']['duration_variance_bot']/1000:.1f}s

### Platform Analysis
"""
        
        # Add platform distribution
        platform_dist = streaming_analysis.get('platform_distribution', {})
        for platform, count in platform_dist.items():
            percentage = (count / streaming_analysis['total_streams']) * 100
            report += f"- {platform}: {count:,} streams ({percentage:.1f}%)\n"
        
        report += f"""

## Recommendations

### For Spotify Platform
1. **Enhanced Detection**: Focus on completion rate patterns and duration anomalies
2. **Geographic Analysis**: Monitor regional streaming patterns for coordinated activity
3. **Premium Account Monitoring**: Implement stricter verification for premium accounts

### For Artists and Labels
1. **Organic Growth**: Avoid bot services despite apparent short-term benefits
2. **Engagement Quality**: Focus on listener retention rather than raw stream counts
3. **Regional Strategy**: Develop authentic fan bases in key markets

### For Researchers
1. **Longitudinal Studies**: Track bot evolution and platform countermeasures
2. **Cross-Platform Analysis**: Compare bot behavior across streaming services
3. **Economic Modeling**: Refine cost-benefit models for different stakeholders

## Technical Notes

### Simulation Parameters
- Artists: {summary_data.get('simulation_parameters', {}).get('tracks', 'N/A')} tracks analyzed
- Real Users: {summary_data.get('simulation_parameters', {}).get('real_users', 'N/A')}
- Bots: {summary_data.get('simulation_parameters', {}).get('bots', 'N/A')}
- Simulation Steps: {summary_data.get('simulation_parameters', {}).get('steps', 'N/A')}

### Limitations
- Simulation based on estimated parameters
- Real bot behavior may be more sophisticated
- Platform detection capabilities continuously evolving
- Regional and cultural factors not fully modeled

---

*Analysis conducted for MATSE research at RWTH Aachen University*
*Software Engineering Chair - Bot Economics Research*
"""
        
        # Save report
        os.makedirs("../results", exist_ok=True)
        with open("../results/spotify_detailed_analysis.md", "w") as f:
            f.write(report)
        
        print(f"✅ Spotify analysis complete!")
        print(f"📊 Report saved to: ../results/spotify_detailed_analysis.md")
        print(f"📈 Visualization saved to: ../results/spotify_analysis.png")
        
        return report

def main():
    """Main execution function"""
    print("🎵 Spotify Bot Economics Analyzer")
    print("=" * 50)
    
    analyzer = SpotifyEconomicsAnalyzer()
    analyzer.generate_spotify_report()

if __name__ == "__main__":
    main()

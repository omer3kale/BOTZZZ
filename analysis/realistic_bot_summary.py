import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def load_realistic_data():
    """Load realistic simulation data and generate comprehensive summary"""
    
    # Load Spotify realistic data
    print("Loading realistic bot simulation data...")
    
    try:
        with open("../data/spotify_realistic_simulation.json", "r") as f:
            spotify_data = json.load(f)
        print("✓ Loaded Spotify realistic simulation data")
    except FileNotFoundError:
        print("⚠ Spotify realistic data not found")
        spotify_data = None
    
    try:
        with open("../data/youtube_realistic_simulation.json", "r") as f:
            youtube_data = json.load(f)
        print("✓ Loaded YouTube realistic simulation data")
    except FileNotFoundError:
        print("⚠ YouTube realistic data not found") 
        youtube_data = None
    
    try:
        with open("../data/spotify_detection_events.json", "r") as f:
            spotify_detection = json.load(f)
        print("✓ Loaded Spotify detection events")
    except FileNotFoundError:
        print("⚠ Spotify detection data not found")
        spotify_detection = []
    
    return spotify_data, youtube_data, spotify_detection

def analyze_bot_sophistication(platform_data, platform_name):
    """Analyze bot sophistication for a given platform"""
    
    if not platform_data or "bots" not in platform_data:
        return {"error": f"No bot data available for {platform_name}"}
    
    analysis = {
        "platform": platform_name,
        "total_bots": len(platform_data["bots"]),
        "bot_types": {},
        "geographic_distribution": {},
        "device_profiles": {},
        "evasion_techniques": {},
        "economic_impact": platform_data.get("economic_summary", {}) if platform_name == "spotify" else platform_data.get("revenue_analysis", {})
    }
    
    # Analyze bot types
    for bot in platform_data["bots"]:
        bot_type = bot["bot_type"]
        if bot_type not in analysis["bot_types"]:
            analysis["bot_types"][bot_type] = {
                "count": 0,
                "description": bot.get("bot_description", ""),
                "avg_daily_quota": 0,
                "evasion_techniques": [],
                "countries": []
            }
        
        stats = analysis["bot_types"][bot_type]
        stats["count"] += 1
        stats["avg_daily_quota"] += bot.get("daily_quota", bot.get("daily_stream_quota", 0))
        
        if "evasion_techniques" in bot:
            stats["evasion_techniques"].extend(bot["evasion_techniques"])
        
        # Geographic analysis
        location = bot.get("location", bot.get("farm_location", {}))
        country = location.get("country", "Unknown")
        stats["countries"].append(country)
        
        if country not in analysis["geographic_distribution"]:
            analysis["geographic_distribution"][country] = 0
        analysis["geographic_distribution"][country] += 1
        
        # Device profile analysis
        device = bot.get("device_profile", {})
        device_type = device.get("device", device.get("platform", "Unknown"))
        if device_type not in analysis["device_profiles"]:
            analysis["device_profiles"][device_type] = 0
        analysis["device_profiles"][device_type] += 1
    
    # Calculate averages and unique counts
    for bot_type, stats in analysis["bot_types"].items():
        if stats["count"] > 0:
            stats["avg_daily_quota"] = round(stats["avg_daily_quota"] / stats["count"], 1)
            stats["unique_evasion_techniques"] = len(set(stats["evasion_techniques"]))
            stats["unique_countries"] = len(set(stats["countries"]))
    
    return analysis

def analyze_engagement_patterns(platform_data, platform_name):
    """Analyze engagement patterns from realistic data"""
    
    if not platform_data or "engagement_log" not in platform_data:
        return {"error": f"No engagement data available for {platform_name}"}
    
    engagement_df = pd.DataFrame(platform_data["engagement_log"])
    
    analysis = {
        "platform": platform_name,
        "total_events": len(engagement_df),
        "real_user_events": len(engagement_df[engagement_df["user_type"] == "real"]),
        "bot_events": len(engagement_df[engagement_df["user_type"] == "bot"]),
        "bot_percentage": 0,
        "action_distribution": {},
        "bot_type_activity": {},
        "temporal_patterns": {}
    }
    
    if analysis["total_events"] > 0:
        analysis["bot_percentage"] = round((analysis["bot_events"] / analysis["total_events"]) * 100, 2)
    
    # Action distribution
    action_counts = engagement_df["action"].value_counts()
    analysis["action_distribution"] = action_counts.to_dict()
    
    # Bot type activity
    bot_data = engagement_df[engagement_df["user_type"] == "bot"]
    if not bot_data.empty and "bot_type" in bot_data.columns:
        bot_type_counts = bot_data["bot_type"].value_counts()
        analysis["bot_type_activity"] = bot_type_counts.to_dict()
    
    # Temporal patterns
    engagement_df['timestamp'] = pd.to_datetime(engagement_df['timestamp'])
    engagement_df['hour'] = engagement_df['timestamp'].dt.hour
    hourly_activity = engagement_df['hour'].value_counts().sort_index()
    analysis["temporal_patterns"] = hourly_activity.to_dict()
    
    return analysis

def create_summary_visualization(spotify_analysis, youtube_analysis, spotify_patterns, youtube_patterns):
    """Create comprehensive summary visualization"""
    
    plt.style.use('default')
    fig = plt.figure(figsize=(20, 12))
    
    # 1. Bot Count Comparison
    plt.subplot(2, 4, 1)
    platforms = []
    bot_counts = []
    
    if spotify_analysis and "total_bots" in spotify_analysis:
        platforms.append("Spotify")
        bot_counts.append(spotify_analysis["total_bots"])
    
    if youtube_analysis and "total_bots" in youtube_analysis:
        platforms.append("YouTube")
        bot_counts.append(youtube_analysis["total_bots"])
    
    if platforms:
        plt.bar(platforms, bot_counts, color=['#1DB954', '#FF0000'])
        plt.title('Total Bots by Platform', fontweight='bold')
        plt.ylabel('Number of Bots')
    
    # 2. Bot Type Distribution - Spotify
    plt.subplot(2, 4, 2)
    if spotify_analysis and "bot_types" in spotify_analysis:
        bot_types = list(spotify_analysis["bot_types"].keys())
        counts = [spotify_analysis["bot_types"][bt]["count"] for bt in bot_types]
        colors = plt.cm.Set3(np.linspace(0, 1, len(bot_types)))
        
        plt.pie(counts, labels=bot_types, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Spotify Bot Types', fontweight='bold')
    
    # 3. Bot Type Distribution - YouTube
    plt.subplot(2, 4, 3)
    if youtube_analysis and "bot_types" in youtube_analysis:
        bot_types = list(youtube_analysis["bot_types"].keys())
        counts = [youtube_analysis["bot_types"][bt]["count"] for bt in bot_types]
        colors = plt.cm.Set2(np.linspace(0, 1, len(bot_types)))
        
        plt.pie(counts, labels=bot_types, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('YouTube Bot Types', fontweight='bold')
    
    # 4. Geographic Distribution
    plt.subplot(2, 4, 4)
    all_countries = {}
    
    if spotify_analysis and "geographic_distribution" in spotify_analysis:
        for country, count in spotify_analysis["geographic_distribution"].items():
            all_countries[country] = all_countries.get(country, 0) + count
    
    if youtube_analysis and "geographic_distribution" in youtube_analysis:
        for country, count in youtube_analysis["geographic_distribution"].items():
            all_countries[country] = all_countries.get(country, 0) + count
    
    if all_countries:
        top_countries = dict(sorted(all_countries.items(), key=lambda x: x[1], reverse=True)[:8])
        plt.barh(list(top_countries.keys()), list(top_countries.values()), color='#FFB6C1')
        plt.title('Bot Farm Geographic Distribution', fontweight='bold')
        plt.xlabel('Number of Bots')
    
    # 5. Engagement Activity Comparison
    plt.subplot(2, 4, 5)
    if spotify_patterns and youtube_patterns:
        activities = ["Real Users", "Bots"]
        spotify_data = [spotify_patterns.get("real_user_events", 0), spotify_patterns.get("bot_events", 0)]
        youtube_data = [youtube_patterns.get("real_user_events", 0), youtube_patterns.get("bot_events", 0)]
        
        x = np.arange(len(activities))
        width = 0.35
        
        plt.bar(x - width/2, spotify_data, width, label='Spotify', color='#1DB954')
        plt.bar(x + width/2, youtube_data, width, label='YouTube', color='#FF0000')
        
        plt.xlabel('User Type')
        plt.ylabel('Number of Events')
        plt.title('Engagement Activity Comparison', fontweight='bold')
        plt.xticks(x, activities)
        plt.legend()
    
    # 6. Bot Activity Percentage
    plt.subplot(2, 4, 6)
    platforms = []
    bot_percentages = []
    
    if spotify_patterns and "bot_percentage" in spotify_patterns:
        platforms.append("Spotify")
        bot_percentages.append(spotify_patterns["bot_percentage"])
    
    if youtube_patterns and "bot_percentage" in youtube_patterns:
        platforms.append("YouTube")
        bot_percentages.append(youtube_patterns["bot_percentage"])
    
    if platforms:
        colors = ['#FF6B6B' if p > 30 else '#FFE66D' if p > 20 else '#95E1D3' for p in bot_percentages]
        plt.bar(platforms, bot_percentages, color=colors)
        plt.title('Bot Activity Percentage', fontweight='bold')
        plt.ylabel('Bot Activity (%)')
        plt.axhline(y=30, color='red', linestyle='--', alpha=0.7, label='High Risk (30%)')
        plt.axhline(y=20, color='orange', linestyle='--', alpha=0.7, label='Medium Risk (20%)')
        plt.legend()
    
    # 7. Economic Impact (Spotify)
    plt.subplot(2, 4, 7)
    if spotify_analysis and "economic_impact" in spotify_analysis:
        economic = spotify_analysis["economic_impact"]
        
        categories = ['Real Revenue', 'Bot Revenue']
        real_rev = economic.get("revenue_analysis", {}).get("total_real_revenue", 0)
        bot_rev = economic.get("revenue_analysis", {}).get("total_bot_revenue", 0)
        revenues = [real_rev, bot_rev]
        
        plt.bar(categories, revenues, color=['#95E1D3', '#FF6B6B'])
        plt.title('Spotify Revenue Distribution', fontweight='bold')
        plt.ylabel('Revenue ($)')
        
        # Add ROI text
        roi = economic.get("revenue_analysis", {}).get("bot_roi", 0)
        plt.text(0.5, max(revenues) * 0.8, f'Bot ROI: {roi:.1f}%', 
                ha='center', fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    # 8. Detection Events
    plt.subplot(2, 4, 8)
    detection_data = []
    labels = []
    
    if spotify_analysis and "economic_impact" in spotify_analysis:
        detection_rate = spotify_analysis["economic_impact"].get("detection_analysis", {}).get("detection_rate", 0)
        if detection_rate > 0:
            detection_data.append(detection_rate)
            labels.append("Spotify")
    
    if youtube_analysis:
        # YouTube detection events from metadata
        metadata = youtube_analysis.get("metadata", {})
        detection_count = metadata.get("detection_events_count", 0)
        if detection_count > 0:
            # Estimate detection rate
            total_bot_events = youtube_patterns.get("bot_events", 1) if youtube_patterns else 1
            detection_rate = (detection_count / total_bot_events) * 100
            detection_data.append(detection_rate)
            labels.append("YouTube")
    
    if detection_data:
        plt.bar(labels, detection_data, color=['#DDA0DD', '#FFB347'])
        plt.title('Detection Rate by Platform', fontweight='bold')
        plt.ylabel('Detection Rate (%)')
    
    plt.tight_layout()
    
    # Save visualization
    os.makedirs("../analysis_results", exist_ok=True)
    plt.savefig("../analysis_results/realistic_bot_summary.png", dpi=300, bbox_inches='tight')
    print("✓ Summary visualization saved")
    
    plt.show()

def generate_summary_report(spotify_analysis, youtube_analysis, spotify_patterns, youtube_patterns, spotify_detection):
    """Generate comprehensive markdown summary report"""
    
    report_content = f"""# Realistic Bot Behavior Analysis Summary

## Executive Summary
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This report analyzes sophisticated bot behavior patterns across Spotify and YouTube platforms using realistic simulation data based on actual bot research.

## Key Findings

### Platform Comparison
"""
    
    if spotify_analysis and youtube_analysis:
        report_content += f"""
| Metric | Spotify | YouTube |
|--------|---------|---------|
| Total Bots | {spotify_analysis.get('total_bots', 'N/A')} | {youtube_analysis.get('total_bots', 'N/A')} |
| Bot Activity % | {spotify_patterns.get('bot_percentage', 'N/A')}% | {youtube_patterns.get('bot_percentage', 'N/A')}% |
| Total Events | {spotify_patterns.get('total_events', 'N/A'):,} | {youtube_patterns.get('total_events', 'N/A'):,} |
"""
    
    # Spotify Analysis
    if spotify_analysis:
        report_content += f"""
### Spotify Analysis

**Bot Sophistication Levels:**
"""
        
        for bot_type, data in spotify_analysis.get("bot_types", {}).items():
            report_content += f"""
- **{bot_type}** ({data['count']} bots)
  - Description: {data['description']}
  - Avg Daily Quota: {data['avg_daily_quota']} streams
  - Evasion Techniques: {data['unique_evasion_techniques']}
  - Geographic Spread: {data['unique_countries']} countries
"""
        
        economic = spotify_analysis.get("economic_impact", {})
        if economic:
            revenue_analysis = economic.get("revenue_analysis", {})
            report_content += f"""
**Economic Impact:**
- Bot Revenue Share: {revenue_analysis.get('bot_revenue_percentage', 0):.1f}%
- Bot ROI: {revenue_analysis.get('bot_roi', 0):.1f}%
- Detection Rate: {economic.get('detection_analysis', {}).get('detection_rate', 0):.1f}%
- Total Detection Events: {len(spotify_detection):,}
"""
    
    # YouTube Analysis
    if youtube_analysis:
        report_content += f"""
### YouTube Analysis

**Bot Sophistication Levels:**
"""
        
        for bot_type, data in youtube_analysis.get("bot_types", {}).items():
            report_content += f"""
- **{bot_type}** ({data['count']} bots)
  - Description: {data['description']}
  - Avg Daily Quota: {data['avg_daily_quota']} actions
  - Evasion Techniques: {data['unique_evasion_techniques']}
  - Geographic Spread: {data['unique_countries']} countries
"""
        
        revenue_analysis = youtube_analysis.get("economic_impact", {})
        if revenue_analysis:
            report_content += f"""
**Economic Impact:**
- Bot Revenue Inflation: {revenue_analysis.get('bot_inflation_factor', 0)*100:.1f}%
- Estimated Ad Revenue: ${revenue_analysis.get('estimated_ad_revenue', 0):.2f}
- Bot vs Real Views: {revenue_analysis.get('bot_views', 0):,} vs {revenue_analysis.get('real_user_views', 0):,}
"""
    
    # Geographic Analysis
    report_content += f"""
### Geographic Bot Farm Distribution

**Top Bot Farm Locations:**
"""
    
    all_countries = {}
    if spotify_analysis:
        for country, count in spotify_analysis.get("geographic_distribution", {}).items():
            all_countries[country] = all_countries.get(country, 0) + count
    
    if youtube_analysis:
        for country, count in youtube_analysis.get("geographic_distribution", {}).items():
            all_countries[country] = all_countries.get(country, 0) + count
    
    top_countries = sorted(all_countries.items(), key=lambda x: x[1], reverse=True)[:10]
    for country, count in top_countries:
        country_names = {
            'BD': 'Bangladesh', 'PK': 'Pakistan', 'ID': 'Indonesia', 'PH': 'Philippines',
            'NG': 'Nigeria', 'VN': 'Vietnam', 'RU': 'Russia', 'CN': 'China', 'IN': 'India'
        }
        full_name = country_names.get(country, country)
        report_content += f"- {full_name} ({country}): {count} bots\n"
    
    # Recommendations
    report_content += f"""
### Detection & Mitigation Recommendations

#### Immediate Actions
- **High Priority**: Implement behavioral pattern analysis for consistency detection
- **Medium Priority**: Deploy geographic clustering detection algorithms
- **Ongoing**: Monitor daily quota anomalies and suspicious activity bursts

#### Platform-Specific Recommendations

**Spotify:**
- Focus on premium farm detection (highest ROI bots)
- Implement stream duration analysis (minimal 30-second threshold)
- Monitor playlist manipulation patterns

**YouTube:**
- Enhance comment pattern analysis for generic/coordinated content
- Deploy engagement pod detection algorithms
- Implement subscriber farm detection based on watch time vs subscription correlation

#### Long-term Strategy
- Develop cross-platform bot intelligence sharing
- Implement machine learning-based behavioral analysis
- Create industry-wide bot detection standards
- Establish economic impact assessment frameworks

---
*Report generated by Realistic Bot Analyzer*
"""
    
    # Save report
    os.makedirs("../analysis_results", exist_ok=True)
    with open("../analysis_results/realistic_bot_summary_report.md", "w") as f:
        f.write(report_content)
    
    print("✓ Summary report saved")
    return report_content

def main():
    print("="*60)
    print("REALISTIC BOT BEHAVIOR ANALYSIS SUMMARY")
    print("="*60)
    
    # Load data
    spotify_data, youtube_data, spotify_detection = load_realistic_data()
    
    # Analyze bot sophistication
    print("\nAnalyzing bot sophistication patterns...")
    spotify_analysis = analyze_bot_sophistication(spotify_data, "spotify") if spotify_data else None
    youtube_analysis = analyze_bot_sophistication(youtube_data, "youtube") if youtube_data else None
    
    # Analyze engagement patterns
    print("Analyzing engagement patterns...")
    spotify_patterns = analyze_engagement_patterns(spotify_data, "spotify") if spotify_data else None
    youtube_patterns = analyze_engagement_patterns(youtube_data, "youtube") if youtube_data else None
    
    # Create visualizations
    print("Creating summary visualizations...")
    create_summary_visualization(spotify_analysis, youtube_analysis, spotify_patterns, youtube_patterns)
    
    # Generate report
    print("Generating comprehensive summary report...")
    report = generate_summary_report(spotify_analysis, youtube_analysis, spotify_patterns, youtube_patterns, spotify_detection)
    
    # Print key insights
    print("\n" + "="*60)
    print("KEY INSIGHTS SUMMARY")
    print("="*60)
    
    if spotify_analysis and spotify_patterns:
        print(f"\nSPOTIFY:")
        print(f"  Total Bots: {spotify_analysis['total_bots']}")
        print(f"  Bot Activity: {spotify_patterns['bot_percentage']}%")
        
        economic = spotify_analysis.get("economic_impact", {})
        if economic:
            revenue_analysis = economic.get("revenue_analysis", {})
            print(f"  Bot Revenue Share: {revenue_analysis.get('bot_revenue_percentage', 0):.1f}%")
            print(f"  Bot ROI: {revenue_analysis.get('bot_roi', 0):.1f}%")
    
    if youtube_analysis and youtube_patterns:
        print(f"\nYOUTUBE:")
        print(f"  Total Bots: {youtube_analysis['total_bots']}")
        print(f"  Bot Activity: {youtube_patterns['bot_percentage']}%")
        
        revenue_analysis = youtube_analysis.get("economic_impact", {})
        if revenue_analysis:
            print(f"  Revenue Inflation: {revenue_analysis.get('bot_inflation_factor', 0)*100:.1f}%")
    
    print(f"\nDETECTION EVENTS:")
    print(f"  Spotify: {len(spotify_detection):,} events")
    
    print(f"\nOUTPUT FILES:")
    print(f"  📊 Visualization: analysis_results/realistic_bot_summary.png")
    print(f"  📄 Report: analysis_results/realistic_bot_summary_report.md")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

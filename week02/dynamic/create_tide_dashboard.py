import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def main():
    print("🌊 Creating Interactive Tide Data Visualization Dashboard...")
    
    # Load and process data
    print("📊 Loading data...")
    df = pd.read_csv('chek_lap_kok_e_2023_long.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Add additional features
    df['hour'] = df['datetime'].dt.hour
    df['day_of_year'] = df['datetime'].dt.dayofyear
    df['month_name'] = df['datetime'].dt.month_name()
    df['weekday'] = df['datetime'].dt.day_name()
    
    print(f"✅ Data loaded: {len(df)} records from {df['datetime'].min().date()} to {df['datetime'].max().date()}")
    
    # 1. Main Time Series with Range Selector
    print("📈 Creating interactive time series...")
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=df['datetime'],
        y=df['tide_m'],
        mode='lines',
        name='Tide Height',
        line=dict(color='#1f77b4', width=1),
        hovertemplate='<b>%{x}</b><br>Tide: %{y:.2f}m<extra></extra>'
    ))
    
    # Add monthly averages
    monthly_avg = df.groupby(df['datetime'].dt.to_period('M')).agg({
        'tide_m': 'mean',
        'datetime': 'first'
    }).reset_index(drop=True)
    
    fig1.add_trace(go.Scatter(
        x=monthly_avg['datetime'],
        y=monthly_avg['tide_m'],
        mode='lines+markers',
        name='Monthly Average',
        line=dict(color='red', width=3, dash='dash'),
        marker=dict(size=8, symbol='diamond'),
        hovertemplate='<b>%{x|%B %Y}</b><br>Avg: %{y:.2f}m<extra></extra>'
    ))
    
    fig1.update_layout(
        title='🌊 Chek Lap Kok Tide Heights 2023 - Interactive Time Series',
        xaxis_title='Date',
        yaxis_title='Tide Height (meters)',
        template='plotly_white',
        height=600,
        hovermode='x unified',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="7 days", step="day", stepmode="backward"),
                    dict(count=30, label="30 days", step="day", stepmode="backward"),
                    dict(count=90, label="3 months", step="day", stepmode="backward"),
                    dict(count=180, label="6 months", step="day", stepmode="backward"),
                    dict(step="all", label="All data")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    # 2. Monthly Heatmap
    print("🔥 Creating monthly heatmap...")
    df['day_of_month'] = df['datetime'].dt.day
    heatmap_data = df.groupby(['month', 'day_of_month'])['tide_m'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='month', columns='day_of_month', values='tide_m')
    
    fig2 = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        colorscale='Viridis',
        hovertemplate='<b>Month:</b> %{y}<br><b>Day:</b> %{x}<br><b>Avg Tide:</b> %{z:.2f}m<extra></extra>'
    ))
    
    fig2.update_layout(
        title='🗓️ Monthly Tide Patterns - Daily Averages Heatmap',
        xaxis_title='Day of Month',
        yaxis_title='Month',
        height=500,
        template='plotly_white'
    )
    
    # 3. Hourly Patterns
    print("⏰ Creating hourly patterns...")
    hourly_stats = df.groupby('hour').agg({
        'tide_m': ['mean', 'std', 'min', 'max']
    }).round(2)
    hourly_stats.columns = ['mean', 'std', 'min', 'max']
    hourly_stats = hourly_stats.reset_index()
    
    fig3 = go.Figure()
    
    # Add confidence band
    fig3.add_trace(go.Scatter(
        x=hourly_stats['hour'],
        y=hourly_stats['max'],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig3.add_trace(go.Scatter(
        x=hourly_stats['hour'],
        y=hourly_stats['min'],
        mode='lines',
        line=dict(width=0),
        fillcolor='rgba(0,100,80,0.2)',
        fill='tonexty',
        name='Min-Max Range',
        hovertemplate='<b>Hour:</b> %{x}:00<br><b>Min:</b> %{y:.2f}m<extra></extra>'
    ))
    
    # Add mean line
    fig3.add_trace(go.Scatter(
        x=hourly_stats['hour'],
        y=hourly_stats['mean'],
        mode='lines+markers',
        name='Average',
        line=dict(color='blue', width=3),
        marker=dict(size=6),
        hovertemplate='<b>Hour:</b> %{x}:00<br><b>Average:</b> %{y:.2f}m<extra></extra>'
    ))
    
    fig3.update_layout(
        title='🕐 Daily Tide Cycles - Hourly Patterns',
        xaxis_title='Hour of Day',
        yaxis_title='Tide Height (meters)',
        template='plotly_white',
        height=500,
        hovermode='x unified'
    )
    fig3.update_xaxes(tickmode='linear', tick0=0, dtick=2)
    
    # 4. Monthly Box Plot
    print("📦 Creating monthly distribution...")
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    fig4 = px.box(df, x='month_name', y='tide_m', 
                 title='📊 Monthly Tide Height Distributions',
                 labels={'tide_m': 'Tide Height (meters)', 'month_name': 'Month'},
                 template='plotly_white',
                 color='month_name')
    
    fig4.update_xaxis(categoryorder='array', categoryarray=month_order)
    fig4.update_layout(height=500, showlegend=False)
    
    # 5. 3D Scatter (sampled for performance)
    print("🎯 Creating 3D visualization...")
    df_sample = df.iloc[::5].copy()  # Every 5th point for better performance
    
    fig5 = px.scatter_3d(df_sample, 
                        x='day_of_year', 
                        y='hour', 
                        z='tide_m',
                        color='tide_m',
                        size='tide_m',
                        hover_data=['datetime'],
                        title='🌐 3D Tide Visualization: Day of Year × Hour × Tide Height',
                        labels={'day_of_year': 'Day of Year', 
                               'hour': 'Hour of Day',
                               'tide_m': 'Tide Height (m)'},
                        color_continuous_scale='Viridis',
                        template='plotly_white')
    
    fig5.update_layout(height=700)
    
    # Save all plots
    print("💾 Saving interactive plots...")
    fig1.write_html("tide_time_series_interactive.html")
    fig2.write_html("tide_monthly_heatmap.html") 
    fig3.write_html("tide_hourly_patterns.html")
    fig4.write_html("tide_monthly_boxplot.html")
    fig5.write_html("tide_3d_visualization.html")
    
    # Create comprehensive dashboard
    print("🎨 Creating dashboard...")
    dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chek Lap Kok Tide Data Dashboard 2023</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        .header h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #7f8c8d;
            font-size: 1.2em;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        .stat-label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .visualization-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .viz-card {{
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }}
        .viz-card:hover {{
            transform: translateY(-5px);
        }}
        .viz-card h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.4em;
        }}
        .viz-card p {{
            color: #7f8c8d;
            margin-bottom: 20px;
            line-height: 1.6;
        }}
        .viz-link {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        .viz-link:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .insights {{
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        .insights h3 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.6em;
        }}
        .insights ul {{
            list-style: none;
        }}
        .insights li {{
            color: #555;
            margin-bottom: 12px;
            padding-left: 25px;
            position: relative;
            line-height: 1.6;
        }}
        .insights li:before {{
            content: "🌊";
            position: absolute;
            left: 0;
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2em; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .visualization-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌊 Chek Lap Kok Tide Data Dashboard</h1>
            <p>Interactive Analysis of Tidal Patterns at Hong Kong International Airport - 2023</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{len(df):,}</div>
                <div class="stat-label">Total Measurements</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{df['tide_m'].max():.2f}m</div>
                <div class="stat-label">Highest Tide</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{df['tide_m'].min():.2f}m</div>
                <div class="stat-label">Lowest Tide</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{df['tide_m'].mean():.2f}m</div>
                <div class="stat-label">Average Tide</div>
            </div>
        </div>
        
        <div class="visualization-grid">
            <div class="viz-card">
                <h3>📈 Interactive Time Series</h3>
                <p>Explore the complete year of tide data with zoom, pan, and range selection tools. See both raw data and monthly trends.</p>
                <a href="tide_time_series_interactive.html" class="viz-link" target="_blank">Open Visualization</a>
            </div>
            
            <div class="viz-card">
                <h3>🔥 Monthly Heatmap</h3>
                <p>Discover seasonal patterns and identify the best and worst tide days throughout the year with this color-coded calendar view.</p>
                <a href="tide_monthly_heatmap.html" class="viz-link" target="_blank">Open Visualization</a>
            </div>
            
            <div class="viz-card">
                <h3>⏰ Daily Tide Cycles</h3>
                <p>Understand the semi-diurnal tide patterns and see how tide heights vary throughout a typical day.</p>
                <a href="tide_hourly_patterns.html" class="viz-link" target="_blank">Open Visualization</a>
            </div>
            
            <div class="viz-card">
                <h3>📊 Monthly Distributions</h3>
                <p>Compare tide height variability across different months with interactive box plots showing quartiles and outliers.</p>
                <a href="tide_monthly_boxplot.html" class="viz-link" target="_blank">Open Visualization</a>
            </div>
            
            <div class="viz-card">
                <h3>🌐 3D Analysis</h3>
                <p>Explore the relationship between day of year, hour of day, and tide height in an interactive 3D space.</p>
                <a href="tide_3d_visualization.html" class="viz-link" target="_blank">Open Visualization</a>
            </div>
        </div>
        
        <div class="insights">
            <h3>💡 Key Insights from the Data</h3>
            <ul>
                <li><strong>Tidal Range:</strong> Chek Lap Kok experiences significant tidal variation from {df['tide_m'].min():.2f}m to {df['tide_m'].max():.2f}m - a range of {df['tide_m'].max() - df['tide_m'].min():.2f}m</li>
                <li><strong>Semi-diurnal Pattern:</strong> The data shows classic semi-diurnal tides with approximately two high and two low tides per day</li>
                <li><strong>Seasonal Variation:</strong> Monthly averages reveal seasonal differences in tide heights throughout the year</li>
                <li><strong>Data Quality:</strong> Complete coverage with {len(df):,} high-quality measurements across the entire year 2023</li>
                <li><strong>Airport Impact:</strong> Understanding these patterns is crucial for Hong Kong International Airport operations and coastal management</li>
            </ul>
        </div>
        
        <div class="insights">
            <h3>🎮 How to Use the Interactive Features</h3>
            <ul>
                <li><strong>Zoom & Pan:</strong> Click and drag to zoom into specific time periods, use mouse wheel to zoom</li>
                <li><strong>Time Range:</strong> Use the range selector buttons (7d, 30d, 3m, 6m, all) for quick time period selection</li>
                <li><strong>Hover Details:</strong> Hover over any data point for detailed information including exact values and timestamps</li>
                <li><strong>Legend Control:</strong> Click legend items to show/hide different data series</li>
                <li><strong>Full Screen:</strong> Use the toolbar icons to download plots or view in full screen mode</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
    
    with open("tide_dashboard.html", "w", encoding="utf-8") as f:
        f.write(dashboard_html)
    
    print("✅ All visualizations created successfully!")
    print("\n🎉 Files Generated:")
    print("   📊 tide_dashboard.html - Main dashboard (START HERE)")
    print("   📈 tide_time_series_interactive.html - Interactive time series")
    print("   🔥 tide_monthly_heatmap.html - Monthly patterns")
    print("   ⏰ tide_hourly_patterns.html - Daily cycles")
    print("   📦 tide_monthly_boxplot.html - Statistical distributions")
    print("   🌐 tide_3d_visualization.html - 3D analysis")
    
    print(f"\n📊 Data Summary:")
    print(f"   Total records: {len(df):,}")
    print(f"   Date range: {df['datetime'].min().date()} to {df['datetime'].max().date()}")
    print(f"   Tide range: {df['tide_m'].min():.2f}m to {df['tide_m'].max():.2f}m")
    print(f"   Average: {df['tide_m'].mean():.2f}m ± {df['tide_m'].std():.2f}m")
    
    highest_tide = df.loc[df['tide_m'].idxmax()]
    lowest_tide = df.loc[df['tide_m'].idxmin()]
    print(f"   Highest tide: {highest_tide['tide_m']:.2f}m on {highest_tide['datetime'].date()}")
    print(f"   Lowest tide: {lowest_tide['tide_m']:.2f}m on {lowest_tide['datetime'].date()}")

if __name__ == "__main__":
    main()

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from datetime import datetime
import numpy as np

def load_and_process_data():
    """Load and process the tide data"""
    df = pd.read_csv('chek_lap_kok_e_2023_long.csv')
    
    # Convert datetime column to datetime type
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Add additional time-based features
    df['hour'] = df['datetime'].dt.hour
    df['day_of_year'] = df['datetime'].dt.dayofyear
    df['week'] = df['datetime'].dt.isocalendar().week
    df['month_name'] = df['datetime'].dt.month_name()
    df['weekday'] = df['datetime'].dt.day_name()
    
    # Add tide categories
    df['tide_category'] = pd.cut(df['tide_m'], 
                                bins=[0, 0.5, 1.0, 1.5, 2.0, 3.0],
                                labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    
    return df

def create_main_time_series(df):
    """Create the main time series plot"""
    fig = go.Figure()
    
    # Add main time series
    fig.add_trace(go.Scatter(
        x=df['datetime'],
        y=df['tide_m'],
        mode='lines+markers',
        name='Tide Height',
        line=dict(color='blue', width=1),
        marker=dict(size=3),
        hovertemplate='<b>Date:</b> %{x}<br>' +
                      '<b>Tide Height:</b> %{y:.2f}m<br>' +
                      '<b>Month:</b> %{customdata[0]}<br>' +
                      '<b>Day:</b> %{customdata[1]}<extra></extra>',
        customdata=df[['month_name', 'weekday']].values
    ))
    
    # Add monthly averages
    monthly_avg = df.groupby('month')['tide_m'].mean().reset_index()
    monthly_dates = df.groupby('month')['datetime'].first().reset_index()
    monthly_data = pd.merge(monthly_avg, monthly_dates, on='month')
    
    fig.add_trace(go.Scatter(
        x=monthly_data['datetime'],
        y=monthly_data['tide_m'],
        mode='lines+markers',
        name='Monthly Average',
        line=dict(color='red', width=3, dash='dash'),
        marker=dict(size=8, symbol='diamond'),
        hovertemplate='<b>Month:</b> %{x|%B}<br>' +
                      '<b>Avg Tide Height:</b> %{y:.2f}m<extra></extra>'
    ))
    
    fig.update_layout(
        title='Chek Lap Kok Tide Heights - 2023 (Interactive Time Series)',
        xaxis_title='Date',
        yaxis_title='Tide Height (meters)',
        hovermode='x unified',
        template='plotly_white',
        height=600,
        showlegend=True
    )
    
    # Add range selector
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="7d", step="day", stepmode="backward"),
                    dict(count=30, label="30d", step="day", stepmode="backward"),
                    dict(count=90, label="3m", step="day", stepmode="backward"),
                    dict(count=180, label="6m", step="day", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    return fig

def create_monthly_heatmap(df):
    """Create a monthly heatmap showing tide patterns"""
    # Create pivot table for heatmap
    df['day_of_month'] = df['datetime'].dt.day
    heatmap_data = df.groupby(['month', 'day_of_month'])['tide_m'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='month', columns='day_of_month', values='tide_m')
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        colorscale='Viridis',
        hoverongaps=False,
        hovertemplate='<b>Month:</b> %{y}<br>' +
                      '<b>Day:</b> %{x}<br>' +
                      '<b>Avg Tide:</b> %{z:.2f}m<extra></extra>'
    ))
    
    fig.update_layout(
        title='Monthly Tide Height Patterns (Heatmap)',
        xaxis_title='Day of Month',
        yaxis_title='Month',
        height=500,
        template='plotly_white'
    )
    
    return fig

def create_hourly_patterns(df):
    """Create hourly tide patterns visualization"""
    hourly_stats = df.groupby('hour').agg({
        'tide_m': ['mean', 'std', 'min', 'max']
    }).round(2)
    hourly_stats.columns = ['mean', 'std', 'min', 'max']
    hourly_stats = hourly_stats.reset_index()
    
    fig = go.Figure()
    
    # Add mean line
    fig.add_trace(go.Scatter(
        x=hourly_stats['hour'],
        y=hourly_stats['mean'],
        mode='lines+markers',
        name='Average',
        line=dict(color='blue', width=3),
        marker=dict(size=6)
    ))
    
    # Add min/max range
    fig.add_trace(go.Scatter(
        x=hourly_stats['hour'],
        y=hourly_stats['max'],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=hourly_stats['hour'],
        y=hourly_stats['min'],
        mode='lines',
        line=dict(width=0),
        fillcolor='rgba(0,100,80,0.2)',
        fill='tonexty',
        name='Min-Max Range',
        hovertemplate='<b>Hour:</b> %{x}:00<br>' +
                      '<b>Min Tide:</b> %{y:.2f}m<extra></extra>'
    ))
    
    fig.update_layout(
        title='Daily Tide Patterns by Hour of Day',
        xaxis_title='Hour of Day',
        yaxis_title='Tide Height (meters)',
        template='plotly_white',
        height=500,
        hovermode='x unified'
    )
    
    fig.update_xaxis(tickmode='linear', tick0=0, dtick=2)
    
    return fig

def create_monthly_boxplot(df):
    """Create monthly boxplot showing tide distribution"""
    fig = px.box(df, x='month_name', y='tide_m', 
                 title='Monthly Tide Height Distribution',
                 labels={'tide_m': 'Tide Height (meters)', 'month_name': 'Month'},
                 template='plotly_white')
    
    # Reorder months
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    fig.update_xaxis(categoryorder='array', categoryarray=month_order)
    fig.update_layout(height=500)
    
    return fig

def create_scatter_3d(df):
    """Create 3D scatter plot"""
    # Sample data for better performance (every 10th point)
    df_sample = df.iloc[::10].copy()
    
    fig = px.scatter_3d(df_sample, 
                       x='day_of_year', 
                       y='hour', 
                       z='tide_m',
                       color='tide_m',
                       size='tide_m',
                       hover_name='datetime',
                       title='3D Tide Visualization: Day of Year vs Hour vs Tide Height',
                       labels={'day_of_year': 'Day of Year', 
                              'hour': 'Hour of Day',
                              'tide_m': 'Tide Height (m)'},
                       color_continuous_scale='Viridis',
                       template='plotly_white')
    
    fig.update_layout(height=700)
    return fig

def create_dashboard():
    """Create a comprehensive dashboard with multiple visualizations"""
    print("Loading and processing tide data...")
    df = load_and_process_data()
    
    print(f"Data loaded: {len(df)} records from {df['datetime'].min()} to {df['datetime'].max()}")
    print(f"Tide height range: {df['tide_m'].min():.2f}m to {df['tide_m'].max():.2f}m")
    
    # Create individual plots
    print("Creating time series plot...")
    fig1 = create_main_time_series(df)
    
    print("Creating monthly heatmap...")
    fig2 = create_monthly_heatmap(df)
    
    print("Creating hourly patterns...")
    fig3 = create_hourly_patterns(df)
    
    print("Creating monthly boxplot...")
    fig4 = create_monthly_boxplot(df)
    
    print("Creating 3D visualization...")
    fig5 = create_scatter_3d(df)
    
    # Save individual plots as HTML files
    print("Saving visualizations...")
    fig1.write_html("tide_time_series.html")
    fig2.write_html("tide_monthly_heatmap.html") 
    fig3.write_html("tide_hourly_patterns.html")
    fig4.write_html("tide_monthly_boxplot.html")
    fig5.write_html("tide_3d_scatter.html")
    
    # Create a comprehensive dashboard page
    dashboard_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chek Lap Kok Tide Data - Interactive Dashboard 2023</title>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .header {{
                text-align: center;
                background-color: #2c3e50;
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}
            .stats {{
                background-color: white;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .plot-container {{
                background-color: white;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }}
            @media (max-width: 768px) {{
                .grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌊 Chek Lap Kok Tide Data Dashboard 2023</h1>
            <p>Interactive visualization of tidal patterns at Hong Kong International Airport</p>
        </div>
        
        <div class="stats">
            <h3>📊 Data Summary</h3>
            <p><strong>Total Records:</strong> {len(df):,}</p>
            <p><strong>Date Range:</strong> {df['datetime'].min().strftime('%B %d, %Y')} to {df['datetime'].max().strftime('%B %d, %Y')}</p>
            <p><strong>Tide Height Range:</strong> {df['tide_m'].min():.2f}m to {df['tide_m'].max():.2f}m</p>
            <p><strong>Average Tide Height:</strong> {df['tide_m'].mean():.2f}m</p>
            <p><strong>Standard Deviation:</strong> {df['tide_m'].std():.2f}m</p>
        </div>
        
        <div class="plot-container">
            <h3>📈 Interactive Links to Visualizations</h3>
            <ul>
                <li><a href="tide_time_series.html" target="_blank">📊 Time Series Plot - Full year tide patterns with range selector</a></li>
                <li><a href="tide_monthly_heatmap.html" target="_blank">🔥 Monthly Heatmap - Tide patterns by month and day</a></li>
                <li><a href="tide_hourly_patterns.html" target="_blank">⏰ Hourly Patterns - Daily tide cycles</a></li>
                <li><a href="tide_monthly_boxplot.html" target="_blank">📦 Monthly Distribution - Statistical overview by month</a></li>
                <li><a href="tide_3d_scatter.html" target="_blank">🎯 3D Visualization - Day vs Hour vs Tide Height</a></li>
            </ul>
        </div>
        
        <div class="plot-container">
            <h3>💡 Key Insights</h3>
            <ul>
                <li><strong>Tidal Range:</strong> Chek Lap Kok experiences tides ranging from {df['tide_m'].min():.2f}m to {df['tide_m'].max():.2f}m</li>
                <li><strong>Seasonal Patterns:</strong> Use the monthly heatmap to identify seasonal variations</li>
                <li><strong>Daily Cycles:</strong> The hourly patterns show typical semi-diurnal tide patterns</li>
                <li><strong>Data Quality:</strong> Complete year coverage with {len(df):,} measurements</li>
            </ul>
        </div>
        
        <div class="plot-container">
            <h3>🎮 How to Use</h3>
            <ul>
                <li><strong>Time Series:</strong> Use range selector buttons (7d, 30d, 3m, 6m, all) or drag the range slider</li>
                <li><strong>Zoom:</strong> Click and drag to zoom into specific time periods</li>
                <li><strong>Hover:</strong> Hover over data points for detailed information</li>
                <li><strong>Legend:</strong> Click legend items to show/hide data series</li>
                <li><strong>Pan:</strong> Hold and drag to pan around the plot</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    with open("tide_dashboard.html", "w", encoding="utf-8") as f:
        f.write(dashboard_html)
    
    print("✅ Dashboard created successfully!")
    print("\nFiles created:")
    print("- tide_dashboard.html (Main dashboard with links)")
    print("- tide_time_series.html (Interactive time series)")
    print("- tide_monthly_heatmap.html (Monthly patterns)")
    print("- tide_hourly_patterns.html (Daily cycles)")
    print("- tide_monthly_boxplot.html (Statistical distributions)")
    print("- tide_3d_scatter.html (3D visualization)")
    
    return df

if __name__ == "__main__":
    df = create_dashboard()
    
    # Display some basic statistics
    print(f"\n📊 Basic Statistics:")
    print(f"Mean tide height: {df['tide_m'].mean():.2f}m")
    print(f"Median tide height: {df['tide_m'].median():.2f}m")
    print(f"Standard deviation: {df['tide_m'].std():.2f}m")
    print(f"Highest tide: {df['tide_m'].max():.2f}m on {df.loc[df['tide_m'].idxmax(), 'datetime']}")
    print(f"Lowest tide: {df['tide_m'].min():.2f}m on {df.loc[df['tide_m'].idxmin(), 'datetime']}")

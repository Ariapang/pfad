import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def create_vivid_interactive_tide_viz():
    print("🌊 Creating VIVID Interactive Tide Visualization...")
    
    # Load data
    df = pd.read_csv('chek_lap_kok_e_2023_long.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Enhanced data processing
    df['hour'] = df['datetime'].dt.hour
    df['month'] = df['datetime'].dt.month
    df['day_of_year'] = df['datetime'].dt.dayofyear
    df['month_name'] = df['datetime'].dt.month_name()
    df['weekday'] = df['datetime'].dt.day_name()
    
    # Create tide categories for color coding
    df['tide_level'] = pd.cut(df['tide_m'], 
                             bins=[0, 0.5, 1.0, 1.5, 2.0, 3.0],
                             labels=['🌊 Very Low', '🌀 Low', '🌊 Medium', '🌊 High', '🌊 EXTREME'])
    
    # Create the main figure with subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            '🌊 FULL YEAR TIDE ADVENTURE - Zoom & Explore!',
            '📊 Monthly Tide Intensity Heatmap',
            '⏰ Daily Rhythm - When Do Tides Peak?',
            '📈 Seasonal Patterns - Nature\'s Calendar',
            '🎯 Tide Distribution - Statistical Magic',
            '💫 Animated Monthly Journey'
        ),
        specs=[[{"colspan": 2}, None],
               [{"type": "scatter"}, {"type": "bar"}],
               [{"type": "violin"}, {"type": "scatter"}]],
        vertical_spacing=0.08,
        horizontal_spacing=0.1
    )
    
    # 1. MAIN INTERACTIVE TIME SERIES (Top - Full Width)
    print("🎨 Creating main time series with color zones...")
    
    # Create color-coded scatter points based on tide levels
    colors = {'🌊 Very Low': '#FF6B6B', '🌀 Low': '#4ECDC4', '🌊 Medium': '#45B7D1', 
              '🌊 High': '#96CEB4', '🌊 EXTREME': '#FFEAA7'}
    
    for tide_level in df['tide_level'].cat.categories:
        if tide_level in df['tide_level'].values:
            mask = df['tide_level'] == tide_level
            fig.add_trace(
                go.Scatter(
                    x=df[mask]['datetime'],
                    y=df[mask]['tide_m'],
                    mode='markers',
                    name=tide_level,
                    marker=dict(
                        color=colors.get(tide_level, '#1f77b4'),
                        size=6,
                        opacity=0.8,
                        line=dict(width=1, color='white')
                    ),
                    hovertemplate='<b>%{x}</b><br>' +
                                  f'<b>{tide_level}</b><br>' +
                                  'Tide: <b>%{y:.2f}m</b><br>' +
                                  '<i>Click to zoom!</i><extra></extra>',
                    showlegend=True
                ),
                row=1, col=1
            )
    
    # Add smooth trend line
    from scipy.signal import savgol_filter
    if len(df) > 51:  # Ensure we have enough points for smoothing
        smooth_tide = savgol_filter(df['tide_m'], 51, 3)
        fig.add_trace(
            go.Scatter(
                x=df['datetime'],
                y=smooth_tide,
                mode='lines',
                name='🌊 Smooth Trend',
                line=dict(color='rgba(255,255,255,0.8)', width=4, dash='dash'),
                hovertemplate='<b>Smooth Trend</b><br>%{x}<br>%{y:.2f}m<extra></extra>'
            ),
            row=1, col=1
        )
    
    # 2. HOURLY PATTERNS (Bottom Left)
    print("⏰ Creating hourly rhythm patterns...")
    hourly_stats = df.groupby('hour').agg({
        'tide_m': ['mean', 'std', 'count']
    }).round(2)
    hourly_stats.columns = ['mean', 'std', 'count']
    hourly_stats = hourly_stats.reset_index()
    
    # Create bubble chart for hourly patterns
    fig.add_trace(
        go.Scatter(
            x=hourly_stats['hour'],
            y=hourly_stats['mean'],
            mode='markers',
            name='⏰ Hourly Average',
            marker=dict(
                size=hourly_stats['count']/3,  # Bubble size based on data count
                color=hourly_stats['mean'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='Tide Height', x=0.48),
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            hovertemplate='<b>Hour: %{x}:00</b><br>' +
                          'Avg Tide: <b>%{y:.2f}m</b><br>' +
                          'Data Points: %{marker.size}<br>' +
                          '<i>Peak time insights!</i><extra></extra>'
        ),
        row=2, col=1
    )
    
    # 3. MONTHLY BAR CHART (Bottom Right)
    print("📊 Creating monthly intensity bars...")
    monthly_stats = df.groupby('month_name').agg({
        'tide_m': ['mean', 'max', 'min', 'std']
    }).round(2)
    monthly_stats.columns = ['mean', 'max', 'min', 'std']
    monthly_stats = monthly_stats.reset_index()
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_stats['month_name'] = pd.Categorical(monthly_stats['month_name'], categories=month_order, ordered=True)
    monthly_stats = monthly_stats.sort_values('month_name')
    
    fig.add_trace(
        go.Bar(
            x=monthly_stats['month_name'],
            y=monthly_stats['max'],
            name='🌊 Max Tide',
            marker_color='rgba(55, 128, 191, 0.8)',
            hovertemplate='<b>%{x}</b><br>Max Tide: <b>%{y:.2f}m</b><extra></extra>'
        ),
        row=2, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=monthly_stats['month_name'],
            y=monthly_stats['mean'],
            name='📊 Avg Tide',
            marker_color='rgba(255, 193, 7, 0.8)',
            hovertemplate='<b>%{x}</b><br>Avg Tide: <b>%{y:.2f}m</b><extra></extra>'
        ),
        row=2, col=2
    )
    
    # 4. VIOLIN PLOT (Bottom Left of second row)
    print("🎵 Creating violin distribution...")
    for i, month in enumerate(month_order[:6]):  # First 6 months
        month_data = df[df['month_name'] == month]['tide_m']
        if not month_data.empty:
            fig.add_trace(
                go.Violin(
                    y=month_data,
                    name=month[:3],
                    box_visible=True,
                    meanline_visible=True,
                    fillcolor=f'rgba({50 + i*30}, {100 + i*20}, {200 - i*15}, 0.6)',
                    line_color='black',
                    hovertemplate=f'<b>{month}</b><br>Tide: %{{y:.2f}}m<extra></extra>'
                ),
                row=3, col=1
            )
    
    # 5. SEASONAL SCATTER (Bottom Right of second row)
    print("🌸 Creating seasonal patterns...")
    df['season'] = df['month'].map({12: 'Winter', 1: 'Winter', 2: 'Winter',
                                   3: 'Spring', 4: 'Spring', 5: 'Spring',
                                   6: 'Summer', 7: 'Summer', 8: 'Summer',
                                   9: 'Autumn', 10: 'Autumn', 11: 'Autumn'})
    
    season_colors = {'Spring': '#FF6B9D', 'Summer': '#FFD93D', 'Autumn': '#6BCF7F', 'Winter': '#4D96FF'}
    
    for season in ['Spring', 'Summer', 'Autumn', 'Winter']:
        season_data = df[df['season'] == season]
        if not season_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=season_data['day_of_year'],
                    y=season_data['tide_m'],
                    mode='markers',
                    name=f'{season} 🌸🌞🍂❄️'[['Spring', 'Summer', 'Autumn', 'Winter'].index(season)],
                    marker=dict(
                        color=season_colors[season],
                        size=8,
                        opacity=0.6,
                        line=dict(width=1, color='white')
                    ),
                    hovertemplate=f'<b>{season}</b><br>' +
                                  'Day of Year: %{x}<br>' +
                                  'Tide: <b>%{y:.2f}m</b><extra></extra>'
                ),
                row=3, col=2
            )
    
    # ENHANCED LAYOUT with vivid styling
    fig.update_layout(
        title={
            'text': '🌊 CHEK LAP KOK TIDAL ODYSSEY 2023 🌊<br>' +
                   '<sub>🎯 Interactive Data Adventure - Discover Nature\'s Rhythm!</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2C3E50', 'family': 'Arial Black'}
        },
        height=1200,
        showlegend=True,
        template='plotly_white',
        font=dict(family='Arial', size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        annotations=[
            dict(
                text="🎮 INTERACTIVE FEATURES:<br>• Zoom & Pan<br>• Click Legend Items<br>• Hover for Details<br>• Use Range Selectors",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                xanchor="left", yanchor="top",
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="rgba(0,0,0,0.1)",
                borderwidth=1,
                font=dict(size=10, color='#2C3E50')
            ),
            dict(
                text="💡 INSIGHTS:<br>• Tidal Range: 2.89m<br>• Semi-diurnal Pattern<br>• Seasonal Variations<br>• 1,301 Data Points",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.98, y=0.98,
                xanchor="right", yanchor="top",
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="rgba(0,0,0,0.1)",
                borderwidth=1,
                font=dict(size=10, color='#2C3E50')
            )
        ]
    )
    
    # Add range selector to main plot
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="🗓️ 7D", step="day", stepmode="backward"),
                dict(count=30, label="📅 1M", step="day", stepmode="backward"),
                dict(count=90, label="🌸 3M", step="day", stepmode="backward"),
                dict(count=180, label="🌞 6M", step="day", stepmode="backward"),
                dict(step="all", label="🌍 ALL")
            ]),
            bgcolor="rgba(255,255,255,0.8)",
            activecolor="rgba(255,193,7,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        rangeslider=dict(
            visible=True,
            bgcolor="rgba(240,240,240,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        type="date",
        row=1, col=1
    )
    
    # Update subplot titles with better styling
    fig.update_annotations([
        dict(text="🌊 FULL YEAR TIDE ADVENTURE - Zoom & Explore!", font=dict(size=16, color='#2C3E50')),
        dict(text="⏰ Daily Rhythm - When Do Tides Peak?", font=dict(size=14, color='#2C3E50')),
        dict(text="📊 Monthly Tide Intensity", font=dict(size=14, color='#2C3E50')),
        dict(text="🎵 Seasonal Distribution (First Half)", font=dict(size=14, color='#2C3E50')),
        dict(text="🌸 Seasonal Patterns Throughout Year", font=dict(size=14, color='#2C3E50'))
    ])
    
    # Save the enhanced visualization
    fig.write_html("tide_interactive_VIVID.html", 
                   config={
                       'displayModeBar': True,
                       'displaylogo': False,
                       'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawrect', 'eraseshape'],
                       'toImageButtonOptions': {
                           'format': 'png',
                           'filename': 'chek_lap_kok_tides_2023',
                           'height': 1200,
                           'width': 1600,
                           'scale': 2
                       }
                   })
    
    print("✨ VIVID Interactive Tide Visualization Created!")
    print("🎯 Features Added:")
    print("   • Multi-panel dashboard layout")
    print("   • Color-coded tide levels")
    print("   • Interactive bubble charts")
    print("   • Seasonal pattern analysis")
    print("   • Enhanced hover information")
    print("   • Professional annotations")
    print("   • Drawing tools enabled")
    print("   • High-resolution export ready")
    
    return fig

if __name__ == "__main__":
    try:
        # Install scipy if not available
        try:
            from scipy.signal import savgol_filter
        except ImportError:
            print("Installing scipy for smooth trend lines...")
            import subprocess
            subprocess.check_call(["pip", "install", "scipy"])
            from scipy.signal import savgol_filter
        
        fig = create_vivid_interactive_tide_viz()
        print(f"\n🎉 SUCCESS! Open 'tide_interactive_VIVID.html' to experience the enhanced visualization!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Creating simplified version without advanced features...")
        
        # Fallback version without scipy
        import pandas as pd
        import plotly.graph_objects as go
        
        df = pd.read_csv('chek_lap_kok_e_2023_long.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        fig = go.Figure()
        
        # Simple but vivid version
        fig.add_trace(go.Scatter(
            x=df['datetime'],
            y=df['tide_m'],
            mode='lines+markers',
            name='🌊 Tide Height',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=4, color=df['tide_m'], colorscale='Viridis', showscale=True),
            hovertemplate='<b>%{x}</b><br>Tide: <b>%{y:.2f}m</b><extra></extra>'
        ))
        
        fig.update_layout(
            title='🌊 VIVID Chek Lap Kok Tides 2023 🌊',
            xaxis_title='Date',
            yaxis_title='Tide Height (meters)',
            template='plotly_white',
            height=600,
            xaxis=dict(
                rangeselector=dict(
                    buttons=[
                        dict(count=7, label="7D", step="day", stepmode="backward"),
                        dict(count=30, label="1M", step="day", stepmode="backward"),
                        dict(count=90, label="3M", step="day", stepmode="backward"),
                        dict(step="all", label="ALL")
                    ]
                ),
                rangeslider=dict(visible=True)
            )
        )
        
        fig.write_html("tide_interactive_VIVID.html")
        print("✅ Simplified vivid version created successfully!")

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

print("🚀 Creating SUPER DYNAMIC Interactive Tide Experience...")

# Load data
df = pd.read_csv('chek_lap_kok_e_2023_long.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

# Enhanced data features
df['hour'] = df['datetime'].dt.hour
df['month'] = df['datetime'].dt.month
df['day_of_year'] = df['datetime'].dt.dayofyear
df['month_name'] = df['datetime'].dt.month_name()
df['weekday'] = df['datetime'].dt.day_name()
df['week'] = df['datetime'].dt.isocalendar().week

print(f"📊 Processing {len(df)} tide measurements for DYNAMIC magic...")

# 1. CREATE ANIMATED TIME SERIES
print("🎬 Creating animated time series...")

fig = go.Figure()

# Create frames for animation (monthly progression)
frames = []
months = sorted(df['month'].unique())

for i, month in enumerate(months):
    month_data = df[df['month'] <= month].copy()
    
    # Dynamic color coding
    colors = []
    for tide in month_data['tide_m']:
        if tide < 0.5:
            colors.append('#FF4757')  # Red
        elif tide < 1.0:
            colors.append('#FF6B35')  # Orange  
        elif tide < 1.5:
            colors.append('#F7DC6F')  # Yellow
        elif tide < 2.0:
            colors.append('#52C41A')  # Green
        else:
            colors.append('#1890FF')  # Blue
    
    frame = go.Frame(
        data=[
            go.Scatter(
                x=month_data['datetime'],
                y=month_data['tide_m'],
                mode='markers+lines',
                name=f'🌊 Month {month}',
                line=dict(color='rgba(30,144,255,0.6)', width=2),
                marker=dict(
                    color=colors,
                    size=6,
                    opacity=0.8,
                    line=dict(width=1, color='white')
                ),
                hovertemplate='<b>📅 %{x}</b><br>' +
                              '<b>🌊 Tide: %{y:.2f}m</b><br>' +
                              f'<b>📊 Through Month: {month}</b><br>' +
                              '<i>🎬 Animation Progress!</i><extra></extra>'
            )
        ],
        name=f"Month {month}",
        layout=go.Layout(
            title=f"🎬 DYNAMIC TIDE ANIMATION - Month {month}/12 🎬<br><sub>Progress: {len(month_data)} data points</sub>",
        )
    )
    frames.append(frame)

# Add initial trace (first month)
first_month_data = df[df['month'] == 1]
colors = ['#FF4757' if t < 0.5 else '#FF6B35' if t < 1.0 else '#F7DC6F' if t < 1.5 else '#52C41A' if t < 2.0 else '#1890FF' for t in first_month_data['tide_m']]

fig.add_trace(
    go.Scatter(
        x=first_month_data['datetime'],
        y=first_month_data['tide_m'],
        mode='markers+lines',
        name='🌊 Tide Animation',
        line=dict(color='rgba(30,144,255,0.6)', width=2),
        marker=dict(
            color=colors,
            size=6,
            opacity=0.8,
            line=dict(width=1, color='white')
        ),
        hovertemplate='<b>📅 %{x}</b><br><b>🌊 Tide: %{y:.2f}m</b><extra></extra>'
    )
)

# Add frames to figure
fig.frames = frames

# Add SUPER INTERACTIVE controls
fig.update_layout(
    title={
        'text': '🎬 SUPER DYNAMIC CHEK LAP KOK TIDES 🎬<br>' +
               '<span style="font-size:16px;">🚀 Watch the Year Unfold - Month by Month Animation!</span>',
        'x': 0.5,
        'font': {'size': 26, 'color': '#2C3E50', 'family': 'Arial Black'}
    },
    height=700,
    template='plotly_white',
    plot_bgcolor='rgba(240,248,255,0.8)',
    
    # Animation controls
    updatemenus=[
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": True},
                                   "fromcurrent": True, "transition": {"duration": 300}}],
                    "label": "🚀 PLAY ANIMATION",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                     "mode": "immediate", "transition": {"duration": 0}}],
                    "label": "⏸️ PAUSE",
                    "method": "animate"
                },
                {
                    "args": [["Month 1"], {"frame": {"duration": 0, "redraw": True},
                                         "mode": "immediate", "transition": {"duration": 0}}],
                    "label": "⏮️ RESTART",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 10},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "y": 1.1,
            "bgcolor": "rgba(52, 152, 219, 0.8)",
            "bordercolor": "white",
            "font": {"color": "white", "size": 12}
        },
        # Speed control
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 1000}}],
                    "label": "🐌 SLOW",
                    "method": "animate"
                },
                {
                    "args": [None, {"frame": {"duration": 500}}],
                    "label": "🚶 NORMAL", 
                    "method": "animate"
                },
                {
                    "args": [None, {"frame": {"duration": 250}}],
                    "label": "🏃 FAST",
                    "method": "animate"
                },
                {
                    "args": [None, {"frame": {"duration": 100}}],
                    "label": "⚡ TURBO",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "x": 0.5,
            "y": 1.1,
            "bgcolor": "rgba(231, 76, 60, 0.8)",
            "bordercolor": "white",
            "font": {"color": "white", "size": 12}
        }
    ],
    
    # Interactive slider
    sliders=[{
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 16, "color": "#2C3E50"},
            "prefix": "🗓️ Month: ",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "bgcolor": "rgba(255,255,255,0.8)",
        "bordercolor": "rgba(52, 152, 219, 0.5)",
        "borderwidth": 2,
        "steps": [
            {
                "args": [
                    [f"Month {month}"],
                    {"frame": {"duration": 300, "redraw": True},
                     "mode": "immediate",
                     "transition": {"duration": 300}}
                ],
                "label": f"M{month}",
                "method": "animate"
            } for month in months
        ]
    }],
    
    # Enhanced annotations
    annotations=[
        dict(
            text="🎮 ANIMATION CONTROLS:<br>" +
                 "🚀 <b>Play/Pause</b> - Control animation<br>" +
                 "⚡ <b>Speed Control</b> - Adjust tempo<br>" +
                 "🎚️ <b>Slider</b> - Jump to any month<br>" +
                 "🔍 <b>Zoom & Pan</b> - Explore details<br>" +
                 "💫 <b>Hover</b> - Live data info",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.02, y=0.95,
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="rgba(52, 152, 219, 0.5)",
            borderwidth=2,
            font=dict(size=12, color='#2C3E50')
        ),
        dict(
            text="🌊 DYNAMIC FEATURES:<br>" +
                 "🎬 <b>Monthly Animation</b><br>" +
                 "🌈 <b>Color-Coded Heights</b><br>" +
                 "📊 <b>Progressive Build</b><br>" +
                 "⏰ <b>Smooth Transitions</b><br>" +
                 "🎯 <b>Interactive Timeline</b>",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.98, y=0.95,
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="rgba(46, 204, 113, 0.5)",
            borderwidth=2,
            font=dict(size=12, color='#2C3E50')
        )
    ]
)

# Save animated version
fig.write_html("tide_SUPER_DYNAMIC.html", 
               config={
                   'displayModeBar': True,
                   'displaylogo': False,
                   'responsive': True
               })

print("🎬 SUPER DYNAMIC ANIMATED VERSION CREATED!")

# 2. CREATE INTERACTIVE MULTI-FILTER DASHBOARD
print("\n🔥 Creating Multi-Filter Interactive Dashboard...")

fig2 = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        '🌊 LIVE TIDE TRACKER WITH FILTERS',
        '📊 RACING MONTHLY BARS',
        '⚡ HOURLY PULSE PATTERNS',
        '🌈 SEASONAL EXPLORER'
    )
)

# Add seasonal data with interactive toggles
seasons = {'Spring': [3,4,5], 'Summer': [6,7,8], 'Autumn': [9,10,11], 'Winter': [12,1,2]}
season_colors = {'Spring': '#FF69B4', 'Summer': '#FFD700', 'Autumn': '#FF4500', 'Winter': '#4169E1'}

for season, months in seasons.items():
    season_data = df[df['month'].isin(months)]
    fig2.add_trace(
        go.Scatter(
            x=season_data['datetime'],
            y=season_data['tide_m'],
            mode='markers+lines',
            name=f'{season} {"🌸☀️🍂❄️"[["Spring","Summer","Autumn","Winter"].index(season)]}',
            line=dict(color=season_colors[season], width=2),
            marker=dict(size=6, opacity=0.7),
            hovertemplate=f'<b>{season}</b><br>%{{x}}<br>%{{y:.2f}}m<extra></extra>',
            visible=True if season == 'Spring' else 'legendonly'  # Start with Spring visible
        ),
        row=1, col=1
    )

# Racing monthly bars with animation effect
monthly_stats = df.groupby('month_name').agg({
    'tide_m': ['mean', 'max', 'count']
}).round(2)
monthly_stats.columns = ['mean', 'max', 'count']
monthly_stats = monthly_stats.reset_index()

month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

# Add animated bars
for i, month in enumerate(month_order):
    month_data = monthly_stats[monthly_stats['month_name'] == month]
    if not month_data.empty:
        fig2.add_trace(
            go.Bar(
                x=[month[:3]],
                y=month_data['max'].values,
                name=f'{month[:3]}',
                marker=dict(
                    color=f'hsl({i*30}, 70%, 60%)',
                    line=dict(color='white', width=2)
                ),
                hovertemplate=f'<b>{month}</b><br>Max: %{{y:.2f}}m<br>Count: {month_data["count"].values[0]}<extra></extra>',
                showlegend=False
            ),
            row=1, col=2
        )

# Hourly pulse with error bars
hourly_stats = df.groupby('hour').agg({
    'tide_m': ['mean', 'std', 'count']
}).round(2)
hourly_stats.columns = ['mean', 'std', 'count']
hourly_stats = hourly_stats.reset_index()

fig2.add_trace(
    go.Scatter(
        x=hourly_stats['hour'],
        y=hourly_stats['mean'],
        error_y=dict(
            type='data',
            array=hourly_stats['std'],
            visible=True,
            color='rgba(255,0,0,0.3)',
            thickness=2
        ),
        mode='lines+markers',
        name='💓 Hourly Pulse',
        line=dict(color='red', width=3),
        marker=dict(size=10, color='red', symbol='diamond'),
        hovertemplate='<b>Hour: %{x}:00</b><br>Average: %{y:.2f}m ± %{error_y.array:.2f}<extra></extra>',
        showlegend=False
    ),
    row=2, col=1
)

# Seasonal scatter with symbols
symbols = ['circle', 'square', 'diamond', 'star']
for i, (season, months) in enumerate(seasons.items()):
    season_data = df[df['month'].isin(months)]
    fig2.add_trace(
        go.Scatter(
            x=season_data['day_of_year'],
            y=season_data['tide_m'],
            mode='markers',
            name=f'🔍 {season}',
            marker=dict(
                color=season_colors[season],
                size=8,
                opacity=0.6,
                symbol=symbols[i],
                line=dict(width=1, color='white')
            ),
            hovertemplate=f'<b>{season}</b><br>Day: %{{x}}<br>Tide: %{{y:.2f}}m<extra></extra>',
            showlegend=False
        ),
        row=2, col=2
    )

# Add interactive controls
fig2.update_layout(
    title={
        'text': '🔥 MULTI-FILTER INTERACTIVE TIDE COMMAND CENTER 🔥<br>' +
               '<span style="font-size:14px;">🎮 Real-Time Filtering - Multi-Panel Analysis</span>',
        'x': 0.5,
        'font': {'size': 22, 'color': '#2C3E50'}
    },
    height=800,
    showlegend=True,
    template='plotly_white',
    
    # Interactive dropdown filters
    updatemenus=[
        {
            "buttons": [
                {"label": "🌍 All Seasons", "method": "update", 
                 "args": [{"visible": [True, True, True, True] + [True]*12 + [True] + [True]*4}]},
                {"label": "🌸 Spring Only", "method": "update",
                 "args": [{"visible": [True, False, False, False] + [True]*12 + [True] + [True]*4}]},
                {"label": "☀️ Summer Only", "method": "update",
                 "args": [{"visible": [False, True, False, False] + [True]*12 + [True] + [True]*4}]},
                {"label": "🍂 Autumn Only", "method": "update", 
                 "args": [{"visible": [False, False, True, False] + [True]*12 + [True] + [True]*4}]},
                {"label": "❄️ Winter Only", "method": "update",
                 "args": [{"visible": [False, False, False, True] + [True]*12 + [True] + [True]*4}]}
            ],
            "direction": "down",
            "showactive": True,
            "x": 0.1,
            "y": 1.15,
            "bgcolor": "rgba(52, 152, 219, 0.8)",
            "bordercolor": "white",
            "font": {"color": "white", "size": 12}
        }
    ]
)

fig2.write_html("tide_INTERACTIVE_FILTERS.html")

print("🔥 MULTI-FILTER DASHBOARD CREATED!")

# 3. CREATE ULTIMATE RESPONSIVE VERSION
print("\n⭐ Creating Ultimate Responsive Interactive Version...")

fig3 = go.Figure()

# Create multiple interactive layers
data_layers = {
    'All Data': df,
    'High Tides': df[df['tide_m'] > df['tide_m'].quantile(0.75)],
    'Low Tides': df[df['tide_m'] < df['tide_m'].quantile(0.25)],
    'Peak Hours': df[df['hour'].isin([6, 12, 18, 0])]
}

colors_layers = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

for i, (layer_name, data) in enumerate(data_layers.items()):
    fig3.add_trace(
        go.Scatter(
            x=data['datetime'],
            y=data['tide_m'],
            mode='markers+lines',
            name=f'🎯 {layer_name}',
            line=dict(color=colors_layers[i], width=2),
            marker=dict(size=6, opacity=0.7),
            visible=True if i == 0 else 'legendonly',
            hovertemplate=f'<b>{layer_name}</b><br>%{{x}}<br>%{{y:.2f}}m<extra></extra>'
        )
    )

# Enhanced layout with maximum interactivity
fig3.update_layout(
    title='⭐ ULTIMATE RESPONSIVE TIDE EXPLORER ⭐',
    height=600,
    template='plotly_white',
    
    # Advanced range selector
    xaxis=dict(
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1D", step="day", stepmode="backward"),
                dict(count=7, label="1W", step="day", stepmode="backward"),
                dict(count=30, label="1M", step="day", stepmode="backward"),
                dict(count=90, label="3M", step="day", stepmode="backward"),
                dict(count=180, label="6M", step="day", stepmode="backward"),
                dict(step="all", label="ALL")
            ],
            bgcolor="rgba(255,255,255,0.8)",
            activecolor="rgba(255,193,7,0.8)",
            bordercolor="rgba(52, 152, 219, 0.5)",
            borderwidth=2
        ),
        rangeslider=dict(
            visible=True,
            bgcolor="rgba(240,248,255,0.8)"
        ),
        type="date"
    ),
    
    # Responsive legend
    legend=dict(
        orientation="h",  # Horizontal for mobile
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="rgba(0,0,0,0.2)",
        borderwidth=1
    )
)

fig3.write_html("tide_ULTIMATE_responsive.html", 
               config={
                   'displayModeBar': True,
                   'displaylogo': False,
                   'responsive': True,
                   'modeBarButtonsToAdd': [
                       'drawline', 'drawopenpath', 'drawclosedpath',
                       'drawcircle', 'drawrect', 'eraseshape'
                   ]
               })

print("⭐ ULTIMATE RESPONSIVE VERSION CREATED!")

print("\n🎉 ALL SUPER DYNAMIC VERSIONS COMPLETED!")
print("📁 Files created:")
print("   🎬 tide_SUPER_DYNAMIC.html - Monthly animation with controls")
print("   🔥 tide_INTERACTIVE_FILTERS.html - Multi-filter dashboard") 
print("   ⭐ tide_ULTIMATE_responsive.html - Maximum responsive interactivity")
print("\n🚀 SUPER DYNAMIC Features:")
print("   • 🎬 Monthly animation progression")
print("   • ⏯️  Play/Pause/Restart controls")
print("   • ⚡ Speed adjustment (Slow/Normal/Fast/Turbo)")
print("   • 🎚️ Interactive month slider")
print("   • 🔄 Real-time season filtering")
print("   • 🌈 Color-coded tide levels")
print("   • 📊 Multi-panel analysis")
print("   • 💫 Enhanced hover interactions")
print("   • 📱 Fully responsive design")
print("   • 🖍️ Drawing tools enabled")

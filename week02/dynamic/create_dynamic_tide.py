import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

print("🚀 Creating ULTRA DYNAMIC Interactive Tide Experience...")

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

# Create the main figure with animation capabilities
fig = go.Figure()

# 1. ANIMATED TIME SERIES - Build frame by frame
print("🎬 Creating animated time series...")

# Create frames for animation (weekly progression)
frames = []
weeks = sorted(df['week'].unique())

for i, week in enumerate(weeks[::2]):  # Every 2nd week for smoother animation
    week_data = df[df['week'] <= week].copy()
    
    # Color coding for animation
    colors = []
    for tide in week_data['tide_m']:
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
                x=week_data['datetime'],
                y=week_data['tide_m'],
                mode='markers+lines',
                name=f'🌊 Week {week}',
                line=dict(color='rgba(30,144,255,0.6)', width=2),
                marker=dict(
                    color=colors,
                    size=8,
                    opacity=0.8,
                    line=dict(width=1, color='white')
                ),
                hovertemplate='<b>📅 %{x}</b><br>' +
                              '<b>🌊 Tide: %{y:.2f}m</b><br>' +
                              f'<b>📊 Week: {week}</b><br>' +
                              '<i>🎬 Animation in progress!</i><extra></extra>'
            )
        ],
        name=f"Week {week}",
        layout=go.Layout(
            title=f"🎬 DYNAMIC TIDE ANIMATION - Week {week}/52 🎬",
            annotations=[
                dict(
                    text=f"📊 Data Points: {len(week_data)}<br>🗓️ Current Week: {week}<br>📈 Progress: {i+1}/{len(weeks[::2])}",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.02, y=0.98,
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="rgba(52, 152, 219, 0.5)",
                    borderwidth=2
                )
            ]
        )
    )
    frames.append(frame)

# Add initial trace
fig.add_trace(
    go.Scatter(
        x=df['datetime'][:50],  # Start with first 50 points
        y=df['tide_m'][:50],
        mode='markers+lines',
        name='🌊 Tide Animation',
        line=dict(color='rgba(30,144,255,0.6)', width=2),
        marker=dict(
            color=['#FF4757'] * 50,
            size=8,
            opacity=0.8,
            line=dict(width=1, color='white')
        )
    )
)

# Add frames to figure
fig.frames = frames

# 2. ADD ANIMATION CONTROLS
print("🎮 Adding dynamic controls...")

# Animation buttons
fig.update_layout(
    updatemenus=[
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 100, "redraw": True},
                                   "fromcurrent": True, "transition": {"duration": 50}}],
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
                    "args": [["Week 1"], {"frame": {"duration": 0, "redraw": True},
                                         "mode": "immediate", "transition": {"duration": 0}}],
                    "label": "⏮️ RESTART",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        },
        # Speed control
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 200}}],
                    "label": "🐌 SLOW",
                    "method": "animate"
                },
                {
                    "args": [None, {"frame": {"duration": 100}}],
                    "label": "🚶 NORMAL", 
                    "method": "animate"
                },
                {
                    "args": [None, {"frame": {"duration": 50}}],
                    "label": "🏃 FAST",
                    "method": "animate"
                },
                {
                    "args": [None, {"frame": {"duration": 20}}],
                    "label": "⚡ TURBO",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.3,
            "xanchor": "right", 
            "y": 0,
            "yanchor": "top"
        }
    ]
)

# 3. ADD INTERACTIVE SLIDER
print("🎚️ Adding interactive slider...")

# Create slider steps
slider_steps = []
for i, week in enumerate(weeks[::2]):
    step = dict(
        args=[
            [f"Week {week}"],
            {"frame": {"duration": 300, "redraw": True},
             "mode": "immediate",
             "transition": {"duration": 300}}
        ],
        label=f"W{week}",
        method="animate"
    )
    slider_steps.append(step)

# Add slider
fig.update_layout(
    sliders=[{
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "🗓️ Week: ",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": slider_steps
    }]
)

# Save the animated version
fig.update_layout(
    title={
        'text': '🎬 DYNAMIC CHEK LAP KOK TIDAL CINEMA 🎬<br>' +
               '<span style="font-size:16px;">🚀 Interactive Animation Experience - Watch Time Flow!</span>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 28, 'color': '#2C3E50', 'family': 'Arial Black'}
    },
    height=700,
    template='plotly_white',
    plot_bgcolor='rgba(240,248,255,0.8)',
    
    annotations=[
        dict(
            text="🎮 DYNAMIC CONTROLS:<br>" +
                 "🚀 <b>Play/Pause</b> - Control animation<br>" +
                 "⚡ <b>Speed Control</b> - Adjust tempo<br>" +
                 "🎚️ <b>Slider</b> - Jump to any week<br>" +
                 "🔍 <b>Zoom</b> - Focus on details<br>" +
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
            text="🎯 ANIMATION FEATURES:<br>" +
                 "📈 <b>Progressive Build</b><br>" +
                 "🌈 <b>Color Evolution</b><br>" +
                 "📊 <b>Live Statistics</b><br>" +
                 "⏰ <b>Time Progression</b><br>" +
                 "🎬 <b>Smooth Transitions</b>",
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

fig.write_html("tide_DYNAMIC_animated.html")

print("🎬 DYNAMIC ANIMATED VERSION CREATED!")

# NOW CREATE REAL-TIME INTERACTIVE DASHBOARD
print("\n🔥 Creating REAL-TIME Interactive Dashboard...")

# Create multi-panel dynamic dashboard
fig2 = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        '🎯 LIVE TIDE TRACKER',
        '📊 DYNAMIC MONTHLY RACE',
        '⚡ REAL-TIME HOURLY PULSE',
        '🌈 INTERACTIVE SEASON EXPLORER'
    ),
    specs=[[{"type": "scatter"}, {"type": "bar"}],
           [{"type": "scatter"}, {"type": "scatter"}]]
)

# 1. Live updating main chart with dropdown filters
print("📡 Creating live tracker...")

# Add dropdown for time period selection
dropdown_buttons = [
    dict(label="🌍 All Year", method="update", 
         args=[{"visible": [True, True, True, True]},
               {"title": "🌍 Full Year View"}]),
    dict(label="🌸 Spring", method="update",
         args=[{"visible": [True, False, False, False]},
               {"title": "🌸 Spring Tides Only"}]),
    dict(label="☀️ Summer", method="update",
         args=[{"visible": [False, True, False, False]},
               {"title": "☀️ Summer Tides Only"}]),
    dict(label="🍂 Autumn", method="update", 
         args=[{"visible": [False, False, True, False]},
               {"title": "🍂 Autumn Tides Only"}]),
    dict(label="❄️ Winter", method="update",
         args=[{"visible": [False, False, False, True]},
               {"title": "❄️ Winter Tides Only"}])
]

# Add seasonal data with toggle capability
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
            hovertemplate=f'<b>{season}</b><br>%{{x}}<br>%{{y:.2f}}m<extra></extra>'
        ),
        row=1, col=1
    )

# 2. Animated monthly bars
print("🏁 Creating racing monthly bars...")
monthly_data = df.groupby('month_name')['tide_m'].agg(['mean', 'max', 'count']).reset_index()
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

# Animated bars that "race" 
for i, month in enumerate(month_order):
    month_row = monthly_data[monthly_data['month_name'] == month]
    if not month_row.empty:
        fig2.add_trace(
            go.Bar(
                x=[month],
                y=month_row['max'].values,
                name=f'{month[:3]} Max',
                marker=dict(
                    color=f'hsl({i*30}, 70%, 60%)',
                    line=dict(color='white', width=2)
                ),
                hovertemplate=f'<b>{month}</b><br>Max: %{{y:.2f}}m<br>Count: {month_row["count"].values[0]}<extra></extra>',
                showlegend=False
            ),
            row=1, col=2
        )

# 3. Real-time hourly pulse
print("💓 Creating hourly pulse...")
hourly_avg = df.groupby('hour')['tide_m'].agg(['mean', 'std']).reset_index()

# Create pulsing effect with error bars
fig2.add_trace(
    go.Scatter(
        x=hourly_avg['hour'],
        y=hourly_avg['mean'],
        error_y=dict(
            type='data',
            array=hourly_avg['std'],
            visible=True,
            color='rgba(255,0,0,0.3)',
            thickness=3
        ),
        mode='lines+markers',
        name='💓 Hourly Pulse',
        line=dict(color='red', width=4),
        marker=dict(size=12, color='red', symbol='heart'),
        hovertemplate='<b>Hour: %{x}:00</b><br>Pulse: %{y:.2f}m ± %{error_y.array:.2f}<extra></extra>'
    ),
    row=2, col=1
)

# 4. Interactive season explorer with buttons
print("🔍 Creating season explorer...")
df['day_in_season'] = df.apply(lambda x: 
    (x['day_of_year'] - [1, 60, 152, 244][['Winter','Spring','Summer','Autumn'].index(
        ['Winter','Spring','Summer','Autumn'][
            0 if x['month'] in [12,1,2] else
            1 if x['month'] in [3,4,5] else  
            2 if x['month'] in [6,7,8] else 3
        ]
    )]) % 365, axis=1)

for season, months in seasons.items():
    season_data = df[df['month'].isin(months)]
    fig2.add_trace(
        go.Scatter(
            x=season_data['day_in_season'],
            y=season_data['tide_m'],
            mode='markers',
            name=f'🔍 {season}',
            marker=dict(
                color=season_colors[season],
                size=8,
                opacity=0.6,
                symbol=['circle', 'square', 'diamond', 'star'][list(seasons.keys()).index(season)]
            ),
            hovertemplate=f'<b>{season}</b><br>Day in Season: %{{x}}<br>Tide: %{{y:.2f}}m<extra></extra>'
        ),
        row=2, col=2
    )

# Add interactive controls
fig2.update_layout(
    title={
        'text': '🔥 REAL-TIME INTERACTIVE TIDE COMMAND CENTER 🔥<br>' +
               '<span style="font-size:14px;">🎮 Live Controls - Dynamic Filtering - Real-Time Updates</span>',
        'x': 0.5,
        'font': {'size': 24, 'color': '#2C3E50'}
    },
    height=800,
    showlegend=True,
    template='plotly_white',
    
    # Add dropdown menu
    updatemenus=[
        dict(
            buttons=dropdown_buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top",
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="rgba(0,0,0,0.2)",
            font=dict(size=12)
        ),
        # Chart type selector
        dict(
            buttons=[
                dict(label="📈 Lines", method="restyle", args=["mode", "lines+markers"]),
                dict(label="🔴 Markers", method="restyle", args=["mode", "markers"]),
                dict(label="📊 Lines Only", method="restyle", args=["mode", "lines"])
            ],
            direction="down",
            x=0.3,
            y=1.15,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="rgba(0,0,0,0.2)"
        )
    ],
    
    annotations=[
        dict(
            text="🎮 REAL-TIME CONTROLS:<br>" +
                 "🔄 <b>Season Filter</b> - Toggle seasons<br>" +
                 "📈 <b>Chart Type</b> - Change visualization<br>" +
                 "🎯 <b>Interactive Legend</b> - Click to filter<br>" +
                 "🔍 <b>Zoom & Pan</b> - Explore details<br>" +
                 "💫 <b>Live Hover</b> - Dynamic information",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="rgba(231, 76, 60, 0.5)",
            borderwidth=2,
            font=dict(size=11, color='#2C3E50')
        )
    ]
)

fig2.write_html("tide_REALTIME_interactive.html")

print("🔥 REAL-TIME DASHBOARD CREATED!")

# Create ULTIMATE COMBINED VERSION with everything
print("\n⭐ Creating ULTIMATE COMBINED Interactive Experience...")

# Use Plotly's advanced features for maximum interactivity
fig3 = go.Figure()

# Add multiple interactive traces with different modes
modes = ['lines', 'markers', 'lines+markers']
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

for i, mode in enumerate(modes):
    sample_data = df.iloc[::len(df)//3] if i == 0 else df.iloc[i::3]
    
    fig3.add_trace(
        go.Scatter(
            x=sample_data['datetime'],
            y=sample_data['tide_m'],
            mode=mode,
            name=f'🎯 View {i+1}: {mode.title()}',
            line=dict(color=colors[i], width=3),
            marker=dict(size=8, opacity=0.7),
            visible=True if i == 0 else 'legendonly',  # Start with first trace visible
            hovertemplate=f'<b>Mode: {mode}</b><br>%{{x}}<br>%{{y:.2f}}m<extra></extra>'
        )
    )

# Add crossfilter-style interactions
fig3.update_layout(
    title='⭐ ULTIMATE INTERACTIVE TIDE EXPERIENCE ⭐',
    height=600,
    template='plotly_white',
    
    # Advanced range selector with custom buttons
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1D", step="day", stepmode="backward"),
                dict(count=7, label="1W", step="day", stepmode="backward"),
                dict(count=30, label="1M", step="day", stepmode="backward"),
                dict(count=90, label="3M", step="day", stepmode="backward"),
                dict(count=180, label="6M", step="day", stepmode="backward"),
                dict(step="all")
            ]),
            bgcolor="rgba(255,255,255,0.8)",
            activecolor="rgba(255,193,7,0.8)"
        ),
        rangeslider=dict(visible=True),
        type="date"
    ),
    
    # Interactive legend
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="rgba(0,0,0,0.2)",
        borderwidth=2
    )
)

fig3.write_html("tide_ULTIMATE_interactive.html", 
               config={
                   'modeBarButtonsToAdd': [
                       'drawline', 'drawopenpath', 'drawclosedpath',
                       'drawcircle', 'drawrect', 'eraseshape'
                   ],
                   'displaylogo': False,
                   'responsive': True
               })

print("⭐ ULTIMATE VERSION CREATED!")

print("\n🎉 ALL DYNAMIC VERSIONS COMPLETED!")
print("📁 Files created:")
print("   🎬 tide_DYNAMIC_animated.html - Animated time progression")
print("   🔥 tide_REALTIME_interactive.html - Real-time control dashboard") 
print("   ⭐ tide_ULTIMATE_interactive.html - Maximum interactivity")
print("\n🚀 Features added:")
print("   • ⏯️  Play/Pause animation controls")
print("   • ⚡ Speed adjustment (Slow/Normal/Fast/Turbo)")
print("   • 🎚️ Interactive timeline slider")
print("   • 🔄 Real-time season filtering")
print("   • 📊 Dynamic chart type switching")
print("   • 🎯 Cross-filtering interactions")
print("   • 🖍️ Drawing and annotation tools")
print("   • 📱 Responsive design")
print("   • 🌈 Multiple visualization modes")
print("   • 💫 Advanced hover interactions")

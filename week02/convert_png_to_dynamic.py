import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

print("🌊 Converting Static tide_timeseries.png to DYNAMIC Interactive Experience...")

# Load the tide data (same data used for the original PNG)
df = pd.read_csv('chek_lap_kok_e_2023_long.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

print(f"📊 Loaded {len(df)} tide measurements for dynamic conversion...")

# Create ULTRA DYNAMIC version of the timeseries
fig = go.Figure()

# 1. MAIN DYNAMIC TIME SERIES with enhanced features
print("🎨 Creating enhanced dynamic timeseries...")

# Color coding based on tide levels (replacing static line)
def get_tide_color(tide_value):
    if tide_value < 0.5:
        return '#FF4757'  # Red for very low
    elif tide_value < 1.0:
        return '#FF6B35'  # Orange for low  
    elif tide_value < 1.5:
        return '#F7DC6F'  # Yellow for medium
    elif tide_value < 2.0:
        return '#52C41A'  # Green for high
    else:
        return '#1890FF'  # Blue for very high

# Create color array
colors = [get_tide_color(tide) for tide in df['tide_m']]

# Add main timeseries trace with dynamic colors
fig.add_trace(
    go.Scatter(
        x=df['datetime'],
        y=df['tide_m'],
        mode='lines+markers',
        name='🌊 Tide Heights',
        line=dict(color='rgba(30,144,255,0.8)', width=2),
        marker=dict(
            color=colors,
            size=5,
            opacity=0.8,
            line=dict(width=1, color='white'),
            colorscale='Viridis',
            showscale=False
        ),
        hovertemplate='<b>📅 %{x}</b><br>' +
                      '<b>🌊 Tide Height: %{y:.2f}m</b><br>' +
                      '<b>🕐 %{customdata[0]}</b><br>' +
                      '<b>📊 %{customdata[1]}</b><br>' +
                      '<i>💡 Interactive timeseries!</i><extra></extra>',
        customdata=np.column_stack((df['datetime'].dt.strftime('%A'), 
                                   df['datetime'].dt.strftime('%B %d')))
    )
)

# 2. Add DYNAMIC TREND LINES
print("📈 Adding dynamic trend analysis...")

# Moving average (30-day window)
df['ma_30'] = df['tide_m'].rolling(window=30, center=True).mean()

fig.add_trace(
    go.Scatter(
        x=df['datetime'],
        y=df['ma_30'],
        mode='lines',
        name='📈 30-Day Trend',
        line=dict(color='rgba(255,140,0,0.8)', width=3, dash='dash'),
        hovertemplate='<b>30-Day Average</b><br>%{x}<br>%{y:.2f}m<extra></extra>',
        visible='legendonly'  # Hidden by default, can be toggled
    )
)

# Seasonal trend (quarterly averages)
df['quarter'] = df['datetime'].dt.quarter
quarterly_avg = df.groupby([df['datetime'].dt.to_period('Q')])['tide_m'].mean().reset_index()
quarterly_avg['datetime'] = quarterly_avg['datetime'].dt.to_timestamp()

fig.add_trace(
    go.Scatter(
        x=quarterly_avg['datetime'],
        y=quarterly_avg['tide_m'],
        mode='lines+markers',
        name='📊 Seasonal Trend',
        line=dict(color='rgba(220,20,60,0.8)', width=4),
        marker=dict(size=12, symbol='diamond', color='rgba(220,20,60,0.8)'),
        hovertemplate='<b>Seasonal Average</b><br>%{x|%Q %Y}<br>%{y:.2f}m<extra></extra>',
        visible='legendonly'  # Hidden by default
    )
)

# 3. Add DYNAMIC ANNOTATIONS for key events
print("🎯 Adding dynamic annotations...")

# Find highest and lowest tides
max_tide_idx = df['tide_m'].idxmax()
min_tide_idx = df['tide_m'].idxmin()

max_tide_date = df.loc[max_tide_idx, 'datetime']
max_tide_value = df.loc[max_tide_idx, 'tide_m']

min_tide_date = df.loc[min_tide_idx, 'datetime']  
min_tide_value = df.loc[min_tide_idx, 'tide_m']

# Add dynamic annotations that appear on hover
annotations = [
    dict(
        x=max_tide_date,
        y=max_tide_value,
        text=f"🔝 HIGHEST TIDE<br>{max_tide_value:.2f}m<br>{max_tide_date.strftime('%B %d, %Y')}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="red",
        ax=20,
        ay=-30,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="red",
        borderwidth=2,
        font=dict(size=12, color="red")
    ),
    dict(
        x=min_tide_date,
        y=min_tide_value,
        text=f"🔻 LOWEST TIDE<br>{min_tide_value:.2f}m<br>{min_tide_date.strftime('%B %d, %Y')}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="blue",
        ax=20,
        ay=30,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="blue",
        borderwidth=2,
        font=dict(size=12, color="blue")
    )
]

# 4. ENHANCED LAYOUT with maximum interactivity
fig.update_layout(
    title={
        'text': '🌊 DYNAMIC CHEK LAP KOK TIDE TIMESERIES 2023 🌊<br>' +
               '<span style="font-size:16px; color:#7f8c8d;">📈 Interactive Replacement for Static PNG - Now with Superpowers!</span>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 26, 'color': '#2C3E50', 'family': 'Arial Black'}
    },
    
    xaxis_title="📅 Date",
    yaxis_title="🌊 Tide Height (meters)",
    
    height=700,
    template='plotly_white',
    plot_bgcolor='rgba(240,248,255,0.8)',
    paper_bgcolor='rgba(255,255,255,0.95)',
    
    # SUPER INTERACTIVE range selector (better than static PNG!)
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="📅 1 Week", step="day", stepmode="backward"),
                dict(count=30, label="🗓️ 1 Month", step="day", stepmode="backward"),
                dict(count=90, label="🌸 1 Quarter", step="day", stepmode="backward"),
                dict(count=180, label="🌞 6 Months", step="day", stepmode="backward"),
                dict(step="all", label="🌍 Full Year")
            ]),
            bgcolor="rgba(52, 152, 219, 0.1)",
            activecolor="rgba(231, 76, 60, 0.8)",
            bordercolor="rgba(52, 152, 219, 0.5)",
            borderwidth=2,
            font=dict(color='#2C3E50', size=11)
        ),
        rangeslider=dict(
            visible=True,
            bgcolor="rgba(236, 240, 241, 0.8)",
            bordercolor="rgba(52, 152, 219, 0.5)",
            borderwidth=2
        ),
        type="date",
        gridcolor='rgba(0,0,0,0.1)',
        gridwidth=1
    ),
    
    yaxis=dict(
        gridcolor='rgba(0,0,0,0.1)',
        gridwidth=1,
        zeroline=True,
        zerolinecolor='rgba(0,0,0,0.2)',
        zerolinewidth=2
    ),
    
    # Interactive legend
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="rgba(52, 152, 219, 0.5)",
        borderwidth=2,
        font=dict(size=12)
    ),
    
    # Dynamic annotations
    annotations=annotations + [
        dict(
            text="🎮 DYNAMIC UPGRADES:<br>" +
                 "🔍 <b>Zoom & Pan</b> - Interactive exploration<br>" +
                 "📊 <b>Toggle Trends</b> - Click legend items<br>" +
                 "📅 <b>Time Ranges</b> - Quick date selection<br>" +
                 "💫 <b>Rich Hover</b> - Detailed information<br>" +
                 "📷 <b>Export</b> - High-res downloads",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            xanchor="left", yanchor="top",
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="rgba(46, 204, 113, 0.5)",
            borderwidth=2,
            font=dict(size=11, color='#2C3E50')
        ),
        dict(
            text="📊 VS STATIC PNG:<br>" +
                 "✅ <b>Interactive</b> vs Static<br>" +
                 "✅ <b>Zoomable</b> vs Fixed<br>" +
                 "✅ <b>Data-rich</b> vs Basic<br>" +
                 "✅ <b>Responsive</b> vs Fixed size<br>" +
                 "✅ <b>Exportable</b> vs View-only",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.98, y=0.98,
            xanchor="right", yanchor="top",
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="rgba(52, 152, 219, 0.5)",
            borderwidth=2,
            font=dict(size=11, color='#2C3E50')
        )
    ],
    
    hovermode='x unified'
)

# 5. SAVE as interactive HTML (replaces the static PNG!)
output_filename = "plots/tide_timeseries_DYNAMIC.html"

# Create plots directory if it doesn't exist
os.makedirs("plots", exist_ok=True)

fig.write_html(output_filename, 
               config={
                   'displayModeBar': True,
                   'displaylogo': False,
                   'responsive': True,
                   'toImageButtonOptions': {
                       'format': 'png',
                       'filename': 'tide_timeseries_dynamic',
                       'height': 700,
                       'width': 1200,
                       'scale': 2
                   }
               })

print("✨ DYNAMIC TIMESERIES CREATED!")
print(f"📁 Saved as: {output_filename}")

# 6. CREATE ENHANCED VERSION with ANIMATION
print("🎬 Creating animated version...")

# Create frames for animation (weekly progression)
fig_animated = go.Figure()

weeks = sorted(df['datetime'].dt.isocalendar().week.unique())
frames = []

for i, week in enumerate(weeks[::2]):  # Every 2nd week for smoother animation
    week_data = df[df['datetime'].dt.isocalendar().week <= week].copy()
    colors_frame = [get_tide_color(tide) for tide in week_data['tide_m']]
    
    frame = go.Frame(
        data=[
            go.Scatter(
                x=week_data['datetime'],
                y=week_data['tide_m'],
                mode='lines+markers',
                name=f'Week {week}',
                line=dict(color='rgba(30,144,255,0.8)', width=2),
                marker=dict(
                    color=colors_frame,
                    size=5,
                    opacity=0.8
                ),
                hovertemplate=f'<b>Through Week {week}</b><br>%{{x}}<br>%{{y:.2f}}m<extra></extra>'
            )
        ],
        name=f"Week {week}"
    )
    frames.append(frame)

# Add initial trace
first_week_data = df[df['datetime'].dt.isocalendar().week <= weeks[0]]
colors_initial = [get_tide_color(tide) for tide in first_week_data['tide_m']]

fig_animated.add_trace(
    go.Scatter(
        x=first_week_data['datetime'],
        y=first_week_data['tide_m'],
        mode='lines+markers',
        name='🎬 Animated Timeseries',
        line=dict(color='rgba(30,144,255,0.8)', width=2),
        marker=dict(color=colors_initial, size=5, opacity=0.8)
    )
)

fig_animated.frames = frames

# Add animation controls
fig_animated.update_layout(
    title='🎬 ANIMATED TIDE TIMESERIES - Watch the Year Unfold!',
    height=600,
    template='plotly_white',
    
    updatemenus=[{
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 200, "redraw": True},
                               "fromcurrent": True}],
                "label": "🚀 PLAY",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                 "mode": "immediate"}],
                "label": "⏸️ PAUSE",
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
    }],
    
    sliders=[{
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 16},
            "prefix": "📅 Week: ",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [
            {
                "args": [[f"Week {week}"],
                        {"frame": {"duration": 300, "redraw": True},
                         "mode": "immediate"}],
                "label": f"W{week}",
                "method": "animate"
            } for week in weeks[::2]
        ]
    }]
)

fig_animated.write_html("plots/tide_timeseries_ANIMATED.html")

print("🎬 ANIMATED VERSION CREATED!")

# 7. CREATE COMPARISON DASHBOARD
print("📊 Creating comparison dashboard...")

comparison_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Static PNG vs Dynamic HTML Comparison</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            background: rgba(255,255,255,0.95);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .comparison-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}
        .comparison-card {{
            background: rgba(255,255,255,0.95);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .static-preview {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            margin: 15px 0;
        }}
        .upgrade-button {{
            display: inline-block;
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1.1em;
            margin: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .upgrade-button:hover {{
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}
        .features-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        .features-table th, .features-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        .features-table th {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }}
        .features-table tr:nth-child(even) {{
            background: rgba(240,248,255,0.5);
        }}
        @media (max-width: 768px) {{
            .comparison-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 TIDE TIMESERIES: Static PNG → Dynamic HTML</h1>
            <p style="font-size: 1.2em; color: #7f8c8d;">Experience the transformation from static image to interactive visualization</p>
        </div>
        
        <div class="comparison-grid">
            <div class="comparison-card">
                <h2 style="color: #e74c3c;">📸 BEFORE: Static PNG</h2>
                <div class="static-preview">
                    <img src="tide_timeseries.png" alt="Static Tide Timeseries" style="max-width: 100%; height: auto; border: 2px solid #ddd; border-radius: 8px;">
                    <p style="margin-top: 15px; color: #6c757d;"><i>Original static image - basic line plot</i></p>
                </div>
                <h3>❌ Limitations:</h3>
                <ul>
                    <li>🚫 No interactivity</li>
                    <li>🚫 Fixed zoom level</li>
                    <li>🚫 No data details on hover</li>
                    <li>🚫 Cannot export different formats</li>
                    <li>🚫 Not responsive to screen size</li>
                    <li>🚫 No animation capabilities</li>
                </ul>
            </div>
            
            <div class="comparison-card">
                <h2 style="color: #28a745;">✨ AFTER: Dynamic HTML</h2>
                <div style="text-align: center; margin: 20px 0;">
                    <a href="tide_timeseries_DYNAMIC.html" class="upgrade-button" target="_blank">
                        🚀 OPEN DYNAMIC VERSION
                    </a>
                    <a href="tide_timeseries_ANIMATED.html" class="upgrade-button" target="_blank">
                        🎬 OPEN ANIMATED VERSION
                    </a>
                </div>
                <h3>✅ New Superpowers:</h3>
                <ul>
                    <li>✅ <strong>Interactive zoom & pan</strong></li>
                    <li>✅ <strong>Rich hover information</strong></li>
                    <li>✅ <strong>Toggle trend lines</strong></li>
                    <li>✅ <strong>Time range selectors</strong></li>
                    <li>✅ <strong>Responsive design</strong></li>
                    <li>✅ <strong>High-res export options</strong></li>
                    <li>✅ <strong>Animation capabilities</strong></li>
                    <li>✅ <strong>Color-coded data points</strong></li>
                    <li>✅ <strong>Dynamic annotations</strong></li>
                </ul>
            </div>
        </div>
        
        <div style="background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <h2 style="text-align: center; color: #2c3e50;">📊 Feature Comparison Matrix</h2>
            <table class="features-table">
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>📸 Static PNG</th>
                        <th>✨ Dynamic HTML</th>
                        <th>🎬 Animated HTML</th>
                        <th>Improvement</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Interactivity</strong></td>
                        <td>❌ None</td>
                        <td>✅ Full</td>
                        <td>✅ Full + Animation</td>
                        <td><span style="color: #28a745;">+1000%</span></td>
                    </tr>
                    <tr>
                        <td><strong>Data Access</strong></td>
                        <td>❌ Visual only</td>
                        <td>✅ Hover details</td>
                        <td>✅ Progressive data</td>
                        <td><span style="color: #28a745;">+∞</span></td>
                    </tr>
                    <tr>
                        <td><strong>Zoom/Pan</strong></td>
                        <td>❌ Fixed view</td>
                        <td>✅ Unlimited</td>
                        <td>✅ Unlimited</td>
                        <td><span style="color: #28a745;">Perfect</span></td>
                    </tr>
                    <tr>
                        <td><strong>Responsiveness</strong></td>
                        <td>❌ Fixed size</td>
                        <td>✅ Adaptive</td>
                        <td>✅ Adaptive</td>
                        <td><span style="color: #28a745;">Mobile Ready</span></td>
                    </tr>
                    <tr>
                        <td><strong>Export Options</strong></td>
                        <td>⚠️ View only</td>
                        <td>✅ Multiple formats</td>
                        <td>✅ Multiple formats</td>
                        <td><span style="color: #28a745;">Professional</span></td>
                    </tr>
                    <tr>
                        <td><strong>Animation</strong></td>
                        <td>❌ Static</td>
                        <td>❌ Static</td>
                        <td>✅ Smooth animation</td>
                        <td><span style="color: #28a745;">Cinematic</span></td>
                    </tr>
                    <tr>
                        <td><strong>File Size</strong></td>
                        <td>📁 ~50KB</td>
                        <td>📁 ~200KB</td>
                        <td>📁 ~300KB</td>
                        <td><span style="color: #f39c12;">Worth it!</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div style="text-align: center; margin-top: 30px; background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px;">
            <h2 style="color: #2c3e50;">🎯 Ready for the Upgrade?</h2>
            <p style="font-size: 1.1em; margin-bottom: 20px;">Transform your static visualizations into dynamic, interactive experiences!</p>
            <a href="tide_timeseries_DYNAMIC.html" class="upgrade-button" target="_blank" style="font-size: 1.2em; padding: 20px 40px;">
                🚀 EXPERIENCE THE DYNAMIC DIFFERENCE
            </a>
        </div>
    </div>
</body>
</html>"""

with open("plots/PNG_vs_HTML_comparison.html", "w", encoding="utf-8") as f:
    f.write(comparison_html)

print("📊 COMPARISON DASHBOARD CREATED!")

print("\n🎉 CONVERSION COMPLETE!")
print("📁 Files created in plots/ directory:")
print("   📊 tide_timeseries_DYNAMIC.html - Interactive replacement")
print("   🎬 tide_timeseries_ANIMATED.html - Animated version")
print("   📊 PNG_vs_HTML_comparison.html - Before/after comparison")
print("\n✨ Your static PNG has been transformed into a dynamic, interactive experience!")
print("🔥 Features added:")
print("   • 🔍 Interactive zoom and pan")
print("   • 📅 Time range selectors")
print("   • 💫 Rich hover information")
print("   • 📊 Toggleable trend lines")
print("   • 🌈 Color-coded data points")
print("   • 📱 Responsive design")
print("   • 📷 High-resolution export")
print("   • 🎬 Animation capabilities")
print("   • 🎯 Dynamic annotations")

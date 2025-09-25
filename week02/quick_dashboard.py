import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
print("Loading data...")
df = pd.read_csv('chek_lap_kok_e_2023_long.csv')
df['datetime'] = pd.to_datetime(df['datetime'])
print(f"Loaded {len(df)} records")

# Create enhanced time series
print("Creating enhanced time series...")
fig = go.Figure()

# Main tide data
fig.add_trace(go.Scatter(
    x=df['datetime'],
    y=df['tide_m'],
    mode='lines',
    name='Tide Height',
    line=dict(color='#1f77b4', width=1),
    hovertemplate='<b>%{x}</b><br>Tide: %{y:.2f}m<extra></extra>'
))

# Add layout with range selector
fig.update_layout(
    title='🌊 Chek Lap Kok Tide Heights 2023 - Interactive Time Series',
    xaxis_title='Date',
    yaxis_title='Tide Height (meters)',
    template='plotly_white',
    height=600,
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="7 days", step="day", stepmode="backward"),
                dict(count=30, label="30 days", step="day", stepmode="backward"),
                dict(count=90, label="3 months", step="day", stepmode="backward"),
                dict(step="all", label="All data")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)

fig.write_html("tide_interactive.html")
print("✅ Interactive time series saved!")

# Create monthly boxplot
print("Creating monthly boxplot...")
df['month_name'] = df['datetime'].dt.month_name()
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

fig2 = px.box(df, x='month_name', y='tide_m', 
             title='📊 Monthly Tide Height Distributions',
             labels={'tide_m': 'Tide Height (meters)', 'month_name': 'Month'},
             template='plotly_white',
             color='month_name')

fig2.update_xaxes(categoryorder='array', categoryarray=month_order)
fig2.update_layout(height=500, showlegend=False)
fig2.write_html("tide_monthly_box.html")
print("✅ Monthly boxplot saved!")

# Create hourly patterns
print("Creating hourly patterns...")
df['hour'] = df['datetime'].dt.hour
hourly_avg = df.groupby('hour')['tide_m'].mean().reset_index()

fig3 = px.line(hourly_avg, x='hour', y='tide_m',
              title='⏰ Average Tide Height by Hour of Day',
              labels={'hour': 'Hour of Day', 'tide_m': 'Average Tide Height (m)'},
              template='plotly_white')

fig3.update_traces(mode='lines+markers', marker=dict(size=8))
fig3.update_layout(height=500)
fig3.write_html("tide_hourly.html")
print("✅ Hourly patterns saved!")

print("All visualizations created successfully!")
print("Files:")
print("- tide_interactive.html")
print("- tide_monthly_box.html") 
print("- tide_hourly.html")

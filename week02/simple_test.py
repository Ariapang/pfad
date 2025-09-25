import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

print("Starting visualization script...")

try:
    # Load the data
    print("Loading CSV data...")
    df = pd.read_csv('chek_lap_kok_e_2023_long.csv')
    print(f"Data loaded successfully! Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"First few rows:")
    print(df.head())
    
    # Convert datetime
    print("Converting datetime...")
    df['datetime'] = pd.to_datetime(df['datetime'])
    print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")
    
    # Create a simple time series plot
    print("Creating time series plot...")
    fig = px.line(df, x='datetime', y='tide_m', 
                  title='Chek Lap Kok Tide Heights 2023',
                  labels={'tide_m': 'Tide Height (meters)', 'datetime': 'Date'})
    
    # Save the plot
    output_file = "simple_tide_plot.html"
    print(f"Saving plot to {output_file}...")
    fig.write_html(output_file)
    print("Plot saved successfully!")
    
    # Basic statistics
    print(f"\nBasic Statistics:")
    print(f"Total records: {len(df)}")
    print(f"Tide range: {df['tide_m'].min():.2f}m to {df['tide_m'].max():.2f}m")
    print(f"Average tide: {df['tide_m'].mean():.2f}m")
    
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()

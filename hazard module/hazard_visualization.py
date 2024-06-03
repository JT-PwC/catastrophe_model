import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from shapely.geometry import Point

# Generate random catastrophe events in Ontario
def generate_cat_events(num_events):
    np.random.seed(42)  # For reproducibility
    data = {
        "event_id": range(1, num_events + 1),
        "longitude": np.random.uniform(-95, -74, num_events),  # Ontario's approximate longitude range
        "latitude": np.random.uniform(41, 56, num_events),     # Ontario's approximate latitude range
        "severity": np.random.uniform(0, 1, num_events),       # Severity on a scale of 0 to 1
        "frequency": np.random.poisson(3, num_events)          # Frequency using a Poisson distribution
    }
    return pd.DataFrame(data)

# Create the catastrophe events DataFrame
num_events = 100
cat_events_df = generate_cat_events(num_events)

# Convert the DataFrame to a GeoDataFrame
geometry = [Point(xy) for xy in zip(cat_events_df["longitude"], cat_events_df["latitude"])]
cat_events_gdf = gpd.GeoDataFrame(cat_events_df, geometry=geometry)

# Initialize a folium map centered around Ontario
m = folium.Map(location=[51, -85], zoom_start=5)

# Add catastrophe events to the map
for _, row in cat_events_gdf.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['frequency'] * 2,  # Scale the frequency for visibility
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=row['severity']
    ).add_to(m)

# Save the map to an HTML file
m.save('ontario_catastrophe_events.html')
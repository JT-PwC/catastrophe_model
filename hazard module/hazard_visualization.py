import os
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from shapely.geometry import Point
import random
import yaml
import utils.stochastic_simulation as stk

project_path = os.getcwd().replace('\\','/')

# Load yaml file
def read_config(directory, filename):
    with open(f'{directory}/{filename}', 'r') as file:
        return yaml.safe_load(file)

config = read_config(project_path,'hazard module/hazard_config.yaml')

# Set parameters according to config
# Temperally set number of events to a constant but will be updated to
# be generated from distribution
shape_file_path = config['shape_file_path']
num_events = 5

# Load shape file
gdf = gpd.read_file(shape_file_path)

# Function to generate random points within a polygon
def generate_random_points(polygon, num_points):
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if polygon.contains(random_point):
            points.append(random_point)
    return points


# Merge all FSA polygons into a single polygon representing Ontario
canada_polygon = gdf.unary_union

# Generate random catastrophe events across Ontario
random_points = generate_random_points(canada_polygon, num_events)

# Create a DataFrame of catastrophe events
catastrophe_data = {
    'latitude': [point.y for point in random_points],
    'longitude': [point.x for point in random_points],
    'event_type': np.random.choice(config['event_types'], len(random_points)),
    'intensity': 10
}

catastrophe_df = pd.DataFrame(catastrophe_data)

# Convert the DataFrame to a GeoDataFrame
geometry = [Point(xy) for xy in zip(catastrophe_df['longitude'], catastrophe_df['latitude'])]
catastrophe_gdf = gpd.GeoDataFrame(catastrophe_df, geometry=geometry)

# Initialize a folium map centered around Ontario
m = folium.Map(location=[51, -85], zoom_start=5)

# Create a Folium map
m = folium.Map(location=[51.2538, -85.3232], zoom_start=6)

# Add catastrophe events to the map
for _, row in catastrophe_gdf.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Event: {row['event_type']}<br>intensity: {row['intensity']}",
        icon=folium.Icon(color='red' if row['intensity'] > 5 else 'blue')
    ).add_to(m)

# Save the map to an HTML file
output_html = config['output_html']
m.save(output_html)
import numpy as np
import scipy.stats as stats

class FloodHazard:
    def __init__(self, region_bounds, min_rainfall, max_rainfall, flood_rate, elevation_data, river_proximity):
        """
        Initialize the flood hazard model.
        
        :param region_bounds: Tuple of (min_lon, max_lon, min_lat, max_lat) representing the region bounds.
        :param min_rainfall: Minimum rainfall (mm).
        :param max_rainfall: Maximum rainfall (mm).
        :param flood_rate: Annual rate of flood events.
        :param elevation_data: Function that returns elevation for a given (longitude, latitude).
        :param river_proximity: Function that returns proximity to river for a given (longitude, latitude).
        """
        self.min_lon, self.max_lon, self.min_lat, self.max_lat = region_bounds
        self.min_rainfall = min_rainfall
        self.max_rainfall = max_rainfall
        self.flood_rate = flood_rate
        self.elevation_data = elevation_data
        self.river_proximity = river_proximity

    def generate_event(self):
        """
        Generate a single flood event.
        
        :return: Dictionary containing event details (longitude, latitude, rainfall, flood_depth, and occurrence time).
        """
        lon = np.random.uniform(self.min_lon, self.max_lon)
        lat = np.random.uniform(self.min_lat, self.max_lat)
        rainfall = np.random.uniform(self.min_rainfall, self.max_rainfall)
        occurrence_time = np.random.exponential(1.0 / self.flood_rate)
        
        # Calculate flood depth based on rainfall, elevation, and proximity to river
        elevation = self.elevation_data(lon, lat)
        proximity = self.river_proximity(lon, lat)
        flood_depth = self.calculate_flood_depth(rainfall, elevation, proximity)
        
        event = {
            "longitude": lon,
            "latitude": lat,
            "rainfall": rainfall,
            "flood_depth": flood_depth,
            "occurrence_time": occurrence_time
        }
        
        return event

    def calculate_flood_depth(self, rainfall, elevation, proximity):
        """
        Calculate flood depth based on rainfall, elevation, and proximity to river.
        
        :param rainfall: Rainfall in mm.
        :param elevation: Elevation in meters.
        :param proximity: Proximity to river in km.
        :return: Flood depth in meters.
        """
        # Simple model for flood depth calculation
        base_depth = rainfall / 100.0  # Base flood depth based on rainfall
        elevation_factor = max(0, 1 - elevation / 100.0)  # Elevation reduces flood depth
        proximity_factor = max(0, 1 - proximity / 10.0)  # Proximity to river increases flood depth
        
        flood_depth = base_depth * elevation_factor * proximity_factor
        return flood_depth

    def simulate_events(self, years):
        """
        Simulate flood events over a given number of years.
        
        :param years: Number of years to simulate.
        :return: List of flood events.
        """
        num_events = np.random.poisson(self.flood_rate * years)
        events = [self.generate_event() for _ in range(num_events)]
        
        return events

# Example usage:
region_bounds = (-125, -114, 32, 42)  # Example region (California)
min_rainfall = 50  # Minimum rainfall in mm
max_rainfall = 300  # Maximum rainfall in mm
flood_rate = 0.2  # Annual rate of flood events

# Mock functions for elevation and proximity to river (replace with real data for accurate modeling)
def mock_elevation_data(lon, lat):
    return np.random.uniform(0, 2000)  # Elevation in meters

def mock_river_proximity(lon, lat):
    return np.random.uniform(0, 10)  # Proximity to river in km

hazard_model = FloodHazard(region_bounds, min_rainfall, max_rainfall, flood_rate, mock_elevation_data, mock_river_proximity)
simulated_events = hazard_model.simulate_events(10)  # Simulate events for 10 years

for event in simulated_events:
    print(event)
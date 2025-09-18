import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import math
import matplotlib.pyplot as plt

class GautengRoadsDataset:
    def __init__(self):
        self.roads_df = pd.read_csv('./GautengRoadsDatasetJun2025/roads_csv.csv')
        self.assignments_df = pd.read_csv('./GautengRoadsDatasetJun2025/assignments_csv.csv')
        self.deliveries_df = pd.read_csv('./GautengRoadsDatasetJun2025/deliveries_csv.csv')
        self.incidents_df = pd.read_csv('./GautengRoadsDatasetJun2025/incidents_csv.csv')
        self.truck_profiles_df = pd.read_csv('./GautengRoadsDatasetJun2025/truck_profiles_csv.csv')
        self.weather_df = pd.read_csv('./GautengRoadsDatasetJun2025/weather_csv.csv')
        self.historical_speeds_df = pd.read_csv('./GautengRoadsDatasetJun2025/historical_speeds_csv.csv')


#traffic Detecter
def detect_current_traffic(road_id, dataset):
    """
    Basic traffic detector that analyzes current traffic conditions
    Returns congestion level (0-1) and status message
    """

    # Get road information
    road_info = dataset.roads_df [dataset.roads_df['road_id'] ]
    road_name = road_info['road_id']
    
    # Get recent speed data
    recent_speeds = dataset.historical_speeds_df[
        (dataset.historical_speeds_df['segment_id'] ) &
        (dataset.historical_speeds_df['interval_minutes'])
        
    ]
    
    if recent_speeds.empty:
        return 0.5, f"No recent data for {road_name}"
    
    # Calculate average speed
    avg_speed = recent_speeds['avg_speed_kph'].mean()
    
    # Get speed limit (default to 60 if not available)
    speed_limit = road_info.get('avg_speed_kph', 60)
    if pd.isna(speed_limit) or speed_limit == 0:
        speed_limit = 60
    
    # Calculate congestion level (0-1)
    congestion = 1 - (avg_speed / speed_limit)
    congestion = max(0, min(1, congestion))  # Clamp between 0 and 1
    
    # Determine traffic status
    if congestion > 0.7:
        status = f"HEAVY traffic on {road_name} - {avg_speed:.0f} kph (limit: {speed_limit} kph)"
    elif congestion > 0.4:
        status = f"MODERATE traffic on {road_name} - {avg_speed:.0f} kph"
    else:
        status = f"LIGHT traffic on {road_name} - {avg_speed:.0f} kph"
    
    return congestion, status

def check_incidents(road_id, dataset):
    """Check if there are any incidents on a specific road"""
    
    
    # Check for active incidents
    active_incidents = dataset.incidents_df[
        (pd.to_datetime(dataset.incidents_df['timestamp']) ) &
        (dataset.incidents_df['road_id'] == road_id)
    ]
    
    if not active_incidents.empty:
        incident = active_incidents.iloc[0]
        return True, f"INCIDENT on {incident['affected_segment_id']}: {incident['type']}"
    
    return False, "No incidents reported"

def monitor_route_traffic(route, dataset):
    """Monitor traffic conditions along a delivery route"""
    print("\n=== TRAFFIC DETECTOR REPORT ")
    
    for road_id in route:
        road_id = road_id.strip()
        if road_id.isdigit():
            # Check traffic conditions
            congestion, traffic_status = detect_current_traffic(int(road_id), dataset)
            
            # Check for incidents
            has_incident, incident_status = check_incidents(int(road_id), dataset)
            
            # Print report
            road_name = dataset.roads_df[dataset.roads_df['road_id'] == int(road_id)]['road_id'].values[0]
            print(f"Road {road_id} ({road_id}):")
            print(f"  - {traffic_status}")
            if has_incident:
                print(f"  - {incident_status}")
            print(f"  - Congestion level: {congestion:.2f}\n")


def predict_congestion(road_id, date_time, dataset):
    hour = date_time.hour
    weekday = date_time.weekday()
    
    speeds = dataset.historical_speeds_df[
        (dataset.historical_speeds_df['road_id'] == road_id) &
        (dataset.historical_speeds_df['interval_minutes'] == hour) &
        (dataset.historical_speeds_df['weekday'] == weekday)
    ]
    
    if speeds.empty:
        return 0.5  # Default congestion
    
    avg_speed = speeds['avg_speed_kph'].mean()
    base_speed = 60
    congestion = 1 - (avg_speed / base_speed)
    return min(max(congestion, 0), 1)

def estimate_delivery_time(road_id, start_time, dataset):
    road_info = dataset.roads_df[dataset.roads_df['road_id'] == road_id].iloc[0]
    length_km = road_info['length_m']
    congestion = predict_congestion(road_id, start_time, dataset)
    base_time = length_km / 60
    adjusted_time = base_time * (1 + congestion)
    return adjusted_time

def simulate_delivery(delivery_id, dataset):
    delivery = dataset.deliveries_df[dataset.deliveries_df['delivery_id'] == delivery_id].iloc[0]
    
    # Check if route exists and is not empty
    if 'destination_name' not in delivery or pd.isna(delivery['destination_name']):
        print(f"No route found for delivery {delivery_id}")
        return
    
    route = delivery['destination_name'].split(',')
    
    # Check if start_time exists and is valid
    if 'scheduled_departure_utc' not in delivery or pd.isna(delivery['scheduled_departure_utc']):
        start_time = 'scheduled_departure_utc'
    else:
        cleaned = str(delivery['scheduled_departure_utc']).replace("T", " ").replace("Z", "")
        start_time = datetime.strptime(cleaned, "%Y-%m-%d %H:%M:%S")
    
    # Use traffic detector to monitor route conditions
    monitor_route_traffic(route, dataset)
    
    total_time = 0
    for road_id in route:
        road_id = road_id.strip()
        if road_id.isdigit():  # Make sure it's a valid road ID
            time_on_road = estimate_delivery_time(int(road_id), start_time + timedelta(hours=total_time), dataset)
            total_time += time_on_road
    
    print(f"Estimated delivery time for {delivery_id}: {total_time:.2f} hours")

def adjust_for_incident(route, incident_road):
    if incident_road not in route:
        return route
    
    print(f"Incident on {incident_road}. Recalculating route...")
    return [r for r in route if r != incident_road]  # Simple reroute

if __name__ == "__main__":
    # Create an instance of the dataset class
    dataset = GautengRoadsDataset()
    
    # Check if we have any deliveries
    if not dataset.deliveries_df.empty:
        # Get the third delivery ID to test with
        six_delivery_id = dataset.deliveries_df.iloc[0]['delivery_id']
        print(f"Testing with delivery ID: {six_delivery_id}")
        
        # Simulate the delivery
        simulate_delivery(six_delivery_id, dataset)
    else:
        print("No deliveries found in the dataset")
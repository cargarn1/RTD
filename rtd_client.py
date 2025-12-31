"""
RTD Denver Transportation API Client
Provides access to RTD's GTFS static and real-time transit data
"""

import requests
from google.transit import gtfs_realtime_pb2
import zipfile
import io
import csv


class RTDClient:
    """Client for accessing RTD Denver's transportation APIs"""
    
    def __init__(self):
        self.static_feed_url = "https://www.rtd-denver.com/google_sync/google_transit.zip"
        self.realtime_base_url = "https://www.rtd-denver.com/google_sync/"
        
    def get_static_data(self, extract_files=None):
        """
        Download GTFS static feed
        
        Args:
            extract_files: List of files to extract from the ZIP (e.g., ['stops.txt', 'routes.txt'])
                         If None, returns all available files
        
        Returns:
            Dictionary with file names as keys and content as values
        """
        try:
            response = requests.get(self.static_feed_url, timeout=30)
            response.raise_for_status()
            
            data = {}
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                files_to_extract = extract_files or zip_file.namelist()
                
                for file_name in files_to_extract:
                    if file_name in zip_file.namelist():
                        data[file_name] = zip_file.read(file_name).decode('utf-8')
                    else:
                        print(f"Warning: {file_name} not found in ZIP")
            
            return data
        except Exception as e:
            print(f"Error downloading static data: {e}")
            return None
    
    def parse_stops(self):
        """
        Get all RTD stops
        
        Returns:
            List of dictionaries containing stop information
        """
        data = self.get_static_data(['stops.txt'])
        if not data or 'stops.txt' not in data:
            return None
        
        stops = []
        reader = csv.DictReader(io.StringIO(data['stops.txt']))
        for row in reader:
            stops.append(row)
        
        return stops
    
    def parse_routes(self):
        """
        Get all RTD routes
        
        Returns:
            List of dictionaries containing route information
        """
        data = self.get_static_data(['routes.txt'])
        if not data or 'routes.txt' not in data:
            return None
        
        routes = []
        reader = csv.DictReader(io.StringIO(data['routes.txt']))
        for row in reader:
            routes.append(row)
        
        return routes
    
    def get_vehicle_positions(self):
        """
        Get real-time vehicle positions
        
        Returns:
            List of dictionaries containing vehicle position data
        """
        url = f"{self.realtime_base_url}VehiclePosition.pb"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            vehicles = []
            for entity in feed.entity:
                if entity.HasField('vehicle'):
                    vehicle_data = {
                        'vehicle_id': entity.vehicle.vehicle.id if entity.vehicle.vehicle.HasField('id') else None,
                        'route_id': entity.vehicle.trip.route_id if entity.vehicle.trip.HasField('route_id') else None,
                        'trip_id': entity.vehicle.trip.trip_id if entity.vehicle.trip.HasField('trip_id') else None,
                        'latitude': entity.vehicle.position.latitude if entity.vehicle.position.HasField('latitude') else None,
                        'longitude': entity.vehicle.position.longitude if entity.vehicle.position.HasField('longitude') else None,
                        'bearing': entity.vehicle.position.bearing if entity.vehicle.position.HasField('bearing') else None,
                        'speed': entity.vehicle.position.speed if entity.vehicle.position.HasField('speed') else None,
                        'timestamp': entity.vehicle.timestamp if entity.vehicle.HasField('timestamp') else None
                    }
                    vehicles.append(vehicle_data)
            
            return vehicles
        except Exception as e:
            print(f"Error fetching vehicle positions: {e}")
            return None
    
    def get_trip_updates(self):
        """
        Get real-time trip updates (delays, cancellations, etc.)
        
        Returns:
            List of dictionaries containing trip update data
        """
        url = f"{self.realtime_base_url}TripUpdate.pb"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            updates = []
            for entity in feed.entity:
                if entity.HasField('trip_update'):
                    trip_update = entity.trip_update
                    
                    stop_time_updates = []
                    for stu in trip_update.stop_time_update:
                        stop_update = {
                            'stop_id': stu.stop_id if stu.HasField('stop_id') else None,
                            'arrival_delay': stu.arrival.delay if stu.HasField('arrival') and stu.arrival.HasField('delay') else None,
                            'arrival_time': stu.arrival.time if stu.HasField('arrival') and stu.arrival.HasField('time') else None,
                            'departure_delay': stu.departure.delay if stu.HasField('departure') and stu.departure.HasField('delay') else None,
                            'departure_time': stu.departure.time if stu.HasField('departure') and stu.departure.HasField('time') else None,
                        }
                        stop_time_updates.append(stop_update)
                    
                    update_data = {
                        'trip_id': trip_update.trip.trip_id if trip_update.trip.HasField('trip_id') else None,
                        'route_id': trip_update.trip.route_id if trip_update.trip.HasField('route_id') else None,
                        'vehicle_id': trip_update.vehicle.id if trip_update.HasField('vehicle') and trip_update.vehicle.HasField('id') else None,
                        'stop_time_updates': stop_time_updates
                    }
                    updates.append(update_data)
            
            return updates
        except Exception as e:
            print(f"Error fetching trip updates: {e}")
            return None
    
    def get_alerts(self):
        """
        Get service alerts
        
        Returns:
            List of dictionaries containing alert information
        """
        url = f"{self.realtime_base_url}Alert.pb"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            alerts = []
            for entity in feed.entity:
                if entity.HasField('alert'):
                    alert = entity.alert
                    
                    # Extract header text
                    header = ''
                    if alert.HasField('header_text') and len(alert.header_text.translation) > 0:
                        header = alert.header_text.translation[0].text
                    
                    # Extract description text
                    description = ''
                    if alert.HasField('description_text') and len(alert.description_text.translation) > 0:
                        description = alert.description_text.translation[0].text
                    
                    # Extract affected routes
                    affected_routes = []
                    for informed_entity in alert.informed_entity:
                        if informed_entity.HasField('route_id'):
                            affected_routes.append(informed_entity.route_id)
                    
                    alert_data = {
                        'id': entity.id,
                        'header': header,
                        'description': description,
                        'affected_routes': list(set(affected_routes)),  # Remove duplicates
                        'cause': alert.cause if alert.HasField('cause') else None,
                        'effect': alert.effect if alert.HasField('effect') else None,
                    }
                    alerts.append(alert_data)
            
            return alerts
        except Exception as e:
            print(f"Error fetching alerts: {e}")
            return None
    
    def find_stops_by_name(self, search_term):
        """
        Search for stops by name
        
        Args:
            search_term: String to search for in stop names
        
        Returns:
            List of matching stops
        """
        stops = self.parse_stops()
        if not stops:
            return None
        
        search_term = search_term.lower()
        matching_stops = [
            stop for stop in stops 
            if search_term in stop.get('stop_name', '').lower()
        ]
        
        return matching_stops
    
    def find_route_by_name(self, search_term):
        """
        Search for routes by name or short name
        
        Args:
            search_term: String to search for in route names
        
        Returns:
            List of matching routes
        """
        routes = self.parse_routes()
        if not routes:
            return None
        
        search_term = search_term.lower()
        matching_routes = [
            route for route in routes 
            if search_term in route.get('route_short_name', '').lower() 
            or search_term in route.get('route_long_name', '').lower()
        ]
        
        return matching_routes


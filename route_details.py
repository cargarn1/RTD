#!/usr/bin/env python3
"""
RTD Route Details Module
Fetches and manages route information, stops, and schedules
"""

import requests
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


class RouteDetailsClient:
    """Client for getting detailed route information"""
    
    def __init__(self):
        self.static_feed_url = "https://www.rtd-denver.com/google_sync/google_transit.zip"
        self.cache = {}
        self.cache_time = None
    
    def get_route_info(self, route_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific route
        
        Args:
            route_id: Route identifier (e.g., "15", "A", "FF1")
        
        Returns:
            Dictionary with route details including stops and schedules
        """
        # For now, return simulated data since GTFS static feed is unavailable
        # In production, this would parse the actual GTFS data
        
        route_info = {
            'route_id': route_id,
            'route_name': self._get_route_name(route_id),
            'route_type': self._get_route_type(route_id),
            'description': self._get_route_description(route_id),
            'stops': self._get_simulated_stops(route_id),
            'schedule': self._get_simulated_schedule(route_id),
            'operating_hours': self._get_operating_hours(route_id)
        }
        
        return route_info
    
    def _get_route_name(self, route_id: str) -> str:
        """Get human-readable route name"""
        route_names = {
            'A': 'A Line - Union Station to Airport',
            'B': 'B Line - Union Station to Westminster',
            'C': 'C Line - Union Station to Littleton',
            'D': 'D Line - Union Station to Lincoln',
            'E': 'E Line - Union Station to Ridgegate',
            'F': 'F Line - Union Station to Mineral',
            'G': 'G Line - Union Station to Wheat Ridge',
            'H': 'H Line - Union Station to Eastlake',
            'N': 'N Line - Union Station to Thornton',
            'R': 'R Line - Union Station to Peoria',
            'W': 'W Line - Union Station to Golden',
            '0': 'Route 0 - Civic Center Station',
            '15': 'Route 15 - Colfax Avenue',
            '16': 'Route 16 - 16th Street Mall',
            '20': 'Route 20 - East Colfax',
            'FF1': 'Flatiron Flyer - US 36',
            'FREE': 'Free MetroRide - 16th Street',
            'MALL': '16th Street Mall Ride'
        }
        return route_names.get(route_id, f'Route {route_id}')
    
    def _get_route_type(self, route_id: str) -> str:
        """Determine route type"""
        if route_id in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'N', 'R', 'W']:
            return 'Light Rail'
        elif route_id in ['FF1', 'FF2', 'FF3', 'FF4', 'FF5']:
            return 'Bus Rapid Transit'
        elif route_id in ['FREE', 'MALL']:
            return 'Free Shuttle'
        else:
            return 'Local Bus'
    
    def _get_route_description(self, route_id: str) -> str:
        """Get route description"""
        descriptions = {
            'A': 'Connects downtown Denver with Denver International Airport via 40th and Airport stations',
            'B': 'Serves Westminster, Federal Center, and downtown Denver',
            'C': 'Connects Denver Union Station to Littleton and Mineral Station',
            'D': 'Serves downtown Denver and southeast corridor to Lincoln Station',
            'E': 'Connects downtown to southeast suburbs including DTC and RidgeGate',
            'F': 'Serves southeast corridor from Union Station to Mineral Station',
            'G': 'Connects downtown Denver to Wheat Ridge and Arvada',
            'H': 'Serves northeast Denver and Eastlake/124th Station',
            'N': 'Connects Union Station to Thornton and 162nd Avenue',
            'R': 'Serves Aurora and eastern suburbs to Peoria Station',
            'W': 'Connects downtown Denver to Golden and the Federal Center',
            '15': 'Major east-west route along Colfax Avenue',
            '16': 'Downtown circulator connecting major attractions',
            'FREE': 'Free shuttle service along 16th Street Mall',
            'FF1': 'Express bus service along US 36 corridor to Boulder'
        }
        return descriptions.get(route_id, f'RTD bus route serving the Denver metro area')
    
    def _get_simulated_stops(self, route_id: str) -> List[Dict]:
        """
        Generate simulated stop data
        In production, this would parse stops.txt and stop_times.txt
        """
        # Major stops for key routes
        major_stops = {
            'A': [
                {'stop_id': '1', 'name': 'Union Station', 'sequence': 1, 'lat': 39.7539, 'lng': -105.0002},
                {'stop_id': '2', 'name': '38th & Blake Station', 'sequence': 2, 'lat': 39.7689, 'lng': -104.9782},
                {'stop_id': '3', 'name': '40th & Airport Station', 'sequence': 3, 'lat': 39.7816, 'lng': -104.8708},
                {'stop_id': '4', 'name': '61st & Peña Station', 'sequence': 4, 'lat': 39.8026, 'lng': -104.7627},
                {'stop_id': '5', 'name': 'Airport Station', 'sequence': 5, 'lat': 39.8492, 'lng': -104.6731},
            ],
            '15': [
                {'stop_id': '101', 'name': 'Civic Center Station', 'sequence': 1, 'lat': 39.7447, 'lng': -104.9888},
                {'stop_id': '102', 'name': 'Colfax & Broadway', 'sequence': 2, 'lat': 39.7402, 'lng': -104.9877},
                {'stop_id': '103', 'name': 'Colfax & Colorado', 'sequence': 3, 'lat': 39.7402, 'lng': -104.9408},
                {'stop_id': '104', 'name': 'Colfax & Monaco', 'sequence': 4, 'lat': 39.7402, 'lng': -104.8967},
                {'stop_id': '105', 'name': 'Colfax & Yosemite', 'sequence': 5, 'lat': 39.7402, 'lng': -104.8476},
            ],
            'FREE': [
                {'stop_id': '201', 'name': 'Union Station', 'sequence': 1, 'lat': 39.7539, 'lng': -105.0002},
                {'stop_id': '202', 'name': '16th & Wynkoop', 'sequence': 2, 'lat': 39.7534, 'lng': -104.9983},
                {'stop_id': '203', 'name': '16th & Larimer', 'sequence': 3, 'lat': 39.7491, 'lng': -104.9970},
                {'stop_id': '204', 'name': '16th & California', 'sequence': 4, 'lat': 39.7489, 'lng': -104.9910},
                {'stop_id': '205', 'name': '16th & Stout', 'sequence': 5, 'lat': 39.7487, 'lng': -104.9889},
                {'stop_id': '206', 'name': 'Civic Center Station', 'sequence': 6, 'lat': 39.7447, 'lng': -104.9888},
            ]
        }
        
        # Return stops if available, otherwise generic stops
        if route_id in major_stops:
            return major_stops[route_id]
        
        # Generic stops for other routes
        return [
            {'stop_id': f'{route_id}_1', 'name': f'Route {route_id} - Stop 1', 'sequence': 1, 'lat': 39.7392, 'lng': -104.9903},
            {'stop_id': f'{route_id}_2', 'name': f'Route {route_id} - Stop 2', 'sequence': 2, 'lat': 39.7492, 'lng': -104.9803},
            {'stop_id': f'{route_id}_3', 'name': f'Route {route_id} - Stop 3', 'sequence': 3, 'lat': 39.7592, 'lng': -104.9703},
        ]
    
    def _get_simulated_schedule(self, route_id: str) -> Dict:
        """
        Generate simulated schedule data
        In production, this would parse stop_times.txt and calendar.txt
        """
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        
        # Generate next 10 departure times based on route type
        if route_id in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'N', 'R', 'W']:
            # Light rail - every 15 minutes
            frequency = 15
        elif route_id == 'FREE':
            # Free mall ride - every 5 minutes
            frequency = 5
        elif route_id in ['FF1', 'FF2', 'FF3']:
            # BRT - every 10-15 minutes
            frequency = 12
        else:
            # Local bus - every 30 minutes
            frequency = 30
        
        departures = []
        for i in range(10):
            minutes_from_now = (i * frequency)
            next_hour = (current_hour + (current_minute + minutes_from_now) // 60) % 24
            next_minute = (current_minute + minutes_from_now) % 60
            departures.append(f"{next_hour:02d}:{next_minute:02d}")
        
        return {
            'weekday': departures,
            'frequency': f'Every {frequency} minutes',
            'first_departure': '05:00',
            'last_departure': '23:45'
        }
    
    def _get_operating_hours(self, route_id: str) -> Dict:
        """Get route operating hours"""
        # Most routes operate similar hours
        if route_id == 'FREE':
            return {
                'weekday': '6:00 AM - 12:00 AM',
                'saturday': '7:00 AM - 12:00 AM',
                'sunday': '7:00 AM - 10:00 PM'
            }
        elif route_id in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'N', 'R', 'W']:
            return {
                'weekday': '3:30 AM - 1:00 AM',
                'saturday': '4:00 AM - 1:00 AM',
                'sunday': '4:00 AM - 12:00 AM'
            }
        else:
            return {
                'weekday': '5:00 AM - 11:00 PM',
                'saturday': '6:00 AM - 10:00 PM',
                'sunday': '7:00 AM - 9:00 PM'
            }
    
    def get_all_routes_summary(self) -> List[Dict]:
        """Get summary of all available routes"""
        # Common RTD routes
        routes = [
            {'route_id': 'A', 'name': 'A Line', 'type': 'Light Rail'},
            {'route_id': 'B', 'name': 'B Line', 'type': 'Light Rail'},
            {'route_id': 'C', 'name': 'C Line', 'type': 'Light Rail'},
            {'route_id': 'D', 'name': 'D Line', 'type': 'Light Rail'},
            {'route_id': 'E', 'name': 'E Line', 'type': 'Light Rail'},
            {'route_id': 'F', 'name': 'F Line', 'type': 'Light Rail'},
            {'route_id': 'G', 'name': 'G Line', 'type': 'Light Rail'},
            {'route_id': 'H', 'name': 'H Line', 'type': 'Light Rail'},
            {'route_id': 'N', 'name': 'N Line', 'type': 'Light Rail'},
            {'route_id': 'R', 'name': 'R Line', 'type': 'Light Rail'},
            {'route_id': 'W', 'name': 'W Line', 'type': 'Light Rail'},
            {'route_id': '0', 'name': 'Route 0', 'type': 'Local Bus'},
            {'route_id': '15', 'name': 'Route 15', 'type': 'Local Bus'},
            {'route_id': '16', 'name': 'Route 16', 'type': 'Local Bus'},
            {'route_id': 'FREE', 'name': 'Free MetroRide', 'type': 'Free Shuttle'},
            {'route_id': 'FF1', 'name': 'Flatiron Flyer', 'type': 'BRT'},
        ]
        return routes


if __name__ == "__main__":
    # Test the module
    client = RouteDetailsClient()
    
    # Test A Line
    print("Testing A Line Details:")
    print("="*60)
    route_info = client.get_route_info('A')
    print(f"Route: {route_info['route_name']}")
    print(f"Type: {route_info['route_type']}")
    print(f"Description: {route_info['description']}")
    print(f"\nStops ({len(route_info['stops'])}):")
    for stop in route_info['stops']:
        print(f"  {stop['sequence']}. {stop['name']}")
    print(f"\nSchedule: {route_info['schedule']['frequency']}")
    print(f"Next departures: {', '.join(route_info['schedule']['weekday'][:5])}")


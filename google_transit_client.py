"""
Google Maps Transit API Client
Provides access to RTD transit data via Google Maps APIs
"""

import requests
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


class GoogleTransitClient:
    """Client for accessing RTD data via Google Maps APIs"""
    
    def __init__(self, api_key: str):
        """
        Initialize the Google Maps Transit client
        
        Args:
            api_key: Your Google Maps API key
                    Get one at: https://console.cloud.google.com/google/maps-apis
        """
        self.api_key = api_key
        self.directions_url = "https://maps.googleapis.com/maps/api/directions/json"
        self.geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
    def get_transit_directions(
        self,
        origin: str,
        destination: str,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        alternatives: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Get transit directions between two locations
        
        Args:
            origin: Starting location (address, place name, or coordinates)
            destination: Ending location (address, place name, or coordinates)
            departure_time: Desired departure time (default: now)
            arrival_time: Desired arrival time (overrides departure_time)
            alternatives: Return multiple route options
        
        Returns:
            Dictionary with route information including:
            - routes: List of possible routes
            - steps: Detailed transit steps
            - duration: Trip duration
            - arrival_time: Estimated arrival time
        """
        params = {
            'origin': origin,
            'destination': destination,
            'mode': 'transit',
            'key': self.api_key,
            'alternatives': str(alternatives).lower()
        }
        
        # Add time parameter
        if arrival_time:
            params['arrival_time'] = int(arrival_time.timestamp())
        elif departure_time:
            params['departure_time'] = int(departure_time.timestamp())
        else:
            params['departure_time'] = 'now'
        
        try:
            response = requests.get(self.directions_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return self._parse_directions(data)
            else:
                print(f"API Error: {data['status']} - {data.get('error_message', '')}")
                return None
        except Exception as e:
            print(f"Error fetching directions: {e}")
            return None
    
    def _parse_directions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the Google Directions API response"""
        routes = []
        
        for route in data.get('routes', []):
            for leg in route.get('legs', []):
                parsed_route = {
                    'summary': route.get('summary', ''),
                    'duration': leg.get('duration', {}).get('text', ''),
                    'duration_seconds': leg.get('duration', {}).get('value', 0),
                    'distance': leg.get('distance', {}).get('text', ''),
                    'distance_meters': leg.get('distance', {}).get('value', 0),
                    'start_address': leg.get('start_address', ''),
                    'end_address': leg.get('end_address', ''),
                    'departure_time': leg.get('departure_time', {}).get('text', ''),
                    'arrival_time': leg.get('arrival_time', {}).get('text', ''),
                    'steps': []
                }
                
                # Parse each step
                for step in leg.get('steps', []):
                    step_info = {
                        'travel_mode': step.get('travel_mode', ''),
                        'duration': step.get('duration', {}).get('text', ''),
                        'distance': step.get('distance', {}).get('text', ''),
                        'instructions': step.get('html_instructions', ''),
                        'start_location': step.get('start_location', {}),
                        'end_location': step.get('end_location', {})
                    }
                    
                    # Add transit-specific details
                    if 'transit_details' in step:
                        transit = step['transit_details']
                        step_info['transit'] = {
                            'line': transit.get('line', {}).get('name', ''),
                            'line_short_name': transit.get('line', {}).get('short_name', ''),
                            'vehicle_type': transit.get('line', {}).get('vehicle', {}).get('type', ''),
                            'departure_stop': transit.get('departure_stop', {}).get('name', ''),
                            'arrival_stop': transit.get('arrival_stop', {}).get('name', ''),
                            'departure_time': transit.get('departure_time', {}).get('text', ''),
                            'arrival_time': transit.get('arrival_time', {}).get('text', ''),
                            'num_stops': transit.get('num_stops', 0),
                            'headsign': transit.get('headsign', ''),
                        }
                    
                    parsed_route['steps'].append(step_info)
                
                routes.append(parsed_route)
        
        return {
            'status': data['status'],
            'routes': routes
        }
    
    def find_nearby_transit_stations(
        self,
        location: str,
        radius: int = 1000
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Find nearby transit stations
        
        Args:
            location: Location to search near (address or coordinates)
            radius: Search radius in meters (default: 1000m = ~0.6 miles)
        
        Returns:
            List of nearby transit stations
        """
        # First geocode the location
        coords = self._geocode(location)
        if not coords:
            return None
        
        params = {
            'location': f"{coords['lat']},{coords['lng']}",
            'radius': radius,
            'type': 'transit_station',
            'key': self.api_key
        }
        
        try:
            response = requests.get(self.places_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                stations = []
                for place in data.get('results', []):
                    stations.append({
                        'name': place.get('name', ''),
                        'address': place.get('vicinity', ''),
                        'location': place.get('geometry', {}).get('location', {}),
                        'place_id': place.get('place_id', ''),
                        'rating': place.get('rating', None),
                        'types': place.get('types', [])
                    })
                return stations
            else:
                print(f"API Error: {data['status']}")
                return None
        except Exception as e:
            print(f"Error finding stations: {e}")
            return None
    
    def _geocode(self, address: str) -> Optional[Dict[str, float]]:
        """Convert address to coordinates"""
        params = {
            'address': address,
            'key': self.api_key
        }
        
        try:
            response = requests.get(self.geocode_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK' and len(data['results']) > 0:
                location = data['results'][0]['geometry']['location']
                return {'lat': location['lat'], 'lng': location['lng']}
            return None
        except Exception as e:
            print(f"Error geocoding: {e}")
            return None
    
    def get_trip_from_union_station(
        self,
        destination: str,
        departure_time: Optional[datetime] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Convenience method to get trips from Union Station
        
        Args:
            destination: Where you want to go
            departure_time: When you want to leave
        
        Returns:
            Route information
        """
        return self.get_transit_directions(
            origin="Union Station, Denver, CO",
            destination=destination,
            departure_time=departure_time
        )
    
    def get_next_departures(
        self,
        from_location: str,
        to_location: str,
        num_options: int = 3
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get next few departure options
        
        Args:
            from_location: Starting location
            to_location: Destination
            num_options: Number of departure times to check
        
        Returns:
            List of route options at different times
        """
        routes = []
        now = datetime.now()
        
        for i in range(num_options):
            departure_time = now + timedelta(minutes=i * 15)
            result = self.get_transit_directions(
                origin=from_location,
                destination=to_location,
                departure_time=departure_time,
                alternatives=False
            )
            
            if result and result['routes']:
                routes.append({
                    'departure_time': departure_time.strftime('%I:%M %p'),
                    'route': result['routes'][0]
                })
        
        return routes if routes else None


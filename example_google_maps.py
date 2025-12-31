"""
Example usage of Google Maps Transit API for RTD data
This demonstrates how to use Google Maps to get RTD transit information
"""

from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY, COMMON_LOCATIONS, validate_google_api_key
from datetime import datetime, timedelta


def print_separator():
    print("\n" + "="*80 + "\n")


def main():
    print_separator()
    print("Google Maps Transit API - RTD Denver Examples")
    print_separator()
    
    # Validate API key
    if not validate_google_api_key():
        print("Please configure your Google Maps API key in config.py")
        print("Example: GOOGLE_MAPS_API_KEY = 'your-api-key-here'")
        return
    
    # Initialize the client
    client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)
    
    # Example 1: Get transit directions
    print("EXAMPLE 1: Transit Directions")
    print("-" * 80)
    print("Getting directions from Union Station to Denver Airport...\n")
    
    result = client.get_transit_directions(
        origin=COMMON_LOCATIONS['union_station'],
        destination=COMMON_LOCATIONS['airport']
    )
    
    if result and result['routes']:
        route = result['routes'][0]
        print(f"📍 From: {route['start_address']}")
        print(f"📍 To: {route['end_address']}")
        print(f"⏱️  Duration: {route['duration']}")
        print(f"📏 Distance: {route['distance']}")
        print(f"🚀 Departure: {route['departure_time']}")
        print(f"🎯 Arrival: {route['arrival_time']}")
        print(f"\n🚶‍♂️ Steps:")
        
        for i, step in enumerate(route['steps'], 1):
            if step['travel_mode'] == 'TRANSIT':
                transit = step['transit']
                print(f"\n  {i}. Take {transit['vehicle_type']}: {transit['line']} ({transit['line_short_name']})")
                print(f"     • Board at: {transit['departure_stop']}")
                print(f"     • Get off at: {transit['arrival_stop']}")
                print(f"     • Headsign: {transit['headsign']}")
                print(f"     • Stops: {transit['num_stops']}")
                print(f"     • Duration: {step['duration']}")
            elif step['travel_mode'] == 'WALKING':
                print(f"\n  {i}. Walk {step['distance']} ({step['duration']})")
    else:
        print("No routes found")
    
    # Example 2: Find nearby transit stations
    print_separator()
    print("EXAMPLE 2: Find Nearby Transit Stations")
    print("-" * 80)
    print("Finding transit stations near Downtown Denver...\n")
    
    stations = client.find_nearby_transit_stations(
        location=COMMON_LOCATIONS['downtown'],
        radius=1000
    )
    
    if stations:
        print(f"Found {len(stations)} stations within 1000 meters:\n")
        for i, station in enumerate(stations[:5], 1):
            print(f"{i}. {station['name']}")
            print(f"   Address: {station['address']}")
            print(f"   Location: ({station['location']['lat']}, {station['location']['lng']})")
            if station['rating']:
                print(f"   Rating: {station['rating']}/5")
            print()
    else:
        print("No stations found")
    
    # Example 3: Multiple route options
    print_separator()
    print("EXAMPLE 3: Compare Multiple Routes")
    print("-" * 80)
    print("Getting alternative routes from Capitol to Union Station...\n")
    
    result = client.get_transit_directions(
        origin=COMMON_LOCATIONS['capitol'],
        destination=COMMON_LOCATIONS['union_station'],
        alternatives=True
    )
    
    if result and result['routes']:
        print(f"Found {len(result['routes'])} route options:\n")
        for i, route in enumerate(result['routes'], 1):
            print(f"Option {i}:")
            print(f"  Duration: {route['duration']}")
            print(f"  Distance: {route['distance']}")
            print(f"  Summary: {route['summary']}")
            print(f"  Steps: {len(route['steps'])}")
            print()
    else:
        print("No routes found")
    
    # Example 4: Plan ahead - departure at specific time
    print_separator()
    print("EXAMPLE 4: Schedule Trip for Later")
    print("-" * 80)
    
    future_time = datetime.now() + timedelta(hours=2)
    print(f"Planning trip from Coors Field to Cherry Creek for {future_time.strftime('%I:%M %p')}...\n")
    
    result = client.get_transit_directions(
        origin=COMMON_LOCATIONS['coors_field'],
        destination=COMMON_LOCATIONS['cherry_creek'],
        departure_time=future_time
    )
    
    if result and result['routes']:
        route = result['routes'][0]
        print(f"🚀 Departure: {route['departure_time']}")
        print(f"🎯 Arrival: {route['arrival_time']}")
        print(f"⏱️  Duration: {route['duration']}")
        print(f"📏 Distance: {route['distance']}")
        print(f"\nNumber of steps: {len(route['steps'])}")
    else:
        print("No routes found")
    
    # Example 5: Next few departure options
    print_separator()
    print("EXAMPLE 5: Next Departure Times")
    print("-" * 80)
    print("Getting next 3 departure options from 16th Street Mall to Airport...\n")
    
    options = client.get_next_departures(
        from_location=COMMON_LOCATIONS['16th_street_mall'],
        to_location=COMMON_LOCATIONS['airport'],
        num_options=3
    )
    
    if options:
        for i, option in enumerate(options, 1):
            route = option['route']
            print(f"Departure {i}: {option['departure_time']}")
            print(f"  Arrives: {route['arrival_time']}")
            print(f"  Duration: {route['duration']}")
            print()
    else:
        print("No options found")
    
    print_separator()
    print("Examples completed!")
    print_separator()


if __name__ == "__main__":
    main()


"""
Comprehensive example using all available RTD transit APIs
Demonstrates RTD direct APIs and Google Maps Transit API
"""

from rtd_client import RTDClient
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY, COMMON_LOCATIONS, validate_google_api_key


def print_separator(title=None):
    print("\n" + "="*80)
    if title:
        print(f"  {title}")
        print("="*80)
    print()


def main():
    print_separator("RTD Denver - Multi-API Transit Client Demo")
    
    print("This example demonstrates accessing RTD transit data through:")
    print("  1. RTD's Direct APIs (GTFS Realtime)")
    print("  2. Google Maps Transit API")
    print()
    
    # ==========================================================================
    # RTD Direct API Examples
    # ==========================================================================
    
    print_separator("Part 1: RTD Direct APIs (Real-time Vehicle Tracking)")
    
    rtd_client = RTDClient()
    
    print("🚌 Fetching real-time vehicle positions...\n")
    vehicles = rtd_client.get_vehicle_positions()
    
    if vehicles:
        print(f"✅ Found {len(vehicles)} active RTD vehicles")
        print("\nShowing first 5 vehicles:\n")
        
        for i, vehicle in enumerate(vehicles[:5], 1):
            print(f"{i}. Vehicle: {vehicle['vehicle_id']}")
            print(f"   Route: {vehicle['route_id']}")
            print(f"   Location: ({vehicle['latitude']:.6f}, {vehicle['longitude']:.6f})")
            if vehicle['bearing']:
                print(f"   Heading: {vehicle['bearing']}°")
            print()
        
        # Group vehicles by route
        route_counts = {}
        for vehicle in vehicles:
            route = vehicle['route_id']
            route_counts[route] = route_counts.get(route, 0) + 1
        
        print("Active vehicles by route:")
        for route in sorted(route_counts.keys())[:10]:
            print(f"  • Route {route}: {route_counts[route]} vehicles")
    else:
        print("❌ Could not fetch vehicle positions")
    
    # ==========================================================================
    # Google Maps Transit API Examples
    # ==========================================================================
    
    print_separator("Part 2: Google Maps Transit API (Trip Planning)")
    
    if not validate_google_api_key():
        print("⚠️  Google Maps API key not configured.")
        print("   To use Google Maps features, set your API key in config.py")
        print("   Get one at: https://console.cloud.google.com/google/maps-apis")
        print("\nSkipping Google Maps examples...\n")
    else:
        google_client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)
        
        # Example: Get directions from Union Station to Airport
        print("🗺️  Getting transit directions from Union Station to Denver Airport...\n")
        
        result = google_client.get_transit_directions(
            origin=COMMON_LOCATIONS['union_station'],
            destination=COMMON_LOCATIONS['airport']
        )
        
        if result and result['routes']:
            route = result['routes'][0]
            print(f"📍 Route: {route['start_address']} → {route['end_address']}")
            print(f"⏱️  Duration: {route['duration']}")
            print(f"📏 Distance: {route['distance']}")
            print(f"🚀 Departure: {route['departure_time']}")
            print(f"🎯 Arrival: {route['arrival_time']}")
            print(f"\nTrip breakdown:")
            
            for i, step in enumerate(route['steps'], 1):
                if step['travel_mode'] == 'TRANSIT':
                    transit = step['transit']
                    print(f"\n  Step {i}: {transit['vehicle_type']} - {transit['line_short_name']}")
                    print(f"    From: {transit['departure_stop']}")
                    print(f"    To: {transit['arrival_stop']}")
                    print(f"    Duration: {step['duration']}")
                elif step['travel_mode'] == 'WALKING':
                    print(f"\n  Step {i}: Walk {step['distance']} ({step['duration']})")
        else:
            print("No routes found")
        
        # Example: Find nearby stations
        print_separator()
        print("🚏 Finding transit stations near Downtown Denver...\n")
        
        stations = google_client.find_nearby_transit_stations(
            location=COMMON_LOCATIONS['downtown'],
            radius=800
        )
        
        if stations:
            print(f"Found {len(stations)} stations within 800 meters:\n")
            for i, station in enumerate(stations[:5], 1):
                print(f"{i}. {station['name']}")
                print(f"   {station['address']}")
                if station['rating']:
                    print(f"   ⭐ Rating: {station['rating']}/5")
                print()
        else:
            print("No stations found")
    
    # ==========================================================================
    # Summary
    # ==========================================================================
    
    print_separator("Summary")
    
    print("📊 Available Features:")
    print()
    print("RTD Direct APIs:")
    print("  ✅ Real-time vehicle positions (working)")
    print("  ❌ Trip updates (endpoint unavailable)")
    print("  ❌ Service alerts (endpoint unavailable)")
    print("  ❌ Static GTFS feed (endpoint unavailable)")
    print()
    print("Google Maps Transit API:")
    if validate_google_api_key():
        print("  ✅ Trip planning with real-time data")
        print("  ✅ Multiple route options")
        print("  ✅ Scheduled departure times")
        print("  ✅ Station finder")
        print("  ✅ Walking directions")
    else:
        print("  ⚠️  Requires API key configuration")
    print()
    print("💡 Recommendation: Use Google Maps API for complete trip planning")
    print("   and RTD Direct API for real-time vehicle tracking!")
    
    print_separator()


if __name__ == "__main__":
    main()


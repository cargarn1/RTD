#!/usr/bin/env python3
"""
Get Transit Routes by Address
Simple script to find RTD routes from any address
"""

import sys
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY, validate_google_api_key, COMMON_LOCATIONS


def get_routes_from_address(origin, destination=None):
    """
    Get transit routes from an address
    
    Args:
        origin: Starting address
        destination: Ending address (optional, defaults to Union Station)
    """
    
    # Check if Google Maps is configured
    if not validate_google_api_key():
        print("\n❌ Google Maps API key not configured!")
        print("   Add your key to config.py:")
        print("   GOOGLE_MAPS_API_KEY = 'your-key-here'")
        print("\n   Get a free key at: https://console.cloud.google.com/")
        return None
    
    # Use Union Station as default destination
    if not destination:
        destination = "Union Station, Denver, CO"
    
    print("\n" + "="*80)
    print(f"🚌 Finding RTD Routes")
    print("="*80)
    print(f"\n📍 From: {origin}")
    print(f"📍 To:   {destination}")
    print("\nSearching...")
    
    # Get directions
    client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)
    result = client.get_transit_directions(
        origin=origin,
        destination=destination,
        alternatives=True  # Get multiple route options
    )
    
    if not result or not result.get('routes'):
        print("\n❌ No routes found. Check your addresses and try again.")
        return None
    
    # Display results
    routes = result['routes']
    print(f"\n✅ Found {len(routes)} route option(s)!\n")
    print("="*80)
    
    for i, route in enumerate(routes, 1):
        print(f"\n🚍 ROUTE OPTION {i}")
        print("-"*80)
        print(f"⏱️  Duration: {route['duration']}")
        print(f"📏 Distance: {route['distance']}")
        print(f"🚀 Depart:   {route['departure_time']}")
        print(f"🎯 Arrive:   {route['arrival_time']}")
        
        if route['summary']:
            print(f"📋 Summary:  {route['summary']}")
        
        print(f"\n📝 Step-by-Step Directions:")
        print()
        
        step_num = 1
        for step in route['steps']:
            if step['travel_mode'] == 'TRANSIT':
                transit = step['transit']
                print(f"  {step_num}. 🚌 Take {transit['vehicle_type']}: {transit['line_short_name']}")
                print(f"     Line: {transit['line']}")
                print(f"     Board at: {transit['departure_stop']}")
                print(f"     Get off at: {transit['arrival_stop']}")
                if transit['headsign']:
                    print(f"     Headsign: {transit['headsign']}")
                print(f"     Stops: {transit['num_stops']} stops")
                print(f"     Depart: {transit['departure_time']}")
                print(f"     Arrive: {transit['arrival_time']}")
                print(f"     Duration: {step['duration']}")
                
            elif step['travel_mode'] == 'WALKING':
                print(f"  {step_num}. 🚶 Walk {step['distance']} ({step['duration']})")
            
            print()
            step_num += 1
        
        if i < len(routes):
            print("="*80)
    
    return routes


def main():
    """Main function with command-line interface"""
    
    print("\n" + "="*80)
    print("🚌 RTD Transit Route Finder")
    print("="*80)
    
    # Check for command-line arguments
    if len(sys.argv) >= 2:
        origin = sys.argv[1]
        destination = sys.argv[2] if len(sys.argv) >= 3 else None
    else:
        # Interactive mode
        print("\nEnter addresses to find transit routes.")
        print("Common locations available:")
        for key, value in COMMON_LOCATIONS.items():
            print(f"  • {key}: {value}")
        print()
        
        origin = input("📍 Starting address (or press Enter for Union Station): ").strip()
        if not origin:
            origin = COMMON_LOCATIONS['union_station']
        elif origin.lower() in COMMON_LOCATIONS:
            origin = COMMON_LOCATIONS[origin.lower()]
        
        destination = input("📍 Destination address (or press Enter for Denver Airport): ").strip()
        if not destination:
            destination = COMMON_LOCATIONS['airport']
        elif destination.lower() in COMMON_LOCATIONS:
            destination = COMMON_LOCATIONS[destination.lower()]
    
    # Get routes
    routes = get_routes_from_address(origin, destination)
    
    if routes:
        print("\n" + "="*80)
        print("✅ Route search complete!")
        print("="*80)
        print(f"\nTip: You can also run this script with addresses:")
        print(f'  python3 get_routes.py "Your Address" "Destination"')
        print()
    else:
        print("\n⚠️  No routes found. Please check:")
        print("  • Addresses are in Denver RTD service area")
        print("  • Google Maps API key is configured")
        print("  • Addresses are spelled correctly")
        print()


if __name__ == "__main__":
    main()


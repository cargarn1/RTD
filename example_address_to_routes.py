#!/usr/bin/env python3
"""
Simple Example: Get Routes from an Address
Shows how to find RTD transit routes from any Denver address
"""

from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY, validate_google_api_key


def main():
    print("\n" + "="*80)
    print("🚌 Example: Get RTD Routes from Any Address")
    print("="*80)
    
    # Check if Google Maps is configured
    if not validate_google_api_key():
        print("\n⚠️  Google Maps API key not configured!")
        print("   Add your key to config.py to use this feature")
        print("   Get a free key at: https://console.cloud.google.com/")
        return
    
    # Initialize the client
    client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)
    
    # Example 1: Simple address lookup
    print("\n" + "-"*80)
    print("Example 1: Get routes from Union Station to Airport")
    print("-"*80)
    
    result = client.get_transit_directions(
        origin="Union Station, Denver, CO",
        destination="Denver International Airport"
    )
    
    if result and result['routes']:
        route = result['routes'][0]
        print(f"\n✅ Found route!")
        print(f"   Duration: {route['duration']}")
        print(f"   Distance: {route['distance']}")
        print(f"   Depart: {route['departure_time']}")
        print(f"   Arrive: {route['arrival_time']}")
        
        print(f"\n   Step-by-step:")
        for i, step in enumerate(route['steps'], 1):
            if step['travel_mode'] == 'TRANSIT':
                transit = step['transit']
                print(f"   {i}. Take {transit['line_short_name']} from {transit['departure_stop']}")
                print(f"      → to {transit['arrival_stop']} ({transit['num_stops']} stops)")
            else:
                print(f"   {i}. Walk {step['distance']}")
    
    # Example 2: Try a specific street address
    print("\n" + "-"*80)
    print("Example 2: From a street address to downtown")
    print("-"*80)
    
    result = client.get_transit_directions(
        origin="1500 Wynkoop St, Denver, CO",  # Specific address
        destination="Colorado State Capitol, Denver, CO"
    )
    
    if result and result['routes']:
        route = result['routes'][0]
        print(f"\n✅ Route found!")
        print(f"   From: {route['start_address']}")
        print(f"   To: {route['end_address']}")
        print(f"   Duration: {route['duration']} - Distance: {route['distance']}")
    
    # Example 3: Get multiple route options
    print("\n" + "-"*80)
    print("Example 3: Compare multiple route options")
    print("-"*80)
    
    result = client.get_transit_directions(
        origin="Coors Field, Denver, CO",
        destination="Cherry Creek Shopping Center, Denver, CO",
        alternatives=True  # Get multiple options!
    )
    
    if result and result['routes']:
        print(f"\n✅ Found {len(result['routes'])} route options:")
        for i, route in enumerate(result['routes'], 1):
            print(f"\n   Option {i}:")
            print(f"   • Duration: {route['duration']}")
            print(f"   • Distance: {route['distance']}")
            print(f"   • Via: {route['summary']}")
    
    # Example 4: Your own addresses!
    print("\n" + "="*80)
    print("✨ Try Your Own Addresses!")
    print("="*80)
    print("\nYou can use this code with ANY Denver address:")
    print("\nPython code:")
    print("""
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY

client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)
result = client.get_transit_directions(
    origin="YOUR ADDRESS HERE",
    destination="YOUR DESTINATION HERE"
)
    """)
    
    print("\nOr use the interactive script:")
    print("  python3 get_routes.py")
    
    print("\nOr command line:")
    print('  python3 get_routes.py "Your Address" "Destination"')
    
    print("\n" + "="*80)
    print("✅ Examples Complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()


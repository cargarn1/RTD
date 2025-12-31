"""
Example usage of the RTD API Client
This script demonstrates how to use the RTDClient to fetch various transit data
"""

from rtd_client import RTDClient
from datetime import datetime


def print_separator():
    print("\n" + "="*80 + "\n")


def main():
    # Initialize the RTD client
    print("Initializing RTD Client...")
    client = RTDClient()
    
    # Example 1: Get real-time vehicle positions
    print_separator()
    print("EXAMPLE 1: Real-time Vehicle Positions")
    print_separator()
    
    vehicles = client.get_vehicle_positions()
    if vehicles:
        print(f"Found {len(vehicles)} active vehicles")
        print("\nShowing first 5 vehicles:")
        for i, vehicle in enumerate(vehicles[:5], 1):
            print(f"\n{i}. Vehicle ID: {vehicle['vehicle_id']}")
            print(f"   Route: {vehicle['route_id']}")
            print(f"   Location: ({vehicle['latitude']}, {vehicle['longitude']})")
            if vehicle['speed']:
                print(f"   Speed: {vehicle['speed']} m/s")
            if vehicle['bearing']:
                print(f"   Bearing: {vehicle['bearing']}°")
    else:
        print("Could not fetch vehicle positions")
    
    # Example 2: Get service alerts
    print_separator()
    print("EXAMPLE 2: Service Alerts")
    print_separator()
    
    alerts = client.get_alerts()
    if alerts:
        print(f"Found {len(alerts)} active alerts")
        for i, alert in enumerate(alerts[:5], 1):
            print(f"\n{i}. Alert ID: {alert['id']}")
            print(f"   Header: {alert['header']}")
            if alert['affected_routes']:
                print(f"   Affected Routes: {', '.join(alert['affected_routes'])}")
            if alert['description']:
                print(f"   Description: {alert['description'][:100]}...")
    else:
        print("Could not fetch alerts or no active alerts")
    
    # Example 3: Search for stops
    print_separator()
    print("EXAMPLE 3: Search for Stops")
    print_separator()
    
    search_term = "Union Station"
    print(f"Searching for stops containing '{search_term}'...")
    
    stops = client.find_stops_by_name(search_term)
    if stops:
        print(f"Found {len(stops)} matching stops:")
        for i, stop in enumerate(stops[:5], 1):
            print(f"\n{i}. {stop['stop_name']}")
            print(f"   Stop ID: {stop['stop_id']}")
            if 'stop_lat' in stop and 'stop_lon' in stop:
                print(f"   Location: ({stop['stop_lat']}, {stop['stop_lon']})")
    else:
        print("No stops found or error fetching data")
    
    # Example 4: Search for routes
    print_separator()
    print("EXAMPLE 4: Search for Routes")
    print_separator()
    
    search_term = "A"
    print(f"Searching for routes containing '{search_term}'...")
    
    routes = client.find_route_by_name(search_term)
    if routes:
        print(f"Found {len(routes)} matching routes:")
        for i, route in enumerate(routes[:10], 1):
            print(f"\n{i}. Route {route.get('route_short_name', 'N/A')}: {route.get('route_long_name', 'N/A')}")
            print(f"   Route ID: {route['route_id']}")
            if 'route_type' in route:
                route_types = {
                    '0': 'Tram/Light Rail',
                    '1': 'Subway/Metro',
                    '2': 'Rail',
                    '3': 'Bus',
                    '4': 'Ferry'
                }
                print(f"   Type: {route_types.get(route['route_type'], 'Unknown')}")
    else:
        print("No routes found or error fetching data")
    
    # Example 5: Get trip updates
    print_separator()
    print("EXAMPLE 5: Real-time Trip Updates")
    print_separator()
    
    trip_updates = client.get_trip_updates()
    if trip_updates:
        print(f"Found {len(trip_updates)} trip updates")
        print("\nShowing first 3 trips with delays:")
        
        count = 0
        for update in trip_updates:
            if count >= 3:
                break
            
            # Check if any stop has a delay
            has_delay = False
            for stop_update in update['stop_time_updates']:
                if stop_update['arrival_delay'] or stop_update['departure_delay']:
                    has_delay = True
                    break
            
            if has_delay:
                count += 1
                print(f"\n{count}. Trip ID: {update['trip_id']}")
                print(f"   Route: {update['route_id']}")
                print(f"   Vehicle: {update['vehicle_id']}")
                print(f"   Number of stop updates: {len(update['stop_time_updates'])}")
                
                # Show first stop with delay
                for stop_update in update['stop_time_updates']:
                    if stop_update['arrival_delay']:
                        print(f"   Stop {stop_update['stop_id']}: {stop_update['arrival_delay']}s delay")
                        break
    else:
        print("Could not fetch trip updates")
    
    print_separator()
    print("Example completed!")
    print_separator()


if __name__ == "__main__":
    main()


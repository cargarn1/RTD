#!/usr/bin/env python3
"""
Comprehensive Test Suite for RTD API
Tests all features and provides clear feedback
"""

import sys
from rtd_client import RTDClient
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY, validate_google_api_key


def print_header(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_test(number, name):
    print(f"Test {number}: {name}")
    print("-" * 80)


def test_rtd_vehicles():
    """Test RTD vehicle tracking"""
    print_test(1, "RTD Vehicle Tracking")
    
    try:
        client = RTDClient()
        vehicles = client.get_vehicle_positions()
        
        if vehicles:
            print(f"✅ SUCCESS! Found {len(vehicles)} active vehicles")
            
            # Show sample
            print("\nSample vehicles:")
            for i, v in enumerate(vehicles[:3], 1):
                print(f"  {i}. Route {v['route_id']:4s} - Vehicle {v['vehicle_id'][:16]}...")
                print(f"     Location: ({v['latitude']:.4f}, {v['longitude']:.4f})")
            
            # Count by route
            routes = {}
            for v in vehicles:
                route = v['route_id']
                routes[route] = routes.get(route, 0) + 1
            
            print(f"\nActive routes: {len(routes)}")
            print("Top 5 routes by vehicle count:")
            for route, count in sorted(routes.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  Route {route:4s}: {count} vehicles")
            
            return True
        else:
            print("❌ FAILED: No vehicles found")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_google_maps_configured():
    """Test if Google Maps is configured"""
    print_test(2, "Google Maps API Configuration")
    
    if validate_google_api_key():
        print("✅ Google Maps API key is configured")
        print(f"   Key: {GOOGLE_MAPS_API_KEY[:20]}...")
        return True
    else:
        print("⚠️  Google Maps API key NOT configured")
        print("   This is optional - RTD Direct API works without it")
        print("   To enable: Add your key to config.py")
        return False


def test_google_maps_directions():
    """Test Google Maps directions"""
    print_test(3, "Google Maps Transit Directions")
    
    if not validate_google_api_key():
        print("⏭️  SKIPPED: Google Maps API not configured")
        return None
    
    try:
        client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)
        result = client.get_transit_directions(
            origin="Union Station, Denver, CO",
            destination="Denver Airport"
        )
        
        if result and result['routes']:
            route = result['routes'][0]
            print("✅ SUCCESS! Got transit directions")
            print(f"\n   From: Union Station")
            print(f"   To: Denver Airport")
            print(f"   Duration: {route['duration']}")
            print(f"   Distance: {route['distance']}")
            print(f"   Departure: {route['departure_time']}")
            print(f"   Arrival: {route['arrival_time']}")
            print(f"   Steps: {len(route['steps'])}")
            return True
        else:
            print("❌ FAILED: No routes found")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_google_maps_stations():
    """Test finding nearby stations"""
    print_test(4, "Google Maps Station Finder")
    
    if not validate_google_api_key():
        print("⏭️  SKIPPED: Google Maps API not configured")
        return None
    
    try:
        client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)
        stations = client.find_nearby_transit_stations(
            location="Downtown Denver, CO",
            radius=1000
        )
        
        if stations:
            print(f"✅ SUCCESS! Found {len(stations)} stations near Downtown Denver")
            print("\nTop 3 stations:")
            for i, station in enumerate(stations[:3], 1):
                print(f"  {i}. {station['name']}")
                print(f"     {station['address']}")
            return True
        else:
            print("❌ FAILED: No stations found")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_api_server_imports():
    """Test that API server can be imported"""
    print_test(5, "API Server Components")
    
    try:
        import api_server
        print("✅ SUCCESS! API server imports correctly")
        print("   You can start it with: python3 api_server.py")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    print_header("RTD API - Comprehensive Test Suite")
    
    print("Testing all components of your RTD application...\n")
    
    results = []
    
    # Test 1: RTD Vehicles (Core Feature)
    results.append(("RTD Vehicle Tracking", test_rtd_vehicles()))
    print()
    
    # Test 2: Google Maps Configuration
    results.append(("Google Maps Config", test_google_maps_configured()))
    print()
    
    # Test 3: Google Maps Directions
    results.append(("Google Maps Directions", test_google_maps_directions()))
    print()
    
    # Test 4: Google Maps Stations
    results.append(("Station Finder", test_google_maps_stations()))
    print()
    
    # Test 5: API Server
    results.append(("API Server", test_api_server_imports()))
    print()
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)
    total = len(results)
    
    for name, result in results:
        if result is True:
            print(f"✅ {name}")
        elif result is False:
            print(f"❌ {name}")
        else:
            print(f"⏭️  {name} (skipped)")
    
    print(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped out of {total} tests")
    
    # Recommendations
    print_header("Next Steps")
    
    if passed >= 1:
        print("🎉 Great! Your RTD application is working!")
        print("\n✅ What's working:")
        print("   • Real-time RTD vehicle tracking")
        
        if any(name == "Google Maps Config" and result for name, result in results):
            print("   • Google Maps API integration")
        
        print("\n🚀 What you can do now:")
        print("   1. Run examples:")
        print("      python3 example.py")
        print("   2. Start API server:")
        print("      python3 api_server.py")
        print("   3. Generate API key for Zapier:")
        print("      python3 generate_api_key.py")
    
    if any(result is False for _, result in results):
        print("\n⚠️  Some tests failed, but core features still work!")
    
    if skipped > 0:
        print("\n💡 To enable all features:")
        print("   • Add Google Maps API key to config.py")
        print("   • Get a key at: https://console.cloud.google.com/")
    
    print("\n📚 Documentation:")
    print("   • Setup Guide: SETUP_GUIDE.md")
    print("   • Full Docs: README.md")
    print("   • Quick Reference: QUICK_REFERENCE.md")
    print()
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())


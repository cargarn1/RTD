# RTD Denver Transportation API Client

A comprehensive Python client for accessing RTD (Regional Transportation District) Denver's transportation data through multiple APIs:
- **RTD Direct APIs**: Real-time vehicle tracking via GTFS feeds
- **Google Maps Transit API**: Complete trip planning with RTD integration

## Features

### RTD Direct APIs
- 📍 **Real-time Vehicle Positions**: Track buses and trains in real-time
- 🚌 **Live Fleet Monitoring**: See all active vehicles on RTD network

### Google Maps Transit API  
- 🗺️ **Trip Planning**: Get detailed transit directions with RTD
- ⏰ **Schedule Planning**: Departure and arrival times
- 🚏 **Station Finder**: Discover nearby transit stops
- 🔀 **Multiple Routes**: Compare different route options
- 🚶‍♂️ **Walking Directions**: Integrated pedestrian navigation
- 📊 **Real-time Updates**: Live transit data including delays

## Installation

### 1. Clone or navigate to this directory

```bash
cd /Users/carlosgarcia/Documents/Code/RTD
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys (for Google Maps features)

Copy the example config file and add your API key:

```bash
cp config_example.py config.py
```

Then edit `config.py` and add your Google Maps API key:

```python
GOOGLE_MAPS_API_KEY = 'your-api-key-here'
```

**Getting a Google Maps API Key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/google/maps-apis)
2. Create a new project or select an existing one
3. Enable these APIs:
   - Directions API
   - Places API
   - Geocoding API
4. Create credentials (API Key)
5. Copy your API key to `config.py`

**Note**: Google Maps API has a free tier with $200/month credit (typically ~40,000 requests).

## Quick Start

### Run the Main Example

```bash
python3 example.py
```

This comprehensive example demonstrates:
- Real-time RTD vehicle tracking
- Google Maps transit directions
- Station finding
- Trip planning

### Run Individual Examples

```bash
# RTD Direct API only (no API key needed)
python3 example_rtd_only.py

# Google Maps Transit API examples
python3 example_google_maps.py
```

## Usage Examples

### 1. Real-time Vehicle Tracking (RTD Direct API)

```python
from rtd_client import RTDClient

# No API key needed!
client = RTDClient()

# Get all active vehicles
vehicles = client.get_vehicle_positions()

for vehicle in vehicles[:5]:
    print(f"Vehicle {vehicle['vehicle_id']} on route {vehicle['route_id']}")
    print(f"Location: ({vehicle['latitude']}, {vehicle['longitude']})")
    if vehicle['bearing']:
        print(f"Heading: {vehicle['bearing']}°")
```

### 2. Trip Planning (Google Maps API)

```python
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY

client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)

# Get transit directions
result = client.get_transit_directions(
    origin="Union Station, Denver, CO",
    destination="Denver International Airport, CO"
)

if result and result['routes']:
    route = result['routes'][0]
    print(f"Duration: {route['duration']}")
    print(f"Departure: {route['departure_time']}")
    print(f"Arrival: {route['arrival_time']}")
    
    # Show each step
    for step in route['steps']:
        if step['travel_mode'] == 'TRANSIT':
            transit = step['transit']
            print(f"Take {transit['line_short_name']} from {transit['departure_stop']}")
```

### 3. Find Nearby Stations

```python
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY

client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)

# Find stations near a location
stations = client.find_nearby_transit_stations(
    location="Downtown Denver, CO",
    radius=1000  # meters
)

for station in stations:
    print(f"{station['name']}: {station['address']}")
```

### 4. Schedule Future Trips

```python
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY
from datetime import datetime, timedelta

client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)

# Plan a trip for 2 hours from now
future_time = datetime.now() + timedelta(hours=2)

result = client.get_transit_directions(
    origin="Coors Field, Denver, CO",
    destination="Cherry Creek Shopping Center, Denver, CO",
    departure_time=future_time
)
```

### 5. Compare Multiple Routes

```python
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY

client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)

result = client.get_transit_directions(
    origin="Union Station, Denver, CO",
    destination="Colorado State Capitol, Denver, CO",
    alternatives=True
)

if result and result['routes']:
    for i, route in enumerate(result['routes'], 1):
        print(f"Option {i}: {route['duration']} - {route['summary']}")
```

## API Reference

### RTDClient Class

#### `get_vehicle_positions()`
Get real-time positions of all active RTD vehicles.

**Returns:** List of dictionaries with:
- `vehicle_id`: Unique vehicle identifier
- `route_id`: Route the vehicle is on (e.g., "A", "15", "FREE")
- `trip_id`: Current trip identifier
- `latitude`, `longitude`: Vehicle location
- `bearing`: Direction of travel (degrees)
- `speed`: Speed in meters per second
- `timestamp`: Last update timestamp

### GoogleTransitClient Class

#### `__init__(api_key)`
Initialize the Google Maps Transit client.

**Parameters:**
- `api_key`: Your Google Maps API key

#### `get_transit_directions(origin, destination, departure_time=None, arrival_time=None, alternatives=True)`
Get transit directions between two locations.

**Parameters:**
- `origin`: Starting location (address or coordinates)
- `destination`: Ending location (address or coordinates)
- `departure_time`: Desired departure time (datetime object)
- `arrival_time`: Desired arrival time (overrides departure_time)
- `alternatives`: Return multiple route options (default: True)

**Returns:** Dictionary with:
- `routes`: List of route options
- Each route contains: steps, duration, distance, departure/arrival times

#### `find_nearby_transit_stations(location, radius=1000)`
Find transit stations near a location.

**Parameters:**
- `location`: Center location (address or coordinates)
- `radius`: Search radius in meters (default: 1000)

**Returns:** List of nearby stations with names, addresses, and coordinates.

#### `get_next_departures(from_location, to_location, num_options=3)`
Get next few departure options.

**Parameters:**
- `from_location`: Starting location
- `to_location`: Destination
- `num_options`: Number of departure times to check (default: 3)

**Returns:** List of route options at different departure times.

## Common Use Cases

### 1. Real-time Bus Tracking Dashboard

```python
from rtd_client import RTDClient

client = RTDClient()
vehicles = client.get_vehicle_positions()

# Group by route
routes = {}
for v in vehicles:
    route_id = v['route_id']
    if route_id not in routes:
        routes[route_id] = []
    routes[route_id].append(v)

# Display by route
for route_id, route_vehicles in sorted(routes.items()):
    print(f"Route {route_id}: {len(route_vehicles)} active vehicles")
```

### 2. "How Do I Get There?" App

```python
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY

def how_do_i_get_there(start, end):
    client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)
    result = client.get_transit_directions(start, end)
    
    if result and result['routes']:
        route = result['routes'][0]
        print(f"Leave at: {route['departure_time']}")
        print(f"Arrive at: {route['arrival_time']}")
        print(f"Total time: {route['duration']}")
        print("\nDirections:")
        
        for i, step in enumerate(route['steps'], 1):
            if step['travel_mode'] == 'TRANSIT':
                t = step['transit']
                print(f"{i}. Take {t['line_short_name']} ({t['headsign']})")
                print(f"   Board at: {t['departure_stop']}")
                print(f"   Get off at: {t['arrival_stop']}")
            else:
                print(f"{i}. Walk {step['distance']}")

how_do_i_get_there("Union Station", "Denver Airport")
```

### 3. Monitor Specific Route

```python
from rtd_client import RTDClient

client = RTDClient()

def track_route(route_id):
    vehicles = client.get_vehicle_positions()
    route_vehicles = [v for v in vehicles if v['route_id'] == route_id]
    
    print(f"Route {route_id} - {len(route_vehicles)} active vehicles:")
    for v in route_vehicles:
        print(f"  Vehicle at ({v['latitude']:.4f}, {v['longitude']:.4f})")
    
    return route_vehicles

# Track the A Line (airport train)
track_route("A")
```

## Data Sources & APIs

### RTD Direct APIs
- **Vehicle Positions**: `https://www.rtd-denver.com/google_sync/VehiclePosition.pb`
- Format: GTFS Realtime Protocol Buffers
- **No API key required**
- Updates: Real-time

### Google Maps APIs
- **Directions API**: Transit routing with RTD data
- **Places API**: Station search
- **Geocoding API**: Address to coordinates
- **API key required** (free tier available)
- Updates: Real-time with traffic and delays

## Project Structure

```
RTD/
├── rtd_client.py              # RTD Direct API client
├── google_transit_client.py   # Google Maps Transit API client
├── config.py                  # Your API keys (git-ignored)
├── config_example.py          # Config template
├── example.py                 # Comprehensive demo
├── example_rtd_only.py        # RTD API only demo
├── example_google_maps.py     # Google Maps API demo
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Comparison: Which API to Use?

| Feature | RTD Direct API | Google Maps API |
|---------|---------------|-----------------|
| Real-time vehicle positions | ✅ Yes | ❌ No |
| Trip planning | ❌ Limited | ✅ Comprehensive |
| Multiple route options | ❌ No | ✅ Yes |
| Walking directions | ❌ No | ✅ Yes |
| Schedule information | ❌ Unavailable | ✅ Yes |
| Service alerts | ❌ Unavailable | ✅ Yes |
| API key required | ✅ No | ⚠️ Yes (free tier) |
| Cost | 🎉 Free | 💰 Free tier + paid |

**Recommendation**: 
- Use **RTD Direct API** for real-time vehicle tracking and fleet monitoring
- Use **Google Maps API** for trip planning, directions, and user-facing applications
- Use **both together** for complete functionality!

## Troubleshooting

### RTD API Issues
- **Vehicle positions not loading**: RTD endpoints may be temporarily down
- **Other GTFS feeds unavailable**: Use Google Maps API instead

### Google Maps API Issues
- **API key not working**: Ensure you've enabled Directions, Places, and Geocoding APIs
- **Quota exceeded**: Check your usage in Google Cloud Console
- **No transit routes found**: Verify locations are within RTD service area

### General Issues
- **Import errors**: Run `pip install -r requirements.txt`
- **SSL warnings**: Your Python version may need updating (cosmetic issue, usually harmless)

## Requirements

- Python 3.7+
- requests >= 2.31.0
- gtfs-realtime-bindings >= 1.0.0
- Google Maps API key (optional, for Google Maps features)

## Free Tier Limits

### RTD Direct API
- ✅ Unlimited free access
- No registration required

### Google Maps API
- $200 free credit per month (~40,000 requests)
- Directions API: ~$5 per 1,000 requests
- Places API: ~$32 per 1,000 requests (nearby search)
- Geocoding API: ~$5 per 1,000 requests

For most personal projects, the free tier is sufficient!

## License

This project uses publicly available RTD data and Google Maps APIs. 
- RTD data: Check [RTD's terms of service](https://www.rtd-denver.com/)
- Google Maps: Follow [Google Maps Platform Terms](https://cloud.google.com/maps-platform/terms)

## Resources

- [RTD Official Website](https://www.rtd-denver.com/)
- [RTD System Map](https://www.rtd-denver.com/services/system-map)
- [Google Maps Platform](https://developers.google.com/maps)
- [GTFS Realtime Reference](https://developers.google.com/transit/gtfs-realtime)

## Contributing

Feel free to submit issues or pull requests to improve this client!

## Support

For issues with:
- **RTD data**: Visit https://www.rtd-denver.com/
- **Google Maps API**: Visit https://developers.google.com/maps/support
- **This client**: Open an issue on this repository

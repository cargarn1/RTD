# RTD Denver Transportation API Client

A comprehensive Python client and REST API for accessing RTD (Regional Transportation District) Denver's transportation data through multiple APIs:
- **RTD Direct APIs**: Real-time vehicle tracking via GTFS feeds
- **Google Maps Transit API**: Complete trip planning with RTD integration
- **REST API Server**: Custom API with authentication for integrations (Zapier, webhooks, etc.)
- **Web Frontend**: Interactive dashboard and live map visualization

## Features

### RTD Direct APIs
- 📍 **Real-time Vehicle Positions**: Track buses and trains in real-time
- 🚌 **Live Fleet Monitoring**: See all active vehicles on RTD network
- 🚏 **Closest Stop Detection**: Automatically find nearest stop to each vehicle
- 📊 **Route Statistics**: Vehicle counts and route information

### Google Maps Transit API  
- 🗺️ **Trip Planning**: Get detailed transit directions with RTD
- ⏰ **Schedule Planning**: Departure and arrival times
- 🚏 **Station Finder**: Discover nearby transit stops
- 🔀 **Multiple Routes**: Compare different route options
- 🚶‍♂️ **Walking Directions**: Integrated pedestrian navigation
- 📊 **Real-time Updates**: Live transit data including delays

### REST API Server
- 🔐 **API Key Authentication**: Secure access to your API
- 🎯 **Zapier Integration**: Ready-to-use triggers and actions
- 📡 **Webhook Support**: Perfect for automation workflows
- 🚏 **Closest Stop Info**: Includes nearest stop for each vehicle
- 📊 **Multiple Endpoints**: Vehicles, routes, directions, stations

### Web Frontend
- 🗺️ **Live Map**: Real-time vehicle positions on interactive map
- 📊 **Dashboard**: Overview of RTD transit data
- 🚏 **Route Planner**: Plan trips and find routes
- 📍 **Route Details**: Detailed information for each route

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

# Address to routes example
python3 example_address_to_routes.py
```

### Start REST API Server

```bash
# Start API server (port 8000)
python3 api_server.py

# Test the API
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8000/api/health
```

### Start Web Frontend

```bash
# Start web app (port 5000)
python3 web_app.py

# Access at http://localhost:5000
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
- `speed`: Speed in meters per second (may be null)
- `timestamp`: Last update timestamp

#### `parse_stops()`
Get all RTD stops from GTFS static feed.

**Returns:** List of dictionaries with stop information including:
- `stop_id`: Stop identifier
- `stop_name`: Stop name
- `stop_lat`, `stop_lon`: Stop coordinates

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

## REST API Server

### Quick Start

```bash
# Start the API server
python3 api_server.py
```

Server runs on `http://localhost:8000` by default.

### API Endpoints

#### Get All Vehicles
```bash
GET /api/vehicles
Headers: X-API-Key: YOUR_API_KEY
```

**Query Parameters:**
- `format=array` - Return array format (for Zapier triggers)
- `include_stops=true` - Include closest stop info (default: true)
- `route=<route_id>` - Filter by route

**Response includes:**
- Vehicle positions, routes, route counts
- Closest stop information (stop name, distance, coordinates)

#### Get Vehicles by Route
```bash
GET /api/vehicles/<route_id>
Headers: X-API-Key: YOUR_API_KEY
```

#### Get All Routes
```bash
GET /api/routes
Headers: X-API-Key: YOUR_API_KEY
```

#### Health Check
```bash
GET /api/health
# No authentication required
```

### Closest Stop Feature

Each vehicle response includes closest stop information:

```json
{
  "vehicle_id": "...",
  "latitude": 39.7539,
  "longitude": -105.0002,
  "closest_stop": {
    "stop_id": "12345",
    "stop_name": "Union Station",
    "stop_latitude": 39.7539,
    "stop_longitude": -105.0002,
    "distance_miles": 0.125,
    "distance_meters": 201.2
  }
}
```

**Disable closest stops** (for faster response):
```bash
GET /api/vehicles?include_stops=false
```

## Zapier Integration

### Setup Guide

See comprehensive guides:
- **[Zapier UI Builder Guide](ZAPIER_UI_BUILDER_GUIDE.md)** - Step-by-step integration setup
- **[Zapier Zap Examples](ZAPIER_ZAP_EXAMPLES.md)** - 12+ practical Zap examples
- **[Zapier Integration Guide](ZAPIER_INTEGRATION.md)** - General integration info

### Quick Setup

1. **Start API Server**: `python3 api_server.py` (port 8000)
2. **Expose with ngrok**: `ngrok http 8000`
3. **Create Zapier App**: Use UI Builder at https://zapier.com/app/developer
4. **Configure Authentication**: API Key type with `X-API-Key` header
5. **Create Triggers/Actions**: Use endpoints with `format=array` for triggers

### Available Triggers

- **New Vehicle in Service** - Polling trigger for new vehicles entering service
  - Uses `/api/vehicles?format=array`
  - Includes closest stop information
  - Automatically deduplicates by vehicle ID

### Available Actions

- **Get All Vehicles** - Retrieve all active vehicles
- **Get Vehicles by Route** - Get vehicles for specific route
- **Get All Routes** - List all active routes

## Web Frontend

### Start Web App

```bash
python3 web_app.py
```

Access at `http://localhost:5000`

### Features

- **Dashboard** (`/`) - Overview of RTD data
- **Live Map** (`/map`) - Real-time vehicle positions
- **Route Planner** (`/routes`) - Plan trips
- **Route Details** (`/route/<route_id>`) - Detailed route information

See [Web Frontend Guide](WEB_FRONTEND_GUIDE.md) for details.

## Project Structure

```
RTD/
├── rtd_client.py              # RTD Direct API client
├── google_transit_client.py   # Google Maps Transit API client
├── route_details.py           # Route details and stop information
├── api_server.py              # REST API server (Flask)
├── web_app.py                 # Web frontend (Flask)
├── config.py                  # Your API keys (git-ignored)
├── config_example.py          # Config template
├── example.py                 # Comprehensive demo
├── example_rtd_only.py        # RTD API only demo
├── example_google_maps.py     # Google Maps API demo
├── example_address_to_routes.py  # Address to routes example
├── generate_api_key.py        # Generate API keys for REST API
├── test_api.sh                # API testing script
├── requirements.txt           # Python dependencies
├── templates/                 # Web frontend templates
│   ├── index.html
│   ├── map.html
│   ├── routes.html
│   └── route_detail.html
├── static/                    # Web frontend assets
│   ├── css/style.css
│   └── js/main.js
├── README.md                  # This file
├── ZAPIER_UI_BUILDER_GUIDE.md # Zapier integration guide
├── ZAPIER_ZAP_EXAMPLES.md     # Zap examples
├── ZAPIER_INTEGRATION.md      # General Zapier guide
├── WEB_FRONTEND_GUIDE.md      # Web frontend guide
└── TESTING_GUIDE.md           # Testing guide
```

## Comparison: Which API to Use?

| Feature | RTD Direct API | Google Maps API | REST API Server |
|---------|---------------|-----------------|-----------------|
| Real-time vehicle positions | ✅ Yes | ❌ No | ✅ Yes (via RTD) |
| Trip planning | ❌ Limited | ✅ Comprehensive | ✅ Yes (via Google) |
| Multiple route options | ❌ No | ✅ Yes | ✅ Yes |
| Walking directions | ❌ No | ✅ Yes | ✅ Yes |
| Schedule information | ❌ Unavailable | ✅ Yes | ✅ Yes |
| Service alerts | ❌ Unavailable | ✅ Yes | ✅ Yes |
| Closest stop info | ❌ No | ❌ No | ✅ Yes |
| Zapier integration | ❌ No | ❌ No | ✅ Yes |
| Webhook support | ❌ No | ❌ No | ✅ Yes |
| API key required | ✅ No | ⚠️ Yes (free tier) | ⚠️ Yes (custom) |
| Cost | 🎉 Free | 💰 Free tier + paid | 🎉 Free (self-hosted) |

**Recommendation**: 
- Use **RTD Direct API** for real-time vehicle tracking and fleet monitoring
- Use **Google Maps API** for trip planning, directions, and user-facing applications
- Use **REST API Server** for Zapier integration, webhooks, and custom integrations
- Use **Web Frontend** for interactive visualization and user-friendly interface
- Use **all together** for complete functionality!

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
- flask >= 2.0.0 (for API server and web frontend)
- google-maps-services-python >= 4.0.0 (for Google Maps features)
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

## API Server Endpoints

### Authentication
All endpoints (except `/api/health`) require API key authentication:
- **Header**: `X-API-Key: YOUR_API_KEY`
- **Query Parameter**: `?api_key=YOUR_API_KEY`

### Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/health` | GET | ❌ No | Health check |
| `/api/vehicles` | GET | ✅ Yes | Get all vehicles |
| `/api/vehicles/<route_id>` | GET | ✅ Yes | Get vehicles by route |
| `/api/routes` | GET | ✅ Yes | Get all routes |
| `/api/directions` | GET | ✅ Yes | Get transit directions |
| `/api/stations/nearby` | GET | ✅ Yes | Find nearby stations |

### Query Parameters

**`/api/vehicles`:**
- `format=array` - Return array format (for Zapier triggers)
- `include_stops=true` - Include closest stop info (default: true)
- `route=<route_id>` - Filter by route

**Example:**
```bash
# Get vehicles with closest stops (default)
curl -H "X-API-Key: YOUR_KEY" http://localhost:8000/api/vehicles

# Get vehicles in array format for Zapier
curl -H "X-API-Key: YOUR_KEY" "http://localhost:8000/api/vehicles?format=array"

# Get vehicles without closest stops (faster)
curl -H "X-API-Key: YOUR_KEY" "http://localhost:8000/api/vehicles?include_stops=false"
```

### Response Format

**Standard format:**
```json
{
  "success": true,
  "count": 340,
  "vehicles": [...],
  "routes": ["A", "AB1", "15", ...],
  "route_counts": {"A": 8, "AB1": 3, ...}
}
```

**Array format** (`format=array`):
```json
[
  {
    "id": "vehicle_id",
    "vehicle_id": "...",
    "route_id": "A",
    "latitude": 39.7539,
    "longitude": -105.0002,
    "closest_stop": {
      "stop_name": "Union Station",
      "distance_meters": 201.2
    }
  }
]
```

## Documentation

- **[Zapier UI Builder Guide](ZAPIER_UI_BUILDER_GUIDE.md)** - Complete Zapier integration setup
- **[Zapier Zap Examples](ZAPIER_ZAP_EXAMPLES.md)** - 12+ practical Zap examples
- **[Zapier Integration Guide](ZAPIER_INTEGRATION.md)** - General Zapier integration info
- **[Web Frontend Guide](WEB_FRONTEND_GUIDE.md)** - Web app setup and usage
- **[Testing Guide](TESTING_GUIDE.md)** - How to test all components
- **[API Key Guide](API_KEY_GUIDE.md)** - API key management

## Resources

- [RTD Official Website](https://www.rtd-denver.com/)
- [RTD System Map](https://www.rtd-denver.com/services/system-map)
- [Google Maps Platform](https://developers.google.com/maps)
- [GTFS Realtime Reference](https://developers.google.com/transit/gtfs-realtime)
- [Zapier Platform Docs](https://platform.zapier.com/docs)

## Contributing

Feel free to submit issues or pull requests to improve this client!

## Support

For issues with:
- **RTD data**: Visit https://www.rtd-denver.com/
- **Google Maps API**: Visit https://developers.google.com/maps/support
- **This client**: Open an issue on this repository

# How to Get Routes from an Address

Complete guide to finding RTD transit routes from any address.

## 🎯 Quick Answer

You can get routes from an address in **3 ways**:

1. **Python Script** (Easiest) - Interactive
2. **Python Code** - For your own apps
3. **REST API** - For Zapier, web apps, etc.

---

## ✨ Method 1: Interactive Python Script (Easiest!)

### Option A: Interactive Mode

```bash
python3 get_routes.py
```

The script will ask you:
```
📍 Starting address: 1500 Wynkoop St, Denver
📍 Destination address: Denver Airport
```

And show you all available routes! 🚌

### Option B: Command Line

```bash
python3 get_routes.py "1500 Wynkoop St, Denver" "Denver Airport"
```

### Option C: Use Common Locations

```bash
python3 get_routes.py union_station airport
```

Available shortcuts:
- `union_station` - Union Station
- `capitol` - Colorado State Capitol
- `airport` - Denver International Airport
- `coors_field` - Coors Field
- `cherry_creek` - Cherry Creek Shopping Center
- `downtown` - Downtown Denver
- `16th_street_mall` - 16th Street Mall

---

## 💻 Method 2: Use Python Code in Your App

### Basic Example

```python
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY

# Initialize client
client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)

# Get routes from an address
result = client.get_transit_directions(
    origin="1500 Wynkoop St, Denver, CO",
    destination="Denver International Airport"
)

# Display results
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

### Get Multiple Route Options

```python
# Get alternative routes
result = client.get_transit_directions(
    origin="Your Address",
    destination="Destination Address",
    alternatives=True  # Returns multiple options
)

# Show all options
for i, route in enumerate(result['routes'], 1):
    print(f"Option {i}: {route['duration']} - {route['summary']}")
```

### Schedule for Later

```python
from datetime import datetime, timedelta

# Plan a trip for 2 hours from now
departure_time = datetime.now() + timedelta(hours=2)

result = client.get_transit_directions(
    origin="Your Address",
    destination="Destination",
    departure_time=departure_time
)
```

### Arrive by Specific Time

```python
from datetime import datetime

# Need to arrive by 3 PM
arrival_time = datetime.now().replace(hour=15, minute=0)

result = client.get_transit_directions(
    origin="Your Address",
    destination="Destination",
    arrival_time=arrival_time
)
```

---

## 🌐 Method 3: Use REST API (For Zapier, Web Apps)

### Step 1: Start Your API Server

```bash
python3 api_server.py
```

### Step 2: Make API Request

#### Using curl:

```bash
curl -H "X-API-Key: your-api-key" \
  "http://localhost:5000/api/directions?origin=1500%20Wynkoop%20St&destination=Denver%20Airport"
```

#### Using JavaScript (fetch):

```javascript
fetch('http://localhost:5000/api/directions?' + new URLSearchParams({
    origin: '1500 Wynkoop St, Denver',
    destination: 'Denver Airport'
}), {
    headers: {
        'X-API-Key': 'your-api-key'
    }
})
.then(response => response.json())
.then(data => {
    console.log(`Duration: ${data.routes[0].duration}`);
    console.log(`Depart: ${data.routes[0].departure_time}`);
});
```

#### Using Python (requests):

```python
import requests

response = requests.get(
    'http://localhost:5000/api/directions',
    params={
        'origin': '1500 Wynkoop St, Denver',
        'destination': 'Denver Airport'
    },
    headers={'X-API-Key': 'your-api-key'}
)

data = response.json()
if data['success']:
    route = data['routes'][0]
    print(f"Duration: {route['duration']}")
```

---

## 📋 Understanding the Response

### What You Get Back

```json
{
  "success": true,
  "origin": "1500 Wynkoop St, Denver",
  "destination": "Denver Airport",
  "routes": [
    {
      "duration": "37 mins",
      "distance": "23.4 miles",
      "departure_time": "2:30 PM",
      "arrival_time": "3:07 PM",
      "summary": "via A Line",
      "start_address": "1500 Wynkoop St, Denver, CO 80202",
      "end_address": "Denver International Airport, CO",
      "steps": [
        {
          "travel_mode": "WALKING",
          "duration": "5 mins",
          "distance": "0.3 miles",
          "instructions": "Walk to Union Station"
        },
        {
          "travel_mode": "TRANSIT",
          "duration": "37 mins",
          "distance": "23.1 miles",
          "transit": {
            "line": "A Line",
            "line_short_name": "A",
            "vehicle_type": "HEAVY_RAIL",
            "departure_stop": "Union Station",
            "arrival_stop": "Denver Airport Station",
            "departure_time": "2:35 PM",
            "arrival_time": "3:12 PM",
            "num_stops": 8,
            "headsign": "Airport"
          }
        }
      ]
    }
  ]
}
```

### Key Fields Explained

| Field | Description | Example |
|-------|-------------|---------|
| `duration` | Total trip time | "37 mins" |
| `distance` | Total distance | "23.4 miles" |
| `departure_time` | When to leave | "2:30 PM" |
| `arrival_time` | When you arrive | "3:07 PM" |
| `summary` | Route description | "via A Line" |
| `steps` | Step-by-step directions | Array of steps |

---

## 🎓 Complete Examples

### Example 1: Home to Work Commute

```python
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY

client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)

# Get directions to work
result = client.get_transit_directions(
    origin="123 Main St, Denver, CO",
    destination="1234 Work Ave, Denver, CO"
)

if result and result['routes']:
    route = result['routes'][0]
    print(f"🏠 → 🏢 Your commute:")
    print(f"   Duration: {route['duration']}")
    print(f"   Leave at: {route['departure_time']}")
    print(f"   Arrive by: {route['arrival_time']}")
```

### Example 2: Compare Multiple Routes

```python
# Get all available route options
result = client.get_transit_directions(
    origin="Your Address",
    destination="Destination",
    alternatives=True
)

print("Available routes:")
for i, route in enumerate(result['routes'], 1):
    print(f"\nOption {i}:")
    print(f"  Time: {route['duration']}")
    print(f"  Distance: {route['distance']}")
    
    # Count transfers
    transfers = sum(1 for step in route['steps'] if step['travel_mode'] == 'TRANSIT') - 1
    print(f"  Transfers: {transfers}")
```

### Example 3: Next 3 Departure Times

```python
from datetime import datetime, timedelta

# Check next 3 departure times
now = datetime.now()

for i in range(3):
    departure = now + timedelta(minutes=i * 15)
    
    result = client.get_transit_directions(
        origin="Your Address",
        destination="Destination",
        departure_time=departure,
        alternatives=False
    )
    
    if result and result['routes']:
        route = result['routes'][0]
        print(f"\nOption {i+1} - Leave at {departure.strftime('%I:%M %p')}:")
        print(f"  Arrive: {route['arrival_time']}")
        print(f"  Duration: {route['duration']}")
```

### Example 4: Find Nearby Stations First

```python
# First, find stations near your address
stations = client.find_nearby_transit_stations(
    location="Your Address",
    radius=500  # meters
)

print(f"Found {len(stations)} stations near you:")
for station in stations[:3]:
    print(f"  • {station['name']} - {station['address']}")

# Then get routes from nearest station
if stations:
    nearest = stations[0]
    result = client.get_transit_directions(
        origin=nearest['name'],
        destination="Your Destination"
    )
```

---

## 🔧 Configuration Required

### Prerequisites

1. **Google Maps API Key** (required for address-based routing)

```bash
# Get a key at: https://console.cloud.google.com/
# Add to config.py:
GOOGLE_MAPS_API_KEY = 'your-key-here'
```

2. **Required APIs** (enable in Google Cloud Console):
   - ✅ Directions API
   - ✅ Geocoding API
   - ✅ Places API (for station search)

### Check Configuration

```python
from config import validate_google_api_key

if validate_google_api_key():
    print("✅ Ready to use!")
else:
    print("⚠️ Configure your API key first")
```

---

## 🎯 Common Use Cases

### Use Case 1: "How do I get there?"

```bash
python3 get_routes.py "My Address" "Destination"
```

### Use Case 2: "When should I leave to arrive by 3 PM?"

```python
arrival_time = datetime.now().replace(hour=15, minute=0)
result = client.get_transit_directions(
    origin="Your Address",
    destination="Destination",
    arrival_time=arrival_time
)
```

### Use Case 3: "What are my options?"

```python
result = client.get_transit_directions(
    origin="Your Address",
    destination="Destination",
    alternatives=True  # Get all options
)
print(f"You have {len(result['routes'])} route options")
```

### Use Case 4: "Where's the nearest station?"

```python
stations = client.find_nearby_transit_stations(
    location="Your Address",
    radius=1000
)
print(f"Nearest: {stations[0]['name']}")
```

---

## 🆘 Troubleshooting

### "No routes found"

**Possible causes:**
- Addresses outside RTD service area
- No transit service available at that time
- Addresses not recognized

**Solutions:**
- Try more specific addresses (include "Denver, CO")
- Check if location is in RTD service area
- Try using landmarks instead

### "API key not configured"

```bash
# Add your key to config.py
GOOGLE_MAPS_API_KEY = 'AIzaSy...'
```

### "Invalid address"

Use complete addresses:
- ✅ "1500 Wynkoop St, Denver, CO"
- ❌ "Wynkoop St"

---

## 💰 Cost

**Google Maps API:**
- Directions API: ~$5 per 1,000 requests
- Geocoding API: ~$5 per 1,000 requests
- **Free tier**: $200/month credit
- **Typical use**: $0-5/month

---

## 📚 Additional Resources

- **Test it**: `python3 get_routes.py`
- **More examples**: `example_google_maps.py`
- **API Reference**: `README.md`
- **Quick Reference**: `QUICK_REFERENCE.md`

---

## ✅ Quick Checklist

- [ ] Configure Google Maps API key in `config.py`
- [ ] Test with: `python3 get_routes.py`
- [ ] Try your home address
- [ ] Compare multiple routes
- [ ] Schedule future trips
- [ ] Find nearby stations

---

**Ready to try it?** Run:

```bash
python3 get_routes.py
```

And enter any Denver address! 🚌


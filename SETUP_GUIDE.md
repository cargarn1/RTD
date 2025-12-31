# RTD API Client - Quick Setup Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Verify Installation

Dependencies are already installed! Verify with:

```bash
python3 -c "import requests; import google.transit.gtfs_realtime_pb2; print('✅ All dependencies installed!')"
```

### Step 2: Test RTD Direct API (No API Key Needed)

Run the RTD-only example to see real-time vehicle tracking:

```bash
cd /Users/carlosgarcia/Documents/Code/RTD
python3 example_rtd_only.py
```

You should see real-time locations of RTD buses and trains! 🚌

### Step 3: Setup Google Maps API (Optional but Recommended)

To enable trip planning and full features:

#### 3.1: Get Your Free API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/google/maps-apis)
2. Create a new project (or select existing)
3. Click "Enable APIs and Services"
4. Enable these three APIs:
   - **Directions API**
   - **Places API** 
   - **Geocoding API**
5. Go to "Credentials" and create an API key
6. Copy your API key

#### 3.2: Configure Your API Key

Edit the `config.py` file:

```bash
# Open config.py in your editor
nano config.py
# or
code config.py
```

Replace `YOUR_GOOGLE_MAPS_API_KEY_HERE` with your actual key:

```python
GOOGLE_MAPS_API_KEY = 'AIzaSyD...'  # Your actual key
```

#### 3.3: Test Google Maps Integration

```bash
python3 example_google_maps.py
```

You should see detailed trip planning and directions! 🗺️

### Step 4: Run the Full Demo

```bash
python3 example.py
```

This shows everything working together!

## 📝 Quick Usage Examples

### Track Buses in Real-Time

```python
from rtd_client import RTDClient

client = RTDClient()
vehicles = client.get_vehicle_positions()

print(f"Found {len(vehicles)} active vehicles")
for v in vehicles[:3]:
    print(f"Route {v['route_id']}: ({v['latitude']}, {v['longitude']})")
```

### Get Trip Directions

```python
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY

client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)
result = client.get_transit_directions(
    "Union Station, Denver",
    "Denver Airport"
)

route = result['routes'][0]
print(f"Duration: {route['duration']}")
print(f"Depart: {route['departure_time']}")
```

## 🎯 What Can You Build?

Ideas to get started:

1. **Real-time Bus Tracker**: Map showing all RTD vehicles
2. **Trip Planner**: Web app for transit directions
3. **Commute Timer**: Check your commute time before leaving
4. **Station Finder**: Find nearest RTD stops
5. **Route Monitor**: Track specific bus/train routes
6. **Delay Alerts**: Get notified of transit delays

## 💰 Cost Estimate

- **RTD Direct API**: 100% Free, unlimited
- **Google Maps API**: 
  - First $200/month: FREE
  - Typical personal use: ~$0-5/month
  - 1,000 trip requests: ~$5

For most projects, you'll stay within the free tier!

## 🆘 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Google Maps API not working
- Check that you enabled all 3 APIs (Directions, Places, Geocoding)
- Verify API key is copied correctly in `config.py`
- Make sure there are no extra spaces around the key

### RTD vehicles not loading
- This is normal if RTD's server is down temporarily
- The Google Maps API still works independently

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the example files for more use cases
- Start building your own transit app!

## 🎉 You're Ready!

Your RTD API client is fully configured and ready to use. Start exploring Denver's transit system programmatically!


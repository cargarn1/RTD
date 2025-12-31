# Testing Guide

Quick guide to test all features of your RTD application.

## ✅ Test Results Summary

**Currently Working:**
- ✅ RTD Vehicle Tracking - **224 active vehicles found!**
- ✅ API Server - Ready to use
- ⚠️ Google Maps - Not configured (optional)

## 🧪 How to Test

### Option 1: Run Comprehensive Tests (Recommended)

```bash
python3 test_all.py
```

This tests everything and gives you a detailed report!

### Option 2: Quick One-Liner Tests

```bash
# Test RTD vehicle tracking
python3 -c "from rtd_client import RTDClient; print(f'Found {len(RTDClient().get_vehicle_positions())} vehicles')"

# Test API server imports
python3 -c "import api_server; print('API server OK')"

# Generate API key
python3 generate_api_key.py
```

### Option 3: Run Individual Examples

```bash
# RTD vehicle tracking (working now!)
python3 example_rtd_only.py

# Complete demo (includes Google Maps if configured)
python3 example.py

# Google Maps only (requires API key)
python3 example_google_maps.py
```

## 🚀 Test the API Server

### Step 1: Start the Server

```bash
python3 api_server.py
```

You should see:
```
🚀 RTD API Server Starting
📋 Configuration:
   RTD Direct API: ✅ Available
🔑 API Keys:
   Default key: demo-key-change-in-production
```

### Step 2: Test with curl (in another terminal)

```bash
# Health check (no auth needed)
curl http://localhost:5000/api/health

# Get vehicles (needs API key)
curl -H "X-API-Key: demo-key-change-in-production" \
     http://localhost:5000/api/vehicles

# Get vehicles for specific route
curl -H "X-API-Key: demo-key-change-in-production" \
     http://localhost:5000/api/vehicles/A
```

### Step 3: Use the Test Script

```bash
./test_api.sh demo-key-change-in-production
```

## 🌐 Test with Your Browser

With the API server running, visit:

- http://localhost:5000/ - API documentation
- http://localhost:5000/api/health - Health check

## 📊 What Should You See?

### Successful RTD Vehicle Test
```json
{
  "success": true,
  "count": 224,
  "vehicles": [
    {
      "vehicle_id": "46EB8ED6CB7DDF73E063DD4D1FACD7C6",
      "route_id": "AT",
      "latitude": 39.771766,
      "longitude": -104.817214,
      "bearing": 276.0
    }
  ]
}
```

### API Health Check
```json
{
  "status": "healthy",
  "rtd_api": "available",
  "google_maps_api": "not configured"
}
```

## 🔑 Test API Key Generation

```bash
python3 generate_api_key.py
```

Output:
```
🔑 RTD API Key Generator
================================================================================
Generated API Keys (store these securely!):

1. yZacCQMKJSoAX8gskkimCkwL83ZRIzMa89vZ37twYc0
2. 2xKXhEw6Bu8dtlCmlabqkh40XzOzoC3y0aRb8XXc128
3. zkvT_iJtlyF6tJCBxGL8zXEbJcEhaEoQNbAB5napMeU
```

## 🧩 Test Individual Components

### Test 1: RTD Client

```python
# Create a file: test_rtd.py
from rtd_client import RTDClient

client = RTDClient()
vehicles = client.get_vehicle_positions()

if vehicles:
    print(f"✅ Found {len(vehicles)} vehicles")
    print(f"Sample: Route {vehicles[0]['route_id']}")
else:
    print("❌ No vehicles found")
```

Run it:
```bash
python3 test_rtd.py
```

### Test 2: Google Maps Client (Optional)

```python
# Create a file: test_google.py
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY

if GOOGLE_MAPS_API_KEY != 'YOUR_GOOGLE_MAPS_API_KEY_HERE':
    client = GoogleTransitClient(GOOGLE_MAPS_API_KEY)
    result = client.get_transit_directions(
        "Union Station, Denver",
        "Denver Airport"
    )
    if result:
        print(f"✅ Route found: {result['routes'][0]['duration']}")
else:
    print("⚠️ Google Maps API key not configured")
```

## 🐛 Troubleshooting Tests

### "Module not found" Error

```bash
pip install -r requirements.txt
```

### "Connection refused" Error

Make sure the server is running:
```bash
python3 api_server.py
```

### "401 Unauthorized" Error

Check your API key:
```bash
curl -H "X-API-Key: demo-key-change-in-production" \
     http://localhost:5000/api/vehicles
```

### RTD Returns Empty Data

This is normal if RTD's API is temporarily down. Try again in a few minutes.

### Google Maps Tests Fail

You need to configure your API key in `config.py`:
```python
GOOGLE_MAPS_API_KEY = 'your-actual-key-here'
```

## 📈 Performance Tests

### Test Response Time

```bash
time curl -H "X-API-Key: demo-key-change-in-production" \
          http://localhost:5000/api/vehicles
```

Typical response time: 0.5-2 seconds

### Test Multiple Requests

```bash
for i in {1..10}; do
  curl -s -H "X-API-Key: demo-key-change-in-production" \
       http://localhost:5000/api/vehicles | grep -o '"count":[0-9]*'
  sleep 1
done
```

## ✅ Test Checklist

Complete this checklist to verify everything works:

- [ ] Run `python3 test_all.py` - passes core tests
- [ ] Run `python3 example_rtd_only.py` - shows vehicles
- [ ] Run `python3 generate_api_key.py` - generates keys
- [ ] Start `python3 api_server.py` - server starts
- [ ] Test `curl http://localhost:5000/api/health` - returns healthy
- [ ] Test with API key - returns vehicle data
- [ ] (Optional) Configure Google Maps API key
- [ ] (Optional) Test Google Maps features

## 🎯 Next Steps After Testing

Once all tests pass:

1. **For Development:**
   - Keep using locally
   - No further setup needed!

2. **For Zapier:**
   - Generate production API key
   - Use ngrok for testing: `ngrok http 5000`
   - Configure webhook in Zapier

3. **For Production:**
   - Deploy to cloud (Heroku, DigitalOcean, etc.)
   - Use environment variables for keys
   - Set up monitoring

## 📚 More Information

- **Quick Reference**: QUICK_REFERENCE.md
- **Setup Guide**: SETUP_GUIDE.md
- **Zapier Integration**: ZAPIER_INTEGRATION.md
- **Full Documentation**: README.md

## 🎉 Success Criteria

Your application is working if:
- ✅ `test_all.py` shows "RTD Vehicle Tracking" passed
- ✅ You can see real-time vehicle data
- ✅ API server starts without errors
- ✅ You can generate API keys

**You're ready to go!** 🚀


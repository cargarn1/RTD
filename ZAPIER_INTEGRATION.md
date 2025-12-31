# Zapier Integration Guide

Complete guide to integrating RTD transit data with Zapier.

## 🎯 Overview

This guide shows you how to:
1. Generate API keys for your service
2. Start your own RTD API server
3. Connect it to Zapier
4. Build automated workflows with RTD data

## 📝 Quick Start (5 Minutes)

### Step 1: Generate an API Key

```bash
python3 generate_api_key.py
```

Copy one of the generated keys. Example: `xK3mP9qR8vL2nF5wB7cZ1aY4tH6jN0sD2eM8gU5v`

### Step 2: Start Your API Server

```bash
# Using default demo key
python3 api_server.py

# Or with your custom key
RTD_API_KEY='your-key-here' python3 api_server.py
```

Server will start at `http://localhost:5000`

### Step 3: Test Your API

```bash
# Test with the included script
./test_api.sh your-api-key-here

# Or manually
curl -H "X-API-Key: your-key-here" http://localhost:5000/api/vehicles
```

### Step 4: Make It Public (for Zapier)

```bash
# Install ngrok
brew install ngrok

# In another terminal, expose your server
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)

### Step 5: Connect to Zapier

1. In Zapier, create a new Zap
2. Add trigger (e.g., "Schedule by Zapier" - every hour)
3. Add action: "Webhooks by Zapier"
   - Event: GET
   - URL: `https://abc123.ngrok.io/api/vehicles`
   - Headers:
     - Key: `X-API-Key`
     - Value: `your-key-here`
4. Test it - you should see RTD vehicle data!

---

## 🔧 Available API Endpoints

### 1. Get All Vehicles

**Endpoint**: `GET /api/vehicles`

**Authentication**: Required (API Key)

**Example**:
```bash
curl -H "X-API-Key: YOUR_KEY" \
     http://localhost:5000/api/vehicles
```

**Response**:
```json
{
  "success": true,
  "count": 233,
  "vehicles": [
    {
      "vehicle_id": "46EB8ED6CB7DDF73E063DD4D1FACD7C6",
      "route_id": "AT",
      "latitude": 39.771766,
      "longitude": -104.817214,
      "bearing": 276.0,
      "timestamp": 1704067200
    }
  ]
}
```

**Use in Zapier**: Get real-time locations of all RTD vehicles

---

### 2. Get Vehicles by Route

**Endpoint**: `GET /api/vehicles/<route_id>`

**Example**:
```bash
curl -H "X-API-Key: YOUR_KEY" \
     http://localhost:5000/api/vehicles/A
```

**Response**:
```json
{
  "success": true,
  "route": "A",
  "count": 5,
  "vehicles": [...]
}
```

**Use in Zapier**: Track specific routes (e.g., A Line to airport)

---

### 3. Get Transit Directions

**Endpoint**: `GET /api/directions`

**Parameters**:
- `origin` (required): Starting location
- `destination` (required): Ending location

**Example**:
```bash
curl -H "X-API-Key: YOUR_KEY" \
     "http://localhost:5000/api/directions?origin=Union%20Station&destination=Denver%20Airport"
```

**Response**:
```json
{
  "success": true,
  "origin": "Union Station",
  "destination": "Denver Airport",
  "routes": [{
    "duration": "37 mins",
    "distance": "23.4 miles",
    "departure_time": "2:30 PM",
    "arrival_time": "3:07 PM",
    "steps": [...]
  }]
}
```

**Use in Zapier**: Calculate trip times, send directions to users

---

### 4. Find Nearby Stations

**Endpoint**: `GET /api/stations/nearby`

**Parameters**:
- `location` (required): Address or location
- `radius` (optional): Search radius in meters (default: 1000)

**Example**:
```bash
curl -H "X-API-Key: YOUR_KEY" \
     "http://localhost:5000/api/stations/nearby?location=Downtown%20Denver"
```

**Response**:
```json
{
  "success": true,
  "location": "Downtown Denver",
  "count": 8,
  "stations": [
    {
      "name": "Union Station",
      "address": "1701 Wynkoop St",
      "location": {"lat": 39.7539, "lng": -105.0002}
    }
  ]
}
```

**Use in Zapier**: Help users find nearby transit

---

## 💡 Zapier Workflow Examples

### Example 1: Daily Transit Report

**Trigger**: Schedule by Zapier (daily at 7 AM)

**Actions**:
1. Webhooks: GET `/api/vehicles`
2. Filter: Count vehicles per route
3. Gmail: Send email with daily stats

**Use Case**: Get a daily report of RTD service

---

### Example 2: Route Delay Alert

**Trigger**: Schedule by Zapier (every 15 minutes)

**Actions**:
1. Webhooks: GET `/api/vehicles/A`
2. Code: Check if count < 3 (fewer trains than normal)
3. SMS by Zapier: Send alert if service is reduced

**Use Case**: Get notified of potential delays

---

### Example 3: Trip Planner Bot

**Trigger**: Gmail (when email received with "RTD directions")

**Actions**:
1. Extract origin/destination from email
2. Webhooks: GET `/api/directions`
3. Gmail: Reply with directions

**Use Case**: Email yourself for instant directions

---

### Example 4: Log Vehicle Positions

**Trigger**: Schedule by Zapier (every 5 minutes)

**Actions**:
1. Webhooks: GET `/api/vehicles`
2. Google Sheets: Add row with timestamp and data

**Use Case**: Build a dataset of RTD vehicle movements

---

## 🌐 Production Deployment

For production use, deploy your API server to a cloud platform:

### Option 1: Heroku (Easiest)

```bash
# Install Heroku CLI
brew install heroku

# Login
heroku login

# Create app
heroku create rtd-api

# Set config
heroku config:set RTD_API_KEY=your-key-here
heroku config:set GOOGLE_MAPS_API_KEY=your-google-key

# Deploy
git add .
git commit -m "Deploy RTD API"
git push heroku main

# Your API is now at: https://rtd-api.herokuapp.com
```

### Option 2: DigitalOcean App Platform

1. Connect your GitHub repo
2. Create new app
3. Set environment variables
4. Deploy!

### Option 3: AWS Lambda + API Gateway

Use the Serverless framework or AWS SAM.

---

## 🔐 Security Best Practices

### 1. Use Environment Variables

```bash
# .env file
RTD_API_KEY=your-secret-key-here
GOOGLE_MAPS_API_KEY=your-google-key
ADMIN_SECRET=super-secret-admin-key
```

### 2. Rate Limiting

Add rate limiting to prevent abuse:

```python
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["100 per hour"])

@app.route('/api/vehicles')
@limiter.limit("30 per minute")
@require_api_key
def get_vehicles():
    ...
```

### 3. HTTPS Only

Always use HTTPS in production:
- Heroku/DigitalOcean provide this automatically
- For custom servers, use Let's Encrypt

### 4. API Key Rotation

Regenerate keys periodically:
```bash
python3 generate_api_key.py
```

---

## 📊 Monitoring & Logs

### View Logs

```bash
# Heroku
heroku logs --tail

# Local
# Logs print to console
```

### Monitor Usage

Add logging to track API usage:

```python
import logging

@app.route('/api/vehicles')
@require_api_key
def get_vehicles():
    logging.info(f"Request from {request.headers.get('User-Agent')}")
    ...
```

---

## 🆘 Troubleshooting

### Zapier Can't Connect

**Problem**: "Connection failed"

**Solutions**:
- Check that your server is running
- Verify ngrok tunnel is active
- Test URL manually with curl
- Check API key is correct

### "401 Unauthorized"

**Problem**: API key not working

**Solutions**:
- Verify X-API-Key header is set
- Check for typos in the key
- Ensure key is in API_KEYS dictionary

### "503 Service Unavailable"

**Problem**: RTD data not available

**Solutions**:
- RTD's API might be down (temporary)
- Google Maps API might not be configured
- Check your Google API quota

### Rate Limits

**Problem**: "429 Too Many Requests"

**Solutions**:
- Reduce Zapier trigger frequency
- Implement caching
- Upgrade your plan

---

## 💰 Cost Estimates

### Your API Server
- **Development**: Free (localhost/ngrok)
- **Production**: 
  - Heroku: $7/month (Hobby tier)
  - DigitalOcean: $5/month (Basic)
  - AWS Lambda: ~$0-5/month (free tier)

### Google Maps API
- First $200/month: **FREE**
- Typical usage: $0-10/month

### Zapier
- Free tier: 100 tasks/month
- Starter: $19.99/month (750 tasks)

**Total for small project**: $0-15/month

---

## 🎓 Advanced Usage

### Custom Zapier App

Build a proper Zapier integration:

1. Go to [Zapier Platform](https://zapier.com/app/developer)
2. Create new app
3. Configure:
   - Authentication: API Key
   - Triggers: "New Vehicle Position"
   - Actions: "Get Directions"
4. Publish to Zapier App Directory

### Webhooks for Real-time Updates

Set up webhooks to push data to Zapier:

```python
@app.route('/api/webhook/subscribe', methods=['POST'])
def subscribe_webhook():
    webhook_url = request.json.get('webhook_url')
    # Store webhook URL
    # Send updates when new data arrives
```

---

## 📚 Additional Resources

- [API Server Documentation](api_server.py)
- [API Key Guide](API_KEY_GUIDE.md)
- [Setup Guide](SETUP_GUIDE.md)
- [Main README](README.md)
- [Zapier Documentation](https://zapier.com/help)

---

## ✅ Checklist

- [ ] Generate API key: `python3 generate_api_key.py`
- [ ] Start server: `python3 api_server.py`
- [ ] Test locally: `./test_api.sh your-key`
- [ ] Expose with ngrok: `ngrok http 5000`
- [ ] Create Zap with Webhooks
- [ ] Test Zap with real data
- [ ] Deploy to production
- [ ] Set up monitoring
- [ ] Configure rate limits
- [ ] Document for your team

---

## 🎉 You're Ready!

Your RTD API is now ready for Zapier integration! Start building powerful automation workflows with Denver transit data.

**Questions?** Check the troubleshooting section or the API_KEY_GUIDE.md for more details.


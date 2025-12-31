# RTD API - Quick Reference

One-page reference for common tasks.

## 🚀 Quick Commands

### Generate API Key
```bash
python3 generate_api_key.py
```

### Start API Server
```bash
python3 api_server.py
```

### Test API
```bash
./test_api.sh your-api-key
```

### Expose to Internet (for Zapier)
```bash
ngrok http 5000
```

---

## 🔑 API Keys You Need

| API Key | Purpose | Where to Get | Required? |
|---------|---------|--------------|-----------|
| **Your Custom Key** | Secure YOUR API | `generate_api_key.py` | ✅ Yes (for Zapier) |
| **Google Maps Key** | Get transit data | [Google Cloud](https://console.cloud.google.com/) | ⚠️ Optional |
| **RTD Key** | RTD's data | Not needed | ❌ Public |

---

## 📡 API Endpoints

### Get All Vehicles
```bash
curl -H "X-API-Key: KEY" http://localhost:5000/api/vehicles
```

### Get Vehicles by Route
```bash
curl -H "X-API-Key: KEY" http://localhost:5000/api/vehicles/A
```

### Get Directions
```bash
curl -H "X-API-Key: KEY" \
  "http://localhost:5000/api/directions?origin=Union%20Station&destination=Airport"
```

### Find Nearby Stations
```bash
curl -H "X-API-Key: KEY" \
  "http://localhost:5000/api/stations/nearby?location=Downtown%20Denver"
```

---

## 🔗 Zapier Setup (3 Steps)

### 1. Start & Expose Your API
```bash
# Terminal 1
python3 api_server.py

# Terminal 2
ngrok http 5000
# Copy the https URL (e.g., https://abc123.ngrok.io)
```

### 2. Create Zap
- **Trigger**: Schedule by Zapier (every hour)
- **Action**: Webhooks by Zapier
  - Method: GET
  - URL: `https://abc123.ngrok.io/api/vehicles`
  - Headers: 
    - `X-API-Key`: `your-generated-key`

### 3. Use the Data
- Send to Google Sheets
- Post to Slack
- Email yourself
- Store in database

---

## 📁 Project Files

### Core API Clients
- `rtd_client.py` - RTD Direct API
- `google_transit_client.py` - Google Maps API
- `api_server.py` - Your REST API server

### Configuration
- `config.py` - Your API keys (git-ignored)
- `config_example.py` - Template

### Examples
- `example.py` - Complete demo
- `example_rtd_only.py` - RTD Direct only
- `example_google_maps.py` - Google Maps only

### Tools
- `generate_api_key.py` - Generate secure keys
- `test_api.sh` - Test your API

### Documentation
- `README.md` - Full documentation
- `API_KEY_GUIDE.md` - Everything about API keys
- `ZAPIER_INTEGRATION.md` - Zapier guide
- `SETUP_GUIDE.md` - Quick setup
- `QUICK_REFERENCE.md` - This file

---

## 🐛 Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "401 Unauthorized"
- Check X-API-Key header
- Verify key in api_server.py

### "Connection refused"
- Is server running? `python3 api_server.py`
- Is ngrok running? `ngrok http 5000`

### "503 Service Unavailable"
- RTD API might be down
- Check Google Maps API key in config.py

---

## 💡 Usage Examples

### Python
```python
from rtd_client import RTDClient

client = RTDClient()
vehicles = client.get_vehicle_positions()
print(f"Found {len(vehicles)} vehicles")
```

### Curl
```bash
curl -H "X-API-Key: YOUR_KEY" \
     http://localhost:5000/api/vehicles
```

### JavaScript
```javascript
fetch('http://localhost:5000/api/vehicles', {
  headers: {'X-API-Key': 'YOUR_KEY'}
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 📊 What Can You Build?

- ✅ Real-time bus tracker map
- ✅ Trip planner web app
- ✅ Commute time checker
- ✅ Delay notification system
- ✅ Transit data analytics
- ✅ Zapier automations
- ✅ Mobile app backend
- ✅ Slack bot for transit info

---

## 🎯 Next Steps

1. **Basic**: Run examples to see it work
   ```bash
   python3 example.py
   ```

2. **API**: Start your server for Zapier
   ```bash
   python3 generate_api_key.py
   python3 api_server.py
   ```

3. **Deploy**: Push to production
   - Heroku, DigitalOcean, AWS, etc.

4. **Automate**: Build Zaps!
   - See ZAPIER_INTEGRATION.md

---

## 📚 Learn More

- **Getting Started**: SETUP_GUIDE.md
- **Full Docs**: README.md
- **API Keys**: API_KEY_GUIDE.md
- **Zapier**: ZAPIER_INTEGRATION.md

---

## ⚡ One-Liner Examples

```bash
# Generate key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Get all vehicles (no auth needed)
python3 -c "from rtd_client import RTDClient; print(len(RTDClient().get_vehicle_positions()))"

# Start everything
python3 api_server.py & ngrok http 5000
```

---

**Need help?** Check the full docs or the troubleshooting sections in each guide!


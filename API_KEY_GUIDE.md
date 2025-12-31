# API Key Guide for Zapier Integration

This guide covers everything about API keys for your RTD application.

## 🎯 What You're Trying to Do

There are **two different types of API keys** involved:

### 1. **Consuming APIs** (Getting data FROM others)
- **Google Maps API Key**: You need this to get transit data from Google
- **RTD API**: No key needed - it's public!

### 2. **Creating Your Own API** (Providing data TO Zapier)
- **Your Custom API Key**: You generate these to secure YOUR endpoints
- Zapier uses YOUR key to access YOUR API server

---

## 🔑 Part 1: Getting API Keys to Use External Services

### Google Maps API Key

**Purpose**: Your app uses this to call Google Maps APIs

**How to Get It:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Click "APIs & Services" → "Library"
4. Enable these APIs:
   - Directions API
   - Places API
   - Geocoding API
5. Go to "Credentials" → "Create Credentials" → "API Key"
6. **Copy your key** (looks like: `AIzaSyD...`)
7. Add to `config.py`:
   ```python
   GOOGLE_MAPS_API_KEY = 'AIzaSyD...'
   ```

**Cost**: Free tier ($200/month credit)

---

## 🏗️ Part 2: Creating YOUR Own API for Zapier

### Why You Need This

Zapier needs to call **YOUR** server to get RTD data. You need to:
1. Run a web server (API)
2. Generate API keys to secure it
3. Give those keys to Zapier

### Step 1: Generate Your API Key

**Method A - Quick (For Testing):**

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Example output: `xK3mP9qR8vL2nF5wB7cZ1aY4tH6jN0sD2eM8gU5v`

**Method B - Programmatic:**

```python
import secrets

# Generate a secure API key
api_key = secrets.token_urlsafe(32)
print(f"Your API key: {api_key}")

# Store this securely!
```

### Step 2: Configure Your API Server

Edit `api_server.py` and add your generated key:

```python
API_KEYS = {
    'xK3mP9qR8vL2nF5wB7cZ1aY4tH6jN0sD2eM8gU5v': {  # Your generated key
        'name': 'Zapier Integration',
        'permissions': ['read']
    }
}
```

### Step 3: Start Your API Server

```bash
python3 api_server.py
```

You should see:
```
🚀 RTD API Server Starting
📋 Configuration:
   RTD Direct API: ✅ Available
   Google Maps API: ✅ Configured
🔑 API Keys:
   Default key: xK3mP9qR8vL2nF5wB7cZ1aY4tH6jN0sD2eM8gU5v
```

### Step 4: Test Your API

```bash
# Test without auth (should fail)
curl http://localhost:5000/api/vehicles

# Test with auth (should work)
curl -H "X-API-Key: xK3mP9qR8vL2nF5wB7cZ1aY4tH6jN0sD2eM8gU5v" \
     http://localhost:5000/api/vehicles
```

---

## 🔗 Part 3: Connecting to Zapier

### Option A: Use Webhooks by Zapier

1. **In Zapier, add "Webhooks by Zapier"**
2. **Choose "GET" request**
3. **Configure:**
   - URL: `http://your-server.com/api/vehicles`
   - Headers: Add `X-API-Key` with your generated key
   
   Example:
   ```
   URL: http://localhost:5000/api/vehicles
   Headers:
     X-API-Key: xK3mP9qR8vL2nF5wB7cZ1aY4tH6jN0sD2eM8gU5v
   ```

4. **Test** - You should see RTD vehicle data!

### Option B: Build a Custom Zapier App

For a better integration:

1. Go to [Zapier Platform](https://zapier.com/app/developer)
2. Create a new app
3. Configure authentication (API Key)
4. Add triggers/actions that call your API endpoints

---

## 🌐 Making Your API Publicly Accessible

Your API runs on `localhost` by default. For Zapier to access it, you need one of these:

### Option 1: Use ngrok (Quick Testing)

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com/

# Start your API server
python3 api_server.py

# In another terminal, expose it
ngrok http 5000
```

You'll get a public URL like: `https://abc123.ngrok.io`

Use this in Zapier: `https://abc123.ngrok.io/api/vehicles`

### Option 2: Deploy to Cloud (Production)

Deploy to:
- **Heroku** (easiest)
- **AWS Lambda** + API Gateway
- **Google Cloud Run**
- **DigitalOcean App Platform**

Then use your deployed URL in Zapier.

---

## 📋 Complete Zapier Setup Example

### Zap: "Get RTD Vehicle Data Every Hour"

**Trigger**: Schedule by Zapier
- Every 1 hour

**Action**: Webhooks by Zapier
- Method: GET
- URL: `https://your-server.com/api/vehicles`
- Headers:
  - Key: `X-API-Key`
  - Value: `xK3mP9qR8vL2nF5wB7cZ1aY4tH6jN0sD2eM8gU5v`

**Response**: JSON with all vehicle positions

**Next Actions** (examples):
- Send to Google Sheets
- Post to Slack
- Send email alert
- Store in Airtable

---

## 🔐 Security Best Practices

### 1. Environment Variables

Don't hardcode keys in your code:

```bash
# Set environment variables
export RTD_API_KEY="your-secret-key"
export ADMIN_SECRET="your-admin-secret"

# Run your server
python3 api_server.py
```

### 2. Use .env File

```bash
# Create .env file
echo "RTD_API_KEY=your-secret-key" > .env
echo "ADMIN_SECRET=your-admin-secret" >> .env

# Install python-dotenv
pip install python-dotenv
```

Update `api_server.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 3. Rotate Keys Regularly

Generate new keys periodically:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Use HTTPS

Always use HTTPS in production (ngrok provides this automatically).

---

## 🧪 Testing Your Setup

### Test 1: Health Check (No Auth)
```bash
curl http://localhost:5000/api/health
```

### Test 2: Get Vehicles (With Auth)
```bash
curl -H "X-API-Key: YOUR_KEY" http://localhost:5000/api/vehicles
```

### Test 3: Get Specific Route
```bash
curl -H "X-API-Key: YOUR_KEY" http://localhost:5000/api/vehicles/A
```

### Test 4: Get Directions
```bash
curl -H "X-API-Key: YOUR_KEY" \
     "http://localhost:5000/api/directions?origin=Union%20Station&destination=Denver%20Airport"
```

---

## 🆘 Troubleshooting

### "401 Unauthorized"
- Check that you're including the `X-API-Key` header
- Verify the key matches what's in `api_server.py`

### "403 Forbidden"
- Your API key is invalid
- Generate a new one and update `API_KEYS` in `api_server.py`

### "503 Service Unavailable"
- RTD's API might be down
- Google Maps API might not be configured

### Zapier Can't Connect
- Make sure your server is publicly accessible (use ngrok)
- Check firewall settings
- Verify the URL is correct

---

## 📊 API Key Types Summary

| Type | What It's For | Where to Get It | Cost |
|------|--------------|-----------------|------|
| **Google Maps API Key** | Your app → Google | Google Cloud Console | Free tier |
| **RTD API Key** | Your app → RTD | Not needed | Free |
| **Your Custom API Key** | Zapier → Your app | You generate it | Free |

---

## 🎯 Quick Start Checklist

- [ ] Generate Google Maps API key → Add to `config.py`
- [ ] Generate your custom API key: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Add your key to `api_server.py`
- [ ] Start API server: `python3 api_server.py`
- [ ] Test locally: `curl -H "X-API-Key: YOUR_KEY" http://localhost:5000/api/vehicles`
- [ ] Expose with ngrok: `ngrok http 5000`
- [ ] Configure Zapier webhook with your ngrok URL and API key
- [ ] Test your Zap!

---

## 🚀 Next Steps

1. **Start the API server**: `python3 api_server.py`
2. **Test it locally** with curl or browser
3. **Expose with ngrok** for Zapier access
4. **Create your Zap** using webhooks
5. **Deploy to production** when ready

Need help? Check the examples in `api_server.py` or run it to see the built-in documentation at `http://localhost:5000/`


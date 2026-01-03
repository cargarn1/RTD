# 🚀 Integrate RTD App with Zapier - Step-by-Step Guide

Complete step-by-step instructions to connect your RTD Transit API to Zapier.

---

## 📋 Prerequisites

- ✅ RTD API server code installed
- ✅ Python 3.7+ installed
- ✅ Zapier account (free tier works!)

---

## 🎯 Step 1: Generate Your API Key

**Time: 2 minutes**

```bash
cd /Users/carlosgarcia/Documents/Code/RTD
python3 generate_api_key.py
```

**What to do:**
1. Run the command above
2. Copy one of the generated keys (e.g., `h2YQRikxcs5uvYBsGNdotSYG7yVsDxlMpUqkitX6QPY`)
3. **Save it securely** - you'll need it for Zapier!

**Example output:**
```
🔑 RTD API Key Generator
Generated API Keys:
1. h2YQRikxcs5uvYBsGNdotSYG7yVsDxlMpUqkitX6QPY
2. xK3mP9qR8vL2nF5wB7cZ1aY4tH6jN0sD2eM8gU5v
```

---

## 🖥️ Step 2: Start Your API Server

**Time: 1 minute**

```bash
cd /Users/carlosgarcia/Documents/Code/RTD
python3 api_server.py
```

**What to expect:**
- Server starts on `http://localhost:8000` (port 8000)
- You'll see startup messages
- Server keeps running (don't close terminal)

**Success looks like:**
```
🚀 RTD API Server Starting
📋 Configuration:
   RTD Direct API: ✅ Available
🔑 API Keys:
   Default key: h2YQRikxcs5uvYBsGNdotSYG7yVsDxlMpUqkitX6QPY
 * Running on http://0.0.0.0:8000
```

**Keep this terminal open!**

---

## ✅ Step 3: Test Your API Locally

**Time: 1 minute**

Open a **new terminal** (keep server running in first terminal):

```bash
# Test health endpoint (no auth needed)
curl http://localhost:8000/api/health

# Test vehicles endpoint (needs API key)
curl -H "X-API-Key: h2YQRikxcs5uvYBsGNdotSYG7yVsDxlMpUqkitX6QPY" \
     http://localhost:8000/api/vehicles
```

**What to expect:**
- Health check returns: `{"status": "healthy", ...}`
- Vehicles endpoint returns JSON with vehicle data

**If it works:** ✅ Ready for Zapier!
**If it fails:** Check your API key matches the one in `api_server.py`

---

## 🌐 Step 4: Make Your Server Publicly Accessible

**Time: 3 minutes**

Zapier needs to reach your server from the internet. Use **ngrok**:

### Install ngrok (if not installed):

```bash
brew install ngrok
```

### Expose Your Server:

In a **new terminal** (keep server running):

```bash
ngrok http 8000
```

**What to expect:**
- ngrok starts and shows a public URL
- Example: `https://abc123.ngrok.io`
- **Copy this URL!** You'll need it for Zapier

**Example output:**
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

**Important:** 
- Keep ngrok running (don't close this terminal)
- Keep your API server running (don't close that terminal either)
- The URL changes each time you restart ngrok (free tier)

---

## 🔗 Step 5: Create Your Zap in Zapier

**Time: 5 minutes**

### 5.1: Go to Zapier

1. Visit: https://zapier.com
2. Sign in (or create free account)
3. Click **"Create Zap"**

### 5.2: Set Up Trigger

**Choose:** "Schedule by Zapier"

**Configure:**
- **Trigger Event:** Every Hour (or your preferred schedule)
- **Time:** Any time
- Click **"Continue"**
- Click **"Test trigger"** (optional)

### 5.3: Add Action - Webhooks

**Choose:** "Webhooks by Zapier"

**Configure:**
- **Event:** GET
- **URL:** `https://abc123.ngrok.io/api/vehicles` (your ngrok URL)
- **Headers:**
  - Click **"Add Header"**
  - **Key:** `X-API-Key`
  - **Value:** `h2YQRikxcs5uvYBsGNdotSYG7yVsDxlMpUqkitX6QPY` (your API key)

**Example:**
```
URL: https://abc123.ngrok.io/api/vehicles
Headers:
  X-API-Key: h2YQRikxcs5uvYBsGNdotSYG7yVsDxlMpUqkitX6QPY
```

### 5.4: Test Your Zap

1. Click **"Test action"**
2. You should see JSON data with vehicles
3. If successful: ✅ **Your Zap is working!**

### 5.5: Turn On Your Zap

1. Click **"Turn on Zap"**
2. Your automation is now live!

---

## 📊 Step 6: Use Your Data (Optional)

After getting vehicle data, you can add more actions:

### Example: Send to Google Sheets

1. Add action: **"Google Sheets"**
2. Event: **"Create Spreadsheet Row"**
3. Map fields from your webhook response
4. Save!

### Example: Send Email Alert

1. Add action: **"Email by Zapier"**
2. Configure email with vehicle data
3. Get notified when vehicles update!

---

## 🎯 Quick Reference

### Your API Endpoints:

| Endpoint | URL | Auth Required |
|----------|-----|---------------|
| Health Check | `/api/health` | ❌ No |
| All Vehicles | `/api/vehicles` | ✅ Yes |
| Vehicles by Route | `/api/vehicles/A` | ✅ Yes |
| Directions | `/api/directions?origin=X&destination=Y` | ✅ Yes |
| Nearby Stations | `/api/stations/nearby?location=X` | ✅ Yes |

### Your API Key:
```
h2YQRikxcs5uvYBsGNdotSYG7yVsDxlMpUqkitX6QPY
```

### Your Server:
- **Local:** http://localhost:8000
- **Public (ngrok):** https://abc123.ngrok.io (changes each restart)

---

## 🔧 Troubleshooting

### Problem: "Connection failed" in Zapier

**Solutions:**
1. ✅ Check ngrok is running (`ngrok http 8000`)
2. ✅ Check API server is running (`python3 api_server.py`)
3. ✅ Verify ngrok URL matches Zapier URL
4. ✅ Test URL manually: `curl https://abc123.ngrok.io/api/health`

### Problem: "401 Unauthorized"

**Solutions:**
1. ✅ Check API key in Zapier headers matches your server
2. ✅ Verify header name is exactly: `X-API-Key`
3. ✅ No extra spaces in the key

### Problem: "503 Service Unavailable"

**Solutions:**
1. ✅ RTD API might be temporarily down (wait a few minutes)
2. ✅ Check server logs for errors
3. ✅ Verify internet connection

### Problem: ngrok URL keeps changing

**Solutions:**
1. **Free tier:** URL changes each restart (normal)
2. **Update Zapier:** Change URL in your Zap when ngrok restarts
3. **Paid ngrok:** Get static domain (optional)

---

## 💡 Pro Tips

### Tip 1: Keep Everything Running
- ✅ API server terminal: Keep open
- ✅ ngrok terminal: Keep open
- ✅ Both must run for Zapier to work

### Tip 2: Use Environment Variables
Instead of hardcoding API key, use:
```bash
export RTD_API_KEY='your-key-here'
python3 api_server.py
```

### Tip 3: Schedule Wisely
- Every 15 minutes = 2,880 tasks/month (needs paid Zapier)
- Every hour = 720 tasks/month (free tier: 100/month)
- Daily = 30 tasks/month (free tier works!)

### Tip 4: Monitor Your Zap
- Check Zapier dashboard for run history
- See if your Zap is executing successfully
- Review any errors

---

## 🚀 Production Deployment (Optional)

For 24/7 operation without ngrok:

### Deploy to Heroku:

```bash
# Install Heroku CLI
brew install heroku

# Login
heroku login

# Create app
heroku create rtd-api

# Set API key
heroku config:set RTD_API_KEY=your-key-here

# Deploy
git push heroku main

# Your API: https://rtd-api.herokuapp.com
```

Then use `https://rtd-api.herokuapp.com` in Zapier instead of ngrok URL!

---

## ✅ Checklist

Use this checklist to ensure everything is set up:

- [ ] API key generated and saved
- [ ] API server running on port 8000
- [ ] Local API test successful
- [ ] ngrok installed and running
- [ ] ngrok URL copied
- [ ] Zapier account created
- [ ] Zap created with Schedule trigger
- [ ] Webhook action configured with:
  - [ ] Correct ngrok URL
  - [ ] X-API-Key header
  - [ ] Correct API key value
- [ ] Zap tested successfully
- [ ] Zap turned on
- [ ] Verified Zap runs automatically

---

## 📚 Additional Resources

- **Full Documentation:** `ZAPIER_INTEGRATION.md`
- **API Reference:** `README.md`
- **Quick Reference:** `QUICK_REFERENCE.md`
- **Zapier Help:** https://zapier.com/help

---

## 🎉 Success!

Once your Zap is running, you'll have:
- ✅ Automated RTD vehicle tracking
- ✅ Scheduled data collection
- ✅ Integration with other apps (Sheets, Email, Slack, etc.)
- ✅ No manual work needed!

**Your RTD Transit API is now integrated with Zapier!** 🚀

---

## 💰 Cost Summary

- **Development:** FREE (localhost + ngrok free tier)
- **Zapier:** FREE (100 tasks/month) or $19.99/month (750 tasks)
- **Production:** $5-7/month (Heroku/DigitalOcean) - optional

**Total:** $0-27/month depending on usage!

---

## 🆘 Need Help?

1. Check troubleshooting section above
2. Review `ZAPIER_INTEGRATION.md` for detailed examples
3. Test each step individually
4. Check Zapier logs for specific errors

**Happy automating!** 🎊


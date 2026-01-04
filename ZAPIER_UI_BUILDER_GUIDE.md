# Zapier UI Builder Integration Guide - RTD Transit API

Complete step-by-step guide to build a Zapier integration using the UI Builder for your RTD Transit API.

## 🎯 Prerequisites

Before starting, ensure you have:

- ✅ API server running on port 8000
- ✅ ngrok configured and running
- ✅ Your API key ready: `h2YQRikxcs5uvYBsGNdotSYG7yVsDxlMpUqkitX6QPY`
- ✅ Zapier account (free tier works)

## 📋 Step 1: Prepare Your API Server

### 1.1 Start Your API Server

```bash
cd /Users/carlosgarcia/Documents/Code/RTD
python3 api_server.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:8000
```

### 1.2 Start ngrok (in a separate terminal)

```bash
ngrok http 8000
```

**Copy your ngrok URL** (e.g., `https://abc123.ngrok.io`)

### 1.3 Test Your API

```bash
# Test health endpoint (no auth)
curl https://YOUR-NGROK-URL.ngrok.io/api/health

# Test vehicles endpoint (with auth)
curl -H "X-API-Key: h2YQRikxcs5uvYBsGNdotSYG7yVsDxlMpUqkitX6QPY" \
     https://YOUR-NGROK-URL.ngrok.io/api/vehicles
```

---

## 🚀 Step 2: Create Your Zapier App

### 2.1 Access Zapier Platform

1. Go to: **https://zapier.com/app/developer**
2. Click **"Create App"** or **"New App"**
3. Choose **"UI Builder"** (not CLI)

### 2.2 Basic App Information

Fill in the form:

- **App Name**: `RTD Transit API`
- **App Description**: `Real-time RTD Denver transit data including vehicle positions, routes, and directions`
- **App Category**: `Travel` or `Productivity`
- **App Logo**: (Optional - upload later)

Click **"Create App"**

---

## 🔐 Step 3: Configure Authentication

### 3.1 Add Authentication Method

1. In your Zapier app, go to **"Authentication"** tab
2. Click **"Add Authentication"**
3. Select **"API Key"** authentication type

### 3.2 Configure API Key Auth

Fill in the fields:

**Label**: `API Key`

**Key Name**: `X-API-Key` (this matches your server's header name)

**Help Text**: 
```
Enter your RTD Transit API key. Get your key from the API server administrator.
```

**Add API Key to**: Select **"Header"**

**Header Name**: `X-API-Key`

### 3.3 Test Authentication

1. Click **"Test Authentication"**
2. Enter your API key: `h2YQRikxcs5uvYBsGNdotSYG7yVsDxlMpUqkitX6QPY`
3. **Test URL**: `https://YOUR-NGROK-URL.ngrok.io/api/health`
4. **Method**: `GET`
5. Click **"Test"**

**Expected**: Should return `{"status": "healthy", ...}`

✅ If successful, authentication is configured!

---

## 🎯 Step 4: Create Triggers

### Trigger 1: New Vehicle Position

#### 4.1 Create Trigger

1. Go to **"Triggers"** tab
2. Click **"Add Trigger"**
3. Name: `New Vehicle Position`
4. Key: `new_vehicle_position`
5. Description: `Triggers when checking for new vehicle positions`

#### 4.2 Configure Input Fields

Click **"Add Input Field"** for each:

**Field 1:**
- **Label**: `Route ID`
- **Key**: `route_id`
- **Type**: `String`
- **Help Text**: `Optional: Filter by specific route (e.g., "A", "AB1"). Leave empty for all routes.`
- **Required**: `No`

#### 4.3 Configure API Request

**Request Method**: `GET`

**URL**: 
```
https://YOUR-NGROK-URL.ngrok.io/api/vehicles
```

**Headers**:
- `X-API-Key`: `{{bundle.authData.api_key}}` (Zapier will auto-populate)

**URL Params** (Optional - if route_id provided):
- If `route_id` is provided, use: `https://YOUR-NGROK-URL.ngrok.io/api/vehicles/{{bundle.inputData.route_id}}`

**Note**: For dynamic URL, you can use:
```
https://YOUR-NGROK-URL.ngrok.io/api/vehicles{{bundle.inputData.route_id ? '/' + bundle.inputData.route_id : ''}}
```

#### 4.4 Configure Response Parsing

**Sample Response** (paste this):
```json
{
  "success": true,
  "count": 340,
  "vehicles": [
    {
      "vehicle_id": "46EB8ED6CB7DDF73E063DD4D1FACD7C6",
      "route_id": "A",
      "latitude": 39.771766,
      "longitude": -104.817214,
      "bearing": 276.0,
      "speed": null,
      "timestamp": 1704067200,
      "trip_id": "115553959"
    }
  ],
  "routes": ["A", "AB1", "0", "1", ...],
  "route_counts": {"A": 8, "AB1": 3, ...}
}
```

**Data to Return**: 
- Click **"Use Response"**
- Select: `vehicles` (this will return an array of vehicles)

#### 4.5 Test the Trigger

1. Click **"Test"**
2. Leave `route_id` empty (to get all vehicles)
3. Click **"Test"**

**Expected**: Should return array of vehicle objects

✅ Trigger is ready!

---

### Trigger 2: New Route Available

#### 4.6 Create Second Trigger

1. **Name**: `New Route Available`
2. **Key**: `new_route_available`
3. **Description**: `Triggers when checking for available routes`

#### 4.7 Configure API Request

**URL**: `https://YOUR-NGROK-URL.ngrok.io/api/routes`

**Method**: `GET`

**Headers**: `X-API-Key: {{bundle.authData.api_key}}`

**Sample Response**:
```json
{
  "success": true,
  "routes": ["A", "AB1", "0", "1", ...],
  "count": 95,
  "route_counts": {"A": 8, "AB1": 3, ...}
}
```

**Data to Return**: `routes` (array of route IDs)

✅ Second trigger ready!

---

## ⚡ Step 5: Create Actions

### Action 1: Get Vehicle Positions

#### 5.1 Create Action

1. Go to **"Actions"** tab
2. Click **"Add Action"**
3. **Name**: `Get Vehicle Positions`
4. **Key**: `get_vehicle_positions`
5. **Description**: `Retrieve current positions of RTD vehicles`

#### 5.2 Configure Input Fields

**Field 1:**
- **Label**: `Route ID`
- **Key**: `route_id`
- **Type**: `String`
- **Required**: `No`
- **Help Text**: `Optional: Filter by route (e.g., "A"). Leave empty for all routes.`

#### 5.3 Configure API Request

**Method**: `GET`

**URL**: 
```
https://YOUR-NGROK-URL.ngrok.io/api/vehicles{{bundle.inputData.route_id ? '/' + bundle.inputData.route_id : ''}}
```

**Headers**:
- `X-API-Key`: `{{bundle.authData.api_key}}`

#### 5.4 Configure Output Fields

Zapier will auto-detect fields from the response. You can customize:

**Output Fields**:
- `vehicle_id`
- `route_id`
- `latitude`
- `longitude`
- `bearing`
- `speed`
- `timestamp`
- `trip_id`

#### 5.5 Test Action

1. Click **"Test"**
2. Leave `route_id` empty
3. Click **"Test"`

✅ Action ready!

---

### Action 2: Get All Routes

#### 5.6 Create Second Action

1. **Name**: `Get All Routes`
2. **Key**: `get_all_routes`
3. **Description**: `Retrieve list of all active RTD routes`

#### 5.7 Configure API Request

**URL**: `https://YOUR-NGROK-URL.ngrok.io/api/routes`

**Method**: `GET`

**Headers**: `X-API-Key: {{bundle.authData.api_key}}`

**Output Fields**:
- `routes` (array)
- `count` (number)
- `route_counts` (object)

✅ Second action ready!

---

### Action 3: Get Vehicles by Route

#### 5.8 Create Third Action

1. **Name**: `Get Vehicles by Route`
2. **Key**: `get_vehicles_by_route`
3. **Description**: `Get all vehicles for a specific route`

#### 5.9 Configure Input Fields

**Field 1:**
- **Label**: `Route ID`
- **Key**: `route_id`
- **Type**: `String`
- **Required**: `Yes`
- **Help Text**: `Route identifier (e.g., "A", "AB1", "15")`

#### 5.10 Configure API Request

**URL**: `https://YOUR-NGROK-URL.ngrok.io/api/vehicles/{{bundle.inputData.route_id}}`

**Method**: `GET`

**Headers**: `X-API-Key: {{bundle.authData.api_key}}`

✅ Third action ready!

---

## 🧪 Step 6: Test Your Integration

### 6.1 Test Each Component

1. **Test Authentication**: Should return health check
2. **Test Triggers**: Should return data arrays
3. **Test Actions**: Should return expected data

### 6.2 Create a Test Zap

1. Go to **"Zaps"** in Zapier
2. Click **"Create Zap"**
3. **Trigger**: Choose your app → "New Vehicle Position"
4. **Action**: Choose your app → "Get Vehicle Positions"
5. **Test**: Run the Zap

**Expected**: Should successfully retrieve vehicle data

---

## 📤 Step 7: Publish Your App

### 7.1 Review App Settings

Before publishing, review:

- ✅ App name and description
- ✅ Authentication configured correctly
- ✅ All triggers and actions tested
- ✅ Help text is clear
- ✅ Logo uploaded (optional)

### 7.2 Invite Testers (Optional)

1. Go to **"Sharing"** tab
2. Add email addresses of testers
3. They can test your app before public release

### 7.3 Submit for Review

1. Go to **"Publishing"** tab
2. Click **"Submit for Review"**
3. Fill out the submission form:
   - **App Description**: Describe your RTD Transit API integration
   - **Use Cases**: List common workflows
   - **Support Contact**: Your email

### 7.4 Private vs Public

**Private App** (Recommended for now):
- Only you can use it
- No review needed
- Perfect for personal use

**Public App**:
- Available in Zapier App Directory
- Requires review
- Great for sharing with others

---

## 🎨 Step 8: Advanced Configuration

### 8.1 Dynamic URL Based on Input

For routes endpoint that changes based on input:

**URL Template**:
```
https://YOUR-NGROK-URL.ngrok.io/api/vehicles{{bundle.inputData.route_id ? '/' + bundle.inputData.route_id : ''}}
```

### 8.2 Error Handling

Zapier will automatically handle:
- 401 Unauthorized (invalid API key)
- 503 Service Unavailable (RTD API down)
- Network errors

### 8.3 Rate Limiting

Your API server should handle rate limiting. Zapier will respect:
- HTTP 429 responses
- Retry logic

---

## 📝 Step 9: Create Your First Zap

### Example Zap: Daily Route Report

1. **Trigger**: Schedule by Zapier (Daily at 7 AM)
2. **Action**: Your App → "Get All Routes"
3. **Action**: Filter by Zapier (optional filtering)
4. **Action**: Gmail → Send Email with route list

### Example Zap: Route Alert

1. **Trigger**: Schedule by Zapier (Every 15 minutes)
2. **Action**: Your App → "Get Vehicles by Route"
   - Route ID: `A`
3. **Action**: Code by Zapier
   - Check if vehicle count < 3
4. **Action**: SMS by Zapier (if count low)

---

## 🔧 Troubleshooting

### Issue: "Authentication Failed"

**Solution**:
- Verify API key is correct
- Check ngrok URL is accessible
- Ensure `X-API-Key` header name matches

### Issue: "No Data Returned"

**Solution**:
- Test API endpoint directly with curl
- Check ngrok tunnel is active
- Verify response format matches sample

### Issue: "Invalid Response Format"

**Solution**:
- Ensure API returns valid JSON
- Check response structure matches sample
- Verify data array is correctly formatted

### Issue: "URL Not Found"

**Solution**:
- Verify ngrok URL is correct
- Check API server is running
- Ensure endpoint path matches exactly

---

## ✅ Checklist

Before going live:

- [ ] API server running and tested
- [ ] ngrok tunnel active
- [ ] Authentication configured and tested
- [ ] All triggers created and tested
- [ ] All actions created and tested
- [ ] Sample responses configured
- [ ] Help text added to all fields
- [ ] Test Zap created and working
- [ ] Error handling verified
- [ ] Documentation reviewed

---

## 🎉 You're Done!

Your RTD Transit API is now integrated with Zapier! You can:

- ✅ Create Zaps with RTD data
- ✅ Share with your team (if private app)
- ✅ Publish publicly (if desired)
- ✅ Build powerful automation workflows

## 📚 Next Steps

1. **Create Your First Zap**: Use your triggers and actions
2. **Monitor Usage**: Check Zapier dashboard for activity
3. **Iterate**: Add more triggers/actions as needed
4. **Deploy Production**: Move from ngrok to production server

## 🔗 Useful Links

- [Zapier Platform Docs](https://platform.zapier.com/docs)
- [Zapier UI Builder Guide](https://platform.zapier.com/docs/quickstart-intro)
- [Your API Server](api_server.py)
- [Zapier Integration Guide](ZAPIER_INTEGRATION.md)

---

**Questions?** Check the troubleshooting section or review Zapier's platform documentation.


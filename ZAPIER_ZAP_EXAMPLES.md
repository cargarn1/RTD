# Zapier Zap Examples - RTD Transit API

Practical examples of Zaps using the RTD Transit API integration, including triggers and actions.

## 📋 Table of Contents

- [Trigger Examples](#trigger-examples)
- [Action Examples](#action-examples)
- [Combined Workflows](#combined-workflows)
- [Field Reference](#field-reference)

---

## 🎯 Trigger Examples

### Example 1: New Vehicle Alert via Email

**Use Case**: Get notified when a new vehicle enters RTD service

**Zap Configuration**:
1. **Trigger**: RTD Transit API - "New Vehicle in Service"
   - Polling frequency: Every 5 minutes
   
2. **Action**: Gmail - Send Email
   - **To**: `your-email@example.com`
   - **Subject**: `New RTD Vehicle on Route {{1.route_id}}`
   - **Body**:
     ```
     A new vehicle has entered RTD service!
     
     Vehicle Details:
     - Vehicle ID: {{1.vehicle_id}}
     - Route: {{1.route_id}}
     - Location: {{1.latitude}}, {{1.longitude}}
     - Direction: {{1.bearing}}°
     - Trip ID: {{1.trip_id}}
     - Timestamp: {{1.timestamp}}
     ```

**Available Fields from Trigger**:
- `{{1.id}}` - Vehicle ID (for deduplication)
- `{{1.vehicle_id}}` - Vehicle identifier
- `{{1.route_id}}` - Route identifier (e.g., "A", "73", "AB1")
- `{{1.latitude}}` - Vehicle latitude
- `{{1.longitude}}` - Vehicle longitude
- `{{1.bearing}}` - Direction of travel (degrees)
- `{{1.speed}}` - Vehicle speed
- `{{1.timestamp}}` - Unix timestamp
- `{{1.trip_id}}` - Trip identifier

---

### Example 2: Log New Vehicles to Google Sheets

**Use Case**: Track all new vehicles entering service in a spreadsheet

**Zap Configuration**:
1. **Trigger**: RTD Transit API - "New Vehicle in Service"
   - Polling frequency: Every 15 minutes
   
2. **Action**: Google Sheets - Create Spreadsheet Row
   - **Spreadsheet**: "RTD Vehicle Log"
   - **Worksheet**: "New Vehicles"
   - **Columns**:
     - **Timestamp**: `{{1.timestamp}}`
     - **Vehicle ID**: `{{1.vehicle_id}}`
     - **Route**: `{{1.route_id}}`
     - **Latitude**: `{{1.latitude}}`
     - **Longitude**: `{{1.longitude}}`
     - **Bearing**: `{{1.bearing}}`
     - **Trip ID**: `{{1.trip_id}}`

**Benefits**: 
- Historical tracking of vehicle entries
- Easy analysis of which routes get new vehicles most often
- Data export capabilities

---

### Example 3: SMS Alert for Specific Route

**Use Case**: Get SMS notification when a new vehicle enters service on a specific route (e.g., A Line to airport)

**Zap Configuration**:
1. **Trigger**: RTD Transit API - "New Vehicle in Service"
   - Polling frequency: Every 5 minutes
   
2. **Filter**: Filter by Zapier
   - **Condition**: `{{1.route_id}}` equals `A`
   - Only proceed if route is "A"
   
3. **Action**: SMS by Zapier - Send SMS
   - **To**: `+1-XXX-XXX-XXXX`
   - **Message**: 
     ```
     🚌 New A Line vehicle in service!
     Vehicle: {{1.vehicle_id}}
     Location: {{1.latitude}}, {{1.longitude}}
     ```

**Note**: You can filter for any route (A, AB1, 15, etc.)

---

### Example 4: Slack Notification with Map Link

**Use Case**: Notify your team in Slack when new vehicles enter service

**Zap Configuration**:
1. **Trigger**: RTD Transit API - "New Vehicle in Service"
   - Polling frequency: Every 10 minutes
   
2. **Action**: Slack - Send Channel Message
   - **Channel**: `#rtd-alerts`
   - **Message**:
     ```
     🚌 New RTD Vehicle in Service
     
     *Route:* {{1.route_id}}
     *Vehicle:* {{1.vehicle_id}}
     *Location:* {{1.latitude}}, {{1.longitude}}
     *Direction:* {{1.bearing}}°
     
     View on map: https://www.google.com/maps?q={{1.latitude}},{{1.longitude}}
     ```

---

### Example 5: Create Calendar Event for New Vehicles

**Use Case**: Track when vehicles enter service (useful for maintenance tracking)

**Zap Configuration**:
1. **Trigger**: RTD Transit API - "New Vehicle in Service"
   - Polling frequency: Every 15 minutes
   
2. **Action**: Google Calendar - Create Event
   - **Calendar**: "RTD Vehicle Service"
   - **Title**: `Vehicle {{1.vehicle_id}} - Route {{1.route_id}}`
   - **Start Time**: Current time (or use timestamp converter)
   - **Description**: 
     ```
     Vehicle entered service
     Route: {{1.route_id}}
     Location: {{1.latitude}}, {{1.longitude}}
     Trip ID: {{1.trip_id}}
     ```

---

## ⚡ Action Examples

### Example 6: Daily Vehicle Report

**Use Case**: Get a daily summary of all active vehicles

**Zap Configuration**:
1. **Trigger**: Schedule by Zapier
   - **Trigger Event**: Every Day
   - **Time**: 7:00 AM
   
2. **Action**: RTD Transit API - "Get All Vehicles"
   - No input fields needed
   
3. **Action**: Code by Zapier - JavaScript
   - **Code**:
     ```javascript
     const vehicles = inputData.vehicles || [];
     const routeCounts = {};
     
     vehicles.forEach(vehicle => {
       const route = vehicle.route_id;
       routeCounts[route] = (routeCounts[route] || 0) + 1;
     });
     
     return {
       totalVehicles: vehicles.length,
       routeCounts: JSON.stringify(routeCounts),
       summary: `Total: ${vehicles.length} vehicles across ${Object.keys(routeCounts).length} routes`
     };
     ```
   
4. **Action**: Gmail - Send Email
   - **To**: `your-email@example.com`
   - **Subject**: `Daily RTD Vehicle Report - {{3.summary}}`
   - **Body**:
     ```
     Daily RTD Vehicle Report
     
     Total Vehicles: {{3.totalVehicles}}
     Routes Active: {{3.routeCounts}}
     ```

---

### Example 7: Check Vehicles on Specific Route

**Use Case**: Get current vehicles on a specific route (e.g., check A Line status)

**Zap Configuration**:
1. **Trigger**: Schedule by Zapier
   - **Trigger Event**: Every 15 minutes
   
2. **Action**: RTD Transit API - "Get Vehicles by Route"
   - **Route ID**: `A` (or any route like "AB1", "15", "73")
   
3. **Action**: Gmail - Send Email (if count is low)
   - **Filter**: Filter by Zapier
     - **Condition**: `{{2.count}}` is less than `3`
     - Only send if fewer than 3 vehicles on route
   - **Subject**: `Alert: Low vehicle count on Route A`
   - **Body**: 
     ```
     Only {{2.count}} vehicles currently active on Route A.
     
     Vehicles:
     {{2.vehicles}}
     ```

---

### Example 8: Route Status Dashboard

**Use Case**: Get all routes and their vehicle counts

**Zap Configuration**:
1. **Trigger**: Schedule by Zapier
   - **Trigger Event**: Every hour
   
2. **Action**: RTD Transit API - "Get All Routes"
   - No input fields needed
   
3. **Action**: Google Sheets - Create Spreadsheet Row
   - **Spreadsheet**: "RTD Route Status"
   - **Columns**:
     - **Timestamp**: Current time
     - **Total Routes**: `{{2.count}}`
     - **Routes List**: `{{2.routes}}`
     - **Route Counts**: `{{2.route_counts}}`

---

### Example 9: Vehicle Position Tracker

**Use Case**: Track vehicle positions over time

**Zap Configuration**:
1. **Trigger**: Schedule by Zapier
   - **Trigger Event**: Every 5 minutes
   
2. **Action**: RTD Transit API - "Get Vehicles by Route"
   - **Route ID**: `A` (or your route of interest)
   
3. **Action**: Google Sheets - Create Spreadsheet Row
   - **Spreadsheet**: "Vehicle Positions"
   - **For each vehicle** (use "Create Many Rows"):
     - **Timestamp**: Current time
     - **Vehicle ID**: `{{2.vehicles[].vehicle_id}}`
     - **Route**: `{{2.vehicles[].route_id}}`
     - **Latitude**: `{{2.vehicles[].latitude}}`
     - **Longitude**: `{{2.vehicles[].longitude}}`
     - **Bearing**: `{{2.vehicles[].bearing}}`

**Note**: Use Zapier's "Create Many Rows" feature to add one row per vehicle

---

### Example 10: Route Comparison Report

**Use Case**: Compare vehicle counts across multiple routes

**Zap Configuration**:
1. **Trigger**: Schedule by Zapier
   - **Trigger Event**: Every hour
   
2. **Action**: RTD Transit API - "Get All Routes"
   - Get list of all routes
   
3. **Action**: Code by Zapier - JavaScript
   - Process route_counts to format data
   
4. **Action**: Google Sheets - Update Row
   - Update dashboard with route statistics

---

## 🔄 Combined Workflows

### Example 11: New Vehicle → Get Details → Notify

**Use Case**: When new vehicle enters, get full details and send comprehensive notification

**Zap Configuration**:
1. **Trigger**: RTD Transit API - "New Vehicle in Service"
   
2. **Action**: RTD Transit API - "Get Vehicles by Route"
   - **Route ID**: `{{1.route_id}}`
   - Get all vehicles on that route
   
3. **Action**: Gmail - Send Email
   - **Subject**: `New Vehicle on Route {{1.route_id}} - Total: {{2.count}} vehicles`
   - **Body**:
     ```
     New Vehicle Alert!
     
     New Vehicle:
     - ID: {{1.vehicle_id}}
     - Route: {{1.route_id}}
     - Location: {{1.latitude}}, {{1.longitude}}
     
     Route Status:
     - Total vehicles on route: {{2.count}}
     - All vehicles: {{2.vehicles}}
     ```

---

### Example 12: Monitor Route Health

**Use Case**: Monitor if a route has sufficient vehicles

**Zap Configuration**:
1. **Trigger**: Schedule by Zapier
   - **Trigger Event**: Every 15 minutes
   
2. **Action**: RTD Transit API - "Get Vehicles by Route"
   - **Route ID**: `A`
   
3. **Filter**: Filter by Zapier
   - **Condition**: `{{2.count}}` is less than `3`
   - Only proceed if vehicle count is low
   
4. **Action**: Slack - Send Channel Message
   - **Message**: 
     ```
     ⚠️ Low vehicle count on Route A
     Only {{2.count}} vehicles active
     Expected: 5-8 vehicles
     ```

---

## 📊 Field Reference

### Trigger Output Fields

When "New Vehicle in Service" trigger fires:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | String | Vehicle ID (for deduplication) | `4777857AE3E45173E063DC4D1FAC2C91` |
| `vehicle_id` | String | Vehicle identifier | `4777857AE3E45173E063DC4D1FAC2C91` |
| `route_id` | String | Route identifier | `73`, `A`, `AB1` |
| `latitude` | Number | Vehicle latitude | `39.76521682739258` |
| `longitude` | Number | Vehicle longitude | `-104.90258026123047` |
| `bearing` | Number | Direction (degrees, 0-360) | `12.0` |
| `speed` | Number/null | Vehicle speed | `null` or `25.5` |
| `timestamp` | Number | Unix timestamp | `1767508396` |
| `trip_id` | String | Trip identifier | `115554251` |

**Access in Zap**: Use `{{1.field_name}}` (where 1 is the trigger step)

---

### Action Output Fields

#### "Get All Vehicles" Action

| Field | Type | Description |
|-------|------|-------------|
| `vehicles` | Array | Array of vehicle objects |
| `count` | Number | Total number of vehicles |
| `routes` | Array | List of route IDs |
| `route_counts` | Object | Vehicle count per route |

**Access in Zap**: Use `{{2.vehicles}}`, `{{2.count}}`, etc.

#### "Get Vehicles by Route" Action

| Field | Type | Description |
|-------|------|-------------|
| `vehicles` | Array | Array of vehicles on the route |
| `count` | Number | Number of vehicles on route |
| `route` | String | Route ID queried |

**Access in Zap**: Use `{{2.vehicles}}`, `{{2.count}}`, `{{2.route}}`

#### "Get All Routes" Action

| Field | Type | Description |
|-------|------|-------------|
| `routes` | Array | List of all route IDs |
| `count` | Number | Total number of routes |
| `route_counts` | Object | Vehicle count per route |

**Access in Zap**: Use `{{2.routes}}`, `{{2.count}}`, `{{2.route_counts}}`

---

## 💡 Tips & Best Practices

### Polling Frequency

- **Every 1 minute**: Very frequent, catches new vehicles quickly, higher API usage
- **Every 5 minutes**: Balanced, good for most use cases
- **Every 15 minutes**: Less frequent, lower API usage
- **Every hour**: For reports and summaries

### Filtering

Use "Filter by Zapier" to:
- Only process specific routes
- Only trigger if vehicle count is above/below threshold
- Filter by location (latitude/longitude ranges)

### Error Handling

- RTD API may occasionally be unavailable
- Use Zapier's retry logic
- Consider fallback actions for errors

### Data Formatting

- Use Zapier's "Formatter" utility to:
  - Convert timestamps to readable dates
  - Format coordinates for maps
  - Format numbers (speed, bearing)

---

## 🚀 Getting Started

1. **Set up your RTD Transit API integration** in Zapier
2. **Choose an example** from above that fits your needs
3. **Create the Zap** following the configuration steps
4. **Test** with a sample run
5. **Turn on** your Zap

---

## 📝 Notes

- All examples assume you've connected your RTD Transit API account in Zapier
- Replace placeholder values (emails, phone numbers, etc.) with your actual values
- Adjust polling frequencies based on your needs
- Some actions may require premium Zapier plans

---

## 🔗 Related Documentation

- [Zapier Integration Guide](ZAPIER_INTEGRATION.md)
- [Zapier UI Builder Guide](ZAPIER_UI_BUILDER_GUIDE.md)
- [API Server Documentation](api_server.py)
- [API Endpoints](README.md#api-endpoints)

---

**Happy Automating!** 🚌✨


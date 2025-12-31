"""
RTD API Server - Flask-based REST API with API Key authentication
This allows you to expose RTD data through your own authenticated API
Perfect for Zapier integration!
"""

from flask import Flask, request, jsonify
from functools import wraps
import secrets
import os
from rtd_client import RTDClient
from google_transit_client import GoogleTransitClient
from config import GOOGLE_MAPS_API_KEY

app = Flask(__name__)

# API Key Management
# In production, store these in a database
API_KEYS = {
    # Generate keys using: python3 -c "import secrets; print(secrets.token_urlsafe(32))"
    os.environ.get('RTD_API_KEY', 'demo-key-change-in-production'): {
        'name': 'Default Key',
        'permissions': ['read']
    }
}

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                'error': 'No API key provided',
                'message': 'Include X-API-Key header or api_key query parameter'
            }), 401
        
        if api_key not in API_KEYS:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is not valid'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


# Initialize clients
rtd_client = RTDClient()
google_client = GoogleTransitClient(GOOGLE_MAPS_API_KEY) if GOOGLE_MAPS_API_KEY != 'YOUR_GOOGLE_MAPS_API_KEY_HERE' else None


@app.route('/')
def index():
    """API documentation"""
    return jsonify({
        'name': 'RTD Transit API',
        'version': '1.0',
        'description': 'REST API for RTD Denver transit data',
        'authentication': 'API Key required (X-API-Key header or api_key parameter)',
        'endpoints': {
            'GET /api/vehicles': 'Get all active vehicle positions',
            'GET /api/vehicles/<route_id>': 'Get vehicles for specific route',
            'GET /api/directions': 'Get transit directions (requires Google Maps API)',
            'GET /api/stations/nearby': 'Find nearby transit stations',
            'GET /api/health': 'Health check (no auth required)',
        },
        'zapier_webhook_url': request.host_url + 'api/vehicles',
        'example_request': request.host_url + 'api/vehicles?api_key=YOUR_API_KEY'
    })


@app.route('/api/health')
def health():
    """Health check endpoint (no authentication required)"""
    return jsonify({
        'status': 'healthy',
        'rtd_api': 'available',
        'google_maps_api': 'configured' if google_client else 'not configured'
    })


@app.route('/api/vehicles', methods=['GET'])
@require_api_key
def get_vehicles():
    """
    Get all active RTD vehicles
    
    Query Parameters:
        route (optional): Filter by route ID (e.g., ?route=A)
        format (optional): Response format (default: json)
    
    Example:
        GET /api/vehicles?api_key=YOUR_KEY
        GET /api/vehicles?api_key=YOUR_KEY&route=A
    """
    route_filter = request.args.get('route')
    
    vehicles = rtd_client.get_vehicle_positions()
    
    if vehicles is None:
        return jsonify({
            'error': 'Failed to fetch vehicle data',
            'message': 'RTD API may be temporarily unavailable'
        }), 503
    
    # Filter by route if specified
    if route_filter:
        vehicles = [v for v in vehicles if v['route_id'] == route_filter.upper()]
    
    return jsonify({
        'success': True,
        'count': len(vehicles),
        'vehicles': vehicles
    })


@app.route('/api/vehicles/<route_id>', methods=['GET'])
@require_api_key
def get_vehicles_by_route(route_id):
    """
    Get vehicles for a specific route
    
    Example:
        GET /api/vehicles/A?api_key=YOUR_KEY
    """
    vehicles = rtd_client.get_vehicle_positions()
    
    if vehicles is None:
        return jsonify({
            'error': 'Failed to fetch vehicle data'
        }), 503
    
    route_vehicles = [v for v in vehicles if v['route_id'] == route_id.upper()]
    
    return jsonify({
        'success': True,
        'route': route_id.upper(),
        'count': len(route_vehicles),
        'vehicles': route_vehicles
    })


@app.route('/api/directions', methods=['GET'])
@require_api_key
def get_directions():
    """
    Get transit directions between two locations
    
    Query Parameters:
        origin (required): Starting location
        destination (required): Ending location
        departure_time (optional): ISO format datetime
    
    Example:
        GET /api/directions?origin=Union%20Station&destination=Denver%20Airport&api_key=YOUR_KEY
    """
    if not google_client:
        return jsonify({
            'error': 'Google Maps API not configured',
            'message': 'Set GOOGLE_MAPS_API_KEY in config.py'
        }), 503
    
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    if not origin or not destination:
        return jsonify({
            'error': 'Missing parameters',
            'message': 'Both origin and destination are required'
        }), 400
    
    result = google_client.get_transit_directions(origin, destination)
    
    if not result or not result.get('routes'):
        return jsonify({
            'error': 'No routes found',
            'message': 'Could not find transit directions'
        }), 404
    
    return jsonify({
        'success': True,
        'origin': origin,
        'destination': destination,
        'routes': result['routes']
    })


@app.route('/api/stations/nearby', methods=['GET'])
@require_api_key
def get_nearby_stations():
    """
    Find nearby transit stations
    
    Query Parameters:
        location (required): Address or location
        radius (optional): Search radius in meters (default: 1000)
    
    Example:
        GET /api/stations/nearby?location=Downtown%20Denver&api_key=YOUR_KEY
    """
    if not google_client:
        return jsonify({
            'error': 'Google Maps API not configured'
        }), 503
    
    location = request.args.get('location')
    radius = request.args.get('radius', 1000, type=int)
    
    if not location:
        return jsonify({
            'error': 'Missing location parameter'
        }), 400
    
    stations = google_client.find_nearby_transit_stations(location, radius)
    
    if stations is None:
        return jsonify({
            'error': 'Failed to find stations'
        }), 503
    
    return jsonify({
        'success': True,
        'location': location,
        'radius': radius,
        'count': len(stations),
        'stations': stations
    })


@app.route('/api/keys/generate', methods=['POST'])
def generate_api_key():
    """
    Generate a new API key (admin only - should be protected in production)
    
    Body:
        {
            "name": "My Application",
            "admin_secret": "your-admin-secret"
        }
    """
    admin_secret = request.json.get('admin_secret')
    expected_secret = os.environ.get('ADMIN_SECRET', 'change-me-in-production')
    
    if admin_secret != expected_secret:
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Invalid admin secret'
        }), 403
    
    # Generate a new API key
    new_key = secrets.token_urlsafe(32)
    name = request.json.get('name', 'Unnamed Key')
    
    API_KEYS[new_key] = {
        'name': name,
        'permissions': ['read']
    }
    
    return jsonify({
        'success': True,
        'api_key': new_key,
        'name': name,
        'message': 'Store this key securely - it cannot be retrieved again'
    }), 201


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 RTD API Server Starting")
    print("="*80)
    print("\n📋 Configuration:")
    print(f"   RTD Direct API: ✅ Available")
    print(f"   Google Maps API: {'✅ Configured' if google_client else '⚠️  Not configured'}")
    print("\n🔑 API Keys:")
    print(f"   Default key: {list(API_KEYS.keys())[0]}")
    print(f"   ⚠️  Change this in production!")
    print("\n📚 Endpoints:")
    print("   GET  / - API documentation")
    print("   GET  /api/health - Health check")
    print("   GET  /api/vehicles - All vehicles")
    print("   GET  /api/vehicles/<route> - Vehicles by route")
    print("   GET  /api/directions - Transit directions")
    print("   GET  /api/stations/nearby - Find stations")
    print("\n🔗 For Zapier:")
    print("   Webhook URL: http://localhost:5000/api/vehicles")
    print("   Add header: X-API-Key: " + list(API_KEYS.keys())[0])
    print("\n" + "="*80 + "\n")
    
    # Run the server
    app.run(debug=True, host='0.0.0.0', port=5000)


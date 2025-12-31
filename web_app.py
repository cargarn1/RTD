#!/usr/bin/env python3
"""
RTD Transit Web Frontend
Beautiful, interactive web interface for RTD transit data
"""

from flask import Flask, render_template, jsonify, request
from rtd_client import RTDClient
from google_transit_client import GoogleTransitClient
from route_details import RouteDetailsClient
from config import GOOGLE_MAPS_API_KEY, validate_google_api_key, COMMON_LOCATIONS

app = Flask(__name__)

# Initialize clients
rtd_client = RTDClient()
google_client = GoogleTransitClient(GOOGLE_MAPS_API_KEY) if validate_google_api_key() else None
route_details_client = RouteDetailsClient()


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         google_maps_configured=google_client is not None,
                         common_locations=COMMON_LOCATIONS)


@app.route('/api/vehicles')
def get_vehicles():
    """Get all active vehicles"""
    route_filter = request.args.get('route')
    
    vehicles = rtd_client.get_vehicle_positions()
    
    if vehicles is None:
        return jsonify({'error': 'Failed to fetch vehicle data'}), 503
    
    # Filter by route if specified
    if route_filter:
        vehicles = [v for v in vehicles if v['route_id'] == route_filter.upper()]
    
    # Get route statistics
    route_counts = {}
    for v in vehicles:
        route = v['route_id']
        route_counts[route] = route_counts.get(route, 0) + 1
    
    return jsonify({
        'success': True,
        'count': len(vehicles),
        'vehicles': vehicles,
        'route_counts': route_counts,
        'routes': sorted(route_counts.keys())
    })


@app.route('/api/routes')
def get_routes():
    """Get unique route list"""
    vehicles = rtd_client.get_vehicle_positions()
    
    if vehicles is None:
        return jsonify({'error': 'Failed to fetch data'}), 503
    
    routes = sorted(list(set(v['route_id'] for v in vehicles)))
    return jsonify({'routes': routes})


@app.route('/api/directions')
def get_directions():
    """Get transit directions"""
    if not google_client:
        return jsonify({
            'error': 'Google Maps API not configured',
            'message': 'Add your API key to config.py'
        }), 503
    
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    
    if not origin or not destination:
        return jsonify({'error': 'Both origin and destination required'}), 400
    
    result = google_client.get_transit_directions(
        origin=origin,
        destination=destination,
        alternatives=True
    )
    
    if not result or not result.get('routes'):
        return jsonify({'error': 'No routes found'}), 404
    
    return jsonify({
        'success': True,
        'origin': origin,
        'destination': destination,
        'routes': result['routes']
    })


@app.route('/api/nearby-stations')
def get_nearby_stations():
    """Find nearby transit stations"""
    if not google_client:
        return jsonify({'error': 'Google Maps API not configured'}), 503
    
    location = request.args.get('location')
    radius = request.args.get('radius', 1000, type=int)
    
    if not location:
        return jsonify({'error': 'Location required'}), 400
    
    stations = google_client.find_nearby_transit_stations(location, radius)
    
    if stations is None:
        return jsonify({'error': 'Failed to find stations'}), 503
    
    return jsonify({
        'success': True,
        'count': len(stations),
        'stations': stations
    })


@app.route('/map')
def map_view():
    """Live vehicle map view"""
    return render_template('map.html')


@app.route('/routes')
def routes_view():
    """Route planner view"""
    return render_template('routes.html',
                         google_maps_configured=google_client is not None,
                         common_locations=COMMON_LOCATIONS)


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/route/<route_id>')
def route_detail(route_id):
    """Route detail page"""
    route_info = route_details_client.get_route_info(route_id)
    return render_template('route_detail.html', route=route_info)


@app.route('/api/route/<route_id>')
def get_route_detail(route_id):
    """Get detailed route information"""
    route_info = route_details_client.get_route_info(route_id)
    
    # Add current vehicles on this route
    vehicles = rtd_client.get_vehicle_positions()
    if vehicles:
        route_vehicles = [v for v in vehicles if v['route_id'] == route_id.upper()]
        route_info['current_vehicles'] = route_vehicles
        route_info['vehicle_count'] = len(route_vehicles)
    else:
        route_info['current_vehicles'] = []
        route_info['vehicle_count'] = 0
    
    return jsonify(route_info)


@app.route('/api/routes/all')
def get_all_routes():
    """Get summary of all routes"""
    routes = route_details_client.get_all_routes_summary()
    return jsonify({'routes': routes})


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 RTD Transit Web App Starting")
    print("="*80)
    print("\n🌐 Access the web interface at:")
    print("   http://localhost:5000")
    print("\n📱 Features:")
    print("   • Real-time vehicle tracking")
    print("   • Interactive map view")
    if google_client:
        print("   • Transit directions")
        print("   • Station finder")
    else:
        print("   ⚠️  Google Maps features disabled (configure API key)")
    print("\n" + "="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)


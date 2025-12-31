"""
Example configuration file - Copy this to config.py and add your API keys
"""

import os

# Google Maps API Configuration
# Get your API key from: https://console.cloud.google.com/google/maps-apis
# Required APIs: Directions API, Places API, Geocoding API
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'YOUR_GOOGLE_MAPS_API_KEY_HERE')

# RTD Configuration (no API key needed for public feeds)
RTD_STATIC_FEED_URL = "https://www.rtd-denver.com/google_sync/google_transit.zip"
RTD_REALTIME_BASE_URL = "https://www.rtd-denver.com/google_sync/"

# Common Denver locations for quick testing
COMMON_LOCATIONS = {
    'union_station': 'Union Station, Denver, CO',
    'capitol': 'Colorado State Capitol, Denver, CO',
    'airport': 'Denver International Airport, CO',
    'coors_field': 'Coors Field, Denver, CO',
    'cherry_creek': 'Cherry Creek Shopping Center, Denver, CO',
    'downtown': 'Downtown Denver, CO',
    '16th_street_mall': '16th Street Mall, Denver, CO'
}

def validate_google_api_key():
    """Check if Google Maps API key is configured"""
    if GOOGLE_MAPS_API_KEY == 'YOUR_GOOGLE_MAPS_API_KEY_HERE':
        print("\n⚠️  Warning: Google Maps API key not configured!")
        print("   Set your API key in config.py or as an environment variable:")
        print("   export GOOGLE_MAPS_API_KEY='your-api-key-here'")
        print("   Get a key at: https://console.cloud.google.com/google/maps-apis\n")
        return False
    return True


# Use this file for writing helper functions that can be used throughout the project.
# If this file grows too large or disorganized, it may be helpful to break it up into multiple files, like date_helpers, string_helpers, etc.
import googlemaps
from dotenv import load_dotenv
import os
"""
Examples of Helper Functions:
- Convert datetime objects to user readable formats or specific timezones.
- Format currency, percentages, or other numerical data.
- Template filters (be sure to not duplicate Django's preexisting and vast libraries here, though).
- Image resizing
"""


def load_api_key():
    """Loads the API key from an environment variable."""
    load_dotenv()
    return os.environ.get("API_KEY")

def initialize_gmaps(api_key):
    """Initializes the Google Maps client with an API key."""
    return googlemaps.Client(api_key)

def search_places_nearby(gmaps, location, radius=1000, place_type='tourist_attraction'):
    """Searches for places nearby a given location.
    
    Args:
        gmaps: Initialized Google Maps client.
        location: A tuple of (latitude, longitude).
        radius: Search radius in meters.
        place_type: Type of place to search for.
        
    Returns:
        A list of places found near the location.
    """
    places_result = gmaps.places_nearby(location=location, radius=radius, type=place_type)
    if places_result['results']:
        return True, places_result['results']
    else:
        return False, "No places found."

def geocode_location(gmaps, location_name):
    """Geocodes a location name to latitude and longitude coordinates.
    
    Args:
        gmaps: Initialized Google Maps client.
        location_name: The name of the location to geocode.
        
    Returns:
        A tuple of (latitude, longitude) coordinates if successful, None otherwise.
    """
    geocode_result = gmaps.geocode(location_name)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return True, (location['lat'], location['lng'])
    else:
        return False, f"Could not geocode the location: {location_name}"
    
def process_and_return_places(places):
    """Extracts places and their vicinities and returns them as a list of tuples."""
    extracted_places = []
    for place in places:
        # Extract the name and vicinity and store them in a tuple
        extracted_place = (place['name'], place['vicinity'])
        extracted_places.append(extracted_place)
    return extracted_places


def get_recommendation(destination):
    api_key = load_api_key()
    if not api_key:
        return False, "API key is not set. Please check your .env file."

    gmaps = initialize_gmaps(api_key)
    success, location_or_error = geocode_location(gmaps, destination)
    if not success:
        return False, location_or_error  # Ensure returning a tuple

    success, places_or_error = search_places_nearby(gmaps, location_or_error)
    if not success:
        return False, places_or_error  # Ensure returning a tuple

    search_results = process_and_return_places(places_or_error)
    return True, search_results



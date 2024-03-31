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

def search_places_nearby(gmaps, location, radius=5000, place_type='shopping_mall'):
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
    

def process_and_return_places(places, api_key):
    """Extracts details from places and returns them as a list of dictionaries, each representing an Activity."""
    extracted_activities = []
    for place in places:
        # Initialize an empty dictionary for the current place
        activity = {}

        # Basic place details
        activity['title'] = place.get('name', '')
        activity['editSummary'] = 'Summary of ' + place.get('name', '')
        activity['name'] = place.get('name', '')
        activity['address'] = place.get('vicinity', '')
        activity['placeID'] = place.get('place_id', '')

        # Handling photos - only storing the first photo reference
        photos = place.get('photos', [])
        if photos:
            photo_reference = photos[0].get('photo_reference', '')
            if photo_reference:
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                activity['photos'] = photo_url
            else:
                activity['photos'] = ''
        else:
            activity['photos'] = ''

        # Open hours
        open_now = place.get('opening_hours', {}).get('open_now', False)
        activity['openHour'] = 'Open Now' if open_now else 'Closed'
        # Assuming 'periods' needs specific processing or fetching from elsewhere as it's not directly available in this input
        activity['periods'] = 'Not Available'

        # Rating and URL link
        activity['rating'] = str(place.get('rating', ''))
        # Assuming 'urlLink' requires generating or fetching from elsewhere as it's not directly available in this input
        activity['urlLink'] = 'URL Placeholder'

        activity['businessStatus'] = str(place.get('business_status', ''))
        # Location details
        location = place.get('geometry', {}).get('location', {})
        viewport = place.get('geometry', {}).get('viewport', {})
        activity['location'] = f"{location.get('lat', '')}, {location.get('lng', '')}"
        activity['lat'] = str(location.get('lat', ''))
        activity['lng'] = str(location.get('lng', ''))
        activity['northeast'] = f"{viewport.get('northeast', {}).get('lat', '')}, {viewport.get('northeast', {}).get('lng', '')}"
        activity['southwest'] = f"{viewport.get('southwest', {}).get('lat', '')}, {viewport.get('southwest', {}).get('lng', '')}"

        # Additional fields
        activity['website'] = 'Website Placeholder'  # Assuming this needs fetching or a placeholder for now

        # Append the activity dictionary to the list
        extracted_activities.append(activity)

    
    return extracted_activities



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

    search_results = process_and_return_places(places_or_error, api_key)
    return True, search_results



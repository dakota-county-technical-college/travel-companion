# Use this file for writing helper functions that can be used throughout the project.
# If this file grows too large or disorganized, it may be helpful to break it up into multiple files, like date_helpers, string_helpers, etc.

"""
Examples of Helper Functions:
- Convert datetime objects to user readable formats or specific timezones.
- Format currency, percentages, or other numerical data.
- Template filters (be sure to not duplicate Django's preexisting and vast libraries here, though).
- Image resizing
"""

import googlemaps
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, time
from random import shuffle
from itineraries.models import Itinerary, Day, Activity

"""
Examples of Helper Functions:
- Convert datetime objects to user readable formats or specific timezones.
- Format currency, percentages, or other numerical data.
- Template filters (be sure to not duplicate Django's preexisting and vast libraries here, though).
- Image resizing
"""


def load_google_maps_api_key():
    """Loads the API key from an environment variable."""
    load_dotenv()
    return os.environ.get("GOOGLE_MAPS_API_KEY")


def initialize_gmaps(google_maps_api_key):
    """Initializes the Google Maps client with an API key."""
    return googlemaps.Client(google_maps_api_key)


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


def process_and_return_places(places, google_maps_api_key):
    """_summary_

    Args:
        places (list): All the places returned from googles api
        google_maps_api_key (str): api key needed to interact with gmaps

    Returns:
        list of dictinaries: Extracted places. appendied to a list
    """
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
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={google_maps_api_key}"
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
        activity[
            'northeast'] = f"{viewport.get('northeast', {}).get('lat', '')}, {viewport.get('northeast', {}).get('lng', '')}"
        activity[
            'southwest'] = f"{viewport.get('southwest', {}).get('lat', '')}, {viewport.get('southwest', {}).get('lng', '')}"

        # Additional fields
        activity['website'] = 'Website Placeholder'  # Assuming this needs fetching or a placeholder for now

        # Append the activity dictionary to the list
        extracted_activities.append(activity)

    return extracted_activities


def calculate_total_days(start_date, end_date):
    """_summary_

    Args:
        start_date (datetime.date): Trip start date
        end_date (datetime.date): Trip end date

    Returns:
        _type_: _description_
    """
    return (end_date - start_date).days + 1


def fetch_places(gmaps, location, total_days):
    """_summary_

    Args:
        gmaps (Client): gmaps client
        location (tuple): long and lat of a location
        total_days (int): total number of days for the trip

    Returns:
        list: A list of all the places of type tourist_attraction and restaurant
    """
    initial_radius = 5000  # Initial search radius in meters
    radius_increment = 5000  # Radius increment for each attempt
    max_attempts = 3  # Maximum expansion attempts
    activities_per_day = 3
    food_places_per_day = 2
    total_activities_needed = total_days * activities_per_day
    total_food_places_needed = total_days * food_places_per_day

    activities = []
    food_places = []

    current_radius = initial_radius
    attempts = 0

    while attempts < max_attempts and (
            len(activities) < total_activities_needed or len(food_places) < total_food_places_needed):
        if len(activities) < total_activities_needed:
            attractions_result = gmaps.places_nearby(
                location=location, radius=current_radius, type='tourist_attraction', language="en"
            )
            activities.extend(attractions_result.get('results', [])[:total_activities_needed - len(activities)])

        if len(food_places) < total_food_places_needed:
            restaurant_result = gmaps.places_nearby(
                location=location, radius=current_radius, type='restaurant', language="en"
            )
            food_places.extend(restaurant_result.get('results', [])[:total_food_places_needed - len(food_places)])

        current_radius += radius_increment
        attempts += 1

    # Combine and shuffle the places to mix activities and food places

    combined_places = activities + food_places
    shuffle(combined_places)

    return combined_places[:total_activities_needed + total_food_places_needed]


def generate_itinerary(gmaps, location, start_date, end_date, google_maps_api_key):
    """_summary_

    Args:
        gmaps (Client): google maps python library
        location (tuple): The lat, long of a destination a user would like an itinerary made for
        start_date (datetime.date): start day of the trip
        end_date (datetime.date): end day of the trip
        google_maps_api_key (str): the api key needed to use gmaps

    Returns:
        dic: itineraries 
    """
    total_days = calculate_total_days(start_date, end_date)
    combined_places = fetch_places(gmaps, location, total_days)
    processed_places = process_and_return_places(combined_places, google_maps_api_key)

    # Distribute places across days
    itinerary = distribute_places_to_days(start_date, end_date, processed_places)

    return itinerary


def distribute_places_to_days(start_date, end_date, places):
    """
    Distributes places evenly across the trip days.

    Args:
        start_date (datetime.date): Trip start date.
        end_date (datetime.date): Trip end date.
        places (list): List of processed places including a mix of activities and food places.

    Returns:
        dict: Places split across days of the trip
    """
    total_days = calculate_total_days(start_date, end_date)
    itinerary = {}
    places_per_day = len(places) // total_days

    for day in range(total_days):
        date = start_date + timedelta(days=day)
        day_places = places[day * places_per_day:(day + 1) * places_per_day]

        itinerary[date] = {
            "places": day_places
        }

    return itinerary


def get_recommendation(destination, start_date, end_date):
    """_summary_

    Args:
        destination (str): Name of destination user would like itinerary generated for
        start_date (datetime.date): start date of the trip
        end_date (datetime.date): end date of the trip

    Returns:
        dict: activities for making up the itinerary
    """
    google_maps_api_key = load_google_maps_api_key()
    if not google_maps_api_key:
        return False, "API key is not set. Please check your .env file."

    gmaps = initialize_gmaps(google_maps_api_key)
    success, location_or_error = geocode_location(gmaps, destination)
    if not success:
        return False, location_or_error  # Ensure returning a tuple

    location = location_or_error
    itinerary = generate_itinerary(gmaps, location, start_date, end_date, google_maps_api_key)

    # Check if the itinerary has entries; if not, return a message indicating no places were found
    if not itinerary:
        return False, "No places found for the given dates. Please try different dates or another destination."

    return True, itinerary


def save_itinerary(user, destination, start_date, end_date, travelers, activities_data):
    """_summary_

    Args:
        user (UserObject): Signed in user object
        destination (str): name of the destination
        start_date (date): when the trip begins
        end_date (date): when the trip ends
        travelers (int): number of party
        activities_data (dict): activities recommended for the itinerary
    """
    # Step 1: Save itinerary
    new_itinerary = Itinerary(
        user=user,
        title=f"My Trip to {destination}",
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        description=f"A trip to {destination} with {travelers} travelers.",
        num_travelers=travelers
    )
    new_itinerary.save()

    # Get number of days for the trip
    num_days = (end_date - start_date).days + 1
    # Activities start at 8 am each day
    initial_start_time = time(8, 0)

    # Step 2: Save each day and its activities
    for day_index in range(num_days):
        current_date = start_date + timedelta(days=day_index)

        activities_for_day = activities_data.get(current_date, {}).get('places', [])

        # Save the day
        new_day = Day(
            itinerary=new_itinerary,
            date=current_date,
            day_number=day_index + 1
        )
        new_day.save()

        # Reset start time for each day
        start_time = initial_start_time

        # Step 3: Save activities for the day
        for activity_data in activities_for_day:
            save_activity(new_day, activity_data, start_time)


def save_activity(day, activity_data, start_time):
    """_summary_

    Args:
        day (day): The specific day
        activity_data (dic): activities set for the day
        start_time (datetime): when activity begins

    Returns:
        datetime: when the activity ends
    """
    # setting activities 2 hours 30 mins apart
    duration = timedelta(hours=2, minutes=30)
    end_time = (datetime.combine(datetime.today(), start_time) + duration).time()

    # Create and save an Activity instance
    new_activity = Activity(
        day=day,
        title=activity_data.get('title', ''),
        start_time=start_time,
        end_time=end_time,
        editSummary=activity_data.get('editSummary', ''),
        name=activity_data.get('name', ''),
        address=activity_data.get('address', ''),
        placeID=activity_data.get('placeID', ''),
        photos=activity_data.get('photos', ''),
        openHour=activity_data.get('openHour', ''),
        periods=activity_data.get('periods', ''),
        businessStatus=activity_data.get('businessStatus', ''),
        rating=activity_data.get('rating', ''),
        urlLink=activity_data.get('urlLink', ''),
        location=activity_data.get('location', ''),
        northeast=activity_data.get('northeast', ''),
        southwest=activity_data.get('southwest', ''),
        website=activity_data.get('website', ''),
    )
    new_activity.save()

    return end_time
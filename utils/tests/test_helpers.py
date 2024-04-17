import pytest
from unittest.mock import patch, Mock
from datetime import datetime, date
from utils.helpers import load_google_maps_api_key, initialize_gmaps, process_and_return_places, search_places_nearby, \
    calculate_total_days, geocode_location, get_recommendation


@pytest.mark.django_db
def test_load_google_maps_api_key():
    with patch('os.environ.get') as mock_get:
        mock_get.return_value = 'fake-api-key'
        assert load_google_maps_api_key() == 'fake-api-key'


@pytest.mark.django_db
def test_initialize_gmaps():
    with patch('googlemaps.Client') as mock_client:
        # Setup
        api_key = 'fake-api-key'

        # Call the function with the fake API key
        initialize_gmaps(api_key)

        # Assert that the Google Maps Client is initialized with the correct API key
        mock_client.assert_called_once_with(api_key)


@pytest.mark.django_db
def test_search_places_nearby():
    with patch('googlemaps.Client') as mock_client:
        # Setup: Create a mock Google Maps client
        mock_gmaps_client = Mock()
        mock_client.return_value = mock_gmaps_client

        # Define the mock response for places_nearby
        fake_response = {
            'results': [{'name': 'Test Mall', 'place_id': '1234'}]
        }
        mock_gmaps_client.places_nearby.return_value = fake_response

        # Parameters for the function
        location = (34.052235, -118.243683)  # Example location (Los Angeles, CA)
        radius = 1000
        place_type = 'shopping_mall'

        # Call the function
        success, results = search_places_nearby(mock_gmaps_client, location, radius, place_type)

        # Check if the function returns the correct results
        assert success == True
        assert results == fake_response['results']

        # Assert that the places_nearby was called with correct parameters
        mock_gmaps_client.places_nearby.assert_called_once_with(location=location, radius=radius, type=place_type)


@pytest.mark.django_db
def test_search_places_nearby_no_results():
    with patch('googlemaps.Client') as mock_client:
        # Setup: Create a mock Google Maps client
        mock_gmaps_client = Mock()
        mock_client.return_value = mock_gmaps_client

        # Define the mock response for places_nearby with empty results
        fake_response = {
            'results': []  # No places found
        }
        mock_gmaps_client.places_nearby.return_value = fake_response

        # Parameters for the function
        location = (34.052235, -118.243683)  # Example location (Los Angeles, CA)
        radius = 1000
        place_type = 'shopping_mall'

        # Call the function
        success, message = search_places_nearby(mock_gmaps_client, location, radius, place_type)

        # Check if the function returns the correct message for no results
        assert success == False
        assert message == "No places found."

        # Assert that the places_nearby was called with correct parameters
        mock_gmaps_client.places_nearby.assert_called_once_with(location=location, radius=radius, type=place_type)


@pytest.mark.django_db
def test_geocode_location_success():
    with patch('googlemaps.Client') as mock_client:
        # Setup: Create a mock Google Maps client
        mock_gmaps_client = Mock()
        mock_client.return_value = mock_gmaps_client

        # Define the mock response for successful geocoding
        fake_geocode_result = [{
            'geometry': {
                'location': {'lat': 34.052235, 'lng': -118.243683}
            }
        }]
        mock_gmaps_client.geocode.return_value = fake_geocode_result

        # Parameters for the function
        location_name = "Los Angeles, CA"

        # Call the function
        success, coordinates = geocode_location(mock_gmaps_client, location_name)

        # Check if the function returns the correct coordinates
        assert success == True
        assert coordinates == (34.052235, -118.243683)

        # Assert that the geocode method was called with the correct parameters
        mock_gmaps_client.geocode.assert_called_once_with(location_name)


@pytest.mark.django_db
def test_geocode_location_failure():
    with patch('googlemaps.Client') as mock_client:
        # Setup: Create a mock Google Maps client
        mock_gmaps_client = Mock()
        mock_client.return_value = mock_gmaps_client

        # Define the mock response for unsuccessful geocoding
        fake_geocode_result = []  # Empty result indicates failure to geocode
        mock_gmaps_client.geocode.return_value = fake_geocode_result

        # Parameters for the function
        location_name = "Nonexistent Place"

        # Call the function
        success, error_message = geocode_location(mock_gmaps_client, location_name)

        # Check if the function returns the correct error message
        assert success == False
        assert error_message == f"Could not geocode the location: {location_name}"

        # Assert that the geocode method was called with the correct parameters
        mock_gmaps_client.geocode.assert_called_once_with(location_name)


@pytest.mark.django_db
def test_process_and_return_places_success():
    # Mock data as would be returned by the Google Maps API
    mock_places = [
        {
            'name': 'Eiffel Tower',
            'vicinity': 'Champ de Mars, 5 Avenue Anatole France, Paris',
            'place_id': '12345',
            'photos': [{'photo_reference': 'abcdef'}],
            'opening_hours': {'open_now': True},
            'geometry': {
                'location': {'lat': 48.8588443, 'lng': 2.2943506},
                'viewport': {
                    'northeast': {'lat': 48.8596934, 'lng': 2.2954995},
                    'southwest': {'lat': 48.8580434, 'lng': 2.2931507}
                }
            },
            'rating': 4.7,
            'business_status': 'OPERATIONAL'
        }
    ]
    google_maps_api_key = 'fake-api-key'

    # Expected result formatted by the function
    expected = [{
        'title': 'Eiffel Tower',
        'editSummary': 'Summary of Eiffel Tower',
        'name': 'Eiffel Tower',
        'address': 'Champ de Mars, 5 Avenue Anatole France, Paris',
        'placeID': '12345',
        'photos': f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=abcdef&key=fake-api-key",
        'openHour': 'Open Now',
        'periods': 'Not Available',
        'rating': '4.7',
        'urlLink': 'URL Placeholder',
        'businessStatus': 'OPERATIONAL',
        'location': '48.8588443, 2.2943506',
        'lat': '48.8588443',
        'lng': '2.2943506',
        'northeast': '48.8596934, 2.2954995',
        'southwest': '48.8580434, 2.2931507',
        'website': 'Website Placeholder'
    }]

    # Call the function with mock data
    results = process_and_return_places(mock_places, google_maps_api_key)

    # Assert the processed data matches the expected output
    assert results == expected


def test_calculate_total_days():
    # Define the test cases with start dates, end dates, and expected results
    test_cases = [
        (date(2024, 1, 1), date(2024, 1, 1), 1),  # Same day
        (date(2024, 1, 1), date(2024, 1, 2), 2),  # Two consecutive days
        (date(2024, 1, 1), date(2024, 1, 10), 10),  # Ten days span
        (date(2023, 12, 25), date(2024, 1, 1), 8)  # Cross-year span
    ]

    # Test each case
    for start_date, end_date, expected_days in test_cases:
        # Calculate days using the function
        calculated_days = calculate_total_days(start_date, end_date)

        # Assert the calculated days match the expected result
        assert calculated_days == expected_days, f"Failed for start_date: {start_date} and end_date: {end_date}"

import pytest
from unittest.mock import patch, Mock
from datetime import datetime, date, time, timedelta
from itineraries.models import Activity, Day, Itinerary
from utils.helpers import distribute_places_to_days, fetch_places, generate_itinerary, load_google_maps_api_key, \
    initialize_gmaps, process_and_return_places, save_activity, save_itinerary, search_places_nearby, \
    calculate_total_days, geocode_location, get_recommendation
from django.contrib.auth import get_user_model


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


@pytest.mark.django_db
def test_fetch_places():
    with patch('googlemaps.Client') as mock_client:
        # Setup a mock Google Maps client
        mock_gmaps_client = Mock()
        mock_client.return_value = mock_gmaps_client

        # Define initial and subsequent mock responses for places_nearby
        initial_response_attractions = {
            'results': [{'name': 'Attraction A'}, {'name': 'Attraction B'}]
        }
        subsequent_response_attractions = {
            'results': [{'name': 'Attraction C'}] * 10
            # Assume multiple identical results to simulate sufficient responses
        }
        initial_response_restaurants = {
            'results': [{'name': 'Restaurant X'}, {'name': 'Restaurant Y'}]
        }
        subsequent_response_restaurants = {
            'results': [{'name': 'Restaurant Z'}] * 10  # Same here for restaurants
        }

        # Define how the mock client should behave on method calls
        # Use a longer side_effect list or a cyclic iterator if the number of calls is variable
        mock_gmaps_client.places_nearby.side_effect = [
                                                          initial_response_attractions,
                                                          initial_response_restaurants,
                                                          subsequent_response_attractions,
                                                          subsequent_response_restaurants,
                                                      ] * 10  # Repeat the pattern to ensure enough responses

        # Parameters for the function call
        location = (34.052235, -118.243683)
        total_days = 2  # For simplicity, assuming we need 3 activities and 2 food places per day

        # Call the function
        results = fetch_places(mock_gmaps_client, location, total_days)

        # Assert expected behavior and results
        expected_activities_needed = 6  # 2 days * 3 activities per day
        expected_food_places_needed = 4  # 2 days * 2 food places per day
        assert len(results) == expected_activities_needed + expected_food_places_needed
        assert {'name': 'Attraction A'} in results
        assert {'name': 'Restaurant Y'} in results
        assert {'name': 'Attraction C'} in results  # From subsequent calls

        # Ensure the client was called with correct parameters and the radius was incremented
        assert mock_gmaps_client.places_nearby.call_count >= 4


@pytest.mark.django_db
def test_generate_itinerary():
    with patch('utils.helpers.calculate_total_days') as mock_calculate_days, \
            patch('utils.helpers.fetch_places') as mock_fetch_places, \
            patch('utils.helpers.process_and_return_places') as mock_process_places, \
            patch('utils.helpers.distribute_places_to_days') as mock_distribute_days:
        # Mock returns
        mock_calculate_days.return_value = 3  # Let's assume the trip is 3 days
        mock_fetch_places.return_value = ['Place1', 'Place2', 'Place3']  # Mocked place data
        mock_process_places.return_value = [{'name': 'Place1'}, {'name': 'Place2'},
                                            {'name': 'Place3'}]  # Processed place data
        mock_distribute_days.return_value = {
            date(2023, 4, 1): {'places': [{'name': 'Place1'}]},
            date(2023, 4, 2): {'places': [{'name': 'Place2'}]},
            date(2023, 4, 3): {'places': [{'name': 'Place3'}]}
        }  # Mocked itinerary structure

        # Parameters for function call
        gmaps = Mock()  # Mock Google Maps client
        location = (34.052235, -118.243683)
        start_date = date(2023, 4, 1)
        end_date = date(2023, 4, 3)
        google_maps_api_key = 'fake-api-key'

        # Call the function
        result = generate_itinerary(gmaps, location, start_date, end_date, google_maps_api_key)

        # Asserts
        assert result == {
            date(2023, 4, 1): {'places': [{'name': 'Place1'}]},
            date(2023, 4, 2): {'places': [{'name': 'Place2'}]},
            date(2023, 4, 3): {'places': [{'name': 'Place3'}]}
        }

        # Ensure the mocked functions were called with the correct parameters
        mock_calculate_days.assert_called_once_with(start_date, end_date)
        mock_fetch_places.assert_called_once_with(gmaps, location, 3)
        mock_process_places.assert_called_once_with(['Place1', 'Place2', 'Place3'], google_maps_api_key)
        mock_distribute_days.assert_called_once_with(start_date, end_date,
                                                     [{'name': 'Place1'}, {'name': 'Place2'}, {'name': 'Place3'}])


def test_distribute_places_to_days():
    # Given dates and places
    start_date = date(2023, 4, 1)
    end_date = date(2023, 4, 3)  # Total 3 days
    places = [
        {'name': 'Place1'}, {'name': 'Place2'}, {'name': 'Place3'},
        {'name': 'Place4'}, {'name': 'Place5'}, {'name': 'Place6'}
    ]

    # Call the function
    result = distribute_places_to_days(start_date, end_date, places)

    # Expected results: Each day should get 2 places
    expected_days = (end_date - start_date).days + 1
    expected_distribution = {
        (start_date + timedelta(days=i)): {'places': places[2 * i:2 * i + 2]}
        for i in range(expected_days)
    }

    # Assertions
    assert len(result) == expected_days, "The number of days in the result should match the range of dates"
    for key, value in expected_distribution.items():
        assert result[key] == value, f"Places on {key} did not match expected distribution"

    # Check if all days are covered and the distribution is correct
    for day, data in result.items():
        assert len(data['places']) == 2, f"Each day should have 2 places, but {day} has {len(data['places'])}"
        assert day in expected_distribution, f"Unexpected day {day} in results"


@pytest.mark.django_db
def test_get_recommendation_success():
    with patch('utils.helpers.load_google_maps_api_key') as mock_load_api_key, \
            patch('utils.helpers.initialize_gmaps') as mock_init_gmaps, \
            patch('utils.helpers.geocode_location') as mock_geocode, \
            patch('utils.helpers.generate_itinerary') as mock_generate_itinerary:
        # Setup mocks
        mock_load_api_key.return_value = 'fake-api-key'
        mock_gmaps_client = Mock()
        mock_init_gmaps.return_value = mock_gmaps_client
        mock_geocode.return_value = (True, (34.052235, -118.243683))  # Simulating successful geocode
        mock_generate_itinerary.return_value = {'itinerary': 'details'}

        # Call function
        success, result = get_recommendation('Los Angeles', date(2023, 4, 1), date(2023, 4, 3))

        # Assertions
        assert success is True
        assert result == {'itinerary': 'details'}

        # Ensure the mocks were called as expected
        mock_load_api_key.assert_called_once()
        mock_init_gmaps.assert_called_once_with('fake-api-key')
        mock_geocode.assert_called_once_with(mock_gmaps_client, 'Los Angeles')
        mock_generate_itinerary.assert_called_once()


@pytest.mark.django_db
def test_get_recommendation_no_api_key():
    with patch('utils.helpers.load_google_maps_api_key') as mock_load_api_key:
        # Setup mocks for failure scenario
        mock_load_api_key.return_value = None  # Simulating missing API key

        # Call function
        success, result = get_recommendation('Los Angeles', date(2023, 4, 1), date(2023, 4, 3))

        # Assertions
        assert success is False
        assert "API key is not set" in result


User = get_user_model()


@pytest.mark.django_db
def test_save_itinerary():
    # Create a test user
    user = User.objects.create(username='testuser', password='password')

    # Sample data to save
    destination = "Paris"
    start_date = date(2023, 4, 1)
    end_date = date(2023, 4, 3)
    travelers = 2
    activities_data = {
        date(2023, 4, 1): {'places': [{'title': 'Eiffel Tower', 'start_time': datetime.now()}]},
        date(2023, 4, 2): {'places': [{'title': 'Louvre Museum', 'start_time': datetime.now()}]},
        date(2023, 4, 3): {'places': [{'title': 'Notre Dame', 'start_time': datetime.now()}]}
    }

    # Call the function under test
    save_itinerary(user, destination, start_date, end_date, travelers, activities_data)

    # Assertions to verify database entries
    itinerary = Itinerary.objects.get(user=user, destination=destination)
    assert itinerary.title == f"My Trip to {destination}"
    assert itinerary.num_travelers == travelers

    # Check days and activities saved correctly
    days = Day.objects.filter(itinerary=itinerary).order_by('date')
    assert days.count() == 3
    for day, data in zip(days, activities_data.values()):
        activities = Activity.objects.filter(day=day)
        assert activities.count() == 1
        assert activities.first().title == data['places'][0]['title']

    # Optionally, cleanup if not using transactional tests
    user.delete()


@pytest.mark.django_db
def test_save_activity():
    # Create test data for Itinerary and Day
    user = User.objects.create(username='testuser', password='password')
    itinerary = Itinerary.objects.create(
        user=user,
        title="Test Trip to Paris",
        destination="Paris",
        start_date=date(2023, 4, 1),
        end_date=date(2023, 4, 3),
        description="A wonderful trip.",
        num_travelers=2
    )
    day = Day.objects.create(
        itinerary=itinerary,
        date=date(2023, 4, 1),
        day_number=1
    )

    # Activity data
    activity_data = {
        'title': 'Visit Eiffel Tower',
        'editSummary': 'Tour of the Eiffel Tower',
        'name': 'Eiffel Tower',
        'address': 'Champ de Mars, 5 Avenue Anatole France, Paris',
        'placeID': '123',
        'photos': '',
        'openHour': 'Open Now',
        'periods': '9:00 AM - 5:00 PM',
        'businessStatus': 'OPERATIONAL',
        'rating': '4.5',
        'urlLink': '',
        'location': '48.8588443, 2.2943506',
        'northeast': '',
        'southwest': '',
        'website': ''
    }
    start_time = time(9, 0)

    # Call the function under test
    end_time = save_activity(day, activity_data, start_time)

    # Assertions to verify database entries
    activity = Activity.objects.get(day=day)
    assert activity.title == 'Visit Eiffel Tower'
    assert activity.start_time == time(9, 0)
    assert activity.end_time == (datetime.combine(date.min, start_time) + timedelta(hours=2, minutes=30)).time()

    # Clean-up
    user.delete()

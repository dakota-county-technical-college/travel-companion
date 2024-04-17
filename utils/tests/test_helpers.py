import pytest
from unittest.mock import patch, Mock
from datetime import datetime, date
from utils.helpers import load_google_maps_api_key, calculate_total_days, geocode_location, get_recommendation

@pytest.mark.django_db
def test_load_google_maps_api_key():
    with patch('os.environ.get') as mock_get:
        mock_get.return_value = 'fake-api-key'
        assert load_google_maps_api_key() == 'fake-api-key'
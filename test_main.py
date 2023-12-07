import requests
from unittest.mock import patch
import json
import pytest
from main import get_openshift_versions

@pytest.mark.parametrize("channel, version, expected_versions", [
    ('fast', '4.14', ['4.14.1', '4.14.2', '4.14.3']),  # Adjust the expected versions accordingly
    ('stable', '4.12', ['4.12.1', '4.12.2', '4.12.3']),  # Adjust the expected versions accordingly
    ('candidate', '4.10', ['4.10.1', '4.10.2', '4.10.3'])  # Adjust the expected versions accordingly
])
def test_get_openshift_versions(channel, version, expected_versions):
    # Mock the response from the requests.get method
    mock_response = requests.models.Response()
    mock_response.status_code = 200
    mock_response.json = lambda: {
        'nodes': [
            {'version': '4.14.1'},
            {'version': '4.14.2'},
            {'version': '4.14.3'},
            {'version': '4.12.1'},
            {'version': '4.12.2'},
            {'version': '4.12.3'},
            {'version': '4.10.1'},
            {'version': '4.10.2'},
            {'version': '4.10.3'},
        ]
    }

    with patch('requests.get', return_value=mock_response):
        result = get_openshift_versions(channel, version)

    assert result == expected_versions

if __name__ == '__main__':
    pytest.main()

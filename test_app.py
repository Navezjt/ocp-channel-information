import subprocess
import requests
import time
import threading
import pytest
from app import app

# Set up the Flask app in a separate thread
flask_thread = threading.Thread(target=app.run, kwargs={'debug': True, 'host': '127.0.0.1', 'port': 5000})
flask_thread.start()
time.sleep(2)  # Allow some time for the Flask app to start

# Base URL for API requests
base_url = 'http://127.0.0.1:5000/api/upgrades_info'

def test_api_upgrades_info():
    try:
        # Test API endpoint with valid parameters
        response = requests.get(f'{base_url}?channel=fast&version=4.14')

        # Print response details for debugging
        print(f'Response status code: {response.status_code}')
        print(f'Response content: {response.content}')

        # Check if the response status code is 200
        assert response.status_code == 200, f'Actual status code: {response.status_code}'

        # Check if actual versions are a subset of expected versions
        actual_versions = set(response.json())
        expected_versions = {'4.14.4', '4.14.1', '4.14.5', '4.14.3', '4.14.2', '4.14.0'}
        assert actual_versions.issubset(expected_versions)
        assert expected_versions.issubset(actual_versions)

        # Test API endpoint with missing parameters
        response = requests.get(base_url)
        assert response.status_code == 400, f'Actual status code: {response.status_code}'

        # Test API endpoint with invalid parameters
        response = requests.get(f'{base_url}?channel=invalid&version=4.14')
        assert response.status_code == 400, f'Actual status code: {response.status_code}'

    finally:
        # Stop the Flask app after the test
        flask_thread.join(timeout=1)  # Wait for the thread to finish

def test_command_line():
    # Test command line with valid parameters
    result = subprocess.run(['python', 'app.py', '--channel', 'fast', '--version', '4.14'], capture_output=True, text=True)
    output_lines = result.stdout.split('\n')

    # Check if actual versions are a subset of expected versions
    actual_versions = set(output_lines[:-1])  # Exclude the last empty string
    expected_versions = {'4.14.4', '4.14.1', '4.14.5', '4.14.3', '4.14.2', '4.14.0'}
    assert actual_versions.issubset(expected_versions)
    assert expected_versions.issubset(actual_versions)

    # Test command line with missing parameters
    result = subprocess.run(['python', 'app.py'], capture_output=True, text=True)
    assert result.returncode != 0  # Non-zero return code indicates an error

# Stop the Flask app thread after the test
flask_thread.join(timeout=1)

# Ensure the Flask app thread is stopped
assert not flask_thread.is_alive(), "Flask app thread is still running"

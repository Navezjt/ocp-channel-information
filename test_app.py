import subprocess
import requests
import time
import threading
import pytest
from app import app

flask_thread = threading.Thread(target=app.run, kwargs={'debug': True, 'host': '127.0.0.1', 'port': 5000})
flask_thread.start()
time.sleep(2)  #Flask sleep 

base_url = 'http://127.0.0.1:5000/api/upgrades_info'

def test_api_upgrades_info():
    try:
        response = requests.get(f'{base_url}?channel=fast&version=4.14')

        print(f'Response status code: {response.status_code}')
        print(f'Response content: {response.content}')

        assert response.status_code == 200, f'Actual status code: {response.status_code}'

        actual_versions = set(response.json())
        expected_versions = {'4.14.4', '4.14.1', '4.14.5', '4.14.3', '4.14.2', '4.14.0'}
        assert actual_versions.issubset(expected_versions)
        assert expected_versions.issubset(actual_versions)

        response = requests.get(base_url)
        assert response.status_code == 400, f'Actual status code: {response.status_code}'
        response = requests.get(f'{base_url}?channel=invalid&version=4.14')
        assert response.status_code == 400, f'Actual status code: {response.status_code}'

    finally:
        flask_thread.join(timeout=1)

def test_command_line():
    result = subprocess.run(['python', 'app.py', '--channel', 'fast', '--version', '4.14'], capture_output=True, text=True)
    output_lines = result.stdout.split('\n')

    actual_versions = set(output_lines[:-1])  
    expected_versions = {'4.14.4', '4.14.1', '4.14.5', '4.14.3', '4.14.2', '4.14.0'}
    assert actual_versions.issubset(expected_versions)
    assert expected_versions.issubset(actual_versions)

    result = subprocess.run(['python', 'app.py'], capture_output=True, text=True)
    assert result.returncode != 0  

flask_thread.join(timeout=1)

assert not flask_thread.is_alive(), "Flask app thread is still running"
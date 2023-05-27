from base import word_url, user_url
import time
import requests
import pytest

def test_health_check_endpoint():
    

    for _ in range(24):  # 24 hours
        response_1 = requests.get(word_url + '/health')
        assert response_1.status_code == 200, f"Endpoint {word_url} returned {response_1.status_code} status code."

        response_2 = requests.get(user_url + '/health')
        assert response_2.status_code == 200, f"Endpoint {user_url} returned {response_2.status_code} status code."

        time.sleep(3600)  # Pause for 1 hour (3600 seconds) before the next check


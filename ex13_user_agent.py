import requests
import pytest

url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

expected_list = [
    ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
    ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1', {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
    ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0', {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),
    ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1', {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})
]
@pytest.mark.parametrize('expected', expected_list)
def test_check_user_agent(expected):
    user_agent, expected_value = expected
    platform_expected = expected_value["platform"]
    device_expected = expected_value["device"]
    browser_expected = expected_value["browser"]

    response = requests.get(url, headers={"User-Agent": user_agent})

    platform_from_response = response.json()["platform"]
    browser_from_response = response.json()["browser"]
    device_from_response = response.json()["device"]

    assert platform_from_response == platform_expected, f"Platform unexpected for user agent '{user_agent}'"
    assert device_from_response == device_expected, f"Device unexpected for user agent '{user_agent}'"
    assert browser_from_response == browser_expected, f"Browser unexpected for user agent '{user_agent}'"

import requests

def test_homework_header():
    url = "https://playground.learnqa.ru/api/homework_header"

    response = requests.get(url)
    headers = response.headers
    print(headers)

    expected_header = 'x-secret-homework-header'
    header_value = headers.get(expected_header)

    assert expected_header in headers, f"No header '{expected_header}' in headers"
    assert headers[expected_header] == header_value, f"Unexpected value of header: '{headers[expected_header]}'"
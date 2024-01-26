import requests

def test_homework_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    cookies = dict(response.cookies)
    print(cookies)

    cookie_value = response.cookies.get('HomeWork')
    assert cookies == {'HomeWork': cookie_value}, f"Unexpected cookie: {cookies}"
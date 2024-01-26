import requests

def test_homework_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    cookies = dict(response.cookies)
    print(cookies)

    cookie_value = response.cookies.get('HomeWork')
    assert 'HomeWork' in cookies, f"There is no cookie 'Homework' in cookies"
    assert cookies == {'HomeWork': cookie_value}, f"Unexpected cookie value: {cookies}"
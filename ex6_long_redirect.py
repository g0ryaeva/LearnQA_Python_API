import requests

url = "https://playground.learnqa.ru/api/long_redirect"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers, allow_redirects=True)

print(len(response.history))
print(response.url)

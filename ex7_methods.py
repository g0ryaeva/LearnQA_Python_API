import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
types = ["get", "post", "put", "delete"]
methods = {"get": "GET", "post": "POST", "put": "PUT", "delete": "DELETE"}

# 1
print("part 1")
response = requests.get(url)
print(response.status_code, response.text, '\n')

# 2
print("part 2")
response = requests.head(url)
print(response.status_code, response.text, '\n')

# 3
print("part 3")
response = requests.get(url, params={"method": "GET"})
print(response.status_code, response.text, '\n')
success = response.text

# 4
print('part 4')
for type in types:
    for method, param in methods.items():
        if type == "get":
            response = requests.request(type, url, params={"method": param})
        else:
            response = requests.request(type, url, data={"method": param})

        if (type == method and response.text != success or
                type != method and response.text == success):
            print(type, param)

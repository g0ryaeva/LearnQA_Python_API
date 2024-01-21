import requests
import json
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# create
response_create_task = requests.get(url)
result_create = json.loads(response_create_task.text)
token = result_create["token"]
timeout = result_create["seconds"]

# check status
response_check = requests.get(url, params={"token": token})
result_check = json.loads(response_check.text)
status = result_check["status"]
print(f"Status after creation: {status}")

# wait timeout
time.sleep(timeout)

# check status & result
response_check_result = requests.get(url, params={"token": token})
result_check_result = json.loads(response_check_result.text)
status = result_check_result["status"]
result = result_check_result["result"]

print(f"Status after waiting: {status}")
print(f"Result: {result}")
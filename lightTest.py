# we are going to use the LIFX api to control the lights
# c07545722e208de4d94b41b0d7497aaebe7b0cfc73c32bf5d76241b54fd37b39
import requests
from time import sleep

token = "c07545722e208de4d94b41b0d7497aaebe7b0cfc73c32bf5d76241b54fd37b39"

headers = {
    "Authorization": "Bearer %s" %token ,
    }

payload = {
    "power": "on",
    }

response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)
print(response.text)
sleep(5)
payload = {
    "power": "off",
    }
response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)
print(response.text)


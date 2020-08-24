from requests import request
from json import loads
payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}


def black_frog(origin, destination, collateral):
    URL = f"https://red-frog.org/api/public/v1/calculator/black/?origin={origin}&destination={destination}&collateral={collateral}"
    response = request("GET", URL, headers=headers, data=payload)
    return loads(response.content)


def red_frog(origin, destination):
    URL = f"https://red-frog.org/api/public/v1/calculator/red/?origin={origin}&destination={destination}"
    response = request("GET", URL, headers=headers, data=payload)
    return loads(response.content)
 
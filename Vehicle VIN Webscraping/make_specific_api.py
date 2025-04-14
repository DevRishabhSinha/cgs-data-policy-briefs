import requests
import json


def fetch_honda_data():
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetMakeForManufacturer/honda?format=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"error": "Failed to fetch data for Honda"}


# Fetch and save Honda data
honda_data = fetch_honda_data()

with open('honda_data.json', 'w') as f:
    json.dump(honda_data, f)

print("Honda data saved to 'honda_data.json'")

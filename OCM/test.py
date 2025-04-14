import requests
import csv

# Define multiple center points and radii that cover the United States.
# For example, choose a few strategically placed "centers" to cover the map.
# This can be adjusted as needed. The larger the radius, the fewer queries needed,
# but also consider API limits and performance.
locations = [
    {'latitude': 37.0902, 'longitude': -95.7129, 'distance': 1600},  # Central US
    {'latitude': 40.7128, 'longitude': -74.0060, 'distance': 800},   # Northeast (NYC)
    {'latitude': 34.0522, 'longitude': -118.2437, 'distance': 800},  # West Coast (LA)
    {'latitude': 47.6062, 'longitude': -122.3321, 'distance': 800},  # Northwest (Seattle)
    {'latitude': 29.7604, 'longitude': -95.3698, 'distance': 800},   # South (Houston)
    {'latitude': 41.8781, 'longitude': -87.6298, 'distance': 800}    # Midwest (Chicago)
]

url = 'https://api.openchargemap.io/v3/poi/'
api_key = 'c0b81fcf-a1b0-4923-8cdd-aaeed7bb06b0'

# To avoid duplicates, use a dictionary keyed by unique station ID
all_stations = {}

for loc in locations:
    params = {
        'output': 'json',
        'latitude': loc['latitude'],
        'longitude': loc['longitude'],
        'distance': loc['distance'],
        'maxresults': 100000,
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for station in data:
            station_id = station.get('ID')
            if station_id not in all_stations:
                all_stations[station_id] = station
    else:
        print(f"Failed to fetch data for coordinates {loc['latitude']}, {loc['longitude']}: {response.status_code}")

# Once all queries are done, write the combined data to CSV
with open('ev_charging_stations_usa.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow([
        'LocationName', 'Address', 'City', 'State', 'Postcode', 'Country',
        'Latitude', 'Longitude', 'PlugTypes', 'PowerKW', 'Quantity',
        'NetworkProvider', 'UsageType', 'Status', 'LastVerified', 'Comments'
    ])
    
    # Process and write each unique charging station's details
    for station in all_stations.values():
        address_info = station.get('AddressInfo', {})
        connections = station.get('Connections', [])
        usage_type = station.get('UsageType', {})
        status_type = station.get('StatusType', {})
        operator_info = station.get('OperatorInfo', {})

        location_name = address_info.get('Title', 'N/A')
        address = address_info.get('AddressLine1', 'N/A')
        city = address_info.get('Town', 'N/A')
        state = address_info.get('StateOrProvince', 'N/A')
        postcode = address_info.get('Postcode', 'N/A')
        country = address_info.get('Country', {}).get('Title', 'N/A')
        latitude = address_info.get('Latitude', 'N/A')
        longitude = address_info.get('Longitude', 'N/A')
        plug_types = ', '.join([conn.get('ConnectionType', {}).get('Title', 'N/A') for conn in connections])
        power_kw = ', '.join([str(conn.get('PowerKW', 'N/A')) for conn in connections])
        quantity = sum(conn.get('Quantity', 0) or 0 for conn in connections)
        network_provider = operator_info.get('Title', 'N/A') if operator_info else 'N/A'
        usage_type_title = usage_type.get('Title', 'N/A') if usage_type else 'N/A'
        status = status_type.get('Title', 'N/A') if status_type else 'N/A'
        last_verified = station.get('DateLastVerified', 'N/A')
        comments = station.get('GeneralComments', 'N/A')

        writer.writerow([
            location_name, address, city, state, postcode, country,
            latitude, longitude, plug_types, power_kw, quantity,
            network_provider, usage_type_title, status, last_verified, comments
        ])

print("Data saved to 'ev_charging_stations_usa.csv'")

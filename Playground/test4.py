import pandas as pd
import requests
import time
from tqdm import tqdm

# Load data
df = pd.read_csv('locations.csv')

# Function to get EV station details using Open Charge Map API
def get_ocm_data(lat, lng, api_key):
    url = f"https://api.openchargemap.io/v3/poi/?output=json&latitude={lat}&longitude={lng}&distance=0.5&distanceunit=KM&maxresults=1&compact=true&verbose=false&key={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data and len(data) > 0:
            station = data[0]
            
            # Extract useful information
            operator = station.get('OperatorInfo', {}).get('Title')
            connections = station.get('Connections', [])
            
            station_type = 'ev charger'
            if operator and 'tesla' in operator.lower():
                station_type = 'tesla supercharger'
            
            # Get additional details about the station
            details = {
                'station_type': station_type,
                'operator': operator,
                'connection_types': [conn.get('ConnectionType', {}).get('Title') for conn in connections],
                'power_levels': [conn.get('PowerKW') for conn in connections]
            }
            
            return details
        
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Alternative: Use Mapbox's ChargeFinder API (newer option)
def get_mapbox_data(lat, lng, api_key):
    url = f"https://api.mapbox.com/charging/v1/stations?lat={lat}&lon={lng}&limit=1&access_token={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('features') and len(data['features']) > 0:
            station = data['features'][0]['properties']
            
            return {
                'station_type': 'ev charger',
                'operator': station.get('network'),
                'connection_types': station.get('connectors', []),
                'amenities': station.get('amenities', [])
            }
        
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Set your API key
api_key = "695d1a07-ae3b-4515-84b0-9f063718ce4a"  # Open Charge Map offers free API keys

# Focus on suspected EV locations
ev_locations = df[
    ((df['Level1Ports'] > 0) | (df['Level2Ports'] > 0) | (df['Level3Ports'] > 0)) &
    (df['location_type'].isna())
]

for idx, row in tqdm(ev_locations.iterrows(), total=len(ev_locations)):
    if pd.notna(row['Lat']) and pd.notna(row['Long']):
        station_data = get_ocm_data(row['Lat'], row['Long'], api_key)
        
        if station_data:
            df.at[idx, 'location_type'] = station_data['station_type']
            # Store additional details if needed
            # df.at[idx, 'operator'] = station_data['operator']
        
        # Respect API limits
        time.sleep(0.5)

# Save results
df.to_csv('locations_with_types_ev_specific.csv', index=False)
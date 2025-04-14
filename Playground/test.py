import pandas as pd
import requests
import time
from tqdm import tqdm

# Load the CSV data
df = pd.read_csv('locations.csv')

def get_place_type_from_osm(lat, lng):
    """Get place type information from OpenStreetMap Nominatim API"""
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=18"
    
    # Important: Add a user agent to comply with OSM usage policy
    headers = {
        'User-Agent': 'LocationCategorization/1.0 (your@email.com)'
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Extract relevant information
        place_type = None
        if 'amenity' in data.get('address', {}):
            place_type = data['address']['amenity']
        elif 'shop' in data.get('address', {}):
            place_type = f"shop: {data['address']['shop']}"
        elif 'tourism' in data.get('address', {}):
            place_type = f"tourism: {data['address']['tourism']}"
        elif 'leisure' in data.get('address', {}):
            place_type = f"leisure: {data['address']['leisure']}"
        elif 'office' in data.get('address', {}):
            place_type = f"office: {data['address']['office']}"
        else:
            # Look at the full response to find any type information
            for key in data.get('address', {}):
                if key in ['amenity', 'building', 'shop', 'office', 'tourism', 'leisure']:
                    place_type = f"{key}: {data['address'][key]}"
                    break
        
        return place_type or 'Unknown'
    
    except Exception as e:
        return 'Error'

# Process data with progress bar
# Note: OSM has strict rate limits (1 request/sec), so this will take ~5.5 hours for 20,000 records
sample_size = len(df)  # For demonstration, limit to 100 records
sample_df = df.sample(sample_size)

print(f"Processing {sample_size} locations with OSM API...")
for idx, row in tqdm(sample_df.iterrows(), total=sample_size):
    sample_df.at[idx, 'OSMPlaceType'] = get_place_type_from_osm(row['Lat'], row['Long'])
    time.sleep(1)  # Required by OSM terms of use
    
# Save results
sample_df.to_csv('osm_categorized_sample1.csv', index=False)

import json

# Load GeoJSON from file
with open('Metals_Industrial_Parks.geojson', 'r') as file:
    geojson_data = json.load(file)

# Define the keys to check for non-zero values
metal_keys = [
    "Nickel", "Aluminum", "Copper", "Palm Oil", "Iron and Steel"
]

# Filter features to keep only those with at least one non-zero value in the specified metal keys
filtered_features = [
    feature for feature in geojson_data['features']
    if any(feature['properties'][key] != 0 for key in metal_keys)
]

# Update the features in the GeoJSON data
geojson_data['features'] = filtered_features

# Save the filtered GeoJSON to a new file
with open('Filtered_Metals_Industrial_Parks.geojson', 'w') as file:
    json.dump(geojson_data, file, indent=4)

print("Filtered GeoJSON has been saved as 'Filtered_Metals_Industrial_Parks.geojson'")

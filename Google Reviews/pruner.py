import pandas as pd

# Load the datasets with "N/A" preserved as a string
data1 = pd.read_csv('output_reviews256789012345678901final.csv', dtype=str, keep_default_na=False, na_values=[])
data2 = pd.read_csv('input8.csv', dtype=str, keep_default_na=False, na_values=[])

# Define the columns to match
matching_columns = [
    "StationID", "LocationName", "Address", "City", "State", "Postcode", "Country", "Latitude", "Longitude"
]

# Create a duplicate of data2 before deletion
data2_duplicate = data2.copy()

# Perform the filtering to remove rows that exist in data1
merged = data2_duplicate.merge(data1[matching_columns], on=matching_columns, how='left', indicator=True)
data2_filtered = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

# Save the filtered dataset
output_file = "input9.csv"
data2_filtered.to_csv(output_file, index=False)

print(f"Filtered data saved to {output_file}")

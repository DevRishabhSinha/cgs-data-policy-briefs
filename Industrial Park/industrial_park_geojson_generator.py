import pandas as pd
import geopandas as gpd

# Load the data
df = pd.read_csv('/Users/a12345/Desktop/ip1010.csv')
df["Latitude"] = pd.to_numeric(df["Latitude"], errors='coerce')
df["Longitude"] = pd.to_numeric(df["Longitude"], errors='coerce')

# Define the column groups
basic_columns = ["Industrial Park Name", "Manager", "Size (ha)", "Location", "Latitude", "Longitude", "Age", "Main Industry", "Sources"]
energy_columns = ["Industrial Park Name","Electricity Provider", "PLN", "Captive Coal Power Plant", "Captive Gas Power Plant", "Bioenergy", "Solar", "Hydropower", "Electricity Provider Unclear",  "Electricity Capacity Notes", "Electricity Capacity (MW)", "GEM", "Latitude", "Longitude", "Sources"]
status_columns = ["Industrial Park Name","Status", "Status Notes", "Latitude", "Longitude", "Sources"]
foreign_involvement_columns = ["Industrial Park Name","Foreign Founder or Manager", "Tenants",  "Foreign Tenants", "Foreign Company Involvement Notes", "Latitude", "Longitude", "Sources", "Taiwan_founder", "France_founder", "China_founder", "South Korea_founder", "Singapore_founder", "Canada_founder", "Germany_founder", "Malaysia_founder", "Japan_founder", "Taiwan_tenant", "South Korea_tenant", "United States_tenant", "Seychelles_tenant", "Germany_tenant", "Myanmar_tenant", "Turkey_tenant", "Lebanon_tenant", "Australia_tenant", "United Kingdom_tenant", "Denmark_tenant", "Phillipines_tenant", "Malaysia_tenant", "China_tenant", "Singapore_tenant", "Netherlands_tenant", "India_tenant", "Canada_tenant", "Japan_tenant", "England_tenant", "Thailand_tenant", "Austria_tenant"]
renewable_energy_columns = ["Industrial Park Name","Specific mention of renewable energy", "Mention of environmentally friendly practices", "Electric Vehicle (Production Mentioned)", "Latitude", "Longitude", "Sources"]
dispute_columns = ["Industrial Park Name", "Location", "Latitude", "Longitude", "Legal dispute with Indonesian government", "Legal dispute with a company", "Dispute with local residents", "Workers' rights dispute", "Environmental Impact", "Land Acquisition Issues", "Dispute Explanations", "Sources"]
metals_columns = ["Industrial Park Name", "Latitude", "Longitude", "Nickel", "Aluminum", "Copper", "Palm Oil", "Iron and Steel", "Sources"]
# Function to create and save a GeoDataFrame
def create_and_save_geojson(df, columns, filename):
    subset_df = df[columns].dropna(subset=["Latitude", "Longitude"])
    gdf = gpd.GeoDataFrame(subset_df, geometry=gpd.points_from_xy(subset_df.Longitude, subset_df.Latitude))
    gdf.to_file(filename, driver='GeoJSON')

# Create and save GeoJSON for each group
create_and_save_geojson(df, basic_columns, "Basic_Industrial_Parks.geojson")
create_and_save_geojson(df, energy_columns, "Energy_Industrial_Parks.geojson")
create_and_save_geojson(df, status_columns, "Status_Industrial_Parks.geojson")
create_and_save_geojson(df, foreign_involvement_columns, "Foreign_Involvement_Industrial_Parks.geojson")
# create_and_save_geojson(df, renewable_energy_columns, "Renewable_Energy_Industrial_Parks.geojson")
create_and_save_geojson(df, dispute_columns, "Dispute_Industrial_Parks.geojson")
create_and_save_geojson(df, metals_columns, "Metals_Industrial_Parks.geojson")



import folium
import pandas as pd

df = pd.read_csv('indus_parks_complete_columns_oct24.csv')
df["Latitude"] = pd.to_numeric(df["Latitude"], errors='coerce')
df["Longitude"] = pd.to_numeric(df["Longitude"], errors='coerce')

m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=6)

icon_image = "ipark.png"
icon = folium.CustomIcon(icon_image, icon_size=(32, 32))

for _, park in df.dropna(subset=["Latitude", "Longitude"]).iterrows():
    tooltip_content = ""
    for column in df.columns:
        tooltip_content += "{}: {}<br>".format(column, park[column])

    if park["Latitude"] >= 0:
        marker_color = "blue"
    else:
        marker_color = "red"

    folium.Marker(
        [park["Latitude"], park["Longitude"]],
        tooltip=tooltip_content,
        icon=folium.Icon(color=marker_color)
    ).add_to(m)

m.save("map_only.html")

import geopandas as gpd

# Convert DataFrame to GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

# Save to GeoJSON
gdf.to_file("Industrial_Parks.geojson", driver='GeoJSON')
import folium
import pandas as pd

df = pd.read_csv('Industrial_Parks.csv')
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=6)
icon_image = "ipark.png"
for _, park in df.iterrows():
    tooltip_content = """
    <strong>{}</strong><br>
    """.format(park["Industrial Park Name"])

    for column in df.columns:
        tooltip_content += "{}: {}<br>".format(column, park[column])

    # Color code based on latitude (North = blue, South = red)
    if park["Latitude"] >= 0:
        marker_color = "blue"
    else:
        marker_color = "red"

    folium.Marker(
        [park["Latitude"], park["Longitude"]],
        tooltip=tooltip_content,
        icon=folium.Icon(color=marker_color )
    ).add_to(m)

m.save("industrial_parks_map.html")

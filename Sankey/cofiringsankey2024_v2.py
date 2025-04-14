import pandas as pd
import plotly.graph_objects as go

# Step 1: Load the data
df = pd.read_excel('cofiringsankey2024.xlsx', index_col=0)

# Step 2: Prepare data for the Sankey diagram
sources, targets, values, labels = [], [], [], []
# Updated color palette for a more professional look
color_palette = {
    'Biomass power plants ': '#4E79A7',  # Blue
    'Processing mills': '#F28E2B',  # Orange
    'Exports': '#E15759',  # Red
    'Animal feed': '#76B7B2',  # Cyan
    'Fertilizer': '#59A14F',  # Green
    'Lumber industry': '#EDC948',  # Yellow
    'Household fuel': '#B07AA1',  # Purple
    'Industrial fuel': '#FF9DA7',  # Pink
    'Existing co-firing': '#9C755F',  # Brown
    'Biomass power plants': '#BAB0AC',  # Grey
    'Misc.': '#AF7AA1',  # Lavender
}

label_list = df.index.tolist() + df.columns[:-1].tolist()
labels.extend(label_list)
for i, source in enumerate(df.index):
    for j, target in enumerate(df.columns[:-1]):
        value = df.loc[source, target]
        if value > 0:
            sources.append(i)
            targets.append(len(df.index) + j)
            values.append(value)

# Step 3: Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color="blue"  # Consider setting individual colors if needed
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=[color_palette[label_list[t].split('\t')[0]] for t in targets]  # Assign colors
    ))])

# Improved layout settings for higher quality output
fig.update_layout(
    height=400,  # Adjust size as needed
    width=600
)

# Note: Adjust 'height' and 'width' for better quality/resolution.

# Step 4: Export the diagram
# For higher quality, consider exporting to SVG or PNG and converting externally.
fig.write_image("sankey_diagram.png", scale=2)  # Increase scale for higher resolution

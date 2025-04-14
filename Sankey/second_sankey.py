import pandas as pd
import plotly.graph_objects as go

# Read the CSV file
df = pd.read_csv('/Users/a12345/Downloads/IP_foreign_for_sankey.csv')
print(df.columns
      )
# Prepare the data
all_nodes = df['IP Name'].tolist() + df['Province'].unique().tolist() + df['Foreign Founder or Manager'].unique().tolist()
node_dict = {node: i for i, node in enumerate(all_nodes)}

# Create lists to define source, target, and value for each link
sources = []
targets = []
values = []

# Adding links from IP Names to Provinces
for _, row in df.iterrows():
    sources.append(node_dict[row['IP Name']])
    targets.append(node_dict[row['Province']])
    values.append(1)  # Assuming equal weight for each link

# Adding links from Provinces to Foreign Founder or Manager
for _, row in df.iterrows():
    sources.append(node_dict[row['Province']])
    targets.append(node_dict[row['Foreign Founder or Manager']])
    values.append(1)  # Assuming equal weight for each link

# Create the Sankey plot
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=all_nodes,
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
    ))])

fig.update_layout(title_text='Sankey Diagram', font_size=10)
fig.show()

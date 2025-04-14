import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# Load your data
df_sankey = pd.read_excel('cofiringsankey2024 (1).xlsx')

# Process your DataFrame into a source-target format as before...
# Now we process the dataframe into a source-target-value format suitable for creating a Sankey diagram.

# Initialize an empty list to store the processed data
sankey_data = []

# Loop through each row in the dataframe
for index, row in df_sankey.iterrows():
    # Extract the feedstock name which is the source node for all flows
    feedstock = row['Feedstock']

    # Loop through each column (excluding 'Feedstock' and 'Total avail (MJ)')
    for target in df_sankey.columns[1:-1]:  # -2 to skip 'Unnamed: 11' and 'Total avail (MJ)'
        value = row[target]
        # Append the source, target, and value to the sankey_data list if value is non-zero
        if value > 0:
            sankey_data.append({
                'source': feedstock,
                'target': target,
                'value': value
            })

    # Add the 'Total remaining' flow
    total_remaining = row['Total avail (MJ)']
    if total_remaining > 0:
        sankey_data.append({
            'source': feedstock,
            'target': 'Total Remaining',
            'value': total_remaining
        })

# Create a dataframe from the sankey_data list
df_sankey_processed = pd.DataFrame(sankey_data)

# Display the processed dataframe
df_sankey_processed.head()

# Create a directed graph
G = nx.DiGraph()

# Add nodes with the label as the node name
for label in df_sankey_processed['source'].unique():
    G.add_node(label, demand = -1)  # You can set demands if you want to reflect quantities
for label in df_sankey_processed['target'].unique():
    G.add_node(label, demand = 1)

# Add edges with weights
for index, row in df_sankey_processed.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['value'])

# Position nodes using networkx's layout algorithms or manually
pos = nx.spring_layout(G)  # This is a simple layout, you may want to place nodes manually

# Draw the nodes
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500)

# Draw the edges
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=30, edge_color='gray', width=2)

# Draw the labels
nx.draw_networkx_labels(G, pos, font_size=15)

# Remove axes
plt.axis('off')

# Set margins and show plot
plt.margins(0.1, 0.1)
plt.show()

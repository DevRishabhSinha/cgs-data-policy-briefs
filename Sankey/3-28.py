import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

df_sankey = pd.read_excel('cofiringsankey2024 (1).xlsx')

sankey_data = []
for index, row in df_sankey.iterrows():
    for col in df_sankey.columns:
        if col not in ['Feedstock', 'Total avail (MJ)']:
            sankey_data.append({'source': row['Feedstock'], 'target': col, 'value': row[col]})
        elif col == 'Total avail (MJ)':
            sankey_data.append({'source': row['Feedstock'], 'target': 'Total Remaining', 'value': row[col]})

df_sankey_formatted = pd.DataFrame(sankey_data)
df_sankey_formatted = df_sankey_formatted[df_sankey_formatted['value'] > 0]

unique_nodes = pd.concat([df_sankey_formatted['source'], df_sankey_formatted['target']]).unique()
label_list = unique_nodes.tolist()

biomass_color_map = {
    'Bagasse': 'rgba(38,88,92, 0.8)',
    'PKS': 'rgba(215,3,1, 0.8)',
    'EFB': 'rgba(230,144,2, 0.8)',
    'Rubber': 'rgba(112,61,1, 0.8)',
    'Rice straw': 'rgba(214,214,158, 0.8)',
    'Rice husk': 'rgba(231,207,43, 0.8)',
    'MSW': 'rgba(157,157,156, 0.8)',
    'Wood waste': 'rgba(128,162,3, 0.8)'
}

color_list = [biomass_color_map[feedstock] for feedstock in df_sankey['Feedstock']]
link_color_list = ['rgba(184,199,148, 0.8)' if target == 'Total Remaining' else 'rgba(128,128,128,0.5)' for source, target in zip(df_sankey_formatted['source'], df_sankey_formatted['target'])]

source_indices = [label_list.index(src) for src in df_sankey_formatted['source']]
target_indices = [label_list.index(tgt) for tgt in df_sankey_formatted['target']]

node_x_positions = [10 if i < len(df_sankey['Feedstock']) else 10 for i in range(len(label_list))]

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=label_list,
        color=color_list,
        x=node_x_positions
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=df_sankey_formatted['value'].tolist(),
        color=link_color_list
    )
)])

fig.update_layout(
    title_text="Cofiring Feedstocks to Total Remaining",
    font=dict(size=14, color='black', family='Arial Black'),
    # Adjust plot margins to prevent cutting off labels
    margin=dict(l=100, r=100, t=100, b=100)
)

fig.show()
pio.write_image(fig, 'sankey_diagram.svg')

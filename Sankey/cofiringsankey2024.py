import pandas as pd
import plotly.graph_objects as go

df = pd.read_excel('cofiringsankey2024.xlsx', index_col=0)


sources, targets, values, labels = [], [], [], []
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

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color='black'
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=[color_palette[label_list[t].split('\t')[0]] for t in targets]  # Assign colors
    ))])
fig.update_layout(font=dict(family="Trade Gothic Next Condensed Font", size=12, color='black'))
fig.write_image("sankey_diagram.eps")
import pandas as pd
import plotly.graph_objects as go

df = pd.read_excel('/Users/a12345/Downloads/IP_foreign_for_sankey (1).xlsx')

source = []
target = []
value = []
link_colors = []

ip_index_map = {ip: i for i, ip in enumerate(df['IP Name'].unique())}
province_index_map = {province: i + len(ip_index_map) for i, province in enumerate(df['Province'].unique())}
founder_index_map = {founder: i + len(ip_index_map) + len(province_index_map) for i, founder in enumerate(df['Foreign Founder or Manager'].unique())}

for _, row in df.iterrows():
    ip_to_province_value = row['Size (ha)']
    province_to_founder_value = row['Size (ha)']

    source.append(ip_index_map[row['IP Name']])
    target.append(province_index_map[row['Province']])
    value.append(ip_to_province_value)

    source.append(province_index_map[row['Province']])
    target.append(founder_index_map[row['Foreign Founder or Manager']])
    value.append(province_to_founder_value)

    link_color = 'rgba(255,0,0,0.8)' if row['Foreign Founder or Manager'] == 'China' else 'rgba(50,50,50,0.3)'
    link_colors.extend([link_color, link_color])

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=list(ip_index_map.keys()) + list(province_index_map.keys()) + list(founder_index_map.keys()),
        color=['rgba(0,0,0,0.2)'] * (len(ip_index_map) + len(province_index_map) + len(founder_index_map))
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=link_colors
    )
)])

fig.update_layout(title_text='Sankey Diagram Highlighting IPs with a Foreign Founder or Manager from China', font_size=10)

fig.write_html('sankey_diagram.html')

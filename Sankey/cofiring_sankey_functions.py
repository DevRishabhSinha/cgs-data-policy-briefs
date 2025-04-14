# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 14:32:48 2023

@author: Aboli Dahiwadkar
@purpose: Define necessary functions used for all Sankey diagrams
"""

# Tutorial for how to use plotly to create Sankey diagram
# https://youtu.be/yyVwvBUFRwY

# %% Importing libraries & data

import pandas as pd
import plotly.graph_objects as go

import plotly

# print(px)
plotly.io.renderers.default = 'browser'


# %% Creating function for getting source, target, & value columns. Specify how value is determined

# df is the dataframe you are generating from the dataset file
# source_name refers to the name of the column in the dataframe you want to use

# If the value is determined by summing the quantities in the value col, then sum_bool is True
# If the value is determined by counting the occurances of a value in a col, then sum is False & count_bool is True

def getting_data(df, source_name, target_name, value_name, sum_bool, count_bool):
    if sum_bool:
        df_temp = df.groupby([source_name, target_name])[value_name].sum().reset_index()
    elif count_bool:
        df_temp = df.groupby([source_name, target_name])[value_name].count().reset_index()
    else:
        print("Try another method\n")
        return

    return df_temp


# %% Creating a [source, target, value] dataframe (used for single-flow diagrams)

def simple_sankey(df_temp):
    df_temp.columns = ["source", "target", "value"]
    print(df_temp.head())

    return df_temp


# %% Creating a dataframe with linked temp dataframes (used for multi-flow diagrams)

def complex_sankey(*df_temp):
    for x in df_temp:
        x.columns = ["source", "target", "value"]
        print(x.head())

    links = pd.concat(df_temp, axis=0)

    return links


# %% Colors for Sankey

def feedstock_color():
    """
    Names = ["Rice husk", "Rice straw", "Palm kernel shell", "Empty fruit bunches",
             "Pulp and paper", "Wood waste", "Sugarcane", "MSW", "Rubber"]

    color_dict = {"Rice husk":"rgb(205,173,0)",
                  "Rice straw":"rgb(238,233,191)",
                  "Palm kernel shell":"rgb(205,38,38)",
                  "Empty fruit bunches":"rgb(205,92,92)",
                  "Pulp and paper":"rgb(221,160,221)",
                  "Wood waste":"rgb(102,205,0)",
                  "Sugarcane":"rgb(141,182,205)",
                  "MSW":"rgb(204,204,204)",
                  "Rubber":"rgb(139,69,19)"}

    in_order_color_array = ['rgb(205,173,0)', 'rgb(238,233,191)', 'rgb(205,38,38)',
                   'rgb(205,92,92)', 'rgb(221,160,221)', 'rgb(102,205,0)',
                   'rgb(141,182,205)', 'rgb(204,204,204)', 'rgb(139,69,19)']

    actual_color_array = ['rgb(238,233,191)', 'rgb(205,92,92)', 'rgb(139,69,19)',
                          'rgb(204,204,204)', 'rgb(205,173,0)', 'rgb(141,182,205)',
                          'rgb(221,160,221)', 'rgb(205,38,38)', 'rgb(102,205,0)']
    """

    in_order_test = ['gold', 'beige', 'crimson', 'indianred', 'plum', 'olive',
                     'lightsteelblue', 'lightslategrey', 'chocolate']

    actual_test = ['indianred', 'silver', 'firebrick', 'plum', 'gold',
                   'beige', 'saddlebrown', 'cadetblue', 'forestgreen']

    return actual_test


def make_fig(sankey_df, title):
    unique_source_target = list(pd.unique(sankey_df[["source", "target"]].values.ravel("K")))

    mapping_dict = {k: v for v, k in enumerate(unique_source_target)}

    sankey_df["source"] = sankey_df["source"].map(mapping_dict)
    sankey_df["target"] = sankey_df["target"].map(mapping_dict)

    sankey_dict = sankey_df.to_dict(orient="list")

    node_colors = feedstock_color()

    link_colors = ['rgba(128, 128, 128, 0.5)'] * len(sankey_dict['source'])

    total_remaining_index = mapping_dict.get("Total remaining", None)

    if total_remaining_index is not None:
        link_colors = [
            'rgba(240,104,65, 1)' if target == total_remaining_index else link_color
            for target, link_color in zip(sankey_dict['target'], link_colors)
        ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0),  # Set width to 0 to remove the border
            label=unique_source_target,
            color=node_colors

        ),
        link=dict(
            source=sankey_dict["source"],
            target=sankey_dict["target"],
            value=sankey_dict["value"],
            color=link_colors
        )
    )]
    )

    fig.update_layout(
        title_text=title,
        paper_bgcolor='rgba(0,0,0,0)',  # set background to transparent
        plot_bgcolor='rgba(0,0,0,0)',  # set background to transparent
        font=dict(color="black")  # set font properties for node labels
    )

    fig.show()


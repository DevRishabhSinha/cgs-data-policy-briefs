# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 14:46:02 2023

@author: Aboli Dahiwadkar
@purpose: Create Sankey diagram for co-firing paper
"""

#%% Importing libraries & data

import pandas as pd
import plotly
# print(px)
plotly.io.renderers.default='browser'

#import sankey_functions

# Import the Sankey functions created in sankey_functions.py
from cofiring_sankey_functions import getting_data, simple_sankey, complex_sankey, make_fig


#%% Creating diagram showing how feedstock is directed

df = pd.read_excel('/Users/a12345/Desktop/cofiringfeedstocksforsankey.xlsx',
                              sheet_name='Sankey')

# View all the column names in the dataframe
print(df.columns)

feedstock_data = getting_data(df, "Feedstock", "Use", "Value (billion MJ)", True, False)
make_fig (simple_sankey(feedstock_data), "Cofiring feedstocks")
"""
Extract insights from combining US census data and the Washington Post's database
on deaths by police in the United States.
                                  Pct_People_Below_Poverty_Level
"""

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
"""### Read the Data"""

below_poverty_level = pd.read_csv('csv\Pct_People_Below_Poverty_Level.csv', encoding='cp1252')

""" Data Exploration & Cleaning """
print(below_poverty_level.shape)
print(below_poverty_level.columns)

""" Check for Duplicates """
# print(below_poverty_level.duplicated().sum)  # False

""" Check for NaN Values """
# print(below_poverty_level.isna().sum())  # 0
indexLevel = below_poverty_level[(below_poverty_level['poverty_rate'] == '-')].index
below_poverty_level.drop(indexLevel, inplace=True)

below_poverty_level['poverty_rate'] = below_poverty_level['poverty_rate'].astype(float)

# print(below_poverty_level)

below_poverty_level_state = below_poverty_level.groupby('Geographic Area')['poverty_rate'].mean()

print(below_poverty_level_state)
#
plt.figure()
map_plot = px.choropleth(locations=below_poverty_level_state.index,
                         title='Percentage People Below Poverty Level', color=below_poverty_level_state.values,
                         locationmode='USA-states',
                         color_continuous_scale='hot_r',
                         hover_name=below_poverty_level_state.index,
                         scope="usa",
                         labels={"color": "Pct Below Poverty Level"},
                         )
map_plot.show()
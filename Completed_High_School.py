"""
Extract insights from combining US census data and the Washington Post's database
on deaths by police in the United States.
                                  Percent over 25 Completed High School
"""

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
"""### Read the Data"""

completed_HS = pd.read_csv('csv\Pct_Over_25_Completed_High_School.csv', encoding='cp1252')

""" Data Exploration & Cleaning """
# print(completed_HS.shape)
# print(completed_HS.columns)

""" Check for Duplicates """
# print(completed_HS.duplicated().sum)  # False

""" Check for NaN Values """
# print(completed_HS.isna().sum()) # 0
indexComplete = completed_HS[(completed_HS['percent_completed_hs'] == '-')].index
completed_HS.drop(indexComplete, inplace=True)
completed_HS['percent_completed_hs'] = completed_HS['percent_completed_hs'].astype(float)

#

completed_HS_state = completed_HS.groupby('Geographic Area')['percent_completed_hs'].mean()


plt.figure()
map_plot = px.choropleth(locations=completed_HS_state.index,
                         title='Percent over 25 Completed High School', color=completed_HS_state.values,
                         locationmode='USA-states',
                         color_continuous_scale='hot_r',
                         hover_name=completed_HS_state.index,
                         scope="usa",
                         labels={"color": "Pct Completed High School Average"}
                         )
map_plot.show()
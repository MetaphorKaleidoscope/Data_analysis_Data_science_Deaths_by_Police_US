"""
Extract insights from combining US census data and the Washington Post's database
on deaths by police in the United States.
                                  Media income data
"""

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
"""### Read the Data"""

media_income = pd.read_csv('csv\Median_Household_Income_2015.csv', encoding='cp1252')

""" Data Exploration & Cleaning """
# print(media_income.shape)
# print(media_income.columns)

""" Check for Duplicates """
# print(media_income.duplicated().sum)  # False

""" Check for NaN Values """
# print(media_income.isna().sum())
media_income = media_income.dropna()
indexIncome = media_income[(media_income['Median Income'] == '-') | (media_income['Median Income'] == '(X)') |
                           (media_income['Median Income'] == '2,500-') | (media_income['Median Income'] == '250,000+')].index
media_income.drop(indexIncome, inplace=True)
media_income['Median Income'] = media_income['Median Income'].astype(int)



median_income_state = media_income.groupby('Geographic Area')['Median Income'].mean()


plt.figure()
map_plot = px.choropleth(locations=median_income_state.index,
                         title='Median Income by state', color=median_income_state.values,
                         locationmode='USA-states',
                         color_continuous_scale='hot_r',
                         hover_name=median_income_state.index,
                         scope="usa",
                         labels={"color": "Median Income Average"}
                         )
map_plot.show()

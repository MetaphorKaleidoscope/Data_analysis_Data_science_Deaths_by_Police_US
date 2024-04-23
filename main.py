"""
Extract insights from combining US census data and the Washington Post's database
on deaths by police in the United States.
"""

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import calendar


pd.set_option('display.max_columns', None)
""" Read the Data"""


deaths_data = pd.read_csv('csv\Deaths_by_Police_US.csv', encoding='cp1252')
media_income = pd.read_csv('csv\Median_Household_Income_2015.csv', encoding='cp1252')

""" Data Exploration & Cleaning """
# print(deaths_data.shape)
# print(deaths_data.columns)

""" Check for Duplicates """
# print(deaths_data.duplicated().sum)  # False

""" Check for NaN Values """
# print(deaths_data.isna().sum())
deaths_data = deaths_data.fillna('Not specified')


""" Convert Date to Datetime """
deaths_data['Date'] = pd.to_datetime(deaths_data['date'])
deaths_data['Year'] = [date.year for date in deaths_data.Date]
deaths_data['Month'] = [datetime.strptime(str(date), '%d/%m/%y').month for date in deaths_data.date]
deaths_data['month'] = [calendar.month_name[month] for month in deaths_data.Month]
deaths_data['Day'] = [datetime.strptime(str(date), '%d/%m/%y').day for date in deaths_data.date]


""" Plotly Donut Chart: Deaths by Police US by gender """
deaths_gender = deaths_data.gender.value_counts()

fig = px.pie(labels=deaths_gender.index, values=deaths_gender.values,
             title='Deaths by Police US by gender',
             names=deaths_gender.index,
             hole=0
             )
fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent+label')
fig.show()

""" Plotly Donut Chart: Deaths by Police in US by race """
deaths_race = deaths_data.race.value_counts()

fig = px.pie(labels=deaths_race.index, values=deaths_race.values,
             title='Deaths by Police US by race',
             names=deaths_race.index,
             hole=0
             )
fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent+label')
fig.show()

""" Plotly Donut Chart: Deaths by Police in US by age and race """
deaths_race_age = deaths_data.groupby(['race', 'age'], as_index=False).\
    agg({'id': pd.Series.count}).sort_values(['id'], ascending=False)

# Clear not specified
deaths_race_age = deaths_race_age[deaths_race_age.age != 'Not specified']

# Group by range of age
deaths_race_age = deaths_race_age.groupby([pd.cut(deaths_race_age['age'], [15, 20, 40, 50, 60, 70, 95]), 'race']).sum()


deaths_race_age_new = deaths_race_age.reset_index()  # reset Multi_Index to index

deaths_race_age_new.age = deaths_race_age_new.age.astype(str)
deaths_race_age_plot = deaths_race_age_new.sort_values(['race', 'id'], ascending=False)

######################################################################
sun_chart = px.sunburst(deaths_race_age_new,
                        path=['race', 'age'],
                        values=deaths_race_age_new.id.values,
                        title='Deaths by Police in US by age and race',
                        labels={"values": "Number of deaths"})
sun_chart.show()
#######################################################################
bar = px.bar(deaths_race_age_new, x='race', y='id',
             color='age',
             color_continuous_scale='Aggrnyl',
             labels={"id": "Number of deaths"}
             )
bar.update_layout(yaxis_title='Number of deaths', xaxis_title='Race',
                  title='Deaths by Police in US by age and race')
bar.show()

""" Deaths by Police in US by state"""
deaths_state = deaths_data.groupby(['state'], as_index=False).\
    agg({'id': pd.Series.count}).sort_values(['id'], ascending=True)


map_plot = px.choropleth(deaths_state, locations='state',
                         title='Number of deaths by state', color='id',
                         locationmode='USA-states',
                         color_continuous_scale='hot_r',
                         hover_name='state',
                         scope="usa",
                         )
map_plot.show()

""" Number of deaths by month"""
deaths_by_month = deaths_data.groupby(['Year', 'month', 'Month'], as_index=False).\
    agg({'id': pd.Series.count}).sort_values(['Year', 'Month'], ascending=True)


plt.figure()
plt.xticks(fontsize=8, rotation=0)
plt.title('Number of Deaths by Month')
ax1 = plt.gca()  # get the axes
ax1.plot(deaths_by_month.month[0:12], deaths_by_month.id[0:12], color='blue', label='2015')
ax1.plot(deaths_by_month.month[12:24], deaths_by_month.id[12:24], color='crimson', label='2016')
ax1.plot(deaths_by_month.month[24:31], deaths_by_month.id[24:31], color='gray', label='2017')
ax1.set_ylabel('Number of Deaths')
ax1.legend(loc='upper right', shadow=True, fontsize='medium')
plt.grid()
plt.show()

""" TYPE OF WEAPON USED """
type_weapon = deaths_data.armed.value_counts()

fig = px.pie(labels=type_weapon.index, values=type_weapon.values,
             title='TYPE OF WEAPON USED',
             names=type_weapon.index,
             hole=0
             )
fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent+label')
fig.show()

""" flee the scene """
flee_scene = deaths_data.flee.value_counts()

fig = px.pie(labels=flee_scene.index, values=flee_scene.values,
             title='Flee the scene?',
             names=flee_scene.index,
             hole=0
             )
fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent+label')
fig.show()

# """     Signs of mental illness     """
mental_illness = deaths_data.signs_of_mental_illness.value_counts()

fig = px.pie(labels=mental_illness.index, values=mental_illness.values,
             title='Signs of mental illness',
             names=mental_illness.index,
             hole=0
             )
fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent+label')
fig.show()

# """     Threat level     """
threat_level = deaths_data.threat_level.value_counts()

fig = px.pie(labels=threat_level.index, values=threat_level.values,
             title='Threat level',
             names=threat_level.index,
             hole=0
             )
fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent+label')
fig.show()

"""     Body camera     """
body_camera = deaths_data.body_camera.value_counts()

fig = px.pie(labels=body_camera.index, values=body_camera.values,
             title='Deaths by Police US: Use of Body Camera',
             names=body_camera.index,
             hole=0
             )
fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent+label')
fig.show()

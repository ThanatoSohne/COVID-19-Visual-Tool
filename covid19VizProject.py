#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import date
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from urllib.request import urlopen
import json
import math
import random

#Grab info from csv and place into dataframe
nytimes = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
df19 = pd.read_csv(nytimes, dtype={'fips':str})

#Sort by fips values
fipsDF = df19.sort_values("fips")

#Get the date from day before to coincide with most current data
ahora = date.today()
if ahora.day == 1:
    if ahora.month == 2 or 4 or 6 or 8 or 9:
        yesterday = ahora.strftime("%Y")+"-"+"0"+(str(int(ahora.strftime("%m"))-1))+"-"+"31"
    elif ahora.month == 5 or 7 or 10:
        yesterday = ahora.strftime("%Y")+"-"+"0"+(str(int(ahora.strftime("%m"))-1))+"-"+"30"
    elif ahora.month == 11:
        yesterday = ahora.strftime("%Y")+"-"+(str(int(ahora.strftime("%m"))-1))+"-"+"31"
    elif ahora.month == 12:
        yesterday = ahora.strftime("%Y")+"-"+(str(int(ahora.strftime("%m"))-1))+"-"+"30"
    elif ahora.month == 1:
        yesterday = (str(int(ahora.strftime("%Y"))-1))+"-"+"12"+"31"
    elif ahora.month == 3:
        yesterday = ahora.strftime("%Y")+"-02-28"
else:        
    yesterday = ahora.strftime("%Y")+"-"+ahora.strftime("%m")+"-"+(str(int(ahora.strftime("%d"))-1))


#Drop unknown values
currentDF = fipsDF[fipsDF.date == yesterday].dropna()
currentDF = currentDF.astype({"fips":int})

#Add in the leading zero to the fips codes that require them
#Borrowed from https://www.datasciencemadesimple.com/add-leading-preceding-zeros-python/
currentDF['fips']=currentDF['fips'].apply(lambda x: '{:05d}'.format(x))


# In[2]:


currentDF


# In[3]:


#A geoson with county info for the usage of the choropleth maps
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

#Opens a choropleth map showcasing the cases of COVID-19 here in the US
#Location information used is based on fips codes of individual counties
#Hover data should show county name, fips code, number of cases, and number of deaths related to COVID-19
usFig = px.choropleth_mapbox(currentDF, geojson=counties, locations='fips', color='cases',
                             color_continuous_scale='plasma_r',
                             range_color=(0, 100000),
                             hover_data=['county', 'state', 'cases', 'deaths'],
                             zoom=1.7, center = {"lat": 44.97, "lon": -103.77})

usFig.update_layout(mapbox_style="satellite-streets",
                    mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
usFig.update_layout(margin={"r": 20, "t": 20, "l": 70, "b": 20})
usFig.show()


# In[5]:


#List out the states within the dataframe
states = list(currentDF.state.unique())

#Within this dictionary, states are connected to their 'center' location and a 'zoom' number for the maps
stateCenter = {
        'Alabama': [32.83, -86.63, 5.4],
        'Alaska' : [64.73, -152.47, 3],
        'Arizona': [34.48, -111.67, 5.4],
        'Arkansas': [34.85, -92.38, 6],
        'California': [37.17, -119.45, 4.5],
        'Colorado': [39, -105.55, 5.5],
        'Connecticut': [41.68, -72.65, 6.7],
        'Delaware': [38.98, -75.51, 6.7],
        'District of Columbia': [38.9, -77, 9],
        'Florida': [28.68, -82.46, 5],
        'Georgia': [32.66, -83.44, 5.5],
        'Hawaii': [20.88, -157.23, 5.5],
        'Idaho': [45.17, -115.04, 5],
        'Illinois': [39.74, -89.5, 5.5],
        'Indiana': [39.77, -86.44, 5.5],
        'Iowa': [42.2, -93.58, 5.5],
        'Kansas': [38.43, -98.42, 5.5],
        'Kentucky':[37.53, -85.32, 5.8],
        'Louisiana': [31.29, -92.44, 5.5],
        'Maine': [45.25, -69.23, 5.5],
        'Maryland': [39.19, -76.77, 6],
        'Massachusetts': [42.38, -71.93, 6.2],
        'Michigan': [45.15, -84.65, 5],
        'Minnesota': [46.38, -94.49, 5],
        'Mississippi': [32.81, -89.53, 5.5],
        'Missouri': [38.47, -92.44, 5.5],
        'Montana': [47.16, -109.3, 5.2],
        'Nebraska': [41.53, -99.86, 5.5],
        'Nevada': [39.4, -116.79, 5.2],
        'New Hampshire': [43.64, -71.51, 6],
        'New Jersey': [40.07, -74.56, 6],
        'New Mexico': [34.45, -105.93, 5.5],
        'New York': [42.73, -75.14, 5.5],
        'North Carolina': [35.54, -79.49, 5.5],
        'North Dakota': [47.51, -100.31, 5.5],
        'Ohio': [40.25, -82.46, 5.5],
        'Oklahoma': [35.54, -96.97, 5.5], 
        'Oregon': [44.03, -120.54, 5.5],
        'Pennsylvania': [40.95, -77.58, 5.5],
        'Rhode Island': [41.67, -71.58, 7.5],
        'South Carolina': [33.84, -80.93, 6],
        'South Dakota': [44.51, -99.92, 5.5],
        'Tennessee': [35.8, -86.29, 5.5],
        'Texas': [31.39, -99.17, 4.5],
        'Utah': [39.29, -111.59, 5.5],
        'Vermont': [44.12, -72.72, 6.3],
        'Virginia': [37.51, -78.31, 5.5],
        'Washington': [47.39, -120.2, 5.5],
        'West Virginia': [38.71, -80.63, 6],
        'Wisconsin': [44.44, -90.13, 5.5],
        'Wyoming': [42.97, -107.67, 5.5],
        'Northern Mariana Islands': [16.81, 145.78, 5.5],
        'Puerto Rico': [18.23, -66.45, 6.5],
        'Virgin Islands': [17.73, -64.77, 6.5]
        }
#Continuous color schemes for the maps; they will be randomly chosen
colors = ["aggrnyl_r", "blackbody_r", "bluered", "blues", 
          "blugrn", "cividis", "electric", "jet", "peach",
          "viridis", "deep", "dense", "geyser", "picnic",
          "portland", "spectral", "balance", "magenta",
          "curl", "amp"]


# In[7]:


# ------------------------- CHOROPLETH & SUBPLOT MAPS------------------------------#
 
for s in states:
    stateDF = currentDF[currentDF.state == s]
    
    print("------------- Choropleth Map of " + s + " -------------")
    maxState = (math.ceil(stateDF['cases'].max() / 50.0) * 50.0) + 150
    stateFig = px.choropleth_mapbox(stateDF, geojson=counties, locations='fips', color='cases',
                                   color_continuous_scale=random.choice(colors), range_color=(0,maxState), 
                                   hover_data=['county', 'cases', 'deaths', 'fips'],
                                   zoom=stateCenter[s][2], center={"lat":stateCenter[s][0], "lon":stateCenter[s][1]},
                                   opacity=0.6, labels={'county': 'County', 'cases': 'Confirmed Cases', 
                                                      'deaths': 'Deaths'})

    stateFig.update_layout(mapbox_style="satellite-streets",
                         mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    stateFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    stateFig.show()
    
# --SUBPLOT--#

    print("-------------  Subplot of " + s + " -------------")
    statePlot = currentDF.loc[currentDF.state == s]
    topStateDF = statePlot.nlargest(10, 'cases')
    labels = list(topStateDF.county)
    values = list(topStateDF.cases)

    stateFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "domain"}]])

    stateFIG.add_trace(go.Bar(
        y=statePlot['county'],
        x=statePlot['cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(194, 174, 23, 0.6)',
            line=dict(color='rgba(194, 174, 23, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    stateFIG.add_trace(go.Bar(
        y=statePlot['county'],
        x=statePlot['deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
        )
    ))
    stateFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Confirmed Cases", "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='Overpass'),
                align='left'
            ),
            cells=dict(
                values=[statePlot[k].tolist() for k in statePlot.columns[1:]],
                fill_color='black',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    
    stateFIG.add_trace(
        go.Pie(labels = labels, values = values, name = "COVID-19 Cases"),
        row=2, col=2
    )
    stateFIG.update_layout(
        barmode='stack',
        height=800,
        width=1100,
        showlegend=False,
        title_text="COVID-19's Impact in " + s
    )
    stateFIG.show()


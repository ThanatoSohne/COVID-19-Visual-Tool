#!/usr/bin/env python
# coding: utf-8

# In[24]:


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
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import json
import math
import random
import numpy as np

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
elif (ahora.day > 1) and (ahora.day < 10):        
    yesterday = ahora.strftime("%Y")+"-"+ahora.strftime("%m")+"-0"+(str(int(ahora.strftime("%d"))-1))
else:
    yesterday = ahora.strftime("%Y")+"-"+ahora.strftime("%m")+"-"+(str(int(ahora.strftime("%d"))-1))


#Drop unknown values
currentDF = fipsDF[fipsDF.date == yesterday].dropna()
currentDF = currentDF.astype({"fips":int})

#Add in the leading zero to the fips codes that require them
#Borrowed from https://www.datasciencemadesimple.com/add-leading-preceding-zeros-python/
currentDF['fips']=currentDF['fips'].apply(lambda x: '{:05d}'.format(x))


# In[13]:


currentDF


# In[14]:


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


# In[15]:


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


# In[30]:


#This function will produce a scatter map showcasing basic info of the COVID-19 spread around the world.
#It employs another of the Plotly geo-maps which allows for easy user interface.
def mundiScatter():
    
    #First let us get access to the content of the webpage wherein the data can be found
    gebMeter = 'https://www.worldometers.info/coronavirus/'
    bypass = {'User-Agent': 'Mozilla/5.0'}
    gebClient = Request(gebMeter, headers=bypass)
    gebPage = urlopen(gebClient)

    #Parse this data using BeautifulSoup4
    site_parse = soup(gebPage, 'lxml')
    gebPage.close()

    #Grab the specific table we are looking for
    tables = site_parse.find("div", {"id":"nav-today"}).find('tbody').findAll('tr')
    
    #Place found data into a list after grabbing text and splitting by '\n' 
    dataCont = []
    for t in tables:
        take = t.text.split('\n')
        dataCont.append(take)

    #Now let's place this into a dataframe starting from the first entry in the table
    worldMapDF = pd.DataFrame(dataCont[8:])

    #The numbers below are the columns I wish to delete from the dataframe (superfluous data) 
    deleteThese = [0,1,11,12,14,17,18]
    for i in deleteThese:
        del worldMapDF[i]

    #Rename the columns 
    worldMapDF.columns = ['Country','Total Cases', 'New Cases', 'Total Deaths', 
                          'New Deaths', 'Total Recovered', 'Newly Recovered', 'Active Cases', 
                          'Serious/Critical', 'Total Tests', 'Population', 'Region']

    #Replace the "+" and "," symbols left over from the move to a dataframe
    #Also replace empty spaces with N/A or NaN
    #Fill these in with zeros
    worldMapDF = worldMapDF.replace("\+", "", regex=True)
    worldMapDF = worldMapDF.replace("\,", "", regex=True)
    worldMapDF = worldMapDF.replace('', np.nan) 
    worldMapDF = worldMapDF.replace(' ', np.nan) 
    worldMapDF = worldMapDF.fillna(0)
    worldMapDF = worldMapDF.replace("N/A", "0", regex=True)
    
    #Change the types of these particular columns from 'object' to 'int'
    worldMapDF[["Total Cases", "New Cases", "Total Deaths", "New Deaths", "Total Recovered", 
                "Newly Recovered", "Active Cases", "Serious/Critical", 
                "Total Tests", "Population"]] = worldMapDF[["Total Cases", "New Cases", "Total Deaths", 
                                                            "New Deaths", "Total Recovered", "Newly Recovered", 
                                                            "Active Cases", "Serious/Critical", "Total Tests", 
                                                            "Population"]].apply(pd.to_numeric)
    
    #Create the map to be presented
    geofig = px.scatter_geo(worldMapDF, locations="Country", locationmode="country names", color="Total Cases",
                            hover_data=["Total Cases", "New Cases", "Total Deaths", "New Deaths", "Serious/Critical",
                                        "Total Recovered", "Newly Recovered", "Active Cases", "Total Tests", 
                                        "Population", "Region"],
                            hover_name="Country", color_continuous_scale="balance",
                            size="Total Cases", projection="orthographic", text="Country",
                            opacity=0.5, size_max=70)
    geofig.update_layout(title="Interactive View of the Spread of COVID-19 Around the World")
    return geofig


# In[31]:


#Now let's run the function!
mundiScatter()


# In[32]:


#This function produces an animated scatter plot of the number of 
#cases and deaths around the world in regards to COVID-19
#The size of the bubble is relative to the number of deaths and the 
#cases are relayed in the text in the bubbles
def aniGlobe():
    
    #First we need to grab the data from the ECDC website. 
    #We need the date to get the most current data as the date is 
    #part of the web address
    ahora = date.today()
    
    #We will pull the date of the day before as the site usually does not
    #update with the date of the day pulled
    if int(ahora.strftime("%d")) <= 10:
        yest = ('0' + str(int(ahora.strftime("%d")) - 1))
    else:
        yest = str(int(ahora.strftime('%d')) - 1)

    #Now we have the proper date and its proper format (YYYY-MM-DD), let's access and store the content using pandas
    ecdc = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-2020-'
    xls = '.xlsx'
    newURL = ecdc + str(ahora.strftime('%m')) + '-' + yest + xls

    #Place into a dataframe and sort by date
    table = pd.read_excel(newURL)
    table = table.sort_values('dateRep')
    table = table.fillna(0)
    holder = table[table['cases'] < 0].index
    table.drop(holder, inplace=True)
    table = table.rename(columns={'dateRep': 'Date', 'cases': 'Cases', 'deaths': 'Deaths',
                                  'countriesAndTerritories': 'Countries/Territories',
                                  'popData2019': 'Population', 'continentExp': 'Continent'})
    see = table['Date'].astype(str).str[:]

    #Create the animated scatter plot
    blanche = px.scatter(table, x='Population', y='Cases', animation_frame=see,
                         animation_group='Countries/Territories', size=table['Deaths'].clip(lower=0),
                         color='Continent', hover_name='Countries/Territories',
                         log_y=True, size_max=500, range_x=[10000000, 2000000000], range_y=[1, 200000])
    blanche.update_layout(showlegend=False,
                          title="ECDC's Data Showing the Infected Cases Color Coded by Continent with Daily Deaths as Time Progressed")
    return blanche


# In[33]:


aniGlobe()


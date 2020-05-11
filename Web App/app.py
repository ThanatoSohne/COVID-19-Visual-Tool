import os
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
import pandas as pd
import math
import random as r
from datetime import date
import xlrd

# ----------------------Variables and Plots Held Here----------------------------------------------#
# Dropdown menu options for state maps on page 2
states = [{'label': 'Alaska', 'value': 'AK'},
          {'label': 'Alabama', 'value': 'AL'},
          {'label': 'Arkansas', 'value': 'AR'},
          {'label': 'Arizona', 'value': 'AZ'},
          {'label': 'California', 'value': 'CA'},
          {'label': 'Colorado', 'value': 'CO'},
          {'label': 'Connecticut', 'value': 'CT'},
          {'label': 'Delaware', 'value': 'DE'},
          {'label': 'Florida', 'value': 'FL'},
          {'label': 'Georgia', 'value': 'GA'},
          {'label': 'Hawai\'i', 'value': 'HI'},
          {'label': 'Idaho', 'value': 'ID'},
          {'label': 'Illinois', 'value': 'IL'},
          {'label': 'Indiana', 'value': 'IN'},
          {'label': 'Iowa', 'value': 'IO'},
          {'label': 'Kansas', 'value': 'KA'},
          {'label': 'Kentucky', 'value': 'KY'},
          {'label': 'Louisiana', 'value': 'LA'},
          {'label': 'Massachusetts', 'value': 'MA'},
          {'label': 'Maryland', 'value': 'MD'},
          {'label': 'Maine', 'value': 'ME'},
          {'label': 'Michigan', 'value': 'MI'},
          {'label': 'Minnesota', 'value': 'MN'},
          {'label': 'Missouri', 'value': 'MO'},
          {'label': 'Mississippi', 'value': 'MS'},
          {'label': 'Montana', 'value': 'MT'},
          {'label': 'North Carolina', 'value': 'NC'},
          {'label': 'North Dakota', 'value': 'ND'},
          {'label': 'Nebraska', 'value': 'NE'},
          {'label': 'New Hampshire', 'value': 'NH'},
          {'label': 'New Jersey', 'value': 'NJ'},
          {'label': 'New Mexico', 'value': 'NM'},
          {'label': 'Nevada', 'value': 'NV'},
          {'label': 'New York', 'value': 'NY'},
          {'label': 'Ohio', 'value': 'OH'},
          {'label': 'Oklahoma', 'value': 'OK'},
          {'label': 'Oregon', 'value': 'OR'},
          {'label': 'Pennsylvania', 'value': 'PA'},
          {'label': 'Puerto Rico', 'value': 'PR'},
          {'label': 'Rhode Island', 'value': 'RI'},
          {'label': 'South Carolina', 'value': 'SC'},
          {'label': 'South Dakota', 'value': 'SD'},
          {'label': 'Tennessee', 'value': 'TN'},
          {'label': 'Texas', 'value': 'TX'},
          {'label': 'Utah', 'value': 'UT'},
          {'label': 'Virginia', 'value': 'VA'},
          {'label': 'Vermont', 'value': 'VT'},
          {'label': 'Washington', 'value': 'WA'},
          {'label': 'Wisconsin', 'value': 'WI'},
          {'label': 'West Virginia', 'value': 'WV'},
          {'label': 'Wyoming', 'value': 'WY'},
          ]

oracle_country = [
    {'label': 'Italy', 'value': 'ITA'},
    {'label': 'New Zealand', 'value': 'NZ'},
    {'label': 'South Africa', 'value': 'SA'},
    {'label': 'South Korea', 'value': 'SK'},
    {'label': 'Brazil', 'value': 'BRZ'},
]

# Pull fips codes for accompanying county/state maps

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


# ---------------------------WORLD SCATTER GEO MAP----------------------------#
def mundiScatter():
    df = pd.read_csv(
        'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/COVID-19_cases_worldMeters.csv',
        encoding='Latin-1')

    # country = df['Country'].tolist()
    # tCases = df['Total Cases'].tolist()
    # nCases = df['New Cases'].tolist()
    # tDeaths = df['Total Deaths'].tolist()
    # nDeaths = df['New Deaths'].tolist()
    # hope = df['Total Recovered'].tolist()
    # active = df['Active Cases'].tolist()
    # serious = df['Serious/Critical'].tolist()
    # tested = df['Total Tested'].tolist()

    geofig = px.scatter_geo(df, locations="Country", locationmode="country names", color="Total Cases",
                            hover_data=["Total Cases", "New Cases", "Total Deaths", "New Deaths", "Serious/Critical",
                                        "Total Recovered", "Active Cases", "Total Tested"],
                            hover_name="Country", color_continuous_scale="balance",
                            size="Total Cases", projection="orthographic", text="Country",
                            opacity=0.5, size_max=70)
    geofig.update_layout(title="Interactive View of the Spread of COVID-19 Around the World")
    return geofig


# --Animation Map--#
def aniGlobe():
    ahora = date.today()

    if int(ahora.strftime("%d")) < 10:
        yest = ('0' + str(int(ahora.strftime("%d")) - 1))
    else:
        yest = str(ahora.strftime('%d'))

    ecdc = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-2020-'
    xls = '.xlsx'
    newURL = ecdc + str(ahora.strftime('%m')) + '-' + yest + xls

    table = pd.read_excel(newURL)
    table = table.sort_values('dateRep')
    table = table.fillna(0)
    holder = table[table['cases'] < 0].index
    table.drop(holder, inplace=True)
    table = table.rename(columns={'dateRep': 'Date', 'cases': 'Cases', 'deaths': 'Deaths',
                                  'countriesAndTerritories': 'Countries/Territories',
                                  'popData2018': 'Population', 'continentExp': 'Continent'})
    see = table['Date'].astype(str).str[:]

    blanche = px.scatter(table, x='Population', y='Cases', animation_frame=see,
                         animation_group='Countries/Territories', size='Deaths',
                         color='Continent', hover_name='Countries/Territories',
                         log_y=True, size_max=500, range_x=[10000000, 2000000000], range_y=[1, 100000])
    blanche.update_layout(showlegend=False,
                          title="ECDC's Data Showing the Infected Cases Color Coded by Continent with Daily Deaths as Time Progressed")

    return blanche


# -------------------------ALASKA CHOROPLETH & SUBPLOT MAPS------------------------------#
akDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_akWiki.csv',
    dtype={'fips': str})
cleanAK = akDF.fillna(0)


def akmap():
    # Used to round up to a proper max for the range_color function
    maxAK = (math.ceil(cleanAK['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    akFig = px.choropleth_mapbox(cleanAK, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='aggrnyl',
                                 range_color=(0, maxAK),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries', 'Latitude',
                                             'Longitude'],
                                 zoom=3, center={"lat": 63.860036, "lon": -150.255849},
                                 opacity=0.6, labels={'County': 'Borough', 'Confirmed Cases': 'Confirmed Cases'})

    akFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    akFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return akFig


# --SUBPLOT--#
def aksub():
    akFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    akFIG.add_trace(go.Bar(
        y=cleanAK['County'],
        x=cleanAK['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(194, 174, 23, 0.6)',
            line=dict(color='rgba(194, 174, 23, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    akFIG.add_trace(go.Bar(
        y=cleanAK['County'],
        x=cleanAK['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
        )
    ))

    akFIG.add_trace(go.Bar(
        y=cleanAK['County'],
        x=cleanAK['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(96, 148, 110, 0.6)',
            line=dict(color='rgba(96, 148, 110, 1.0)', width=3)
        )
    ))

    akFIG.add_trace(
        go.Densitymapbox(lat=cleanAK.Latitude, lon=cleanAK.Longitude,
                         z=cleanAK['Confirmed Cases'], radius=30,
                         showscale=False,
                         visible=True),
        row=2, col=2)

    akFIG.add_trace(
        go.Table(
            header=dict(
                values=["Borough", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='Overpass'),
                align='left'
            ),
            cells=dict(
                values=[cleanAK[k].tolist() for k in cleanAK.columns[:]],
                fill_color='black',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    akFIG.update_layout(
        mapbox_style="stamen-terrain", mapbox_center_lon=-143.6,
        mapbox_center_lat=64.2,
        mapbox=dict(
            zoom=3
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Alaska"
    )
    return akFIG


# -------------------------ALABAMA CHOROPLETH MAP------------------------------#
alDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_aldoh.csv',
    dtype={'fips': str})
cleanAL = alDF.fillna(0)


def almap():
    # Used to round up to a proper max for the range_color function
    maxAL = (math.ceil(cleanAL['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    # Leaving this here in case we will need it later
    # alfips = ['01001','01003','01005','01007','01009','01011','01013','01015','01017','01019','01021','01023','01025','01027','01029',
    #          '01031','01033','01035','01037','01039','01041','01043','01045','01047','01049','01051','01053','01055','01057','01059',
    #          '01061','01063','01065','01067','01069','01071','01073','01075','01077','01079','01081','01083','01085','01087','01089',
    #          '01091','01093','01095','01097','01099','01101','01103','01105','01107','01109','01111','01113','01117','01115','01119',
    #          '01121','01123','01125','01127','01129','01131','01133']

    alFig = px.choropleth_mapbox(cleanAL, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale="viridis",
                                 range_color=(0, maxAL),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Latitude', 'Longitude'],
                                 zoom=5.5, center={"lat": 32.756902, "lon": -86.844513},
                                 opacity=0.6, labels={'Confirmed Cases': 'Confirmed Cases'}
                                 )

    alFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    alFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return alFig


# --SUBPLOT--#
def alsub():
    alFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    alFIG.add_trace(go.Bar(
        y=cleanAL['County'],
        x=cleanAL['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(159, 121, 224, 0.6)',
            line=dict(color='rgba(159, 121, 224, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    alFIG.add_trace(go.Bar(
        y=cleanAL['County'],
        x=cleanAL['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
        )
    ))

    alFIG.add_trace(
        go.Densitymapbox(lat=cleanAL.Latitude, lon=cleanAL.Longitude,
                         z=cleanAL['Confirmed Cases'], radius=25,
                         showscale=False,
                         visible=True),
        row=2, col=2)

    alFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanAL[k].tolist() for k in cleanAL.columns[:]],
                fill_color='black',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    alFIG.update_layout(
        mapbox_style="stamen-terrain", mapbox_center_lon=-86.6,
        mapbox_center_lat=33.3,
        mapbox=dict(
            zoom=4.7
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Alabama"
    )
    return alFIG


# -------------------------ARKANSAS CHOROPLETH MAP------------------------------#
arDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_ardoh.csv',
    dtype={'fips': str})
cleanAR = arDF.fillna(0)


def armap():
    # Used to round up to a proper max for the range_color function
    maxAR = (math.ceil(cleanAR['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    arFig = px.choropleth_mapbox(cleanAR, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='sunsetdark', range_color=(0, maxAR),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.5, center={"lat": 34.899764, "lon": -92.439213},
                                 opacity=0.6, labels={"County": "County"})

    arFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    arFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return arFig


# --SUBPLOT--#
def arsub():
    arFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    arFIG.add_trace(go.Bar(
        y=cleanAR['County'],
        x=cleanAR['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(194, 174, 23, 0.6)',
            line=dict(color='rgba(194, 174, 23, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    arFIG.add_trace(go.Bar(
        y=cleanAR['County'],
        x=cleanAR['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
        )
    ))
    arFIG.add_trace(go.Bar(
        y=cleanAR['County'],
        x=cleanAR['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(96, 148, 110, 0.6)',
            line=dict(color='rgba(96, 148, 110, 1.0)', width=3)
        )
    ))

    arFIG.add_trace(
        go.Densitymapbox(lat=cleanAR.Latitude, lon=cleanAR.Longitude,
                         z=cleanAR['Confirmed Cases'], radius=20,
                         showscale=False,
                         visible=True),
        row=2, col=2)

    arFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed<br>Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='Overpass'),
                align="left"
            ),
            cells=dict(
                values=[cleanAR[k].tolist() for k in cleanAR.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    arFIG.update_layout(
        mapbox_style="stamen-terrain", mapbox_center_lon=-92.1,
        mapbox_center_lat=34.7,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Arkansas"
    )
    return arFIG


# -------------------------ARIZONA CHOROPLETH MAP------------------------------#
azDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_azWiki.csv',
    dtype={'fips': str})
cleanAZ = azDF.fillna(0)


def azmap():
    # Used to round up to a proper max for the range_color function
    maxAZ = (math.ceil(cleanAZ['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    azFig = px.choropleth_mapbox(cleanAZ, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='picnic', range_color=(0, maxAZ),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.5, center={"lat": 34.333217, "lon": -111.712983},
                                 opacity=0.6, labels={"County": "County"})

    azFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    azFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return azFig


# --SUBPLOT--#
def azsub():
    azFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    azFIG.add_trace(go.Bar(
        y=cleanAZ['County'],
        x=cleanAZ['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(194, 174, 23, 0.6)',
            line=dict(color='rgba(194, 174, 23, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    azFIG.add_trace(go.Bar(
        y=cleanAZ['County'],
        x=cleanAZ['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
        )
    ))
    azFIG.add_trace(
        go.Densitymapbox(lat=cleanAZ.Latitude, lon=cleanAZ.Longitude,
                         z=cleanAZ['Confirmed Cases'], radius=30,
                         showscale=False,
                         visible=True),
        row=2, col=2)

    azFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed<br>Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='Overpass'),
                align="left"
            ),
            cells=dict(
                values=[cleanAZ[k].tolist() for k in cleanAZ.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    azFIG.update_layout(
        mapbox_style="stamen-terrain", mapbox_center_lon=-111.8,
        mapbox_center_lat=34.2,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Arizona"
    )
    return azFIG


# -------------------------CALIFORNIA CHOROPLETH MAP------------------------------#
caDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_caWiki.csv',
    dtype={'fips': str})
cleanCA = caDF.fillna(0)


def camap():
    # Used to round up to a proper max for the range_color function
    maxCA = (math.ceil(cleanCA['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    caFig = px.choropleth_mapbox(cleanCA, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='mrybm', range_color=(0, maxCA),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=4.5, center={"lat": 37.863942, "lon": -120.753667},
                                 opacity=0.6, labels={"County": "County"},
                                 )

    caFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    caFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    caFig.update_geos(fitbounds="locations")
    return caFig


# --SUBPLOT--#
def casub():
    caFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    caFIG.add_trace(go.Bar(
        y=cleanCA['County'],
        x=cleanCA['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    caFIG.add_trace(go.Bar(
        y=cleanCA['County'],
        x=cleanCA['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    caFIG.add_trace(
        go.Densitymapbox(lat=cleanCA.Latitude, lon=cleanCA.Longitude,
                         z=cleanCA['Confirmed Cases'], radius=20,
                         showscale=False, colorscale='rainbow',
                         visible=True),
        row=2, col=2)

    caFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed<br>Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanCA[k].tolist() for k in cleanCA.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    caFIG.update_layout(
        mapbox_style="stamen-terrain", mapbox_center_lon=-120.0,
        mapbox_center_lat=37.1,
        mapbox=dict(
            zoom=4
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in California"
    )
    return caFIG


# -------------------------COLORADO CHOROPLETH MAP------------------------------#
coDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_coDOH.csv',
    dtype={'fips': str})
cleanCO = coDF.fillna(0)


def comap():
    # Used to round up to a proper max for the range_color function
    maxCO = (math.ceil(cleanCO['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    coFig = px.choropleth_mapbox(cleanCO, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='mint', range_color=(0, maxCO),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5, center={"lat": 39.055183, "lon": -105.547831},
                                 opacity=0.6, labels={"County": "County"})

    coFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    coFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return coFig


# --SUBPLOT--#
def cosub():
    coFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    coFIG.add_trace(go.Bar(
        y=cleanCO['County'],
        x=cleanCO['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    coFIG.add_trace(go.Bar(
        y=cleanCO['County'],
        x=cleanCO['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    coFIG.add_trace(
        go.Densitymapbox(lat=cleanCO.Latitude, lon=cleanCO.Longitude,
                         z=cleanCO['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    coFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanCO[k].tolist() for k in cleanCO.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    coFIG.update_layout(
        mapbox_style="stamen-terrain", mapbox_center_lon=-105.4,
        mapbox_center_lat=38.9,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Colorado"
    )
    return coFIG


# -------------------------CONNECTICUT CHOROPLETH MAP------------------------------#
ctDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_ctDOH.csv',
    dtype={'fips': str})
cleanCT = ctDF.fillna(0)


def ctmap():
    # Used to round up to a proper max for the range_color function
    maxCT = (math.ceil(cleanCT['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    ctFig = px.choropleth_mapbox(cleanCT, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='curl_r', range_color=(0, maxCT),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Hospitalized'],
                                 zoom=6.5, center={"lat": 41.647811, "lon": -72.641075},
                                 opacity=0.6, labels={"County": "County"})

    ctFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    ctFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return ctFig


# --SUBPLOT--#
def ctsub():
    ctFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    ctFIG.add_trace(go.Bar(
        y=cleanCT['County'],
        x=cleanCT['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    ctFIG.add_trace(go.Bar(
        y=cleanCT['County'],
        x=cleanCT['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(3, 252, 248, 0.6)',
            line=dict(color='rgba(3, 252, 248, 1.0)', width=3)
        )
    )
    )
    ctFIG.add_trace(go.Bar(
        y=cleanCT['County'],
        x=cleanCT['Hospitalized'],
        name='Hospitalized',
        orientation='h',
        marker=dict(
            color='rgba(28, 3, 252, 0.6)',
            line=dict(color='rgba(28, 3, 252, 1.0)', width=3)
        )
    )

    )
    ctFIG.add_trace(
        go.Densitymapbox(lat=cleanCT.Latitude, lon=cleanCT.Longitude,
                         z=cleanCT['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    ctFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases", "Deaths",
                        "Hospitalized"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanCT[k].tolist() for k in cleanCT.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    ctFIG.update_layout(
        mapbox_style="stamen-terrain", mapbox_center_lon=-72.64,
        mapbox_center_lat=41.6,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Connecticut"
    )
    return ctFIG


# -------------------------DELAWARE CHOROPLETH MAP------------------------------#
deDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_deWiki.csv',
    dtype={'fips': str})
cleanDE = deDF.fillna(0)


def demap():
    # Used to round up to a proper max for the range_color function
    maxDE = (math.ceil(cleanDE['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    deFig = px.choropleth_mapbox(cleanDE, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='geyser', range_color=(0, maxDE),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=7.1, center={"lat": 39.051475, "lon": -75.416010},
                                 opacity=0.6, labels={"County": "County"})

    deFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    deFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return deFig


# --SUBPLOT--#
def desub():
    deFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    deFIG.add_trace(go.Bar(
        y=cleanDE['County'],
        x=cleanDE['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    deFIG.add_trace(go.Bar(
        y=cleanDE['County'],
        x=cleanDE['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    deFIG.add_trace(go.Bar(
        y=cleanDE['County'],
        x=cleanDE['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(95, 107, 106, 0.6)',
            line=dict(color='rgba(95, 107, 106, 1.0)', width=3)
        )
    ))
    deFIG.add_trace(
        go.Densitymapbox(lat=cleanDE.Latitude, lon=cleanDE.Longitude,
                         z=cleanDE['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='rainbow',
                         visible=True),
        row=2, col=2)
    deFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanDE[k].tolist() for k in cleanDE.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    deFIG.update_layout(
        mapbox_style="stamen-terrain", mapbox_center_lon=-75.4,
        mapbox_center_lat=39.1,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Delaware"
    )
    return deFIG


# -------------------------FLORIDA CHOROPLETH MAP------------------------------#
flDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_flWiki.csv',
    dtype={'fips': str})
cleanFL = flDF.fillna(0)


def flmap():
    # Used to round up to a proper max for the range_color function
    maxFL = (math.ceil(cleanFL['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    flFig = px.choropleth_mapbox(cleanFL, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='sunset', range_color=(0, maxFL),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.2, center={"lat": 28.311684, "lon": -81.446706},
                                 opacity=0.6, labels={"County": "County"})

    flFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    flFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return flFig


# --SUBPLOT--#
def flsub():
    flFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    flFIG.add_trace(go.Bar(
        y=cleanFL['County'],
        x=cleanFL['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    flFIG.add_trace(go.Bar(
        y=cleanFL['County'],
        x=cleanFL['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    flFIG.add_trace(go.Bar(
        y=cleanFL['County'],
        x=cleanFL['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(95, 107, 106, 0.6)',
            line=dict(color='rgba(95, 107, 106, 1.0)', width=3)
        )
    ))
    flFIG.add_trace(
        go.Densitymapbox(lat=cleanFL.Latitude, lon=cleanFL.Longitude,
                         z=cleanFL['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='rainbow',
                         visible=True),
        row=2, col=2)
    flFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanFL[k].tolist() for k in cleanFL.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    flFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=28.3,
        mapbox_center_lon=-81.5,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Florida"
    )
    return flFIG


# -------------------------GEORGIA CHOROPLETH MAP------------------------------#
gaDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_gadoh.csv',
    dtype={'fips': str})
cleanGA = gaDF.fillna(0)


def gamap():
    # Used to round up to a proper max for the range_color function
    maxGA = (math.ceil(cleanGA['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    gaFig = px.choropleth_mapbox(cleanGA, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='teal', range_color=(0, maxGA),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.5, center={"lat": 32.699989, "lon": -83.427133},
                                 opacity=0.6, labels={"County": "County"})

    gaFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    gaFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return gaFig


# --SUBPLOT--#
def gasub():
    gaFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    gaFIG.add_trace(go.Bar(
        y=cleanGA['County'],
        x=cleanGA['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    gaFIG.add_trace(go.Bar(
        y=cleanGA['County'],
        x=cleanGA['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    gaFIG.add_trace(
        go.Densitymapbox(lat=cleanGA.Latitude, lon=cleanGA.Longitude,
                         z=cleanGA['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='rainbow',
                         visible=True),
        row=2, col=2)
    gaFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanGA[k].tolist() for k in cleanGA.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    gaFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=32.7,
        mapbox_center_lon=-83.4,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Georgia"
    )
    return gaFIG


##-------------------------GUAM/ MP CHOROPLETH MAP------------------------------#
# guMP = pd.read_csv('https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/Web%20Scrapers/US%20States/COVID-19_cases_gu_mp_Wiki.csv')
# cleanGM = guMP.fillna(0)
#
##Used to round up to a proper max for the range_color function
# maxGM = (math.ceil(cleanGM['Confirmed Cases'].max() / 50.0) * 50.0) + 150
#
# gmFig = px.choropleth_mapbox(cleanGM, geojson = counties, locations = 'fips', color = 'Confirmed Cases',
#                             color_continuous_scale = 'tropic', range_color = (0,maxGM),
#                             hover_data = ['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
#                             zoom = 5, center = {"lat": 14.272591, "lon": 145.346504},
#                             opacity = 0.6, labels = {"County": "Territory"})
#
# gmFig.update_layout(mapbox_style = "satellite-streets", mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
# gmFig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# gmFig.show()
# -------------------------HAWAI'I CHOROPLETH MAP------------------------------#
hiDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_hidoh.csv',
    dtype={'fips': str})
cleanHI = hiDF.fillna(0)


def himap():
    # Used to round up to a proper max for the range_color function
    maxHI = (math.ceil(cleanHI['Total Cases'].max() / 50.0) * 50.0) + 150

    hiFig = px.choropleth_mapbox(cleanHI, geojson=counties, locations='fips', color='Total Cases',
                                 color_continuous_scale='magma_r', range_color=(0, maxHI),
                                 hover_data=['County', 'Total Cases', 'Deaths', 'Released from Isolation',
                                             'Hospitalization'],
                                 zoom=5.7, center={"lat": 20.906635, "lon": -157.027297},
                                 opacity=0.6, labels={"County": "County"})

    hiFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    hiFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return hiFig


# --SUBPLOT--#
def hisub():
    hiFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    hiFIG.add_trace(go.Bar(
        y=cleanHI['County'],
        x=cleanHI['Total Cases'],
        name='Total Cases',
        orientation='h',
        marker=dict(
            color='rgba(255, 128, 168, 0.6)',
            line=dict(color='rgba(255, 128, 168, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    hiFIG.add_trace(go.Bar(
        y=cleanHI['County'],
        x=cleanHI['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    hiFIG.add_trace(go.Bar(
        y=cleanHI['County'],
        x=cleanHI['Released from Isolation'],
        name='Released from Isolation',
        orientation='h',
        marker=dict(
            color='rgba(95, 107, 106, 0.6)',
            line=dict(color='rgba(95, 107, 106, 1.0)', width=3)
        )
    ))
    hiFIG.add_trace(go.Bar(
        y=cleanHI['County'],
        x=cleanHI['Hospitalization'],
        name='Required Hospitalization',
        orientation='h',
        marker=dict(
            color='rgba(208, 217, 50, 0.6)',
            line=dict(color='rgba(208, 217, 50, 1.0)', width=3)
        )
    ))
    hiFIG.add_trace(
        go.Densitymapbox(lat=cleanHI.Latitude, lon=cleanHI.Longitude,
                         z=cleanHI['Total Cases'], radius=25,
                         showscale=False, colorscale='rainbow',
                         visible=True),
        row=2, col=2)
    hiFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Total Cases",
                        "Deaths", "Recoveries", "Released from Isolation",
                        "Required Hospitalization", "Pending"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanHI[k].tolist() for k in cleanHI.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    hiFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=20.9,
        mapbox_center_lon=-157.1,
        mapbox=dict(
            zoom=4.8
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Hawai'i"
    )
    return hiFIG


# ---------------------------IDAHO CHOROPLETH MAP------------------------------#
idDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_idWiki.csv',
    dtype={'fips': str})
cleanID = idDF.fillna(0)


def idmap():
    # Used to round up to a proper max for the range_color function
    maxID = (math.ceil(cleanID['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    idFig = px.choropleth_mapbox(cleanID, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='plotly3', range_color=(0, maxID),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=4.9, center={"lat": 45.570854, "lon": -115.131137},
                                 opacity=0.55, labels={"County": "County"})

    idFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    idFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return idFig


# --SUBPLOT--#
def idsub():
    idFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    idFIG.add_trace(go.Bar(
        y=cleanID['County'],
        x=cleanID['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    idFIG.add_trace(go.Bar(
        y=cleanID['County'],
        x=cleanID['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    idFIG.add_trace(go.Bar(
        y=cleanID['County'],
        x=cleanID['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(252, 186, 3, 0.6)',
            line=dict(color='rgba(252, 186, 3, 1.0)', width=3)
        )
    ))
    idFIG.add_trace(
        go.Densitymapbox(lat=cleanID.Latitude, lon=cleanID.Longitude,
                         z=cleanID['Confirmed Cases'], radius=30,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    idFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanID[k].tolist() for k in cleanID.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    idFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=44.06,
        mapbox_center_lon=-114.74,
        mapbox=dict(
            zoom=4.8
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Idaho"
    )
    return idFIG


# ---------------------------ILLINOIS CHOROPLETH MAP------------------------------#
ilDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_ilWiki.csv',
    dtype={'fips': str})
cleanIL = ilDF.fillna(0)


def ilmap():
    # Used to round up to a proper max for the range_color function
    maxIL = (math.ceil(cleanIL['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    ilFig = px.choropleth_mapbox(cleanIL, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='plasma_r', range_color=(0, maxIL),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.3, center={"lat": 40.0190, "lon": -88.3000},
                                 opacity=0.6, labels={"County": "County"})

    ilFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    ilFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return ilFig


# --SUBPLOT--#
def ilsub():
    ilFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    ilFIG.add_trace(go.Bar(
        y=cleanIL['County'],
        x=cleanIL['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(252, 186, 3, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    ilFIG.add_trace(go.Bar(
        y=cleanIL['County'],
        x=cleanIL['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    ilFIG.add_trace(go.Bar(
        y=cleanIL['County'],
        x=cleanIL['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(95, 107, 106, 0.6)',
            line=dict(color='rgba(95, 107, 106, 1.0)', width=3)
        )
    ))
    ilFIG.add_trace(
        go.Densitymapbox(lat=cleanIL.Latitude, lon=cleanIL.Longitude,
                         z=cleanIL['Confirmed Cases'], radius=35,
                         showscale=False, colorscale='rainbow',
                         visible=True),
        row=2, col=2)
    ilFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanIL[k].tolist() for k in cleanIL.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    ilFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=40.6,
        mapbox_center_lon=-89.3,
        mapbox=dict(
            zoom=4.8
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Illinois"
    )
    return ilFIG


# ---------------------------INDIANA CHOROPLETH MAP------------------------------#
inDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_inWiki.csv',
    dtype={'fips': str})
cleanIN = inDF.fillna(0)


def inmap():
    # Used to round up to a proper max for the range_color function
    maxIN = (math.ceil(cleanIN['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    inFig = px.choropleth_mapbox(cleanIN, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='ylgnbu', range_color=(0, maxIN),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.4, center={"lat": 40.013050, "lon": -86.208909},
                                 opacity=0.6, labels={"County": "County"})

    inFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    inFig.update_layout(margin={"r": 100, "t": 0, "l": 100, "b": 0})
    return inFig


# --SUBPLOT--#
def insub():
    inFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    inFIG.add_trace(go.Bar(
        y=cleanIN['County'],
        x=cleanIN['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    inFIG.add_trace(go.Bar(
        y=cleanIN['County'],
        x=cleanIN['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    inFIG.add_trace(
        go.Densitymapbox(lat=cleanIN.Latitude, lon=cleanIN.Longitude,
                         z=cleanIN['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='rainbow',
                         visible=True),
        row=2, col=2)
    inFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanIN[k].tolist() for k in cleanIN.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    inFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=40.01,
        mapbox_center_lon=-86.21,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Indiana"
    )
    return inFIG


# ---------------------------IOWA CHOROPLETH MAP------------------------------#
ioDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_ioWiki.csv',
    dtype={'fips': str})
cleanIO = ioDF.fillna(0)


def iomap():
    # Used to round up to a proper max for the range_color function
    maxIO = (math.ceil(cleanIO['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    ioFig = px.choropleth_mapbox(cleanIO, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='rdpu', range_color=(0, maxIO),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.3, center={"lat": 42.074622, "lon": -93.500036},
                                 opacity=0.6, labels={"County": "County"})

    ioFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    ioFig.update_layout(margin={"r": 100, "t": 0, "l": 100, "b": 0})
    return ioFig


# --SUBPLOT--#
def iosub():
    ioFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    ioFIG.add_trace(go.Bar(
        y=cleanIO['County'],
        x=cleanIO['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    ioFIG.add_trace(go.Bar(
        y=cleanIO['County'],
        x=cleanIO['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    ioFIG.add_trace(go.Bar(
        y=cleanIO['County'],
        x=cleanIO['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(102, 25, 105, 0.6)',
            line=dict(color='rgba(102, 25, 105, 1.0)', width=3)
        )
    ))
    ioFIG.add_trace(
        go.Densitymapbox(lat=cleanIO.Latitude, lon=cleanIO.Longitude,
                         z=cleanIO['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    ioFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanIO[k].tolist() for k in cleanIO.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    ioFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=42.07,
        mapbox_center_lon=-93.5,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Iowa"
    )
    return ioFIG


# ---------------------------KANSAS CHOROPLETH MAP------------------------------#
kaDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_kaWiki.csv',
    dtype={'fips': str})
cleanKA = kaDF.fillna(0)


def kamap():
    # Used to round up to a proper max for the range_color function
    maxKA = (math.ceil(cleanKA['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    kaFig = px.choropleth_mapbox(cleanKA, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='darkmint', range_color=(0, maxKA),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5, center={"lat": 38.541749, "lon": -98.428791},
                                 opacity=0.6, labels={"County": "County"})

    kaFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    kaFig.update_layout(margin={"r": 100, "t": 0, "l": 100, "b": 0})
    return kaFig


# --SUBPLOT--#
def kasub():
    kaFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    kaFIG.add_trace(go.Bar(
        y=cleanKA['County'],
        x=cleanKA['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    kaFIG.add_trace(go.Bar(
        y=cleanKA['County'],
        x=cleanKA['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    kaFIG.add_trace(go.Bar(
        y=cleanKA['County'],
        x=cleanKA['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(102, 25, 105, 0.6)',
            line=dict(color='rgba(102, 25, 105, 1.0)', width=3)
        )
    ))
    kaFIG.add_trace(
        go.Densitymapbox(lat=cleanKA.Latitude, lon=cleanKA.Longitude,
                         z=cleanKA['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    kaFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanKA[k].tolist() for k in cleanKA.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    kaFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=38.54,
        mapbox_center_lon=-98.43,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Kansas"
    )
    return kaFIG


# ---------------------------KENTUCKY CHOROPLETH MAP------------------------------#
kyDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_kyNews.csv',
    dtype={'fips': str})
cleanKY = kyDF.fillna(0)


def kymap():
    # Used to round up to a proper max for the range_color function
    maxKY = (math.ceil(cleanKY['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    kyFig = px.choropleth_mapbox(cleanKY, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='twilight', range_color=(0, maxKY),
                                 color_continuous_midpoint=maxKY / 2,
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.5, center={"lat": 37.526671, "lon": -85.290470},
                                 opacity=0.6, labels={"County": "County"})

    kyFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    kyFig.update_layout(margin={"r": 90, "t": 0, "l": 90, "b": 0})
    return kyFig


# --SUBPLOT--#
def kysub():
    kyFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    kyFIG.add_trace(go.Bar(
        y=cleanKY['County'],
        x=cleanKY['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    kyFIG.add_trace(go.Bar(
        y=cleanKY['County'],
        x=cleanKY['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    kyFIG.add_trace(
        go.Densitymapbox(lat=cleanKY.Latitude, lon=cleanKY.Longitude,
                         z=cleanKY['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='rainbow',
                         visible=True),
        row=2, col=2)
    kyFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanKY[k].tolist() for k in cleanKY.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    kyFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=37.52,
        mapbox_center_lon=-85.29,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Kentucky"
    )
    return kyFIG


# ---------------------------LOUISIANA CHOROPLETH MAP------------------------------#
laDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_laWiki.csv',
    dtype={'fips': str})
cleanLA = laDF.fillna(0)


def lamap():
    # Used to round up to a proper max for the range_color function
    maxLA = (math.ceil(cleanLA['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    laFig = px.choropleth_mapbox(cleanLA, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='bluyl', range_color=(0, maxLA),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.6, center={"lat": 31.220691, "lon": -92.381019},
                                 opacity=0.6, labels={"County": "Parish"})

    laFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    laFig.update_layout(margin={"r": 100, "t": 0, "l": 100, "b": 0})
    return laFig


# --SUBPLOT--#
def lasub():
    laFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    laFIG.add_trace(go.Bar(
        y=cleanLA['County'],
        x=cleanLA['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    laFIG.add_trace(go.Bar(
        y=cleanLA['County'],
        x=cleanLA['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    laFIG.add_trace(go.Bar(
        y=cleanLA['County'],
        x=cleanLA['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(206,42,55, 0.6)',
            line=dict(color='rgba(206,42,55, 1.0)', width=3)
        )
    ))
    laFIG.add_trace(
        go.Densitymapbox(lat=cleanLA.Latitude, lon=cleanLA.Longitude,
                         z=cleanLA['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    laFIG.add_trace(
        go.Table(
            header=dict(
                values=["Parish", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanLA[k].tolist() for k in cleanLA.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    laFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=31.22,
        mapbox_center_lon=-92.38,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Louisiana"
    )
    return laFIG


# ---------------------------MASSACHUSETTS CHOROPLETH MAP------------------------------#
maDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_maNews.csv',
    dtype={'fips': str})
cleanMA = maDF.fillna(0)


def mamap():
    # Used to round up to a proper max for the range_color function
    maxMA = (math.ceil(cleanMA['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    maFig = px.choropleth_mapbox(cleanMA, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='brwnyl', range_color=(0, maxMA),
                                 hover_data=['County', 'Confirmed Cases'],
                                 zoom=6.3, center={"lat": 42.357952, "lon": -72.062769},
                                 opacity=0.6, labels={"County": "County"})

    maFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    maFig.update_layout(margin={"r": 0, "t": 90, "l": 90, "b": 0})
    return maFig


# --SUBPLOT--#
def masub():
    maFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    maFIG.add_trace(go.Bar(
        y=cleanMA['County'],
        x=cleanMA['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    maFIG.add_trace(
        go.Densitymapbox(lat=cleanMA.Latitude, lon=cleanMA.Longitude,
                         z=cleanMA['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    maFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanMA[k].tolist() for k in cleanMA.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    maFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=42.35,
        mapbox_center_lon=-72.06,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Massachusetts"
    )
    return maFIG


# ---------------------------MARYLAND CHOROPLETH MAP------------------------------#
mdDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_mdWiki.csv',
    dtype={'fips': str})
cleanMD = mdDF.fillna(0)


def mdmap():
    # Used to round up to a proper max for the range_color function
    maxMD = (math.ceil(cleanMD['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    mdFig = px.choropleth_mapbox(cleanMD, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='purpor', range_color=(0, maxMD),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=6.4, center={"lat": 39.026261, "lon": -76.808917},
                                 opacity=0.6, labels={"County": "County"})

    mdFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    mdFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return mdFig


# --SUBPLOT--#
def mdsub():
    mdFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    mdFIG.add_trace(go.Bar(
        y=cleanMD['County'],
        x=cleanMD['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    mdFIG.add_trace(go.Bar(
        y=cleanMD['County'],
        x=cleanMD['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    mdFIG.add_trace(
        go.Densitymapbox(lat=cleanMD.Latitude, lon=cleanMD.Longitude,
                         z=cleanMD['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    mdFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanMD[k].tolist() for k in cleanMD.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    mdFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=39.03,
        mapbox_center_lon=-76.81,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Maryland and in Our Nation's Capital"
    )
    return mdFIG


# ---------------------------MAINE CHOROPLETH MAP------------------------------#
meDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_meDDS.csv',
    dtype={'fips': str})
cleanME = meDF.fillna(0)
neuME = cleanME[
    ['County', 'State', 'fips', 'Latitude', 'Longitude', 'Confirmed Cases', 'Deaths', 'Recoveries', 'Hospitalizations']]


def memap():
    # Used to round up to a proper max for the range_color function
    maxME = (math.ceil(neuME['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    meFig = px.choropleth_mapbox(neuME, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='emrld', range_color=(0, maxME),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries', 'Hospitalizations'],
                                 zoom=5.6, center={"lat": 45.274323, "lon": -69.202765},
                                 opacity=0.6, labels={"County": "County"})

    meFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    meFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return meFig


# --SUBPLOT--#
def mesub():
    meFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    meFIG.add_trace(go.Bar(
        y=cleanME['County'],
        x=cleanME['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    meFIG.add_trace(go.Bar(
        y=cleanME['County'],
        x=cleanME['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    meFIG.add_trace(go.Bar(
        y=cleanME['County'],
        x=cleanME['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(102, 25, 105, 0.6)',
            line=dict(color='rgba(102, 25, 105, 1.0)', width=3)
        )
    ))
    meFIG.add_trace(go.Bar(
        y=cleanME['County'],
        x=cleanME['Hospitalizations'],
        name='Hospitalizations',
        orientation='h',
        marker=dict(
            color='rgba(201, 76, 34, 0.6)',
            line=dict(color='rgba(201, 76, 34, 1.0)', width=3)
        )
    ))
    meFIG.add_trace(
        go.Densitymapbox(lat=cleanME.Latitude, lon=cleanME.Longitude,
                         z=cleanME['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    meFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries", "Hospitalizations"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanME[k].tolist() for k in cleanME.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    meFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=45.27,
        mapbox_center_lon=-69.20,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Maine"
    )
    return meFIG


# ---------------------------MICHIGAN CHOROPLETH MAP------------------------------#
miDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_midoh.csv',
    dtype={'fips': str})
cleanMI = miDF.fillna(0)


def mimap():
    # Used to round up to a proper max for the range_color function
    maxMI = (math.ceil(cleanMI['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    miFig = px.choropleth_mapbox(cleanMI, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='spectral_r', range_color=(0, maxMI),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.2, center={"lat": 44.488022, "lon": -84.746015},
                                 opacity=0.6, labels={"County": "County"})

    miFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    miFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return miFig


# --SUBPLOT--#
def misub():
    miFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    miFIG.add_trace(go.Bar(
        y=cleanMI['County'],
        x=cleanMI['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    miFIG.add_trace(go.Bar(
        y=cleanMI['County'],
        x=cleanMI['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    miFIG.add_trace(
        go.Densitymapbox(lat=cleanMI.Latitude, lon=cleanMI.Longitude,
                         z=cleanMI['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='rainbow',
                         visible=True),
        row=2, col=2)
    miFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanMI[k].tolist() for k in cleanMI.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    miFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=44.48,
        mapbox_center_lon=-84.75,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Michigan"
    )
    return miFIG


# ---------------------------MINNESOTA CHOROPLETH MAP------------------------------#
mnDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_mndoh.csv',
    dtype={'fips': str})
cleanMN = mnDF.fillna(0)


def mnmap():
    # Used to round up to a proper max for the range_color function
    maxMN = (math.ceil(cleanMN['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    mnFig = px.choropleth_mapbox(cleanMN, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='tealgrn_r', range_color=(0, maxMN),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.2, center={"lat": 46.441920, "lon": -93.361527},
                                 opacity=0.6, labels={"County": "County"})

    mnFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    mnFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return mnFig


# --SUBPLOT--#
def mnsub():
    mnFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    mnFIG.add_trace(go.Bar(
        y=cleanMN['County'],
        x=cleanMN['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    mnFIG.add_trace(go.Bar(
        y=cleanMN['County'],
        x=cleanMN['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    mnFIG.add_trace(
        go.Densitymapbox(lat=cleanMN.Latitude, lon=cleanMN.Longitude,
                         z=cleanMN['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    mnFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanMN[k].tolist() for k in cleanMN.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    mnFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=46.44,
        mapbox_center_lon=-93.36,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Minnesota"
    )
    return mnFIG


# ---------------------------MISSOURI CHOROPLETH MAP------------------------------#
moDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_modoh.csv',
    dtype={'fips': str})
cleanMO = moDF.fillna(0)


def momap():
    # Used to round up to a proper max for the range_color function
    maxMO = (math.ceil(cleanMO['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    moFig = px.choropleth_mapbox(cleanMO, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='temps', range_color=(0, maxMO),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.5, center={"lat": 38.462767, "lon": -92.574534},
                                 opacity=0.6, labels={"County": "County"})

    moFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    moFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return moFig


# --SUBPLOT--#
def mosub():
    moFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    moFIG.add_trace(go.Bar(
        y=cleanMO['County'],
        x=cleanMO['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    moFIG.add_trace(go.Bar(
        y=cleanMO['County'],
        x=cleanMO['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    moFIG.add_trace(
        go.Densitymapbox(lat=cleanMO.Latitude, lon=cleanMO.Longitude,
                         z=cleanMO['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    moFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanMO[k].tolist() for k in cleanMO.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    moFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=38.46,
        mapbox_center_lon=-92.57,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Missouri"
    )
    return moFIG


# ---------------------------MISSISSIPPI CHOROPLETH MAP------------------------------#
msDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_msdoh.csv',
    dtype={'fips': str})
cleanMS = msDF.fillna(0)


def msmap():
    # Used to round up to a proper max for the range_color function
    maxMS = (math.ceil(cleanMS['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    msFig = px.choropleth_mapbox(cleanMS, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='balance', range_color=(0, maxMS),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.5, center={"lat": 32.940921, "lon": -89.702028},
                                 opacity=0.6, labels={"County": "County"})

    msFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    msFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return msFig


# --SUBPLOT--#
def mssub():
    msFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    msFIG.add_trace(go.Bar(
        y=cleanMS['County'],
        x=cleanMS['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    msFIG.add_trace(go.Bar(
        y=cleanMS['County'],
        x=cleanMS['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    msFIG.add_trace(
        go.Densitymapbox(lat=cleanMS.Latitude, lon=cleanMS.Longitude,
                         z=cleanMS['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    msFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanMS[k].tolist() for k in cleanMS.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    msFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=32.94,
        mapbox_center_lon=-89.70,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Mississippi"
    )
    return msFIG


# ---------------------------MONTANA CHOROPLETH MAP------------------------------#
mtDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_mtdoh.csv',
    dtype={'fips': str})
cleanMT = mtDF.fillna(0)


def mtmap():
    # Used to round up to a proper max for the range_color function
    maxMT = (math.ceil(cleanMT['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    mtFig = px.choropleth_mapbox(cleanMT, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='sunset_r', range_color=(0, maxMT),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5, center={"lat": 47.072205, "lon": -109.398931},
                                 opacity=0.6, labels={"County": "County"})

    mtFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    mtFig.update_layout(margin={"r": 0, "t": 100, "l": 0, "b": 0})
    return mtFig


# --SUBPLOT--#
def mtsub():
    mtFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    mtFIG.add_trace(go.Bar(
        y=cleanMT['County'],
        x=cleanMT['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    mtFIG.add_trace(go.Bar(
        y=cleanMT['County'],
        x=cleanMT['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    mtFIG.add_trace(
        go.Densitymapbox(lat=cleanMT.Latitude, lon=cleanMT.Longitude,
                         z=cleanMT['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    mtFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanMT[k].tolist() for k in cleanMT.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    mtFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=47.07,
        mapbox_center_lon=-109.39,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Montana"
    )
    return mtFIG


# ---------------------------NORTH CAROLINA CHOROPLETH MAP------------------------------#
ncDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_ncdoh.csv',
    dtype={'fips': str})
cleanNC = ncDF.fillna(0)


def ncmap():
    # Used to round up to a proper max for the range_color function
    maxNC = (math.ceil(cleanNC['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    ncFig = px.choropleth_mapbox(cleanNC, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='delta', range_color=(0, maxNC),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.5, center={"lat": 35.591409, "lon": -78.979338},
                                 opacity=0.7, labels={"County": "County"})

    ncFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    ncFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return ncFig


# --SUBPLOT--#
def ncsub():
    ncFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    ncFIG.add_trace(go.Bar(
        y=cleanNC['County'],
        x=cleanNC['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    ncFIG.add_trace(go.Bar(
        y=cleanNC['County'],
        x=cleanNC['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    ncFIG.add_trace(
        go.Densitymapbox(lat=cleanNC.Latitude, lon=cleanNC.Longitude,
                         z=cleanNC['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    ncFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanNC[k].tolist() for k in cleanNC.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    ncFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=35.59,
        mapbox_center_lon=-78.97,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in North Carolina"
    )
    return ncFIG


# ---------------------------NORTH DAKOTA CHOROPLETH MAP------------------------------#
ndDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_ndWiki.csv',
    dtype={'fips': str})
cleanND = ndDF.fillna(0)


def ndmap():
    # Used to round up to a proper max for the range_color function
    maxND = (math.ceil(cleanND['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    ndFig = px.choropleth_mapbox(cleanND, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='tealrose', range_color=(0, maxND),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.7, center={"lat": 47.528438, "lon": -100.445038},
                                 opacity=0.6, labels={"County": "County"})

    ndFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    ndFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return ndFig


# --SUBPLOT--#
def ndsub():
    ndFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    ndFIG.add_trace(go.Bar(
        y=cleanND['County'],
        x=cleanND['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    ndFIG.add_trace(go.Bar(
        y=cleanND['County'],
        x=cleanND['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(194, 255, 210, 0.6)',
            line=dict(color='rgba(194, 255, 210, 1.0)', width=3)
        )
    ))
    ndFIG.add_trace(go.Bar(
        y=cleanND['County'],
        x=cleanND['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(224, 13, 13, 0.6)',
            line=dict(color='rgba(224, 13, 13, 1.0)', width=3)
        )
    ))
    ndFIG.add_trace(
        go.Densitymapbox(lat=cleanND.Latitude, lon=cleanND.Longitude,
                         z=cleanND['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='rainbow',
                         visible=True),
        row=2, col=2)
    ndFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases"
                        ],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanND[k].tolist() for k in cleanND.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    ndFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=47.52,
        mapbox_center_lon=-100.44,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=80,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in North Dakota"
    )
    return ndFIG


# ---------------------------NEBRASKA CHOROPLETH MAP------------------------------#
neDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_neWiki.csv',
    dtype={'fips': str})
cleanNE = neDF.fillna(0)


def nemap():
    # Used to round up to a proper max for the range_color function
    maxNE = (math.ceil(cleanNE['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    neFig = px.choropleth_mapbox(cleanNE, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='teal', range_color=(0, maxNE),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.7, center={"lat": 41.527111, "lon": -99.810728},
                                 opacity=0.6, labels={"County": "County"})

    neFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    neFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return neFig


# --SUBPLOT--#
def nesub():
    neFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    neFIG.add_trace(go.Bar(
        y=cleanNE['County'],
        x=cleanNE['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    neFIG.add_trace(go.Bar(
        y=cleanNE['County'],
        x=cleanNE['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    neFIG.add_trace(
        go.Densitymapbox(lat=cleanNE.Latitude, lon=cleanNE.Longitude,
                         z=cleanNE['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    neFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanNE[k].tolist() for k in cleanNE.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    neFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=41.52,
        mapbox_center_lon=-99.81,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Nebraska"
    )
    return neFIG


# ---------------------------NEW HAMPSHIRE CHOROPLETH MAP-----------------------------#
nhDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_nhNews.csv',
    dtype={'fips': str})
cleanNH = nhDF.fillna(0)


def nhmap():
    # Used to round up to a proper max for the range_color function
    maxNH = (math.ceil(cleanNH['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    nhFig = px.choropleth_mapbox(cleanNH, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='phase', range_color=(0, maxNH),
                                 hover_data=['County', 'Confirmed Cases'],
                                 zoom=6, center={"lat": 43.989517, "lon": -71.469112},
                                 opacity=0.6, labels={"County": "County"})

    nhFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    nhFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return nhFig


# --SUBPLOT--#
def nhsub():
    nhFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    nhFIG.add_trace(go.Bar(
        y=cleanNH['County'],
        x=cleanNH['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    nhFIG.add_trace(
        go.Densitymapbox(lat=cleanNH.Latitude, lon=cleanNH.Longitude,
                         z=cleanNH['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    nhFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases"
                        ],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanNH[k].tolist() for k in cleanNH.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    nhFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=43.99,
        mapbox_center_lon=-71.469,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in New Hampshire"
    )
    return nhFIG


# ---------------------------NEW JERSEY CHOROPLETH MAP-----------------------------#
njDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_njWiki.csv',
    dtype={'fips': str})
cleanNJ = njDF.fillna(0)


def njmap():
    # Used to round up to a proper max for the range_color function
    maxNJ = (math.ceil(cleanNJ['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    njFig = px.choropleth_mapbox(cleanNJ, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='curl', range_color=(0, maxNJ),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=6.2, center={"lat": 40.267895, "lon": -74.412674},
                                 opacity=0.6, labels={"County": "County"})

    njFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    njFig.update_layout(margin={"r": 100, "t": 0, "l": 100, "b": 0})
    return njFig


# --SUBPLOT--#
def njsub():
    njFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    njFIG.add_trace(go.Bar(
        y=cleanNJ['County'],
        x=cleanNJ['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    njFIG.add_trace(go.Bar(
        y=cleanNJ['County'],
        x=cleanNJ['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    njFIG.add_trace(go.Bar(
        y=cleanNJ['County'],
        x=cleanNJ['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(147, 5, 230, 0.6)',
            line=dict(color='rgba(147, 5, 230, 1.0)', width=3)
        )
    ))
    njFIG.add_trace(
        go.Densitymapbox(lat=cleanNJ.Latitude, lon=cleanNJ.Longitude,
                         z=cleanNJ['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    njFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanNJ[k].tolist() for k in cleanNJ.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    njFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=40.267,
        mapbox_center_lon=-74.41,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in New Jersey"
    )
    return njFIG


# ---------------------------NEW MEXICO CHOROPLETH MAP-----------------------------#
nmDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_nmWiki.csv',
    dtype={'fips': str})
cleanNM = nmDF.fillna(0)


def nmmap():
    # Used to round up to a proper max for the range_color function
    maxNM = (math.ceil(cleanNM['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    nmFig = px.choropleth_mapbox(cleanNM, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='purp_r', range_color=(0, maxNM),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.3, center={"lat": 34.481461, "lon": -106.059789},
                                 opacity=0.7, labels={"County": "County"})

    nmFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    nmFig.update_layout(margin={"r": 100, "t": 0, "l": 100, "b": 0})
    return nmFig


# --SUBPLOT--#
def nmsub():
    nmFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    nmFIG.add_trace(go.Bar(
        y=cleanNM['County'],
        x=cleanNM['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    nmFIG.add_trace(go.Bar(
        y=cleanNM['County'],
        x=cleanNM['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    nmFIG.add_trace(
        go.Densitymapbox(lat=cleanNM.Latitude, lon=cleanNM.Longitude,
                         z=cleanNM['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)

    nmFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanNM[k].tolist() for k in cleanNM.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    nmFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=34.48,
        mapbox_center_lon=-106.059,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in New Mexico"
    )
    return nmFIG


# ---------------------------NEVADA CHOROPLETH MAP-----------------------------#
nvDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_nvNews.csv',
    dtype={'fips': str})
cleanNV = nvDF.fillna(0)


def nvmap():
    # Used to round up to a proper max for the range_color function
    maxNV = (math.ceil(cleanNV['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    nvFig = px.choropleth_mapbox(cleanNV, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='curl', range_color=(0, maxNV),
                                 hover_data=['County', 'Confirmed Cases'],
                                 zoom=5, center={"lat": 38.502032, "lon": -117.023060},
                                 opacity=0.6, labels={"County": "County"})

    nvFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    nvFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return nvFig


# --SUBPLOT--#
def nvsub():
    nvFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    nvFIG.add_trace(go.Bar(
        y=cleanNV['County'],
        x=cleanNV['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    nvFIG.add_trace(
        go.Densitymapbox(lat=cleanNV.Latitude, lon=cleanNV.Longitude,
                         z=cleanNV['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    nvFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases"
                        ],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanNV[k].tolist() for k in cleanNV.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    nvFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=38.502,
        mapbox_center_lon=-117.023,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Nevada"
    )
    return nvFIG


# ---------------------------NEW YORK CHOROPLETH MAP-----------------------------#
nyDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_nydoh.csv',
    dtype={'fips': str})
cleanNY = nyDF.fillna(0)


def nymap():
    # Used to round up to a proper max for the range_color function
    maxNY = (math.ceil(cleanNY['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    nyFig = px.choropleth_mapbox(cleanNY, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='geyser', range_color=(0, maxNY),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.3, center={"lat": 42.917153, "lon": -75.519960},
                                 opacity=0.6, labels={"County": "County"})

    nyFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    nyFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return nyFig


# --SUBPLOT--#
def nysub():
    nyFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    nyFIG.add_trace(go.Bar(
        y=cleanNY['County'],
        x=cleanNY['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    nyFIG.add_trace(go.Bar(
        y=cleanNY['County'],
        x=cleanNY['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    nyFIG.add_trace(go.Bar(
        y=cleanNY['County'],
        x=cleanNY['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(147, 5, 230, 0.6)',
            line=dict(color='rgba(147, 5, 230, 1.0)', width=3)
        )
    ))
    nyFIG.add_trace(
        go.Densitymapbox(lat=cleanNY.Latitude, lon=cleanNY.Longitude,
                         z=cleanNY['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    nyFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanNY[k].tolist() for k in cleanNY.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    nyFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=42.91,
        mapbox_center_lon=-75.52,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in New York"
    )
    return nyFIG


# ---------------------------OHIO CHOROPLETH MAP-----------------------------#
ohDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_ohWiki.csv',
    dtype={'fips': str})
cleanOH = ohDF.fillna(0)


def ohmap():
    # Used to round up to a proper max for the range_color function
    maxOH = (math.ceil(cleanOH['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    ohFig = px.choropleth_mapbox(cleanOH, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='tealrose', range_color=(0, maxOH),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.7, center={"lat": 40.300325, "lon": -82.700806},
                                 opacity=0.6, labels={"County": "County"})

    ohFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    ohFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return ohFig


# --SUBPLOT--#
def ohsub():
    ohFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    ohFIG.add_trace(go.Bar(
        y=cleanOH['County'],
        x=cleanOH['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    ohFIG.add_trace(go.Bar(
        y=cleanOH['County'],
        x=cleanOH['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    ohFIG.add_trace(
        go.Densitymapbox(lat=cleanOH.Latitude, lon=cleanOH.Longitude,
                         z=cleanOH['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    ohFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanOH[k].tolist() for k in cleanOH.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    ohFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=40.30,
        mapbox_center_lon=-82.70,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Ohio"
    )
    return ohFIG


# ---------------------------OKLAHOMA CHOROPLETH MAP-----------------------------#
okDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_okdoh.csv',
    dtype={'fips': str})
cleanOK = okDF.fillna(0)


def okmap():
    # Used to round up to a proper max for the range_color function
    maxOK = (math.ceil(cleanOK['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    okFig = px.choropleth_mapbox(cleanOK, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='haline', range_color=(0, maxOK),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.5, center={"lat": 35.732412, "lon": -97.386798},
                                 opacity=0.6, labels={"County": "County"})

    okFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    okFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return okFig


# --SUBPLOT--#
def oksub():
    okFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    okFIG.add_trace(go.Bar(
        y=cleanOK['County'],
        x=cleanOK['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    okFIG.add_trace(go.Bar(
        y=cleanOK['County'],
        x=cleanOK['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    okFIG.add_trace(go.Bar(
        y=cleanOK['County'],
        x=cleanOK['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(147, 5, 230, 0.6)',
            line=dict(color='rgba(147, 5, 230, 1.0)', width=3)
        )
    ))
    okFIG.add_trace(
        go.Densitymapbox(lat=cleanOK.Latitude, lon=cleanOK.Longitude,
                         z=cleanOK['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    okFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanOK[k].tolist() for k in cleanOK.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    okFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=35.73,
        mapbox_center_lon=-97.38,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Oklahoma"
    )
    return okFIG


# ---------------------------OREGON CHOROPLETH MAP-----------------------------#
orDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_ordoh.csv',
    dtype={'fips': str})
cleanOR = orDF.fillna(0)


def ormap():
    # Used to round up to a proper max for the range_color function
    maxOR = (math.ceil(cleanOR['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    orFig = px.choropleth_mapbox(cleanOR, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='redor', range_color=(0, maxOR),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.3, center={"lat": 43.940439, "lon": -120.605284},
                                 opacity=0.6, labels={"County": "County"})

    orFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    orFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return orFig


# --SUBPLOT--#
def orsub():
    orFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    orFIG.add_trace(go.Bar(
        y=cleanOR['County'],
        x=cleanOR['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    orFIG.add_trace(go.Bar(
        y=cleanOR['County'],
        x=cleanOR['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    orFIG.add_trace(
        go.Densitymapbox(lat=cleanOR.Latitude, lon=cleanOR.Longitude,
                         z=cleanOR['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    orFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanOR[k].tolist() for k in cleanOR.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    orFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=43.94,
        mapbox_center_lon=-120.61,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Oregon"
    )
    return orFIG


# ---------------------------PENNSYLVANIA CHOROPLETH MAP-----------------------------#
paDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_padoh.csv',
    dtype={'fips': str})
cleanPA = paDF.fillna(0)


def pamap():
    # Used to round up to a proper max for the range_color function
    maxPA = (math.ceil(cleanPA['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    paFig = px.choropleth_mapbox(cleanPA, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='sunset', range_color=(0, maxPA),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.5, center={"lat": 40.896699, "lon": -77.838908},
                                 opacity=0.6, labels={"County": "County"})

    paFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    paFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return paFig


# --SUBPLOT--#
def pasub():
    paFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    paFIG.add_trace(go.Bar(
        y=cleanPA['County'],
        x=cleanPA['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    paFIG.add_trace(go.Bar(
        y=cleanPA['County'],
        x=cleanPA['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    paFIG.add_trace(
        go.Densitymapbox(lat=cleanPA.Latitude, lon=cleanPA.Longitude,
                         z=cleanPA['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    paFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanPA[k].tolist() for k in cleanPA.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    paFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=40.89,
        mapbox_center_lon=-77.84,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Pennsylvania"
    )
    return paFIG


##---------------------------PUERTO RICO CHOROPLETH MAP-----------------------------#

prDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_prWiki.csv',
    encoding='Latin-1', dtype={'fips': str})
cleanPR = prDF.fillna(0)


def prmap():
    # Used to round up to a proper max for the range_color function
    maxPR = (math.ceil(cleanPR['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    prFig = px.choropleth_mapbox(cleanPR, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='sunset', range_color=(0, maxPR),
                                 hover_data=['County', 'Confirmed Cases'],
                                 zoom=6, center={"lat": 18.192825, "lon": -66.448568},
                                 opacity=0.6, labels={"County": "Municipality"})

    prFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    prFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return prFig


# --SUBPLOT--#
def prsub():
    prFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    prFIG.add_trace(go.Bar(
        y=cleanPR['County'],
        x=cleanPR['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )

    prFIG.add_trace(
        go.Densitymapbox(lat=cleanPR.Latitude, lon=cleanPR.Longitude,
                         z=cleanPR['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    prFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanPR[k].tolist() for k in cleanPR.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    prFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=18.19,
        mapbox_center_lon=-66.45,
        mapbox=dict(
            zoom=5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Puerto Rico"
    )
    return prFIG


# -----------------------RHODE ISLAND CHOROPLETH MAP----------------------------#
riDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_riNews.csv',
    dtype={'fips': str})
cleanRI = riDF.fillna(0)


def rimap():
    # Used to round up to a proper max for the range_color function
    maxRI = (math.ceil(cleanRI['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    riFig = px.choropleth_mapbox(cleanRI, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='phase', range_color=(0, maxRI),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=7.5, center={"lat": 41.640049, "lon": -71.524728},
                                 opacity=0.6, labels={"County": "County"})

    riFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    riFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return riFig


# --SUBPLOT--#
def risub():
    riFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    riFIG.add_trace(go.Bar(
        y=cleanRI['County'],
        x=cleanRI['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    riFIG.add_trace(go.Bar(
        y=cleanRI['County'],
        x=cleanRI['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    riFIG.add_trace(
        go.Densitymapbox(lat=cleanRI.Latitude, lon=cleanRI.Longitude,
                         z=cleanRI['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    riFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanRI[k].tolist() for k in cleanRI.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    riFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=41.64,
        mapbox_center_lon=-71.52,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Rhode Island"
    )
    return riFIG


# -----------------------SOUTH CAROLINA CHOROPLETH MAP----------------------------#
scDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_scWiki.csv',
    dtype={'fips': str})
cleanSC = scDF.fillna(0)


def scmap():
    # Used to round up to a proper max for the range_color function
    maxSC = (math.ceil(cleanSC['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    scFig = px.choropleth_mapbox(cleanSC, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='tealgrn', range_color=(0, maxSC),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=6, center={"lat": 33.877856, "lon": -80.864605},
                                 opacity=0.6, labels={"County": "County"})

    scFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    scFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return scFig


# --SUBPLOT--#
def scsub():
    scFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    scFIG.add_trace(go.Bar(
        y=cleanSC['County'],
        x=cleanSC['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    scFIG.add_trace(go.Bar(
        y=cleanSC['County'],
        x=cleanSC['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    scFIG.add_trace(
        go.Densitymapbox(lat=cleanSC.Latitude, lon=cleanSC.Longitude,
                         z=cleanSC['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    scFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanSC[k].tolist() for k in cleanSC.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    scFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=33.87,
        mapbox_center_lon=-80.86,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in South Carolina"
    )
    return scFIG


# -----------------------SOUTH DAKOTA CHOROPLETH MAP----------------------------#
sdDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_sdWiki.csv',
    dtype={'fips': str})
cleanSD = sdDF.fillna(0)


def sdmap():
    # Used to round up to a proper max for the range_color function
    maxSD = (math.ceil(cleanSD['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    sdFig = px.choropleth_mapbox(cleanSD, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='cividis', range_color=(0, maxSD),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.3, center={"lat": 44.576328, "lon": -100.291920},
                                 opacity=0.6)

    sdFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    sdFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return sdFig


# --SUBPLOT--#
def sdsub():
    sdFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    sdFIG.add_trace(go.Bar(
        y=cleanSD['County'],
        x=cleanSD['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    sdFIG.add_trace(go.Bar(
        y=cleanSD['County'],
        x=cleanSD['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    sdFIG.add_trace(go.Bar(
        y=cleanSD['County'],
        x=cleanSD['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(147, 5, 230, 0.6)',
            line=dict(color='rgba(147, 5, 230, 1.0)', width=3)
        )
    ))
    sdFIG.add_trace(
        go.Densitymapbox(lat=cleanSD.Latitude, lon=cleanSD.Longitude,
                         z=cleanSD['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    sdFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanSD[k].tolist() for k in cleanSD.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    sdFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=44.57,
        mapbox_center_lon=-100.29,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in South Dakota"
    )
    return sdFIG


# -----------------------TENNESSEE CHOROPLETH MAP----------------------------#
tnDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_tnWiki.csv',
    dtype={'fips': str})
cleanTN = tnDF.fillna(0)


def tnmap():
    # Used to round up to a proper max for the range_color function
    maxTN = (math.ceil(cleanTN['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    tnFig = px.choropleth_mapbox(cleanTN, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='matter', range_color=(0, maxTN),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.7, center={"lat": 35.866924, "lon": -85.881291},
                                 opacity=0.6, labels={"County": "County"})

    tnFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    tnFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return tnFig


# --SUBPLOT--#
def tnsub():
    tnFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    tnFIG.add_trace(go.Bar(
        y=cleanTN['County'],
        x=cleanTN['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    tnFIG.add_trace(go.Bar(
        y=cleanTN['County'],
        x=cleanTN['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    tnFIG.add_trace(go.Bar(
        y=cleanTN['County'],
        x=cleanTN['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(147, 5, 230, 0.6)',
            line=dict(color='rgba(147, 5, 230, 1.0)', width=3)
        )
    ))
    tnFIG.add_trace(
        go.Densitymapbox(lat=cleanTN.Latitude, lon=cleanTN.Longitude,
                         z=cleanTN['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    tnFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanTN[k].tolist() for k in cleanTN.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    njFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=35.86,
        mapbox_center_lon=-85.88,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Tennessee"
    )
    return tnFIG


# -----------------------TEXAS CHOROPLETH MAP----------------------------#
txDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_txgit.csv',
    dtype={'fips': str})
cleanTX = txDF.fillna(0)


def txmap():
    # Used to round up to a proper max for the range_color function
    maxTX = (math.ceil(cleanTX['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    txFig = px.choropleth_mapbox(cleanTX, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='agsunset', range_color=(0, maxTX),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=4, center={"lat": 31.364552, "lon": -99.161239},
                                 opacity=0.6, labels={"County": "County"})

    txFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    txFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return txFig


# --SUBPLOT--#
def txsub():
    txFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    txFIG.add_trace(go.Bar(
        y=cleanTX['County'],
        x=cleanTX['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    txFIG.add_trace(go.Bar(
        y=cleanTX['County'],
        x=cleanTX['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    txFIG.add_trace(go.Bar(
        y=cleanTX['County'],
        x=cleanTX['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(147, 5, 230, 0.6)',
            line=dict(color='rgba(147, 5, 230, 1.0)', width=3)
        )
    ))
    txFIG.add_trace(
        go.Densitymapbox(lat=cleanTX.Latitude, lon=cleanTX.Longitude,
                         z=cleanTX['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    txFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanTX[k].tolist() for k in cleanTX.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    txFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=31.36,
        mapbox_center_lon=-99.161,
        mapbox=dict(
            zoom=4
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Texas"
    )
    return txFIG


# -----------------------UTAH CHOROPLETH MAP----------------------------#
utDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_utNews.csv',
    dtype={'fips': str})
cleanUT = utDF.fillna(0)
cleanUT = cleanUT[
    ['County', 'State', 'fips', 'Latitude', 'Longitude', 'Confirmed Cases', 'Deaths', 'Recoveries', 'Hospitalizations']]


def utmap():
    # Used to round up to a proper max for the range_color function
    maxUT = (math.ceil(cleanUT['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    utFig = px.choropleth_mapbox(cleanUT, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='tealrose', range_color=(0, maxUT),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries', 'Hospitalizations'],
                                 zoom=5.2, center={"lat": 39.323777, "lon": -111.678222},
                                 opacity=0.6, labels={"County": "County"})

    utFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    utFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return utFig


# --SUBPLOT--#
def utsub():
    utFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    utFIG.add_trace(go.Bar(
        y=cleanUT['County'],
        x=cleanUT['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    utFIG.add_trace(go.Bar(
        y=cleanUT['County'],
        x=cleanUT['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    utFIG.add_trace(go.Bar(
        y=cleanUT['County'],
        x=cleanUT['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(147, 5, 230, 0.6)',
            line=dict(color='rgba(147, 5, 230, 1.0)', width=3)
        )
    ))
    utFIG.add_trace(go.Bar(
        y=cleanUT['County'],
        x=cleanUT['Hospitalizations'],
        name='Hospitalizations',
        orientation='h',
        marker=dict(
            color='rgba(245, 71, 83, 0.6)',
            line=dict(color='rgba(245, 71, 83, 1.0)', width=3)
        )
    ))
    utFIG.add_trace(
        go.Densitymapbox(lat=cleanUT.Latitude, lon=cleanUT.Longitude,
                         z=cleanUT['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    utFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries", "Hospitalizations"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanUT[k].tolist() for k in cleanUT.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    utFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=39.32,
        mapbox_center_lon=-111.678,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Utah"
    )
    return utFIG


# -----------------------VIRGINIA CHOROPLETH MAP----------------------------#
vaDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_vaWiki.csv',
    dtype={'fips': str})
cleanVA = vaDF.fillna(0)


def vamap():
    # Used to round up to a proper max for the range_color function
    maxVA = (math.ceil(cleanVA['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    vaFig = px.choropleth_mapbox(cleanVA, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='matter', range_color=(0, maxVA),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Hospitalizations'],
                                 zoom=5.3, center={"lat": 37.510857, "lon": -78.666367},
                                 opacity=0.6, labels={"County": "County"})

    vaFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    vaFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return vaFig


# --SUBPLOT--#
def vasub():
    vaFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    vaFIG.add_trace(go.Bar(
        y=cleanVA['County'],
        x=cleanVA['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    vaFIG.add_trace(go.Bar(
        y=cleanVA['County'],
        x=cleanVA['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    vaFIG.add_trace(go.Bar(
        y=cleanVA['County'],
        x=cleanVA['Hospitalizations'],
        name='Hospitalizations',
        orientation='h',
        marker=dict(
            color='rgba(245, 71, 83, 0.6)',
            line=dict(color='rgba(245, 71, 83, 1.0)', width=3)
        )
    ))
    vaFIG.add_trace(
        go.Densitymapbox(lat=cleanVA.Latitude, lon=cleanVA.Longitude,
                         z=cleanVA['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    vaFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Hospitalizations"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanVA[k].tolist() for k in cleanVA.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    vaFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=37.52,
        mapbox_center_lon=-78.666,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Virginia"
    )
    return vaFIG


# -----------------------VERMONT CHOROPLETH MAP----------------------------#
vtDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_vtWiki.csv',
    dtype={'fips': str})
cleanVT = vtDF.fillna(0)


def vtmap():
    # Used to round up to a proper max for the range_color function
    maxVT = (math.ceil(cleanVT['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    vtFig = px.choropleth_mapbox(cleanVT, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='purp', range_color=(0, maxVT),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=6, center={"lat": 44.075207, "lon": -72.735624},
                                 opacity=0.6, labels={"County": "County"})

    vtFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    vtFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return vtFig


# --SUBPLOT--#
def vtsub():
    vtFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    vtFIG.add_trace(go.Bar(
        y=cleanVT['County'],
        x=cleanVT['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    vtFIG.add_trace(go.Bar(
        y=cleanVT['County'],
        x=cleanVT['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    vtFIG.add_trace(go.Bar(
        y=cleanVT['County'],
        x=cleanVT['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(147, 5, 230, 0.6)',
            line=dict(color='rgba(147, 5, 230, 1.0)', width=3)
        )
    ))
    vtFIG.add_trace(
        go.Densitymapbox(lat=cleanVT.Latitude, lon=cleanVT.Longitude,
                         z=cleanVT['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    vtFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanVT[k].tolist() for k in cleanVT.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    vtFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=44.07,
        mapbox_center_lon=-72.73,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in Vermont"
    )
    return vtFIG


# -----------------------WASHINGTON CHOROPLETH MAP----------------------------#
waDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_waWiki.csv',
    dtype={'fips': str})
cleanWA = waDF.fillna(0)


def wamap():
    # Used to round up to a proper max for the range_color function
    maxWA = (math.ceil(cleanWA['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    waFig = px.choropleth_mapbox(cleanWA, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='temps', range_color=(0, maxWA),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.3, center={"lat": 47.572970, "lon": -120.320940},
                                 opacity=0.65, labels={"County": "County"})

    waFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    waFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return waFig


# --SUBPLOT--#
def wasub():
    waFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    waFIG.add_trace(go.Bar(
        y=cleanWA['County'],
        x=cleanWA['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    waFIG.add_trace(go.Bar(
        y=cleanWA['County'],
        x=cleanWA['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    waFIG.add_trace(
        go.Densitymapbox(lat=cleanWA.Latitude, lon=cleanWA.Longitude,
                         z=cleanWA['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    waFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanWA[k].tolist() for k in cleanWA.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    waFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=47.57,
        mapbox_center_lon=-120.32,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in the State of Washington"
    )
    return waFIG


# -----------------------WISCONSIN CHOROPLETH MAP----------------------------#
wiDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_widoh.csv',
    dtype={'fips': str})
cleanWI = wiDF.fillna(0)


def wimap():
    # Used to round up to a proper max for the range_color function
    maxWI = (math.ceil(cleanWI['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    wiFig = px.choropleth_mapbox(cleanWI, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='tropic', range_color=(0, maxWI),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.3, center={"lat": 44.672245, "lon": -89.878727},
                                 opacity=0.6, labels={"County": "County"})

    wiFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    wiFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return wiFig


# --SUBPLOT--#
def wisub():
    wiFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    wiFIG.add_trace(go.Bar(
        y=cleanWI['County'],
        x=cleanWI['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    wiFIG.add_trace(go.Bar(
        y=cleanWI['County'],
        x=cleanWI['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    wiFIG.add_trace(
        go.Densitymapbox(lat=cleanWI.Latitude, lon=cleanWI.Longitude,
                         z=cleanWI['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    wiFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanWI[k].tolist() for k in cleanWI.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    wiFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=44.67,
        mapbox_center_lon=-89.88,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in the State of Wisconsin"
    )
    return wiFIG


# -----------------------WEST VIRGINIA CHOROPLETH MAP----------------------------#
wvDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_wvWiki.csv',
    dtype={'fips': str})
cleanWV = wvDF.fillna(0)


def wvmap():
    # Used to round up to a proper max for the range_color function
    maxWV = (math.ceil(cleanWV['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    wvFig = px.choropleth_mapbox(cleanWV, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='thermal_r', range_color=(0, maxWV),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths'],
                                 zoom=5.5, center={"lat": 38.718442, "lon": -80.735224},
                                 opacity=0.7, labels={"County": "County"})

    wvFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    wvFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return wvFig


# --SUBPLOT--#
def wvsub():
    wvFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    wvFIG.add_trace(go.Bar(
        y=cleanWV['County'],
        x=cleanWV['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    wvFIG.add_trace(go.Bar(
        y=cleanWV['County'],
        x=cleanWV['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    wvFIG.add_trace(
        go.Densitymapbox(lat=cleanWV.Latitude, lon=cleanWV.Longitude,
                         z=cleanWV['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    wvFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanWV[k].tolist() for k in cleanWV.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    wvFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=38.72,
        mapbox_center_lon=-80.73,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in the State of West Virginia"
    )
    return wvFIG


# -----------------------WYOMING CHOROPLETH MAP----------------------------#
wyDF = pd.read_csv(
    'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Visual-Tool/master/Web%20Scraped%20Docs/US%20States/COVID-19_cases_wyWiki.csv',
    dtype={'fips': str})
cleanWY = wyDF.fillna(0)


def wymap():
    # Used to round up to a proper max for the range_color function
    maxWY = (math.ceil(cleanWY['Confirmed Cases'].max() / 50.0) * 50.0) + 150

    wyFig = px.choropleth_mapbox(cleanWY, geojson=counties, locations='fips', color='Confirmed Cases',
                                 color_continuous_scale='mygbm', range_color=(0, maxWY),
                                 hover_data=['County', 'Confirmed Cases', 'Deaths', 'Recoveries'],
                                 zoom=5.2, center={"lat": 42.999627, "lon": -107.551451},
                                 opacity=0.6, labels={"County": "County"})

    wyFig.update_layout(mapbox_style="satellite-streets",
                        mapbox_accesstoken='pk.eyJ1IjoibGFlc3RyeWdvbmVzIiwiYSI6ImNrOHlpdHo5bjA1dzYzZm5yZGduMTBvZTcifQ.ztpWyjPI2kHzwSbcdYrj7w')
    wyFig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return wyFig


# --SUBPLOT--#
def wysub():
    wyFIG = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.6],
        row_heights=[0.6, 0.6],
        vertical_spacing=0.03,
        horizontal_spacing=0.03,
        specs=[[{"type": "table", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "Densitymapbox"}]])

    wyFIG.add_trace(go.Bar(
        y=cleanWY['County'],
        x=cleanWY['Confirmed Cases'],
        name='Confirmed Cases',
        orientation='h',
        marker=dict(
            color='rgba(59, 82, 105, 0.6)',
            line=dict(color='rgba(59, 82, 105, 1.0)', width=3)
        )
    ),
        row=2, col=1
    )
    wyFIG.add_trace(go.Bar(
        y=cleanWY['County'],
        x=cleanWY['Deaths'],
        name='Deaths',
        orientation='h',
        marker=dict(
            color='rgba(160, 184, 152, 0.6)',
            line=dict(color='rgba(160, 184, 152, 1.0)', width=3)
        )
    ))
    wyFIG.add_trace(go.Bar(
        y=cleanWY['County'],
        x=cleanWY['Recoveries'],
        name='Recoveries',
        orientation='h',
        marker=dict(
            color='rgba(171, 0, 0, 0.6)',
            line=dict(color='rgba(171, 0, 0, 1.0)', width=3)
        )
    ))
    wyFIG.add_trace(
        go.Densitymapbox(lat=cleanWY.Latitude, lon=cleanWY.Longitude,
                         z=cleanWY['Confirmed Cases'], radius=25,
                         showscale=False, colorscale='picnic',
                         visible=True),
        row=2, col=2)
    wyFIG.add_trace(
        go.Table(
            header=dict(
                values=["County", "State", "fips",
                        "Latitude", "Longitude", "Confirmed Cases",
                        "Deaths", "Recoveries"],
                line_color='darkslategray',
                fill_color='grey',
                font=dict(color='white', size=14, family='PT Sans Narrow'),
                align="left"
            ),
            cells=dict(
                values=[cleanWY[k].tolist() for k in cleanWY.columns[:]],
                fill_color='black',
                line_color='white',
                font=dict(color='white', size=12, family='Gravitas One'),
                align="left")
        ),
        row=1, col=1
    )
    wyFIG.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=42.999,
        mapbox_center_lon=-107.55,
        mapbox=dict(
            zoom=4.5
        ),
        barmode='stack',
        height=800,
        width=1100,
        showlegend=True,
        title_text="COVID-19's Impact in the State of Wyoming"
    )
    return wyFIG


# ----Prediction Model Graphs---------------------------------------------------------------------------------
# Confirmed/death prediction model for the US
def mortModel():
    mortAct = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/Death_Actual.csv'
    mortPre = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/Death_Predict.csv'

    mortA = pd.read_csv(mortAct)
    mortP = pd.read_csv(mortPre)

    mA = mortA.rename(columns={mortA.columns[0]: 'index'})
    mP = mortP.rename(columns={mortP.columns[0]: 'index'})

    plt = go.Figure()
    plt.add_trace(go.Scatter(x=mA['Actual Confirmed'], y=mA['Actual Deaths'],
                             mode="markers", name="Actual",
                             marker_color="rgba(255, 64, 64,.8)"))
    plt.add_trace(go.Scatter(
        x=mP['Predicted Confirmed'], y=mP['Predicted Deaths'],
        mode="lines",
        line=go.scatter.Line(color="rgba(214, 242, 56,.8)"), name="Predict"))
    plt.update_layout(xaxis={"title": "Confirmed Cases"},
                      yaxis={"title": "Deaths"},
                      title="US Prediction Model: Confirmed/Deaths",
                      plot_bgcolor="black"
                      )
    return plt


# Confirmed/Recovery prediction model for the US

def recModel():
    recAct = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/Recovered_Actual.csv'
    recPre = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/Recovered_Predict.csv'

    recA = pd.read_csv(recAct)
    recP = pd.read_csv(recPre)

    rA = recA.rename(columns={recA.columns[0]: 'index'})
    rP = recP.rename(columns={recP.columns[0]: 'index'})

    rose = go.Figure()
    rose.add_trace(go.Scatter(x=rA['Actual Confirmed'], y=rA['Actual Recovered'],
                              mode="markers", name="Actual",
                              marker_color="rgba(0,255,188,.8)"))
    rose.add_trace(go.Scatter(
        x=rP['Predicted Confirmed'], y=rP['Predicted Recovered'],
        mode="lines",
        line=go.scatter.Line(color="MediumPurple"), name="Predict"))
    rose.update_layout(xaxis={"title": "Confirmed Cases"},
                       yaxis={"title": "Recovered"},
                       title="US Prediction Model: Confirmed/Recoveries",
                       plot_bgcolor="black"
                       )
    return rose


def italiaModel():
    itAct = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/ItalyAct.csv'
    itPre = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/ItalyPred.csv'

    iA = pd.read_csv(itAct)
    iP = pd.read_csv(itPre)

    sophia = go.Figure()
    sophia.add_trace(go.Scatter(x=iA['Actual Confirmed'], y=iA['Actual Deaths'],
                                mode="markers", name="Actual",
                                marker_color="rgba(0,147,68,.8)"))
    sophia.add_trace(go.Scatter(
        x=iP['Predicted Confirmed'], y=iP['Predicted Deaths'],
        mode="lines",
        line=go.scatter.Line(color="rgba(207,39,52,.8)"), name="Predict"))
    sophia.update_layout(xaxis={"title": "Confirmed Cases"},
                         yaxis={"title": "Deaths"},
                         title="Italy Prediction Model",
                         plot_bgcolor="black"
                         )
    return sophia


def newZeaModel():
    nzAct = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/NewZealandAct.csv'
    nzPre = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/NewZealandPred.csv'

    zA = pd.read_csv(nzAct)
    zP = pd.read_csv(nzPre)

    maori = go.Figure()
    maori.add_trace(go.Scatter(x=zA['Actual Confirmed'], y=zA['Actual Deaths'],
                               mode="markers", name="Actual",
                               marker_color="white"))
    maori.add_trace(go.Scatter(
        x=zP['Predicted Confirmed'], y=zP['Predicted Deaths'],
        mode="lines",
        line=go.scatter.Line(color="red"), name="Predict"))
    maori.update_layout(xaxis={"title": "Confirmed Cases"},
                        yaxis={"title": "Deaths"},
                        title="New Zealand Prediction Model",
                        plot_bgcolor="black"
                        )
    return maori


def southAfricaModel():
    saAct = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/SouthAfricaAct.csv'
    saPre = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/SouthAfricaPred.csv'

    sA = pd.read_csv(saAct)
    sP = pd.read_csv(saPre)

    noah = go.Figure()
    noah.add_trace(go.Scatter(x=sA['Actual Confirmed'], y=sA['Actual Deaths'],
                              mode="markers", name="Actual",
                              marker_color="rgba(255,183,10,.8)"))
    noah.add_trace(go.Scatter(
        x=sP['Predicted Confirmed'], y=sP['Predicted Deaths'],
        mode="lines",
        line=go.scatter.Line(color="rgba(113, 242, 65,.8)"), name="Predict"))
    noah.update_layout(xaxis={"title": "Confirmed Cases"},
                       yaxis={"title": "Deaths"},
                       title="South Africa Prediction Model",
                       plot_bgcolor="black"
                       )
    return noah


def skoreaModel():
    skAct = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/SouthKoreaAct.csv'
    skPre = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/SouthKoreaPred.csv'

    kA = pd.read_csv(skAct)
    kP = pd.read_csv(skPre)

    ssingssing = go.Figure()
    ssingssing.add_trace(go.Scatter(x=kA['Actual Confirmed'], y=kA['Actual Deaths'],
                                    mode="markers", name="Actual",
                                    marker_color="rgba(122, 179, 255,.9)"))
    ssingssing.add_trace(go.Scatter(
        x=kP['Predicted Confirmed'], y=kP['Predicted Deaths'],
        mode="lines",
        line=go.scatter.Line(color="rgba(206,42,55,.9)"), name="Predict"))
    ssingssing.update_layout(xaxis={"title": "Confirmed Cases"},
                             yaxis={"title": "Deaths"},
                             title="South Korea Prediction Model",
                             plot_bgcolor="black"
                             )
    return ssingssing


def brazilModel():
    brAct = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/BrazilAct.csv'
    brPre = 'https://raw.githubusercontent.com/ThanatoSohne/COVID-19-Outbreak-Visualization-Tool/master/BrazilPred.csv'

    bA = pd.read_csv(brAct)
    bP = pd.read_csv(brPre)

    yanomami = go.Figure()
    yanomami.add_trace(go.Scatter(x=bA['Actual Confirmed'], y=bA['Actual Deaths'],
                                  mode="markers", name="Actual",
                                  marker_color="rgba(185,195,217,.9)"))
    yanomami.add_trace(go.Scatter(
        x=bP['Predicted Confirmed'], y=bP['Predicted Deaths'],
        mode="lines",
        line=go.scatter.Line(color="rgba(254,223,0,.8)"), name="Predict"))
    yanomami.update_layout(xaxis={"title": "Confirmed Cases"},
                           yaxis={"title": "Deaths"},
                           title="Brazil Prediction Model",
                           plot_bgcolor="black"
                           )
    return yanomami


# -------------------------------------------------------------------------------------------------#

# boots="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
app.config.suppress_callback_exceptions = True
server = app.server

CONTENT_STYLE = {
    "margin": "auto",
    "padding": "2rem 1rem",
    "width": "90%",
    "background-color": "rgb(232, 228, 227)",
}

dropdown = dbc.Row([
    dbc.Col(
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Home", href="/page-1", id="page-1-link"),
                dbc.DropdownMenuItem("US Maps", href="/page-2", id="page-2-link"),
                dbc.DropdownMenuItem("World View", href="/page-3", id="page-3-link"),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Proteins", header=True),
                        dbc.DropdownMenuItem("5RE4", href="/page-4", id="page-4-link"),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("6VXX", href="/page-6", id="page-6-link"),
                    ],
                    in_navbar=True,
                    direction="left",
                    label="3D Viewer",
                    color="link",
                    bs_size="small",
                ),
                dbc.DropdownMenuItem("Prediction Models", href="/page-5", id="page-5-link"),
            ],
            nav=True,
            in_navbar=True,
            label="Menu",
            direction="right",
            color="info",
            bs_size="large",
        ),
    )
],
    align="right",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src="https://i.imgur.com/WxEvNHv.png",
                                height="50px"
                            )
                        ),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "COVID-19 OUTBREAK VISUALIZATION TOOL",
                                className="m1-2",
                                href="https://covid19-outbreak-vis.herokuapp.com",
                            )
                        ),
                        dbc.Col(
                            html.Img(
                                src="https://i.imgur.com/qGvKrmj.gif",
                                height="30px"
                            )
                        )
                    ],
                    align="left",
                    no_gutters=True,

                ),
            ),
            dbc.NavbarToggler(
                id="navbar-toggler"
            ),
            dbc.Collapse(
                dbc.Nav(
                    [dropdown],
                    pills=True,
                    className="m1-auto",
                    justified=True,
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
            dbc.Col(
                dbc.Button("Our GitHub Repo", href="https://github.com/ThanatoSohne/COVID-19-Visual-Tool",
                           outline=True, color="warning", size="sm", className="mr-1")
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-6",
    sticky="top",
    style={
        "padding": "10px"
    },
)

page1_card1 = [

    dbc.CardHeader("#HelpStopTheSpread", style={'font-family': 'Avantgarde',
                                                'font-variant': 'small-caps'}),
    dbc.CardBody(
        [
            html.H4("Together we can overcome",
                    style={
                        'font-family': 'fangsong',
                        'text-align': 'center',
                        'text-size': '16px'
                    }),
            html.P(
                [
                    html.Ul(
                        children=[
                            html.Li("Remember to wash your hands periodically for at least 20 seconds"),
                            html.Li("Avoid touching your face as much as possible"),
                            html.Li("Always keep a good social distance from others while in public"),
                            html.Li("Do these things to save yourself, your loved ones, and those around you"),
                        ],
                        style={
                            'font-family': 'Book Antiqua',
                            'font-size': '12px',
                            'font-style': 'normal'
                        },
                    ),
                ]

            ),
        ]
    ),
]

page1_card2 = dbc.CardBody(
    [
        html.Blockquote(
            [
                html.P(
                    """You may encounter many defeats, but you must not be defeated. 
                    In fact, it may be necessary to encounter the defeats, so you can know who you are, 
                    what you can rise from, how you can still come out of it.""",
                    style={
                        "font-family": "American Typewriter",
                        "font-weight": "bold",
                        "font-style": "italic",
                    },
                ),
                html.Footer(
                    html.Strong("Maya Angelou",
                                style={
                                    "font-family": "Brush Script MT, Brush Script Std, cursive",
                                    "font-variant": "small-caps",
                                    "text-align": "center",
                                })
                ),
            ],
            className="blockquote",
        )
    ]
)

page1_card3 = [
    dbc.CardImg(src="https://i.imgur.com/Ddq82cf.png", top=True),
    dbc.CardBody(
        [
            html.H5("Remember these simple facts", className="card-title"),
            dbc.Button("Zoomable view provided by zoomable.ca",
                       color="light",
                       size="sm",
                       external_link="True",
                       block="True",
                       href="https://srv2.zoomable.ca/viewer.php?i=img881cb6eab2ea3665_Protecting_yourself_and_your_loved_ones_from_covid_19"),
        ]
    ),
]

page1_card4 = [
    dbc.CardImg(src="https://i.imgur.com/9rzkj5d.png", top=True),
    dbc.CardBody(
        [
            html.P("Structure of novel coronavirus spike receptor-binding domain complexed with its receptor ACE2",
                   className="card-title")
        ]
    ),
]

page1_card5 = [
    dbc.CardImg(src="https://i.imgur.com/QrVTseP.png", top=True),
    dbc.CardBody(
        [
            html.P("Structure of the SARS-CoV-2 spike glycoprotein (closed state)", className="card-title")
        ]
    ),
]

page1_card6 = [
    dbc.CardHeader("CDC's COVID-19 Self-Checker", style={'font-family': 'Avantgarde',
                                                         'font-variant': 'small-caps'}),
    dbc.CardBody(
        [
            html.H4("This is simply to help you in deciding whether you need to seek further medical assistance",
                    style={
                        'font-family': 'fangsong',
                        'text-align': 'center',
                        'text-size': '16px'
                    }),
            dbc.Button("CDC Self Checker",
                       color="light",
                       size="lg",
                       external_link="False",
                       block="True",
                       href="https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/index.html#cdc-chat-bot-open"),
        ]
    ),
]

page1_card7 = [
    dbc.CardImg(
        src="https://i.imgur.com/U1doCT1.jpg",
        top=True,
        style={
            "height": "100%",
        },
    ),
    dbc.CardBody(
        [
            html.H5("Let us not forget the sacrifices made by the doctors and healthcare workers on the frontlines",
                    className="card-title"),
            dbc.Button("Zoomable view provided by zoomable.ca",
                       color="light",
                       size="sm",
                       external_link="False",
                       block="True",
                       href="https://srv2.zoomable.ca/viewer.php?i=imge0b92f57b34150e3_earlyDays"),
        ]
    ),
]

page1_card8 = [
    dbc.CardImg(
        src="https://www.who.int/images/default-source/health-topics/coronavirus/social-media-squares/be-ready-social-2.jpg",
        top=True,
        style={
            "height": "auto%",
        },
    ),
    dbc.CardBody(
        [
            html.H5("Be kind to one another", className="card-title"),
            dbc.Button("WHO Source",
                       color="light",
                       size="sm",
                       external_link="True",
                       block="True",
                       href="https://www.who.int/images/default-source/health-topics/coronavirus/social-media-squares/be-ready-social-2.jpg"),
        ]
    ),
]

page1_card9 = [
    dbc.CardHeader("Self-Care is Truly Essential", style={'font-family': 'Avantgarde',
                                                          'font-variant': 'small-caps',
                                                          'font-stretch': 'semi-expanded'}),
    dbc.CardBody(
        [
            dbc.ListGroup([
                dbc.ListGroupItem("Imgur's Feel Good Moments", href="https://imgur.com/t/uplifting", color="secondary"),
                dbc.ListGroupItem(
                    "Take a break from the constant news dealing with COVID-19 and read a book or listen to music.",
                    color="info"),
                dbc.ListGroupItem(
                    html.Embed(src="https://www.youtube.com/embed/-kcOpyM9cBg",
                               height="auto",
                               width="100%"),
                    color="warning"),
                dbc.ListGroupItem("Take a moment to call, text, or Skype a loved one, a neighbor, or a friend.",
                                  color="primary"),
                dbc.ListGroupItem("Sometimes we need a little bit of quiet. Try some meditations at Headspace.",
                                  href="https://www.headspace.com/covid-19", color="warning"),
                dbc.ListGroupItem("Always remember to be kind to yourself and others.", color="secondary"),
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading("Happy Playlist for These Tough Times"),
                        html.Embed(src="https://www.youtube.com/embed/videoseries?list=PL7eGsz72w679_8u2NEz4Ag3YyqPjxYtlb",
                                   height="auto",
                                   width="100%"),
                    ]
                ),
            ]
            ),
        ]
    ),
]

page1_card10 = dbc.CardBody(
    [
        html.Blockquote(
            [
                html.P(
                    """Keep informed on the FACTS of COVID-19. This way you can help
                    to squash rumors that you come across thus stemming the tide
                    of undue hatred, reckless behavior, and -ultimately- save lives.""",
                    style={
                        "font-family": "American Typewriter",
                        "font-weight": "bold",
                        "font-style": "italic",
                    },
                ),
                dbc.Button("CDC's COVID-19 Homepage",
                           color="info",
                           size="sm",
                           external_link="True",
                           block="True",
                           href="https://www.cdc.gov/coronavirus/2019-nCoV/index.html"),

            ],
            className="blockquote",
        )
    ]
)


mason = dbc.CardColumns(
    [
        dbc.Card(page1_card7, color="dark", outline=True),
        dbc.Card(page1_card5, color="secondary", inverse=False),
        dbc.Card(page1_card9, color="primary", outline=True),
        dbc.Card(page1_card2, color="info", inverse=True, body=True),
        dbc.Card(page1_card1, color="warning", inverse=False),
        dbc.Card(page1_card8, color="dark", outline=True),
        dbc.Card(page1_card6, color="secondary", inverse=False),
        dbc.Card(page1_card4, color="success", outline=True),
        dbc.Card(page1_card3, color="dark", outline=True),
        dbc.Card(page1_card10, color="warning", outline=True),
        ###So on and so forth....
    ]
)

slow = html.Div(
    [
        dbc.Button(
            "Click here, please!",
            id="auto-toast-toggle",
            color="warning",
            className="mb-3",
        ),
        dbc.Toast(
            [html.P("The maps may be a little slow in rendering", className="mb-0")],
            id="auto-toast",
            header="We apologize and thank you for your patience",
            icon="primary",
            duration=4000,
        ),
    ]
)

us_map = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("Mapped Visuals of COVID-19's Virulent Spread Here in the US",
                                        style={
                                            "position": "relative",
                                            "text-align": "center"
                                        }),
                                #                               html.Br(),
                                html.P(
                                    """\
                                        The maps to the right are broken down into a state by state basis, wherein one can see
                                        the overall reach COVID-19 has had within our communities here in the US. Some maps will 
                                        have a few counties missing due to either those counties not having cases or because their
                                        numbers have yet to be reported. All data scraped in order to build these sites come from a 
                                        range of sources that had the most reliable and most current of information. You can
                                        view these on our GitHub repo within the Scrapers or Scraped Docs page.""",
                                    style={'border': '4mm ridge rgba(28, 106, 128,.6)',
                                           'outline': '0.5rem rgba(222, 109, 89,.7)',
                                           'font-family': 'Goudy Old Style, Garamond, Big Caslon, Times New Roman, serif',
                                           'font-size': '14px',
                                           'font-style': 'normal',
                                           'font-variant': 'small-caps',
                                           'font-weight': '700',
                                           'line-height': '20px',
                                           'padding': '1rem'})],
                            md=4,
                            width="auto"
                        ),
                        dbc.Col(
                            [
                                html.H3("US Maps on a State by State Basis"),
                                slow,
                                dcc.Dropdown(
                                    id="map_menu",
                                    options=states,
                                    value="AK"
                                ),
                                dcc.Graph(
                                    id='map',
                                    style={
                                        'width': 'auto',
                                        'height': 'auto',
                                        'display': 'block',
                                        'position': 'relative',
                                        'border': '3px solid grey',
                                        'padding': '10px'
                                    }
                                ),
                            ],
                            md=8,
                            width="auto"
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="table"
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
)

mundiMap = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("The Absolute Immensity of the Infection",
                                        style={
                                            "position": "relative",
                                            "text-align": "center"
                                        }),
                                html.P("""\
                                The maps and graphs on this page showcases the devastation of COVID-19
                                purely in way of visuals and numbers. The data used was scraped from both the 
                                ECDC and the WorldMeters site. Both have a comprehensive and extensive list
                                of data and graphs that go into further detail about COVID-19. Please do 
                                take the time to visit their site! 
                                """,
                                       style={'border': '4mm ridge rgba(116, 163, 114,.6)',
                                              'outline': '0.5rem rgba(222, 109, 89,.7)',
                                              'font-family': 'Goudy Old Style, Garamond, Big Caslon, Times New Roman, serif',
                                              'font-size': '14px',
                                              'font-style': 'normal',
                                              'font-variant': 'small-caps',
                                              'font-weight': '700',
                                              'line-height': '20px',
                                              'padding': '1rem'}
                                       )
                            ],
                            md=4,
                            width="auto"
                        ),
                        dbc.Col(
                            [
                                html.H3("We Are All in This Together!"),
                                dcc.Graph(
                                    figure=mundiScatter(),
                                    style={
                                        'width': 'auto',
                                        'height': 'auto',
                                        'display': 'block',
                                        'position': 'relative',
                                        'border': '3px solid grey'
                                        # 'padding': '5px'
                                    }
                                ),
                            ],
                            md=8,
                            width="auto"
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Span(
                                    [
                                        dbc.Badge("Press 'play' and Wait for it....", pill=True, color="dark",
                                                  className="mr-1"),
                                    ]
                                ),
                                dcc.Graph(
                                    figure=aniGlobe()
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
)

sarsView = html.Div(
    [
        dbc.Row(
            [
                html.Embed(
                    height=1000,
                    width=1200,
                    src=(f'https://mateov97.github.io/Molecule/')
                ),
            ]
        ),

    ]
)

sarsView2 = html.Div(
    [
        dbc.Row(
            [
                html.Iframe(
                    height=1000,
                    width=1200,
                    src=(f'https://mateov97.github.io/Molecule2/')
                ),
            ]
        ),
        # dbc.Row(
        #     [
        #         html.Embed(
        #             height="600px",
        #             width="600px",
        #             src="https://embed.molview.org/v1/?mode=vdw&pdbid=6LXT&chainType=ribbon&chainColor=residue"
        #         ),
        #     ]
        # ),

    ]
)

oracle = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        html.Header("A Peek into the Future of COVID-19 in Our Lives",
                                    style={
                                        "font-family": "Bookman Old Style",
                                        "font-variant": "small-caps",
                                        "font-weight": "600",
                                        "font-style": "oblique",
                                        "text-align": "center",
                                        "padding": "10px",
                                        "font-size": "300%",
                                        "margin-left": "auto",
                                        "margin-right": "auto",
                                    }),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(
                                    figure=mortModel(),
                                    style={
                                        "width": "auto",
                                    }
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    figure=recModel(),
                                    style={
                                        "width": "auto",
                                    }
                                ),
                            ]
                        ),
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        html.Header("COVID-19's Global Regression",
                                    style={
                                        "font-family": "Bookman Old Style",
                                        "font-variant": "small-caps",
                                        "font-weight": "600",
                                        "font-style": "oblique",
                                        "text-align": "center",
                                        "padding": "10px",
                                        "font-size": "150%",
                                        "margin-left": "auto",
                                        "margin-right": "auto",
                                    }
                                    ),
                        html.P("""\
                                Our prediction models on this page use machine learning to train the United States 
                                time series data for confirmed cases against the data for recoveries and deaths 
                                in two separate data frames.  
                                The prediction line, shown and demarcated in the legend, gives a 
                                representation for the most probable ratio of deaths and recoveries 
                                (in the model for recoveries) for any number of confirmed cases and 
                                it is shown against the line representing a sample of the actual cases 
                                from the dataset that we used. The models to below takes the data from the what
                                is observed in the model above, particularly those dealing with confirmed cases over
                                deaths in the US and extends the outlook to a particular country from every continent.
                                """,
                                   style={'border': '4mm ridge rgba(144, 96, 181,.6)',
                                          'outline': '0.5rem rgba(237, 245, 122,.7)',
                                          'font-family': 'Goudy Old Style, Garamond, Big Caslon, Times New Roman, serif',
                                          'font-size': '18px',
                                          'font-style': 'normal',
                                          'font-variant': 'small-caps',
                                          'font-weight': '700',
                                          'line-height': '20px',
                                          'padding': '1rem'}
                                ),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="oracle_menu",
                                    options=oracle_country,
                                    value="ITA",
                                ),
                                dcc.Graph(
                                    id='oracle',
                                    style={
                                        "width": "auto",
                                    }
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div(
    [dcc.Location(id="url", refresh=True), navbar, content]
)


# we use a callback to toggle the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


app.callback(
    Output(f"navbar-collapse", "is_open"),
    [Input(f"navbar-toggler", "n_clicks")],
    [State(f"navbar-collapse", "is_open")],
)(toggle_navbar_collapse)


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        return True, False, False
    return [pathname == f"page-{i}" for i in range(1, 6)]


@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return mason
    elif pathname == "/page-2":
        return us_map
    elif pathname == "/page-3":
        return mundiMap
    elif pathname == "/page-4":
        return sarsView
    elif pathname == "/page-5":
        return oracle
    elif pathname == "/page-6":
        return sarsView2
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P("Pathname {pathname} was not recognized... Oopss..")
        ]
    )


@app.callback(
    Output("auto-toast", "is_open"), [Input("auto-toast-toggle", "n_clicks")]
)
def open_toast(n):
    return True


@app.callback(
    Output("map", "figure"),
    [Input("map_menu", "value")]
)
def build_map(value):
    if value == 'AK':
        return akmap()
    elif value == 'AL':
        return almap()
    elif value == 'AR':
        return armap()
    elif value == 'AZ':
        return azmap()
    elif value == 'CA':
        return camap()
    elif value == 'CO':
        return comap()
    elif value == 'CT':
        return ctmap()
    elif value == 'DE':
        return demap()
    elif value == 'FL':
        return flmap()
    elif value == 'GA':
        return gamap()
    elif value == 'HI':
        return himap()
    elif value == 'ID':
        return idmap()
    elif value == 'IL':
        return ilmap()
    elif value == 'IN':
        return inmap()
    elif value == 'IO':
        return iomap()
    elif value == 'KA':
        return kamap()
    elif value == 'KY':
        return kymap()
    elif value == 'LA':
        return lamap()
    elif value == 'MA':
        return mamap()
    elif value == 'MD':
        return mdmap()
    elif value == 'ME':
        return memap()
    elif value == 'MI':
        return mimap()
    elif value == 'MN':
        return mnmap()
    elif value == 'MO':
        return momap()
    elif value == 'MS':
        return msmap()
    elif value == 'MT':
        return mtmap()
    elif value == 'NC':
        return ncmap()
    elif value == 'ND':
        return ndmap()
    elif value == 'NE':
        return nemap()
    elif value == 'NH':
        return nhmap()
    elif value == 'NJ':
        return njmap()
    elif value == 'NM':
        return nmmap()
    elif value == 'NV':
        return nvmap()
    elif value == 'NY':
        return nymap()
    elif value == 'OH':
        return ohmap()
    elif value == 'OK':
        return okmap()
    elif value == 'OR':
        return ormap()
    elif value == 'PA':
        return pamap()
    elif value == 'PR':
        return prmap()
    elif value == 'RI':
        return rimap()
    elif value == 'SC':
        return scmap()
    elif value == 'SD':
        return sdmap()
    elif value == 'TN':
        return tnmap()
    elif value == 'TX':
        return txmap()
    elif value == 'UT':
        return utmap()
    elif value == 'VA':
        return vamap()
    elif value == 'VT':
        return vtmap()
    elif value == 'WA':
        return wamap()
    elif value == 'WI':
        return wimap()
    elif value == 'WV':
        return wvmap()
    elif value == 'WY':
        return wymap()


@app.callback(
    Output("table", "figure"),
    [Input("map_menu", "value")]
)
def build_tables(value):
    if value == 'AK':
        return aksub()
    elif value == 'AL':
        return alsub()
    elif value == 'AR':
        return arsub()
    elif value == 'AZ':
        return azsub()
    elif value == 'CA':
        return casub()
    elif value == 'CO':
        return cosub()
    elif value == 'CT':
        return ctsub()
    elif value == 'DE':
        return desub()
    elif value == 'FL':
        return flsub()
    elif value == 'GA':
        return gasub()
    elif value == 'HI':
        return hisub()
    elif value == 'ID':
        return idsub()
    elif value == 'IL':
        return ilsub()
    elif value == 'IN':
        return insub()
    elif value == 'IO':
        return iosub()
    elif value == 'KA':
        return kasub()
    elif value == 'KY':
        return kysub()
    elif value == 'LA':
        return lasub()
    elif value == 'MA':
        return masub()
    elif value == 'MD':
        return mdsub()
    elif value == 'ME':
        return mesub()
    elif value == 'MI':
        return misub()
    elif value == 'MN':
        return mnsub()
    elif value == 'MO':
        return mosub()
    elif value == 'MS':
        return mssub()
    elif value == 'MT':
        return mtsub()
    elif value == 'NC':
        return ncsub()
    elif value == 'ND':
        return ndsub()
    elif value == 'NE':
        return nesub()
    elif value == 'NH':
        return nhsub()
    elif value == 'NJ':
        return njsub()
    elif value == 'NM':
        return nmsub()
    elif value == 'NV':
        return nvsub()
    elif value == 'NY':
        return nysub()
    elif value == 'OH':
        return ohsub()
    elif value == 'OK':
        return oksub()
    elif value == 'OR':
        return orsub()
    elif value == 'PA':
        return pasub()
    elif value == 'PR':
        return prsub()
    elif value == 'RI':
        return risub()
    elif value == 'SC':
        return scsub()
    elif value == 'SD':
        return sdsub()
    elif value == 'TN':
        return tnsub()
    elif value == 'TX':
        return txsub()
    elif value == 'UT':
        return utsub()
    elif value == 'VA':
        return vasub()
    elif value == 'VT':
        return vtsub()
    elif value == 'WA':
        return wasub()
    elif value == 'WI':
        return wisub()
    elif value == 'WV':
        return wvsub()
    elif value == 'WY':
        return wysub()


@app.callback(
    Output("oracle", "figure"),
    [Input("oracle_menu", "value")]
)
def oracle_model(value):
    if value == 'ITA':
        return italiaModel()
    elif value == 'NZ':
        return newZeaModel()
    elif value == 'SA':
        return southAfricaModel()
    elif value == 'SK':
        return skoreaModel()
    elif value == 'BRZ':
        return brazilModel()


if __name__ == "__main__":
    app.run_server(debug=True)
